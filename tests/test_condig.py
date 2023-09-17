"""Test the application config class."""

from rich import inspect
import os
from datetime import datetime, timezone
import time

from petnet_app.config import Config


def test_create():
    cfg = Config.create()
    inspect(cfg)
    assert cfg.env == "dev"
    assert cfg.created
    assert cfg.version == "0.1.0"
    assert cfg.apikey != ""
    assert cfg.pid == os.getpid()


def test_uptime():
    now = datetime.now(tz=timezone.utc)
    cfg = Config.create()

    assert cfg.created >= now
    uptime = cfg.uptime()
    inspect(uptime)
    assert str.startswith(uptime, "0 days")
    assert str.endswith(uptime, "0:00:00")


def test_uptime_days():
    dt = datetime.fromtimestamp(time.time() - 864000, tz=timezone.utc)
    cfg = Config("prod", dt, "0.0.0", "apikey", os.getpid())
    uptime = cfg.uptime()
    inspect(uptime)
    assert str.startswith(uptime, "10 days,")
