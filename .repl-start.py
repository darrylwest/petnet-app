import sys
import os
import time
from datetime import datetime
# import importlib

from rich import inspect

# print("pid=", os.getpid())
sys.path.append('/Users/dpw/Library/Caches/pypoetry/virtualenvs/petnet-app-I8h4Bcsw-py3.11/lib/python3.11/site-packages')

from tests import test_main, test_user

def create_keys(count: int = 100):
    """return a list of keys"""
    from pydomkeys.keys import KeyGen, Counter, Base62
    keygen = KeyGen.create("US", 4)

    return [keygen.route_key() for _ in range(count)]



