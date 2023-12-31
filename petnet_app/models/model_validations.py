"""Model Validations for common business rules."""

from datetime import datetime, timezone
from typing import Union


# pylint: disable=too-few-public-methods
class BirthYearError(ValueError):
    """BirthYearError raised if birth year > current year."""


class ModelVersionError(ValueError):
    """ModelVersionError raised if an update is attempted on an out-of-date model version."""


class ModelValidationError(ValueError):
    """ModelValidationError raised if the model is not valid."""


class ModelValidations:
    """Common data model validations shared between models."""

    def birth_year(self, year: int) -> Union[BirthYearError, None]:
        """Verify that the birth year is not in the future."""
        today = datetime.now(tz=timezone.utc)

        if year > today.year:
            return BirthYearError(f"Birth year must be in the past, got {year}")

        return None
