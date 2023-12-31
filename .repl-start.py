import sys
import os

from pathlib import Path

import time
from datetime import datetime
# import importlib

from rich import inspect
import platform

# print("pid=", os.getpid())

user_home = Path.home().as_posix()

if platform.system() == 'Linux':
    libpath = Path(f'{user_home}/.cache/pypoetry/virtualenvs/petnet-app-c3NNDXsb-py3.11/lib/python3.11/site-packages').as_posix()
else:
    libpath = Path(f'{user_home}/Library/Caches/pypoetry/virtualenvs/petnet-app-I8h4Bcsw-py3.11/lib/python3.11/site-packages').as_posix()

sys.path.append(libpath)

# from tests import test_main, test_user, test_version, test_status, test_data_store, test_user_db, fake_data_store
from tests import test_main, test_user, test_version, test_status, fake_data_store

from petnet_app.models.version import Version
from petnet_app.models.status import Status
from petnet_app.models.user import UserModel, Person
from petnet_app.db.user_db import UserDb
from petnet_app.db.data_store import DataStore, DataStoreConfig
from petnet_app.config import Config

fake = fake_data_store.FakeDataStore()

def create_user_data_store():
    cfg = DataStoreConfig.create(db_number=1, shard_count=1)
    data_store = DataStore(cfg)
    return data_store

def create_user_db():
    ds = create_user_data_store()
    user_db = UserDb(ds)

    return user_db
