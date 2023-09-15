"""Test the UserDb."""

from rich import inspect
from tests.fake_data_store import FakeDataStore
from petnet_app.db.user_db import UserDb, DataStore, DataStoreConfig
from petnet_app.models.user import UserModel, Person

from datetime import datetime, timezone

fake = FakeDataStore()


ctx = DataStoreConfig(
    base="data",
    file="user-test.json",
    keygen=UserModel.get_keygen(),
)


store = DataStore(ctx)
db = UserDb(store)


def test_save():
    model = fake.user_model()
    updated = db.save(model)

    # TODO(dpw): this should fail
    assert model == updated

    # TODO(dpw): check version updated


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
    except Exception:
        assert True


def test_fetch():
    model = fake.user_model()
    db.save(model)

    fetched = db.fetch(model.key)
    assert fetched == model


def test_fetch_bad_key():
    key = "bad-key"
    model = db.fetch(key)

    inspect(model)

    assert model is None


def test_keys():
    count = 10
    models = [fake.user_model() for _ in range(count)]
    for model in models:
        db.save(model)

    shard = 0
    keys = db.keys(shard)

    assert len(keys) >= count


def test_models():
    count = 10
    models = [fake.user_model() for _ in range(count)]
    for model in models:
        db.save(model)

    keys = [model.key for model in models]
    results = db.models(keys)
    assert len(keys) == len(results)
    assert len(models) == len(results)


def test_remove():
    model = fake.user_model()
    removed = db.remove(model)
    assert model.key == removed.key


def test_check_version():
    model = fake.user_model()
    ok = db.check_version(model)
    assert ok
