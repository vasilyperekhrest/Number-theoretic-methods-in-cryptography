import random

import gmpy2

from cryptopy import diemitko as dk
from cryptopy import utils


def gen_keys(num_digits: int = 120) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    p = dk.prime_gen(num_digits)
    q = dk.prime_gen(num_digits)

    n = p * q
    phi = (p-1) * (q-1)

    while True:
        public_key = gmpy2.mpz(random.randint(1, 10**(phi.num_digits() - 1)))
        d, a, b = gmpy2.gcdext(public_key, phi)
        if d == 1:
            break

    private_key = a
    return n, public_key, private_key


def encrypt(
        string: str,
        public_key: gmpy2.mpz,
        n: gmpy2.mpz
) -> list[gmpy2.mpz]:
    blocks = utils.str_to_blocks(string, n)

    encrypted_blocks = []

    for block in blocks:
        encrypted_blocks.append(gmpy2.powmod(block, public_key, n))

    return encrypted_blocks


def decrypt(
        encrypted_blocks: list[gmpy2.mpz],
        private_key: gmpy2.mpz,
        n: gmpy2.mpz
) -> str:
    decrypted_blocks = []

    for block in encrypted_blocks:
        decrypted_blocks.append(gmpy2.powmod(block, private_key, n))

    return utils.blocks_to_str(decrypted_blocks)
