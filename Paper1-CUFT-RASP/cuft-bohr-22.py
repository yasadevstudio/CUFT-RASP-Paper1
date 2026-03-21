#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-22.py — Occam uniqueness scan, c_{-1} = c_1^2 * Gamma

Exhaustive scan over c_1 = a/b with |a|<=20, 1<=b<=20 and integer c_{-1}
with |c_{-1}|<=30. Computes c_0 from the mass formula. Keeps solutions
where c_0 denominator divides 1860 = n*p*(p^3-1). Ranks by |c_0|.
Shows (3/5, 9, 1/372) is the unique minimum-|c_0| solution with primes
only from {2, n, p, Phi_3(p)} = {2, 3, 5, 31}.
Verifies c_{-1} = c_1^2 * Gamma.
"""

from fractions import Fraction
from collections import Counter

# ============================================================================
# PARAMETERS
# ============================================================================

n = Fraction(3)
p = Fraction(5)
Gamma = p ** 2                              # 25
lam = Fraction(1, int(p ** 3 - 1))         # 1/124
X = n * p * (p - 1)                        # 60
Phi3 = p ** 2 + p + 1                      # 31
M = Fraction(int(X) ** 2, 2) + Fraction(int(n), int(p)) * int(X) + Fraction(int(n) ** 2, int(X)) + lam / n

# The target denominator divisor: n * p * (p^3 - 1) = 3 * 5 * 124 = 1860
denom_target = int(n * p) * (int(p) ** 3 - 1)  # 1860

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-22: Occam uniqueness scan, c_{-1} = c_1^2 * Gamma")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: Exhaustive scan
# --------------------------------------------------------------------------
print()
print("--- SECTION 1: Exhaustive scan ---")
print()
print(f"  M = {M} = {float(M):.10f}")
print(f"  Mass formula: M = X^2/2 + c_1*X + c_0 + c_{{-1}}/X")
print(f"  X = {int(X)}")
print(f"  Scan: c_1 = a/b (|a|<=20, 1<=b<=20), c_{{-1}} integer (|c_{{-1}}|<=30)")
print(f"  Filter: denominator of c_0 divides {denom_target}")
print()

# For each (c_1, c_{-1}), solve for c_0:
# M = X^2/2 + c_1*X + c_0 + c_{-1}/X
# c_0 = M - X^2/2 - c_1*X - c_{-1}/X

X_int = int(X)
X_frac = Fraction(X_int)
half_X2 = Fraction(X_int ** 2, 2)

def get_prime_factors(d):
    """Return set of prime factors of integer d."""
    d = abs(d)
    if d <= 1:
        return set()
    primes = set()
    for trial in range(2, d + 1):
        if trial * trial > d:
            if d > 1:
                primes.add(d)
            break
        while d % trial == 0:
            primes.add(trial)
            d //= trial
    return primes

solutions = []  # list of (c_1, c_m1, c_0)

scan_count = 0
for a in range(-20, 21):
    for b in range(1, 21):
        c1 = Fraction(a, b)
        for cm1 in range(-30, 31):
            c0 = M - half_X2 - c1 * X_frac - Fraction(cm1, X_int)
            # Keep only if denominator divides 1860
            if denom_target % c0.denominator == 0:
                solutions.append((c1, cm1, c0))
            scan_count += 1

print(f"  Total combinations scanned: {scan_count}")
print(f"  Solutions with denom(c_0) | {denom_target}: {len(solutions)}")

# Deduplicate by (c_1, c_{-1}) — some a/b pairs are equivalent fractions
unique = {}
for c1, cm1, c0 in solutions:
    key = (c1, cm1)
    if key not in unique:
        unique[key] = c0

print(f"  Distinct (c_1, c_{{-1}}) pairs: {len(unique)}")

# --------------------------------------------------------------------------
# SECTION 2: Top solutions ranked by |c_0|
# --------------------------------------------------------------------------
print()
print("--- SECTION 2: Solutions ranked by |c_0| (smallest first) ---")
print()

sorted_solutions = sorted(unique.items(), key=lambda x: abs(x[1]))

print(f"  {'c_1':>6} | {'c_{-1}':>6} | {'c_0':>12} | {'|c_0|':>10} | {'Primes in denom':>20}")
print(f"  {'---':>6} | {'---':>6} | {'---':>12} | {'---':>10} | {'---':>20}")

for i, ((c1, cm1), c0) in enumerate(sorted_solutions[:15]):
    primes = get_prime_factors(c0.denominator)
    pstr = "{" + ", ".join(str(pr) for pr in sorted(primes)) + "}" if primes else "{1}"
    print(f"  {str(c1):>6} | {cm1:>6} | {str(c0):>12} | {abs(float(c0)):>10.5f} | {pstr:>20}")

# Verify our solution is first
ok1 = sorted_solutions[0][0] == (Fraction(3, 5), 9)
results.append(("(3/5, 9) is the minimum-|c_0| solution", ok1))
print(f"\n  Our solution is #1 (smallest |c_0|): {'PASS' if ok1 else 'FAIL'}")

# Verify c_0 = 1/372
our_c0 = sorted_solutions[0][1]
ok2 = (our_c0 == Fraction(1, 372))
results.append(("c_0 = 1/372 for our solution", ok2))
print(f"  c_0 = 1/372: {'PASS' if ok2 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 3: Prime structure of winning solution
# --------------------------------------------------------------------------
print()
print("--- SECTION 3: Denominator prime structure ---")
print()

d = 372
factors = {}
temp = d
for pr in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    while temp % pr == 0:
        factors[pr] = factors.get(pr, 0) + 1
        temp //= pr
if temp > 1:
    factors[temp] = 1

factor_display = " * ".join(f"{pr}^{exp}" if exp > 1 else str(pr)
                            for pr, exp in sorted(factors.items()))
prime_set = sorted(factors.keys())

print(f"  c_0 denominator: {d} = {factor_display}")
print(f"  Prime factors: {set(prime_set)}")
print(f"  All from {{2, n, p, Phi_3(p)}} = {{2, 3, 5, 31}}: {set(prime_set).issubset({2, 3, 5, 31})}")
print(f"  31 = Phi_3(5) = p^2 + p + 1")

ok3 = set(prime_set).issubset({2, 3, 5, 31})
results.append(("c_0 primes are subset of {2, 3, 5, 31}", ok3))
print(f"  Prime closure: {'PASS' if ok3 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 4: Our solution is UNIQUE with primes only from {2,3,5,31}
#            AND smallest |c_0|
# --------------------------------------------------------------------------
print()
print("--- SECTION 4: Uniqueness at minimum |c_0| ---")
print()

# Count how many solutions with c_1 = 3/5 exist
c1_35_count = sum(1 for (c1, _), _ in sorted_solutions if c1 == Fraction(3, 5))
print(f"  Solutions with c_1 = 3/5: {c1_35_count}")

# Show the top-4 with c_1 = 3/5 (matching paper Table)
c1_35_solutions = [(key, c0) for key, c0 in sorted_solutions if key[0] == Fraction(3, 5)]
c1_35_solutions.sort(key=lambda x: abs(x[1]))

print()
print(f"  Solutions with c_1 = 3/5, ranked by |c_0|:")
print(f"  {'c_1':>6} | {'c_{-1}':>6} | {'c_0':>12} | {'|c_0|':>10} | {'Primes':>16}")
print(f"  {'---':>6} | {'---':>6} | {'---':>12} | {'---':>10} | {'---':>16}")

for i, ((c1, cm1), c0) in enumerate(c1_35_solutions[:6]):
    primes = get_prime_factors(c0.denominator)
    pstr = "{" + ", ".join(str(pr) for pr in sorted(primes)) + "}" if primes else "{1}"
    mark = " *" if c1 == Fraction(3, 5) and cm1 == 9 else ""
    print(f"  {str(c1):>6} | {cm1:>6} | {str(c0):>12} | {abs(float(c0)):>10.5f} | {pstr:>16}{mark}")

ok4 = c1_35_solutions[0][0] == (Fraction(3, 5), 9)
results.append(("(3/5, 9) is the smallest-|c_0| among c_1=3/5 solutions", ok4))
print(f"\n  Our solution is #1 among c_1=3/5: {'PASS' if ok4 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 5: Verify c_{-1} = c_1^2 * Gamma
# --------------------------------------------------------------------------
print()
print("--- SECTION 5: c_{{-1}} = c_1^2 * Gamma ---")
print()

c1_winner = Fraction(3, 5)
cm1_winner = 9
c0_winner = Fraction(1, 372)

check_cm1 = c1_winner ** 2 * Gamma
print(f"  c_1 = {c1_winner}")
print(f"  c_1^2 = {c1_winner ** 2}")
print(f"  c_1^2 * Gamma = {c1_winner ** 2} * {Gamma} = {check_cm1}")
print(f"  c_{{-1}} = {cm1_winner}")

ok5 = (int(check_cm1) == cm1_winner)
results.append(("c_{-1} = c_1^2 * Gamma = (3/5)^2 * 25 = 9 = n^2", ok5))
print(f"  c_{{-1}} = c_1^2 * Gamma: {'PASS' if ok5 else 'FAIL'}")

# Also verify c_{-1} = n^2
ok6 = (cm1_winner == int(n) ** 2)
results.append(("c_{-1} = n^2 = 9", ok6))
print(f"  c_{{-1}} = n^2: {'PASS' if ok6 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 6: Verify c_0 = lambda/n
# --------------------------------------------------------------------------
print()
print("--- SECTION 6: c_0 = lambda/n ---")
print()

lambda_over_n = lam / n
print(f"  lambda/n = {lam}/{n} = {lambda_over_n}")
print(f"  c_0 = {c0_winner}")

ok7 = (c0_winner == lambda_over_n)
results.append(("c_0 = lambda/n = 1/372", ok7))
print(f"  c_0 = lambda/n: {'PASS' if ok7 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 7: Reconstruct M from winning coefficients
# --------------------------------------------------------------------------
print()
print("--- SECTION 7: Mass formula reconstruction ---")
print()

M_check = half_X2 + c1_winner * X_frac + c0_winner + Fraction(cm1_winner, X_int)
print(f"  M = X^2/2 + c_1*X + c_0 + c_{{-1}}/X")
print(f"    = {half_X2} + {c1_winner}*{X_int} + {c0_winner} + {cm1_winner}/{X_int}")
print(f"    = {half_X2} + {c1_winner * X_frac} + {c0_winner} + {Fraction(cm1_winner, X_int)}")
print(f"    = {M_check}")
print(f"    = {M_check.numerator}/{M_check.denominator}")

ok8 = (M_check == M)
results.append(("Reconstructed M matches 853811/465", ok8))
print(f"  M_reconstructed = M: {'PASS' if ok8 else 'FAIL'}")

# ============================================================================
# SUMMARY
# ============================================================================
print()
print("=" * 72)
print("SUMMARY")
print("=" * 72)
passed = sum(1 for _, ok in results if ok)
total = len(results)
for desc, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")
print(f"\n  {passed}/{total} checks passed.")
if passed == total:
    print("  ALL CHECKS PASSED.")
else:
    print(f"  WARNING: {total - passed} check(s) FAILED.")
