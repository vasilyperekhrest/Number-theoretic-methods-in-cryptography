import random

import gmpy2

from ntmcrypt import utils


def gen_keys(size: int = 128) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    """Function for generating public and private keys for a user.

    :param size: required number of bits (default 128).
    :return: User's public and private keys.
    """
    p = utils.prime_gen(size)
    phi = p - 1
    g = utils.primitive_root(p)

    while True:
        private_key = gmpy2.mpz(random.randint(1, phi))
        if gmpy2.gcd(private_key, phi) == 1:
            break

    y = gmpy2.powmod(g, private_key, p)

    return p, g, y, private_key


def gen_session_key(other_p: gmpy2.mpz) -> gmpy2.mpz:
    """Function for creating a session key between users.

    :param other_p: the public key of the user to connect to.
    :return: your session key.
    """
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
    """Data (string) encryption function with El Gamal scheme.

    :param string: the string to encrypt.
    :param session_key: the session key of the user who is going to encrypt the message.
    :param other_p: another user's public key p.
    :param other_g: another user's public key g.
    :param other_y: another user's public key y.
    :return: Encrypted blocks and parameter "a".
    """
    b = gmpy2.powmod(other_y, session_key, other_p)

    encrypted_blocks = []
    for block in utils.str_to_blocks(string, other_p):
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
    """Decryption function for data encrypted using El Gamal's scheme.

    :param encrypted_blocks: encrypted blocks.
    :param a: parameter "a".
    :param p: your public key p.
    :param private_key: your private key.
    :return: decrypted string.
    """
    m = gmpy2.powmod(a, p - 1 - private_key, p)

    decrypted_blocks = []
    for block in encrypted_blocks:
        decrypted_block = gmpy2.f_mod(gmpy2.mul(m, block), p)
        decrypted_blocks.append(decrypted_block)

    return utils.blocks_to_str(decrypted_blocks)
