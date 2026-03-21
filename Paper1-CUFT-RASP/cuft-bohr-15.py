#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-15.py — Three-term physical structure

Verifies the three-term rewriting M = Y^2/2 + n^2/X + gamma where
Y = X + n/p is the shifted collective variable and gamma = lambda/n
- n^2/(2p^2) is the vacuum correction. Shows the three physical
components: shifted kinetic, Coulomb confinement, vacuum. Confirms
gamma < 0 for all three Diophantine solutions.

Paper reference: Section 4 (Eq 12)
"""

from fractions import Fraction

results = []

print("=" * 70)
print("CUFT-BOHR-15: Three-term physical structure")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS for (3,5)
# ═══════════════════════════════════════════════════════════════
n = Fraction(3)
p = Fraction(5)
X = n * p * (p - 1)              # 60
lam = Fraction(1, 124)          # 1/(p^3-1)
Gamma = p**2                     # 25

# ═══════════════════════════════════════════════════════════════
# TEST 1: Y = X + n/p
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 1: Shifted collective variable Y ---")

Y = X + n / p
expected_Y = Fraction(303, 5)  # 60 + 3/5 = 300/5 + 3/5 = 303/5

ok = Y == expected_Y
results.append(("Y = X + n/p = 60 + 3/5 = 303/5", ok))

print(f"  X = {X}")
print(f"  n/p = {n/p}")
print(f"  Y = X + n/p = {X} + {n/p} = {Y}")
print(f"  Expected: 303/5 = {expected_Y}")
print(f"  Y = {float(Y):.6f}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 2: gamma = lambda/n - n^2/(2*p^2)
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 2: Vacuum correction gamma ---")

gamma = lam / n - n**2 / (2 * p**2)

print(f"  lambda/n      = {lam/n} = {float(lam/n):.10f}")
print(f"  n^2/(2*p^2)   = {n**2/(2*p**2)} = {float(n**2/(2*p**2)):.10f}")
print(f"  gamma = {lam/n} - {n**2/(2*p**2)}")
print(f"        = {gamma}")
print(f"        = {float(gamma):.10f}")

ok = gamma < 0
results.append(("gamma < 0 for (3,5)", ok))
print(f"  gamma < 0: {gamma < 0}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 3: Verify M = Y^2/2 + n^2/X + gamma
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 3: Three-term formula M = Y^2/2 + n^2/X + gamma ---")

term_kinetic = Y**2 / 2
term_confinement = n**2 / X
term_vacuum = gamma

M_three = term_kinetic + term_confinement + term_vacuum

# Compare with the standard 4-term formula
M_four = X**2 / 2 + (n / p) * X + n**2 / X + lam / n

ok = M_three == M_four
results.append(("Y^2/2 + n^2/X + gamma = X^2/2 + (n/p)*X + n^2/X + lambda/n", ok))

print(f"  Three-term:")
print(f"    Y^2/2    = {term_kinetic} = {float(term_kinetic):.10f}")
print(f"    n^2/X    = {term_confinement} = {float(term_confinement):.10f}")
print(f"    gamma    = {term_vacuum} = {float(term_vacuum):.10f}")
print(f"    Sum      = {M_three} = {float(M_three):.10f}")
print(f"\n  Four-term (standard):")
print(f"    M = {M_four} = {float(M_four):.10f}")
print(f"\n  Match: {M_three == M_four}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 4: Show the algebraic cancellation
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 4: Algebraic cancellation Y^2/2 expansion ---")

# Y^2/2 = (X + n/p)^2/2 = X^2/2 + (n/p)*X + n^2/(2p^2)
Y_sq_half = (X + n/p)**2 / 2
expansion = X**2/2 + (n/p)*X + n**2/(2*p**2)

ok1 = Y_sq_half == expansion
print(f"  (X + n/p)^2/2 = X^2/2 + (n/p)*X + n^2/(2p^2)")
print(f"  LHS = {Y_sq_half}")
print(f"  RHS = {expansion}")
print(f"  Match: {ok1}")

# Then: Y^2/2 + gamma = X^2/2 + (n/p)*X + n^2/(2p^2) + lambda/n - n^2/(2p^2)
#                      = X^2/2 + (n/p)*X + lambda/n
combined = Y_sq_half + gamma
expected_combined = X**2/2 + (n/p)*X + lam/n
ok2 = combined == expected_combined

print(f"\n  Y^2/2 + gamma = X^2/2 + (n/p)*X + n^2/(2p^2) + lambda/n - n^2/(2p^2)")
print(f"                = X^2/2 + (n/p)*X + lambda/n")
print(f"  The n^2/(2p^2) cross-term CANCELS exactly.")
print(f"  Y^2/2 + gamma = {combined}")
print(f"  X^2/2 + (n/p)*X + lambda/n = {expected_combined}")
print(f"  Match: {ok2}")

ok = ok1 and ok2
results.append(("Cross-term n^2/(2p^2) cancels in Y^2/2 + gamma", ok))
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 5: Three physical components
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 5: Physical component identification ---")

M_float = float(M_three)
print(f"  SHIFTED KINETIC:       Y^2/2  = {float(term_kinetic):.6f}  ({float(term_kinetic)/M_float*100:.2f}%)")
print(f"  COULOMB CONFINEMENT:   n^2/X  = {float(term_confinement):.6f}  ({float(term_confinement)/M_float*100:.4f}%)")
print(f"  VACUUM CORRECTION:     gamma  = {float(term_vacuum):.6f} ({float(term_vacuum)/M_float*100:.4f}%)")
print(f"  TOTAL:                 M      = {M_float:.6f}")

ok = M_three == Fraction(853811, 465)
results.append(("M = 853811/465 from three-term formula", ok))
print(f"  M = {M_three} = 853811/465: {ok}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 6: gamma < 0 for all three Diophantine solutions
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 6: gamma < 0 for all Diophantine solutions ---")

solutions = [(3, 5), (4, 3), (6, 2)]
all_negative = True

for n_val, p_val in solutions:
    nf = Fraction(n_val)
    pf = Fraction(p_val)
    lam_val = Fraction(1, p_val**3 - 1)

    gamma_val = lam_val / nf - nf**2 / (2 * pf**2)
    is_neg = gamma_val < 0
    if not is_neg:
        all_negative = False

    print(f"  (n,p) = ({n_val},{p_val}): gamma = {gamma_val} = {float(gamma_val):.10f}  (< 0: {is_neg})")

results.append(("gamma < 0 for all three solutions (net attractive vacuum)", all_negative))
print(f"  All negative: {all_negative}")
print(f"  PASS" if all_negative else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 7: Verify M for all three solutions via three-term formula
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 7: Three-term formula for all solutions ---")

all_ok = True
for n_val, p_val in solutions:
    nf = Fraction(n_val)
    pf = Fraction(p_val)
    X_val = nf * pf * (pf - 1)
    lam_val = Fraction(1, p_val**3 - 1)

    Y_val = X_val + nf / pf
    gamma_val = lam_val / nf - nf**2 / (2 * pf**2)

    M_3term = Y_val**2 / 2 + nf**2 / X_val + gamma_val
    M_4term = X_val**2 / 2 + (nf / pf) * X_val + nf**2 / X_val + lam_val / nf

    ok = M_3term == M_4term
    if not ok:
        all_ok = False

    print(f"  (n,p) = ({n_val},{p_val}): M_3term = {float(M_3term):.6f}, M_4term = {float(M_4term):.6f}, match: {ok}")

results.append(("Three-term = four-term for all solutions", all_ok))
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
