"""My Pet Net App Tests"""

import pytest
import sys
from rich import inspect
import tomllib
from pathlib import Path


from petnet_app import main


@pytest.mark.asyncio
async def test_home():
    request = {}
    result = await main.home(request)
    inspect(result)
    assert "home" in result


@pytest.mark.asyncio
async def test_ping():
    result = await main.ping()
    inspect(result)
    assert "pong" in result


@pytest.mark.asyncio
async def test_info():
    result = await main.info()
    inspect(result)
    assert "pid" in result


def test_version():
    from petnet_app import __version__ as vers

    assert vers == "0.1.0"
    with Path.open(
        "./pyproject.toml",
        "rb",
    ) as f:
        project = tomllib.load(f)

    assert vers == project["tool"]["poetry"]["version"]


def test_keygen():
    from pydomkeys.keys import KeyGen

    keygen = KeyGen.create("XX", 4)
    inspect(keygen)
    key = keygen.route_key()
    inspect(key)
    assert len(key) == 16
