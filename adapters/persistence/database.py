"""Setup do banco de dados com SQLAlchemy 2.0."""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from saet.config.settings import get_settings


class Base(DeclarativeBase):
    """Classe base para modelos SQLAlchemy."""


def create_engine(database_url: str | None = None):
    """Cria engine do SQLAlchemy."""
    settings = get_settings()
    url = database_url or settings.database_url
    return create_async_engine(url, echo=settings.debug)


def create_session_factory(database_url: str | None = None) -> async_sessionmaker[AsyncSession]:
    """Cria factory de sessoes."""
    engine = create_engine(database_url)
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session(
    session_factory: async_sessionmaker[AsyncSession] | None = None,
) -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection para sessao do banco de dados."""
    factory = session_factory or create_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise