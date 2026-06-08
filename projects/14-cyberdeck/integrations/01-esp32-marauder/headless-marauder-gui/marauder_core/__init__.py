"""Shared core for the Headless Marauder apps: serial controller, command catalog,
parser, flasher, capture logger, and self-updater."""

__version__ = "1.0.0"

from .controller import MarauderController
from .parsing import MarauderParser, AP, Station
from .capture import CaptureLogger, default_log_dir
from . import commands
from . import flasher
from . import updater

__all__ = [
    "MarauderController", "MarauderParser", "AP", "Station",
    "CaptureLogger", "default_log_dir",
    "commands", "flasher", "updater", "__version__",
]
