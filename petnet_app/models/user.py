"""User model."""

from dataclasses import dataclass

from pydantic import BaseModel, EmailStr
from pydomkeys.keys import KeyGen

# the user keygen
keygen = KeyGen.create("US", 4)


class Version(BaseModel):
    create_date: int
    last_update: int
    version: int


class UserModel(BaseModel):
    key: str
    version: Version
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: str
