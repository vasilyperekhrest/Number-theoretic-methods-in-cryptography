import gmpy2
import sympy

from ntmcrypt import quadratic_field as qf
from ntmcrypt import diemitko
from ntmcrypt import utils


def gen_keys(size: int = 128):
    p = diemitko.prime_gen(size)
    q = diemitko.prime_gen(size)
    n = p * q

    c = 2
    while True:
        legendre_symbol_p = sympy.legendre_symbol(c, p)
        legendre_symbol_q = sympy.legendre_symbol(c, q)
        if -p % 4 == legendre_symbol_p % 4 and -q % 4 == legendre_symbol_q % 4:
            break
        c += 1

    s = 2
    while True:
        jacobi_symbol_s = sympy.jacobi_symbol(s ** 2 - c, n)
        if jacobi_symbol_s == -1 and gmpy2.gcd(s, n) == 1:
            break
        s += 1

    m = ((p - legendre_symbol_p) >> 1) * ((q - legendre_symbol_q) >> 1)

    d = diemitko.prime_gen(size//2)
    while True:
        if gmpy2.gcd(d, m) == 1:
            break
        d = diemitko.prime_gen(size//2)

    e = ((m + 1) >> 1) * gmpy2.invert(d, m) % m

    return (p, q, m, d), (n, c, s, e)


def encrypt(
        string: str,
        other_pub_keys: tuple[int, int, int, int],
) -> list[tuple[int, int, int]]:
    n, c, s, e = other_pub_keys
    blocks = utils.str_to_blocks(string, n)

    encrypted_blocks = []
    for block in blocks:
        jacobi_symbol_w = sympy.jacobi_symbol(block ** 2 - c, n)

        if jacobi_symbol_w == 1:
            b1 = 0
            gamma = qf.Number(block, 1, c)
        elif jacobi_symbol_w == -1:
            b1 = 1
            gamma = qf.Number(block, 1, c) * qf.Number(s, 1, c) % n
        else:
            raise Exception("Jacobi symbol == 0")

        alpha = qf.divmod(gamma, gamma.conjugate(), n)
        b2 = alpha.a % 2

        alpha_e = qf.powmod(alpha, e, n)
        e = alpha_e.a * gmpy2.invert(alpha_e.b, n) % n

        encrypted_blocks.append((e, b1, b2))

    return encrypted_blocks


def decrypt(
        encrypted_blocks: list,
        private_keys: list,
        me_pub_keys: list
):
    p, q, m, d = private_keys
    n, c, s, e = me_pub_keys

    decrypted_blocks = []
    for block in encrypted_blocks:
        e, b1, b2 = block

        alpha_2e = qf.divmod(qf.Number(e, 1, c), qf.Number(e, -1, c), n)
        alpha_2ed = qf.powmod(alpha_2e, d, n)

        if (b2 == 1 and alpha_2ed.a % 2 == 0) or (b2 == 0 and alpha_2ed.a % 2 == 1):
            alpha_2ed = qf.Number(n - alpha_2ed.a, n - alpha_2ed.b, alpha_2ed.c) % n

        if b1 == 1:
            addition = qf.Number(s, 1, c)
            addition = qf.divmod(addition, addition.conjugate(), n)
            addition.b *= -1
            alpha_2ed = alpha_2ed * addition % n

        num = qf.divmod(qf.Number(alpha_2ed.a + 1, alpha_2ed.b, alpha_2ed.c),
                        qf.Number(alpha_2ed.a - 1, alpha_2ed.b, alpha_2ed.c),
                        n) * qf.Number(0, 1, alpha_2ed.c) % n

        decrypted_blocks.append((num.a + num.b) % n)

    return utils.blocks_to_str(decrypted_blocks)
