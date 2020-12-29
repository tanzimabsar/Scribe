from typing import List, Optional
from pydantic import BaseModel
from fastapi import Body
from datetime import date


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    date_joined: date

    class Config:
        orm_mode = True


class License(BaseModel):

    id: int
    title: str
    license_start: date
    license_end: date
    license_duration: int
    license_owner: int


class LicenseCreate(BaseModel):

    title: str
    license_start: str
    license_end: str
    user_id: int
