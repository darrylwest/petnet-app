"""Test the log library."""

from rich import inspect

from petnet_app.loglib import LogLib
import logging


def test_stream_logger():
    lib = LogLib("test")
    lib.init_stream_logger()
    log = logging.getLogger("test")

    log.info("this is a test")
    assert lib.name == "test"
