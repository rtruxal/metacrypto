import string
DEFAULT_PERMISSIBLE_CHARS = string.printable[:-6].replace('\\', '').replace("'", "").replace('"', '') # the last 6 chars are: " \t\n\r\x0b\x0"