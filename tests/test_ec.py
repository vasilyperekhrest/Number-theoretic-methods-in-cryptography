import pytest

from ntmcrypt.elliptic_curve.elliptic_curve import EllipticCurve
from ntmcrypt.elliptic_curve.point import Point


@pytest.mark.parametrize(
    "ec, p1, p2, answer",
    [(EllipticCurve(1, 1, 13, 0), (4, 2), (10, 6), (11, 2)),
     (EllipticCurve(2, 3, 97, 0), (17, 10), (95, 31), (1, 54)),
     (EllipticCurve(24, 28, 113, 0), (51, 26), (102, 44), (9, 42)),
     (EllipticCurve(24, 28, 113, 0), (99, 98), (105, 51), (30, 96)),
     (EllipticCurve(42, 55, 127, 0), (66, 126), (99, 26), (12, 126))])
def test_elliptic_curve_add(ec, p1, p2, answer):
    p = Point(*p1, ec.get_params())
    q = Point(*p2, ec.get_params())

    assert p + q == Point(*answer, ec.get_params())


@pytest.mark.parametrize(
    "ec, p, k, answer",
    [(EllipticCurve(45, 44, 101, 0), (39, 35), 12, (60, 33)),
     (EllipticCurve(39, 48, 107, 0), (62, 30), 7, (10, 49)),
     (EllipticCurve(36, 39, 103, 0), (82, 42), 16, (6, 33)),
     (EllipticCurve(12, 456, 233, 0), (84, 22), 211, (33, 212)),
     (EllipticCurve(342, 92, 347, 0), (55, 72), 45, (155, 323))])
def test_elliptic_curve_mul(ec, p, k, answer):
    p = Point(*p, ec.get_params())

    assert p * k == Point(*answer, ec.get_params())



