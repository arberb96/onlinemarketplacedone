from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# class Post(Base):
#     __tablename__ = "posts"
    
#     id = Column(Integer, primary_key=True, index=True, nullable=False)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, server_default='TRUE', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, server_default='FALSE', nullable=False)
    user_since = Column(
        TIMESTAMP(timezone=True),
        nullable=False, 
        server_default=text('now()'))
 
    
class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True, nullable=False)
    product_title = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    product_price = Column(Integer, nullable=False)
    product_image = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)


class Category(Base):
    __tablename__ = "categories"
    
    category_id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String, nullable=False, unique=True)
    category_description = Column(String, nullable=False)


class Cart(Base):
    __tablename__= 'carts'
    
    cart_id = Column(Integer, primary_key=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    user = relationship('User')


class CartProducts(Base):
    __tablename__= 'cart_products'
    
    cart_products_id = Column(Integer, primary_key=True, nullable=False)
    cart_id = Column(Integer, ForeignKey('carts.cart_id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    
    cart = relationship('Cart')
    product = relationship('Product')
