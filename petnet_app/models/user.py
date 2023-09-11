"""User model."""


from pydantic import BaseModel, EmailStr
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
