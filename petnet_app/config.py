"""Config the application."""


import os
from datetime import datetime, timedelta, timezone
from typing import NamedTuple

VALID_ENVIRONMENTS = frozenset({"test", "staging", "prod", "dev"})


class Config(NamedTuple):
    """Config the application configurator thingy."""

    env: str
    created: datetime
    version: str
    apikey: str
    pid: int

    @classmethod
    def create(cls, env: str = "dev"):
        """Create the config for the give env."""
        env = os.getenv("PETNET_APP_ENV", env)
        now = datetime.now(tz=timezone.utc)
        apikey = os.getenv("PETNET_APIKEY", "my-api-key")

        return cls(
            env=env,
            created=now,
            version="0.1.0",
            apikey=apikey,
            pid=os.getpid(),
        )

    def uptime(self) -> timedelta:
        """Return the time delta representing uptime."""
        now = datetime.now(tz=timezone.utc)
        return now - self.created
