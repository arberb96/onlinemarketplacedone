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
    prefix="/categories",
    tags=["Categories"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    new_category = models.Category(
        category_name=category.category_name,
        category_description=category.category_description
    )

    db.add(new_category)
    db.commit()

    return {"data": "sucessfully created!"}


@router.get("")
def get_all_categories(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    
    categories = db.query(models.Category).all()

    return {"data": categories}