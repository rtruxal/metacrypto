class SecretGarbageValidator(object):
    def __init__(self): # Cuz python2
        super(SecretGarbageValidator, self).__init__()

    @staticmethod
    def validate_gen_random_printables(num_chars, line_length):
        assert isinstance(num_chars, int) and num_chars > 0, \
            'Please enter a valid number for `num_chars` in `regularcrypt/core/secret_garbage._gen_random_printables()`'
        assert line_length is None or (isinstance(line_length, int) and line_length > 0), \
            'Please enter `None` or a valid number for `line_length` in `regularcrypt/core/secret_garbage._gen_random_printables()`'
