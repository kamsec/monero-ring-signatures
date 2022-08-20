# Concise Linkable Spontaneous Anonymous Group signatures
# minified version

# I tried to find the compromise between following three ideas
# - use as simple python syntax as possible
# - use as close to mathematical notation syntax as possible (extensive use of list comprehensions)
# - stay as close to zero-to-monero paper as possible

import secrets
from ed25519 import EC, H_n, H_p

# SET PARAMS
b, G, ord_G = EC.b, EC.G, EC.ord_G
n, m = 5, 6
# n = number of ring members
# m = number of private keys per ring member

# INIT Other Public Keys
k = [[secrets.randbelow(ord_G) for _ in range(m)] for _ in range (n - 1)]
K = [[k[i][j] * G for j in range(m)] for i in range(n - 1)]

# INIT PROVER
k_pi = [secrets.randbelow(ord_G) for _ in range(m)]
K_pi = [k_pi[j] * G for j in range(m)]


def sign(msg, k_pi, K_pi, G, K):
    pi = secrets.randbelow(n)
    K.insert(pi, K_pi)
    K_tilde = [k_pi[j] * H_p(K[pi][0]) for j in range(m)]
    a = secrets.randbelow(ord_G)
    r = [secrets.randbelow(ord_G) if i != pi else None for i in range(n)]

    W = [sum([H_n([f'CLSAG_{j}'] + K + K_tilde) * K[i][j] for j in range(m)], start=EC.O) for i in range(n)]
    W_tilde = sum([H_n([f'CLSAG_{j}'] + K + K_tilde) * K_tilde[j] for j in range(m)], start=EC.O)
    w_pi = sum([H_n([f'CLSAG_{j}'] + K + K_tilde) * k_pi[j] for j in range(m)])

    c = [H_n(f'CLSAG_c', K, msg, a * G, a * H_p(K[pi][0])) if i == (pi + 1) % n else None for i in range(n)]
    for i in [(pi + i) % n for i in range(1, n)]:
        c[(i + 1) % n] = H_n(f'CLSAG_c', K, msg, r[i] * G + c[i] * W[i], r[i] * H_p(K[i][0]) + c[i] * W_tilde)

    r[pi] = (a - c[pi] * w_pi) % ord_G
    return (c[0], r, K_tilde, K)

def verify(msg, c_0, r, K_tilde, K):
    for j in range(m):
        if ord_G * K_tilde[j] != EC.O: raise Exception('ord_G * K_tilde[j] != EC.O')

    W = [sum([H_n([f'CLSAG_{j}'] + K + K_tilde) * K[i][j] for j in range(m)], start=EC.O) for i in range(n)]

    W_tilde = sum([H_n([f'CLSAG_{j}'] + K + K_tilde) * K_tilde[j] for j in range(m)], start=EC.O)

    c_prim = [None] * n
    c_prim[0] = c_0

    for i in range(n):
        c_prim[(i + 1) % n] = H_n(f'CLSAG_c', K, msg, r[i] * G + c_prim[i] * W[i], r[i] * H_p(K[i][0]) + c_prim[i] * W_tilde)
    return c_0 == c_prim[0]

msg = 'message'
sig = sign(msg, k_pi, K_pi, G, K)
is_valid = verify(msg, *sig)
print('Accepted?', is_valid)
