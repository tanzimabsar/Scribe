from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

# In production these configs will be places in a secure location and rotated
config = configparser.ConfigParser()
config.read("config.ini")
config = config["dev"]

PG_USER = config["PG_USER"]
PG_PASSWORD = config["PG_PASSWORD"]

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{PG_USER}:{PG_PASSWORD}@127.0.0.1:5432/scribedev"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
