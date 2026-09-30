# LegalEase — AI-Powered Legal Document Generator

LegalEase is a complete FastAPI + Streamlit application based on the supplied project documentation. It accepts a document type, parties, terms, and effective date, generates a structured legal draft with Google Gemini, previews/edits the result, and exports TXT/DOCX/PDF.

> **Important:** LegalEase generates drafts for informational/document-preparation purposes. It is not a substitute for advice from a qualified lawyer. Users should review generated documents for jurisdiction-specific requirements before signing or relying on them.

## Architecture

```text
Streamlit UI
    |
    | POST /generate
    v
FastAPI backend
    |
    v
GeminiDocumentGenerator
    |
    v
Google Gemini API
    |
    v
Generated legal draft
    |
    +--> TXT
    +--> DOCX
    +--> PDF
```

The supplied documentation selected Gemini 1.5 Pro and the legacy `google-generativeai` SDK. This implementation uses Google's current `google-genai` SDK and a configurable model. The default is `gemini-3.8-flash`; set `GEMINI_MODEL` to another available model if required.

## Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── dependencies.py
│   └── ai_core/
│       ├── __init__.py
│       └── gemini_generator.py
├── frontend/
│   ├── __init__.py
│   └── app.py
├── services/
│   ├── __init__.py
│   └── document_formatter.py
├── utils/
│   ├── __init__.py
│   └── text_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_formatters.py
├── assets/
│   └── logo.svg
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
└── run_local.bat
```

## 1. Requirements

- Python 3.10+
- A Google Gemini API key
- VS Code recommended

## 2. Windows / VS Code setup

Open the project folder in VS Code.

Open **Terminal → New Terminal**, then:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment file:

```powershell
copy .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=YOUR_REAL_GEMINI_API_KEY
```

You can get a Gemini API key from Google AI Studio.

## 3. Run the backend

In Terminal 1:

```powershell
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```

Check:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 4. Run the Streamlit frontend

In Terminal 2:

```powershell
.venv\Scripts\activate
streamlit run frontend/app.py
```

Open the URL Streamlit prints, normally:

```text
http://localhost:8501
```

The frontend expects the backend at:

```env
BACKEND_URL=http://127.0.0.1:8000
```

## 5. Generate a document

Example:

**Document Type**
```text
Freelance Work Contract
```

**Parties**
```text
Jane Doe (Service Provider), TechNova Inc. (Client)
```

**Terms**
```text
Payment to be made within 30 days of invoice;
The provider agrees to deliver work by the agreed deadline;
Confidentiality must be maintained at all times;
Either party may terminate with 15 days notice
```

**Effective Date**
```text
April 15, 2026
```

Click **Generate Document**.

Then edit the generated text if required and download TXT, DOCX, or PDF.

## 6. Run tests

Install development dependencies:

```powershell
pip install -r requirements-dev.txt
```

Run:

```powershell
pytest -q
```

The tests do not call Gemini. The API tests use a deterministic fake generator.

## 7. Docker

Create `.env` first.

```powershell
docker compose up --build
```

Then:

- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Frontend: http://localhost:8501

## Notes about the supplied documentation

The supplied PDF describes FastAPI, Streamlit, Gemini, editable previews, and TXT/DOCX/PDF export. It also mentions `google-generativeai` and Gemini 1.5 Pro. Those are legacy choices now, so this implementation uses Google's newer `google-genai` Python SDK and makes the model configurable.

Current Google documentation shows the Python SDK pattern as:

```python
from google import genai
client = genai.Client()
response = client.models.generate_content(...)
```

and lists current Gemini models separately. Keep `GEMINI_MODEL` configurable so the project can be changed without modifying application code.

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Set the key in `.env` and restart the backend.

### `Connection refused`
Start FastAPI first:

```powershell
uvicorn backend.main:app --reload --port 8000
```

### PDF contains missing characters
LegalEase sanitizes typographic Unicode characters before PDF creation because the bundled PDF font is intentionally dependency-light. DOCX preserves normal Unicode.

### Gemini model unavailable
Change `GEMINI_MODEL` in `.env` to a model available to your API project.

## Security checklist before production

- Do not commit `.env`.
- Add authentication/authorization.
- Add rate limiting.
- Add request-size limits.
- Store documents securely if persistence is added.
- Do not log confidential legal input.
- Use HTTPS.
- Review generated content with a qualified legal professional for real legal use.
