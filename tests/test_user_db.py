"""Test the UserDb."""

import pytest
from rich import inspect
from tests.fake_data_store import FakeDataStore
from tests.clocker import clock
from petnet_app.db.user_db import UserDb
from petnet_app.db.data_store import DataStore, DataStoreConfig
from petnet_app.models.user import Person
from petnet_app.models.version import Version
from petnet_app.models.model_validations import ModelVersionError, ModelValidationError

from datetime import datetime, timezone

fake = FakeDataStore()


cfg = DataStoreConfig.create(0, 1)
store = DataStore(cfg)
db = UserDb(store)


@clock
@pytest.mark.redis
def test_save():
    """Save a new user model."""
    model = fake.user_model()
    updated = db.save(model)

    # TODO(dpw): this should fail
    assert model != updated
    assert model.key == updated.key
    assert model.version.create_date == updated.version.create_date
    assert model.version.create_date <= updated.version.last_update
    assert model.version.version + 1 == updated.version.version
    assert model.status == updated.status

    # TODO(dpw): check version updated


@clock
@pytest.mark.redis
def test_save_with_old_version():
    ref = fake.user_model()
    model = db.save(ref)

    try:
        db.save(ref)
        assert False, "should have raised version exception"
    except ModelVersionError as err:
        inspect(err)


@clock
@pytest.mark.redis
def test_save_bad_birth_year():
    user = fake.user_model()
    today = datetime.now(tz=timezone.utc)
    person = Person(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        birth_year=today.year + 1,
        status=user.status,
    )
    model = user.update(person)

    try:
        updated = db.save(model)
        assert False, "should have thrown an exception"
    except ModelValidationError as err:
        inspect(err)


@clock
@pytest.mark.redis
def test_find_by_email():
    model = fake.user_model()
    user = db.save(model)

    found = db.find_by_email(user.email)
    assert found.email == user.email


@clock
@pytest.mark.redis
def test_find_by_email_bad():
    model = fake.user_model()
    found = db.find_by_email(model.email)
    assert found is None


@clock
@pytest.mark.redis
def test_fetch():
    model = fake.user_model()
    model = db.save(model)

    fetched = db.fetch(model.key)
    assert fetched == model


@clock
@pytest.mark.redis
def test_fetch_bad_key():
    key = fake.route_key()
    assert db.fetch(key) is None


@clock
@pytest.mark.redis
def test_keys_iter():
    count = 10
    models = [fake.user_model() for _ in range(count)]
    for model in models:
        db.save(model)

    kiter = db.keys_iter(0)
    for i, key in enumerate(kiter):
        assert len(key) == 16
        if i >= count:
            break

    print(f"keys iterated over: {i}")

    assert i >= count


@clock
@pytest.mark.redis
def test_models():
    count = 10
    models = fake.user_models(count)
    for model in models:
        db.save(model)

    keys = [model.key for model in models]
    results = list(db.models(keys))
    assert len(keys) == len(results)
    assert len(models) == len(results)


@clock
@pytest.mark.redis
def test_remove_not_found():
    model = fake.user_model()
    removed = db.remove(model)
    assert removed.key == model.key


@clock
@pytest.mark.redis
def test_remove():
    model = fake.user_model()
    user = db.save(model)

    deleted = db.remove(user)
    assert deleted is not None


@clock
@pytest.mark.redis
def test_check_version_on_insert():
    model = fake.user_model()
    assert db.check_version(model), "user should not exist in database"


@clock
@pytest.mark.redis
def test_check_version():
    model = fake.user_model()
    user = db.save(model)

    ok = db.check_version(user)
    assert ok, "should be in database with same version"


@clock
@pytest.mark.redis
def test_check_version_bad():
    model = fake.user_model()
    user = db.save(model)

    vers = Version.update(model.version)
    assert vers != user.version, f"versions should not match: {vers}  {model.version}"

    ok = db.check_version(user)
    assert ok, "should be in database with same version"


@clock
@pytest.mark.redis
def test_bad_save_response():
    response = [True, True, False]
    model = fake.user_model()
    assert db.handle_save_transaction(response, model) is None, "should return none"
