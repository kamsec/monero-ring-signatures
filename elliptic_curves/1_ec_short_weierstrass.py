
# First implementation of the elliptic curves arithmetic
# - affine coordinates: (x, y)
# - short Weierstrass curve equation: y**2 = x**3 + a * x + b
# - small parameters

p = 13; a = 1; b = 0

class EllipticCurve:
    def __init__(self, p, a, b):
        self.p = p  # characteristic of the finite field that curve is defined over
        self.a = a  # a coefficient in short Weierstrass form
        self.b = b  # b coefficient in short Weierstrass form
        self.O = Point(None, None, self)  # point at infinity

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

    # point inversion
    def __neg__(self):
        if self.x is None:
            return self
        return Point(self.x, (-self.y) % self.EC.p, self.EC)

    # point addition and doubling
    def __add__(self, other):
        if self.EC != other.EC:
            raise Exception('You cannot add two points on different curves')
        p = self.EC.p

        # cases involving identity element
        if self.x is None:
            return other
        elif other.x is None:
            return self
        elif self.x == other.x and other.y == ((-self.y) % self.EC.p):
            return self.EC.O
        else:
            # cases not involving identity element
            if self.x == other.x and self.y == other.y:
                # doubling
                s = ((3 * self.x ** 2 + self.EC.a) * pow(2 * self.y, -1, p)) % p
            else:
                # addition
                s = ((other.y - self.y) * pow((other.x - self.x + p), -1, p)) % p
            x = (s ** 2 - self.x - other.x) % p
            y = (s * (self.x - x) - self.y) % p
            return Point(x, y, self.EC)

    # point scalar multiplication, scalar * Point
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

    # point scalar multiplication, Point * scalar
    def __mul__(self, other):
        return self.__rmul__(other)

    # point substraction, Point_1 - Point_2
    def __sub__(self, other):
        return self + (-other)

    # points equality check, Point_1 == Point_2
    def __eq__(self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False

    # printing
    def __repr__(self):
        return f'({self.x}, {self.y})'

    # check if point lays on the curve
    def validate(self):
        if self.x is None:
            return True
        return ((self.y ** 2 - (self.x ** 3 + self.EC.a * self.x + self.EC.b)) % self.EC.p == 0 and
                0 <= self.x < self.EC.p and 0 <= self.y < self.EC.p)


EC = EllipticCurve(p, a, b)


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
    P1 = EC.point(9, 6); print('P1', P1)
    P2 = P1
    for i in range(2, 20):
        P2 = P2 + P1; print(f"P{i}", P2)
find_subgroup()


def test_arithmetic():
    print('Testing curve arithmetic')
    G = EC.point(9, 6)
    print(17*G == 15*G + 5*G - 3*G + EC.O - EC.O + 0*G)
test_arithmetic()
