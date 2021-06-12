import re

import gmpy2

from ntmcrypt import diemitko
from ntmcrypt import utils


def gen_keys(size: int = 128) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    while True:
        p = diemitko.prime_gen(size)
        if p % 4 == 3:
            break

    while True:
        q = diemitko.prime_gen(size)
        if q % 4 == 3:
            break

    return p, q, p * q


def encrypt(
        string: str,
        other_pub_key: gmpy2.mpz
) -> list[gmpy2.mpz]:
    encrypted_blocks = []
    for block in utils.str_to_blocks(string, other_pub_key):
        encrypted_blocks.append(gmpy2.powmod(block, 2, other_pub_key))

    return encrypted_blocks


def decrypt(
        encrypted_blocks: list[gmpy2.mpz],
        p: gmpy2.mpz,
        q: gmpy2.mpz
) -> str:
    _, a, b = gmpy2.gcdext(p, q)
    n = p * q

    decrypted_blocks = []

    for block in encrypted_blocks:
        r = gmpy2.powmod(block, (p + 1) // 4, p)
        s = gmpy2.powmod(block, (q + 1) // 4, q)

        # x = (a * p * s + b * q * r) % n
        # y = (a * p * s - b * q * r) % n
        m1 = gmpy2.f_mod(a * p, n)
        m1 = gmpy2.f_mod(m1 * s, n)

        m2 = gmpy2.f_mod(b * q, n)
        m2 = gmpy2.f_mod(m2 * r, n)

        x = (m1 + m2) % n
        y = (m1 - m2) % n

        for item in [x % n, -x % n, y % n, -y % n]:
            item_str = str(item)[::-1]
            if re.match("^[0-2]+$", ''.join(item_str[i] for i in range(2, len(item_str), 3))) is not None:
                decrypted_blocks.append(item)
                break

    return utils.blocks_to_str(decrypted_blocks)
