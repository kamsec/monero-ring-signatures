# Edwards-curve Digital Signature Algorithm

import secrets
from ed25519 import EC, H

# SET PARAMS
b, G, ord_G = EC.b, EC.G, EC.ord_G

# INIT SIGNER
k = secrets.randbelow(ord_G)
K = k * G

def sign(m, k, K):
    h_k = H(k)
    a = H(h_k, m)
    A = a * G
    c = H(A, K, m)
    r = (a + c * k) % ord_G
    return (A, r)

def verify(m, K, A, r):
    c_prim = H(A,K,m)
    return 2**3 * r * G == 2**3 * A + 2**3 * c_prim * K

m = 'message'
sig = sign(m, k, K)
is_valid = verify(m, K, *sig)
print('is_valid', is_valid)
