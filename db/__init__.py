import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy import text
from .models import Base, User, Receipt, Product, check_product_association

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

    async def reset_db(self):
         """Drop and recreate all tables, handling dependencies."""
         async with self.engine.begin() as conn:
             await conn.execute(text("DROP TABLE IF EXISTS receipt_products CASCADE"))
             await conn.execute(text("DROP TABLE IF EXISTS products CASCADE"))
             await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
             await conn.execute(text("DROP TABLE IF EXISTS receipts CASCADE"))
             
             # Recreate all tables
             await conn.run_sync(Base.metadata.create_all)


DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("Переменная среды DATABASE_URL не установлена в .env")

db = Database(DATABASE_URL)

async def init_db():
    await db.reset_db() # Использовать при дебаге
    await db.init_models()

__all__ = ['db', 'init_db', 'User', 'Receipt', 'Product', 'check_product_association']
