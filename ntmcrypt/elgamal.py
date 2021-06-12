import random

import gmpy2

from ntmcrypt import diemitko
from ntmcrypt import utils


def gen_keys(size: int = 128) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    p = diemitko.prime_gen(size)
    phi = p - 1
    g = utils.primitive_root(p)

    while True:
        private_key = gmpy2.mpz(random.randint(1, phi))
        if gmpy2.gcd(private_key, phi) == 1:
            break

    y = gmpy2.powmod(g, private_key, p)

    return p, g, y, private_key


def gen_session_key(other_p: gmpy2.mpz) -> gmpy2.mpz:
    phi = other_p - 1

    while True:
        session_key = random.randint(1, phi)
        if gmpy2.gcd(session_key, phi) == 1:
            break

    return session_key


def encrypt(
        string: str,
        session_key: gmpy2.mpz,
        other_p: gmpy2.mpz,
        other_g: gmpy2.mpz,
        other_y: gmpy2.mpz
) -> tuple[list[gmpy2.mpz], gmpy2.mpz]:
    blocks = utils.str_to_blocks(string, other_p)
    b = gmpy2.powmod(other_y, session_key, other_p)

    encrypted_blocks = []
    for block in blocks:
        encrypted_block = gmpy2.f_mod(gmpy2.mul(b, block), other_p)
        encrypted_blocks.append(encrypted_block)

    a = gmpy2.powmod(other_g, session_key, other_p)

    return encrypted_blocks, a


def decrypt(
        encrypted_blocks: list[gmpy2.mpz],
        a: gmpy2.mpz,
        p: gmpy2.mpz,
        private_key: gmpy2.mpz
) -> str:
    m = gmpy2.powmod(a, p - 1 - private_key, p)

    decrypted_blocks = []
    for block in encrypted_blocks:
        decrypted_block = gmpy2.f_mod(gmpy2.mul(m, block), p)
        decrypted_blocks.append(decrypted_block)

    return utils.blocks_to_str(decrypted_blocks)
