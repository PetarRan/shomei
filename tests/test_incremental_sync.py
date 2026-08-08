from datetime import datetime, timedelta, timezone
import importlib

from click.testing import CliRunner

from shomei.sync_state import (
    get_sync_record,
    load_state,
    mark_commit_synced,
    save_state,
)
from shomei.github_api import _github_date


cli_module = importlib.import_module("shomei.cli")


def _commit(commit_hash, day):
    return {
        "hash": commit_hash,
        "date": datetime(2025, 1, day, 12, tzinfo=timezone.utc),
    }


def test_sync_state_round_trip_records_source_and_mirror_hashes(tmp_path):
    state_path = tmp_path / ".shomei" / "state.json"
    state = load_state(state_path)

    mark_commit_synced(
        state,
        "me/work-mirror",
        "https://github.com/company/work.git",
        "work@example.com",
        "source-1",
        _commit("source-1", 1)["date"],
        "mirror-1",
    )
    save_state(state_path, state)

    loaded = load_state(state_path)
    record = get_sync_record(
        loaded,
        "me/work-mirror",
        "https://github.com/company/work.git",
        "work@example.com",
    )
    assert record["commits"] == {
        "source-1": {
            "date": "2025-01-01T12:00:00+00:00",
            "mirror_sha": "mirror-1",
        }
    }


def test_legacy_timestamp_matching_preserves_duplicate_commits():
    source_commits = [_commit("source-1", 1), _commit("source-2", 1), _commit("source-3", 2)]
    mirrored_dates = [
        datetime(2025, 1, 1, 12, tzinfo=timezone.utc),
        datetime(2025, 1, 1, 12, tzinfo=timezone.utc),
    ]

    new_commits, already_mirrored = cli_module._split_legacy_mirror_commits(
        source_commits,
        mirrored_dates,
    )

    assert [commit["hash"] for commit in already_mirrored] == ["source-1", "source-2"]
    assert [commit["hash"] for commit in new_commits] == ["source-3"]


def test_github_dates_are_serialized_in_utc():
    local_date = datetime(2025, 1, 1, 12, tzinfo=timezone(timedelta(hours=1)))
    assert _github_date(local_date) == "2025-01-01T11:00:00Z"


def test_cli_only_mirrors_new_commits_on_later_runs(monkeypatch, tmp_path):
    commits = [_commit("source-1", 1), _commit("source-2", 2)]
    created = []
    parent_shas = []

    monkeypatch.setattr(cli_module, "validate_github_username", lambda _: (True, "ok"))
    monkeypatch.setattr(cli_module, "validate_github_token", lambda _: (True, None))
    monkeypatch.setattr(cli_module, "get_git_user_name", lambda: "Developer")
    monkeypatch.setattr(cli_module, "get_repo_name", lambda: "work")
    monkeypatch.setattr(cli_module, "get_git_root", lambda: str(tmp_path))
    monkeypatch.setattr(
        cli_module,
        "get_git_remote_url",
        lambda: "https://github.com/company/work.git",
    )
    monkeypatch.setattr(cli_module, "get_commits_by_author", lambda _: list(commits))
    monkeypatch.setattr(cli_module, "check_repo_exists", lambda *_: (True, True, None))
    monkeypatch.setattr(cli_module, "get_mirrored_commit_dates", lambda *_: [])
    monkeypatch.setattr(cli_module, "get_main_branch_sha", lambda *_: "remote-head")
    monkeypatch.setattr(cli_module, "time", type("NoSleep", (), {"sleep": staticmethod(lambda _: None)}))
    monkeypatch.setattr(cli_module, "update_branch_ref", lambda *_: True)
    monkeypatch.setattr(cli_module, "update_repo_readme", lambda *_: True)

    def fake_create_empty_commit(username, repo_name, date, token, parent_sha):
        created.append(date)
        parent_shas.append(parent_sha)
        return f"mirror-{len(created)}", None

    monkeypatch.setattr(cli_module, "create_empty_commit", fake_create_empty_commit)

    runner = CliRunner()
    args = [
        "--username", "me",
        "--repo-name", "work-mirror",
        "--token", "test-token",
        "--email", "work@example.com",
        "--non-interactive",
    ]

    first = runner.invoke(cli_module.cli, args)
    assert first.exit_code == 0, first.output
    assert len(created) == 2

    commits.append(_commit("source-3", 3))
    second = runner.invoke(cli_module.cli, args)
    assert second.exit_code == 0, second.output
    assert len(created) == 3
    assert "1 new commits" in second.output

    third = runner.invoke(cli_module.cli, args)
    assert third.exit_code == 0, third.output
    assert len(created) == 3
    assert "already up to date" in third.output

    state = load_state(tmp_path / ".shomei" / "state.json")
    record = get_sync_record(
        state,
        "me/work-mirror",
        "https://github.com/company/work.git",
        "work@example.com",
    )
    assert set(record["commits"]) == {"source-1", "source-2", "source-3"}
    assert parent_shas == ["remote-head", "mirror-1", "remote-head"]
