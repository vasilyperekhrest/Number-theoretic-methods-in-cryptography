import random
import time

import gmpy2


def prime_gen(
        size: int,
        verbose: bool = False
) -> gmpy2.mpz:
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

        u = 0
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
