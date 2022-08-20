# Spontaneous Anonymous Group signature algorithm

import secrets
from ed25519 import EC, H_n

# SET PARAMS
b, G, ord_G = EC.b, EC.G, EC.ord_G
d = 5  # number of ring members

# INIT Other Public Keys
k = [secrets.randbelow(ord_G) for _ in range(d - 1)]
K = [k[i] * G for i in range(d - 1)]

# INIT PROVER
k_pi = secrets.randbelow(ord_G)

def sign(m, k_pi, G, K):
    print('Signer (m, k_pi, G, K)')
    pi = secrets.randbelow(d)
    print('pi', pi)
    K.insert(pi, k_pi * G)

    a = secrets.randbelow(ord_G)
    r = [None] * d
    for i in range(d):
        if i != pi:
            r[i] = secrets.randbelow(ord_G)
    print('r', r)

    c = [None] * d
    c[(pi + 1) % d] = H_n(K, m, a * G)
    print('c', c)

    indexes = [(pi + i) % d for i in range(1, d)]
    print('indexes', indexes)

    for i in indexes:
        c[(i + 1) % d] = H_n(K, m, r[i] * G + c[i] * K[i])
        print(f'c_{(i + 1) % d} {c[(i + 1) % d]}')
    print('c', c)

    r[pi] = (a - c[pi] * k_pi) % ord_G
    print('r', r)
    return (c[0], r, K)

def verify(m, c_0, r, K):
    print('\nVerifier (m, c_0, r, K)')
    c_prim = [None] * d
    c_prim[0] = c_0
    print('c_prim', c_prim)
    for i in range(d):
        # when i=d-1 then (i+1)%d=0 so c_prim[0] is overwritten and it's the last result
        c_prim[(i + 1) % d] = H_n(K, m, r[i] * G + c_prim[i] * K[i])
        print(f'c_prim_{(i + 1) % d} {c_prim[(i + 1) % d]}')
    return c_0 == c_prim[0]

m = 'message'
sig = sign(m, k_pi, G, K)
is_valid = verify(m, *sig)
print('Accepted?', is_valid)
