import string
import random

from .utils import join, cached_property


class Alphabet:

    """ Utility class for handling alphabets.
    """

    def __init__(self, chars):
        """
        Create an Alphabet instance

        Parameters:
            chars - the characters in the alphabet
        """
        self._chars = chars

    @cached_property(["_chars"])
    def chars(self):
        return tuple(join(sorted(self._chars)))

    def __str__(self):
        """
        String representation
        """
        return join(self.chars)

    def diff(self, *strings):
        """
        Return a new alphabet with the set difference between the
        characters and the new strings.

        Parameters:
            *strings - strings of characters to remove from the alphabet
        """
        # Handle alphabet instances
        _strings = []
        for obj in strings:
            try:
                _strings.append(obj.string)
            except AttributeError:
                # we just have a string
                _strings.append(obj)
        strings = _strings

        # Join everything together
        other = set(join(*strings))
        return Alphabet(join(set(self.chars) - other))

    def choose(self, count=1):
        """
        Return `limit` random characters from the alphabet.

        Characters are chosen with replacement

        Parameters:
            count - the number of characters to choose
        """
        if count == 1:
            return random.choice(self.chars)
        else:
            return random.choices(self.chars, k=count)


ALPHABET_STRINGS = dict(
    printable=tuple(string.printable),
    letters=tuple(string.ascii_letters),
    uppercase=tuple(string.ascii_uppercase),
    lowercase=tuple(string.ascii_lowercase),
    digits=tuple(string.digits),
    punctuation=tuple(string.punctuation),
    not_digits=tuple(string.ascii_letters + string.punctuation),
    not_letters=tuple(string.digits + string.punctuation),
    whitespace=tuple(string.whitespace),
    not_whitespace=tuple(set(string.printable) - set(string.whitespace)),
    normal=tuple(string.ascii_letters + string.digits + " "),
    word=tuple(string.ascii_letters + string.digits + "_"),
    not_word=tuple(
        set(string.printable) - set(string.ascii_letters + string.digits + "_")
    ),
    unambiguous=tuple(set(string.ascii_letters + string.digits) - set("0O1lI")),
    postalsafe=tuple(string.ascii_letters + string.digits + " .-#/"),
    urlsafe=tuple(string.ascii_letters + string.digits + "-._~"),
    domainsafe=tuple(string.ascii_letters + string.digits + "-"),
)

# Expose all the alphabets as Alphabet classes
for name, alphabet in ALPHABET_STRINGS.items():
    globals()[name] = Alphabet(alphabet)
