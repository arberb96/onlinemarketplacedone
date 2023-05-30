from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .db import database, models, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "arberbiljali12345longlonglongverylongstring"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# class Setting(BaseModel):
#     authjwt_algorithm: str = settings.JWT_ALGORITHM
#     authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
#     authjwt_token_location: set = {"cookies", "headers"}
#     authjwt_access_cookie_key: str = "access_token"
#     authjwt_refresh_cookie_key: str = "refresh_token"
#     authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode("utf-8")
#     authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode(
#         "utf-8"
#     )


class Settings:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    SECRET_KEY = "arberbiljali12345longlonglongverylongstring"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict) -> str:
    """
    Create a new access token for a user.

    Parameters:
    -----------
    data : dict
        A dictionary containing the user's data to be included in the token.

    Returns:
    --------
    str
        A string representation of the newly created access token.
    """
    to_encode = data.copy()

    # Add expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException) -> str:
    """
    Verify the access token for a user.

    Parameters:
    -----------
    token : str
        The access token to verify.
    credentials_exception : HTTPException
        An exception to raise if the credentials cannot be validated.

    Returns:
    --------
    str
        The user ID associated with the access token, if it is valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_id=user_id)
        return user_id

    except JWTError:
        raise credentials_exception

    return user_id


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
) -> models.User:
    """
    Retrieve the current user based on their access token.

    Parameters:
    -----------
    token : str, optional
        The user's access token.
    db : Session, optional
        A SQLAlchemy database session.

    Returns:
    --------
    models.User
        The user object associated with the provided access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.user_id == token).first()

    return user




# def require_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         user_id = Authorize.get_jwt_subject()
#         user = db.query(models.User).filter(models.User.id == user_id).first()
#         if not user:
#             raise UserNotFound("User no longer exist")

#     except Exception as e:
#         error = e.__class__.__name__
#         print(error)
#         if error == "MissingTokenError":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in"
#             )
#         if error == "UserNotFound":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exist"
#             )
#         if error == "NotVerified":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Please verify your account",
#             )
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token is invalid or has expired",
#         )

#     return user_id
