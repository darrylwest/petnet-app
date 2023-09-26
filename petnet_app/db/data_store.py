"""DataStore implementing the pickle database."""

import logging
import os
from dataclasses import dataclass
from typing import Iterable, Self, Union

import redis
from redis.client import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

log = logging.getLogger("db")


@dataclass
class DataStoreConfig:
    """DataStore config with redis unix socket or pickledb json file."""

    env: str
    name: str
    host: str
    port: int
    auth: str
    db_number: int
    shard_count: int

    @classmethod
    def create(cls, db_number: int, shard_count: int = 1) -> Self:
        """Create the db config instance with the model's db number and shard count."""
        env = os.getenv("PETNET_ENV", "dev")
        auth = os.getenv("PETNET_DBAUTH", "bad-auth")
        port = int(os.getenv("PETNET_DBPORT", "0"))
        host = os.getenv("PETNET_DBHOST", "")
        name = f"pet-db-{port}"

        cfg = cls(
            env=env,
            name=name,
            host=host,
            port=port,
            auth=auth,
            db_number=db_number,
            shard_count=shard_count,
        )

        # TODO(dpw): validate this first...

        return cfg


class DataStore:
    """DataStore a wrapper around the real k/v store."""

    def __init__(self, cfg: DataStoreConfig):
        """Initialize and connect to the database."""
        self.cfg = cfg
        self.conn = [None for _ in range(cfg.shard_count)]

    def connect(self, shard: int) -> Redis:
        """Connect to redis using shard."""
        cfg = self.cfg
        port = cfg.port + shard
        name = f"{cfg.name}-{shard}"
        dbnum = 1

        db = redis.Redis(
            host=cfg.host,
            port=port,
            password=cfg.auth,
            client_name=name,
            health_check_interval=30,
            db=dbnum,
        )

        # this is to establish the RESP 3 protocol
        db.connection_pool.get_connection("PING", None).send_command("HELLO", 3)

        self.conn[shard] = db  # type: ignore[call-overload]

        return db

    def get_connection(self, shard: int = 0):
        """Return the redis connection for the specified shard."""
        if self.conn[shard] is None:
            try:
                self.connect(shard)
            except RedisConnectionError as err:
                cfg = self.cfg
                err.add_note(
                    f"Redis connection error attempting to connect to {cfg.name}-{shard}",
                )
                err.add_note(f"{cfg.host}:{cfg.port + shard} -> {err}")
                raise ValueError("redis connect error") from err

        return self.conn[shard]

    def dbsize(self) -> int:
        """Return the total number of rows in this data store, summing up all the shards."""
        db = self.get_connection(0)
        return db.dbsize()

    def pipeline(self, shard: int = 0) -> bool:
        """Return a pipeline for the specified shard."""
        db = self.get_connection(shard)
        return db.pipeline()

    def exists(self, key: str, shard: int = 0) -> bool:
        """Return True if this key is in the database, else False."""
        db = self.get_connection(shard)

        return db.exists(key) == 1

    def get(self, key: str, shard: int = 0) -> Union[str, None]:
        """Get the model by key."""
        db = self.get_connection(shard)
        return db.get(key)

    def mget(self, key_list: list, shard: int = 0) -> list[str]:
        """Return a list of json strings from the list of keys. Filter out None types."""
        db = self.get_connection(shard)
        return [jstr for jstr in db.mget(key_list) if jstr is not None]

    def put(self, key: str, value: str, shard: int = 0) -> bool:
        """Put/Set the key/value."""
        db = self.get_connection(shard)
        return db.set(key, value)

    def keys_iter(self, prefix: str = "*", shard: int = 0) -> Iterable:
        """Return a generator over all keys for the given shard."""
        db = self.get_connection(shard)

        return db.scan_iter(prefix)
