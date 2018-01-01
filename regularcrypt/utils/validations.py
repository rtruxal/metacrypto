from __future__ import print_function, unicode_literals
from regularcrypt.utils.custom_errors import TooBigError
from os import path

class NoiseGenValidator(object):
    def __init__(self): # Cuz python2
        super(NoiseGenValidator, self).__init__()

    @staticmethod
    def validate_keygen_params(num_chars, line_length, output_type):
        if num_chars > 100000:
            raise TooBigError("You're trying to generate over 100,000 characters in a non-concurrent manner. This will probably crash your laptop.")
        assert isinstance(num_chars, int) and num_chars > 0, \
            'Please enter a valid number for `num_chars` in `regularcrypt/core/secret_garbage._gen_keystore_string()`'
        if line_length is not None:
            assert isinstance(line_length, int) and line_length > 0, \
                'Please enter `None` or a valid number for `line_length` in `regularcrypt/core/secret_garbage._gen_keystore_string()`'
        if not line_length and output_type == 'lines':
            raise ValueError("You're asking for lines but have either set the line-length at 0, or specified no line-length.")
        assert isinstance(output_type, (str, unicode)) and output_type in ('str', 'list'), \
            "Your options for output_type are \n`str` : Gives back a string with \\n or some analog @ the specified line-length interval.\n\nOR\n\n`list` <default>: Good for use with `.writelines()`, it gives you back a list of strings."


class TranslatorsValidator(object):
    def __init__(self):
        super(TranslatorsValidator, self).__init__()

    @staticmethod
    def validate_garbage_saver_init_types(keystore_model, outfile_name):
        assert isinstance(outfile_name, str) and isinstance(keystore_model, (str, list)), \
            "Your filename or keystore file is the wrong type. See the GarbageSaver() class docstring."
        if isinstance(keystore_model, list):
            for line in keystore_model:
                assert isinstance(line, str), \
                    "one of the items given to you by secret_garbage.py is not a string. Something is seriously wrong."


class OutputValidator(object):
    def __inti__(self):
        super(OutputValidator, self).__init__()

    @staticmethod
    def validate_writefunc_params(data, filepath, open_mode):
        assert isinstance(data, (list, str))
        assert isinstance(filepath, str) and path.exists(path.split(filepath)[0]), \
            "Directory {} does not exist.".format(path.split(filepath)[0])
        assert open_mode in 'wba+-', "enter a valid write mode for the open() __builtin__ func."
