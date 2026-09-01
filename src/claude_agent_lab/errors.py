class AgentLabError(RuntimeError):
    """Base exception for stable application-level error mapping."""


class AgentConfigurationError(AgentLabError):
    """Local configuration or authentication precondition failed."""


class AgentTimeoutError(AgentLabError):
    """A bounded agent operation exceeded the configured timeout."""


class AgentUpstreamError(AgentLabError):
    """The Claude Agent SDK or its transport returned an error."""
