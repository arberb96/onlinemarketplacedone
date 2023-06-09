from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db import database, models, schemas


from .. import oauth2, utils

router = APIRouter(
    tags=["Authentitation"],
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid credentials!")
        
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid credentials!")
        
    #Generate token
    access_token = oauth2.create_access_token(data={"user_id": user.user_id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    
    pass
