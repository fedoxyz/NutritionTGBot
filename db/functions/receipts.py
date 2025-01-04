from typing import List, Optional, Literal, Dict
from db import db, User, Receipt, Product, check_product_association
from sqlalchemy.future import select
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from logger import logger

MAX_PAGE_SIZE = 6

async def new_receipt(user_id: int, receipt_data: Dict) -> Optional[Receipt]:
    async with db.session() as session:
        # Find the user by Telegram ID
        user = await session.execute(select(User).where(User.telegram_id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            logger.warning(f"User with telegram_id {user_id} not found.")
            return None

        logger.debug(f"{user.telegram_id} - is new_order.user_id")

        # Create a new Receipt entry
        new_receipt = Receipt(user_id=user.telegram_id, time=receipt_data["receipt_date"])
        session.add(new_receipt)

        # Commit to get the receipt ID
        try:
            await session.commit()
            logger.debug(f"Created new receipt: {new_receipt}")
        except IntegrityError as e:
            logger.error(f"Failed to commit new receipt: {e}")
            return None

        # Associate new products with the receipt
        products = receipt_data["products"]
        logger.debug(f"{products} - products")
        for product_data in products:
            logger.debug(f"{product_data} - product_data")

            new_product = Product(name=product_data["name"], 
                                  price=product_data["price"], 
                                  quantity=product_data["quantity"], 
                                  category=product_data['category'])

            session.add(new_product)
            logger.debug(f"Adding new product: {new_product.name}")

            # Commit to ensure the new_product has an ID
            try:
                await session.commit()  # Commit here to get new_product.id
                logger.debug(f"Created new product: {new_product}")
            except IntegrityError as e:
                logger.error(f"Failed to commit new product: {e}")
                return None

            # Insert into the association table
            stmt = check_product_association.insert().values(
                receipt_id=new_receipt.id, product_id=new_product.id
            )
            await session.execute(stmt)

        try:
            await session.commit()
            logger.debug(f"Associated new products with receipt: {new_receipt.id}")
        except IntegrityError as e:
            logger.error(f"Failed to associate products: {e}")
            return None

        return new_receipt

async def fetch_user_receipts(
    user_id: int, 
    offset: int = 0, 
    limit: int = MAX_PAGE_SIZE, 
    sort_order: Literal['asc', 'desc'] = 'desc'
) -> List[Receipt]:
    async with db.session() as session:  # Assuming `db.session()` returns an AsyncSession
        logger.debug(f"Fetching orders for user_id {user_id} with offset {offset}, limit {limit}, and sort order {sort_order}")
        
        # Base query
        query = select(Receipt).where(Receipt.user_id == user_id)

        
        # Apply sorting
        if sort_order == 'desc':
            query = query.order_by(desc(Receipt.created_at))  # Assuming there's a 'created_at' field
        else:
            query = query.order_by(Receipt.created_at)
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        result = await session.execute(query)
        receipts = result.scalars().all()
        
        logger.debug(f"Fetched orders: {receipts}")
        
        return receipts

