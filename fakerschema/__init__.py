import catalogue

from .xeger import xeger

fakers = catalogue.create("fakerschema", "fakers")

__all__ = ["fakers", "xeger"]
