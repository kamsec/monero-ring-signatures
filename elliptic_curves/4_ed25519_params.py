
# Fourth implementation of the elliptic curves arithmetic
# - affine coordinates: (x, y)
# - Twisted Edwards curve equation: a * x**2 + y**2 = 1 + d * x**2 * y**2
# - Point compression and decompression functions
# - Ed25519 curve parameters used
# https://datatracker.ietf.org/doc/html/rfc8032#page-10


from math import ceil, log2

def inv(x, p):
    return pow(x, -1, p)

# straight to Twisted Edwards curves as they contain Edwards curves
class EllipticCurve:
    def __init__(self, p, a, d):
        self.p = p
        self.a = a
        self.d = d
        self.b = 8 * ceil((p).bit_length() / 8)  # for 13 gives 8, for 2^255-19 gives 256
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

    def validate(self):
        x, y, a, d, p = self.x, self.y, self.EC.a, self.EC.d, self.EC.p
        return ((a*x**2+y**2-1-d*x**2*y**2) % p == 0 and
                (0 <= x < p) and (0 <= y < p))

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
        x = ((x1 * y2 + y1 * x2) * inv(1 + s, p)) % p
        y = ((y1 * y2 - a * x1 * x2) * inv(1 - s, p)) % p
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

    def compress(self):
        # for b=256, x is in (1, 2**255)
        # for b=8, x is in (1, 2**7)
        y_bin = bin(self.y)[2:].zfill(self.EC.b)
        if self.x & 1 == 1:  # if last bit of x is 1 (x is odd)
            new_y = '1' + y_bin[1:]
        else:
            new_y = '0' + y_bin[1:]
        return int(new_y, 2)  # .to_bytes(int(log2(b)), byteorder='little') # 1*

    @staticmethod
    def decompress(compressed_point, EC): # compressed_point = y with msb set to x's lsb
        # y = int.from_bytes(y, byteorder='little') # 1*
        p = EC.p
        y_msb = int(bin(compressed_point)[2:].zfill(EC.b)[0])  # if msb was 0 then zfill needed
        y = int('0' + bin(compressed_point)[2:].zfill(EC.b)[1:], 2)
        u = (y**2-1) % p
        v = ((d*y**2)+1) % p
        z = ((u*v**3)*pow((u*v**7), ((p-5)*inv(8,p))%p, p)) % p  # int((p-5)/8)  (p-5) * inv(8, p)
        vz2 = (v*z**2) % p
        if vz2 == u:
            x = z
        elif vz2 == -u % p:
            x = (z*pow(2, ((p-1)*inv(4,p))%p, p)) % p  # int((p-1)/4),  (p-1) * inv(4, p)
        else:
            raise Exception('Error in decompression formulas')
        if y_msb != x & 1:
            x = -x % p
        return EC.point(x, y)

p = pow(2, 255) - 19
a = -1
d = -(121665 * inv(121666, p)) % p

EC = EllipticCurve(p, a, d)

Gy = (4 * inv(5, p)) % p  # generator point is defined by y coordinate only, x coordinate is obtained from decompression
G = Point.decompress(Gy, EC)  # (15112221349535400772501151409588531511454012693041857206046113283949847762202, 46316835694926478169428394003475163141307993866256225615783033603165251855960)

def test_arithmetic():
    G = EC.point(15112221349535400772501151409588531511454012693041857206046113283949847762202, 46316835694926478169428394003475163141307993866256225615783033603165251855960)
    print(17*G == 15*G + 5*G - 3*G + EC.O - EC.O + 0*G)
test_arithmetic()

def test_compression():
    G = EC.point(15112221349535400772501151409588531511454012693041857206046113283949847762202, 46316835694926478169428394003475163141307993866256225615783033603165251855960)
    some_points = [x*G for x in range(50)]
    compressed_points = [x.compress() for x in some_points]
    decompressed_points = [Point.decompress(x, EC) for x in compressed_points]
    print(some_points == decompressed_points)
test_compression()

