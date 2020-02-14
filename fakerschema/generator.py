from random import randint

from faker import Faker

from . import fakers


def should_include(key, required_list):
    """Probabilistically include non-required keys in a document.

    Required keys are always included. Optional keys are included
    based on a coin flip (i.e. a uniform distribution over {0, 1}).

    Parameters:
        key - the key to check
        required_list - the required properties from the schema
    """
    if key in required_list:
        return True
    else:
        return bool(randint(0, 1))


def generate(schema):
    """Generate a bunch of data given a JSONSchema instance.

    Parameters:
        schema - the JSONSchema object to use.
        schema - the JSONSchema object to use.
    """
    fake = Faker()
    fake.email()
