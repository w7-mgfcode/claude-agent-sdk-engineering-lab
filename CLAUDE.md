# CLAUDE.md

Read `AGENTS.md` first.

## Repository intent

This is a recruiter-reviewable skill demonstration for Claude Agent SDK + async Python + FastAPI. The ideal diff is small, typed, tested, and easy for a hiring manager to inspect.

## Implementation preferences

- Python 3.11+.
- Async-first on Claude Agent SDK boundaries.
- Pydantic models for HTTP contracts.
- Dependency injection at the FastAPI boundary.
- Conservative permissions and bounded time/cost.
- Unit/integration tests must not require live credentials.
- Prefer direct, explicit code over framework-heavy indirection.

## Do not

- silently accept unsupported OpenAI fields;
- swallow SDK errors;
- log credentials or raw private prompts;
- add production-scale claims without measured evidence;
- add a vector database or RAG just to make the repo larger.
