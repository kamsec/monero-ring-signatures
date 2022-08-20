# Concise Linkable Spontaneous Anonymous Group signatures

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

    K_tilde = [k_pi[j] * H_p(K[pi][0]) for j in range(m)]

    a = secrets.randbelow(ord_G)
    r = [None] * n

    for i in range(n):
        if i != pi:
            r[i] = secrets.randbelow(ord_G)
    print('r', r)

    W = []
    for i in range(n):
        to_sum = []
        for j in range(m):
            to_sum.append(H_n([f'CLSAG_{j}'] + K + K_tilde) * K[i][j])
        W.append(sum(to_sum, start=EC.O))  # start= is required by sum() to handle non ints

    to_sum = []
    for j in range(m):
        to_sum.append(H_n([f'CLSAG_{j}'] + K + K_tilde) * K_tilde[j])
    W_tilde = sum(to_sum, start=EC.O)
    w_pi = sum([H_n([f'CLSAG_{j}'] + K + K_tilde) * k_pi[j] for j in range(m)])

    c = [None] * n
    c[(pi + 1) % n] = H_n(f'CLSAG_c', K, msg, a * G, a * H_p(K[pi][0]))
    print('c', c)

    indexes = [(pi + i) % n for i in range(1, n)]
    print('indexes', indexes)

    for i in indexes:
        c[(i + 1) % n] = H_n(f'CLSAG_c', K, msg, r[i] * G + c[i] * W[i], r[i] * H_p(K[i][0]) + c[i] * W_tilde)
        print(f'c_{(i + 1) % n} {c[(i + 1) % n]}')

    r[pi] = (a - c[pi] * w_pi) % ord_G
    print('r', r)
    return (c[0], r, K_tilde, K)

# todo instead of K (as output, input), the input is the list offsets on blockchain to find public keys
def verify(msg, c_0, r, K_tilde, K):  # todo K passed or derived from K_tilde? m n lenghts should be derived as well!
    print('Verifier (msg, c_0, r, K_tilde, K)')
    for j in range(m):
        if ord_G * K_tilde[j] != EC.O:
            raise Exception('ord_G * K_tilde[j] != EC.O')

    W = []
    for i in range(n):
        to_sum = []
        for j in range(m):
            to_sum.append(H_n([f'CLSAG_{j}'] + K + K_tilde) * K[i][j])
        W.append(sum(to_sum, start=EC.O))  # start= is required by sum() to handle non ints

    to_sum = []
    for j in range(m):
        to_sum.append(H_n([f'CLSAG_{j}'] + K + K_tilde) * K_tilde[j])
    W_tilde = sum(to_sum, start=EC.O)

    c_prim = [None] * n
    c_prim[0] = c_0

    for i in range(n):
        c_prim[(i + 1) % n] = H_n(f'CLSAG_c', K, msg, r[i] * G + c_prim[i] * W[i], r[i] * H_p(K[i][0]) + c_prim[i] * W_tilde)
        print(f'c_prim_{(i + 1) % n} {c_prim[(i + 1) % n]}')
    return c_0 == c_prim[0]

msg = 'message'
sig = sign(msg, k_pi, K_pi, G, K)
is_valid = verify(msg, *sig)
print('Accepted?', is_valid)
