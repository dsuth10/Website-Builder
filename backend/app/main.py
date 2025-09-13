from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .core.config import get_settings
from .core.db import init_db
from .api.content import router as content_router


load_dotenv()
app = FastAPI(title="School Site Generator")
settings = get_settings()

origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.include_router(content_router)

