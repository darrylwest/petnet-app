"""User Db module and API."""

from typing import Iterable, Union

from petnet_app.models.user import UserModel

# implement the pickle calls here then refactor to DbProtocol


class UserDb:
    """UserDb API."""

    def validate(self, model: UserModel) -> list:
        """Return any detected validation errors, or and empty list."""
        print(f"validate user model: {model}")
        return []

    def save(self, model: UserModel) -> UserModel:
        """Save the UserModel to the database.

        Find existing from key.  if exists, compare the versions.  reject and old version.

        Validate.

        raise exception(s) group? on any error(s)

        Create a copy with new version and save to db (the correct shard.)

        Return the copy.

        """
        print(f"save user from model: {model}")
        return model

    def fetch(self, key: str) -> Union[UserModel, None]:
        """Return the UserModel or None if not found."""
        print(f"fetch user from key: {key}")
        return None

    def keys(self, shard: int) -> Iterable[UserModel]:
        """Return the full list of keys for a given shard."""
        print(f"return all keys for the shard: {shard}")
        return []

    def models(self, keys: Iterable[str]) -> Iterable[UserModel]:
        """Fetch the list of models from the list of keys."""
        print(f"fetch models from keys: {keys}")

        return []

    def remove(self, model: UserModel) -> Union[UserModel, None]:
        """Remove the model if it exists.  Check the version first."""
        print(f"remove user from model: {model}")

        return model

    def check_version(self, model: UserModel) -> bool:
        """Return true if the version in the db matches the model's version."""
        print(f"check the version from model: {model}")

        return True
