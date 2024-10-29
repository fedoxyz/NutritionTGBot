from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, ForeignKey, Identity, Table, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

# Association table between Check and Product
check_product_association = Table(
    'check_products',
    Base.metadata,
    Column('check_id', BigInteger, ForeignKey('checks.id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', BigInteger, ForeignKey('products.id', ondelete='SET NULL'), primary_key=True)  # Allow product deletion without affecting checks
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

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"

class Check(Base):
    __tablename__ = 'checks'

    id = Column(BigInteger, Identity(), primary_key=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False)
    time = Column(DateTime, nullable=False, default=lambda: datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Relationship with User and Products
    user = relationship('User', backref='checks')
    products = relationship('Product', secondary=check_product_association, backref='checks')

    def __repr__(self):
        return f"<Check(id={self.id}, user_id={self.user_id})>"

