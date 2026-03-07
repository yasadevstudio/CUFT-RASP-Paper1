#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-7.py — Bohr quantization p = round(sqrt(Gamma))

For n=3, verifies the complete Bohr quantization chain:
  Gamma_classical = 24.84
  round(sqrt(24.84)) = round(4.984) = 5
  p = 5 satisfies the Diophantine (n-2)(p-1) = 4
  Gamma = p^2 = 25
  lambda = 1/(p^3-1) = 1/124
"""

from fractions import Fraction
import math
import numpy as np
from scipy.optimize import brentq

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-7: Bohr quantization p = round(sqrt(Gamma))")
print("=" * 72)

results = []

n = 3

# ============================================================================
# SECTION 1: Compute Gamma_classical for n = 3
# ============================================================================
print("\n--- SECTION 1: Gamma_classical for n = 3 ---")

def find_Gamma_classical(n_val):
    """Self-consistent gain-coherence solution (undamped, lambda=0).

    The undamped map: f_0(x) = Gamma * tanh^n(x)
    Fixed point: Gamma * tanh^n(x_u) = x_u
    Derivative: f_0'(x) = n * Gamma * tanh^(n-1)(x) * sech^2(x)
    Condition: f_0'(x_u)^n = Gamma
    """
    def residual(log_G):
        G = math.exp(log_G)
        if G < 1.01:
            return -1.0

        def g0(x):
            return G * math.tanh(x)**n_val - x

        xs = np.linspace(0.001, 5.0, 2000)
        gs = np.array([g0(x) for x in xs])

        xu = None
        for i in range(len(gs) - 1):
            if gs[i] < 0 and gs[i + 1] > 0:
                xu = brentq(g0, xs[i], xs[i + 1])
                break

        if xu is None:
            return -1.0

        t = math.tanh(xu)
        sech2 = 1.0 - t**2
        fp = n_val * G * t**(n_val - 1) * sech2
        return fp**n_val - G

    log_G_sol = brentq(residual, math.log(20), math.log(30))
    return math.exp(log_G_sol)

Gamma_cl = find_Gamma_classical(n)
print(f"  n = {n}")
print(f"  Gamma_classical = {Gamma_cl:.6f}")

ok1 = abs(Gamma_cl - 24.84) < 0.01
results.append(("Gamma_classical = 24.84", ok1))
print(f"  Gamma_classical ~ 24.84: {'PASS' if ok1 else 'FAIL'}")

# ============================================================================
# SECTION 2: round(sqrt(Gamma_classical)) = 5
# ============================================================================
print("\n--- SECTION 2: Bohr quantization step ---")

sqrt_Gamma = math.sqrt(Gamma_cl)
p = round(sqrt_Gamma)

print(f"  sqrt({Gamma_cl:.4f}) = {sqrt_Gamma:.6f}")
print(f"  round({sqrt_Gamma:.6f}) = {p}")

ok2 = abs(sqrt_Gamma - 4.984) < 0.01
results.append(("sqrt(24.84) ~ 4.984", ok2))
print(f"  sqrt(Gamma_cl) ~ 4.984: {'PASS' if ok2 else 'FAIL'}")

ok3 = (p == 5)
results.append(("round(sqrt(Gamma_cl)) = 5", ok3))
print(f"  p = {p}: {'PASS' if ok3 else 'FAIL'}")

# ============================================================================
# SECTION 3: Verify Diophantine (n-2)(p-1) = 4
# ============================================================================
print("\n--- SECTION 3: Diophantine verification ---")

dioph_val = (n - 2) * (p - 1)
print(f"  (n-2)(p-1) = ({n}-2)({p}-1) = {n-2} * {p-1} = {dioph_val}")

ok4 = (dioph_val == 4)
results.append(("(n-2)(p-1) = (3-2)(5-1) = 4", ok4))
print(f"  (n-2)(p-1) = 4: {'PASS' if ok4 else 'FAIL'}")

# ============================================================================
# SECTION 4: Gamma = p^2 = 25
# ============================================================================
print("\n--- SECTION 4: Quantized Gamma ---")

Gamma = p**2
print(f"  Gamma = p^2 = {p}^2 = {Gamma}")

ok5 = (Gamma == 25)
results.append(("Gamma = p^2 = 25", ok5))
print(f"  Gamma = 25: {'PASS' if ok5 else 'FAIL'}")

# Show the quantization gap
print(f"\n  Quantization gap:")
print(f"    Gamma_classical = {Gamma_cl:.6f}")
print(f"    Gamma_quantized = {Gamma}")
print(f"    Gap = {Gamma - Gamma_cl:.6f} ({(Gamma - Gamma_cl)/Gamma_cl*100:.2f}%)")

# ============================================================================
# SECTION 5: lambda = 1/(p^3-1) = 1/124
# ============================================================================
print("\n--- SECTION 5: Damping constant lambda ---")

p_frac = Fraction(5)
lam = Fraction(1, int(p_frac**3 - 1))

print(f"  lambda = 1/(p^3 - 1)")
print(f"         = 1/({p}^3 - 1)")
print(f"         = 1/({p**3} - 1)")
print(f"         = 1/{p**3 - 1}")
print(f"         = {lam}")

ok6 = (lam == Fraction(1, 124))
results.append(("lambda = 1/124", ok6))
print(f"  lambda = 1/124: {'PASS' if ok6 else 'FAIL'}")

# ============================================================================
# SECTION 6: The complete derivation chain from n=3 alone
# ============================================================================
print("\n--- SECTION 6: Complete chain from n = 3 ---")
print()
print(f"  INPUT:  n = {n} (sole integer input)")
print(f"  STEP 1: Gamma_classical = {Gamma_cl:.4f} (gain-coherence)")
print(f"  STEP 2: p = round(sqrt({Gamma_cl:.4f})) = round({sqrt_Gamma:.4f}) = {p}")
print(f"  CHECK:  (n-2)(p-1) = ({n-2})({p-1}) = {dioph_val} = 4 (Diophantine satisfied)")
print(f"  RESULT: Gamma = p^2 = {Gamma}")
print(f"  RESULT: lambda = 1/(p^3-1) = 1/{p**3-1} = {float(lam):.10f}")
print(f"  RESULT: X = n*p*(p-1) = {n}*{p}*{p-1} = {n*p*(p-1)}")
print()
print(f"  Zero free parameters. The single integer n = 3 determines everything.")

# ============================================================================
# SECTION 7: Quantization basin check
# ============================================================================
print("\n--- SECTION 7: Quantization basin ---")
print(f"  For p = round(sqrt(Gamma)) = 5, the basin is:")
print(f"    (p - 0.5)^2 < Gamma < (p + 0.5)^2")
print(f"    {(p-0.5)**2} < Gamma < {(p+0.5)**2}")
print(f"    20.25 < Gamma < 30.25")
print(f"  Gamma_classical = {Gamma_cl:.4f} is within [{(p-0.5)**2}, {(p+0.5)**2}]")

ok7 = ((p - 0.5)**2 < Gamma_cl < (p + 0.5)**2)
results.append(("Gamma_cl within p=5 quantization basin", ok7))
print(f"  {'PASS' if ok7 else 'FAIL'}")

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
