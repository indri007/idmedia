import re
import requests

HEADERS = {
    "User-Agent": "ScientificManuscriptQA/1.0 (research quality-assurance tool)"
}

def split_references(text):
    match = re.search(
        r"\b(references|bibliography|daftar pustaka)\b", text, re.I
    )
    if not match:
        return []
    tail = text[match.end():]
    chunks = re.split(r"\n\s*\n", tail)
    return [
        re.sub(r"\s+", " ", item).strip()
        for item in chunks
        if len(item.strip()) > 25
    ][:30]

def lookup_crossref(reference, timeout=8):
    try:
        response = requests.get(
            "https://api.crossref.org/works",
            params={"query.bibliographic": reference, "rows": 1},
            headers=HEADERS, timeout=timeout
        )
        response.raise_for_status()
        items = response.json().get("message", {}).get("items", [])
        if not items:
            return {"provider": "Crossref", "match": False}
        item = items[0]
        title = (item.get("title") or [""])[0]
        return {
            "provider": "Crossref",
            "match": bool(title),
            "title": title,
            "doi": item.get("DOI"),
            "year": (item.get("published-print") or item.get("published-online") or {}).get("date-parts", [[None]])[0][0],
            "url": item.get("URL"),
        }
    except Exception as exc:
        return {"provider": "Crossref", "match": None, "error": str(exc)}

def lookup_openalex(reference, timeout=8):
    try:
        response = requests.get(
            "https://api.openalex.org/works",
            params={"search": reference, "per-page": 1},
            headers=HEADERS, timeout=timeout
        )
        response.raise_for_status()
        items = response.json().get("results", [])
        if not items:
            return {"provider": "OpenAlex", "match": False}
        item = items[0]
        return {
            "provider": "OpenAlex",
            "match": bool(item.get("title")),
            "title": item.get("title"),
            "year": item.get("publication_year"),
            "doi": item.get("doi"),
            "url": item.get("id"),
        }
    except Exception as exc:
        return {"provider": "OpenAlex", "match": None, "error": str(exc)}

def audit_references(text, provider="Crossref", limit=10):
    refs = split_references(text)[:limit]
    results = []
    for ref in refs:
        match = lookup_crossref(ref) if provider == "Crossref" else lookup_openalex(ref)
        results.append({"reference": ref, **match})
    return results
