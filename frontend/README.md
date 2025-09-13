# Frontend (React + Vite)

React 18 app built with Vite. Talks to the FastAPI backend (`http://localhost:8000` by default).

## Quick Start

### Prerequisites
- Node.js 18+ (LTS recommended)

### Install
```bash
cd frontend
npm install
```

### Run (development)
- Windows PowerShell
```powershell
cd frontend
# Only set VITE_API_BASE if your backend is not at the default http://localhost:8000
$env:VITE_API_BASE = "http://127.0.0.1:8000"
npm run dev -- --host 0.0.0.0 --port 5173 --strictPort
```

- Git Bash / macOS / Linux
```bash
cd frontend
VITE_API_BASE=http://127.0.0.1:8000 npm run dev -- --host 0.0.0.0 --port 5173 --strictPort
```

Open the app at: `http://localhost:5173`

### Build
```bash
cd frontend
npm run build
```

### Preview (static server)
```bash
cd frontend
npx vite preview --host 127.0.0.1 --port 5173 --strictPort
```

## Environment
The frontend reads the API base URL from `import.meta.env.VITE_API_BASE`.
- Default: `http://localhost:8000`
- Override at runtime when starting dev server (see above) or create a `.env` in `frontend/`:

```
VITE_API_BASE=http://127.0.0.1:8000
```

## Troubleshooting
- API requests failing (CORS or 404)?
  - Ensure the backend is running: `http://127.0.0.1:8000/api/health` should return `{ "status": "ok" }`.
  - If using a different host/port for backend, set `VITE_API_BASE` accordingly.
- Port 5173 already in use?
  - Change `--port` in the dev/preview command.
- Dev server not starting or no logs visible?
  - Run interactively (avoid hidden/detached windows) to see startup output.
- Build succeeded, preview says `dist` missing?
  - Run `npm run build` in `frontend/` first, then `npx vite preview`.

## Key Files
- `src/main.jsx`
- `src/App.jsx`
- `src/api.js`
- `index.html`




