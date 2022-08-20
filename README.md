
# monero-ring-signatures

This project contains Python implementations of elliptic curves and signature protocols used in Monero cryptocurrency described in <a href="https://www.getmonero.org/library/Zero-to-Monero-2-0-0.pdf">Zero to Monero: Second Edition</a>.

The main point is to visualise signatures and ZKP protocols with simple, commented, and executable code similar to mathematical notation.

Implemented using Python 3.8.10 \
It has no external dependencies, therefore you can just run any file with:

```
git clone https://github.com/kamsec/monero-ring-signatures.git
python signatures/12_clsag_signature_min.py
```

## Contents
```
+---elliptic_curves
|       1_ec_short_weierstrass.py
|       2_ec_twisted_edwards.py
|       2b_params_validation.py
|       3_tw_ed_compressed.py
|       4_ed25519_params.py
|       5_ed25519.py
|
\---signatures
        1_schnorr_interactive.py
        2_schnorr_non_interactive.py
        3_schnorr_signature.py
        4_eddsa.py
        5_multi_base_proof.py
        6_multi_key_proof.py
        7_sag_signature.py
        8_lsag_signature.py
        9_blsag_signature.py
        10_mlsag_signature.py
        11_clsag_signature.py
        12_clsag_signature_min.py
        ed25519.py
```
## Description
### `elliptic_curves/`
- `1_ec_short_weierstrass.py` - first implementation of elliptic curves in short Weierstrass form, with small parameters, functions for finding points and subgroups, and tests of arithmetic

- `2_ec_twisted_edwards.py` - second implementation, the same as first but for twisted Edwards curves

- `2b_params_validation.py` - functions for finding parameters that result in curves with complete addition formulas (so implementation of exceptional cases, as in curves in short Weierstrass form is not needed)

- `3_tw_ed_compressed` - added compression and decompression functions

- `4_ed25519_params.py` - added hardcoded Ed25519 curve parameters, the same curve used in Monero

- `5_ed25519.py` - added hash functions, removed tests and refactored the code. This script is used in `signatures/` folder as `ed25519.py`

### `signatures/`
This folder contains ZKP and signature protocols mentioned in Chapter 2 and 3 of Zero to Monero: Second Edition. The last two files contain implementation of Concise Linkable Spontaneous Anonymous Group signature protocol used currently in monero.

- `11_clsag_signature.py` - annotated version of CLSAG signatures

- `12_clsag_signature_min.py` - minified version

## Notes
- Monero uses different implementation of Keccak hash function and encodings. Here, for simplicity, all arguments to hash functions are converted to strings and concatenated  instead of using bytes. The point is to focus on signature protocols and keep stuff related to hashing and encoding as simple as possible.

- In this implementation of CLSAG and other group signature protocols, there's set of public keys K ("ring") included in signer output and passed to verifier as part of  input. In Monero, instead of sending set of public keys, transaction contains just set of integer offsets that point to public keys existing on blockchain.
