"""Generate assets/card-stats.svg from a GitHub user's public activity.

Usage:
    python scripts/generate_stats_card.py --user aayushpanda77
    python scripts/generate_stats_card.py --user aayushpanda77 --offline   # sample numbers, no network

Set GITHUB_TOKEN to avoid API rate limits (the workflow does this for you).
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from html import escape
from pathlib import Path

API = "https://api.github.com"
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "assets" / "card-stats.svg"


def _get(url: str) -> object:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-card"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310 - fixed https host
        return json.load(resp)


def fetch_stats(user: str) -> dict:
    """Collect simple public numbers for a user."""
    profile = _get(f"{API}/users/{user}")
    repos = _get(f"{API}/users/{user}/repos?per_page=100&type=owner")
    prs = _get(f"{API}/search/issues?q=is:pr+author:{user}+-user:{user}&per_page=1")
    return {
        "user": user,
        "repos": int(profile.get("public_repos", 0)),
        "followers": int(profile.get("followers", 0)),
        "stars": sum(int(r.get("stargazers_count", 0)) for r in repos),
        "upstream_prs": int(prs.get("total_count", 0)),
    }


def sample_stats(user: str) -> dict:
    return {"user": user, "repos": 0, "followers": 0, "stars": 0, "upstream_prs": 0}


def render_card(stats: dict) -> str:
    """Return the SVG text for a stats dict. Pure function, easy to test."""
    items = [
        ("Public repos", stats["repos"]),
        ("Stars earned", stats["stars"]),
        ("Upstream PRs", stats["upstream_prs"]),
        ("Followers", stats["followers"]),
    ]
    cells = []
    for i, (label, value) in enumerate(items):
        x = 24 + i * 118
        cells.append(
            f'<text x="{x}" y="86" class="num">{int(value)}</text>'
            f'<text x="{x}" y="108" class="lbl">{escape(label)}</text>'
        )
    user = escape(str(stats["user"]))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="140" '
        f'viewBox="0 0 500 140" role="img" aria-label="{user} GitHub activity summary">'
        "<style>"
        ".bg{fill:#0d1117;stroke:#30363d}"
        ".ttl{font:600 16px sans-serif;fill:#e6edf3}"
        ".num{font:700 26px sans-serif;fill:#58a6ff}"
        ".lbl{font:12px sans-serif;fill:#8b949e}"
        "</style>"
        '<rect class="bg" x="0.5" y="0.5" width="499" height="139" rx="10"/>'
        f'<text x="24" y="36" class="ttl">{user} · GitHub activity</text>'
        + "".join(cells)
        + "</svg>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--offline", action="store_true", help="use zeroed sample numbers")
    args = parser.parse_args()

    stats = sample_stats(args.user) if args.offline else fetch_stats(args.user)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_card(stats), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
