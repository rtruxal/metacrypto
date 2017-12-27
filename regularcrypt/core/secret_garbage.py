from __future__ import print_function, unicode_literals

import string
import os
from regularcrypt.utils.validations import SecretGarbageValidator
from regularcrypt.utils.custom_errors import ImpossibleError
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


def _gen_random_printables(num_chars=500, line_length=32, validate=True):
    if validate is True: # This is a crypto library after all...call me paranoid.
        SecretGarbageValidator.validate_gen_random_printables(num_chars, line_length)

    _current_line_length = 0
    _chars_generated = 0
    # This gives me the set of all normal chars that aren't weird or escape-chars..ever.
    # The following line is for explication. `_permissible_chars = regularcrypt.DEFAULT_PERMISSIBLE_CHARS` would also work.
    _permissible_chars = string.printable[:-6].replace('\\', '').replace("'", "").replace('"', '')
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

def gen_default_keystore(validate=True, output='raw'):
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    res = _gen_random_printables(validate=validate)
    if output == 'raw':
        return ''.join(res)
    elif output == 'lines':
        return ''.join(res).split(os.linesep)
    else:
        raise ImpossibleError('output must be either "raw" or "lines"')

def gen_single_line_keystore(num_chars=500, validate=True, output='raw'):
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    line_length = None
    res = _gen_random_printables(num_chars=num_chars, line_length=line_length, validate=validate)
    if output == 'raw':
        return ''.join(res)
    elif output == 'lines':
        SecretGarbageValidator.validate_line_related_params(line_length, output)
        return ''.join(res)
    else:
        raise ImpossibleError('output must be either "raw" or "lines"')



def gen_keystore(num_chars=500, line_length=32, validate=True, output='raw'):
    # This one's not optional.
    SecretGarbageValidator.validate_line_related_params(line_length, output)
    if validate:
        SecretGarbageValidator.validate_output_param(output)

def gen_custom_char_keystore(include_chars, num_chars=500, line_length=32, validate=True, output='raw'):
    #TODO: FIX THIS SO num_chars IS ACTUALLY WHAT GETS OUTPUT AFTER FILTERING.
    """
    Reduce the allowed characters to a whitelist-set of your specification
    ...maybe you don't want digits! or parentheses!

    !WARNING!:
    You can only reduce the number of possible chars with this function.
    Doing so decreases the difficulty of brute-forcing a malicious attempt to retrieve your password.
    !WARNING!
    """
    #...again...not optional.
    SecretGarbageValidator.validate_line_related_params(line_length, output)
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    orig_keystore = [i for i in _gen_random_printables(num_chars, line_length, validate)]
    filter_func = lambda j: j in include_chars
    if output == 'raw':
        return ''.join(filter(filter_func, orig_keystore))
    elif output == 'lines':
        #TODO: Crap...there is no more `os.linesep` after we filter the raw-string.
        return ''.join(filter(filter_func, orig_keystore)).split(os.linesep)
    else:
        raise ImpossibleError('output must be either "raw" or "lines"')

def main():
    print(''.join(list(_gen_random_printables())))



if __name__ == "__main__":
    print('YOU BETTER BE TESTING.')
    # main()