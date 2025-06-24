import requests
from bs4 import BeautifulSoup, Tag

def fetch_factcheck_claims(limit=25):
    url = "https://www.factcheck.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = []
    for i, tag in enumerate(soup.find_all("a", href=True)):
        if i >= limit:
            break

        if not isinstance(tag, Tag):
            continue  # skip if tag isn't a valid BeautifulSoup Tag

        claim = tag.get_text(strip=True)
        link = tag.get("href")

        if not claim or not isinstance(link, str):
            continue

        if not link.startswith("http"):
            link = url.rstrip("/") + "/" + link.lstrip("/")

        results.append({
            "claim": claim,
            "rating": "Unrated",
            "publisher": "FactCheck.org",
            "url": link
        })

    return results
