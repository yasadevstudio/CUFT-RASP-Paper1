#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-18.py — Fine structure constant

Verifies the fine-structure constant formula:
    1/alpha = p^3 + n(p-1) + n^2/(2p^3) = 34259/250
and compares against CODATA 2022 at 6.0 ppb precision.
"""

from fractions import Fraction

# ============================================================================
# PARAMETERS
# ============================================================================

n = Fraction(3)
p = Fraction(5)
Gamma = p ** 2                              # 25
lam = Fraction(1, int(p ** 3 - 1))         # 1/124
X = n * p * (p - 1)                        # 60
Phi3 = p ** 2 + p + 1                      # 31

# CODATA 2022
CODATA_inv_alpha = 137.035999177            # uncertainty: (21) = 0.000000021

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-18: Fine structure constant")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: The alpha formula (Eq 17)
# --------------------------------------------------------------------------
print()
print("--- SECTION 1: 1/alpha = p^3 + n(p-1) + n^2/(2p^3) ---")
print()

term1 = p ** 3                              # 125
term2 = n * (p - 1)                         # 12
term3 = n ** 2 / (2 * p ** 3)              # 9/250

print(f"  Term 1 (cubic gain):    p^3        = {term1}")
print(f"  Term 2 (quark-gate):    n(p-1)     = {term2}")
print(f"  Term 3 (correction):    n^2/(2p^3) = {term3}")
print()

inv_alpha = term1 + term2 + term3
print(f"  1/alpha = {term1} + {term2} + {term3}")
print(f"          = {inv_alpha}")
print(f"          = {inv_alpha.numerator}/{inv_alpha.denominator}")
print(f"          = {float(inv_alpha):.12f}")

ok1 = (inv_alpha == Fraction(34259, 250))
results.append(("1/alpha = 34259/250 exactly", ok1))
print(f"  Verify 34259/250: {'PASS' if ok1 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 2: Numerical decomposition
# --------------------------------------------------------------------------
print()
print("--- SECTION 2: Numerical decomposition ---")
print()

print(f"  p^3        = {float(term1):>10.6f}  ({float(term1/inv_alpha)*100:.2f}%)")
print(f"  n(p-1)     = {float(term2):>10.6f}  ({float(term2/inv_alpha)*100:.2f}%)")
print(f"  n^2/(2p^3) = {float(term3):>10.6f}  ({float(term3/inv_alpha)*100:.4f}%)")
print(f"  Total      = {float(inv_alpha):>10.6f}")

# --------------------------------------------------------------------------
# SECTION 3: CODATA comparison
# --------------------------------------------------------------------------
print()
print("--- SECTION 3: CODATA 2022 comparison ---")
print()

fractional = abs(float(inv_alpha) - CODATA_inv_alpha) / CODATA_inv_alpha
ppb = fractional * 1e9

print(f"  Predicted:   {float(inv_alpha):.12f}")
print(f"  CODATA 2022: {CODATA_inv_alpha:.12f}")
print(f"  |predicted - CODATA| = {abs(float(inv_alpha) - CODATA_inv_alpha):.2e}")
print(f"  Fractional accuracy: {fractional:.2e} = {ppb:.1f} ppb")

ok2 = abs(ppb - 6.0) < 1.0
results.append(("Fractional accuracy approximately 6.0 ppb", ok2))
print(f"  Accuracy ~ 6.0 ppb: {'PASS' if ok2 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 4: Integer part uniqueness across Diophantine solutions
# --------------------------------------------------------------------------
print()
print("--- SECTION 4: Integer part uniqueness ---")
print()

dioph_solutions = [(3, 5), (4, 3), (6, 2)]
print(f"  {'(n,p)':>8}  {'p^3':>6}  {'n(p-1)':>8}  {'p^3+n(p-1)':>12}  {'Match 137?':>10}")
print(f"  {'---':>8}  {'---':>6}  {'---':>8}  {'---':>12}  {'---':>10}")

for nn, pp in dioph_solutions:
    t1 = pp ** 3
    t2 = nn * (pp - 1)
    total = t1 + t2
    match = "YES" if total == 137 else "no"
    print(f"  ({nn},{pp}){t1:>6}{t2:>8}{total:>12}  {match:>10}")

ok3 = True
for nn, pp in dioph_solutions:
    if nn == 3 and pp == 5:
        ok3 = ok3 and (pp ** 3 + nn * (pp - 1) == 137)
    else:
        ok3 = ok3 and (pp ** 3 + nn * (pp - 1) != 137)

results.append(("Only (3,5) gives integer part 137", ok3))
print(f"\n  Only (3,5) gives 137: {'PASS' if ok3 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 5: Verify (4,3) and (6,2) give 35 and 14
# --------------------------------------------------------------------------
print()
print("--- SECTION 5: Other Diophantine solutions ---")
print()

val_43 = 3 ** 3 + 4 * (3 - 1)  # 27 + 8 = 35
val_62 = 2 ** 3 + 6 * (2 - 1)  # 8 + 6 = 14

print(f"  (4,3): p^3 + n(p-1) = 27 + 8 = {val_43}")
print(f"  (6,2): p^3 + n(p-1) =  8 + 6 = {val_62}")

ok4 = (val_43 == 35) and (val_62 == 14)
results.append(("(4,3) gives 35, (6,2) gives 14", ok4))
print(f"  Verify: {'PASS' if ok4 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 6: Denominator structure
# --------------------------------------------------------------------------
print()
print("--- SECTION 6: Denominator structure ---")
print()

denom = inv_alpha.denominator
print(f"  Denominator: {denom}")
print(f"  250 = 2 * 5^3 = 2 * p^3")

# Factor 250
d = denom
factors = {}
for pr in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    while d % pr == 0:
        factors[pr] = factors.get(pr, 0) + 1
        d //= pr
if d > 1:
    factors[d] = 1

factor_str = " * ".join(f"{pr}^{exp}" if exp > 1 else str(pr)
                        for pr, exp in sorted(factors.items()))
print(f"  Factorization: {denom} = {factor_str}")

ok5 = (denom == 250) and (denom == 2 * 5 ** 3)
results.append(("Denominator 250 = 2 * p^3", ok5))
print(f"  Verify 250 = 2*5^3: {'PASS' if ok5 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 7: Numerator structure
# --------------------------------------------------------------------------
print()
print("--- SECTION 7: Numerator structure ---")
print()

numer = inv_alpha.numerator
print(f"  Numerator: {numer}")
print(f"  34259 = 250 * 137 + 9 = 250 * (p^3 + n(p-1)) + n^2")

verify_num = 250 * 137 + 9
ok6 = (numer == 34259) and (verify_num == 34259)
results.append(("Numerator 34259 = 250*137 + 9", ok6))
print(f"  Verify: 250*137 + 9 = {verify_num}: {'PASS' if ok6 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 8: Full exact rational verification
# --------------------------------------------------------------------------
print()
print("--- SECTION 8: Complete rational verification ---")
print()

# Rebuild from scratch with pure Fraction
alpha_inv_check = Fraction(5) ** 3 + Fraction(3) * (Fraction(5) - 1) + Fraction(9, 250)
print(f"  125 + 12 + 9/250 = {alpha_inv_check}")
print(f"  = {alpha_inv_check.numerator}/{alpha_inv_check.denominator}")

ok7 = (alpha_inv_check == Fraction(34259, 250))
results.append(("Cross-check: 125 + 12 + 9/250 = 34259/250", ok7))
print(f"  Cross-check: {'PASS' if ok7 else 'FAIL'}")

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
