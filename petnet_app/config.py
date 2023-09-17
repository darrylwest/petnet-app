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
        apikey = os.getenv("PETNET_APIKEY", "3b448ff245a54f16848fc5f2f69a36d5")

        return cls(
            env=env,
            created=now,
            version="0.1.0",
            apikey=apikey,
            pid=os.getpid(),
        )

    def uptime_delta(self) -> timedelta:
        """Return the timedelta of seconds and microseconds since startup."""
        now = datetime.now(tz=timezone.utc)
        return now - self.created

    def uptime(self) -> str:
        """Return the days, hours, minutes and seconds representing uptime."""
        delta = self.uptime_delta()
        days = delta.days
        return f"{days} days, {timedelta(seconds=delta.seconds)}"
