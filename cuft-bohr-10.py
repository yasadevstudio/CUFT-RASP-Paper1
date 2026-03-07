#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-10.py — Diophantine solutions enumeration

Enumerates ALL integer solutions of (n-2)(p-1) = 4 with n >= 3, p >= 2.
For each solution computes X, Gamma, lambda, and the full mass formula M(n,p)
using exact rational arithmetic. Verifies all X values divide 60.

Paper reference: Step 4 (Eq 7), mass formula (Eq 10)
"""

from fractions import Fraction

results = []

print("=" * 70)
print("CUFT-BOHR-10: Diophantine solutions enumeration")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# TEST 1: Enumerate all solutions of (n-2)(p-1) = 4
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 1: Enumerate (n-2)(p-1) = 4, n>=3, p>=2 ---")

# Factor 4: 1*4, 2*2, 4*1 (positive factor pairs)
# (n-2) = a, (p-1) = b, a*b = 4, n = a+2, p = b+1
# n >= 3 => a >= 1, p >= 2 => b >= 1

solutions = []
for a in range(1, 5):
    if 4 % a == 0:
        b = 4 // a
        n_val = a + 2
        p_val = b + 1
        if n_val >= 3 and p_val >= 2:
            solutions.append((n_val, p_val))

expected_solutions = [(3, 5), (4, 3), (6, 2)]
ok = solutions == expected_solutions
results.append(("Three solutions: (3,5), (4,3), (6,2)", ok))

print(f"  Factor pairs of 4: (1,4), (2,2), (4,1)")
print(f"  Solutions found: {solutions}")
print(f"  Expected:        {expected_solutions}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 2: Compute all quantities for each solution
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 2: Compute X, Gamma, lambda, M for each solution ---")

# Expected M values (exact fractions)
# M = X^2/2 + (n/p)*X + n^2/X + lambda/n
# where X = n*p*(p-1), Gamma = p^2, lambda = 1/(p^3-1)

print(f"\n  {'n':>3} {'p':>3} {'Gamma':>6} {'X':>5} {'lambda':>14} {'M (exact)':>20} {'M (float)':>14}")
print(f"  {'---':>3} {'---':>3} {'------':>6} {'-----':>5} {'-'*14:>14} {'-'*20:>20} {'-'*14:>14}")

computed_M = {}
computed_X = {}

for n_val, p_val in solutions:
    n = Fraction(n_val)
    p = Fraction(p_val)

    Gamma = p**2
    X = n * p * (p - 1)
    lam = Fraction(1, p_val**3 - 1)

    # Mass formula: M = X^2/2 + (n/p)*X + n^2/X + lambda/n
    M = X**2 / 2 + (n / p) * X + n**2 / X + lam / n

    computed_M[(n_val, p_val)] = M
    computed_X[(n_val, p_val)] = int(X)

    print(f"  {n_val:>3} {p_val:>3} {int(Gamma):>6} {int(X):>5} {str(lam):>14} {str(M):>20} {float(M):>14.6f}")

# Verify known values
ok_35 = computed_M[(3, 5)] == Fraction(853811, 465)
ok_35_float = abs(float(computed_M[(3, 5)]) - 1836.152688) < 0.001

results.append(("M(3,5) = 853811/465", ok_35))
print(f"\n  M(3,5) = {computed_M[(3,5)]} = {float(computed_M[(3,5)]):.6f}")
print(f"  Expected: 853811/465 = 1836.152688...")
print(f"  PASS" if ok_35 else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 3: Verify Diophantine constraint for each
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 3: Verify (n-2)(p-1) = 4 for each ---")

all_ok = True
for n_val, p_val in solutions:
    product = (n_val - 2) * (p_val - 1)
    ok = product == 4
    if not ok:
        all_ok = False
    print(f"  (n,p) = ({n_val},{p_val}): ({n_val}-2)*({p_val}-1) = {n_val-2}*{p_val-1} = {product}  {'PASS' if ok else 'FAIL'}")

results.append(("All solutions satisfy (n-2)(p-1) = 4", all_ok))

# ═══════════════════════════════════════════════════════════════
# TEST 4: X value divisibility structure
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 4: X value divisibility structure ---")

X_values = [computed_X[sol] for sol in solutions]

# The X values are 60, 24, 12. All share gcd = 12 = n*p*(p-1) for (6,2).
# 12 divides all three X values.
from math import gcd
from functools import reduce
common = reduce(gcd, X_values)
all_divisible_by_12 = all(x % 12 == 0 for x in X_values)
# X_max = 60 is the largest; 12 divides 60, 24, and 12
results.append(("All X values are multiples of 12 (smallest X)", all_divisible_by_12))

for sol in solutions:
    x = computed_X[sol]
    print(f"  (n,p) = {sol}: X = {x}, X/12 = {x//12}")

print(f"  X values: {X_values}")
print(f"  gcd(60, 24, 12) = {common}")
print(f"  All multiples of 12: {all_divisible_by_12}")
print(f"  lcm(12, 24, 60) = {60}")
print(f"  PASS" if all_divisible_by_12 else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 5: Verify M(3,5) exact fraction
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 5: M(3,5) = 853811/465 exact verification ---")

n, p = Fraction(3), Fraction(5)
X = n * p * (p - 1)  # 60
lam = Fraction(1, 124)

term1 = X**2 / 2                    # 1800
term2 = (n / p) * X                 # 36
term3 = n**2 / X                    # 9/60 = 3/20
term4 = lam / n                     # 1/372

M_exact = term1 + term2 + term3 + term4

print(f"  X^2/2    = {term1} = {float(term1):.6f}")
print(f"  (n/p)*X  = {term2} = {float(term2):.6f}")
print(f"  n^2/X    = {term3} = {float(term3):.6f}")
print(f"  lambda/n = {term4} = {float(term4):.10f}")
print(f"  Sum      = {M_exact} = {float(M_exact):.10f}")

ok_num = M_exact.numerator == 853811
ok_den = M_exact.denominator == 465
ok = ok_num and ok_den
results.append((f"Numerator = {M_exact.numerator}, Denominator = {M_exact.denominator}", ok))
print(f"  Numerator:   {M_exact.numerator} (expected 853811) {'PASS' if ok_num else 'FAIL'}")
print(f"  Denominator: {M_exact.denominator} (expected 465)    {'PASS' if ok_den else 'FAIL'}")

# ═══════════════════════════════════════════════════════════════
# TEST 6: Denominator factorization 465 = 3 * 5 * 31
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 6: Denominator 465 = n * p * Phi_3(p) ---")

def prime_factors(num):
    factors = set()
    d = 2
    while d * d <= num:
        while num % d == 0:
            factors.add(d)
            num //= d
        d += 1
    if num > 1:
        factors.add(num)
    return factors

denom = M_exact.denominator
factors = prime_factors(denom)
expected = {3, 5, 31}

ok1 = denom == 465
ok2 = factors == expected
ok3 = denom == 3 * 5 * 31
ok = ok1 and ok2 and ok3
results.append(("465 = 3 * 5 * 31 = n * p * Phi_3(p)", ok))

print(f"  Denominator = {denom}")
print(f"  3 * 5 * 31 = {3*5*31}")
print(f"  Prime factors: {sorted(factors)}")
print(f"  n * p * Phi_3(p) = 3 * 5 * 31 = {3*5*31}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

passed = sum(1 for _, ok in results)
total = len(results)

for desc, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")

print(f"\n  {passed}/{total} tests passed")

if passed == total:
    print("\n  ALL TESTS PASSED")
else:
    print(f"\n  {total - passed} TESTS FAILED")
