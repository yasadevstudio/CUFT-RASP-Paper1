#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-3.py — Coupling constant kappa

Verifies the coupling constant identities:
  kappa = 1/p = 1/5
  kappa = lambda * x_s
  kappa^n = lambda/(1+lambda) = 1/p^n = 1/125
  x_s = p^2/(1+lambda) = Gamma/(1+lambda)
"""

from fractions import Fraction
import math
from scipy.optimize import brentq

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-3: Coupling constant kappa")
print("=" * 72)

results = []

# ============================================================================
# PARAMETERS (exact rational)
# ============================================================================
n = 3
p = 5
Gamma_exact = Fraction(p**2)         # 25
lam_exact = Fraction(1, p**3 - 1)    # 1/124
kappa_exact = Fraction(1, p)          # 1/5

print(f"\nParameters: n = {n}, p = {p}")
print(f"  Gamma = {Gamma_exact}")
print(f"  lambda = {lam_exact}")
print(f"  kappa = 1/p = {kappa_exact}")

# ============================================================================
# Numerically find x_s for cross-checking
# ============================================================================
Gamma_f = float(Gamma_exact)
lam_f = float(lam_exact)

def g(x):
    return Gamma_f * math.tanh(x)**n - lam_f * x - x

x_s_num = brentq(g, 10.0, 30.0)
print(f"\n  x_s (numerical) = {x_s_num:.12f}")

# ============================================================================
# SECTION 1: kappa = 1/p = 1/5
# ============================================================================
print("\n--- SECTION 1: kappa = 1/p ---")
print(f"  kappa = 1/p = 1/{p} = {kappa_exact}")
print(f"  kappa (decimal) = {float(kappa_exact):.10f}")

ok1 = (kappa_exact == Fraction(1, 5))
results.append(("kappa = 1/5", ok1))
print(f"  {'PASS' if ok1 else 'FAIL'}")

# ============================================================================
# SECTION 2: kappa = lambda * x_s
# ============================================================================
print("\n--- SECTION 2: kappa = lambda * x_s ---")

# Exact: x_s = Gamma/(1+lambda) = p^2 / (1 + 1/(p^3-1)) = p^2 * (p^3-1) / p^3
#       = p^2 * (p^3-1) / p^3
x_s_exact = Gamma_exact / (1 + lam_exact)
print(f"  x_s (exact) = Gamma/(1+lambda) = {x_s_exact}")
print(f"  x_s (exact decimal) = {float(x_s_exact):.12f}")
print(f"  x_s (numerical)     = {x_s_num:.12f}")

kappa_check = lam_exact * x_s_exact
print(f"\n  lambda * x_s = {lam_exact} * {x_s_exact}")
print(f"              = {kappa_check}")
print(f"  kappa        = {kappa_exact}")

ok2 = (kappa_check == kappa_exact)
results.append(("kappa = lambda * x_s", ok2))
print(f"  {'PASS' if ok2 else 'FAIL'}")

# ============================================================================
# SECTION 3: kappa^n = lambda/(1+lambda) = 1/p^n = 1/125
# ============================================================================
print("\n--- SECTION 3: kappa^n = lambda/(1+lambda) = 1/p^n ---")

kappa_n = kappa_exact ** n
lam_over_1plam = lam_exact / (1 + lam_exact)
one_over_pn = Fraction(1, p**n)

print(f"  kappa^n         = (1/{p})^{n} = {kappa_n}")
print(f"  lambda/(1+lam)  = {lam_exact}/({1 + lam_exact}) = {lam_over_1plam}")
print(f"  1/p^n           = 1/{p**n} = {one_over_pn}")

ok3a = (kappa_n == lam_over_1plam)
ok3b = (kappa_n == one_over_pn)
ok3c = (lam_over_1plam == one_over_pn)

results.append(("kappa^n = lambda/(1+lambda)", ok3a))
results.append(("kappa^n = 1/p^n", ok3b))
results.append(("lambda/(1+lambda) = 1/p^n", ok3c))

print(f"  kappa^n = lambda/(1+lambda): {'PASS' if ok3a else 'FAIL'}")
print(f"  kappa^n = 1/p^n:             {'PASS' if ok3b else 'FAIL'}")
print(f"  lambda/(1+lambda) = 1/p^n:   {'PASS' if ok3c else 'FAIL'}")

# Show the chain
print(f"\n  Verification chain:")
print(f"  kappa^n         = {kappa_n} = {float(kappa_n):.10f}")
print(f"  lambda/(1+lam)  = {lam_over_1plam} = {float(lam_over_1plam):.10f}")
print(f"  1/p^n           = {one_over_pn} = {float(one_over_pn):.10f}")
print(f"  All three are identical: {'PASS' if ok3a and ok3b and ok3c else 'FAIL'}")

# ============================================================================
# SECTION 4: x_s = p^2/(1+lambda) = Gamma/(1+lambda)
# ============================================================================
print("\n--- SECTION 4: x_s = p^2/(1+lambda) = Gamma/(1+lambda) ---")

x_s_from_p = Fraction(p**2) / (1 + lam_exact)
x_s_from_Gamma = Gamma_exact / (1 + lam_exact)

print(f"  p^2/(1+lambda)     = {p**2}/({1 + lam_exact}) = {x_s_from_p}")
print(f"  Gamma/(1+lambda)   = {Gamma_exact}/({1 + lam_exact}) = {x_s_from_Gamma}")
print(f"  These are equal (p^2 = Gamma): {x_s_from_p == x_s_from_Gamma}")

ok4a = (x_s_from_p == x_s_from_Gamma)
results.append(("p^2/(1+lambda) = Gamma/(1+lambda)", ok4a))
print(f"  {'PASS' if ok4a else 'FAIL'}")

# Verify against numerical
print(f"\n  x_s (exact)     = {float(x_s_from_p):.12f}")
print(f"  x_s (numerical) = {x_s_num:.12f}")
print(f"  Difference: {abs(float(x_s_from_p) - x_s_num):.2e}")

ok4b = abs(float(x_s_from_p) - x_s_num) < 1e-8
results.append(("x_s exact matches numerical", ok4b))
print(f"  {'PASS' if ok4b else 'FAIL'}")

# Simplify the exact form
print(f"\n  Simplified: x_s = {x_s_from_p.numerator}/{x_s_from_p.denominator}")
# p^2 / (1 + 1/(p^3-1)) = p^2 / (p^3/(p^3-1)) = p^2 * (p^3-1)/p^3
#                        = (p^3-1)/p = (p^5 - p^2)/p^3
# Actually: p^2 * (p^3-1)/p^3 = (p^5 - p^2)/p^3
# For p=5: 25 * 124/125 = 3100/125 = 124/5
print(f"  = {x_s_from_p.numerator}/{x_s_from_p.denominator} = {float(x_s_from_p):.6f}")

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
