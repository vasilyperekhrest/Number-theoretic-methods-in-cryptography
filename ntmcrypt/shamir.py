import random

import gmpy2

from ntmcrypt import utils


def gen_keys(p: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    phi = p - 1

    while True:
        public_key = gmpy2.mpz(random.randint(1, phi))
        d, private_key, b = gmpy2.gcdext(public_key, phi)
        if d == 1:
            break

    return public_key, private_key


def encrypt(data: any, key, p) -> list[gmpy2.mpz]:
    if type(data) is str:
        blocks = utils.str_to_blocks(data, p)
    else:
        blocks = data

    encrypted_blocks = []
    for block in blocks:
        encrypted_block = gmpy2.powmod(block, key, p)
        encrypted_blocks.append(encrypted_block)

    return encrypted_blocks


def decrypt(
        encrypted_blocks: list[gmpy2.mpz],
        key: gmpy2.mpz,
        p: gmpy2.mpz
) -> str:
    decrypted_blocks = []

    for block in encrypted_blocks:
        decrypted_block = gmpy2.powmod(block, key, p)
        decrypted_blocks.append(decrypted_block)

    return utils.blocks_to_str(decrypted_blocks)
