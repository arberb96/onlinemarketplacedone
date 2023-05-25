from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from ..db import models, schemas

from .. import utils, oauth2
from ..db.database import get_db

# Image processing
from fastapi import File, UploadFile  # For image upload
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets  # For generating random hex
import os  # For file path

# User to create post class
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/carts",
    tags=["Carts"],
)

"""
closed functions are tested and they work
"""

@router.post("", status_code=status.HTTP_201_CREATED)
def create_cart(
    #product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    
    print(f"current user: {current_user}")
    print(f"current user email : {current_user.email}")

    new_cart = models.Cart(
        owner_id=current_user.user_id,
    )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return {"data": "sucessfully created!"}



# Needs to be fixed
@router.get("")
def get_carts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    print(f"current user: {current_user}")
    carts = db.query(models.Cart).filter(models.Cart.owner_id == current_user.user_id).all()

    return {"data": carts}



@router.post("/{cart_id}")
def add_to_cart(
    cart_id: int,
    product_to_add: schemas.AddProductToCartSchema,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    
    print("this one is being printed")
    print(f"current user: {current_user}")
    print(f"cart_id : {cart_id}")
    cart = (
        db.query(models.Cart)
        .filter(models.Cart.owner_id == current_user.user_id, models.Cart.cart_id == int(cart_id))
        .first()
    )
    
    print(cart)

    if cart != []:
        try:
            product_to_add_id = product_to_add.dict()["product_id"]
            
            print(f"PRODUCT TO ADD ID - {product_to_add_id}")
            
            product = (
                db.query(models.Product).filter(models.Product.product_id == int(product_to_add_id)).first()
            )
            
            print(f"PRODUCT - {product}")
        
        except Exception as e:
            return {"status": "Failed1", "Error": e}

        try:
            
            id = len(db.query(models.Products).all()) + 1
            
            new_products = models.Products(
                product_id=id,
                product_code=product_to_add.dict()["product_id"],
                description=product.description,
                cart_id=int(cart_id),
            )
            db.add(new_products)
            db.commit()
            db.refresh(new_products)
            
            return {
                "status": "success", 
                "Cart": new_products
            }
            
        except Exception as e:
            
            return {
                "status": "Failed2", 
                "Error": e
            }

    return {
        "status": "Failed", 
        "Error": "Cart not Founded!"
    }


# @router.post("", status_code=status.HTTP_201_CREATED)
# def create_cart(
#     product: schemas.ProductCreate,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     print(current_user.email)

#     new_product = models.Product(
#         product_name=product.name,
#         product_description=product.description,
#         product_price=product.price,
#         # product_stock=product.stock,
#         owner_id=current_user.id,
#     )

#     db.add(new_product)
#     db.commit()

#     # post_dict = new_post.dict()
#     # if post_dict["id"] == None:
#     #     post_dict["id"] = randrange(1, 100000)
#     # my_posts.append(post_dict)

#     return {"data": "sucessfully created!"}


# Create a new cart
# @router.post("")
# def create_cart(
#     #cart: schemas.CartCreate,
#     db: Session = Depends(get_db),
#     user_id: int = Depends(oauth2.get_current_user),
# ):
    
#     print(user_id)
    
#     new_cart = models.Cart(
#         user_id=user_id,
#     )

#     db.add(new_cart)
#     db.commit()
#     db.refresh(new_cart)

#     return {"status": "success", "Cart": new_cart}


# Get cart by id
@router.get("/{cart_id}")
def get_cart(
    cart_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
):
    carts = (
        db.query(models.Cart)
        .filter(models.Cart.user_id == user_id, models.Cart.id == int(cart_id))
        .first()
    )

    products_in_cart = (
        db.query(models.Products).filter(models.Products.cart_id == int(cart_id)).all()
    )
    return {
        "status": "success",
        "results": 1,
        "Cart": carts,
        "products in cart": products_in_cart,
    }


# Add product to cart
@router.post("/carts/{cart_id}")
def create_cart(
    cart_id: str,
    prdc: schemas.AddProductToCartSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.get_current_user),
):
    cart = (
        db.query(models.Cart)
        .filter(models.Cart.user_id == user_id, models.Cart.id == int(cart_id))
        .first()
    )

    if cart != []:
        try:
            t_id = prdc.dict()["product_id"]
            print(t_id)
            product = (
                db.query(models.Product).filter(models.Product.id == int(t_id)).first()
            )
            print(product)
        except Exception as e:
            return {"status": "Failed1", "Error": e}

        try:
            id = len(db.query(models.Products).all()) + 1
            new_products = models.Products(
                id=id,
                product_code=prdc.dict()["product_id"],
                description=product.description,
                cart_id=int(cart_id),
            )
            db.add(new_products)
            db.commit()
            db.refresh(new_products)
            return {"status": "success", "Cart": new_products}
        except Exception as e:
            return {"status": "Failed2", "Error": e}

    return {"status": "Failed", "Error": "Cart not Founded!"}


@router.delete("/products/{products_id}")
def delete_products(
    products_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.get_current_user),
):
    products_query = db.query(models.Products).filter(
        models.Products.id == int(products_id)
    )
    products = products_query.first()
    if not products:
        return {"status": "Failed", "Error": "Product not Founded!"}

    cart = db.query(models.Cart).filter(models.Cart.id == products.cart_id).first()

    if int(user_id) != cart.user_id:
        return {"status": "Failed", "Error": "You are not the Owner!"}

    products_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "result": "Done!"}


@router.delete("/carts/{cart_id}")
def delete_cart(
    cart_id: str, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)
):
    cart_query = db.query(models.Cart).filter(models.Cart.id == int(cart_id))
    cart = cart_query.first()

    if not cart:
        return {"status": "Failed", "Error": "Cart not found!"}

    if int(user_id) != cart.user_id:
        return {"status": "Failed", "Error": "You are not the owner!"}

    cart_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "result": "Done!"}


# @router.delete("/product/{product_id}")
# def get_carts(
#     product_id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)
# ):
#     product_query = db.query(models.Product).filter(
#         models.Product.id == int(product_id)
#     )
#     product = product_query.first()

#     if not product:
#         return {"status": "Failed", "Error": "Cart not Founded!"}

#     product_query.delete(synchronize_session=False)
#     db.commit()
#     return {"status": "success", "result": "Done!"}


@router.put("/product/{product_id}")
def get_carts(
    product_id: str,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.get_current_user),
):
    product_query = db.query(models.Product).filter(
        models.Product.id == int(product_id)
    )

    product_i = product_query.first()

    if not product_i:
        return {"status": "Failed", "Error": "Product not Founded!"}

    product_query.update(product.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    
    return {"status": "success", "result": product_query}
