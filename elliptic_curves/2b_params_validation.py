
# Implementation of functions for checking (large numbers) and finding (small numbers) parameters of twisted edwards curves
# such that addition formulas are COMPLETE - so there is no need implementing arithmetic for exceptional cases
# https://datatracker.ietf.org/doc/html/rfc8032


def twisted_ed_params_validator(a, d, p):
    # print('Function for validating a, d, p params')
    a, d, p = -1, 2, 13
    # p has to be prime ofc - check with online tools
    square_roots = {x**2 % p for x in range(0, p)}
    a_div_d = (a * pow(d, -1, p)) % p
    # print(f'square_roots={square_roots}')
    # print(f'd={d}')
    # print(f'a/d={a_div_d}')
    if (d in square_roots):
        raise Exception(f"d={d} is in square_roots. Addition formulas wouldn't be complete - Find other parameters")
    if (a_div_d in square_roots):
        raise Exception(f"a/d={a_div_d} in square_roots. Addition formulas wouldn't be complete - Find other parameters")
    # print('params ok')
    return True


def twisted_ed_params_complete_finder():
    print('Function for finding sets of parameters that result in complete addition formulas (without exceptional cases)')
    p = 13  # for p=13, square_roots={0, 1, 3, 4, 9, 10, 12}
    a = -1
    for d in range(p):
        try:
            twisted_ed_params_validator(a, d, p)
            print(f'Success! p={p} a={a} d={d}') # parameters for which formulas are complete
        except:
            pass
    # Success! p=13 a=-1 d=2
twisted_ed_params_complete_finder()


def check_ed25519():
    print('Function for checking if real ed25519 curve parameters make addition formulas complete')
    p = 2**255 - 19  # 57896044618658097711785492504343953926634992332820282019728792003956564819949
    a = -1
    d = (121665 * pow(121666, -1, p)) % p  # 20800338683988658368647408995589388737092878452977063003340006470870624536394
    # p, a, d = 13, -1, 2
    print(p, '=p')
    # Legrende symbol (d/p)
    ls1 = pow(d, ((p - 1) * pow(2, -1, p)) % p, p)
    # ls1 = pow(d, int((p - 1) / 2) , p)  # this doesnt work idk if math reason or python
    print(ls1, '=d') # should be -1 - then basic formulas are COMPLETE
    # Legrende symbol ((a/d)/p)
    ls2 = pow((a * pow(d, -1, p)) % p, ((p - 1) * pow(2, -1, p)) % p, p)
    # ls2 = pow((a * pow(d, -1, p)) % p, int((p - 1) / 2), p)
    print(ls2, '=a/d') # should be -1 - then basic formulas are COMPLETE

    # 57896044618658097711785492504343953926634992332820282019728792003956564819949 =p
    # 57896044618658097711785492504343953926634992332820282019728792003956564819948 =d
    # 57896044618658097711785492504343953926634992332820282019728792003956564819948 =a/d
    print(ls1 == -1 % p)
    print(ls2 == -1 % p)
    # d and a/d are equal -1 mod p, so formulas are complete!
check_ed25519()
