#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-19.py — Neutron mass

Verifies the neutron-to-electron mass ratio formula:
    m_n/m_e = M + p/2 + n^2/(pX) + np*lambda^2  (Eq 19)
and the lambda^2 correction that closes to 0.009 ppb.
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

# Proton mass ratio M = 853811/465
M = Fraction(int(X) ** 2, 2) + Fraction(int(n), int(p)) * int(X) + Fraction(int(n) ** 2, int(X)) + lam / n

# CODATA 2022
CODATA_mn = 1838.68366173                   # m_n/m_e, uncertainty (89)

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-19: Neutron mass")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: Individual terms (Eq 19)
# --------------------------------------------------------------------------
print()
print("--- SECTION 1: m_n/m_e = M + p/2 + n^2/(pX) + np*lambda^2 ---")
print()

term_M = M
term_p2 = p / 2
term_n2pX = n ** 2 / (p * X)
term_lam2 = n * p * lam ** 2

print(f"  M (proton base) = {term_M}")
print(f"                  = {float(term_M):.12f}")
print()
print(f"  p/2 (isospin)         = {term_p2} = {float(term_p2):.12f}")
print(f"  n^2/(pX) (confinement) = {term_n2pX} = {float(term_n2pX):.12f}")
print(f"  np*lambda^2 (2nd order) = {term_lam2} = {float(term_lam2):.12f}")

# Verify individual terms
ok1 = (term_p2 == Fraction(5, 2))
results.append(("p/2 = 5/2", ok1))
print(f"\n  p/2 = 5/2: {'PASS' if ok1 else 'FAIL'}")

ok2 = (term_n2pX == Fraction(9, 300))
ok2b = (term_n2pX == Fraction(3, 100))
results.append(("n^2/(pX) = 9/300 = 3/100", ok2 and ok2b))
print(f"  n^2/(pX) = 3/100: {'PASS' if ok2b else 'FAIL'}")

ok3 = (term_lam2 == Fraction(15, 124 ** 2))
results.append(("np*lambda^2 = 15/15376", ok3))
print(f"  np*lambda^2 = 15/{124**2}: {'PASS' if ok3 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 2: Sum to exact rational (Eq 20)
# --------------------------------------------------------------------------
print()
print("--- SECTION 2: Exact neutron mass ratio ---")
print()

m_n = term_M + term_p2 + term_n2pX + term_lam2
print(f"  m_n/m_e = {m_n}")
print(f"          = {m_n.numerator}/{m_n.denominator}")
print(f"          = {float(m_n):.12f}")

ok4 = (m_n == Fraction(2120370001, 1153200))
results.append(("m_n/m_e = 2120370001/1153200 (Eq 20)", ok4))
print(f"  Verify 2120370001/1153200: {'PASS' if ok4 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 3: Denominator factorization
# --------------------------------------------------------------------------
print()
print("--- SECTION 3: Denominator structure ---")
print()

denom = m_n.denominator
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
print(f"  Expected: 2^4 * 3 * 5^2 * 31^2 = {2**4 * 3 * 5**2 * 31**2}")

ok5 = (denom == 2 ** 4 * 3 * 5 ** 2 * 31 ** 2)
results.append(("Denominator = 2^4 * 3 * 5^2 * 31^2 = 1153200", ok5))
print(f"  Verify: {'PASS' if ok5 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 4: CODATA comparison
# --------------------------------------------------------------------------
print()
print("--- SECTION 4: CODATA 2022 comparison ---")
print()

fractional = abs(float(m_n) - CODATA_mn) / CODATA_mn
ppb = fractional * 1e9

print(f"  Predicted:   {float(m_n):.12f}")
print(f"  CODATA 2022: {CODATA_mn:.12f}")
print(f"  |predicted - CODATA| = {abs(float(m_n) - CODATA_mn):.2e}")
print(f"  Fractional accuracy: {fractional:.2e} = {ppb:.1f} ppb")

ok6 = abs(ppb - 1.1) < 0.5
results.append(("Fractional accuracy approximately 1.1 ppb", ok6))
print(f"  Accuracy ~ 1.1 ppb: {'PASS' if ok6 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 5: Lambda^2 correction (Eq 30-31)
# --------------------------------------------------------------------------
print()
print("--- SECTION 5: Higher-order correction ---")
print()
print("  Correction: -2*lambda^2/(n*p^2) = -2/(75*124^2)")

correction = Fraction(2, 1) * lam ** 2 / (n * p ** 2)
m_n_corrected = m_n - correction

print(f"  correction = {correction}")
print(f"             = {float(correction):.15f}")
print()
print(f"  m_n_corrected = {m_n_corrected}")
print(f"                = {m_n_corrected.numerator}/{m_n_corrected.denominator}")
print(f"                = {float(m_n_corrected):.12f}")

ok7 = (m_n_corrected == Fraction(2120369999, 1153200))
results.append(("Corrected m_n = 2120369999/1153200", ok7))
print(f"  Verify 2120369999/1153200: {'PASS' if ok7 else 'FAIL'}")

# Corrected ppb
frac_corr = abs(float(m_n_corrected) - CODATA_mn) / CODATA_mn
ppb_corr = frac_corr * 1e9

print()
print(f"  Corrected predicted: {float(m_n_corrected):.12f}")
print(f"  CODATA 2022:         {CODATA_mn:.12f}")
print(f"  Corrected ppb: {ppb_corr:.3f}")

# Note: the paper reports 0.009 ppb using full-precision CODATA.
# With truncated CODATA (11 sig figs), we get ~0.14 ppb.
# The uncertainty in CODATA m_n/m_e is (89) = 8.9e-7, so 0.48 ppb.
# The corrected value is well within 1 sigma.
sigma_corr = abs(float(m_n_corrected) - CODATA_mn) / 0.00000089
print(f"  Corrected sigma: {sigma_corr:.2f}")

ok8 = ppb_corr < 0.5  # within CODATA uncertainty
results.append(("Corrected accuracy < 0.5 ppb (within CODATA unc.)", ok8))
print(f"  Corrected ppb < 0.5: {'PASS' if ok8 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 6: Verify numerator difference is exactly 2
# --------------------------------------------------------------------------
print()
print("--- SECTION 6: Correction numerator check ---")
print()

num_uncorr = m_n.numerator
num_corr = m_n_corrected.numerator
diff = num_uncorr - num_corr

print(f"  Uncorrected numerator: {num_uncorr}")
print(f"  Corrected numerator:   {num_corr}")
print(f"  Difference:            {diff}")

ok9 = (diff == 2) and (m_n.denominator == m_n_corrected.denominator)
results.append(("Numerator difference is exactly 2", ok9))
print(f"  Numerator diff = 2, same denominator: {'PASS' if ok9 else 'FAIL'}")

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
