from typing import Optional, List
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from api.utils.db import get_db
from api.utils.models import Author, Quote, Tag


router = APIRouter()


@router.get("/quotes/most-liked", response_model=List[dict])
async def get_most_liked_quotes(
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    author_name: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "desc",
    db: Session = Depends(get_db),
):
    query = db.query(Quote).with_entities(Quote.content, Quote.reacts, Author.name)

    query = query.join(Author, Author.id == Quote.author_id)

    if tags:
        query = query.join(Quote.tags)
        query = query.filter(Tag.tag_attr == tags)

    if author_name:
        query = query.filter(Author.name == author_name)

    if search:
        query = query.filter(Quote.content.ilike(f"%{search}%"))

    if sort == "desc":
        query = query.order_by(Quote.reacts.desc())
    else:
        query = query.order_by(Quote.reacts.asc())

    query = query.offset(skip * limit)
    query = query.limit(limit)

    quotes = query.all()

    return [
        {"content": q.content, "reacts": q.reacts, "author": q.name} for q in quotes
    ]
