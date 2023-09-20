"""User Db module and API."""


import logging
from typing import Iterable, Union

from petnet_app.db.data_store import DataStore
from petnet_app.models.model_validations import (ModelValidationError,
                                                 ModelVersionError)
from petnet_app.models.user import UserModel

log = logging.getLogger("db")


class UserDb:
    """UserDb API."""

    def __init__(self, data_store: DataStore):
        """Initialize UserDb with an active datastore."""
        self.data_store = data_store

    def save(self, model: UserModel) -> UserModel:
        """Save the UserModel to the database.

        Find existing from key.  if exists, compare the versions.  reject and old version.

        Validate.

        raise exception(s) group? on any error(s)

        Create a copy with new version and save to db (the correct shard.)

        Return the copy.

        """
        if errors := model.validate_user():
            msg = f"{len(errors)} detected"
            log.warning(msg)
            raise ModelValidationError(msg, errors)

        exists = self.data_store.exists(model.key)
        if exists and not self.check_version(model):
            msg = f"version mismatch key: {model.key}, version: {model.version}"
            log.warning(msg)
            raise ModelVersionError(msg)

        model = self.update_version(model)
        self.data_store.put(model.key, model.model_dump_json())
        self.update_index(model)

        return model

    def fetch(self, key: str) -> Union[UserModel, None]:
        """Return the UserModel or None if not found."""
        log.info(f"fetch user from key: {key}")
        if jstring := self.data_store.get(key):
            user = UserModel.from_json(jstring)
            self.update_index(user)
            return user

        return None

    def find_by_email(self, email: str) -> UserModel | None:
        """Find the user model where there is an exact email match."""
        id = self.data_store.index.get(email)
        if id is None:
            return None
        
        return self.fetch(id)
        
    def keys_iter(self, shard: int) -> Iterable[str]:
        """Return a generator over keys for a given shard."""
        log.info(f"return a generator over all keys for the shard: {shard}")
        return self.data_store.keys_iter(shard)

    def models(self, keys: Iterable[str]) -> Iterable[UserModel | None]:
        """Return a generator over the list of models from the list of keys."""
        log.info(f"fetch models from keys: {keys}")
        models = (self.fetch(key) for key in keys)

        return models

    def remove(self, model: UserModel) -> Union[UserModel, None]:
        """Remove the model if it exists.  Check the version first."""
        user = self.fetch(model.key)
        if user is None:
            return model

        # remove the model and item from the index
        self.data_store.remove(model.key, model.email)

        return model

    def dbsize(self) -> int:
        """Return the total number of rows in this database."""
        return self.data_store.dbsize()

    def check_version(self, model: UserModel) -> bool:
        """Return true if the version in the db matches the model's version."""
        log.info(f"check the version from model: {model}")

        user = self.fetch(model.key)
        if user is None:
            return True

        return model.version == user.version

    def update_version(self, model: UserModel) -> UserModel:
        """Update the user model's version. Return a copy."""
        vers = model.version.update()

        return UserModel(
            key=model.key,
            version=vers,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone=model.phone,
            birth_year=model.birth_year,
            status=model.status,
        )

    def update_index(self, model):
        """Update all indexes for this model."""
        self.data_store.update_index(model.email, model.key)
