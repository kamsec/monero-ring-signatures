
# Second implementation of the elliptic curves arithmetic
# - affine coordinates: (x, y)
# - Twisted Edwards curve equation: a * x**2 + y**2 = 1 + d * x**2 * y**2
# - small parameters

# - going straight to Twisted Edwards curves as they contain Edwards curves
# Edwards curves:
#       x**2 + y**2 = 1 + d * x**2 * y**2
# Twisted Edwards curves:
#   a * x**2 + y**2 = 1 + d * x**2 * y**2

p = 13; a = -1; d = 2

def inv(x):
    return pow(x, -1, p)


class EllipticCurve:
    def __init__(self, p, a, d):
        self.p = p
        self.a = a
        self.d = d
        self.O = Point(0, 1, self)

    def point(self, x, y):
        return Point(x, y, self)

class Point:
    def __init__(self, x, y, EC):
        self.x = x
        self.y = y
        self.EC = EC
        if Point.validate(self):
            pass
        else:
            raise Exception(f"Provided coordinates {self} don't form a point on that curve")

    def __neg__(self):
        x, y, p = self.x, self.y, self.EC.p
        if x == 0 and y == 1:
            return self
        return Point((-x) % p, y, EC)

    def __add__(self, other):
        x1, y1, a, d, p = self.x, self.y, self.EC.a, self.EC.d, self.EC.p
        x2, y2 = other.x, other.y
        if self.EC != other.EC: raise Exception('You cannot add points on different curves')
        # a and d chosen in a way that formulas are COMPLETE - no exceptional cases
        # (a and a/d are not quadratic-residues in Fp)
        # no separate formulas for doubling
        s = (d * x1 * x2 * y1 * y2) % p
        x = ((x1 * y2 + y1 * x2) * inv(1 + s)) % p
        y = ((y1 * y2 - a * x1 * x2) * inv(1 - s)) % p
        return Point(x, y, self.EC)

    def __rmul__(self, other):  # (Point, scalar)
        if not isinstance(other, int) and not isinstance(self, Point):
            raise Exception('You can multiply only point by integer')
        else:
            Q = self.EC.O
            Q2 = Q
            bits = bin(other)[2:]
            min_number_of_bits = 64
            bits = '0' * (min_number_of_bits - len(bits)) + bits
            for b in bits[::-1]:
                Q2 = Q + self
                if b == '1':
                    Q = Q2
                self = self + self
            return Q

    def __mul__(self, other):
        return self.__rmul__(other)

    def __sub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def validate(self):
        x, y, a, d, p = self.x, self.y, self.EC.a, self.EC.d, self.EC.p
        if x is None:
            return True
        return ((a * x**2 + y**2 - 1 - d * x**2 * y**2) % p == 0 and
                (0 <= x < p) and (0 <= y < p))

EC = EllipticCurve(p, a, d)

def find_curve_points():
    print('Finding some points on that curve...')
    i = 1
    for x in range(0, p):
        for y in range(0, p):
            try:
                P_i = EC.point(x, y); print(f"P{i}", P_i)
                i += 1
            except:
                pass
find_curve_points()


def find_subgroup():
    print('Setting basepoint and checking generated group')
    P1 = EC.point(2, 4); print('P1', P1)
    P2 = P1
    for i in range(2, 20):
        P2 = P2 + P1; print(f"P{i}", P2)
find_subgroup()

def test_arithmetic():
    print('Testing curve arithmetic')
    G = EC.point(2, 4)
    print(17*G == 15*G + 5*G - 3*G + EC.O - EC.O + 0*G)
test_arithmetic()
