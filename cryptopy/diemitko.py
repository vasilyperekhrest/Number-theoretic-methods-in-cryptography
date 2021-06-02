import random

import gmpy2
import sympy


def prime_gen(
        size: int,
        q: gmpy2.mpz = None,
        base: int = 10
) -> gmpy2.mpz:
    """
    Generation of primes of a given length based on the Diemitko theorem.

    :param size: Number of digits in a number.
    :param q: Initial prime number.
    :param base: Number system, on the basis of which a number of a given length will be built.
    (base = 2 -> size = number of bits).

    :return: A prime number of a given length.
    """
    if q is None:
        q = gmpy2.mpz(sympy.prime(size))

    num_digits = gmpy2.mpz(base**(size-1))
    u = gmpy2.mpz()

    n1 = gmpy2.f_div(num_digits, q)
    n2 = gmpy2.mpz(num_digits * gmpy2.mpfr(random.random()) / q)
    n = n1 + n2

    if gmpy2.is_odd(n):
        n += 1

    while True:
        p = (n + u)*q + 1

        if gmpy2.powmod(2, p - 1, p) == 1 and gmpy2.powmod(2, n + u, p) != 1:
            break

        u += 2

    return p
