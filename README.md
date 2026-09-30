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

---

## SmartBridge Project Team

| Detail | Information |
|---|---|
| **Team ID** | SWTID-2026-6491 |
| **Team Size** | 3 |
| **Team Leader** | Manjula S |
| **Team Member** | P Dayana |
| **Team Member** | Gomathy R |
| **Project** | LegalEase – AI-Powered Legal Document Generator |

### SmartBridge Enrollment

Our team was successfully enrolled for the project through **SmartBridge / MySkillWallet**.

MySkillWallet: https://myskillwallet.ai/login

## Project Objectives

- Generate structured legal document drafts using AI.
- Provide a simple and user-friendly interface for document creation.
- Accept document type, parties, terms, and dates as input.
- Allow users to review and edit generated content.
- Export documents in TXT, DOCX, and PDF formats.
- Provide a modular architecture that can be extended with additional document types and AI providers.

## Key Features

- AI-assisted legal document generation
- FastAPI REST API
- Streamlit web interface
- Editable generated-document preview
- TXT, DOCX, and PDF export
- Configurable Gemini model
- Environment-variable based API configuration
- API health-check endpoint
- Swagger/OpenAPI documentation
- Automated tests for core functionality
- Demo mode when a Gemini API key is not configured

## Basic Workflow

```text
User enters legal details
        ↓
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
Google Gemini API
        ↓
Generated Legal Document
        ↓
Editable Preview
        ↓
TXT / DOCX / PDF
```

## Quick Start

### 1. Create and activate the virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure the environment

Copy `.env.example` to `.env` and add the Gemini API key:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
APP_NAME=LegalEase
LOG_LEVEL=INFO
```

Never commit `.env` or expose the API key in source code.

### 4. Start the backend

Run this command from the **LegalEase project root**, not from the `backend` directory:

```powershell
uvicorn backend.main:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the frontend

Open a second terminal, return to the **LegalEase project root**, activate the same `.venv`, and run:

```powershell
python -m streamlit run frontend/app.py
```

The frontend normally opens at:

```text
http://localhost:8501
```

## API Endpoints

### `GET /`

Returns basic application information.

### `GET /health`

Checks whether the backend is running.

### `POST /generate`

Accepts legal-document information and returns generated document content.

Example request:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Party A: ABC Technologies\nParty B: John Doe",
  "terms": "Confidential information must not be disclosed to third parties.",
  "dates": "Effective Date: 01-10-2026"
}
```

## Testing

Install development dependencies:

```powershell
pip install -r requirements-dev.txt
```

Run the test suite:

```powershell
pytest -q
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'backend'`

Run Uvicorn from the project root:

```powershell
cd C:\path\to\LegalEase
uvicorn backend.main:app --reload --port 8000
```

Do not run the command from `LegalEase\backend`.

### `ModuleNotFoundError: No module named 'services'`

Run Streamlit from the project root:

```powershell
cd C:\path\to\LegalEase
python -m streamlit run frontend/app.py
```

Do not first change into the `frontend` directory and then use `frontend/app.py` as the script path.

### `streamlit is not recognized`

Use the Python module form:

```powershell
python -m streamlit run frontend/app.py
```

If Streamlit is not installed:

```powershell
pip install -r requirements.txt
```

## Security and Responsible Use

- Keep API keys in `.env` and never commit them to a public repository.
- Do not hard-code credentials in Python files.
- Avoid entering unnecessary confidential information into external AI services.
- Review all AI-generated legal content before real-world use.
- LegalEase is an educational document-drafting prototype and does not replace qualified legal advice.

## Future Enhancements

Potential future improvements include:

- User authentication and role-based access
- Document history and database storage
- Additional legal document templates
- Multi-language document generation
- Clause libraries and reusable templates
- Digital signatures
- Document comparison
- Cloud deployment
- Additional AI model providers
- Enhanced validation and legal-content checks

## Acknowledgement

We sincerely thank **SmartBridge** for providing the project opportunity and guidance through the SkillWallet / MySkillWallet platform.

This project was developed by the above team as part of the SmartBridge project program.
