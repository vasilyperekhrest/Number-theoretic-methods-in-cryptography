import random

import sympy
import gmpy2

from ntmcrypt.elliptic_curve.point import Point, Params
from ntmcrypt import utils


class EllipticCurve:
    def __init__(
            self,
            a: gmpy2.mpz,
            b: gmpy2.mpz,
            p: gmpy2.mpz,
            q: gmpy2.mpz
    ) -> None:
        """ An elliptic curve of the form y^2 = x^3 + ax + b

        :param a: parameter 'a' of an elliptic curve. (mpz)
        :param b: parameter 'b' of an elliptic curve. (mpz)
        :param p: parameter (module) 'p' of an elliptic curve. (mpz)
        :param q: parameter (group order) 'q' of an elliptic curve. (mpz)
        """
        if p < 4 or (4 * gmpy2.powmod(a, 3, p) + 27 * gmpy2.powmod(b, 2, p)) % p == 0:
            raise Exception("Error!\n"
                            "Parameter n must be greater than 3.\n"
                            "Parameters a and b must satisfy the comparison 4a^3 + 27b^2 != 0 (mod p)\n")
        self.a = a
        self.b = b
        self.p = p
        self.q = q

    def is_includes_point(self, pnt: Point) -> bool:
        """Whether a point belongs to an elliptic curve or not.

        :param pnt: the point to be checked.
        :return: True or False.
        """
        if pnt.at_infinity:
            return True

        if gmpy2.powmod(pnt.y, 2, self.p) == (gmpy2.powmod(pnt.x, 3, self.p) + self.a * pnt.x + self.b) % self.p:
            return True
        else:
            return False

    def rand_point(self) -> Point:
        """Method for generating a random point.

        :return: randomly generated point.
        """
        while True:
            x = gmpy2.mpz(random.randint(1, self.p))
            f = (gmpy2.powmod(x, 3, self.p) + self.a * x + self.b) % self.p

            if not (sympy.legendre_symbol(f, self.p) != 1):
                break

        y = utils.sqrt_mod(f, self.p)
        return Point(x, y, self.get_params())

    def get_params(self) -> Params:
        return Params(self.a, self.b, self.p, self.q)

    def __str__(self):
        return f"y^2 = x^3 + {self.a}x + {self.b}"

    def __eq__(self, other):
        if self.a == other.a and \
                self.b == other.b and \
                self.p == other.p and \
                self.q == other.q:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True
