"""DataStore implementing the pickle database."""

import logging
from pathlib import Path
from typing import Iterable, NamedTuple, Union

import pickledb
from pydomkeys.keys import KeyGen

log = logging.getLogger("db")

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
        base = Path(ctx.base)

        if not base.exists():
            Path.mkdir(base)

        path = base / Path(ctx.file)

        self.keygen = ctx.keygen
        self.shard_count = self.keygen.domain_router.shard_count

        self.dbs = []
        for shard in range(self.shard_count):
            full_path = path.absolute().as_posix().replace(".json", f"{shard}.json")
            self.dbs.append(pickledb.load(full_path, True))

    def dbsize(self) -> int:
        """Return the total number of rows in this data store, summing up all the shards."""
        return sum(db.totalkeys() for db in self.dbs)

    def exists(self, key: str) -> bool:
        """Return true if this key is in the database, else false."""
        shard = self.keygen.parse_route(key)
        db = self.dbs[shard]
        return db.exists(key)

    def get(self, key: str) -> Union[str, None]:
        """Get the model by key."""
        shard = self.keygen.parse_route(key)
        db = self.dbs[shard]
        if jstring := db.get(key):
            return jstring

        log.warning(f"record not found for key {key}")

        return None

    def put(self, key: str, value: str) -> bool:
        """Put/Set the key/value."""
        shard = self.keygen.parse_route(key)
        db = self.dbs[shard]
        return db.set(key, value)

    def keys_iter(self, shard: int) -> Iterable:
        """Return a generator over all keys for the given shard."""
        db = self.dbs[shard]

        return (key for key in db.getall().mapping.keys())

    def remove(self, key: str):
        """Remove the value pointed to by the key. Return true if the key exists and was deleted."""
        shard = self.keygen.parse_route(key)
        db = self.dbs[shard]
        return db.rem(key)
