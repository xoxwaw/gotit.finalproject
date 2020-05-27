import binascii
import hashlib
import random
import string

from main.constants import SALT_LENGTH

ALGORITHM = 'sha512'
SEED = 10000


def hash_password(password):
    """Hash a password for storing.
    """
    salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=SALT_LENGTH))

    hashed_password = hashlib.pbkdf2_hmac(ALGORITHM, password.encode('utf-8'),
                                          salt.encode('utf-8'), SEED)
    hashed_password = binascii.hexlify(hashed_password)
    return hashed_password.decode('ascii'), salt


def verify_password(password, hashed_password, salt):
    """Verify a stored password against one provided by user.
    """
    hashed = hashlib.pbkdf2_hmac(ALGORITHM,
                                 password.encode('utf-8'),
                                 salt.encode('utf-8'), SEED)
    hashed = binascii.hexlify(hashed).decode('ascii')
    return hashed == hashed_password
