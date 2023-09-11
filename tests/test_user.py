"""Tests for user, user model, userdb"""

from rich import inspect
import time

from tests.fake_data_store import FakeDataStore
from petnet_app.models.user import Version, UserModel, keygen
from petnet_app.models.status import Status


fake = FakeDataStore()


def create_user_model() -> UserModel:
    now = time.time_ns()
    version = Version(
        create_date=now,
        last_update=now,
        version=1,
    )

    key = keygen.route_key()
    first_name, last_name, email = fake.person()
    model = UserModel(
        key=key,
        version=version,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=fake.phone(),
        birth_year=fake.birth_year(),
        status=Status.new(128),
    )

    return model


def test_user():
    model = create_user_model()
    inspect(model)
    assert len(model.first_name) > 1
    assert len(model.last_name) > 1

    print(model.model_dump_json())


def test_create():
    user = create_user_model()
    model = UserModel.create(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        birth_year=user.birth_year,
        status=Status.active(128),
    )
    inspect(model)
    assert len(model.first_name) > 1
    assert len(model.last_name) > 1
    assert model.version.create_date == model.version.last_update
    assert model.version.version == 0
    assert model.status.label == "active"
    assert model.status.value == 128


def test_update():
    model = fake.user_model()

    inspect(model)
    assert model.version.create_date == model.version.last_update

    # TODO(dpw): test that an attempt to change a field will raise and exception

    first_name, last_name, email = fake.person()

    updated = model.update(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=fake.phone(),
        birth_year=model.birth_year,
        status=Status.active(0),
    )

    assert updated.key == model.key
    assert updated.version == model.version
    assert updated.first_name == first_name
    assert updated.last_name == last_name
    assert updated.email == email
    assert updated.birth_year == model.birth_year
    assert updated.status.label == "active"
    assert updated.status.value == 0
