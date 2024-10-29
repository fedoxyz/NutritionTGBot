import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from .models import Base, User, Check, Product, check_product_association

class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=True)
        self.AsyncSessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self):
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("Переменная среды DATABASE_URL не установлена в .env")

db = Database(DATABASE_URL)

async def init_db():
    await db.init_models()

__all__ = ['db', 'init_db', 'User', 'Check', 'Product', 'check_product_association']
