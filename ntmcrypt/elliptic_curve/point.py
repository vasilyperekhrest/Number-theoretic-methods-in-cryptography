import gmpy2


class Params:
    def __init__(
            self,
            a: gmpy2.mpz,
            b: gmpy2.mpz,
            p: gmpy2.mpz,
            q: gmpy2.mpz
    ) -> None:
        self.a = a
        self.b = b
        self.p = p
        self.q = q

    def __str__(self) -> str:
        return f"Elliptic curve params:\n" \
               f"a = {self.a}\n" \
               f"b = {self.b}\n" \
               f"p = {self.p}\n" \
               f"q = {self.q}\n"

    def __eq__(self, other) -> bool:
        if self.a == other.a and \
                self.b == other.b and \
                self.p == other.p and \
                self.q == other.q:
            return True
        else:
            return False

    def __ne__(self, other) -> bool:
        if self == other:
            return False
        else:
            return True


class Point:
    def __init__(
            self,
            x: gmpy2.mpz,
            y: gmpy2.mpz,
            params: Params,
            at_infinity: bool = False
    ) -> None:
        self.x: gmpy2.mpz = x
        self.y: gmpy2.mpz = y
        # point at infinity or not
        self.at_infinity: bool = at_infinity
        self.curve: Params = params

    def inverse(self):
        y = -self.y % self.curve.p
        return Point(self.x, y, self.curve)

    def __neg__(self):
        return self.inverse()

    def __str__(self) -> str:
        return f"({self.x};{self.y})"

    def __add__(self, other):
        if self.curve != other.curve:
            raise Exception("Elliptic curves are different")

        if self.at_infinity:
            return other

        if other.at_infinity:
            return self

        if self.x == other.x and self.y != other.y:
            return Point(gmpy2.mpz(), gmpy2.mpz(), self.curve, True)

        if self.y == other.y == 0:
            return Point(gmpy2.mpz(), gmpy2.mpz(), self.curve, True)

        if self == other:
            m = (3 * self.x ** 2 + self.curve.a) * \
                gmpy2.invert(2 * self.y, self.curve.p) % self.curve.p
        else:
            m = (self.y - other.y) * gmpy2.invert(self.x - other.x, self.curve.p)

        xr = (m ** 2 - self.x - other.x) % self.curve.p
        yr = (m * (self.x - xr) - self.y) % self.curve.p
        return Point(xr, yr, self.curve)

    def __iadd__(self, other):
        return self + other

    def __mul__(self, other):
        if not isinstance(other, int) and not isinstance(other, type(gmpy2.mpz())):
            raise Exception("The scalar must be of type int or mpz.")

        result = Point(gmpy2.mpz(), gmpy2.mpz(), self.curve, True)
        addend = Point(self.x, self.y, self.curve)

        for bit in bin(other)[2::][::-1]:
            if bit == "1":
                result += addend
            addend += addend

        return result

    def __imul__(self, other):
        return self * other

    def __eq__(self, other):
        if self.x == other.x and \
                self.y == other.y and \
                self.curve == other.curve and \
                self.at_infinity == other.at_infinity:
            return True
        else:
            return False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True
