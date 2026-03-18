# 📚 Book Summarizer — AI Powered

## Local Setup

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Create .env file
cp .env.example .env
# Apna Anthropic API key daalo .env mein

# Step 3: Run karo
python app.py

# Step 4: Browser mein kholo
# http://localhost:5000
```

## Deploy on Render.com (FREE)

1. Yeh folder GitHub pe upload karo
2. render.com pe jao → New Web Service
3. GitHub repo connect karo
4. Environment variable add karo:
   - Key:   `ANTHROPIC_API_KEY`
   - Value: `sk-ant-xxxxxxx`
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Deploy karo ✅

## Deploy on Railway.app (FREE)

1. railway.app pe jao
2. New Project → GitHub se deploy karo
3. Variable add karo: `ANTHROPIC_API_KEY`
4. Auto deploy ho jayega ✅

## Project Structure

```
BookSummarizer_Final/
├── app.py                  → Flask server (API routes)
├── summarizer.py           → Claude AI logic
├── requirements.txt        → Python dependencies
├── Procfile                → Deployment config
├── .env.example            → API key template
├── README.md               → Yeh file
├── templates/
│   └── index.html          → Frontend UI (dark theme)
└── utils/
    ├── __init__.py
    ├── pdf_extractor.py    → PDF text extraction
    └── history_manager.py  → Summary history
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET  | / | Main page |
| POST | /api/summarize | Generate summary |
| POST | /api/extract-pdf | Extract PDF text |
| GET  | /api/history | Get history |
| DELETE | /api/history/clear | Clear history |
