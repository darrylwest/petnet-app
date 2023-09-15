"""User model."""


from typing import NamedTuple, Self

from pydantic import BaseModel, EmailStr
from pydomkeys.keys import KeyGen

from petnet_app.models.model_validations import ModelValidations
from petnet_app.models.status import Status
from petnet_app.models.version import Version

# the user keygen
keygen = KeyGen.create("US", 4)

validator = ModelValidations()


class Person(NamedTuple):
    """Person tuple used to construct or update a UserModel."""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_year: int
    status: Status = Status.new(0)


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

    def validate_user(self) -> list:
        """Return a list of detected errors or an empty list."""
        errors = []
        if birth_error := validator.birth_year(self.birth_year) is not None:
            errors.append(birth_error)

        return errors

    @classmethod
    def from_json(cls, json_string: str) -> Self:
        """Parse the json string and return a user model."""
        return cls.model_validate_json(json_string)

    @classmethod
    def create(cls, person: Person) -> Self:
        """Create a new user model and assign new key, version and set status."""
        key = keygen.route_key()
        version = Version.create()
        return cls(
            key=key,
            version=version,
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            phone=person.phone,
            birth_year=person.birth_year,
            status=person.status,
        )

    def update(self, person: Person):
        """Update the user model with updatable fields, all but key and version."""
        return UserModel(
            key=self.key,
            version=self.version,
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            phone=person.phone,
            birth_year=person.birth_year,
            status=person.status,
        )

    @staticmethod
    def get_keygen() -> KeyGen:
        """Return the keygen for this user model."""
        return keygen
