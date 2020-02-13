from itertools import repeat, chain
import re

import pytest

from fakerschema import xeger

# Generate repeats of each regex
n_repeats = 1
regexes = [
    r'([0-9]{4}[ -]}{3}\d{4}',
    r'$\d+$', r'\d*', r'\d?',
    r'number|21',
    r'\w{3}', r'[xyz2]',
    r'[^tesringu\s]',
    r'(number).(\d+)', r"(number).(?:\d+)"
]

@pytest.mark.parametrize('regex', list(chain(
    *(list(repeat(r, n_repeats)) for r in regexes)
)))
def test_xeger(regex):
    matcher = re.compile(regex)
    for generated_string in xeger(regex, 5):
        print(generated_string, regex)
        assert matcher(generated_string) is not None
