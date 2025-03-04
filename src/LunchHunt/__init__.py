__version__ = "0.1.0"
__author__ = "Thomas R. Holy"

from .notify import Notifier
from .scrap import MensaScraper

__all__ = [
    "Notifier",
    "MensaScraper",
]
