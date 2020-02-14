import random
from itertools import chain, count, islice
from re import sre_parse

from .utils import join
from .alpha import printable, digits, not_digits, \
    whitespace, not_whitespace, word, not_word  # pylint: disable=no-name-in-module

class RegexInverter:

    """
    Inverts a regex, i.e. given a regex, find a random string
    that matches the regex.

    You probably don't want to create this class directly, think about
    using the xeger function instead.

    """

    default_range_limit = 100

    # A mapping from opcode to a handling function. These have a signature
    # of func(self, obj) -> str
    # pylint: disable=no-member
    handlers = {
        sre_parse.LITERAL: lambda s, o: chr(o),
        sre_parse.NOT_LITERAL: lambda s, o: printable.diff(chr(o)).choose(),
        sre_parse.AT: lambda s, o: "",
        sre_parse.IN: lambda s, o: s.handle_in(o),
        sre_parse.ANY: lambda s, o: printable.choose(),
        sre_parse.RANGE: lambda s, o: [chr(i) for i in range(o[0], o[1] + 1)],
        sre_parse.BRANCH: lambda s, o: join(s.delegate(x) for x in random.choice(o[1])),
        sre_parse.SUBPATTERN: lambda s, o: s.handle_group(o),
        sre_parse.ASSERT: lambda s, o: join(s.delegate(x) for x in o[1]),
        sre_parse.ASSERT_NOT: lambda s, o: '',
        sre_parse.GROUPREF: lambda s, o: s.cache[o],
        sre_parse.MAX_REPEAT: lambda s, o: s.handle_repeat(o),
        sre_parse.MIN_REPEAT: lambda s, o: s.handle_repeat(o),
        sre_parse.NEGATE: lambda s, o: [False],
        sre_parse.CATEGORY: lambda s, o: s.categories[o]
    }

    # A mapping from category to an alphabet
    categories = {
        sre_parse.CATEGORY_DIGIT: str(digits),
        sre_parse.CATEGORY_NOT_DIGIT: str(not_digits),
        sre_parse.CATEGORY_SPACE: str(whitespace),
        sre_parse.CATEGORY_NOT_SPACE: str(not_whitespace),
        sre_parse.CATEGORY_WORD: str(word),
        sre_parse.CATEGORY_NOT_WORD: str(not_word),
    }
    # pylint: enable=no-member

    def __init__(self, range_limit=None):
        """
        Create an RegexInverter

        Parameters:
            range_limit - generally * and + will match an infinitely
                long list, this limits the number of matches which will return.
                If None, defaults to a limit of 100
        """
        self.cache = dict()
        self.range_limit = range_limit or self.default_range_limit

    def __call__(self, regex, limit=None):
        r"""
        Invert a regex, i.e. given a regex, generate random strings that match
        the regex.

        Usage:

        ```python
        # to make things reproduceable
        >>> from random import seed
        >>> seed(42)
        >>> xeger = RegexInverter(range_limit=5)

        # Random credit card numbers
        >>> list(xeger('([0-9]{4}[ -]){3}[0-9]{4}', count=4))
        ['4332-8196-0133-8386',
         '9402-5423-1161-5940',
         '6184-9310-4131-4752',
         '3419-8327-4835-3056']

        # Random HTML tags
        >>> list(xeger(r'^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$', count=3))
        ['<cgs6o[nV-=:{`={fROJ7,]\t/>',
         '<esR#MLhW;b\nsxs|>~nG>R/</e>',
         '<axxi\\(m\\i.Ka_>DY\x0b)</axxi>']
        ```

        You might also like to look at the `xeger` function which handles
        creating the inverter class under the covers for you.

        Parameters:
            regex - a re.Regex object or string
            limit - the number of strings to generate. If None, returns
                an infinite generator

        Returns a generator over random strings
        """
        # If we've got a re.Regex object then unwrap it, then parse
        try:
            tree = sre_parse.parse(regex.pattern)
        except AttributeError:
            tree = sre_parse.parse(regex)

        # Build a string each pass
        if limit:
            yield from islice((self.build(tree) for _ in count()), limit)
        else:
            yield from (self.build(tree) for _ in count())

    def build(self, parse_tree):
        """
        Build an example of the string given a parse tree
        """
        result = join(*(self.delegate(obj) for obj in parse_tree))
        self.cache.clear()
        return result

    def delegate(self, obj):
        """
        Delegate the object to the correct handler

        Objects are made of an opcode from re.sre_parse.OPCODES, and
        a child object, so we just pass these off to the relevant
        handler for processing.
        """
        opcode, obj = obj  # unwrap the opcode
        return self.handlers[opcode](self, obj)

    def handle_group(self, obj):
        """
        Handle a group object in the regex.

        A group object is a tuple of (group_index, obj), where group_index
        may be None if the group isn't labeled.
        """
        group_index, obj = obj[0], obj[-1]
        result = join(self.delegate(o) for o in obj)
        if group_index:
            self.cache[group_index] = result
        return result

    def handle_repeat(self, obj):
        """
        Handle a repeat object in the regex.

        Both max and min repeat objects have the form (start, end, obj),
        which tells us how many repeats to generate. We select a number of repeats
        randomly.
        """
        start, end, obj = obj
        repeats = random.randint(start, min(end, max(start + 1, self.range_limit)))
        return join(join(self.delegate(o) for o in obj) for _ in range(repeats))

    def handle_in(self, obj):
        """
        Handle an in object in the regex

        These are a list of objects - we first resolve these and then just
        select one uniformly. The obj has the form (flag, candidates) - if flag
        is false then we want objects not in this selection.
        """
        candidates = list(chain(*(self.delegate(o) for o in obj)))
        if candidates[0] is False:
            candidates = printable.diff(*candidates[1:])
            return candidates.choose()
        else:
            return random.choice(candidates)


# A light wrapper to hide the nasty classes
def xeger(regex, count=None, range_limit=None):
    r"""
    Invert a regex, i.e. given a regex, generate random strings that match
    the regex.

    A wrapper around the RegexInverter class to make it easier to call.

    Example usage:

    ```python
    # to make things reproduceable
    >>> from random import seed
    >>> seed(42)

    # Random credit card numbers
    >>> list(xeger('([0-9]{4}[ -]){3}[0-9]{4}', count=4))
    ['4332-8196-0133-8386',
     '9402-5423-1161-5940',
     '6184-9310-4131-4752',
     '3419-8327-4835-3056']

    # Random HTML tags
    >>> list(xeger(r'^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$', range_limit=5, count=3))
    ['<cgs6o[nV-=:{`={fROJ7,]\t/>',
     '<esR#MLhW;b\nsxs|>~nG>R/</e>',
     '<axxi\\(m\\i.Ka_>DY\x0b)</axxi>']
    ```

    Parameters:
        regex - a re.Regex object or string
        count - the number of strings to generate. If None, returns
            an infinite generator
        range_limit - generally * and + will match an infinitely
            long list, tis limits the number of matches which will return

    Returns:
        a generator over random strings
    """
    generator = RegexInverter(range_limit=range_limit)
    return generator(regex, count)
