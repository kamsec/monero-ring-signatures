# Schnorr signature algorithm

import secrets
from ed25519 import EC, H

print('SET PARAMS')
[print(f'{k}={v}') for k, v in vars(EC).items()]
b, G, ord_G = EC.b, EC.G, EC.ord_G

print('\nINIT SIGNER')
k = secrets.randbelow(ord_G);           print(f'a={k}')
K = k * G;                              print(f'K={K}')

print("\nSTART")
def sign(m, k):
    print('\nsign(m, k)')
    a = secrets.randbelow(ord_G);       print(f'a={a}')
    A = a * G;                          print(f'A={A}')
    c = H(m, A);                        print(f'c={c}')
    r = (a - c * k) % ord_G;            print(f'r={r}')
    return (c, r)

def verify(m, K, c, r):
    print('\nverify(m, K, c, r)')
    c_prim = H(m, r * G + c * K);       print(f'c_prim={c_prim}')
    return c == c_prim

m = 'message'
sig = sign(m, k)
is_valid = verify(m, K, *sig)
print('is_valid', is_valid)
