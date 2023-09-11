"""Tests for Version model"""

from rich import inspect
import time

from petnet_app.models.version import Version


def test_version():
    now = time.time_ns()
    vers = Version(
        create_date=now,
        last_update=now,
        version=0,
    )

    assert isinstance(vers, Version)
    assert vers.create_date == vers.last_update
    assert vers.version == 0


def test_create():
    vers = Version.create()
    assert isinstance(vers, Version)
    assert vers.create_date == vers.last_update
    assert vers.version == 0


def test_update():
    vers = Version.create()
    assert vers.create_date == vers.last_update
    time.sleep(0.01)
    updated = vers.update()

    # ensure original is intact
    assert vers != updated
    assert vers.create_date == vers.last_update
    assert updated.create_date == vers.create_date
    assert updated.last_update > vers.last_update
    assert updated.version == vers.version + 1
