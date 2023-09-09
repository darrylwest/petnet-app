"""User model."""

from dataclasses import dataclass

from pydantic import BaseModel, EmailStr
from pydomkeys.keys import KeyGen

# the user keygen
keygen = KeyGen.create("US", 4)


@dataclass
class Version:
    create_date: int
    last_update: int
    version: int


class UserModel(BaseModel):
    key: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: str
