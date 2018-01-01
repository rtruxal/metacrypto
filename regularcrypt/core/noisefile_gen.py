from __future__ import print_function, unicode_literals
__doc__ = """
A big warm bear-hug to https://github.com/N2ITN for turning my 240-line random-character generator mess 
into 27 functional lines of code.

Good on ya' mate.
"""
import itertools
import os
from regularcrypt import DEFAULT_PERMISSIBLE_CHARS
from regularcrypt.utils.validations import NoiseGenValidator
try:
    from secrets import SystemRandom
    r = SystemRandom()
except ImportError:
    import random as r

def gen_choice(permissible_chars=None):
    while True:
        try:
            if permissible_chars:
                yield r.choice(permissible_chars)
            else:
                yield r.choice(DEFAULT_PERMISSIBLE_CHARS)
        except KeyboardInterrupt:
            print('Congrats! You put the random-character generator into an infinite loop!')
            break

def make_all(num_chars, line_len, permissible_chars=None, output_type='list', validate_input=True):
    if validate_input:
        NoiseGenValidator().validate_keygen_params(num_chars, line_len, output_type)
    if line_len > num_chars or line_len == 0:
        return ''.join([next(gen_choice(permissible_chars)) for _ in range(num_chars)])
    sep = os.linesep
    div_, mod_ = divmod(num_chars, line_len)
    raw = (next(gen_choice(permissible_chars)) for i in range(num_chars))
    raw = sep.join(''.join(list(itertools.islice(raw, line_len))) for _ in range(div_))
    raw = raw + sep + ''.join(list(itertools.islice(raw, mod_)))
    if output_type == 'str':
        return raw
    elif output_type == 'list':
        return raw.split(sep)

def main():
    num_chars = 1000
    line_len = 13
    permissible_chars = DEFAULT_PERMISSIBLE_CHARS
    # permissible_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!'
    result = make_all(num_chars, line_len, permissible_chars, 'str')

    def tests(res):
        if isinstance(res, list):
            print('Number of lines: {}'.format(len(res)))
            print('line-length: {}'.format(len(res[0])))
            print('last line-length: {}'.format(len(res[-1])))
            print('total number of chars: {}'.format(len(''.join(res))))
        elif isinstance(res, (str, unicode)):
            print('Number of lines: {}'.format(res.count(os.linesep)))
            print('total number of chars: {}'.format(len(res.replace(os.linesep, ''))))
            #TODO: Fix spookines around type(os.linesep) == str && type(res) == unicode.
            print(os.linesep.split(res)) # <-- WTF????
            # print('line-length: {}'.format(len(os.linesep.split(res)[0])))
            # print('last line-length: {}'.format(len(res[last_line_start:])))
        else:
            print(type(res))
    tests(result)


if __name__ == "__main__":
    main()