"""Version Model."""

import time
from typing import Self

from pydantic import BaseModel


class Version(BaseModel):
    """Version to hold create, update and version number."""

    create_date: int
    last_update: int
    version: int

    @staticmethod
    def now() -> int:
        """Return the current time in nano-seconds."""
        return time.time_ns()

    @classmethod
    def create(cls) -> Self:
        """Create a new version."""
        now = Version.now()
        return cls(
            create_date=now,
            last_update=now,
            version=0,
        )

    # TODO(dpw): how to properly document that a Version object is being returned
    def update(self):  # -> Version:  or -> Self:
        """Update to the next version and return a copy."""
        now = Version.now()
        vers = self.version + 1
        return Version(
            create_date=self.create_date,
            last_update=now,
            version=vers,
        )
