"""SQLAlchemy engine and request-scoped session configuration."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base class for application database models."""


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set before using the database")
    return database_url


def create_database_engine():
    return create_engine(get_database_url(), pool_pre_ping=True)


engine = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    global engine
    if engine is None:
        engine = create_database_engine()
        SessionLocal.configure(bind=engine)

    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()