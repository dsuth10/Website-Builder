from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from ..core.db import get_session
from ..models import ContentItem, ContentVersion, VersionStatus
from ..schemas import GenerateRequest, ItemOut, ItemDetailOut, VersionOut, ImportItemIn, ImportItemsIn
from ..services.ai import AIClient
from ..services.pdf import html_to_pdf_bytes
from ..services.readability import compute_metrics
from itsdangerous import URLSafeSerializer


router = APIRouter(prefix="/api/content", tags=["content"])


def to_version_out(v: ContentVersion) -> VersionOut:
    return VersionOut(
        id=v.id,  # type: ignore[arg-type]
        version=v.version,
        status=v.status,
        reading_level=v.reading_level,
        grade=v.grade,
        genre=v.genre,
        topic=v.topic,
        created_at=v.created_at,
        published_at=v.published_at,
        word_count=v.word_count,
        difficult_words_count=v.difficult_words_count,
        flesch_reading_ease=v.flesch_reading_ease,
        flesch_kincaid_grade=v.flesch_kincaid_grade,
        gunning_fog=v.gunning_fog,
        smog_index=v.smog_index,
        automated_readability_index=v.automated_readability_index,
        coleman_liau_index=v.coleman_liau_index,
        linsear_write_formula=v.linsear_write_formula,
        dale_chall_readability_score=v.dale_chall_readability_score,
        readability_consensus=v.readability_consensus,
    )


@router.post("/generate", response_model=ItemOut)
async def generate_content(payload: GenerateRequest, session: AsyncSession = Depends(get_session)):
    # derive title when blank
    title = (payload.title or "").strip()
    if not title:
        title = payload.topic.strip()

    # slug by normalized title
    slug = (
        title.lower().strip().replace(" ", "-").replace("/", "-").replace("_", "-")
    )

    # ensure item exists
    result = await session.execute(select(ContentItem).where(ContentItem.slug == slug))
    item = result.scalar_one_or_none()
    if not item:
        item = ContentItem(title=title, slug=slug)
        session.add(item)
        await session.flush()

    # next version number
    vres = await session.execute(
        select(func.max(ContentVersion.version)).where(ContentVersion.item_id == item.id)
    )
    max_ver = vres.scalar() or 0
    next_ver = max_ver + 1

    # generate html
    target_level = payload.grade or payload.reading_level or "Grade 5"
    html = await AIClient().generate_html(
        title=title, topic=payload.topic, reading_level=target_level
    )

    # compute readability/text stats
    m = compute_metrics(html)

    version = ContentVersion(
        item_id=item.id,  # type: ignore[arg-type]
        version=next_ver,
        status=VersionStatus.draft,
        reading_level=payload.reading_level,
        grade=payload.grade or payload.reading_level,
        genre=payload.genre,
        topic=payload.topic,
        body_html=html,
        word_count=m.word_count,
        difficult_words_count=m.difficult_words_count,
        flesch_reading_ease=m.flesch_reading_ease,
        flesch_kincaid_grade=m.flesch_kincaid_grade,
        gunning_fog=m.gunning_fog,
        smog_index=m.smog_index,
        automated_readability_index=m.automated_readability_index,
        coleman_liau_index=m.coleman_liau_index,
        linsear_write_formula=m.linsear_write_formula,
        dale_chall_readability_score=m.dale_chall_readability_score,
        readability_consensus=m.readability_consensus,
    )
    session.add(version)
    await session.commit()
    await session.refresh(item)

    latest = to_version_out(version)
    return ItemOut(id=item.id, title=item.title, slug=item.slug, latest_version=latest)  # type: ignore[arg-type]


@router.get("/", response_model=list[ItemOut])
async def list_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ContentItem))
    items = result.scalars().all()

    out: list[ItemOut] = []
    for item in items:
        vres = await session.execute(
            select(ContentVersion).where(ContentVersion.item_id == item.id).order_by(ContentVersion.version.desc()).limit(1)
        )
        latest = vres.scalar_one_or_none()
        out.append(
            ItemOut(
                id=item.id,  # type: ignore[arg-type]
                title=item.title,
                slug=item.slug,
                latest_version=to_version_out(latest) if latest else None,
            )
        )
    return out


@router.get("/{item_id}", response_model=ItemDetailOut)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = (await session.execute(select(ContentItem).where(ContentItem.id == item_id))).scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Item not found")

    versions = (
        await session.execute(
            select(ContentVersion).where(ContentVersion.item_id == item.id).order_by(ContentVersion.version.desc())
        )
    ).scalars().all()

    return ItemDetailOut(
        id=item.id,  # type: ignore[arg-type]
        title=item.title,
        slug=item.slug,
        versions=[to_version_out(v) for v in versions],
    )


@router.post("/{item_id}/versions/{version_id}/publish", response_model=VersionOut)
async def publish_version(item_id: int, version_id: int, session: AsyncSession = Depends(get_session)):
    version = (
        await session.execute(
            select(ContentVersion).where(ContentVersion.id == version_id, ContentVersion.item_id == item_id)
        )
    ).scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")

    # archive currently published
    published_versions = (
        await session.execute(
            select(ContentVersion).where(
                ContentVersion.item_id == item_id, ContentVersion.status == VersionStatus.published
            )
        )
    ).scalars().all()
    for pv in published_versions:
        pv.status = VersionStatus.archived

    version.status = VersionStatus.published
    from datetime import datetime

    version.published_at = datetime.utcnow()
    await session.commit()
    await session.refresh(version)
    return to_version_out(version)


