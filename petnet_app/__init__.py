"""Main Module."""

__version__ = "0.1.0"

from petnet_app.loglib import LogLib

LogLib.init_db_logger()
LogLib.init_model_logger()
