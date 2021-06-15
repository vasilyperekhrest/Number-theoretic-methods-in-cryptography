import random

import gmpy2

from ntmcrypt import utils


def gen_keys(p: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Function for generating public and private user keys.

    :param p: a large prime from which public and private keys will be generated.
    :return: public and private keys.
    """
    phi = p - 1

    while True:
        public_key = gmpy2.mpz(random.randint(1, phi))
        d, private_key, b = gmpy2.gcdext(public_key, phi)
        if d == 1:
            break

    return public_key, private_key % phi


def encrypt(data: any, public_key, p) -> list[gmpy2.mpz]:
    """Data encryption function by Shamir protocol.

    :param data: data, string or list with numbers, where each number is not more than p.
    :param public_key: the public key of the user to whom the encrypted data will be sent.
    :param p: public large prime number, on the basis of which the private and public keys of users were built.
    :return: list containing encrypted blocks.
    """
    if type(data) is str:
        blocks = utils.str_to_blocks(data, p)
    else:
        blocks = data

    encrypted_blocks = []
    for block in blocks:
        encrypted_block = gmpy2.powmod(block, public_key, p)
        encrypted_blocks.append(encrypted_block)

    return encrypted_blocks


def decrypt(
        encrypted_blocks: list[gmpy2.mpz],
        private_key: gmpy2.mpz,
        p: gmpy2.mpz
) -> str:
    """The function of decrypting data encrypted using the Shamir protocol.

    :param encrypted_blocks: encrypted blocks.
    :param private_key: your private key.
    :param p: public large prime number, on the basis of which the private and public keys of users were built.
    :return: decrypted string.
    """
    decrypted_blocks = []

    for block in encrypted_blocks:
        decrypted_block = gmpy2.powmod(block, private_key, p)
        decrypted_blocks.append(decrypted_block)

    return utils.blocks_to_str(decrypted_blocks)
