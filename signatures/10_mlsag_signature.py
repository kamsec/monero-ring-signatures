# Multilayer Linkable Spontaneous Anonymous Group signatures

import secrets
from ed25519 import EC, H_n, H_p

# SET PARAMS
b, G, ord_G = EC.b, EC.G, EC.ord_G
n, m = 5, 6
# n = number of ring members
# m = number of private keys per ring member

# INIT Other Public Keys
k = [[secrets.randbelow(ord_G) for _ in range(m)] for _ in range (n - 1)]
# [[k_1_1, ..., k_1_m]]
# [[ ... , ...,  ... ]]
# [[k_pi_1,...,k_pi_m]]
# [[ ... , ...,  ... ]]
# [[k_n_1, ..., k_n_m]]
K = [[k[i][j] * G for j in range(m)] for i in range(n - 1)]

# INIT PROVER
k_pi = [secrets.randbelow(ord_G) for _ in range(m)]
K_pi = [k_pi[j] * G for j in range(m)]


def sign(msg, k_pi, K_pi, G, K):
    print('Signer (msg, k_pi, K_pi, G, K)')
    pi = secrets.randbelow(n)

    print('pi', pi)
    K.insert(pi, K_pi)

    K_tilde = [k_pi[j] * H_p(K[pi][j]) for j in range(m)]

    a = [secrets.randbelow(ord_G) for _ in range(m)]
    r = [[None] * m for _ in range(n)]  # [[None] * m] * n won't work https://stackoverflow.com/questions/2739552/2d-list-has-weird-behavor-when-trying-to-modify-a-single-value

    for i in range(n):
        for j in range(m):
            if i != pi:
                r[i][j] = secrets.randbelow(ord_G)

    print('r', r)
    c = [None] * n
    to_hash = []
    for i in range(m):
        to_hash.extend([a[i] * G,  a[i] * H_p(K[pi][i])])
    c[(pi + 1) % n] = H_n(msg, *to_hash)
    print('c', c)

    indexes = [(pi + i) % n for i in range(1, n)]
    print('indexes', indexes)

    to_hash = []
    for i in indexes:
        to_hash = []
        for j in range(m):
            to_hash.extend([r[i][j] * G + c[i] * K[i][j],  r[i][j] * H_p(K[i][j]) + c[i] * K_tilde[j]])  # appends multiple elements to flat list
        c[(i + 1) % n] = H_n(msg, *to_hash)
        print(f'c_{(i + 1) % n} {c[(i + 1) % n]}')
    print('c', c)

    r[pi] = [(a[j] - c[pi] * k_pi[j]) % ord_G for j in range(m)]
    print('r', r)
    return (c[0], r, K_tilde, K)

def verify(msg, c_0, r, K_tilde, K):
    print('Verifier (msg, c_0, r, K_tilde, K)')
    for j in range(m):
        if ord_G * K_tilde[j] != EC.O:
            raise Exception('ord_G * K_tilde != EC.O')

    c_prim = [None] * n
    c_prim[0] = c_0

    for i in range(n):
        to_hash = []
        for j in range(m):
            to_hash.extend([r[i][j] * G + c_prim[i] * K[i][j],  r[i][j] * H_p(K[i][j]) + c_prim[i] * K_tilde[j]])
        c_prim[(i + 1) % n] = H_n(msg, *to_hash)
        print(f'c_prim_{(i + 1) % n} {c_prim[(i + 1) % n]}')
    return c_0 == c_prim[0]

msg = 'message'
sig = sign(msg, k_pi, K_pi, G, K)
is_valid = verify(msg, *sig)
print('Accepted?', is_valid)
