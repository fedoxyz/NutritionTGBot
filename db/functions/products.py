from typing import List, Literal
from db import db, Product, check_product_association, Receipt
from sqlalchemy.future import select
from sqlalchemy import desc
from logs.logger import logger

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
