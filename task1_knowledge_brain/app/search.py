
import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "articles.json"

STOP_WORDS = {
    "the", "and", "for", "are", "what", "how", "can", "does",
    "with", "from", "this", "that", "you", "your", "have",
    "is", "a", "an", "to", "of", "in", "on", "i", "my",
    "please", "tell", "me", "about"
}


def search_articles(question: str, limit: int = 3) -> list[dict]:
    """Search saved articles using keyword matching."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    words = set(re.findall(r"\b[a-z0-9]+\b", question.lower()))
    words -= STOP_WORDS

    if not words:
        return []

    results = []

    for article in articles:
        title = article.get("title", "")
        text = article.get("text", "")
        title_lower = title.lower()
        content_lower = text.lower()

        score = sum(
            3 * len(re.findall(r"\b" + re.escape(word) + r"\b", title_lower))
            + len(re.findall(r"\b" + re.escape(word) + r"\b", content_lower))
            for word in words
        )

        if score > 0:
            results.append({
                "title": title,
                "url": article["url"],
                "score": score,
                "snippet": text[:500],
            })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def answer_question(question: str) -> dict:
    """Return relevant sources and avoid unsupported answers."""
    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    results = search_articles(question)

    if not results:
        return {
            "answer": (
                "I could not find relevant information in the saved "
                "support articles. Please ask a human expert."
            ),
            "sources": [],
        }

    return {
        "answer": (
            "I found potentially relevant support articles. "
            "Please review the sources to verify the answer. "
            "AI-generated answers have not been enabled yet."
        ),
        "sources": [
            {
                "title": item["title"],
                "url": item["url"],
                "snippet": item["snippet"],
            }
            for item in results
        ],
    }
