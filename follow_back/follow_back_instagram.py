#!/usr/bin/env python3
"""Print accounts from an Instagram export that do not follow back.

Pass the HTML files downloaded from Instagram's *Download your information*
export, or place ``following.html`` and ``followers.html`` next to this file.
"""

import argparse
from pathlib import Path

from bs4 import BeautifulSoup


def read_usernames(filename: Path) -> set[str]:
    """Return usernames linked by an Instagram export HTML file.

    Instagram exports use one anchor per account.  Reading the anchor text,
    rather than iterating over its children, also works when an anchor contains
    formatting tags or whitespace.
    """
    try:
        document = filename.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Instagram export file not found: {filename}") from exc

    soup = BeautifulSoup(document, "html.parser")
    return {
        anchor.get_text(strip=True)
        for anchor in soup.find_all("a", target="_blank")
        if anchor.get_text(strip=True)
    }


def accounts_not_following_back(following_file: Path, followers_file: Path) -> list[str]:
    """Return sorted accounts followed by the user but absent from followers."""
    return sorted(read_usernames(following_file) - read_usernames(followers_file), key=str.casefold)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Find Instagram accounts that do not follow back")
    parser.add_argument("--following", type=Path, default=script_dir / "following.html")
    parser.add_argument("--followers", type=Path, default=script_dir / "followers.html")
    args = parser.parse_args()

    accounts = accounts_not_following_back(args.following, args.followers)
    print("The usernames below don't follow you back:\n")
    print("\n".join(accounts))
    print(f"\nTotal users who don't follow you back = {len(accounts)}")


if __name__ == "__main__":
    main()
