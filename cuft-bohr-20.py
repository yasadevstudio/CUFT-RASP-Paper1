#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-20.py — Muon mass

Verifies the muon-to-electron mass ratio formula:
    m_mu/m_e = p/(n*lambda) + 1/(2p) + lambda/p  (Eq 21)
               = 384589/1860  (Eq 22)
and compares against CODATA 2022 at 15 ppb (0.68 sigma).
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
CODATA_mmu = 206.7682827                    # m_mu/m_e, uncertainty (46)

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-20: Muon mass")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: Individual terms (Eq 21)
# --------------------------------------------------------------------------
print()
print("--- SECTION 1: m_mu/m_e = p/(n*lambda) + 1/(2p) + lambda/p ---")
print()

term1 = p / (n * lam)          # p * (p^3-1) / n = 5*124/3 = 620/3
term2 = Fraction(1, int(2 * p))  # 1/10
term3 = lam / p                # 1/(p*(p^3-1)) = 1/620

print(f"  Term 1 (leading):     p/(n*lambda) = {term1}")
print(f"                        = p*(p^3-1)/n = 5*124/3 = {float(term1):.12f}")
print()
print(f"  Term 2 (constant):    1/(2p) = {term2} = {float(term2):.12f}")
print()
print(f"  Term 3 (correction):  lambda/p = {term3} = {float(term3):.12f}")

# Verify individual terms
ok1 = (term1 == Fraction(620, 3))
results.append(("p/(n*lambda) = 620/3", ok1))
print(f"\n  p/(n*lambda) = 620/3: {'PASS' if ok1 else 'FAIL'}")

ok2 = (term2 == Fraction(1, 10))
results.append(("1/(2p) = 1/10", ok2))
print(f"  1/(2p) = 1/10: {'PASS' if ok2 else 'FAIL'}")

ok3 = (term3 == Fraction(1, 620))
results.append(("lambda/p = 1/620", ok3))
print(f"  lambda/p = 1/620: {'PASS' if ok3 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 2: Sum to exact rational (Eq 22)
# --------------------------------------------------------------------------
print()
print("--- SECTION 2: Exact muon mass ratio ---")
print()

m_mu = term1 + term2 + term3
print(f"  m_mu/m_e = {term1} + {term2} + {term3}")
print(f"           = {m_mu}")
print(f"           = {m_mu.numerator}/{m_mu.denominator}")
print(f"           = {float(m_mu):.12f}")

ok4 = (m_mu == Fraction(384589, 1860))
results.append(("m_mu/m_e = 384589/1860 (Eq 22)", ok4))
print(f"  Verify 384589/1860: {'PASS' if ok4 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 3: CODATA comparison
# --------------------------------------------------------------------------
print()
print("--- SECTION 3: CODATA 2022 comparison ---")
print()

fractional = abs(float(m_mu) - CODATA_mmu) / CODATA_mmu
ppb = fractional * 1e9
sigma = abs(float(m_mu) - CODATA_mmu) / 0.0000046  # uncertainty 46 in last digits

print(f"  Predicted:   {float(m_mu):.12f}")
print(f"  CODATA 2022: {CODATA_mmu:.12f}")
print(f"  |predicted - CODATA| = {abs(float(m_mu) - CODATA_mmu):.2e}")
print(f"  Fractional accuracy: {fractional:.2e} = {ppb:.1f} ppb")
print(f"  Sigma: {sigma:.2f} (within experimental uncertainty)")

ok5 = abs(ppb - 15) < 3
results.append(("Fractional accuracy approximately 15 ppb", ok5))
print(f"  Accuracy ~ 15 ppb: {'PASS' if ok5 else 'FAIL'}")

ok6 = sigma < 1.0
results.append(("Within 1 sigma of CODATA (0.68 sigma)", ok6))
print(f"  Within 1 sigma: {'PASS' if ok6 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 4: Denominator structure
# --------------------------------------------------------------------------
print()
print("--- SECTION 4: Denominator structure ---")
print()

denom = m_mu.denominator
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
print(f"  Denominator: {denom}")
print(f"  Factorization: {denom} = {factor_str}")
print(f"  Expected: 2^2 * 3 * 5 * 31 = {2**2 * 3 * 5 * 31}")

ok7 = (denom == 2 ** 2 * 3 * 5 * 31)
results.append(("Denominator = 2^2 * 3 * 5 * 31 = 1860", ok7))
print(f"  Verify: {'PASS' if ok7 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 5: Verify 1860 = 4 * 465
# --------------------------------------------------------------------------
print()
print("--- SECTION 5: Denominator relationship ---")
print()

print(f"  1860 = 4 * 465 = 4 * n * p * Phi_3(p)")
print(f"  465 = n * p * Phi_3(p) = 3 * 5 * 31 (proton denominator)")
print(f"  1860 / 465 = {1860 // 465}")
print(f"  1860 = 2^2 * n * p * Phi_3(p)")

ok8 = (denom == 4 * 465) and (465 == 3 * 5 * 31)
results.append(("1860 = 4 * 465 = 4 * n * p * Phi_3", ok8))
print(f"  Verify: {'PASS' if ok8 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 6: Lambda-order hierarchy position
# --------------------------------------------------------------------------
print()
print("--- SECTION 6: Lambda-order hierarchy ---")
print()

print("  The muon sits at lambda^{-1} order in the hierarchy:")
print()
print("  | Constant | Lambda order | Leading term    | Value     |")
print("  |----------|-------------|-----------------|-----------|")
print(f"  | m_mu/m_e | lambda^{{-1}} | p/(n*lambda)    | {float(term1):.4f}  |")
print(f"  | 1/alpha  | lambda^0    | p^3 + n(p-1)   | 137       |")
print(f"  | m_p/m_e  | lambda^1    | X^2/2           | 1800      |")
print(f"  | m_n/m_e  | lambda^2    | M + np*lam^2    | ~1838.68  |")
print()
print(f"  Leading term p/(n*lambda) = p*(p^3-1)/n = {float(term1):.4f}")
print(f"  diverges as lambda -> 0: the muon mass is SET by the confinement scale.")

# --------------------------------------------------------------------------
# SECTION 7: Cross-check computation
# --------------------------------------------------------------------------
print()
print("--- SECTION 7: Cross-check with direct arithmetic ---")
print()

# Compute 620/3 + 1/10 + 1/620 from scratch
check = Fraction(620, 3) + Fraction(1, 10) + Fraction(1, 620)
print(f"  620/3 + 1/10 + 1/620 = {check}")
print(f"  = {check.numerator}/{check.denominator}")

ok9 = (check == Fraction(384589, 1860))
results.append(("Cross-check: 620/3 + 1/10 + 1/620 = 384589/1860", ok9))
print(f"  Cross-check: {'PASS' if ok9 else 'FAIL'}")

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
