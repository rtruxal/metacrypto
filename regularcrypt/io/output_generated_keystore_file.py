from __future__ import print_function, unicode_literals

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
