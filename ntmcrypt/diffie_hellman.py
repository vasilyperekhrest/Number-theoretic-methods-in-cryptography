import random

import gmpy2

from ntmcrypt import utils


def gen_public_shared_keys(size: int = 128) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Function for generating shared public keys.

    :param size: required number of bits (default 128).
    :return: prime number and its primitive root.
    """
    p = utils.prime_gen(size)
    g = utils.primitive_root(p)
    return p, g


def gen_keys(p: gmpy2.mpz, g: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Function for generating private and public keys for a user based on public keys (p and g).

    :param p: large prime number.
    :param g: primitive root.
    :return: User's public and private keys.
    """
    private_key = gmpy2.mpz(random.randint(1, 200))
    public_key = gmpy2.powmod(g, private_key, p)
    return public_key, private_key


def create_private_shared_key(
        public_key: gmpy2.mpz,
        private_key: gmpy2.mpz,
        p: gmpy2.mpz
) -> gmpy2.mpz:
    """A function to create a shared private key for users based on their public keys.

    :param public_key: The public key of the user to connect to.
    :param private_key: The private key of the user with whom the connection is established (you).
    :param p: large prime number - public shared key.
    :return: private shared key (if 2 users) or part of the private key (if 3 and more users).
    """
    shared_key = gmpy2.powmod(public_key, private_key, p)
    return shared_key
