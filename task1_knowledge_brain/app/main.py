from app.search import answer_question
from app.crawler import crawl_articles
from fastapi import FastAPI

app = FastAPI(
    title="AI Tech Consultant - Knowledge Brain",
    description="A searchable knowledge base for support articles.",
    version="0.1.0",
)


@app.get("/")
def home():
    return {"message": "Knowledge Brain API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/crawl")
def run_crawler(limit: int = 10):
    if limit < 1 or limit > 50:
        return {"error": "limit must be between 1 and 50"}

    return crawl_articles(limit=limit)

@app.get("/ask")
def ask_question(question: str):
    return answer_question(question)
