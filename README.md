# Website Builder

Single-school website generator with a FastAPI backend and a React (Vite) frontend. Generates content via LLM (OpenRouter), computes readability metrics (textstat), versions content (draft/publish), exports PDFs, and supports JSON import/export.

## Quick Start

### Prerequisites
- Python 3.12
- Node.js 18+ (LTS recommended)
- Windows: PowerShell (preferred) or Git Bash. macOS/Linux: a POSIX shell.

### 1) Clone and install
- Windows PowerShell
```powershell
cd "C:\Users\<you>\Documents\Code Projects\Website Builder"
python -m pip install -r backend/requirements.txt --disable-pip-version-check
cd frontend; npm install; cd ..
```

- macOS/Linux
```bash
cd "~/Documents/Code Projects/Website Builder"
python3 -m pip install -r backend/requirements.txt --disable-pip-version-check
(cd frontend && npm install)
```

### 2) Configure environment (optional but recommended)
Create a `.env` file in the project root if you need non-defaults:

```
# AI (optional). Without a key, placeholder HTML is returned.
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openrouter/auto

# Frontend CORS allowed origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173

# Dev database (SQLite file in repo root)
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

Notes:
- The backend loads `.env` from the repository root.
- The frontend defaults to `http://127.0.0.1:8004` for API calls. Override with `VITE_API_BASE` if you use a different backend port.

### 3) Run the backend (FastAPI)
- PowerShell (recommended on Windows)
```powershell
cd "C:\Users\<you>\Documents\Code Projects\Website Builder"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8004 --app-dir ./backend
```

- macOS/Linux
```bash
cd "~/Documents/Code Projects/Website Builder"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8004 --app-dir ./backend
```

Verify:
- Open `http://127.0.0.1:8004/api/health` — should return `{"status":"ok"}`.

### 4) Run the frontend (Vite + React)
- PowerShell
```powershell
cd "C:\Users\<you>\Documents\Code Projects\Website Builder\frontend"
# Only set VITE_API_BASE if your backend is not at the default http://127.0.0.1:8004
# $env:VITE_API_BASE = "http://127.0.0.1:8004"
npm run dev -- --host 0.0.0.0 --port 5173 --strictPort
```

- Git Bash or macOS/Linux
```bash
cd "~/Documents/Code Projects/Website Builder/frontend"
# VITE_API_BASE=http://127.0.0.1:8004 npm run dev -- --host 0.0.0.0 --port 5173 --strictPort
npm run dev -- --host 0.0.0.0 --port 5173 --strictPort
```

Open the app UI: `http://localhost:5173`

If the dev server struggles to bind, you can also:
```bash
# Build + preview (static preview server)
cd frontend
npm run build
npx vite preview --host 127.0.0.1 --port 5173 --strictPort
```

## Using the App (UI)
1. Visit `http://localhost:5173`.
2. Generate content:
   - Title (optional; auto-derives from Topic if blank)
   - Topic (required)
   - Reading level (required)
   - Grade and Genre (optional)
   - Click Generate → a new draft version appears for the item.
3. Select an item to view versions:
   - View HTML (new tab)
   - Download PDF
   - Publish (archives previously published)
   - Export Item (JSON) or Import JSON (single item or `{ items: [...] }`)

## REST API Quick Test
- Health: `GET http://127.0.0.1:8004/api/health`
- Generate (auto-title if `title` empty):
```bash
curl -X POST http://127.0.0.1:8004/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{"title":"","topic":"Amazon Rainforest","reading_level":"Grade 5","grade":"5","genre":"Informational"}'
```
- List: `GET http://127.0.0.1:8004/api/content/`
- Item: `GET http://127.0.0.1:8004/api/content/{item_id}`
- Publish: `POST http://127.0.0.1:8004/api/content/{item_id}/versions/{version_id}/publish`
- Version HTML: `GET http://127.0.0.1:8004/api/content/{item_id}/versions/{version_id}/html`
- Version PDF: `GET http://127.0.0.1:8004/api/content/{item_id}/versions/{version_id}/pdf`
- Export item: `GET http://127.0.0.1:8004/api/content/{item_id}/export`
- Import single item:
```bash
curl -X POST http://127.0.0.1:8004/api/content/import \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","versions":[{"body_html":"<h1>Test</h1><p>Body</p>","status":"draft"}]}'
```

## Technology Overview
- Backend: FastAPI + `sqlmodel` + SQLite (`aiosqlite`), `xhtml2pdf` for PDFs, readability metrics via `textstat` + BeautifulSoup.
- Frontend: React 18 + Vite.
- AI (optional): OpenRouter. Without a key, the backend returns placeholder HTML so flows are testable.

## Troubleshooting
- Cannot import `app` when running uvicorn?
  - Always include `--app-dir ./backend` (as shown above).
  - Alternatively, set `PYTHONPATH` to the `backend` folder in your shell.
- CORS blocked in the browser?
  - Set `ALLOWED_ORIGINS` in `.env` (default allows `http://localhost:5173`).
- Port already in use (5173 or 8004)?
  - Use `--port` with a different number, and update `VITE_API_BASE` accordingly.
- Vite dev server not reachable?
  - Start it interactively (avoid hidden/detached windows) to view logs.
  - Try `npm run build && npx vite preview` as a fallback.
- Reset database schema
  - Stop the backend and delete `app.db` in the repo root; it will be recreated on startup.

### Windows PowerShell vs Git Bash tips
- PowerShell sets env vars using `$env:NAME = "value"` and the variable applies only to the current shell.
- Git Bash/macOS/Linux set env inline: `NAME=value command`.
- Example (frontend dev server):
  - PowerShell:
    - `$env:VITE_API_BASE = "http://127.0.0.1:8004"`
    - `npm run dev -- --host 0.0.0.0 --port 5173 --strictPort`
  - Git Bash/macOS/Linux:
    - `VITE_API_BASE=http://127.0.0.1:8004 npm run dev -- --host 0.0.0.0 --port 5173 --strictPort`

## Key Files
- `backend/app/main.py`
- `backend/app/api/content.py`
- `backend/app/models.py`
- `backend/app/schemas.py`
- `backend/app/services/ai.py`
- `backend/app/services/readability.py`
- `backend/app/services/pdf.py`
- `frontend/src/App.jsx`
- `frontend/src/api.js`
- `scripts/run-backend.ps1`
- `scripts/run-frontend.ps1`
