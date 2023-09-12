"""Status module defined by a label and byte value."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Status:
    """Status of a data model with label and value."""

    label: str
    value: int

    @classmethod
    def new(cls, value: int) -> Self:
        """Return a status of new with the given value."""
        return cls("new", value)

    @classmethod
    def active(cls, value: int) -> Self:
        """Return a status of active with the given value indicating the level of activity."""
        return cls("active", value)

    @classmethod
    def inactive(cls, value: int) -> Self:
        """Return a status of inactive with the given value."""
        return cls("inactive", value)

    @classmethod
    def deleted(cls, value: int) -> Self:
        """Return a status of deleted with the given value."""
        return cls("deleted", value)
