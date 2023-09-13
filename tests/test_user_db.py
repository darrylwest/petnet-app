"""Test the UserDb."""

from rich import inspect
from tests.fake_data_store import FakeDataStore
from petnet_app.db.user_db import UserDb, DataStore
from petnet_app.models.user import UserModel

fake = FakeDataStore()


ctx = {
    "base": "data",
    "file": "user-test.json",
    "keygen": UserModel.get_keygen(),
}

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
    shard = 0
    keys = db.keys(shard)

    assert len(keys) == 0


def test_models():
    keys = []
    models = db.models(keys)
    assert len(keys) == len(models)


def test_remove():
    model = fake.user_model()
    removed = db.remove(model)
    assert model.key == removed.key


def test_check_version():
    model = fake.user_model()
    ok = db.check_version(model)
    assert ok
