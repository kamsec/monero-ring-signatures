
# Fifth and final implementation of the elliptic curves arithmetic
# - affine coordinates: (x, y)
# - Twisted Edwards curve equation: a * x**2 + y**2 = 1 + d * x**2 * y**2
# - Point compression and decompression functions
# - Ed25519 curve parameters used
# - Hash functions added
# - Refactored code, removed tests - this file is used in signatures/ folder as elliptic curves implementation
# https://datatracker.ietf.org/doc/html/rfc8032#page-10

# from math import log2  # needed if we want compression / decompression bytes as output
import secrets


def inv(x, p):
    return pow(x, -1, p)


class Ed25519Curve:
    def __init__(self):
        self.p = pow(2, 255) - 19
        self.a = -1
        self.d = -(121665 * inv(121666, self.p)) % self.p
        self.b = 256
        self.O = Point(0, 1, self)
        self.G = Point.decompress((4 * inv(5, self.p)) % self.p, self)
        self.ord_G = 2**252 + 27742317777372353535851937790883648493
        self.ord_EC = 2**3 * self.ord_G

    def point(self, x, y):
        return Point(x, y, self)

    def randpoint(self):  # name following secrets.randbits
        found = False
        while not found:
            try:
                P = Point.decompress(secrets.randbits(self.b), self)
                found = True
            except:
                pass
        return P


class Point:
    def __init__(self, x, y, EC):
        self.x = x
        self.y = y
        self.EC = EC
        if not Point.validate(self):
            raise Exception(f"Provided coordinates {self} don't form a point on that curve")

    def __neg__(self):
        x, y, p = self.x, self.y, self.EC.p
        if x == 0 and y == 1:
            return self
        return Point((-x) % p, y, self.EC)

    def __add__(self, other):
        x1, y1, a, d, p = self.x, self.y, self.EC.a, self.EC.d, self.EC.p
        x2, y2 = other.x, other.y
        if self.EC != other.EC: raise Exception('You cannot add points on different curves')
        s = (d * x1 * x2 * y1 * y2) % p
        x = ((x1 * y2 + y1 * x2) * inv(1 + s, p)) % p
        y = ((y1 * y2 - a * x1 * x2) * inv(1 - s, p)) % p
        return Point(x, y, self.EC)

    def __rmul__(self, other):
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
        return ((a*x**2+y**2-1-d*x**2*y**2) % p == 0 and
                (0 <= x < p) and (0 <= y < p))

    def compress(self):
        y_bin = bin(self.y)[2:].zfill(self.EC.b)
        if self.x & 1 == 1:
            new_y = '1' + y_bin[1:]
        else:
            new_y = '0' + y_bin[1:]
        return int(new_y, 2)  # .to_bytes(int(log2(b)), byteorder='little')

    @staticmethod
    def decompress(compressed_point, EC):
        # y = int.from_bytes(compressed_point, byteorder='little')
        p, d, b = EC.p, EC.d, EC.b
        y_msb = int(bin(compressed_point)[2:].zfill(b)[0])
        y = int('0' + bin(compressed_point)[2:].zfill(b)[1:], 2)
        u = (y**2-1) % p
        v = ((d*y**2)+1) % p
        z = ((u*v**3)*pow((u*v**7), ((p-5)*inv(8,p))%p, p)) % p
        vz2 = (v*z**2) % p
        if vz2 == u:
            x = z
        elif vz2 == -u % p:
            x = (z*pow(2, ((p-1)*inv(4,p))%p, p)) % p
        else:
            raise Exception('Error in decompression formulas')
        if y_msb != x & 1:
            x = -x % p
        return EC.point(x, y)


# Monero uses different implementation of Keccak and encodings
# for simplicity I convert to strings and concatenate all arguments to hash functions
# I want to focus on signature schemes and keep stuff related to hashing and encoding as simple as possible, so
from hashlib import sha3_256

EC = Ed25519Curve()

def H(*args):
    m = ''.join([str(arg) for arg in args]).encode('utf-8')
    return int(sha3_256(m).hexdigest(), 16)

def H_n(*args):
    return H(*args) % EC.ord_G

def H_p(*args):
    # this funciton is used for testing in mininero, its more secure than H_n(*args) * EC.G but it's not efficient
    n = H_n(*args)
    found = False
    while not found:
        try:
            P = Point.decompress(n, EC)
            found = True
        except:
            n = H_n(n)
    return 8 * P  # note that it hashes to point from group generated by Ed25519 curve basepoint

""" Other ways of Hashing directly to point
def H_p(*args):
    # insecure way of hashing to point, for illustration only
    return H_n(*args) * EC.G

for more accurate reference how it's implemented in monero, check out hashToPointCN() function from mininero
https://github.com/monero-project/mininero/blob/master/mininero.py#L238
and
https://www.getmonero.org/resources/research-lab/pubs/ge_fromfe.pdf
"""
