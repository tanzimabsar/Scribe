from sqlalchemy.orm import Session
from . import models, schemas
import datetime
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import configparser

# In production these configs will be places in a secure location and rotated
config = configparser.ConfigParser()
config.read("config.ini")
config = config["dev"]

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_password(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user.hashed_password


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):

    fake_hashed_password = get_password_hash(user.password)

    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def calculate_license_duration(start, end):

    start = datetime.datetime.fromisoformat(start)
    end = datetime.datetime.fromisoformat(end)
    duration = end - start
    return duration.days


def create_license(db: Session, license: schemas.LicenseCreate):

    user_id = (
        db.query(models.User).filter(models.User.id == license.user_id).first()
    )

    if user_id is None:
        return {
            "error": f"error ocurred, no user id: {license.user_id} does not exist, cannot create license for given user"
        }

    license_duration = calculate_license_duration(
        license.license_start, license.license_end
    )

    db_license = models.License(
        title=license.title,
        license_start=license.license_start,
        license_end=license.license_end,
        license_owner=license.user_id,
        license_duration=license_duration,
    )

    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license


def get_licenses(db: Session, skip: int = 0, limit: int = 100):
    """ For a given user id, create a license that the user owns """
    return db.query(models.License).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
