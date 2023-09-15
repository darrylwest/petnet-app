"""Tests for common validations."""

from rich import inspect
from datetime import datetime, timezone

from petnet_app.models.model_validations import ModelValidations, BirthYearError


def test_birth_year():
    validator = ModelValidations()
    today = datetime.now(tz=timezone.utc)

    year = today.year - 10

    assert validator.birth_year(year) is None


def test_birth_year_error():
    validator = ModelValidations()
    today = datetime.now(tz=timezone.utc)

    year = today.year + 1

    error = validator.birth_year(year)
    assert isinstance(error, BirthYearError)