@router.get("/{item_id}/versions/{version_id}/html")
async def get_version_html(item_id: int, version_id: int, session: AsyncSession = Depends(get_session)):
    version = (
        await session.execute(
            select(ContentVersion).where(ContentVersion.id == version_id, ContentVersion.item_id == item_id)
        )
    ).scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")
    return Response(content=version.body_html, media_type="text/html")


@router.get("/{item_id}/versions/{version_id}/pdf")
async def get_version_pdf(item_id: int, version_id: int, session: AsyncSession = Depends(get_session)):
    version = (
        await session.execute(
            select(ContentVersion).where(ContentVersion.id == version_id, ContentVersion.item_id == item_id)
        )
    ).scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")

    pdf_bytes = html_to_pdf_bytes(version.body_html, title=f"{version.topic or 'Content'}")
    return StreamingResponse(iter([pdf_bytes]), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=content_{item_id}_v{version.version}.pdf"
    })


@router.get("/share/{token}")
async def share_view(token: str, session: AsyncSession = Depends(get_session)):
    # simple share link encoder: item_id:version_id
    s = URLSafeSerializer("share-secret")
    try:
        payload = s.loads(token)
    except Exception:
        raise HTTPException(400, "Invalid token")
    item_id = int(payload.get("item_id"))
    version_id = int(payload.get("version_id"))
    version = (
        await session.execute(
            select(ContentVersion).where(ContentVersion.id == version_id, ContentVersion.item_id == item_id)
        )
    ).scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")
    return Response(content=version.body_html, media_type="text/html")


@router.get("/{item_id}/export")
async def export_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = (await session.execute(select(ContentItem).where(ContentItem.id == item_id))).scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Item not found")
    versions = (
        await session.execute(select(ContentVersion).where(ContentVersion.item_id == item.id).order_by(ContentVersion.version.asc()))
    ).scalars().all()

    data = {
        "title": item.title,
        "slug": item.slug,
        "versions": [
            {
                "version": v.version,
                "status": v.status,
                "reading_level": v.reading_level,
                "grade": v.grade,
                "genre": v.genre,
                "topic": v.topic,
                "body_html": v.body_html,
                "word_count": v.word_count,
                "difficult_words_count": v.difficult_words_count,
                "flesch_reading_ease": v.flesch_reading_ease,
                "flesch_kincaid_grade": v.flesch_kincaid_grade,
                "gunning_fog": v.gunning_fog,
                "smog_index": v.smog_index,
                "automated_readability_index": v.automated_readability_index,
                "coleman_liau_index": v.coleman_liau_index,
                "linsear_write_formula": v.linsear_write_formula,
                "dale_chall_readability_score": v.dale_chall_readability_score,
                "readability_consensus": v.readability_consensus,
            }
            for v in versions
        ],
    }
    from fastapi.responses import JSONResponse
    return JSONResponse(data)


@router.post("/import")
async def import_items(payload: ImportItemsIn | ImportItemIn, session: AsyncSession = Depends(get_session)):
    # Support both single item and wrapper { items: [...] }
    items: list[ImportItemIn]
    if isinstance(payload, ImportItemsIn):
        items = payload.items
    else:
        items = [payload]

    created = []
    for item_in in items:
        title = item_in.title
        slug = (item_in.slug or title).lower().strip().replace(" ", "-").replace("/", "-").replace("_", "-")
        existing = (await session.execute(select(ContentItem).where(ContentItem.slug == slug))).scalar_one_or_none()
        if not existing:
            existing = ContentItem(title=title, slug=slug)
            session.add(existing)
            await session.flush()

        vres = await session.execute(
            select(func.max(ContentVersion.version)).where(ContentVersion.item_id == existing.id)
        )
        max_ver = vres.scalar() or 0

        for vin in item_in.versions:
            ver_no = vin.version or (max_ver + 1)
            max_ver = max(max_ver, ver_no)
            v = ContentVersion(
                item_id=existing.id,  # type: ignore[arg-type]
                version=ver_no,
                status=vin.status or VersionStatus.draft,
                reading_level=vin.reading_level,
                grade=vin.grade or vin.reading_level,
                genre=vin.genre,
                topic=vin.topic,
                body_html=vin.body_html,
                word_count=vin.word_count,
                difficult_words_count=vin.difficult_words_count,
                flesch_reading_ease=vin.flesch_reading_ease,
                flesch_kincaid_grade=vin.flesch_kincaid_grade,
                gunning_fog=vin.gunning_fog,
                smog_index=vin.smog_index,
                automated_readability_index=vin.automated_readability_index,
                coleman_liau_index=vin.coleman_liau_index,
                linsear_write_formula=vin.linsear_write_formula,
                dale_chall_readability_score=vin.dale_chall_readability_score,
                readability_consensus=vin.readability_consensus,
            )
            session.add(v)
        created.append({"title": existing.title, "slug": existing.slug, "versions": max_ver})

    await session.commit()
    return {"imported": created}
