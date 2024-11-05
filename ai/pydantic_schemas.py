from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from datetime import datetime

class Product(BaseModel):
    name: str = Field(description="Name of the product")  # 'required=True' is implicit
    quantity: float = Field(description="Quantity of the product")  # 'required=True' is implicit
    price: float = Field(description="Price of the product")  # 'required=True' is implicit

class ClassifiedProduct(Product):
    product: str = Field(description="Product identifier")  # 'required=True' is implicit
    category: str = Field(description="Category of the product")  # 'required=True' is implicit

class Receipt(BaseModel):
    date: datetime = Field(description="Time and date of receipt")  # 'required=True' is implicit
    products: List[Product] = Field(description="Products in receipt")  # 'required=True' is implicit

