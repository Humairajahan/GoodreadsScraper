from datetime import datetime
from api.utils.dto import ScraperOutput
from api.utils.db import SessionLocal
from api.utils.models import Author, Quote, Tag


class Populate:
    session = SessionLocal()

    def __init__(self) -> None:
        pass

    def create_author(self, author_name: str):
        print("AUTHOR!!!!!!!!!!!!!!!!!!!!!!!!!")
        author_exists = (
            self.session.query(Author).filter(Author.name == author_name).first()
        )
        if not author_exists:
            new_author = Author(name=author_name)
            self.session.add(new_author)
            self.session.commit()
            self.session.refresh(new_author)
            return new_author
        return author_exists

    def create_quote(self, content: str, author_id: int, reacts: int, author):
        quote_exists = (
            self.session.query(Quote)
            .filter((Quote.content == content) & (Quote.author_id == author_id))
            .first()
        )
        print("QUOTE!!!!!!!!!!!!!!!!!!!!!!!!!")
        if not quote_exists:
            new_quote = Quote(
                content=content,
                reacts=reacts,
                date=datetime.now(),
                author_id=author_id,
                author=author,
            )
            self.session.add(new_quote)
            self.session.commit()
            self.session.refresh(new_quote)
            return new_quote
        return quote_exists

    def create_tag(self, tag: str):
        tag_exists = self.session.query(Tag).filter(Tag.tag_attr == tag).first()
        print("TAG!!!!!!!!!!!!!!!!!!!!!!!!!")
        if not tag_exists:
            new_tag = Tag(tag_attr=tag)
            self.session.add(new_tag)
            self.session.commit()
            self.session.refresh(new_tag)
            return new_tag
        return tag_exists

    def populate(self, scraped_content: ScraperOutput):
        for content in scraped_content.quotes:
            author = self.create_author(content.author)
            quote = self.create_quote(
                content=content.quote,
                author_id=author.id,
                reacts=content.likes,
                author=author,
            )
            for it in content.tags:
                tag = self.create_tag(tag=it)
                tag.quotes.append(quote)
                self.session.commit()

        self.session.close()
