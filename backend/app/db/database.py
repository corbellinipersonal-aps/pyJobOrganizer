from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData
from ..core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        # Create any missing tables
        await conn.run_sync(Base.metadata.create_all)
        # Add date_modified column if missing (for schema migration)
        from sqlalchemy import text
        await conn.execute(text(
            "ALTER TABLE jobs ADD COLUMN IF NOT EXISTS date_modified TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP"
        ))