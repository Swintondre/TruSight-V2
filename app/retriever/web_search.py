# app/retriever/web_search.py
import requests
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search"

def search_web(query: str, num_results: int = 5) -> List[dict]:
    """
    Calls Serper API and returns a list of results.
    Each result: {"title": ..., "snippet": ..., "link": ...}
    """
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": num_results
    }

    try:
        response = requests.post(SERPER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("organic", [])[:num_results]:
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            })

        return results

    except requests.RequestException as e:
        print(f"[!] Serper API Error: {e}")
        return []

    return []

# Optional test
if __name__ == "__main__":
    import json
    print(json.dumps(search_web("Joe Biden student loan forgiveness"), indent=2))
