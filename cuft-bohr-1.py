#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-1.py — Coherent energy, Diophantine discovery

Verifies the Diophantine equation (n-2)(p-1) = 4, enumerates its three
integer solutions, and computes M(n,p) for each, showing that (3,5)
matches the proton-to-electron mass ratio.
"""

from fractions import Fraction
import math

# ============================================================================
# PARAMETERS
# ============================================================================

def mass_formula(n, p):
    """Compute M(n,p) = X^2/2 + (n/p)*X + n^2/X + lambda/n
    using exact Fraction arithmetic."""
    n = Fraction(n)
    p = Fraction(p)
    X = n * p * (p - 1)
    lam = Fraction(1, int(p**3 - 1))
    M = X**2 / 2 + (n / p) * X + n**2 / X + lam / n
    return M, X, lam

def f(x, Gamma, lam, n):
    """f(x) = Gamma * tanh^n(x) - lambda * x"""
    return Gamma * math.tanh(x)**n - lam * x

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-1: Coherent energy, Diophantine discovery")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: Define the recursion f(x) = Gamma * tanh^n(x) - lambda * x
# --------------------------------------------------------------------------
print("\n--- SECTION 1: The gated cubic recursion ---")
print("f(x) = Gamma * tanh^n(x) - lambda * x")
print()

# For (n,p) = (3,5):
n_val, p_val = 3, 5
Gamma = p_val**2  # = 25
lam = 1.0 / (p_val**3 - 1)  # = 1/124

print(f"For (n,p) = ({n_val},{p_val}): Gamma = {Gamma}, lambda = 1/{p_val**3-1} = {lam:.10f}")
print()

# Demonstrate fixed points by finding where f(x) = x, i.e. g(x) = f(x) - x = 0
print("Fixed points satisfy f(x) = x, i.e. Gamma*tanh^n(x) - lambda*x = x")
print("Equivalently: Gamma*tanh^n(x) = (1 + lambda)*x")
print()

# Find the three fixed points numerically
from scipy.optimize import brentq

def g(x, Gamma_v, lam_v, n_v):
    return f(x, Gamma_v, lam_v, n_v) - x

# x = 0 is trivial
x0 = 0.0
print(f"  Trivial fixed point: x_0 = {x0}")

# Unstable fixed point x_u (small positive)
x_u = brentq(lambda x: g(x, Gamma, lam, n_val), 0.01, 3.0)
print(f"  Unstable fixed point: x_u = {x_u:.10f}")

# Stable fixed point x_s (large positive)
x_s = brentq(lambda x: g(x, Gamma, lam, n_val), 10.0, 30.0)
print(f"  Stable fixed point:  x_s = {x_s:.10f}")

check_fp = abs(g(x_s, Gamma, lam, n_val)) < 1e-12
print(f"  Verify f(x_s) = x_s: residual = {abs(g(x_s, Gamma, lam, n_val)):.2e}")
ok1 = check_fp
results.append(("Fixed points found for (3,5)", ok1))
print(f"  PASS" if ok1 else f"  FAIL")

# --------------------------------------------------------------------------
# SECTION 2: The Diophantine equation (n-2)(p-1) = 4
# --------------------------------------------------------------------------
print("\n--- SECTION 2: Diophantine equation (n-2)(p-1) = 4 ---")
print()
print("For the virial relation c_2 = 1/2 to hold, the Diophantine")
print("equation (n-2)(p-1) = 4 must be satisfied.")
print()

# Enumerate all integer solutions with n >= 3, p >= 2
solutions = []
for n_try in range(3, 100):
    for p_try in range(2, 100):
        if (n_try - 2) * (p_try - 1) == 4:
            solutions.append((n_try, p_try))

print("Integer solutions with n >= 3, p >= 2:")
print(f"{'n':>4} {'p':>4} {'(n-2)(p-1)':>12}")
print("-" * 24)
for n_s, p_s in solutions:
    val = (n_s - 2) * (p_s - 1)
    print(f"{n_s:>4} {p_s:>4} {val:>12}")

ok2 = (solutions == [(3, 5), (4, 3), (6, 2)])
results.append(("Three Diophantine solutions: (3,5),(4,3),(6,2)", ok2))
print(f"\n  Expected: (3,5), (4,3), (6,2)")
print(f"  Found:    {solutions}")
print(f"  {'PASS' if ok2 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 3: Mass formula M(n,p) for each solution
# --------------------------------------------------------------------------
print("\n--- SECTION 3: Mass formula M(n,p) for each solution ---")
print()
print("M = X^2/2 + (n/p)*X + n^2/X + lambda/n")
print(f"where X = n*p*(p-1), lambda = 1/(p^3-1)")
print()

CODATA_mu = 1836.152673426  # CODATA 2022 proton-to-electron mass ratio

print(f"{'(n,p)':>8} {'Gamma':>6} {'X':>5} {'M (exact fraction)':>25} {'M (decimal)':>16} {'Match?':>8}")
print("-" * 72)

proton_match = False
for n_s, p_s in solutions:
    M, X, lam_val = mass_formula(n_s, p_s)
    Gamma_s = p_s**2
    M_float = float(M)
    match = "proton" if abs(M_float - CODATA_mu) / CODATA_mu < 1e-6 else ""
    if match:
        proton_match = True
    print(f"({n_s},{p_s}){Gamma_s:>6}{int(X):>6}   {str(M):>22}   {M_float:>14.6f} {match:>8}")

ok3 = proton_match
results.append(("(3,5) matches proton mass ratio", ok3))
print(f"\n  (3,5) matches CODATA mu = {CODATA_mu}: {'PASS' if ok3 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 4: Verify (3,5) mass formula value
# --------------------------------------------------------------------------
print("\n--- SECTION 4: Exact (3,5) mass formula ---")
M35, X35, lam35 = mass_formula(3, 5)
print(f"  M = {M35}")
print(f"  M = {M35.numerator}/{M35.denominator}")
print(f"  M = {float(M35):.12f}")
print(f"  CODATA mu = {CODATA_mu:.12f}")

frac_acc = abs(float(M35) - CODATA_mu) / CODATA_mu
print(f"  Fractional accuracy: {frac_acc:.1e} = {frac_acc*1e9:.1f} ppb")

ok4 = (M35 == Fraction(853811, 465))
results.append(("M = 853811/465 exactly", ok4))
print(f"  M = 853811/465: {'PASS' if ok4 else 'FAIL'}")

ok5 = abs(frac_acc - 8.0e-9) < 2e-9
results.append(("Fractional accuracy ~ 8 ppb", ok5))
print(f"  Accuracy ~ 8 ppb: {'PASS' if ok5 else 'FAIL'}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 72)
print("SUMMARY")
print("=" * 72)
passed = sum(1 for _, ok in results)
total = len(results)
for desc, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")
passed = sum(1 for _, ok in results if ok)
print(f"\n  {passed}/{total} checks passed.")
if passed == total:
    print("  ALL CHECKS PASSED.")
else:
    print(f"  WARNING: {total - passed} check(s) FAILED.")
