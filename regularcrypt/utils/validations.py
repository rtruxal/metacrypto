from __future__ import print_function, unicode_literals
from regularcrypt.utils.custom_errors import TooBigError
class SecretGarbageValidator(object):
    def __init__(self): # Cuz python2
        super(SecretGarbageValidator, self).__init__()

    @staticmethod
    def validate_gen_random_printables(num_chars, line_length, permissible=False):
        if num_chars > 100000 and not permissible:
            raise TooBigError("You're trying to generate over 100,000 characters in a non-concurrent manner. This will probably crash your laptop.")
        assert isinstance(num_chars, int) and num_chars > 0, \
            'Please enter a valid number for `num_chars` in `regularcrypt/core/secret_garbage._gen_random_printables()`'
        if line_length is not None:
            assert isinstance(line_length, int) and line_length > 0, \
                'Please enter `None` or a valid number for `line_length` in `regularcrypt/core/secret_garbage._gen_random_printables()`'

    @staticmethod
    def validate_line_related_params(line_lenth_arg, output_type):
        if not line_lenth_arg and output_type == 'lines':
            raise ValueError("You're asking for lines but have either set the line-length at 0, or specified no line-length.")

    @staticmethod
    def validate_output_param(output_type):
        # NOTICE THE `and output_type in ('raw', 'lines')`.
        # YOU CAN ONLY CHOOSE TO GET BACK A RAW STRING, OR GET A LIST OF LINES.
        
        assert isinstance(output_type, str) and output_type in ('raw', 'lines'), \
            "Your options for output_type are \n`raw` <default>: Gives back a string with \\n or some analog @ the specified line-length interval.\n\nOR\n\n`lines`: Named after `.writelines()`, it gives you back a list of strings of equal length."