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

Work on here to add products to cart, with or without quantity

not tested yet: create_cart, get_carts, get_cart_by_id, put_cart_by_id, delete_cart_by_id
"""


@router.post("", status_code=status.HTTP_201_CREATED)
def create_cart(
    # product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_cart = models.Cart(
        owner_id=current_user.user_id,
    )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return {"data": "sucessfully created!"}


@router.get("")
def get_carts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    carts = (
        db.query(models.Cart).filter(models.Cart.owner_id == current_user.user_id).all()
    )

    return {"data": carts}


@router.get("/{cart_id}")
def get_cart_by_id(
    cart_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
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


@router.put("/{cart_id}")
def put_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    cart = (
        db.query(models.Cart)
        .filter(models.Cart.user_id == user_id, models.Cart.id == int(cart_id))
        .first()
    )
    if cart:
        cart.owner_id = user_id
        db.commit()
        return {"status": "success", "message": "Cart updated!"}
    else:
        return {"status": "error", "message": "Cart not found!"}


    
@router.delete("/{cart_id}")
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
):
    cart = (
        db.query(models.Cart)
        .filter(models.Cart.user_id == user_id, models.Cart.id == int(cart_id))
        .first()
    )
    if cart:
        db.delete(cart)
        db.commit()
        return {"status": "success", "message": "Cart deleted!"}
    else:
        return {"status": "error", "message": "Cart not found!"}
