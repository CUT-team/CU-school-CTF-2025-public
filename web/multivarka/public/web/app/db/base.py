import logging
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(settings.pg_url, echo=True)
Base = declarative_base()
async_session = sessionmaker(
	engine, class_=AsyncSession, expire_on_commit=False
)

async def init_models():
	logging.info("Initializing database models...")
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_session():
	async with async_session() as session:
		yield session