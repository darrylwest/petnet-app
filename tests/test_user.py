"""Tests for user, user model, userdb"""

import pytest
from rich import inspect
import time

from datetime import datetime, timezone
from pydomkeys.keys import KeyGen
from petnet_app.models.user import Version, UserModel, keygen


def create_user_model() -> UserModel:
    now = time.time_ns()
    version = Version(
        create_date=now,
        last_update=now,
        version=1,
    )

    key = keygen.route_key()
    model = UserModel(
        key=key,
        version=version,
        first_name="First",
        last_name="Last",
        email="first@gmail.com",
        phone="555-111-2222",
        status="new",
    )

    return model


def test_create_user():
    model = create_user_model()
    inspect(model)
    assert model.first_name == "First"
    assert model.last_name == "Last"

    print(model.model_dump_json())
