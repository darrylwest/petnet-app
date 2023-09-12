"""User model."""


from typing import Self

from pydantic import BaseModel, EmailStr
from pydomkeys.keys import KeyGen

from petnet_app.models.status import Status
from petnet_app.models.version import Version

# the user keygen
keygen = KeyGen.create("US", 4)


class UserModel(BaseModel, frozen=True):
    """User data model."""

    key: str
    version: Version
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_year: int
    status: Status

    @classmethod
    def from_json(cls, json_string: str) -> Self:
        """Parse the json string and return a user model."""
        return cls.model_validate_json(json_string)

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: EmailStr,
        phone: str,
        birth_year: int,
        status: Status,
    ) -> Self:
        """Create a new user model and assign new key, version and set status."""
        key = keygen.route_key()
        version = Version.create()
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

    def update(
        self,
        first_name: str,
        last_name: str,
        email: EmailStr,
        phone: str,
        birth_year: int,
        status: Status,
    ):
        """Update the user model with updatable fields, all but key and version."""
        return UserModel(
            key=self.key,
            version=self.version,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            birth_year=birth_year,
            status=status,
        )
