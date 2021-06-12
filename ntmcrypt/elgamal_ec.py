import random

import gmpy2

from ntmcrypt.elliptic_curve import elliptic_curve as ec
from ntmcrypt.elliptic_curve import point
from ntmcrypt.elliptic_curve import consts
from ntmcrypt import utils


def get_elliptic_curve(num: int = 1) -> ec.EllipticCurve:
    if not 0 < num < len(consts.curves):
        raise Exception(f"Error! Invalid elliptic curve index! (Try a range like this 0-{len(consts.curves)})")
    return ec.EllipticCurve(*map(lambda x: gmpy2.mpz(x), consts.curves.get(num)))


def gen_keys(curve: ec.EllipticCurve) -> tuple[gmpy2.mpz, point.Point, point.Point]:
    private_key = gmpy2.mpz(random.randint(1, curve.q))
    g = curve.rand_point()
    public_key = g * private_key
    return private_key, public_key, g


def encrypt(
        string: str,
        curve: ec.EllipticCurve,
        other_pub_key: point.Point,
        g: point.Point
) -> tuple[point.Point, list[gmpy2.mpz]]:
    k = gmpy2.mpz(random.randint(1, curve.q))
    r = g * k
    p = other_pub_key * k

    blocks = utils.str_to_blocks(string, curve.p)
    encrypted_blocks = []

    for block in blocks:
        encrypted_blocks.append(block * p.x % curve.p)

    return r, encrypted_blocks


def decrypt(
        r: point.Point,
        encrypted_blocks: list[gmpy2.mpz],
        curve: ec.EllipticCurve,
        private_key: gmpy2.mpz
) -> str:
    q = r * private_key

    decrypted_blocks = []

    for block in encrypted_blocks:
        decrypted_blocks.append(block * gmpy2.invert(q.x, curve.p) % curve.p)

    return utils.blocks_to_str(decrypted_blocks)
