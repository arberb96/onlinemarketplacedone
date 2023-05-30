from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

#Image processing
from fastapi import File, UploadFile #For image upload
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets #For generating random hex
import os

from ..db import models, schemas #For file path
from .. import utils, oauth2
from ..db.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    #kobra
)


@router.post("", status_code=status.HTTP_201_CREATED)#, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Hash the password
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    
    template = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Verify Your Email</title>
        </head>
        <body style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.5; background-color: #f5f5f5;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                    <td align="center">
                        <table cellpadding="0" cellspacing="0" border="0" width="600" style="background-color: #ffffff;">
                            <tr>
                                    <td style="padding: 30px;">
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                        
                                            <tr>
                                                    <td style="padding-top: 30px;">
                                                        <h2 style="font-size: 24px; margin-top: 0;">Verify Your Email Address</h2>
                                                        <p style="margin-bottom: 30px;">Thank you for choosing our services! To complete your registration, please click the button below to verify your email address.</p>
                                                        <p style="margin-bottom: 30px;"><a href="http://localhost:8000/verification/?token=token" style="display: inline-block; padding: 10px 20px; background-color: #0275d8; color: #ffffff; text-decoration: none; border-radius: 5px;">Verify Your Email Address</a></p>
                                                        <p>If you did not request this verification, please ignore this message.</p>
                                                        <hr style="margin-top: 30px; margin-bottom: 30px;">
                                                        <p>If you have any questions or concerns, please contact us at <a href="mailto:support@example.com">support@babaecommerce.com</a></p>
                                                        <p>Take a look at features that we offer at <a href="https://example.com/features" style="color: #ff0000;">babaecommerce.com/features</a>.</p>
                                                        <p>If you did not request this verification, please ignore this message.</p>
                                                    </td>
                                            </tr>
                                        </table>
                                    </td>
                            </tr>
                            <tr>
                                <td style="padding: 20px; background-color: #f5f5f5; text-align: center;">
                                    <p style="font-size: 12px; color: #999999; margin: 0;">This email was sent by Baba E-Commerce</p>
                                    <p style="font-size: 12px; color: #999999; margin: 0;">Makedonska Kosovska Brigada, Skopje 1000, Republic of North Macedonia</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
        
    return {
        "status": "ok",
        "message": f"Hello, {new_user.email}! Thanks for choosing our services! " + 
        "Please check your email to activate your account.",
        #"data": new_user
    }
    
@router.post(f"/upload-profile-picture", status_code=status.HTTP_201_CREATED)
def upload_profile_picture(
    image: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    user: schemas.User = Depends(oauth2.get_current_user)
):
        
        #Generate random hex
        random_hex = secrets.token_hex(8)
        
        #Get file extension
        _, file_ext = os.path.splitext(image.filename)
        
        #Create new file name
        file_name = random_hex + file_ext
        
        #Save image
        with open(f'./static/images/{file_name}', 'wb') as f:
            f.write(image.file.read())
            
        return {
            "status": "ok",
            "message": "Image uploaded successfully!",
            "data": {
                "image_url": f"http://localhost:8000/static/images/{file_name}"
            }
        }

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
