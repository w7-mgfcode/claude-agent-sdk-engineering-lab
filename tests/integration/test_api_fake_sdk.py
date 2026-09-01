from fastapi.testclient import TestClient

from claude_agent_lab.api import app, get_gateway
from claude_agent_lab.errors import AgentTimeoutError, AgentUpstreamError
from claude_agent_lab.models import AgentResult


class FakeGateway:
    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> AgentResult:
        assert prompt == "Hello"
        assert model == "claude-test"
        assert system_prompt == "Be concise"
        return AgentResult(text="Hi from fake Claude", total_cost_usd=0.01, num_turns=1)


class TimeoutGateway:
    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> AgentResult:
        raise AgentTimeoutError("fake timeout")


class UpstreamErrorGateway:
    async def complete(
        self,
        prompt: str,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> AgentResult:
        raise AgentUpstreamError("fake upstream error")


def test_chat_completion_contract_without_live_credentials() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [
                    {"role": "system", "content": "Be concise"},
                    {"role": "user", "content": "Hello"},
                ],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["object"] == "chat.completion"
    assert body["choices"][0]["message"] == {
        "role": "assistant",
        "content": "Hi from fake Claude",
    }
    assert body["usage"]["num_turns"] == 1
    assert response.headers["x-request-id"].startswith("req_")


def test_streaming_is_explicitly_rejected() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": True,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    assert "not implemented" in response.json()["detail"]


def test_timeout_maps_to_504() -> None:
    app.dependency_overrides[get_gateway] = lambda: TimeoutGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "user", "content": "Hello"}],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 504
    assert response.json()["type"] == "upstream_timeout"


def test_upstream_error_maps_to_502() -> None:
    app.dependency_overrides[get_gateway] = lambda: UpstreamErrorGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "user", "content": "Hello"}],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json()["type"] == "upstream_sdk_error"


def test_multiple_system_messages_rejected() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [
                    {"role": "system", "content": "System 1"},
                    {"role": "system", "content": "System 2"},
                    {"role": "user", "content": "Hello"},
                ],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    assert "at most one system message" in response.json()["detail"]


def test_empty_conversation_rejected() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "system", "content": "Be concise"}],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    assert "at least one user/assistant message" in response.json()["detail"]


def test_blank_message_content_rejected() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "user", "content": "   "}],
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_temperature_is_explicitly_rejected() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.7,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    assert "temperature is not implemented" in response.json()["detail"]


def test_forbidden_extra_fields_rejected() -> None:
    app.dependency_overrides[get_gateway] = lambda: FakeGateway()
    client = TestClient(app)
    try:
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "claude-test",
                "messages": [{"role": "user", "content": "Hello"}],
                "unsupported_field": "some_value",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
