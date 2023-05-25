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
    prefix="/products",
    tags=["Products"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    new_product = models.Product(
        product_title=product.title,
        product_description=product.description,
        product_image=product.image,
        product_price=product.price,
        category_id=product.category_id,
        owner_id=current_user.user_id,
    )

    db.add(new_product)
    db.commit()

    return {"data": "sucessfully created!"}

@router.get("")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return {"data": products}

@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    
    product = db.query(models.Product).filter(models.Product.product_id == id).first()
    
    return product

@router.get("/category={id}")
def get_product_by_category(id: int, db: Session = Depends(get_db)):
    
    products = db.query(models.Product).filter(models.Product.category_id == id).all()
    
    return products

# Needs to be fixed
@router.post(f"/upload-product-picture", status_code=status.HTTP_201_CREATED)
def upload_product_picture(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    FILE_PATH = "./app/static/images/"

    # Generate random hex
    random_hex = secrets.token_hex(8)

    # Get file extension
    _, file_ext = os.path.splitext(image.filename)

    # Create new file name
    file_name = random_hex + file_ext

    # Save image
    with open(f"{FILE_PATH}/{file_name}", "wb") as f:
        f.write(image.file.read())

    return {
        "status": "ok",
        "message": "Image uploaded successfully!",
        "data": {"image_url": f"http://localhost:8000/static/images/{file_name}"},
    }
