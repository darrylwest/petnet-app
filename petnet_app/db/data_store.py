"""DataStore implementing the pickle database."""

from pathlib import Path
from typing import Iterable, NamedTuple, Union

import pickledb
from pydomkeys.keys import KeyGen

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
        self.db = pickledb.load(self.full_path, True)

    # TODO(dpw): implement the data store api

    def dbsize(self) -> int:
        """Return the total number of rows in this data store."""
        return self.db.totalkeys()

    def get(self, key: str) -> Union[str, None]:
        """Get the model by key."""
        if jstring := self.db.get(key):
            return jstring

        return None

    def put(self, key: str, value: str) -> bool:
        """Put/Set the key/value."""
        return self.db.set(key, value)

    def keys(self) -> Iterable:
        """Return an iterable over all keys."""
        return self.db.getall()

    def remove(self, key: str):
        """Remove the value pointed to by the key. Return true if the key exists and was deleted."""
        return self.db.rem(key)
