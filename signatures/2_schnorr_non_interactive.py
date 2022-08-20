# Schnorr authentication protocol (non-interactive)
# aka Schnorr identification protocol (non-interactive)
# aka Schnorr zero knowledge proof (non-interactive)

import secrets
from ed25519 import EC, H

print('SET PARAMS')
[print(f'{k}={v}') for k, v in vars(EC).items()]
b, G, ord_G = EC.b, EC.G, EC.ord_G

print('\nINIT PROVER')
k = secrets.randbelow(ord_G);           print(f'a={k}')
K = k * G;                              print(f'K={K}')

print("\nSTART")
def prove(k):
    print('\nprove(k)')
    a = secrets.randbelow(ord_G);       print(f'a={a}')
    A = a * G;                          print(f'A={A}')
    c = H(A);                           print(f'c={c}')
    r = (a + c * k) % ord_G;            print(f'r={r}')
    return (A, r)

def verify(K, A, r):
    print('\nverify(k)')
    c_prim = H(A);                      print(f'c_prim={c_prim}')
    R = r * G;                          print(f'R={R}')
    R_prim = A + c_prim * K;            print(f'R_prim={R_prim}')
    return R == R_prim

proof = prove(k)
is_valid = verify(K, *proof)
print('is_valid', is_valid)
