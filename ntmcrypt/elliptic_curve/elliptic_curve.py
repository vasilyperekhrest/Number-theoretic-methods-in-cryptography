import random

import sympy

from ntmcrypt.elliptic_curve.point import Point, Params
from ntmcrypt import utils


class EllipticCurve:
    def __init__(self, a: int, b: int, p: int, q: int):
        if p < 4 or (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p == 0:
            raise Exception("Error!\n"
                            "Parameter n must be greater than 3.\n"
                            "Parameters a and b must satisfy the comparison 4a^3 + 27b^2 != 0 (mod p)\n")
        self.a = a
        self.b = b
        self.p = p
        self.q = q

    def is_includes_point(self, pnt: Point) -> bool:
        """
        y^2 = x^3 + ax + b

        :param pnt:
        :return bool:
        """

        if pnt.at_infinity:
            return True

        if pow(pnt.y, 2, self.p) == (pow(pnt.x, 3, self.p) + self.a * pnt.x + self.b) % self.p:
            return True
        else:
            return False

    def rand_point(self) -> Point:
        while True:
            x: int = random.randint(1, self.p)
            f: int = (pow(x, 3, self.p) + self.a * x + self.b) % self.p

            if not (sympy.legendre_symbol(f, self.p) != 1):
                break

        y: int = utils.sqrt_mod(f, self.p)
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
