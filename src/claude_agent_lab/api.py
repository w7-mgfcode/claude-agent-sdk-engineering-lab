from __future__ import annotations

import time
from typing import Annotated, Protocol
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from claude_agent_lab.api_models import (
    AssistantMessageResponse,
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    ErrorBody,
    Usage,
)
from claude_agent_lab.config import get_settings
from claude_agent_lab.errors import AgentTimeoutError, AgentUpstreamError
from claude_agent_lab.models import AgentResult
from claude_agent_lab.sdk_adapter import ClaudeAgentGateway


class CompletionGateway(Protocol):
    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> AgentResult: ...


def get_gateway() -> CompletionGateway:
    return ClaudeAgentGateway(get_settings())


def _to_sdk_prompt(request: ChatCompletionRequest) -> tuple[str, str | None]:
    system_messages = [m.content for m in request.messages if m.role == "system"]
    if len(system_messages) > 1:
        raise HTTPException(status_code=422, detail="v1 supports at most one system message")

    conversation = [m for m in request.messages if m.role != "system"]
    if not conversation:
        raise HTTPException(
            status_code=422, detail="at least one user/assistant message is required"
        )

    if len(conversation) == 1 and conversation[0].role == "user":
        prompt = conversation[0].content
    else:
        lines = ["Continue the following conversation and answer the final user message."]
        for message in conversation:
            lines.append(f"{message.role.upper()}: {message.content}")
        prompt = "\n\n".join(lines)

    return prompt, system_messages[0] if system_messages else None


app = FastAPI(
    title="Claude Agent SDK Engineering Lab",
    version="0.1.0",
    description="Small OpenAI-shaped compatibility subset backed by Claude Agent SDK.",
)


@app.middleware("http")
async def request_id_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    request_id = request.headers.get("x-request-id") or f"req_{uuid4().hex}"
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.exception_handler(AgentTimeoutError)
async def timeout_handler(request: Request, exc: AgentTimeoutError) -> JSONResponse:
    body = ErrorBody(
        error=str(exc),
        type="upstream_timeout",
        request_id=request.state.request_id,
    )
    return JSONResponse(status_code=504, content=body.model_dump())


@app.exception_handler(AgentUpstreamError)
async def upstream_handler(request: Request, exc: AgentUpstreamError) -> JSONResponse:
    body = ErrorBody(
        error=str(exc),
        type="upstream_sdk_error",
        request_id=request.state.request_id,
    )
    return JSONResponse(status_code=502, content=body.model_dump())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "claude-agent-sdk-engineering-lab"}


@app.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
    response_model_exclude_none=True,
)
async def chat_completions(
    payload: ChatCompletionRequest,
    gateway: Annotated[CompletionGateway, Depends(get_gateway)],
) -> ChatCompletionResponse:
    if payload.stream:
        raise HTTPException(status_code=422, detail="stream=true is not implemented in v1")
    if payload.temperature is not None:
        raise HTTPException(status_code=422, detail="temperature is not implemented in v1")

    prompt, system_prompt = _to_sdk_prompt(payload)
    result = await gateway.complete(
        prompt,
        model=payload.model,
        system_prompt=system_prompt,
    )

    usage = None
    if result.total_cost_usd is not None or result.num_turns is not None:
        usage = Usage(total_cost_usd=result.total_cost_usd, num_turns=result.num_turns)

    return ChatCompletionResponse(
        id=f"chatcmpl_{uuid4().hex}",
        created=int(time.time()),
        model=payload.model,
        choices=[
            Choice(
                message=AssistantMessageResponse(content=result.text),
            )
        ],
        usage=usage,
    )
