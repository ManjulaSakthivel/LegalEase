@echo off
echo Starting LegalEase backend...
start "LegalEase Backend" cmd /k ".venv\Scripts\activate && uvicorn backend.main:app --reload --port 8000"
timeout /t 3 >nul
echo Starting LegalEase frontend...
start "LegalEase Frontend" cmd /k ".venv\Scripts\activate && streamlit run frontend\app.py"
echo Done.
