from itertools import repeat, chain
import re

import pytest

from fakerschema import xeger

# Generate a bunch of regexes
regexes = [
    r'([0-9]{4}[ -]){3}\d{4}',
    r'\d+$', r'\d*', r'\d?',
    r'-?\$[ \d]{3}\.\d{2}',
    r'number|21',
    r'\w{3}', r'[xyz2]',
    r'[^tesringu\s]',
    r'(number)\.(\d+)', r"(number)\.(?:\d+)",
    r'^[a-z0-9_-]{3,16}$', r'^[a-z0-9_-]{6,18}$',
    r'^#?([a-f0-9]{6}|[a-f0-9]{3})$',
    r'^[a-z0-9-]+$',
    r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$',
    r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    # r'^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$',  # this one is sometimes buggy - suggests a problem with generating groups?
    r'\b[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?\b',
    r'((\b[0-9]+)?\.)?\b[0-9]+([eE][-+]?[0-9]+)?\b',
]

@pytest.mark.parametrize('regex', regexes)
def test_xeger(regex):
    matcher = re.compile(regex)

    # Generate 1000 random strings and test
    # Limit ranges to 10 characters as some of these regexes end up huuuge
    for generated_string in xeger(regex, count=1000, range_limit=10):
        print(generated_string, regex)
        assert matcher.match(generated_string) is not None
