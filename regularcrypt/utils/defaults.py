from __future__ import unicode_literals

import string
# privides base 64 randommmmness. Much like RSA Private Keys which we're gonna impersonate by default!
DEFAULT_PERMISSIBLE_CHARS = string.ascii_letters + string.digits + '+/'

REGEX_CONTROL_CHARS = '+?.*^$()[]{}|'

