from __future__ import print_function, unicode_literals

import string
import os
from regularcrypt.utils.validations import SecretGarbageValidator
try:
    import secrets as s
except ImportError:
    print("WARNING: YOU ARE USING PYTHON2, THIS MEANS YOU DON'T HAVE ACCESS TO THE `secrets` PACKAGE.\nUSING `random` AS A REPLACEMENT")
    import random as s # random.choice() is a thing. which is all we're using `s` for here.

__doc__ = """
This module creates a file full'a garbage.
 
The size is up to you, but the default is XXXXXXXXXXXXXXXXX

Once a file is generated, several regex extractors will be made for you to select from.

These extractors will produce passwords out of the noise-files that this module creates.
"""


def _gen_random_printables(num_chars=500, line_length=32, validator=None):
    if not validator: # This is a crypto library after all...call me paranoid.
        SecretGarbageValidator.validate_gen_random_printables(num_chars, line_length)

    _current_line_length = 0
    _chars_generated = 0

    _permissible_chars = string.printable[:-6] # This is a string...the last 6 chars are " \t\n\r\x0b\x0" so no thank you.
    # secrets.SystemRandom is not always available
    try:
        sec = s.SystemRandom()
    except:
        sec = s

    while _chars_generated < num_chars + 1: # This is gonna be a generator to avoid accidental blue-screens.
        _chars_generated += 1
        if line_length is not None and _current_line_length > line_length: # test if we're done with a line, then insert an `os.linesep` before continuing.
            _current_line_length = 0
            yield os.linesep
        else:
            _current_line_length += 1
            yield sec.choice(_permissible_chars)


def main():
    print(''.join(list(_gen_random_printables())))



if __name__ == "__main__":
    # print('YOU BETTER BE TESTING.')
    main()