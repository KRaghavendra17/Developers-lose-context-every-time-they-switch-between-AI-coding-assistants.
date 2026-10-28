# LearnPilot AI — Quizlet-inspired study dashboard

This is original starter code inspired by common study-tool features. It is not Quizlet's private source code and is not affiliated with Quizlet.

## Features
- Responsive dark navy/purple dashboard
- PDF/TXT note upload
- Starter flashcards and multiple-choice practice questions
- Study guide summary preview
- Progress counters saved in browser localStorage
- Mobile navigation

## Run on Windows / VS Code
Open this folder (the one containing `app.py` and `requirements.txt`) in VS Code. In Terminal > New Terminal, run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Then visit http://127.0.0.1:5000

If you already have a virtual environment in a different folder, create one here for the simplest setup.

## Limitations
The generated questions are a basic offline demo, not a full AI system. Scanned PDFs need OCR. No login or database is included yet; progress is browser-local.
