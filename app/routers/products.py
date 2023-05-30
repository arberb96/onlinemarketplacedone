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

@router.get("/search={search}")
def get_product_by_search(
    search_string: str, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    
    products_query = (
        db.query(models.Product)
        .filter(models.Product.product_title.ilike(f"%{search_string}%"), models.Product.owner_id == current_user.user_id)
    )
    
    products = products_query.all()
    
    if products == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with title {search_string} not found"
        )
    else:
        return {"data": products}


@router.put("/{id}")
def update_product(
    id: int, 
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
    ):

    product_query = db.query(models.Product).filter(models.Product.id == id)
    
    product = product_query.first()
    
    if product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )
    
    product_query.update(
        updated_product.dict(),
        synchronize_session=False
    )
    
    db.commit()
    
    return {"data": product_query.first()}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    product = db.query(models.Product).filter(models.Product.id == id)
    
    if product.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
        
    product.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

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
