from __future__ import annotations

from typing import Any
import requests
from tools._shared import TIMEOUT, err

def wikipedia_search(query: str = "", limit: int = 3) -> dict[str, Any]:
    """
    Search Wikipedia and return page summaries for the top matches.
    """
    if not query:
        return {"tool": "wikipedia", "query": query, "items": []}
    
    headers = {
        "User-Agent": "Day04-Research-Agent/1.0 (educational lab; looby@example.com)"
    }
    
    try:
        # Step 1: Search Wikipedia for the query
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": int(limit or 3),
            "format": "json",
            "utf8": 1
        }
        
        search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=TIMEOUT)
        search_resp.raise_for_status()
        search_data = search_resp.json()
        
        search_results = search_data.get("query", {}).get("search", [])
        if not search_results:
            return {"tool": "wikipedia", "query": query, "items": []}
            
        # Step 2: For each title, get the intro extract
        items = []
        for result in search_results:
            title = result.get("title")
            pageid = result.get("pageid")
            
            # Fetch summary extract
            extract_params = {
                "action": "query",
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
                "titles": title,
                "format": "json"
            }
            extract_resp = requests.get(search_url, params=extract_params, headers=headers, timeout=TIMEOUT)
            extract_resp.raise_for_status()
            extract_data = extract_resp.json()
            
            pages = extract_data.get("query", {}).get("pages", {})
            page_content = ""
            for pid, pdata in pages.items():
                if str(pid) == str(pageid) or pdata.get("title") == title:
                    page_content = pdata.get("extract", "")
                    break
            
            # Format the URL safely
            safe_title = title.replace(" ", "_")
            url = f"https://en.wikipedia.org/wiki/{safe_title}"
            
            items.append({
                "title": title,
                "url": url,
                "source": "Wikipedia",
                "summary": page_content or result.get("snippet", "")
            })
            
        return {"tool": "wikipedia", "query": query, "items": items}
        
    except Exception as exc:
        return err("wikipedia", exc)
