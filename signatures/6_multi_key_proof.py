# Proof of knowledge of multiple discrete logarithms in single proof

import secrets
from ed25519 import EC, H_n

# SET PARAMS
b, ord_G = EC.b, EC.ord_G
d = 5  # number of private keys and bases

# INIT PROVER
k = [secrets.randbelow(ord_G) for _ in range(d)]

G = [8 * EC.randpoint() for _ in range(d)]
K = [k[i] * G[i] for i in range(d)]

def prove(k, G, K):
    a = [secrets.randbelow(ord_G) for _ in range(d)]
    A = [a[i] * G[i] for i in range(d)]
    c = H_n(G, K, A)
    r = [(a[i] - c * k[i]) % ord_G for i in range(d)]
    return (c, r)

def verify(G, K, c, r):
    c_prim = H_n(G, K, [r[i] * G[i] + c * K[i] for i in range(d)])
    return c == c_prim

proof = prove(k, G, K)
is_valid = verify(G, K, *proof)
print('is_valid', is_valid)
