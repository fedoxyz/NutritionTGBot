from typing import List, Optional, Literal, Dict
from db import db, User, Check, Product, check_product_association
from sqlalchemy.future import select
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from logs.logger import logger

MAX_PAGE_SIZE = 6

async def new_check(user_id: int, check_data: Dict) -> Optional[Check]:
    async with db.session() as session:
        # Find the user by Telegram ID
        user = await session.execute(select(User).where(User.telegram_id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        logger.debug(f"{user.telegram_id} - is new_order.user_id")

        # Create a new Check entry
        new_check = Check(user_id=user.telegram_id, time=check_data["check_date"])
        session.add(new_check)

        # Commit to get the check ID
        try:
            await session.commit()
            logger.debug(f"Created new check: {new_check}")
        except IntegrityError as e:
            logger.error(f"Failed to commit new check: {e}")
            return None

        # Associate products with the check
        products = check_data.get("products", [])
        for product_data in products:
            product_id = product_data.get("id")
            quantity = product_data.get("quantity", 1)

            # Fetch the product by ID
            product = await session.get(Product, product_id)
            if product:
                # Insert into the association table
                stmt = check_product_association.insert().values(
                    check_id=new_check.id, product_id=product.id
                )
                await session.execute(stmt)

                # Optionally, update product quantity if needed
                if product.quantity is not None:
                    product.quantity -= quantity
                    session.add(product)

        # Final commit with the product associations
        try:
            await session.commit()
            logger.debug(f"Associated products with check: {new_check.id}")
        except IntegrityError as e:
            logger.error(f"Failed to associate products: {e}")
            return None

        return new_check

async def fetch_user_checks(
    user_id: int, 
    offset: int = 0, 
    limit: int = MAX_PAGE_SIZE, 
    sort_order: Literal['asc', 'desc'] = 'desc'
) -> List[Check]:
    async with db.session() as session:  # Assuming `db.session()` returns an AsyncSession
        logger.debug(f"Fetching orders for user_id {user_id} with offset {offset}, limit {limit}, and sort order {sort_order}")
        
        # Base query
        query = select(Check).where(Check.user_id == user_id)

        
        # Apply sorting
        if sort_order == 'desc':
            query = query.order_by(desc(Check.created_at))  # Assuming there's a 'created_at' field
        else:
            query = query.order_by(Check.created_at)
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        result = await session.execute(query)
        checks = result.scalars().all()
        
        logger.debug(f"Fetched orders: {checks}")
        
        return checks

