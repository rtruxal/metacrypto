# metacrypto
A novel credential generation & obfuscation mechanism using giant files full of noise & regex-extractors made on-the-fly.

# Some Definitions:
- *Keystore*: a file used to store passwords in an obfuscated manner. A "Skeleton-key" is usually used to decrypt and retrieve passwords from it.
- *Skeleton-Key*: The device used to de-obfuscate a "Keystore," allowing passwords to be retrieved. Traditionally this is another password.
- *Password*: A secret bit of information you use to access various services, & which you might like to store securely somewhere...like in a "Keystore" for example.

# What does a typical keystore look like?
When you want to store passwords, you'll put them in some kind of keystore-file, which is itself encrypted.

That's a relatively safe mechanism for storing preexisting passwords, & in fact it's the industry standard.

However, the computational complexity of decrypting said keystore is necessarily `<` O(n^n), because there is a necessarily a pattern in your resultant keystore (albeit an impressively obfuscated one if you're using a standard like Twofish, Blowfish, or AES256.)


# How is metacrypto different?

- The keystore file is generated first from random-noise, and your passwords *must* be generated from that.
- instead of using a Skeleton-Key to decrypt your keystore, you'll use line-numbers + regex extracts characters from the noise-file keystore allowing you to generate your passwords from the noise on-the-fly.
- This means the computational complexity of decrypting a metacrypto keystore file is `==` O(n^n), as all relevant decryption patterns reside *only* within your regex skeleton-key.