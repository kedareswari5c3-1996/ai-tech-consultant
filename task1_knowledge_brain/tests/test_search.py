
import json

from app.search import answer_question, search_articles


def test_search_finds_matching_article(tmp_path, monkeypatch):
    import app.search as search_module

    data_file = tmp_path / "articles.json"
    data_file.write_text(
        json.dumps([
            {
                "title": "How to configure a membership website",
                "url": "https://example.com/membership",
                "text": "Learn how to configure membership website settings.",
            }
        ]),
        encoding="utf-8",
    )
    monkeypatch.setattr(search_module, "DATA_FILE", data_file)

    results = search_articles("membership website")
    assert results
    assert results[0]["url"] == "https://example.com/membership"


def test_answer_includes_source_citation(tmp_path, monkeypatch):
    import app.search as search_module

    data_file = tmp_path / "articles.json"
    data_file.write_text(
        json.dumps([
            {
                "title": "Website settings",
                "url": "https://example.com/settings",
                "text": "Open the website settings page to update your website.",
            }
        ]),
        encoding="utf-8",
    )
    monkeypatch.setattr(search_module, "DATA_FILE", data_file)

    response = answer_question("website settings")
    assert len(response["sources"]) > 0
    assert response["sources"][0]["url"] == "https://example.com/settings"


def test_unknown_question_returns_human_fallback(tmp_path, monkeypatch):
    import app.search as search_module

    data_file = tmp_path / "articles.json"
    data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(search_module, "DATA_FILE", data_file)

    response = answer_question("unrelated question")
    assert response["sources"] == []
    assert "human expert" in response["answer"].lower()
