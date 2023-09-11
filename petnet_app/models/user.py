"""User model."""


from pydantic import BaseModel, EmailStr 
from typing import Self
from pydomkeys.keys import KeyGen

from petnet_app.models.version import Version

# the user keygen
keygen = KeyGen.create("US", 4)


class UserModel(BaseModel):
    """User data model."""

    key: str
    version: Version
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_year: int
    status: str

    @classmethod
    def create(cls, first_name: str, last_name: str, email: EmailStr, phone: str, birth_year: int) -> Self:
        key = keygen.route_key()
        version = Version.create()
        status = "new"
        return cls(
            key=key,
            version=version,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            birth_year=birth_year,
            status=status,
        )
