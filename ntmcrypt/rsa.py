import random

import gmpy2

from ntmcrypt import utils


def gen_keys(size: int = 120) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    """Function for generating n, public and private keys of the RSA cryptosystem.

    :param size: the dimension of prime numbers (in bits).
    :return: n, public and private keys
    """
    p = utils.prime_gen(size)
    q = utils.prime_gen(size)

    n = p * q
    phi = (p-1) * (q-1)

    while True:
        public_key = gmpy2.mpz(random.randint(1, 10**(phi.num_digits() - 1)))
        d, private_key, b = gmpy2.gcdext(public_key, phi)
        if d == 1:
            break

    return n, public_key, private_key % phi


def encrypt(
        string: str,
        public_key: gmpy2.mpz,
        n: gmpy2.mpz
) -> list[gmpy2.mpz]:
    """Data encryption function (strings) using the RSA cryptosystem.

    :param string: the string to encrypt.
    :param public_key: the public key of the user to whom the ciphertext will be sent.
    :param n: product of prime p and q, which are secret.
    :return: list containing encrypted blocks
    """
    encrypted_blocks = []

    for block in utils.str_to_blocks(string, n):
        encrypted_blocks.append(gmpy2.powmod(block, public_key, n))

    return encrypted_blocks


def decrypt(
        encrypted_blocks: list[gmpy2.mpz],
        private_key: gmpy2.mpz,
        n: gmpy2.mpz
) -> str:
    """Function of decryption of data encrypted using the RSA cryptosystem.

    :param encrypted_blocks: encrypted blocks.
    :param private_key: your private keys.
    :param n: product of prime p and q, which are secret.
    :return: decrypted string.
    """
    decrypted_blocks = []

    for block in encrypted_blocks:
        decrypted_blocks.append(gmpy2.powmod(block, private_key, n))

    return utils.blocks_to_str(decrypted_blocks)
