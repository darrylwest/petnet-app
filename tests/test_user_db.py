"""Test the UserDb."""

from rich import inspect
from tests.fake_data_store import FakeDataStore
from petnet_app.db.user_db import UserDb, DataStore, DataStoreConfig
from petnet_app.models.user import UserModel

fake = FakeDataStore()


ctx = DataStoreConfig(
    base="data",
    file="user-test.json",
    keygen=UserModel.get_keygen(),
)


store = DataStore(ctx)
db = UserDb(store)


def test_validate():
    model = fake.user_model()
    errors = db.validate(model)

    assert len(errors) == 0


def test_save():
    model = fake.user_model()
    updated = db.save(model)

    assert model == updated


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
