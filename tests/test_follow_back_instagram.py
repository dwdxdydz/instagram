from pathlib import Path

import pytest

from follow_back.follow_back_instagram import accounts_not_following_back, read_usernames


def write_export(path: Path, usernames: list[str]) -> None:
    links = "".join(f'<a target="_blank" href="https://instagram.com/{name}"> {name} </a>' for name in usernames)
    path.write_text(f"<html><body>{links}</body></html>", encoding="utf-8")


def test_accounts_not_following_back_is_sorted_and_deduplicated(tmp_path: Path) -> None:
    following = tmp_path / "following.html"
    followers = tmp_path / "followers.html"
    write_export(following, ["zoe", "Alice", "zoe", "bob"])
    write_export(followers, ["bob"])

    assert accounts_not_following_back(following, followers) == ["Alice", "zoe"]


def test_read_usernames_reports_missing_export_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Instagram export file not found"):
        read_usernames(tmp_path / "missing.html")
