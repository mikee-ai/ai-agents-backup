"""GitHub Trending Tracker

Run:
    python3 github_trending_tracker.py
Then open http://127.0.0.1:8090
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')

GITHUB_API_BASE = "https://api.github.com"
DEFAULT_LANGUAGE = "python"
DEFAULT_DAYS = 7
DEFAULT_LIMIT = 12


def _headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "github-trending-tracker",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_trending_repositories(language: str, days: int, limit: int) -> list[dict[str, Any]]:
    created_after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    query_parts = [f"created:>{created_after}"]
    if language and language.lower() != "all":
        query_parts.append(f"language:{language}")

    params = {
        "q": " ".join(query_parts),
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }

    response = requests.get(
        f"{GITHUB_API_BASE}/search/repositories",
        headers=_headers(),
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    items = response.json().get("items", [])
    repositories: list[dict[str, Any]] = []

    for repo in items:
        repositories.append(
            {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description") or "No description provided.",
                "url": repo.get("html_url"),
                "language": repo.get("language") or "Unknown",
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "open_issues": repo.get("open_issues_count", 0),
                "watchers": repo.get("watchers_count", 0),
                "owner": repo.get("owner", {}).get("login", "unknown"),
                "owner_avatar": repo.get("owner", {}).get("avatar_url"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "topics": repo.get("topics", []),
            }
        )

    return repositories


@app.route("/")
def index() -> str:
    return render_template("github_trending_tracker.html")


@app.route("/api/trending")
def trending() -> Any:
    language = request.args.get("language", DEFAULT_LANGUAGE)
    days = int(request.args.get("days", DEFAULT_DAYS))
    limit = int(request.args.get("limit", DEFAULT_LIMIT))

    try:
        repositories = fetch_trending_repositories(language=language, days=days, limit=limit)
        return jsonify(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "language": language,
                "days": days,
                "count": len(repositories),
                "repositories": repositories,
            }
        )
    except requests.HTTPError as exc:
        return jsonify({"error": "GitHub API request failed", "detail": str(exc)}), 502
    except ValueError:
        return jsonify({"error": "Invalid query parameters for days/limit"}), 400
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": "Unexpected server error", "detail": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=False)
