# Proof of knowledge of a discrete logarithm across multiple bases

import secrets
from ed25519 import EC, H_n

# SET PARAMS
# order of randomly selected point multiplied by 8 will be same as ord_G
b, ord_G = EC.b, EC.ord_G
d = 5  # number of base keys

# INIT PROVER
k = secrets.randbelow(ord_G)
G = [8 * EC.randpoint() for _ in range(d)]  # 8 * ensures they are in the same group
K = [k * G[i] for i in range(d)]

def prove(k, G, K):
    a = secrets.randbelow(b)
    A = [a * G[i] for i in range(d)]
    c = H_n(G, K, A)
    r = (a - c * k) % ord_G
    return (c, r)

def verify(G, K, c, r):
    c_prim = H_n(G, K, [r * G[i] + c * K[i] for i in range(d)])
    return c == c_prim

proof = prove(k, G, K)
is_valid = verify(G, K, *proof)
print('is_valid', is_valid)
