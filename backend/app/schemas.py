from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .models import VersionStatus


class GenerateRequest(BaseModel):
    title: str
    topic: str
    reading_level: str | None = None
    grade: str | None = None
    genre: str | None = None


class VersionOut(BaseModel):
    id: int
    version: int
    status: VersionStatus
    reading_level: Optional[str]
    grade: Optional[str]
    genre: Optional[str]
    topic: Optional[str]
    created_at: datetime
    published_at: Optional[datetime]
    word_count: Optional[int]
    difficult_words_count: Optional[int]
    flesch_reading_ease: Optional[float]
    flesch_kincaid_grade: Optional[float]
    gunning_fog: Optional[float]
    smog_index: Optional[float]
    automated_readability_index: Optional[float]
    coleman_liau_index: Optional[float]
    linsear_write_formula: Optional[float]
    dale_chall_readability_score: Optional[float]
    readability_consensus: Optional[str]


class ItemOut(BaseModel):
    id: int
    title: str
    slug: str
    latest_version: Optional[VersionOut] = None


class ItemDetailOut(BaseModel):
    id: int
    title: str
    slug: str
    versions: list[VersionOut]


class ImportVersionIn(BaseModel):
    version: Optional[int] = None
    status: Optional[VersionStatus] = VersionStatus.draft
    reading_level: Optional[str] = None
    grade: Optional[str] = None
    genre: Optional[str] = None
    topic: Optional[str] = None
    body_html: str
    word_count: Optional[int] = None
    difficult_words_count: Optional[int] = None
    flesch_reading_ease: Optional[float] = None
    flesch_kincaid_grade: Optional[float] = None
    gunning_fog: Optional[float] = None
    smog_index: Optional[float] = None
    automated_readability_index: Optional[float] = None
    coleman_liau_index: Optional[float] = None
    linsear_write_formula: Optional[float] = None
    dale_chall_readability_score: Optional[float] = None
    readability_consensus: Optional[str] = None


class ImportItemIn(BaseModel):
    title: str
    slug: Optional[str] = None
    versions: list[ImportVersionIn]


class ImportItemsIn(BaseModel):
    items: list[ImportItemIn]
