from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SessionMetadata:
    session_id: str
    cwd: str


class LocalSessionStore:
    """Stores only non-secret convenience metadata for SDK session resume."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, metadata: SessionMetadata) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(metadata), indent=2), encoding="utf-8")

    def load(self) -> SessionMetadata | None:
        if not self.path.exists():
            return None
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return SessionMetadata(session_id=str(data["session_id"]), cwd=str(data["cwd"]))
        except (json.JSONDecodeError, KeyError, TypeError):
            return None

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)
