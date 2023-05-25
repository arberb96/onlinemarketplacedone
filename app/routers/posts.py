from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from ..db import models, schemas
from ..db.database import get_db

from .. import utils, oauth2

#User to create post class
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    print(current_user.email)
    
    new_post = models.Post(
        title=post.title, 
        content=post.content, 
        published=post.published
    )
    
    # new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    # post_dict = new_post.dict()
    # if post_dict["id"] == None:
    #     post_dict["id"] = randrange(1, 100000)
    # my_posts.append(post_dict)
    
    return {"data": "sucessfully created!"}

@router.get("")
def get_posts(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    # post = find_post(id)
    
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, 
    #         detail=f"Post with id {id} not found"
    #     )
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
        
    return {"post_detail": f"Here post with id {id}", "data": post}


@router.put("/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    # index =  find_index_post(id=id)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
        
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    post_query.update(
        updated_post.dict(),
        # {
        #     "title": "New title which is updated!",
        #     "content": "New content which is updated!",
        # },
        synchronize_session=False
        #post.dict()
    )
    
    db.commit()
    
    
    return {"data": post_query.first()}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
        
    post.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)