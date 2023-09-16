"""The LogLib module configures logging for the application."""

# @see https://docs.python.org/3/library/logging.html for the python docs
# @see https://docs.python.org/3/howto/logging-cookbook.html for improved formatting, file rotation, etc.

import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LogLib:
    """LogLib configures logging."""

    @staticmethod
    def init_db_logger():
        """Initialize the database logger."""
        name = "db"
        lib = LogLib(name)
        lib.init_file_logger(f"logs/{name}.log")

    @staticmethod
    def init_model_logger():
        """Initialize the model logger."""
        name = "mdl"
        lib = LogLib(name)
        lib.init_file_logger(f"logs/{name}.log")

    def __init__(self, name: str):
        """Initialize the logger with or withow config."""
        self.level = logging.INFO
        self.version = "0.1.0"
        self.max_bytes = 100_000

        self.name = name

        self.log = logging.getLogger(name)
        self.log.setLevel(self.level)

    def get_formatter(self):
        """Return the standard log formmater including UTC and nanoseconds."""
        logging.Formatter.converter = time.gmtime
        return logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S.%s",
        )

    def init_stream_logger(self):
        """Initialize the stream logger."""
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = self.get_formatter()
        handler.setFormatter(formatter)

        self.log.addHandler(handler)

    def init_file_logger(self, filename: str):
        """Initialize the rotating file logger."""
        # try to find a logs folder
        path = Path(filename)

        handler = RotatingFileHandler(path, backupCount=5, maxBytes=self.max_bytes)
        handler.setLevel(self.level)

        formatter = self.get_formatter()
        handler.setFormatter(formatter)

        self.log.addHandler(handler)
