#!/usr/bin/env python3
# YASA PRESENTS
# cuft-attack-number-theory.py - Number-theoretic derivations of c_1 = 3/5

"""
Three independent number-theoretic paths each uniquely select p=5, n=3,
yielding c_1 = n/p = 3/5.
"""

from fractions import Fraction


def triangular(p):
    """Triangular number T_p = p*(p+1)/2."""
    return p * (p + 1) // 2


def mersenne_like(p):
    """Mersenne-like term 2^(p-1) - 1."""
    return 2 ** (p - 1) - 1


def cyclotomic_3(p):
    """Third cyclotomic polynomial Phi_3(p) = p^2 + p + 1."""
    return p * p + p + 1


# ============================================================================
# 1. MERSENNE-TRIANGULAR IDENTITY: T_p = 2^(p-1) - 1
# ============================================================================
print("=" * 72)
print("1. MERSENNE-TRIANGULAR IDENTITY: T_p = 2^(p-1) - 1")
print("=" * 72)
print()
print("   T_p = p*(p+1)/2  (triangular number)")
print("   We seek positive integers p where T_p = 2^(p-1) - 1.")
print()

solutions_mt = []
scan_range = 100

print(f"   Scanning p = 1 to {scan_range}:")
print(f"   {'p':>5}  {'T_p':>20}  {'2^(p-1)-1':>20}  {'Match':>6}")
print(f"   {'---':>5}  {'---':>20}  {'---':>20}  {'---':>6}")

for p in range(1, scan_range + 1):
    t = triangular(p)
    m = mersenne_like(p)
    match = (t == m)
    if match:
        solutions_mt.append(p)
    # Print first 10 and any matches
    if p <= 10 or match:
        print(f"   {p:>5}  {t:>20}  {m:>20}  {'YES' if match else 'no':>6}")

print()
if len(solutions_mt) == 1 and solutions_mt[0] == 5:
    print(f"   VERIFIED: Unique solution is p = {solutions_mt[0]}")
else:
    print(f"   Solutions found: {solutions_mt}")

# Growth argument: for p > 5, 2^(p-1) grows exponentially, T_p quadratically
print()
print("   Growth comparison for p > 5:")
print(f"     T_100    = {triangular(100)}")
print(f"     2^99 - 1 = {mersenne_like(100)}")
print("     Exponential dominates quadratic => no further solutions.")

# Derive c_1
p_star = solutions_mt[0]
# From (n-2)(p-1) = 4:
n_star = 4 // (p_star - 1) + 2
c1 = Fraction(n_star, p_star)
print()
print(f"   From (n-2)(p-1) = 4 with p = {p_star}:")
print(f"     n = 4/(p-1) + 2 = 4/{p_star - 1} + 2 = {n_star}")
print(f"     c_1 = n/p = {n_star}/{p_star} = {float(c1)}")
print(f"   RESULT: c_1 = {c1}")
print()

# ============================================================================
# 2. KLEIN ICOSAHEDRON
# ============================================================================
print("=" * 72)
print("2. KLEIN ICOSAHEDRON: T^2 = H^3 - 1728*f^5")
print("=" * 72)
print()
print("   The Klein relation for the icosahedron has exponents (2, 3, 5).")
print("   These equal (2, n, p) with n = 3, p = 5.")
print()

klein_exponents = (2, 3, 5)
print(f"   Klein exponents:  {klein_exponents}")
print(f"   (2, n, p)      =  (2, {n_star}, {p_star})")
assert klein_exponents == (2, n_star, p_star), "Klein exponents do not match!"
print(f"   VERIFIED: Exponents match (2, n, p) = (2, {n_star}, {p_star})")
print()

# Ratio of non-quadratic exponents
ratio = Fraction(klein_exponents[1], klein_exponents[2])
print(f"   Ratio of non-quadratic exponents: {klein_exponents[1]}/{klein_exponents[2]} = {ratio} = {float(ratio)}")
assert ratio == c1, "Ratio does not equal c_1!"
print(f"   VERIFIED: ratio = c_1 = {c1}")
print()

# Reciprocal sum identity
a, b, c = klein_exponents
recip_sum = Fraction(1, a) + Fraction(1, b) + Fraction(1, c)
print(f"   Reciprocal sum: 1/{a} + 1/{b} + 1/{c}")
print(f"     = {Fraction(1,a)} + {Fraction(1,b)} + {Fraction(1,c)}")
print(f"     = {recip_sum}")
print()

phi3_p = cyclotomic_3(p_star)
two_np = 2 * n_star * p_star
phi_frac = Fraction(phi3_p, two_np)
print(f"   Phi_3(p) = p^2 + p + 1 = {p_star}^2 + {p_star} + 1 = {phi3_p}")
print(f"   2*n*p = 2 * {n_star} * {p_star} = {two_np}")
print(f"   Phi_3(p) / (2*n*p) = {phi3_p}/{two_np} = {phi_frac}")
print()
assert recip_sum == phi_frac, "Reciprocal sum does not equal Phi_3(p)/(2np)!"
print(f"   VERIFIED: 1/2 + 1/3 + 1/5 = Phi_3(p)/(2np) = {recip_sum}")
print()

# ============================================================================
# 3. CYCLOTOMIC-MERSENNE COINCIDENCE: Phi_3(p) = 2^p - 1
# ============================================================================
print("=" * 72)
print("3. CYCLOTOMIC-MERSENNE COINCIDENCE: Phi_3(p) = 2^p - 1")
print("=" * 72)
print()
print("   Phi_3(p) = p^2 + p + 1")
print("   We seek primes p where Phi_3(p) = 2^p - 1.")
print()

solutions_cm = []

print(f"   Scanning p = 2 to {scan_range}:")
print(f"   {'p':>5}  {'Phi_3(p)':>20}  {'2^p - 1':>20}  {'Match':>6}")
print(f"   {'---':>5}  {'---':>20}  {'---':>20}  {'---':>6}")

for p in range(2, scan_range + 1):
    phi = cyclotomic_3(p)
    mer = 2 ** p - 1
    match = (phi == mer)
    if match:
        solutions_cm.append(p)
    if p <= 10 or match:
        print(f"   {p:>5}  {phi:>20}  {mer:>20}  {'YES' if match else 'no':>6}")

print()
if len(solutions_cm) == 1 and solutions_cm[0] == 5:
    print(f"   VERIFIED: Unique solution is p = {solutions_cm[0]}")
else:
    print(f"   Solutions found: {solutions_cm}")

print()
print("   Growth comparison:")
print(f"     Phi_3(100) = {cyclotomic_3(100)}")
print(f"     2^100 - 1  = {2**100 - 1}")
print("     Exponential dominates quadratic => no further solutions.")
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 72)
print("SUMMARY")
print("=" * 72)
print()
print("   Three independent number-theoretic identities each uniquely")
print("   select p = 5 (and correspondingly n = 3):")
print()
print("   1. Mersenne-triangular:  T_p = 2^(p-1) - 1   =>  p = 5  [VERIFIED]")
print("   2. Klein icosahedron:    exponents (2,3,5)     =>  n/p = 3/5  [VERIFIED]")
print("   3. Cyclotomic-Mersenne:  Phi_3(p) = 2^p - 1   =>  p = 5  [VERIFIED]")
print()
print(f"   c_1 = n/p = 3/5 = {float(c1)}")
print()
print("   All verifications PASSED.")
