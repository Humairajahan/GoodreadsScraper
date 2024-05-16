from typing import List
from pydantic import BaseModel


class Quote(BaseModel):
    quote: str
    author: str
    tags: List[str] = None
    likes: int


class ScraperOutput(BaseModel):
    total_quote_count: int = None
    quotes: List[Quote]


class ScrapeIn(BaseModel):
    url: str = "https://www.goodreads.com/quotes/tag/life"
    page: int = 1


class ScrapedQuote(BaseModel):
    quote: str
    author: str


class ScrapeOut(ScraperOutput):
    quotes: List[ScrapedQuote]
