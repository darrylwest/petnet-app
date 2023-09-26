"""Test Data Store"""

from rich import inspect
from tests.fake_data_store import FakeDataStore
from petnet_app.db.data_store import DataStore, DataStoreConfig

fake = FakeDataStore()

cfg = DataStoreConfig.create(0, 1)


def test_exists():
    model = fake.user_model()
    store = DataStore(cfg)
    assert not store.exists(model.key), "should not exist"

    
def test_bad_connect():
    cfg = DataStoreConfig.create(0, 1)
    cfg.port = 24999
    store = DataStore(cfg)
    try:
        db = store.get_connection()
        assert False, 'should not connect'
    except ValueError:
        assert True


def test_dbsize():
    store = DataStore(cfg)
    sz = store.dbsize()
    assert sz >= 0

    model = fake.user_model()
    assert len(model.key) == 16

    store.put(model.key, model.model_dump_json())
    assert store.dbsize() == sz + 1


def test_put():
    store = DataStore(cfg)
    sz = store.dbsize()

    ref = fake.user_model()

    resp = store.put(ref.key, ref.model_dump_json())
    inspect(resp)
    assert store.dbsize() == sz + 1
