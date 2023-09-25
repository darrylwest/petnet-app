"""Tests for user, user model, userdb"""

from rich import inspect
import time

from tests.fake_data_store import FakeDataStore
from petnet_app.models.user import Version, Person, UserModel, keygen
from petnet_app.models.status import Status

from datetime import datetime, timezone

fake = FakeDataStore()


def create_user_model() -> UserModel:
    now = time.time_ns()
    version = Version(
        create_date=now,
        last_update=now,
        version=1,
    )

    key = keygen.route_key()
    person = fake.person()
    inspect(f"person: {person}")
    model = UserModel(
        key=key,
        version=version,
        first_name=person.first_name,
        last_name=person.last_name,
        email=person.email,
        phone=person.phone,
        birth_year=person.birth_year,
        status=Status.new(128),
    )

    return model


def test_validate_user():
    model = fake.user_model()
    errors = model.validate_user()

    assert len(errors) == 0


def test_validate_birth_year():
    user = fake.user_model()
    today = datetime.now(tz=timezone.utc)
    person = Person(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        birth_year=today.year + 1,
        status=Status.active(128),
    )
    model = user.update(person)

    errors = model.validate_user()

    assert len(errors) == 1


def test_user():
    model = create_user_model()
    inspect(model)
    assert len(model.first_name) > 1
    assert len(model.last_name) > 1

    print(model.model_dump_json())


def test_from_json():
    ref = create_user_model()
    jmodel = ref.model_dump_json()
    model = UserModel.from_json(jmodel)

    assert isinstance(model, UserModel)
    assert ref == model


def test_from_json_bad():
    jstr = '{"bad":"json"}'
    resp = UserModel.from_json(jstr)
    assert resp is None


def test_create():
    user = create_user_model()
    person = Person(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        birth_year=user.birth_year,
        status=Status.active(128),
    )

    model = UserModel.create(person)
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

    person = fake.person()
    person.birth_year = model.birth_year
    person.status = Status.active(127)

    updated = model.update(person)

    assert updated.key == model.key
    assert updated.version == model.version
    assert updated.first_name == person.first_name
    assert updated.last_name == person.last_name
    assert updated.email == person.email
    assert updated.birth_year == model.birth_year
    assert updated.status.label == "active"
    assert updated.status.value == 127


def test_to_persion():
    model = fake.user_model()
    person = model.to_person()
    assert model.email == person.email
    assert model.phone == person.phone
    assert model.status == person.status


def test_is_valid_key():
    model = fake.user_model()
    assert UserModel.is_valid_key(model.key)


def test_get_keygen():
    assert UserModel.get_keygen() is not None
