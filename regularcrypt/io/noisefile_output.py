from __future__ import print_function, unicode_literals
import os

from regularcrypt.utils.validations import OutputValidator

__doc__ = """
Purpose:
========
We'll save our "secret garbage" file(s) here. 
These will be the default document-type used by our Skeleton-Key generator.


Keep in mind!: We're still in Stage #1: Create an arbitrary document for input & analysis. 
               We ARE NOT reading in an arbitrary file yet. 
               That's next. It's in Stage #2: Read-in Arbitrary File & Index. 

Theory:
=======
Starting with the minimalist approach...Going to disguise our output as an openssh private-key file.

Keep in mind!: Any data-corruption within our keyfile-doc will break everything, so it's gonna need to be redundant AF.
               Going to make 3 copies to start off...will probably add some in-file redundancy logic eventually.

Application:
============

 - Unicode to ascii is gonna be a thing here. 

 - Need to make the save-mechanism simplistic & modular to allow for future expansion.

 - Need somewhere to put this.
   - Default's gonna be `$HOME/Documents/` if it exists.
   - We'll also give teh user the option to store it in `$HOME/.ssh/` if they want.

 - Need a filetype.
   - Default filetype is going to be `.openssh` to make it look like this is an encrypted file...it's not.
     - Side Note: I find this hilarious. I hope someone tries to decrypt it.
   - We'll also give the user the option to specify whatever filetype they desire.
     - Ideally it will correspond to a text-document with line-numbers...kinda riding on that @ this point.

- Need a USER-ENTERED filename.
   - going to be mandatory
     - ...no escaping that without introducing a pretty massive security-hole.
     - if the filename was regular, it would stand out like a sore thumb if someone has this source-code.
       the `.openssh` default filetype is bad-enough on this front.

"""

def file_out(data, filepath, open_mode, writelines=True, verbose=False):
    OutputValidator.validate_writefunc_params(data=data, filepath=filepath, open_mode=open_mode)
    with open(filepath, open_mode) as outfile:
        if writelines:
            outfile.writelines(data)
        else:
            outfile.write(data)
    if verbose:
        print("INFO: {} Written.".format(filepath))



def join_path_and_save(root_dir, full_filename, overwrite_if_exists=False, verbose=False):
    full_filepath = os.path.join(root_dir, full_filename)
    file_exists_already = os.path.exists(full_filepath)
    if file_exists_already:
        if overwrite_if_exists:
            print('WARN: {} already exists & will be overwritten.\n'.format(os.path.join(root_dir, full_filename)))
            try:
                input('\nPress ENTER to continue, Ctrl+C to exit.\n> ')
            except KeyboardInterrupt:
                exit(1)
        else:
            print('ERROR: {} already exists, & the flag allowing overwriting has not been set to True.')
            exit(1)
    else:
        #Todo: idk...
        pass


