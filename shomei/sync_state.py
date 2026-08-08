"""Persistent state for incremental shōmei synchronizations.

The state file contains source commit hashes and the corresponding mirror
commit hashes.  It deliberately does not contain commit messages, paths, or
any other source-repository content.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_VERSION = 1
STATE_DIRECTORY = ".shomei"
STATE_FILENAME = "state.json"


class SyncStateError(RuntimeError):
    """Raised when the local sync state cannot be read or written safely."""


def get_state_path(repo_root: Path | None = None) -> Path:
    """Return the state path for a source repository."""

    root = repo_root or Path.cwd()
    return root / STATE_DIRECTORY / STATE_FILENAME


def _new_state() -> dict[str, Any]:
    return {"version": STATE_VERSION, "syncs": {}}


def load_state(path: Path) -> dict[str, Any]:
    """Load state from *path*, returning an empty state when it is absent."""

    if not path.exists():
        return _new_state()

    try:
        with path.open("r", encoding="utf-8") as state_file:
            state = json.load(state_file)
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncStateError(f"couldn't read sync state at {path}: {exc}") from exc

    if not isinstance(state, dict) or state.get("version") != STATE_VERSION:
        raise SyncStateError(
            f"unsupported or invalid sync state at {path}; "
            "remove it only if you are willing to mirror the history again"
        )
    if not isinstance(state.get("syncs"), dict):
        raise SyncStateError(f"invalid sync state at {path}: 'syncs' must be an object")

    return state


def _source_key(source_repository: str, author_email: str) -> str:
    """Build a stable, unambiguous key for one source/email pair."""

    return json.dumps(
        {"author_email": author_email, "source_repository": source_repository},
        sort_keys=True,
        separators=(",", ":"),
    )


def get_sync_record(
    state: dict[str, Any],
    target: str,
    source_repository: str,
    author_email: str,
) -> dict[str, Any]:
    """Return the mutable state record for one source and mirror target."""

    syncs = state.setdefault("syncs", {})
    target_state = syncs.setdefault(target, {"sources": {}})
    if not isinstance(target_state, dict):
        raise SyncStateError(f"invalid state for mirror target {target}")

    sources = target_state.setdefault("sources", {})
    if not isinstance(sources, dict):
        raise SyncStateError(f"invalid source state for mirror target {target}")

    source_key = _source_key(source_repository, author_email)
    record = sources.setdefault(
        source_key,
        {
            "source_repository": source_repository,
            "author_email": author_email,
            "commits": {},
        },
    )
    if not isinstance(record, dict):
        raise SyncStateError(f"invalid source state for mirror target {target}")

    commits = record.setdefault("commits", {})
    if not isinstance(commits, dict):
        raise SyncStateError(f"invalid commit state for mirror target {target}")

    return record


def mark_commit_synced(
    state: dict[str, Any],
    target: str,
    source_repository: str,
    author_email: str,
    source_commit_hash: str,
    commit_date: datetime,
    mirror_commit_sha: str | None,
) -> None:
    """Record a source commit after its mirror branch has been updated."""

    record = get_sync_record(state, target, source_repository, author_email)
    record["commits"][source_commit_hash] = {
        "date": commit_date.isoformat(),
        "mirror_sha": mirror_commit_sha,
    }
    record["last_synced_at"] = datetime.now(timezone.utc).isoformat()


def save_state(path: Path, state: dict[str, Any]) -> None:
    """Atomically save state so an interrupted write cannot corrupt it."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None

    try:
        file_descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as state_file:
            json.dump(state, state_file, ensure_ascii=False, indent=2, sort_keys=True)
            state_file.write("\n")
            state_file.flush()
            os.fsync(state_file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    except OSError as exc:
        raise SyncStateError(f"couldn't save sync state at {path}: {exc}") from exc
    finally:
        if temporary_path:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass
