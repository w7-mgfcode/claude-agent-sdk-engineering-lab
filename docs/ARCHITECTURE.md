# Architecture

## Design objective

Keep Claude Agent SDK integration visible while still showing application engineering around it.

## Boundaries

### Example/application layer
Owns CLI UX, HTTP validation, timeout policy, dependency injection, local non-secret session metadata, and stable error responses.

### Claude Agent SDK layer
Owns the agent protocol, `query()`/`ClaudeSDKClient`, SDK messages, session semantics exposed by the SDK, and MCP/tool dispatch integration.

### Claude runtime/service
Owns model inference and provider-side behavior.

## Runtime flows

### One shot

```mermaid
sequenceDiagram
    actor U as User
    participant E as Example 01
    participant G as ClaudeAgentGateway
    participant S as Claude Agent SDK query()
    participant C as Claude
    U->>E: prompt
    E->>G: complete(prompt)
    G->>S: query(prompt, options)
    S->>C: agent execution
    C-->>S: message stream
    S-->>G: AssistantMessage / ResultMessage
    G-->>E: AgentResult
    E-->>U: text + safe metadata
```

### Interactive session

```mermaid
sequenceDiagram
    actor U as User
    participant CLI as Terminal CLI
    participant SDK as ClaudeSDKClient
    U->>CLI: prompt
    CLI->>SDK: await client.query(prompt)
    loop response messages
        SDK-->>CLI: receive_response()
    end
    CLI-->>U: assistant text
    CLI->>CLI: store session ID only
```

### FastAPI

The HTTP layer depends on a `CompletionGateway` protocol. Production runtime resolves it to `ClaudeAgentGateway`; tests override it with deterministic fakes. This demonstrates dependency injection without hiding the actual SDK implementation.

## OpenAI compatibility boundary

The server supports only:

- one request endpoint: `POST /v1/chat/completions`;
- roles: system/user/assistant;
- non-streaming response;
- one assistant choice;
- model passed through to the SDK;
- optional cost/turn metadata when trustworthy.

`stream=true` and `temperature` are rejected in v1 rather than ignored.
