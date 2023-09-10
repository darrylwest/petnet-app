"""Tests for user, user model, userdb"""

import pytest
from rich import inspect
import time

from datetime import datetime, timezone
from pydomkeys.keys import KeyGen
from petnet_app.models.user import Version, UserModel, keygen
from faker import Faker

# TODO(dpw): put this into a library...
fake = Faker()
today = datetime.now(tz=timezone.utc)


def birth_year(min_age: int = 20, max_age: int = 100):
    return today.year - fake.random_int(min_age, max_age)


def fake_phone() -> str:
    return f"{fake.random_int(100,999)}-{fake.random_int(100,999)}-{fake.random_int(1000, 9999)}"


def fake_person() -> tuple:
    """return first, last and eamil"""
    fname = fake.first_name()
    lname = fake.last_name()
    suffix = f"{fake.random_digit_above_two()}{fake.random_digit()}"
    email = f"{fname.lower()}.{lname.lower()}-{suffix}@{fake.domain_name()}"

    return (fname, lname, email)


def create_user_model() -> UserModel:
    now = time.time_ns()
    version = Version(
        create_date=now,
        last_update=now,
        version=1,
    )

    key = keygen.route_key()
    first_name, last_name, email = fake_person()
    model = UserModel(
        key=key,
        version=version,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=fake_phone(),
        birth_year=birth_year(),
        status="new",
    )

    return model


def test_create_user():
    model = create_user_model()
    inspect(model)
    assert len(model.first_name) > 1
    assert len(model.last_name) > 1

    print(model.model_dump_json())
