#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-5.py — Mass formula terms

For (n,p) = (3,5): X = n*p*(p-1) = 60.
Computes each term of M = X^2/2 + (n/p)*X + n^2/X + lambda/n
using exact Fraction arithmetic. Verifies M = 853811/465 and
that denominator 465 = 3 * 5 * 31.
"""

from fractions import Fraction

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-5: Mass formula terms")
print("=" * 72)

results = []

# ============================================================================
# PARAMETERS (exact rational)
# ============================================================================
n = Fraction(3)
p = Fraction(5)
Gamma = p**2              # 25
lam = Fraction(1, int(p**3 - 1))  # 1/124
X = n * p * (p - 1)       # 3 * 5 * 4 = 60

print(f"\nParameters:")
print(f"  n = {n}")
print(f"  p = {p}")
print(f"  Gamma = p^2 = {Gamma}")
print(f"  lambda = 1/(p^3-1) = 1/{int(p**3-1)} = {lam}")
print(f"  X = n*p*(p-1) = {n}*{p}*{p-1} = {X}")

ok_X = (X == Fraction(60))
results.append(("X = 60", ok_X))
print(f"  X = 60: {'PASS' if ok_X else 'FAIL'}")

# ============================================================================
# SECTION 1: Compute each term individually
# ============================================================================
print("\n--- SECTION 1: Individual mass formula terms ---")
print("M = X^2/2 + (n/p)*X + n^2/X + lambda/n")
print()

term1 = X**2 / 2
term2 = (n / p) * X
term3 = n**2 / X
term4 = lam / n

print(f"  Term 1: X^2/2     = {X}^2/2 = {X**2}/2 = {term1}")
print(f"                    = {float(term1):.6f}")

print(f"  Term 2: (n/p)*X   = ({n}/{p})*{X} = {term2}")
print(f"                    = {float(term2):.6f}")

print(f"  Term 3: n^2/X     = {n}^2/{X} = {n**2}/{X} = {term3}")
print(f"                    = {float(term3):.6f}")

print(f"  Term 4: lambda/n  = (1/{int(p**3-1)})/{n} = {term4}")
print(f"                    = {float(term4):.10f}")

# Verify individual term values
ok_t1 = (term1 == Fraction(1800))
ok_t2 = (term2 == Fraction(36))
ok_t3 = (term3 == Fraction(9, 60))
ok_t3b = (term3 == Fraction(3, 20))
ok_t4 = (term4 == Fraction(1, 372))

results.append(("X^2/2 = 1800", ok_t1))
results.append(("(n/p)*X = 36", ok_t2))
results.append(("n^2/X = 9/60 = 3/20", ok_t3 and ok_t3b))
results.append(("lambda/n = 1/372", ok_t4))

print(f"\n  X^2/2 = 1800: {'PASS' if ok_t1 else 'FAIL'}")
print(f"  (n/p)*X = 36: {'PASS' if ok_t2 else 'FAIL'}")
print(f"  n^2/X = 9/60 = 3/20 = 0.15: {'PASS' if ok_t3 and ok_t3b else 'FAIL'}")
print(f"    9/60 reduces to {term3} (= {float(term3)})")
print(f"  lambda/n = 1/372: {'PASS' if ok_t4 else 'FAIL'}")

# ============================================================================
# SECTION 2: Sum all terms -> M
# ============================================================================
print("\n--- SECTION 2: Total mass formula ---")

M = term1 + term2 + term3 + term4
print(f"  M = {term1} + {term2} + {term3} + {term4}")
print(f"  M = {M}")
print(f"  M = {M.numerator}/{M.denominator}")
print(f"  M = {float(M):.12f}")

ok_M = (M == Fraction(853811, 465))
results.append(("M = 853811/465", ok_M))
print(f"  M = 853811/465: {'PASS' if ok_M else 'FAIL'}")

# ============================================================================
# SECTION 3: Verify denominator factorization
# ============================================================================
print("\n--- SECTION 3: Denominator factorization ---")

denom = M.denominator
print(f"  Denominator = {denom}")

# Factorize
def factorize(n_val):
    factors = {}
    d = 2
    while d * d <= n_val:
        while n_val % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n_val //= d
        d += 1
    if n_val > 1:
        factors[n_val] = factors.get(n_val, 0) + 1
    return factors

factors = factorize(denom)
factor_str = " * ".join(f"{p_f}^{e}" if e > 1 else str(p_f) for p_f, e in sorted(factors.items()))
print(f"  {denom} = {factor_str}")
print(f"  Prime factors: {sorted(factors.keys())}")

ok_denom = (denom == 465)
ok_factors = (sorted(factors.keys()) == [3, 5, 31])

results.append(("Denominator = 465", ok_denom))
results.append(("465 = 3 * 5 * 31", ok_factors))

print(f"  Denominator = 465: {'PASS' if ok_denom else 'FAIL'}")
print(f"  465 = 3 * 5 * 31: {'PASS' if ok_factors else 'FAIL'}")

# Identify with n, p, Phi_3(p)
Phi3 = int(p**2 + p + 1)  # p^2 + p + 1 = 31
print(f"\n  n = {int(n)}")
print(f"  p = {int(p)}")
print(f"  Phi_3(p) = p^2 + p + 1 = {Phi3}")
print(f"  n * p * Phi_3(p) = {int(n)} * {int(p)} * {Phi3} = {int(n)*int(p)*Phi3}")

ok_nphi = (int(n) * int(p) * Phi3 == 465)
results.append(("465 = n * p * Phi_3(p) = 3 * 5 * 31", ok_nphi))
print(f"  {'PASS' if ok_nphi else 'FAIL'}")

# ============================================================================
# SECTION 4: Decomposition summary
# ============================================================================
print("\n--- SECTION 4: Term decomposition summary ---")
print()
print(f"  | Term       | Expression | Fraction | Decimal        | % of M  |")
print(f"  |------------|------------|----------|----------------|---------|")
for label, expr, val in [
    ("X^2/2",     "1800",    term1),
    ("(n/p)*X",   "36",      term2),
    ("n^2/X",     "3/20",    term3),
    ("lambda/n",  "1/372",   term4),
]:
    pct = float(val) / float(M) * 100
    print(f"  | {label:>10} | {expr:>10} | {str(val):>8} | {float(val):>14.10f} | {pct:>6.3f}% |")

print(f"  |------------|------------|----------|----------------|---------|")
print(f"  | {'TOTAL':>10} | {'':>10} | {str(M):>8} | {float(M):>14.10f} | 100.000%|")

# ============================================================================
# SECTION 5: Verify the step-by-step algebra
# ============================================================================
print("\n--- SECTION 5: Step-by-step common denominator ---")

# term1 = 1800/1, term2 = 36/1, term3 = 3/20, term4 = 1/372
# LCD of 1, 1, 20, 372
# 372 = 4 * 93 = 4 * 3 * 31 = 2^2 * 3 * 31
# 20 = 2^2 * 5
# LCD = 2^2 * 3 * 5 * 31 = 4 * 465 = 1860
# Wait: 465 = 3 * 5 * 31
# LCD(1, 1, 20, 372) = LCD(20, 372)
# 20 = 2^2 * 5
# 372 = 2^2 * 3 * 31
# LCD = 2^2 * 3 * 5 * 31 = 1860

from math import gcd
def lcm(a, b):
    return a * b // gcd(a, b)

lcd = lcm(lcm(term1.denominator, term2.denominator),
          lcm(term3.denominator, term4.denominator))
print(f"  LCD({term1.denominator}, {term2.denominator}, {term3.denominator}, {term4.denominator}) = {lcd}")
print(f"  But M reduces to {M.numerator}/{M.denominator} after GCD cancellation")
print(f"  GCD({M.numerator * (lcd // M.denominator)}, {lcd}) = {lcd // M.denominator}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 72)
print("SUMMARY")
print("=" * 72)
for desc, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")
passed = sum(1 for _, ok in results if ok)
total = len(results)
print(f"\n  {passed}/{total} checks passed.")
if passed == total:
    print("  ALL CHECKS PASSED.")
else:
    print(f"  WARNING: {total - passed} check(s) FAILED.")
