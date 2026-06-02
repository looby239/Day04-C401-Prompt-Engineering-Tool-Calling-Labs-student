from __future__ import annotations

import os
from typing import Any
import requests
from tools._shared import TIMEOUT, err

def github_search(query: str = "", limit: int = 5, sort: str = "stars") -> dict[str, Any]:
    """
    Search for repositories on GitHub using the GitHub Search API.
    """
    if not query:
        return {"tool": "github_search", "query": query, "items": []}
    
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Day04-Research-Agent/1.0"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "per_page": int(limit or 5),
            "sort": sort or "stars",
            "order": "desc"
        }
        
        resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        
        items = []
        for repo in data.get("items", []):
            items.append({
                "title": repo.get("full_name"),
                "url": repo.get("html_url"),
                "source": "GitHub",
                "summary": repo.get("description") or "No description provided.",
                "stars": repo.get("stargazers_count"),
                "language": repo.get("language")
            })
            
        return {"tool": "github_search", "query": query, "items": items}
        
    except Exception as exc:
        return err("github_search", exc)
