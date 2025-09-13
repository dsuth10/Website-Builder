param(
  [string]$Host="127.0.0.1",
  [int]$Port=8000
)

Write-Host "Starting FastAPI on http://$Host:$Port" -ForegroundColor Green
python -m uvicorn app.main:app --host $Host --port $Port --reload --app-dir ./backend
