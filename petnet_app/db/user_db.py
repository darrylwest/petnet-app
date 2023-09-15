"""User Db module and API."""

from pathlib import Path
from typing import Iterable, NamedTuple, Union

import pickledb
from pydomkeys.keys import KeyGen

from petnet_app.models.user import UserModel

# implement the pickle calls here then refactor to DbProtocol


class DataStoreConfig(NamedTuple):
    """DataStore config with redis unix socket or pickledb json file."""

    base: str
    file: str
    keygen: KeyGen


class DataStore:
    """DataStore a wrapper around the real k/v store."""

    def __init__(self, ctx: DataStoreConfig):
        """Initialize and connect to the database."""
        path = Path(ctx.base) / Path(ctx.file)
        self.full_path = path.absolute().as_posix()
        self.db = pickledb.load(self.full_path, False)

    # TODO(dpw): implement the data store api

    def get(self, key: str):
        """Get the model by key."""
        if jstring := self.db.get(key):
            return jstring

        return None

    def put(self, key: str, value: str):
        """Put/Set the key/value."""
        self.db.set(key, value)

    def keys(self) -> list:
        """Return a list of all keys."""
        return self.db.getall()


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
        print(f"save user from model: {model}")
        if errors := model.validate_user():
            raise ValueError(f"errors: {len(errors)}")

        # if not self.check_version(model):

        self.data_store.put(model.key, model.model_dump_json())
        return model

    def fetch(self, key: str) -> Union[UserModel, None]:
        """Return the UserModel or None if not found."""
        print(f"fetch user from key: {key}")
        if jstring := self.data_store.get(key):
            return UserModel.from_json(jstring)

        return None

    def keys(self, shard: int) -> Iterable[UserModel]:
        """Return the full list of keys for a given shard."""
        print(f"return all keys for the shard: {shard}")
        return self.data_store.keys()

    def models(self, keys: Iterable[str]) -> Iterable[UserModel]:
        """Fetch the list of models from the list of keys."""
        print(f"fetch models from keys: {keys}")
        models = [self.data_store.get(key) for key in keys]

        return models

    def remove(self, model: UserModel) -> Union[UserModel, None]:
        """Remove the model if it exists.  Check the version first."""
        print(f"remove user from model: {model}")

        return model

    def check_version(self, model: UserModel) -> bool:
        """Return true if the version in the db matches the model's version."""
        print(f"check the version from model: {model}")

        return True
