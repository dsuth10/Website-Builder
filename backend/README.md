# Backend (FastAPI)

School website generator backend built with FastAPI, `sqlmodel` (SQLite + aiosqlite), and services for readability metrics and PDF export.

## Quick Start

### Prerequisites
- Python 3.12

### Install dependencies
```powershell
# From repo root (Windows PowerShell)
python -m pip install -r backend/requirements.txt --disable-pip-version-check
```
```bash
# macOS/Linux
python3 -m pip install -r backend/requirements.txt --disable-pip-version-check
```

### Configure environment (optional)
Create a `.env` in the repository root if you need non-defaults:

```
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openrouter/auto
ALLOWED_ORIGINS=http://localhost:5173
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

Notes:
- If `OPENROUTER_API_KEY` is not set, the generate endpoint returns placeholder HTML so you can test the flow.
- Tables auto-create on startup (no migrations required for first run).

### Run the server
```powershell
# From repo root (Windows PowerShell)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir ./backend
```
```bash
# macOS/Linux
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir ./backend
```

Verify health:
```
GET http://127.0.0.1:8000/api/health
```

## API
- `GET /api/health` — health check
- `POST /api/content/generate` — body: `{ title, topic, reading_level, grade?, genre? }`
- `GET /api/content` — list items with latest version
- `GET /api/content/{item_id}` — item with versions
- `POST /api/content/{item_id}/versions/{version_id}/publish` — publish a version
- `GET /api/content/{item_id}/versions/{version_id}/html` — raw HTML
- `GET /api/content/{item_id}/versions/{version_id}/pdf` — download PDF
- `GET /api/content/share/{token}` — simple share view
- `GET /api/content/{item_id}/export` — export one item with versions as JSON
- `POST /api/content/import` — import one item or `{ items: [...] }` JSON

## Services
- AI (`backend/app/services/ai.py`): calls OpenRouter; returns placeholder HTML if no API key.
- Readability (`backend/app/services/readability.py`): parses HTML to text and computes Textstat metrics.
- PDF (`backend/app/services/pdf.py`): converts HTML to PDF via `xhtml2pdf` (no external binaries).

## Troubleshooting
- Module import errors when starting uvicorn
  - Ensure you pass `--app-dir ./backend` as shown above (so `app.*` imports resolve).
- CORS blocked by browser
  - Set `ALLOWED_ORIGINS` in `.env` (default allows `http://localhost:5173`).
- Reset the database schema
  - Stop the server and delete `app.db` in the repo root; it will be recreated on next startup.
- Want migrations?
  - Ask to add Alembic; current setup auto-creates tables on startup.

## Data (stored per version)
- Title, slug (on item)
- Version number, status (draft/published/archived)
- Reading level, grade, genre, topic, HTML body
- Metrics: word_count, difficult_words_count, Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog, SMOG, ARI, Coleman-Liau, Linsear Write, Dale-Chall, consensus
