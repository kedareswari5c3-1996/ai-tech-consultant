import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Tech Consultant - Inbox Agent")

KNOWLEDGE_BRAIN_URL = "http://127.0.0.1:8000/ask"


class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str


class DraftResponse(BaseModel):
    subject: str
    draft: str
    knowledge_context: str
    requires_human_review: bool = True


@app.get("/")
def home():
    return {"message": "Inbox Agent is running"}


@app.post("/draft", response_model=DraftResponse)
async def draft_reply(email: EmailRequest):
    question = f"Customer email subject: {email.subject}\nMessage: {email.body}"

    knowledge_context = "Knowledge Brain is unavailable. Please review manually."

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                KNOWLEDGE_BRAIN_URL,
                params={"question": question},
            )
            response.raise_for_status()
            result = response.json()

            if isinstance(result, dict):
                knowledge_context = str(
                    result.get("answer", result.get("detail", result))
                )
            else:
                knowledge_context = str(result)

    except (httpx.HTTPError, ValueError):
        pass

    draft = (
        f"Hello,\n\n"
        f"Thank you for contacting us about '{email.subject}'.\n\n"
        f"Here is the information available for your question:\n"
        f"{knowledge_context}\n\n"
        "Please let us know if you need any further assistance.\n\n"
        "Best regards,\nSupport Team"
    )

    return DraftResponse(
        subject=f"Re: {email.subject}",
        draft=draft,
        knowledge_context=knowledge_context,
        requires_human_review=True,
    )
