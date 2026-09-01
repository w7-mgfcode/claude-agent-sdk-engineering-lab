# Movement 02 — SSE Streaming & Async Task Cancellation Boundary

## Objective

Implement real-time Server-Sent Events (SSE) streaming on the FastAPI `/v1/chat/completions` endpoint (`stream: true`), coupled with graceful client-disconnect task cancellation to prevent compute and token waste.

---

## Architectural Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client as HTTP Client / Frontend
    participant API as FastAPI Router (/v1/chat/completions)
    participant Adapter as SDK Adapter (ClaudeAgentGateway)
    participant SDK as Claude Agent SDK (query / iterator)

    Client->>API: POST /v1/chat/completions {"stream": true, ...}
    API->>Adapter: stream_complete(messages, options)
    Adapter->>SDK: query(prompt, options) (async generator)
    
    loop Stream Chunks
        SDK-->>Adapter: Yield TextBlock / Message Delta
        Adapter-->>API: Yield ChatCompletionChunk (Pydantic)
        API-->>Client: data: {"id":..., "choices":[{"delta":{"content":"..."}}]}\n\n
    end

    alt Client Disconnects Mid-Stream
        Client--xAPI: TCP Connection Dropped
        API->>Adapter: Cancel generator / Task
        Adapter->>SDK: Abort execution cleanly
    else Successful Stream End
        API-->>Client: data: [DONE]\n\n
    end
```

---

## Implementation Tasks

### 1. Schema & Request Models
- Update `ChatCompletionRequest` in [src/claude_agent_lab/api_models.py](../../src/claude_agent_lab/api_models.py):
  - Allow `stream: bool = False`.
  - Add `ChatCompletionChunk` and `ChatCompletionChunkChoice` models matching OpenAI streaming chunk specs.

### 2. Adapter Streaming Method
- Add `stream_complete()` method in [src/claude_agent_lab/sdk_adapter.py](../../src/claude_agent_lab/sdk_adapter.py):
  - Consumes SDK async message stream.
  - Yields structured text delta tokens.
  - Handles `asyncio.CancelledError` gracefully.

### 3. FastAPI SSE Endpoint with Disconnect Detection
- Update [src/claude_agent_lab/api.py](../../src/claude_agent_lab/api.py):
  - Return `StreamingResponse(..., media_type="text/event-stream")` when `stream=True`.
  - Monitor `request.is_disconnected()` in the streaming generator loop to trigger immediate SDK task cancellation.

### 4. Fake Gateway & Test Suite
- Expand `FakeClaudeGateway` in [tests/integration/test_api_fake_sdk.py](../../tests/integration/test_api_fake_sdk.py):
  - Implement async stream generator mock.
  - Add integration tests verifying chunk structure, `[DONE]` terminator, and simulated disconnect cancellation.

---

## Definition of Done

- [ ] `POST /v1/chat/completions` with `"stream": true` returns valid SSE chunks.
- [ ] Dropping client connection aborts active background async tasks immediately.
- [ ] Integration tests in `tests/integration/test_api_fake_sdk.py` verify full streaming and cancellation paths.
- [ ] `make verify` passes with strict typing and no linter warnings.
