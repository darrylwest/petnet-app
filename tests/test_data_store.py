"""Test Data Store"""

from rich import inspect
from pydomkeys.keys import KeyGen
from tests.fake_data_store import FakeDataStore
from petnet_app.db.data_store import DataStore, DataStoreConfig

fake = FakeDataStore()

keygen = KeyGen.create("ST", 1)

cfg = DataStoreConfig.create(keygen)

store = DataStore(cfg)


def test_exists():
    key = cfg.keygen.route_key()
    assert not store.exists(key), "should not exist"


def test_dbsize():
    sz = store.dbsize()
    assert sz >= 0

    model = fake.user_model()
    assert len(model.key) == 16

    store.put(model.key, model.model_dump_json())
    assert store.dbsize() == sz + 1


def test_put():
    sz = store.dbsize()

    ref = fake.user_model()

    resp = store.put(ref.key, ref.model_dump_json())
    inspect(resp)
    assert store.dbsize() == sz + 1
