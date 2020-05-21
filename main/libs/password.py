import hashlib
import binascii
import os

from main.constants import SALT_LEN

ALGORITHM = 'sha512'
SEED = 10000


def encoder(password):
    """Hash a password for storing.
    """
    salt = os.urandom(SALT_LEN)
    pwdhash = hashlib.pbkdf2_hmac(ALGORITHM, password.encode('utf-8'),
                                  salt, SEED)
    pwdhash = binascii.hexlify(pwdhash)
    return pwdhash.decode('ascii'), salt


def verify_password(stored_pwd, salt, provided_pwd):
    """Verify a stored password against one provided by user.
    """
    pwdhash = hashlib.pbkdf2_hmac(ALGORITHM,
                                  provided_pwd.encode('utf-8'),
                                  salt, SEED)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_pwd
