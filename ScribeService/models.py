from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_joined = Column(DateTime(timezone=True), default=func.now())

    licenses = relationship("License", back_populates="owner")


class License(Base):

    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    license_start = Column(Date)
    license_end = Column(Date, index=True)
    license_duration = Column(Integer)
    license_owner = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="licenses")


class UserInDB(User):
    hashed_password: str
