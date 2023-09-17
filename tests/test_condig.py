"""Test the application config class."""

from rich import inspect
import os
from datetime import datetime, timezone

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
    assert uptime.seconds >= 0
    assert uptime.microseconds >= 0
