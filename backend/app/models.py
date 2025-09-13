from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class VersionStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class ContentItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship removed; queries use explicit joins/selects


class ContentVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="contentitem.id", index=True)
    version: int = Field(index=True)
    status: VersionStatus = Field(default=VersionStatus.draft)
    reading_level: Optional[str] = None
    grade: Optional[str] = None
    genre: Optional[str] = None
    topic: Optional[str] = None
    body_html: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None

    # Relationship removed; use item_id for joins

    # Readability & counts
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
