import random
from itertools import chain, count, islice
from re import sre_parse
from re.sre_parse import (   # pylint: disable=no-member,import-error
    LITERAL, NOT_LITERAL, AT, IN, ANY, RANGE, BRANCH, SUBPATTERN,
    ASSERT, ASSERT_NOT, GROUPREF, MAX_REPEAT, MIN_REPEAT, NEGATE
)

from .utils import flatten, join
from .alpha import printable  # pylint: disable=no-name-in-module

class RegexInverter:

    # Generally, * and + will match an infinitely long list,
    # this limits the number of matches which will return
    range_limit = 100

    # A mapping from opcode to a handling function. These have a signature
    # of func(self, obj) -> str
    handlers = {
        LITERAL: lambda _, o: chr(o),
        NOT_LITERAL: lambda _, o: printable.diff(chr(o)).choose(), 
        AT: lambda _, _: "",
        IN: lambda s, o: s.handle_in(o),
        ANY: lambda _, _: printable.choose(),
        RANGE: lambda _, o: [chr(i) for i in range(o[0], o[1] + 1)],
        BRANCH: lambda s, o: join(s.delegate(x) for x in random.choice(o[1])),
        SUBPATTERN: lambda s, o: s.handle_group(o),
        ASSERT: lambda s, o: join(s.delegate(x) for x in [1]),
        ASSERT_NOT: lambda _, _: '',
        GROUPREF: lambda s, o: s.cache[o],
        MAX_REPEAT: lambda s, o: s.handle_repeat(o),
        MIN_REPEAT: lambda s, o: s.handle_repeat(o),
        NEGATE: lambda _, _: [False]
    }

    def __init__(self):
        self.cache = dict()

    def __call__(self, regex, limit=None):
        """
        Invert a regex, i.e. given a regex, generate random strings that match
        the regex.

        Parameters:
            regex - a re.Regex object or string
            limit - the number of strings to generate. If None, returns
                an infinite generator
            
        Returns:
            a generator over random strings
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
        result = join(self.delegate(obj) for obj in parse_tree)
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
        return join(self.handlers[opcode](self, obj))

    def handle_group(self, obj):
        """
        Handle a group object in the regex.
        
        A group object is a tuple of (group_index, obj), where group_index
        may be None if the group isn't labeled. 
        """
        group_index, obj = obj
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
        repeats = random.randint(start, min(end, self.range_limit))
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
            return candidates.choose
        else:
            return random.choice(candidates)


# A light wrapper to hide the nasty classes 
def xeger(regex, limit=None):
    """
    Invert a regex, i.e. given a regex, generate random strings that match
    the regex.

    Parameters:
        regex - a re.Regex object or string
        limit - the number of strings to generate. If None, returns
            an infinite generator
        
    Returns:
        a generator over random strings
    """
    generator = RegexInverter()
    return generator(regex, limit)
