import random

import gmpy2

from ntmcrypt import diemitko as dk
from ntmcrypt import utils


def gen_public_shared_keys(num_digits: int = 128, base: int = 2):
    p = dk.prime_gen(num_digits, base=base)
    g = utils.primitive_root(p)
    return p, g


def gen_keys(p: gmpy2.mpz, g: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    private_key = random.randint(1, 200)
    public_key = gmpy2.powmod(g, private_key, p)
    return public_key, private_key


def create_private_shared_key(
        public_key: gmpy2.mpz,
        private_key: gmpy2.mpz,
        p: gmpy2.mpz
) -> gmpy2.mpz:
    shared_key = gmpy2.powmod(public_key, private_key, p)
    return shared_key
