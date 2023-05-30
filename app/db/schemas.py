from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from pydantic.types import conint


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    user_since: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    user_since: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class CategoryBase(BaseModel):
    category_name: str
    category_description: str
    
class CategoryCreate(BaseModel):
    category_name: str
    category_description: str
    
class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    category_description: str



class Product(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    image: Optional[str] = None
    category_id: int



class CartBase(BaseModel):
    id: int


class CartCreate(BaseModel):
    pass


class Cart(CartBase):
    id: int
    user_id: int
    products: List[Product] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
class AddProductToCartSchema(BaseModel):
    product_id : int
