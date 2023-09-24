"""DataStore implementing the pickle database."""

import logging
from pathlib import Path
from typing import Iterable, Union, Self
from dataclasses import dataclass
import os

import redis
from redis.client import Redis
# from redis.exceptions import DbConnectError

from pydomkeys.keys import KeyGen

log = logging.getLogger("db")



@dataclass
class DataStoreConfig():
    """DataStore config with redis unix socket or pickledb json file."""

    env: str
    name: str
    host: str
    port: int
    auth: str
    keygen: KeyGen

    @classmethod
    def create(cls, keygen: KeyGen) -> Self:
        """Create the db config instance."""
        env = os.getenv("PETNET_ENV", "dev")
        auth = os.getenv("PETNET_DBAUTH")
        port = int(os.getenv("PETNET_DBPORT"))

        cfg = cls(
            env=env,
            name="petnet-db",
            host="localhost",
            port=port,
            keygen=keygen,
            auth=auth,
        )

        # TODO(dpw): validate this first...
        
        return cfg


class DataStore:
    """DataStore a wrapper around the real k/v store."""

    def __init__(self, cfg: DataStoreConfig):
        """Initialize and connect to the database."""
        self.cfg = cfg

        self.keygen = cfg.keygen
        self.shard_count = self.keygen.domain_router.shard_count

        self.conn = [None for _ in range(self.shard_count)]


    def connect(self, shard: int) -> Redis:
        """Connect to redis using shard."""
        cfg = self.cfg
        port = cfg.port + shard
        name = f"{cfg.name}-{shard}"

        db = redis.Redis(
            host=cfg.host,
            port=port,
            password=cfg.auth,
            client_name=name,
            health_check_interval=30,
        )

        self.conn[shard] = db

        return db

    def get_connection(self, shard: int = 0):
        """Return the redis connection for the specified shard."""
        return self.conn[shard] if self.conn[shard] is not None else self.connect(shard)

    def dbsize(self) -> int:
        """Return the total number of rows in this data store, summing up all the shards."""
        return 0

    def exists(self, key: str) -> bool:
        """Return true if this key is in the database, else false."""
        # shard = self.keygen.parse_route(key)
        return false

    def get(self, key: str) -> Union[str, None]:
        """Get the model by key."""
        # shard = self.keygen.parse_route(key)
        return None


    def put(self, key: str, value: str) -> bool:
        """Put/Set the key/value."""
        # shard = self.keygen.parse_route(key)
        return db.set(key, value)

    def keys_iter(self, shard: int) -> Iterable:
        """Return a generator over all keys for the given shard."""
        db = self.dbs[shard]

        return (key for key in db.getall().mapping.keys())

    def remove(self, key: str, index_key: str):
        """Remove the value pointed to by the key. Return true if the key exists and was deleted."""
        shard = self.keygen.parse_route(key)
        db = self.dbs[shard]
        self.index.rem(index_key)

        return db.rem(key)

    def update_index(self, key, value):
        """Update the index."""
        self.index.set(key, value)
