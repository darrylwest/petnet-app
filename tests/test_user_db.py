"""Test the UserDb."""

from tests.fake_data_store import FakeDataStore
from petnet_app.db.user_db import UserDb

fake = FakeDataStore()
db = UserDb()


def test_validate():
    model = fake.user_model()
    errors = db.validate(model)

    assert len(errors) == 0


def test_save():
    model = fake.user_model()
    updated = db.save(model)

    assert model == updated


def test_fetch_bad_key():
    key = "bad-key"
    model = db.fetch(key)
    assert model is None


def test_keys():
    keys = db.keys()

    assert len(keys) == 0


def test_remove():
    model = fake.user_model()
    removed = db.remove(model)
    assert model.key == removed.key


def test_check_version():
    model = fake.user_model()
    ok = db.check_version(model)
    assert ok
