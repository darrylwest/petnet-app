"""Test the Status Model."""


from petnet_app.models.status import Status


def test_new():
    status = Status.new(128)
    assert status.label == "new"
    assert status.value == 128


def test_active():
    status = Status.active(128)
    assert status.label == "active"
    assert status.value == 128


def test_inactive():
    status = Status.inactive(128)
    assert status.label == "inactive"
    assert status.value == 128


def test_deleted():
    status = Status.deleted(128)
    assert status.label == "deleted"
    assert status.value == 128
