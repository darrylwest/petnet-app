"""User model."""


from pydantic import BaseModel, EmailStr
from pydomkeys.keys import KeyGen

# the user keygen
keygen = KeyGen.create("US", 4)


class Version(BaseModel):
    """Version to hold create, update and version number."""

    create_date: int
    last_update: int
    version: int


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
