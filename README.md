# AI Tech Consultant Capstone

## Overview
This project aims to help a technology consulting team answer customer support questions, draft email replies, and prepare scopes of work from meeting transcripts.

## Tasks

### Task 1: Knowledge Brain
A Python and FastAPI service that collects Brilliant Directories support articles, stores their text locally, and searches for relevant information with source URLs.

### Task 2: Inbox Agent
An email assistant designed to prepare customer reply drafts using the Knowledge Brain and support human review.

### Task 3: Meeting-to-Scope-of-Work
A tool designed to turn meeting transcripts into structured scopes of work, estimates, and proposals.

## Technology Stack
- Python
- FastAPI and Uvicorn
- HTTPX
- Beautiful Soup and lxml
- pytest
- TypeScript or Python for additional tasks, depending on implementation

## Run Task 1
Open PowerShell in the project root and run:

```powershell
.\task1_knowledge_brain\.venv\Scripts\Activate.ps1
cd task1_knowledge_brain
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## Run Tests
From the `task1_knowledge_brain` directory:

```powershell
python -m pytest -v
```

## Current Status and Limitations
Task 1 currently supports basic sitemap crawling, local JSON storage, keyword-based search, source citations, and automated tests. Semantic retrieval, AI-generated answers, automated content updates, and human-review workflows still need implementation. Tasks 2 and 3 must be completed and tested before the full capstone is ready.