"""
table authors
    - id int pk
    - name str

table quotes
    - id int pk
    - content str
    - reacts int
    - date datetime
    - author_id => fk => authors.id

table tags
    - id int pk
    - tag_attr str

table quote_tag_association
    - tag_id => fk => tags.id
    - quote_id => fk => quotes.id
"""


from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Identity,
    func,
    Table,
)
from sqlalchemy.orm import relationship

from api.utils.db import Base, engine


quote_tag_association_table = Table(
    "quote_tag_association",
    Base.metadata,
    Column("quote_id", Integer, ForeignKey("quotes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, Identity(start=1000, cycle=True), primary_key=True)
    name = Column(String)

    quotes = relationship(
        "Quote", back_populates="author", cascade="all, delete-orphan"
    )

    class Config:
        orm_mode = True


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, Identity(start=1000, cycle=True), primary_key=True)
    content = Column(String)
    reacts = Column(Integer)
    date = Column(DateTime, default=func.now())
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author", back_populates="quotes")

    tags = relationship(
        "Tag", secondary=quote_tag_association_table, back_populates="quotes"
    )

    class Config:
        orm_mode = True


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, Identity(start=1000, cycle=True), primary_key=True)
    tag_attr = Column(String)

    quotes = relationship(
        "Quote", secondary=quote_tag_association_table, back_populates="tags"
    )

    class Config:
        orm_mode = True


Base.metadata.create_all(bind=engine)
