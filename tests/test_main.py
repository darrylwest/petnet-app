"""My Pet Net App Tests"""

import pytest
import sys
from rich import inspect

from petnet_app import main


@pytest.mark.asyncio
async def test_home():
    request = {}
    result = await main.home(request)
    inspect(result)
    assert True


@pytest.mark.asyncio
async def test_ping():
    result = await main.ping()
    inspect(result)
    assert True
