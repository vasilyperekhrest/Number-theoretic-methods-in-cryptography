import time
import random

import gmpy2
import sympy

from ntmcrypt import pyecm


def str_to_blocks(string: str, p: gmpy2.mpz) -> gmpy2.mpz:
    """This function converts a string to a number and forms blocks of such numbers,
    where each number is not more than a given p.

    :param string: the line to be split into blocks.
    :param p: the module by which the line will be divided.
    :return: blocks piece by piece, since the function is a generator.
    """
    string_buffer = ""

    for byte in bytes(string, "utf-8"):
        string_buffer += str(byte).zfill(3)
        if len(string_buffer) + 3 >= p.num_digits():
            yield gmpy2.mpz(string_buffer)
            string_buffer = ""

    if string_buffer != "":
        yield gmpy2.mpz(string_buffer)


def blocks_to_str(blocks: list[gmpy2.mpz]) -> str:
    """The function converts blocks of numbers to a line.

    :param blocks: blocks - a list containing numbers like mpz.
    :return: string, if successful, otherwise an exception is thrown or the string will contain invalid characters.
    """
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
    """function for calculating the primitive root modulo a prime number. For the calculation,
    it is required to factorize p-1, which is long enough for large p. For factorization, the ECM method is used,
    module pyecm.py

    :param p: module - prime number (p > 2).
    :return: primitive root.
    """
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


def sqrt_mod(a: gmpy2.mpz, p: gmpy2.mpz) -> gmpy2.mpz:
    """The function for calculating the square root modulo a prime number is Tonelli-Shanks algorithm.
    For comparisons like x^2 = a (mod p)

    :param a: quadratic residue.
    :param p: prime number (p > 2).
    :return: x satisfying the comparison.
    """
    if sympy.legendre_symbol(a, p) != 1:
        return gmpy2.mpz()
    elif a == 0:
        return gmpy2.mpz()
    elif p == 2:
        return gmpy2.mpz()
    elif p % 4 == 3:
        return gmpy2.powmod(a, (p + 1) >> 2, p)

    s = p - 1
    e = gmpy2.mpz()
    while s % 2 == 0:
        s >>= 1
        e += 1

    n = 2
    while sympy.legendre_symbol(n, p) != -1:
        n += 1

    x = gmpy2.powmod(a, (s + 1) >> 1, p)
    b = gmpy2.powmod(a, s, p)
    g = gmpy2.powmod(n, s, p)
    r = e

    while True:
        t = b
        m = 0

        for m in range(r):
            if t == 1:
                break

            t = gmpy2.powmod(t, 2, p)

        if m == 0:
            return x

        gs = gmpy2.powmod(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def prime_gen(
        size: int = 128,
        verbose: bool = False
) -> gmpy2.mpz:
    """Generation of a prime number of a given dimension (in bits). This function is an implementation of the
    GOST algorithm, which in turn is based on the Diemitko theorem.

    :param size: required number of bits (default 128).
    :param verbose: detailed output of each generation step (True or False).
    :return: prime number of given dimension.
    """
    q = gmpy2.mpz(3)

    t_list = [gmpy2.mpz(size)]
    while True:
        t = gmpy2.mpz(gmpy2.ceil(t_list[-1] / 2))
        if t > q.bit_length():
            t_list.append(t)
        else:
            break

    t_list = t_list[::-1]
    if verbose:
        print(t_list)
        print()

    all_time = 0
    index = 0
    while index < len(t_list):
        begin_t = time.time()
        num_bits = gmpy2.mpz(2 ** (t_list[index] - 1))
        n1 = gmpy2.mpz(gmpy2.ceil(num_bits / q))
        n2 = gmpy2.mpz(num_bits / q * gmpy2.mpfr(random.random()))
        n = n1 + n2

        if gmpy2.is_odd(n):
            n += 1

        u = gmpy2.mpz()
        while True:
            p = q*(n + u) + 1

            if p > 2**t_list[index]:
                break

            if gmpy2.powmod(2, p - 1, p) == 1 and gmpy2.powmod(2, n + u, p) != 1:
                index += 1
                end_t = time.time() - begin_t
                all_time += end_t
                if verbose:
                    print("time =", end_t)
                    print("p =", p)
                    print("q =", q)
                    print("p: num digits =", p.num_digits())
                    print("p: num bits =", p.bit_length())
                    print("q: num digits =", q.num_digits())
                    print("q: num bits =", q.bit_length())
                    print("n =", n)
                    print("u =", u)
                    print("r < 4(q+1):", n+u < 4*(q+1))
                    print()

                q = p
                break

            u += 2

    if verbose:
        print("all time =", all_time)
        print()

    return p
