# Back's Linkable Spontaneous Anonymous Group signatures

import secrets
from ed25519 import EC, H_n, H_p

# SET PARAMS
b, G, ord_G = EC.b, EC.G, EC.ord_G
d = 5  # number of ring members

# INIT Other Public Keys
k = [secrets.randbelow(ord_G) for _ in range(d - 1)]
K = [k[i] * G for i in range(d - 1)]

# INIT PROVER
k_pi = secrets.randbelow(ord_G)
K_pi = k_pi * G

def sign(m, k_pi, K_pi, G, K):
    print('Signer (m, k_pi, K_pi, G, K)')
    pi = secrets.randbelow(d)

    print('pi', pi)
    K.insert(pi, K_pi)

    K_tilde = k_pi * H_p(K_pi)

    a = secrets.randbelow(ord_G)
    r = [None] * d
    for i in range(d):
        if i != pi:
            r[i] = secrets.randbelow(ord_G)
    print('r', r)

    c = [None] * d
    c[(pi + 1) % d] = H_n(m, a * G, a * H_p(K_pi))
    print('c', c)

    indexes = [(pi + i) % d for i in range(1, d)]
    print('indexes', indexes)

    for i in indexes:
        c[(i + 1) % d] = H_n(m, r[i] * G + c[i] * K[i], r[i] * H_p(K[i]) + c[i] * K_tilde)
        print(f'c_{(i + 1) % d} {c[(i + 1) % d]}')
    print('c', c)

    r[pi] = (a - c[pi] * k_pi) % ord_G
    print('r', r)
    return (c[0], r, K_tilde, K)

def verify(m, c_0, r, K_tilde, K):
    print('Verifier (m, c_0, r, K_tilde, K)')
    if ord_G * K_tilde != EC.O:
        raise Exception('ord_G * K_tilde != EC.O')
    c_prim = [None] * d
    c_prim[0] = c_0
    for i in range(d):
        c_prim[(i + 1) % d] = H_n(m, r[i] * G + c_prim[i] * K[i], r[i] * H_p(K[i]) + c_prim[i] * K_tilde)
        print(f'c_prim_{(i + 1) % d} {c_prim[(i + 1) % d]}')
    return c_0 == c_prim[0]

m = 'message'
sig = sign(m, k_pi, K_pi, G, K)
is_valid = verify(m, *sig)
print('Accepted?', is_valid)
