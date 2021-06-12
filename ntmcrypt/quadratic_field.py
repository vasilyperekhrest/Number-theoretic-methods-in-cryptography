import gmpy2


class Number:
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a = a
        self.b = b
        self.c = c

    def conjugate(self):
        return Number(self.a, -self.b, self.c)

    def __str__(self):
        if self.b < 0:
            return f"{self.a}{self.b}√{self.c}"
        else:
            return f"{self.a}+{self.b}√{self.c}"

    def __mul__(self, other):
        if self.c != other.c:
            raise Exception("Error! The 'c' values must be the same.")

        return Number(self.a * other.a + self.c * self.b * other.b,
                      self.a * other.b + self.b * other.a, self.c)

    def __imul__(self, other):
        if self.c != other.c:
            raise Exception("Error! The 'c' values must be the same.")

        self.a = self.a * other.a + self.c * self.b * other.b
        self.b = self.a * other.b + self.b * other.a
        return self

    def __add__(self, other):
        if self.c != other.c:
            raise Exception("Error! The 'c' values must be the same.")

        return Number(self.a + other.a, self.b + other.b, self.c)

    def __iadd__(self, other):
        if self.c != other.c:
            raise Exception("Error! The 'c' values must be the same.")

        self.a += other.a
        self.b += other.b
        return self

    def __sub__(self, other):
        if self.c != other.c:
            raise Exception("Error! The 'c' values must be the same.")

        return Number(self.a - other.a, self.b - other.b, self.c)

    def __isub__(self, other):
        if self.c != other.c:
            raise Exception("Error! The 'c' values must be the same.")

        self.a -= other.a
        self.b -= other.b
        return self

    def __mod__(self, other):
        return Number(self.a % other, self.b % other, self.c)

    def __imod__(self, other):
        self.a %= other
        self.b %= other
        return self


def divmod(numerator: Number, denominator: Number, m: int) -> Number:
    numerator = numerator * denominator.conjugate() % m
    denominator = denominator * denominator.conjugate() % m
    reverse_elem = gmpy2.invert(denominator.a, m)
    return Number(numerator.a * reverse_elem, numerator.b * reverse_elem, numerator.c) % m


def powmod(num: Number, exp, m) -> Number:
    pw_list = [(1, num)]
    pw = 1
    while pw << 1 <= exp:
        pw <<= 1
        num = num * num % m
        pw_list.append((pw, num))

    for i, j in pw_list[::-1]:
        while pw + i <= exp:
            pw += i
            num = num * j % m

        if pw == exp:
            break

    return num
