from typing import List, Literal
from db import db, Product, check_product_association, Receipt
from sqlalchemy.future import select
from sqlalchemy import desc
from logger import logger
from datetime import datetime
from sqlalchemy import and_

MAX_PAGE_SIZE = 6

async def fetch_user_products(
    user_id: int,
    offset: int = 0,
    limit: int = MAX_PAGE_SIZE,
    sort_order: Literal['asc', 'desc'] = 'desc'
) -> List[Product]:
    """Fetch products associated with a user through receipts, with pagination and sorting."""
    async with db.session() as session:  # Assuming `db.session()` returns an AsyncSession
        logger.debug(f"Fetching products for user_id {user_id} with offset {offset}, limit {limit}, and sort order {sort_order}")

        # Base query to join Receipt and Product through the association table
        query = (
            select(Product)
            .join(check_product_association)  # Join with association table
            .join(Receipt)  # Join with Receipt
            .where(Receipt.user_id == user_id)  # Filter by user ID
        )

        # Apply sorting
        if sort_order == 'desc':
            query = query.order_by(desc(Product.created_at))  # Assuming 'created_at' exists in Product
        else:
            query = query.order_by(Product.created_at)

        # Apply pagination
        query = query.offset(offset).limit(limit)

        result = await session.execute(query)
        products = result.scalars().all()

        logger.debug(f"Fetched products: {products}")

        return products


async def fetch_user_products_in_period(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    offset: int = 0,
    limit: int = MAX_PAGE_SIZE,
    sort_order: Literal['asc', 'desc'] = 'desc'
) -> List[Product]:
    """Fetch products associated with a user in a specific time period, with pagination and sorting."""
    async with db.session() as session:
        logger.debug(f"Fetching products for user_id {user_id} from {start_date} to {end_date}")

        query = (
            select(Product)
            .join(check_product_association)
            .join(Receipt)
            .where(
                and_(
                    Receipt.user_id == user_id,
                    Product.created_at >= start_date,
                    Product.created_at <= end_date
                )
            )
        )

        if sort_order == 'desc':
            query = query.order_by(desc(Product.created_at))
        else:
            query = query.order_by(Product.created_at)

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        products = result.scalars().all()

        logger.debug(f"Fetched products in period: {products}")
        return products

async def fetch_product_by_id(product_id: int) -> Product:
    """Fetch a single product by its ID."""
    async with db.session() as session:
        logger.debug(f"Fetching product with ID {product_id}")

        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        product = result.scalar_one_or_none()

        logger.debug(f"Fetched product: {product}")
        return product

#async def set_category(product_id, category):
#    """Assign category to product"""
#    async with db.session() as session:
#        query = select(Product).where(Product.id == product_id) = category

