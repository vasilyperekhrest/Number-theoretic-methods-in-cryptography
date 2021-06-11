import gmpy2
import sympy

from ntmcrypt import pyecm


def str_to_blocks(string: str, p: gmpy2.mpz) -> list[gmpy2.mpz]:
    blocks = []

    string_buffer = ""

    for byte in bytes(string, "utf-8"):
        string_buffer += str(byte).zfill(3)
        if len(string_buffer) + 3 >= p.num_digits():
            blocks.append(gmpy2.mpz(string_buffer))
            string_buffer = ""

    if string_buffer != "":
        blocks.append(gmpy2.mpz(string_buffer))

    return blocks


def blocks_to_str(blocks: list[gmpy2.mpz]):
    string_bytes = bytearray()
    buffer_bytes = bytearray()

    for block in blocks:
        block = str(block)[::-1]
        for pos in range(0, len(block), 3):
            buffer_bytes.append(gmpy2.mpz(block[pos:pos + 3][::-1]))

        string_bytes += buffer_bytes[::-1]
        buffer_bytes.clear()

    return string_bytes.decode("utf-8")


def primitive_root(p: gmpy2.mpz) -> gmpy2.mpz:
    phi = p - 1
    factor_list = pyecm.factors(phi, False, False, 4, 1)

    powers = []
    for divider in factor_list:
        powers.append(gmpy2.divexact(phi, divider))

    for root in range(2, p):
        flag = True
        for power in powers:
            if gmpy2.powmod(root, power, p) == 1:
                flag = False
                break

        if flag and gmpy2.is_prime(root):
            return root


def sqrt_mod(a: int, p: int) -> int:
    # Tonelli-Shanks
    if sympy.legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) >> 2, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s >>= 1
        e += 1

    n = 2
    while sympy.legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) >> 1, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0

        for m in range(r):
            if t == 1:
                break

            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m
