#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-8.py — Virial equivalence

Proves c_2 = 1/2 for all three Diophantine solutions.
Shows the virial relation n*(p-1) = 2*(p+1) is algebraically
equivalent to the Diophantine equation (n-2)(p-1) = 4.
"""

from fractions import Fraction

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-8: Virial equivalence")
print("=" * 72)

results = []

# ============================================================================
# THE VIRIAL RELATION
# ============================================================================
print("\n--- The virial relation ---")
print("The leading coefficient of the mass formula is:")
print("  c_2 = n * Gamma * (Gamma - 1) / X^2")
print("      = (p + 1) / (n * (p - 1))")
print()
print("THEOREM: c_2 = 1/2 if and only if n*(p-1) = 2*(p+1).")
print()

# ============================================================================
# SECTION 1: Verify c_2 = 1/2 via both formulas for each solution
# ============================================================================
print("--- SECTION 1: c_2 = 1/2 for all Diophantine solutions ---")
print()

diophantine_solutions = [(3, 5), (4, 3), (6, 2)]

print(f"  {'(n,p)':>6} {'Gamma':>6} {'X':>4} {'n*G*(G-1)/X^2':>16} {'(p+1)/(n*(p-1))':>18} {'c_2':>6} {'=1/2?':>6}")
print("  " + "-" * 62)

all_half = True
for n_val, p_val in diophantine_solutions:
    n = Fraction(n_val)
    p = Fraction(p_val)
    Gamma = p**2
    X = n * p * (p - 1)

    # Formula 1: c_2 = n * Gamma * (Gamma - 1) / X^2
    c2_formula1 = n * Gamma * (Gamma - 1) / X**2

    # Formula 2: c_2 = (p + 1) / (n * (p - 1))
    c2_formula2 = (p + 1) / (n * (p - 1))

    is_half = (c2_formula1 == Fraction(1, 2) and c2_formula2 == Fraction(1, 2))
    if not is_half:
        all_half = False

    print(f"  ({n_val},{p_val}){int(Gamma):>6}{int(X):>5}   {str(c2_formula1):>14}   {str(c2_formula2):>16}  {str(c2_formula1):>5} {'YES' if is_half else 'NO':>5}")

results.append(("c_2 = 1/2 for all three solutions", all_half))
print(f"\n  c_2 = 1/2 for all three solutions: {'PASS' if all_half else 'FAIL'}")

# ============================================================================
# SECTION 2: Detailed verification for each solution
# ============================================================================
print("\n--- SECTION 2: Detailed c_2 computation ---")

for n_val, p_val in diophantine_solutions:
    n = Fraction(n_val)
    p = Fraction(p_val)
    print(f"\n  (n,p) = ({n_val},{p_val}):")
    print(f"    c_2 = (p+1)/(n*(p-1)) = ({p_val}+1)/({n_val}*({p_val}-1)) = {p_val+1}/({n_val}*{p_val-1}) = {p_val+1}/{n_val*(p_val-1)}")
    c2 = (p + 1) / (n * (p - 1))
    print(f"    = {c2}")

    ok_ind = (c2 == Fraction(1, 2))
    results.append((f"c_2 = {p_val+1}/{n_val*(p_val-1)} = 1/2 for ({n_val},{p_val})", ok_ind))
    print(f"    {'PASS' if ok_ind else 'FAIL'}")

# ============================================================================
# SECTION 3: Algebraic equivalence proof
# ============================================================================
print("\n--- SECTION 3: Virial <=> Diophantine equivalence ---")
print()
print("  CLAIM: n*(p-1) = 2*(p+1) is equivalent to (n-2)(p-1) = 4")
print()
print("  PROOF (forward direction):")
print("    Start:  n*(p-1) = 2*(p+1)")
print("    Expand: n*p - n = 2*p + 2")
print("    Subtract 2*(p-1) from both sides:")
print("      n*p - n - 2*p + 2 = 2*p + 2 - 2*p + 2 = 4")
print("    Factor left side:")
print("      (n-2)*(p-1) = n*p - n - 2*p + 2 = 4")
print("    QED")
print()
print("  PROOF (reverse direction):")
print("    Start:  (n-2)*(p-1) = 4")
print("    Expand: n*p - n - 2*p + 2 = 4")
print("    Rearrange: n*p - n = 2*p + 2")
print("    Factor: n*(p-1) = 2*(p+1)")
print("    QED")
print()

# Verify algebraically for all solutions
print("  Numerical verification:")
all_equiv = True
for n_val, p_val in diophantine_solutions:
    virial = n_val * (p_val - 1)
    rhs_virial = 2 * (p_val + 1)
    dioph = (n_val - 2) * (p_val - 1)

    match_v = (virial == rhs_virial)
    match_d = (dioph == 4)

    if not (match_v and match_d):
        all_equiv = False

    print(f"    ({n_val},{p_val}): n*(p-1) = {virial}, 2*(p+1) = {rhs_virial}, equal: {match_v} | (n-2)(p-1) = {dioph} = 4: {match_d}")

results.append(("Virial <=> Diophantine for all solutions", all_equiv))
print(f"  {'PASS' if all_equiv else 'FAIL'}")

# ============================================================================
# SECTION 4: Physical significance
# ============================================================================
print("\n--- SECTION 4: Physical significance ---")
print()
print("  The virial relation c_2 = 1/2 means the leading coefficient of the")
print("  mass formula is DERIVED, not assumed. This single coefficient accounts")
print("  for the dominant term X^2/2, which contributes:")
print()

for n_val, p_val in diophantine_solutions:
    n = Fraction(n_val)
    p = Fraction(p_val)
    X = n * p * (p - 1)
    lam = Fraction(1, int(p**3 - 1))
    M = X**2 / 2 + (n / p) * X + n**2 / X + lam / n
    dom = X**2 / 2
    pct = float(dom) / float(M) * 100
    print(f"    ({n_val},{p_val}): X^2/2 = {dom}, M = {float(M):.4f}, X^2/2 is {pct:.2f}% of M")

# ============================================================================
# SECTION 5: Completeness check - no other c_2 works
# ============================================================================
print("\n--- SECTION 5: Uniqueness of c_2 = 1/2 ---")
print()
print("  If c_2 were any value other than 1/2, the virial relation would fail,")
print("  meaning the Diophantine (n-2)(p-1) = 4 would not hold, and the")
print("  parameter selection chain would break.")
print()
print("  The virial equivalence PROVES that the leading term is not a free")
print("  parameter -- it is a consequence of the same Diophantine constraint")
print("  that selects the integer solutions.")
print()

# Test: for n=3, what c_2 would we get if we used a WRONG p?
print("  Counter-examples (wrong p values for n=3):")
print(f"  {'p':>4} {'c_2 = (p+1)/(3*(p-1))':>25} {'= 1/2?':>8}")
print("  " + "-" * 40)
n = Fraction(3)
for p_val in [2, 3, 4, 5, 6, 7, 8]:
    p = Fraction(p_val)
    c2 = (p + 1) / (n * (p - 1))
    is_half = (c2 == Fraction(1, 2))
    print(f"  {p_val:>4}   {str(c2):>23}   {'YES' if is_half else 'no':>6}")

ok_unique = True  # only p=5 gives 1/2 for n=3
for p_val in [2, 3, 4, 6, 7, 8]:
    c2 = Fraction(p_val + 1, 3 * (p_val - 1))
    if c2 == Fraction(1, 2):
        ok_unique = False
c2_5 = Fraction(6, 3 * 4)
ok_unique = ok_unique and (c2_5 == Fraction(1, 2))
results.append(("Only p=5 gives c_2=1/2 for n=3", ok_unique))
print(f"\n  Only p=5 yields c_2 = 1/2 for n=3: {'PASS' if ok_unique else 'FAIL'}")

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
