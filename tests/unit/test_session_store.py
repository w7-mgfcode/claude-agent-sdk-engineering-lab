from pathlib import Path

from claude_agent_lab.session_store import LocalSessionStore, SessionMetadata


def test_session_metadata_round_trip(tmp_path: Path) -> None:
    store = LocalSessionStore(tmp_path / "session.json")
    metadata = SessionMetadata(session_id="abc-123", cwd="/tmp/repo")

    store.save(metadata)

    assert store.load() == metadata
    store.clear()
    assert store.load() is None


def test_corrupted_session_file_returns_none(tmp_path: Path) -> None:
    path = tmp_path / "session.json"
    path.write_text("{not-valid-json", encoding="utf-8")
    store = LocalSessionStore(path)
    assert store.load() is None


def test_missing_keys_in_session_file_returns_none(tmp_path: Path) -> None:
    path = tmp_path / "session.json"
    path.write_text('{"other_key": "val"}', encoding="utf-8")
    store = LocalSessionStore(path)
    assert store.load() is None
