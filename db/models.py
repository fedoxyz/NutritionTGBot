from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, ForeignKey, Identity, Table, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table between Receipt and Product
check_product_association = Table(
    'receipt_products',
    Base.metadata,
    Column('receipt_id', BigInteger, ForeignKey('receipts.id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', BigInteger, ForeignKey('products.id', ondelete='SET NULL'), primary_key=True)  # Allow product deletion without affecting receipts
)

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, Identity(), nullable=False)
    telegram_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"

class Product(Base):
    __tablename__ = 'products'

    id = Column(BigInteger, Identity(), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(BigInteger, nullable=True)
    quantity = Column(Float, nullable=True)
    category = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())


    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"

class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(BigInteger, Identity(), primary_key=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False)
    time = Column(DateTime, nullable=False, default=lambda: datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Relationship with User and Products
    user = relationship('User', backref='receipts')
    products = relationship('Product', secondary=check_product_association, backref='receipts')

    def __repr__(self):
        return f"<Receipt(id={self.id}, user_id={self.user_id})>"

