# Schnorr authentication protocol (interactive)
# aka Schnorr identification protocol (interactive)
# aka Schnorr zero knowledge proof (interactive)

from ed25519 import EC
import secrets

print('SET PARAMS')
[print(f'{k}={v}') for k, v in vars(EC).items()]
b, G, ord_G = EC.b, EC.G, EC.ord_G

print('\nINIT PROVER')
k = secrets.randbelow(ord_G);           print(f'k={k}')
K = k * G;                              print(f'K={K}')

print("\nSTART")
print('STEP 1 - Prover')
x = secrets.randbelow(ord_G);           print(f'x={x}')
X = x * G;                              print(f'X={X}')

print('\nSTEP 2 - Verifier')
c = secrets.randbelow(ord_G);           print(f'c={c}')

print('\nSTEP 3 - Prover')
r = (x + c * k) % ord_G;                print(f'r={r}')

print('\nSTEP 4 - Verifier')
R = r * G;                              print(f'R={R}')
R_prim = X + c * K;                     print(f'R_prim={R_prim}')
print('is_valid', R == R_prim)
