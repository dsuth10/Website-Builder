from __future__ import annotations
from dataclasses import dataclass
from bs4 import BeautifulSoup
import textstat
import math


@dataclass
class ReadabilityMetrics:
    word_count: int
    difficult_words_count: int
    flesch_reading_ease: float | None
    flesch_kincaid_grade: float | None
    gunning_fog: float | None
    smog_index: float | None
    automated_readability_index: float | None
    coleman_liau_index: float | None
    linsear_write_formula: float | None
    dale_chall_readability_score: float | None
    readability_consensus: str


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    # remove scripts/styles if any slipped in
    for tag in soup(['script', 'style']):
        tag.decompose()
    return soup.get_text(separator=' ', strip=True)


def compute_metrics(html: str) -> ReadabilityMetrics:
    text = html_to_text(html)
    # textstat expects plain text
    word_count = textstat.lexicon_count(text, removepunct=True)
    difficult_words_count = textstat.difficult_words(text)

    def safe_float(value: float | int) -> float | None:
        v = float(value)
        return v if math.isfinite(v) else None

    return ReadabilityMetrics(
        word_count=word_count,
        difficult_words_count=difficult_words_count,
        flesch_reading_ease=safe_float(textstat.flesch_reading_ease(text)),
        flesch_kincaid_grade=safe_float(textstat.flesch_kincaid_grade(text)),
        gunning_fog=safe_float(textstat.gunning_fog(text)),
        smog_index=safe_float(textstat.smog_index(text)),
        automated_readability_index=safe_float(textstat.automated_readability_index(text)),
        coleman_liau_index=safe_float(textstat.coleman_liau_index(text)),
        linsear_write_formula=safe_float(textstat.linsear_write_formula(text)),
        dale_chall_readability_score=safe_float(textstat.dale_chall_readability_score(text)),
        readability_consensus=str(textstat.text_standard(text, float_output=False)),
    )

