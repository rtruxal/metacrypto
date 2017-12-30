from __future__ import print_function, unicode_literals

import string
import os
from itertools import islice

from regularcrypt.utils.validations import SecretGarbageValidator
from regularcrypt.utils.custom_errors import ImpossibleError
from regularcrypt import DEFAULT_PERMISSIBLE_CHARS
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

dEAR LOR D -- PLZ FORGIVE ME FOR ALL FUNCTIONS STARTING WITH AN _
"""
########################################################################################################################
# DEMON MAGIC BELOW THIS LINE...SKIP TO BOTTOM.
# ---------------------------------------------
###############################################
def _gen_random_chars(num_chars, current_num_chars, permissible_chars, infinite=False):
    _current_num_chars = current_num_chars
    try:
        sec = s.SystemRandom()
    except:
        sec = s
    if not infinite:
        while _current_num_chars <= num_chars: # This is gonna be a generator to avoid accidental blue-screens.
            _current_num_chars += 1
            yield sec.choice(permissible_chars)
    else:
        while True:
            _current_num_chars += 1
            yield sec.choice(permissible_chars)

def _gen_keystore_string(num_chars, line_length, validate=True, permissible_chars=None):
    if validate is True: # This is a crypto library after all...call me paranoid.
        SecretGarbageValidator.validate_gen_random_printables(num_chars, line_length)
    _chars_generated = 0
    # This gives me the set of all normal chars that aren't weird or escape-chars..ever.
    # The following line is for explication. `_permissible_chars = regularcrypt.DEFAULT_PERMISSIBLE_CHARS` would also work.
    if permissible_chars is not None:
        _permissible_chars = permissible_chars
    else: # default
        _permissible_chars = string.printable[:-6].replace('\\', '').replace("'", "").replace('"', '')    # secrets.SystemRandom is not always available
    randomness_generator = _gen_random_chars(num_chars, _chars_generated, _permissible_chars)
    if not line_length:
        while True:
            try:
                yield next(randomness_generator)
            except StopIteration as err:
                print(err)
                break
    else:
        _current_line_length = 0
        while True:
            try:
                while _current_line_length <= line_length - 1:
                    yield next(randomness_generator)
                    _current_line_length += 1
                yield os.linesep
                _current_line_length = 0
            except StopIteration as stopiter:
                print(stopiter)
                break


def _gen_keystore_list(num_chars, line_length, validate=True, permissible_chars=None):
    if validate is True: # This is a crypto library after all...call me paranoid.
        SecretGarbageValidator.validate_gen_random_printables(num_chars, line_length)
    _chars_generated = 0
    if permissible_chars is not None:
        _permissible_chars = permissible_chars
    else: # default
        _permissible_chars = string.printable[:-6].replace('\\', '').replace("'", "").replace('"', '')
    res = []
    # secrets.SystemRandom is not always available
    randomness_generator = _gen_random_chars(num_chars, _chars_generated, _permissible_chars, infinite=True)
    if not line_length:
        res = [''.join([i for i in randomness_generator])]
        return res
    else:
        _current_offset = 0
        _desired_offset = 0
        # writing this portion is making me think I should have allowed either dimensions
        # or a set number of chars...
        while len(res) < int((num_chars / line_length) + 1):
            _desired_offset = _current_offset + line_length
            line = ''.join(list(islice(randomness_generator, _current_offset, _desired_offset)))
            res.append(line)
            _current_offset = _desired_offset
        return res


def _finish_keystore_list(unfinished_keystore, num_chars, line_length, validate=True, permissible_chars=None):
    _last_line_offset = line_length - len(unfinished_keystore[-1]) # difference b/w ideal & actual....gah ima redo this eventually.
    _current_num_chars = sum([len(i) for i in unfinished_keystore]) # sum the num of chars in each line
    if permissible_chars is not None:
        _permissible_chars = permissible_chars
    else: # default
        _permissible_chars = string.printable[:-6].replace('\\', '').replace("'", "").replace('"', '')
    # LOGIC TIME!
    if _current_num_chars < num_chars: # then we need to add more.
        res = []
        # first, finish off the last line
        res.append(unfinished_keystore[-1] + ''.join([i for i in _gen_random_chars(num_chars=_last_line_offset, current_num_chars=0, permissible_chars=_permissible_chars)]))
        _current_num_chars += _last_line_offset # <-- added benefit of explicating what this^ does.
        # jesus. ok now let's generate the rest of the list:
        if _current_num_chars <= num_chars:
            _num_chars_to_make_up = num_chars - _current_num_chars
            res = res + _gen_keystore_list(num_chars=_num_chars_to_make_up, line_length=line_length, permissible_chars=_permissible_chars)
        return res
    elif _current_num_chars > num_chars: # then we need to remove some.
        _finished_keystore = unfinished_keystore
        num_chars_to_remove = _current_num_chars - num_chars
        # while the num of chars we want to remove is longer than the line-length,
        # we can just remove the line and decrement our counter.
        while num_chars_to_remove > int(line_length):
            num_chars_to_remove -= int(line_length)
            del _finished_keystore[-1]
        _finished_keystore[-1] = _finished_keystore[-1][:(-1 * num_chars_to_remove)]
        return _finished_keystore
    else: #...then what are we doing here?
        return unfinished_keystore

########################################################################################################################
# PUBLIC UTILITY FUNCS BELOW THIS LINE
# ------------------------------------
######################################
def gen_default_keystore(validate=True, output='lines'):
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    if output == 'raw':
        res = _gen_keystore_string(num_chars=1024, line_length=32,validate=validate)
        return ''.join(res)
    elif output == 'lines':
        res = _gen_keystore_list(num_chars=1024, line_length=32, validate=validate)
        return res
    else:
        raise ImpossibleError('output must be either "raw" or "lines"')

def gen_single_line_keystore(num_chars=1024, validate=True, output='raw'):
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    line_length = None
    if output == 'raw':
        res = _gen_keystore_string(num_chars=num_chars, line_length=line_length, validate=validate)
        return ''.join(res)
    elif output == 'lines':
        SecretGarbageValidator.validate_line_related_params(line_length, output)
        # res = _gen_keystore_list(num_chars=num_chars, line_length=line_length, validate=validate)
        # return ''.join(res)
        return ''
    else:
        raise ImpossibleError('output must be either "raw" or "lines"')


def gen_keystore(num_chars=1024, line_length=32, validate=True, output='lines', include_chars=DEFAULT_PERMISSIBLE_CHARS):
    # ...again...not optional.
    SecretGarbageValidator.validate_line_related_params(line_length, output)
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    filter_func = lambda j: j in include_chars
    if output == 'raw':
        orig_keystore = [i for i in
                         _gen_keystore_string(num_chars, line_length, validate, permissible_chars=include_chars)]
        # now trim.
        if len(orig_keystore) > num_chars:
            num_to_cut = int(len(orig_keystore) - num_chars)
            result_keystore = orig_keystore[:(-1 * num_to_cut)]
        elif len(orig_keystore) < num_chars:
            num_to_add = int(num_chars - len(orig_keystore))
            result_keystore = orig_keystore + [i for i in _gen_random_chars(num_chars=num_to_add, current_num_chars=0,
                                                                            permissible_chars=include_chars)]
        else:
            result_keystore = orig_keystore
        return ''.join(result_keystore)
    elif output == 'lines':
        orig_keystore = _gen_keystore_list(num_chars=num_chars, line_length=line_length, validate=validate,
                                           permissible_chars=include_chars)
        if sum([len(i) for i in orig_keystore]) != num_chars:  # we have a function for this!!!
            return _finish_keystore_list(orig_keystore, num_chars=num_chars, line_length=line_length, validate=validate,
                                         permissible_chars=include_chars)
        else:
            return orig_keystore



def gen_custom_char_keystore(include_chars, num_chars=1024, line_length=32, validate=True, output='lines'):
    """
    !WARNING!:
    You can only reduce the number of possible chars with this function.
    Doing so decreases the difficulty of brute-forcing a malicious attempt to retrieve your password.
    !WARNING!
    """
    #...again...not optional.
    SecretGarbageValidator.validate_line_related_params(line_length, output)
    if validate:
        SecretGarbageValidator.validate_output_param(output)
    filter_func = lambda j: j in include_chars
    if output == 'raw':
        orig_keystore = [i for i in _gen_keystore_string(num_chars, line_length, validate, permissible_chars=include_chars)]
        # now trim.
        if len(orig_keystore) > num_chars:
            num_to_cut = int(len(orig_keystore) - num_chars)
            result_keystore = orig_keystore[:(-1 * num_to_cut)]
        elif len(orig_keystore) < num_chars:
            num_to_add = int(num_chars - len(orig_keystore))
            result_keystore = orig_keystore + [i for i in _gen_random_chars(num_chars=num_to_add, current_num_chars=0, permissible_chars=include_chars)]
        else:
            result_keystore = orig_keystore
        return ''.join(result_keystore)
    elif output == 'lines':
        orig_keystore = _gen_keystore_list(num_chars=num_chars, line_length=line_length, validate=validate, permissible_chars=include_chars)
        if sum([len(i) for i in orig_keystore]) != num_chars: # we have a function for this!!!
            return _finish_keystore_list(orig_keystore, num_chars=num_chars, line_length=line_length, validate=validate, permissible_chars=include_chars)
        else:
            return orig_keystore
    else:
        raise ImpossibleError('output must be either "raw" or "lines"')

def main():
    y = _gen_keystore_string(20, 3)
    # print(''.join([i for i in y]))
    z = _gen_keystore_list(20, 3)
    print(z)

if __name__ == "__main__":
    # print('YOU BETTER BE TESTING.')
    main()