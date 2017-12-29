from __future__ import print_function, unicode_literals
# import os
# import sys
import argparse
from regularcrypt.utils.custom_errors import NotYetImplementedError

def make(parser_arguments):
    from regularcrypt.utils.translators import GarbageSaver
    import regularcrypt.core.secret_garbage as sg_module
    _parser_argument_container = parser_arguments
    #TODO: fill this skeleton out.
    outfile_name = _parser_argument_container.outfile
    #TODO: Make a warning if the user doesn't EVER specify a file-extension that the default will be used.
    if not _parser_argument_container.string:
        keystore = sg_module.gen_default_keystore()
        saver = GarbageSaver(keystore_model=keystore, outfile_name=outfile_name)
        #TODO: make the following 2 lines uncomment-able.
        #saver.save_in_triplicate()
        #saver.validate_self()

    else:
        raise NotImplementedError("Not yet implemented...try using less args!")

def crypt(parser_arguments):
    _parser_argument_container = parser_arguments



def main(args=None):
    if not args:
        #TODO: STRUCTURE, STRUCTURE, STRUCTURE. This package has several modalities of application. Make them distinct (like git).
        top_level_parser = argparse.ArgumentParser(prog="metacrypto")
        top_level_parser.add_argument('-v', '--verbose', action="store_true", help="This program will make more noise.")
        subparsers = top_level_parser.add_subparsers(help='command options are `metacrypto <make|crypt>`. Try `metacrypto make -h` or `metacrypto crypt --help` for more info.')

        make_parser = subparsers.add_parser('make', help="make a noise-file for input. Several sub-choices.")
        make_parser.add_argument('outfile', nargs="+", default='', type=str,
                                 help='Enter an outfile name for your noise-file.')
        make_parser.add_argument('-t', '--file-type', default='', help="enter the desired outfile type. If your outfile name contains a `.foo` at the end of it, this arg will append to that.")
        make_parser.add_argument('-s', '--string', action='store_true',
                                 help="make your noise-file a single line of random chars.")


        crypt_parser = subparsers.add_parser('crypt', help="Turn an arbitrary text document into a keystore.")
        crypt_parser.add_argument('infile', nargs="+", default='', type=str, help='enter an arbitrary text-file to analyze.')

        arrgs = top_level_parser.parse_args()

    else:
        raise argparse.ArgumentTypeError("you managed to mess up the entry-point function...you shouldn't be importing this into a module man this is the cli interface...")

if __name__ == "__main__":
    main()
