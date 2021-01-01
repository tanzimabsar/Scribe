from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
import configparser

tags_metadata = [
    {
        "name": "token",
        "description": "Create a temporary JWT Token (Expiry in 30 Minutes) to use to authenticate.",
    },
    {
        "name": "user",
        "description": "Manage Users, create users and get information on the current user."
    },
    {
        "name": "licenses",
        "description": "Manage Licenses, create and list licenses for the current user"
    }
]

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Scribe",
    description="Scribe API back end service",
    version="0.0.1",
    openapi_tags=tags_metadata
)

config = configparser.ConfigParser()
config.read("config.ini")
config = config["dev"]

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, username)

    if user is None:
        raise credentials_exception

    return user


@app.post("/token", tags=['token'])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # Check if the username exists in the database
    db_user = crud.get_user_by_email(db, email=form_data.username)

    if not db_user:
        raise HTTPException(
            status_code=400, detail="Email/Pasword is not correct"
        )

    # Check the password hash is correct
    password = crud.get_password(db, email=form_data.username)

    if verify_password(form_data.password, password):
        # Return a jwt token with the username encoded in it
        data = {"username": form_data.username}

        token, expire = crud.create_access_token(data=data)
        return {
            "jwt_token": token,
            "token_type": "bearer",
            "refresh_token": "random_string",
            "expires": expire,
        }

    else:
        raise HTTPException(
            status_code=400, detail="Email/Pasword is not correct"
        )


@app.post("/users/", response_model=schemas.User, tags=['user'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/me/", response_model=schemas.User, tags=['user'])
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@app.get("/licenses/", tags=['licenses'])
def get_licenses(
    db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    return crud.get_licenses(db)


@app.post("/licenses/", tags=['licenses'])
def create_license(
    license: schemas.LicenseCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    token: str = Depends(get_current_user),
):

    return crud.create_license(
        db=db, license=license, current_user=current_user
    )