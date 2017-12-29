from __future__ import print_function, unicode_literals


__doc__ = """
This module is full of various objects.
Each of these will expose methods which mediate information-transforms throughout the package.
"""
import re
from regularcrypt.utils.validations import TranslatorsValidator

class GarbageSaver(object):
    def __init__(self, keystore_model, outfile_name, outfile_extension=None):
        """
        This is going to mediate saving our default input-files.
        That means it's going to mediate interactions...:
        BETWEEN:
         - regularcrypt.__main__.py
         - regularcrypt.core.secret_garbage.py
        TO UTILIZE:
         - regularcrypt.io.output_generated_keystore_file.py

        You'll note that keystore_model & outfile_name are NOT optional params.

        :param keystore_model: Type: <str|list>; Comes from core.secret_garbage.py
        :param outfile_name: Type: <str>; Comes from __main__.py
        :param outfile_extension: [Type: <str>]; optional param giving a filetype.
                                  If provided, it will ALWAYS be the last chars of the filename.
        """
        TranslatorsValidator.validate_garbage_saver_init_types(keystore_model, outfile_name)
        super(GarbageSaver, self).__init__()

        self.model = keystore_model
        self.model_type = type(keystore_model) # this is permissible due to the validator^
        self.filename = outfile_name
        self.ext = outfile_extension

        # yaaaay for making things semi-hidden in python.
        def _get_filetype_from_filename(filename):
            """
            If file-extension not in filename, return None.
            Otherwise, return a tuple to reassign self.filename & self.ext
            """
            file_ext_regex = r'[^\.](\.\w+)$' # capture the last "." and everything after it.
            if re.search(file_ext_regex, filename):
                file_ext = re.search(file_ext_regex, filename).group(1)
                new_filename = filename[:int((-1 * len(file_ext)))]
                return new_filename, file_ext
            else:
                return None
        # if no extension on the filename, use default.
        if not _get_filetype_from_filename(self.filename):
            self.ext = '.openssh'
        else:
            self.filename, self.ext = _get_filetype_from_filename(self.filename)



