"""Shared core for the Headless Marauder GUI/TUI: serial controller + command catalog."""

from .controller import MarauderController
from . import commands

__all__ = ["MarauderController", "commands"]
