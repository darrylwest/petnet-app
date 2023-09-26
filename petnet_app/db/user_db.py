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

        store = self.data_store
        exists = store.exists(model.key)
        if exists and not self.check_version(model):
            msg = f"version mismatch key: {model.key}, version: {model.version}"
            log.warning(msg)
            raise ModelVersionError(msg)

        model = self.update_version(model)
        pipe = store.pipeline()
        pipe.set(model.key, model.model_dump_json())  # type: ignore[attr-defined]
        pipe.set(self.email_index_key(model.email), model.key)  # type: ignore[attr-defined]
        pipe.set(self.phone_index_key(model.phone), model.key)  # type: ignore[attr-defined]

        results = pipe.execute()  # type: ignore[attr-defined]

        self.handle_save_transaction(results, model)

        pipe.reset()  # type: ignore[attr-defined]

        return model

    def handle_save_transaction(self, results: list, model: UserModel) -> None:
        """Integigate the save response."""
        if not all(results):
            log.error(f"Error saving: {model}, {results}")

    def fetch(self, key: str) -> Union[UserModel, None]:
        """Return the UserModel or None if not found."""
        log.info(f"fetch user from key: {key}")
        if jstr := self.data_store.get(key):
            user = UserModel.from_json(jstr)
            return user

        return None

    def keys_iter(self, shard: int) -> Iterable[str]:
        """Return a generator over keys for a given shard."""
        log.info(f"return a generator over all keys for the shard: {shard}")
        return self.data_store.keys_iter("US*", shard)

    def models(self, keys: Iterable[str]) -> Iterable[UserModel | None]:
        """Return a generator over the list of models from the list of keys."""
        klist = list(keys)
        log.info(f"fetch models from keys: {keys}")

        # TODO(dpw): loop over all the shards
        shard = 0
        models = [
            UserModel.from_json(jstr)
            for jstr in self.data_store.mget(klist, shard)
            if jstr is not None
        ]

        return models

    def remove(self, model: UserModel) -> Union[UserModel, None]:
        """Remove the model if it exists.  Check the version first."""
        user = self.fetch(model.key)
        if user is None:
            return model

        # TODO(dpw): fix to use pipeline and remove indexes as well
        # remove the model and item from the index

        return model

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

    def find_by_email(self, email: str) -> UserModel | None:
        """Return the user that has this unique email address, or None if not found."""
        email_key = self.email_index_key(email)
        if key := self.data_store.get(email_key):
            return self.fetch(key)

        return None

    def email_index_key(self, email: str) -> str:
        """Return the key used for this index."""
        return f"eIX{email}"

    def phone_index_key(self, phone: str) -> str:
        """Return the key used for this index."""
        return f"pIX{phone}"
