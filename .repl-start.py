import sys
import os
import time
from datetime import datetime
# import importlib

from rich import inspect
import platform

# print("pid=", os.getpid())
if platform.system() == 'Linux':
    sys.path.append(f'{os.getenv("HOME")}/.cache/pypoetry/virtualenvs/petnet-app-c3NNDXsb-py3.11/lib/python3.11/site-packages')
else:
    sys.path.append(f'{os.getenv("HOME")}/Library/Caches/pypoetry/virtualenvs/petnet-app-I8h4Bcsw-py3.11/lib/python3.11/site-packages')

from tests import test_main, test_user

