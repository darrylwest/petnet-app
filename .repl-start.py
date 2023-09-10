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

from tests import test_main, test_user
