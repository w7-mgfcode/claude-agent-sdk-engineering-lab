.PHONY: setup simple cli tool hook api test lint format typecheck verify lock

setup:
	uv sync --all-groups

lock:
	uv lock

simple:
	uv run python examples/01_simple_query.py

cli:
	uv run python examples/02_terminal_cli.py

tool:
	uv run python examples/04_tool_use.py

hook:
	uv run python examples/05_permission_hook.py

api:
	uv run python examples/03_api_server.py

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run mypy src examples tests

verify: lint typecheck test
