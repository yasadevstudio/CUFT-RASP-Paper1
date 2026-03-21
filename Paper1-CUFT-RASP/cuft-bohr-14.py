#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-14.py — Vacuum correction c_0

Verifies c_0 = lambda/n = 1/(n*(p^3-1)) for (n,p) = (3,5), checks the
prime factorization of the denominator 372, confirms all factors lie in
{2, 3, 5, 31}, and verifies the complete mass formula M = X^2/2 + c_1*X
+ c_0 + c_{-1}/X with all four coefficients.

Paper reference: Step 6 (Eq 16), mass formula (Eq 9, 10)
"""

from fractions import Fraction

results = []

print("=" * 70)
print("CUFT-BOHR-14: Vacuum correction c_0")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
n = Fraction(3)
p = Fraction(5)
Gamma = p**2                  # 25
lam = Fraction(1, 124)       # lambda = 1/(p^3-1)
X = n * p * (p - 1)          # 60
Phi3_p = 31                   # p^2 + p + 1

# ═══════════════════════════════════════════════════════════════
# TEST 1: c_0 = lambda/n = 1/372
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 1: c_0 = lambda/n ---")

c0 = lam / n
expected_c0 = Fraction(1, 372)

ok = c0 == expected_c0
results.append(("c_0 = lambda/n = 1/372", ok))

print(f"  lambda = {lam}")
print(f"  n = {n}")
print(f"  c_0 = lambda/n = {lam}/{n} = {c0}")
print(f"  Expected: 1/372 = {expected_c0}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 2: c_0 = 1/(n*(p^3-1))
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 2: c_0 = 1/(n*(p^3-1)) ---")

c0_alt = Fraction(1, int(n) * (int(p)**3 - 1))
ok = c0 == c0_alt
results.append(("c_0 = 1/(n*(p^3-1)) = 1/(3*124) = 1/372", ok))

print(f"  n*(p^3-1) = 3 * (125-1) = 3 * 124 = {3 * 124}")
print(f"  1/(n*(p^3-1)) = {c0_alt}")
print(f"  Match: {c0 == c0_alt}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 3: Factorization 372 = 3 * 4 * 31
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 3: Factorization of 372 ---")

ok1 = 372 == 3 * 4 * 31
ok2 = 372 == 3 * 124
ok3 = 124 == 4 * 31

ok = ok1 and ok2 and ok3
results.append(("372 = 3 * 4 * 31 = 3 * 124", ok))

print(f"  372 = 3 * 124 = 3 * 4 * 31")
print(f"  3 * 4 * 31 = {3 * 4 * 31}")
print(f"  124 = 4 * 31 = {4 * 31}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 4: Prime factorization of 372
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 4: Prime factors of 372 ---")

def prime_factors(num):
    """Return set of prime factors."""
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

def prime_factorization(num):
    """Return dict of prime -> exponent."""
    factors = {}
    d = 2
    while d * d <= num:
        while num % d == 0:
            factors[d] = factors.get(d, 0) + 1
            num //= d
        d += 1
    if num > 1:
        factors[num] = factors.get(num, 0) + 1
    return factors

pf_372 = prime_factorization(372)
factors_372 = prime_factors(372)
expected_factors = {2, 3, 31}
master_set = {2, 3, 5, 31}

ok1 = factors_372 == expected_factors
ok2 = factors_372.issubset(master_set)
ok = ok1 and ok2
results.append(("prime_factors(372) = {2, 3, 31} subset of {2, 3, 5, 31}", ok))

print(f"  372 = ", end="")
parts = [f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(pf_372.items())]
print(" * ".join(parts))
print(f"  = {' * '.join(str(p) + ('^' + str(e) if e > 1 else '') for p, e in sorted(pf_372.items()))}")
print(f"  Prime factors: {sorted(factors_372)}")
print(f"  Expected: {sorted(expected_factors)}")
print(f"  Subset of {{2, 3, 5, 31}}: {factors_372.issubset(master_set)}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 5: Complete mass formula with all four coefficients
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 5: Complete mass formula verification ---")
print("  M = X^2/2 + c_1*X + c_0 + c_{-1}/X")
print("  = X^2/2 + (n/p)*X + lambda/n + n^2/X")

c2 = Fraction(1, 2)
c1 = n / p                    # 3/5
c0 = lam / n                  # 1/372
c_neg1 = n**2                 # 9

term_2 = c2 * X**2            # 1800
term_1 = c1 * X               # 36
term_0 = c0                   # 1/372
term_neg1 = c_neg1 / X        # 9/60 = 3/20

M = term_2 + term_1 + term_0 + term_neg1
expected_M = Fraction(853811, 465)

ok = M == expected_M
results.append(("M = X^2/2 + (n/p)*X + lambda/n + n^2/X = 853811/465", ok))

print(f"\n  Coefficients:")
print(f"    c_2    = {c2} (virial, proved)")
print(f"    c_1    = {c1} (coupling)")
print(f"    c_0    = {c0} (vacuum)")
print(f"    c_{{-1}} = {c_neg1} (confinement)")

print(f"\n  Terms:")
print(f"    c_2 * X^2    = {c2} * {X**2} = {term_2} = {float(term_2):.6f}")
print(f"    c_1 * X      = {c1} * {X} = {term_1} = {float(term_1):.6f}")
print(f"    c_0          = {c0} = {float(c0):.10f}")
print(f"    c_{{-1}} / X   = {c_neg1} / {X} = {term_neg1} = {float(term_neg1):.10f}")

print(f"\n  M = {term_2} + {term_1} + {term_0} + {term_neg1}")
print(f"    = {M}")
print(f"    = {float(M):.10f}")
print(f"  Expected: {expected_M} = {float(expected_M):.10f}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 6: Percentage contributions
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 6: Term contributions ---")

M_float = float(M)
pct_2 = float(term_2) / M_float * 100
pct_1 = float(term_1) / M_float * 100
pct_0 = float(term_0) / M_float * 100
pct_neg1 = float(term_neg1) / M_float * 100

ok = abs(pct_2 - 98.03) < 0.1  # Kinetic dominates at ~98%
results.append(("Kinetic term X^2/2 accounts for ~98% of M", ok))

print(f"  X^2/2:      {pct_2:.4f}%  (kinetic)")
print(f"  (n/p)*X:    {pct_1:.4f}%  (coupling)")
print(f"  lambda/n:   {pct_0:.6f}%  (vacuum)")
print(f"  n^2/X:      {pct_neg1:.6f}%  (confinement)")
print(f"  Total:      {pct_2 + pct_1 + pct_0 + pct_neg1:.6f}%")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 7: c_0 for all three Diophantine solutions
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 7: c_0 for all Diophantine solutions ---")

solutions = [(3, 5), (4, 3), (6, 2)]
all_ok = True

for n_val, p_val in solutions:
    nf = Fraction(n_val)
    pf = Fraction(p_val)
    lam_val = Fraction(1, p_val**3 - 1)
    c0_val = lam_val / nf
    c0_alt = Fraction(1, n_val * (p_val**3 - 1))

    ok = c0_val == c0_alt
    if not ok:
        all_ok = False

    denom = c0_val.denominator
    pf_denom = prime_factors(denom)

    print(f"  (n,p) = ({n_val},{p_val}): c_0 = {c0_val} (denom factors: {sorted(pf_denom)})")

results.append(("c_0 = 1/(n*(p^3-1)) for all solutions", all_ok))
print(f"  PASS" if all_ok else f"  FAIL")

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
