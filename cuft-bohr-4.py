#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-4.py — Exact Gamma_classical = 24.84

Implements the gain-coherence equation |f_0'(x_u)|^n = Gamma
and solves for Gamma_classical numerically for n=3.
Verifies Gamma_classical = 24.84 and sqrt(24.84) = 4.984, round to 5.

The gain-coherence is solved PRE-QUANTIZATION (lambda = 0):
  f_0(x) = Gamma * tanh^n(x)
  Fixed point: Gamma * tanh^n(x_u) = x_u
  Condition: |f_0'(x_u)|^n = Gamma
"""

import math
import numpy as np
from scipy.optimize import brentq

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-4: Exact Gamma_classical = 24.84")
print("=" * 72)

results = []

# ============================================================================
# THE GAIN-COHERENCE EQUATION
# ============================================================================
print("\n--- The gain-coherence equation ---")
print("At the unstable fixed point x_u of the undamped map")
print("  f_0(x) = Gamma * tanh^n(x)")
print("the gain per iteration is |f_0'(x_u)|.")
print("The gain-coherence condition requires n iterations of the")
print("linearized map to reproduce the total gain:")
print()
print("    |f_0'(x_u)|^n = Gamma                                      (2)")
print()
print("This is solved pre-quantization (lambda = 0). The damping lambda")
print("is determined AFTER quantization in Step 3.")

# ============================================================================
# SECTION 1: Self-consistent solution for n=3
# ============================================================================
print("\n--- SECTION 1: Solve gain-coherence for n = 3 ---")

n = 3

def find_Gamma_classical(n_val):
    """Find Gamma_classical from the undamped gain-coherence equation.

    The undamped map: f_0(x) = Gamma * tanh^n(x)
    Fixed point: Gamma * tanh^n(x_u) = x_u
    Derivative: f_0'(x) = n * Gamma * tanh^(n-1)(x) * sech^2(x)
    Condition: f_0'(x_u)^n = Gamma

    For small x: f_0(x) ~ Gamma * x^n, fixed point at x ~ Gamma^(-1/(n-1))
    For large x: f_0(x) ~ Gamma, fixed point at x ~ Gamma
    The unstable fixed point x_u is the small one.
    """
    def residual(log_G):
        G = math.exp(log_G)
        if G < 1.01:
            return -1.0

        # g0(x) = G*tanh^n(x) - x
        # For small x: g0 ~ G*x^n - x = x*(G*x^(n-1) - 1) < 0
        # Rises, crosses zero at x_u, then tanh saturates and g0 -> G - x < 0
        def g0(x):
            return G * math.tanh(x)**n_val - x

        # Scan for the zero crossing (negative -> positive)
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
        fp_val = n_val * G * t**(n_val - 1) * sech2

        return fp_val**n_val - G

    log_G_sol = brentq(residual, math.log(20), math.log(30))
    return math.exp(log_G_sol)

Gamma_cl = find_Gamma_classical(n)

print(f"  n = {n}")
print(f"  Gamma_classical = {Gamma_cl:.6f}")

ok1 = abs(Gamma_cl - 24.84) < 0.01
results.append(("Gamma_classical = 24.84 (to 2 decimal places)", ok1))
print(f"  Expected: 24.84")
print(f"  {'PASS' if ok1 else 'FAIL'}")

# ============================================================================
# SECTION 2: Verify sqrt(Gamma_classical) and round to p = 5
# ============================================================================
print("\n--- SECTION 2: sqrt(Gamma_classical) -> p = 5 ---")

sqrt_Gamma = math.sqrt(Gamma_cl)
p_rounded = round(sqrt_Gamma)

print(f"  sqrt({Gamma_cl:.4f}) = {sqrt_Gamma:.6f}")
print(f"  round({sqrt_Gamma:.6f}) = {p_rounded}")

ok2 = abs(sqrt_Gamma - 4.984) < 0.01
results.append(("sqrt(24.84) ~ 4.984", ok2))
print(f"  sqrt(Gamma_cl) ~ 4.984: {'PASS' if ok2 else 'FAIL'}")

ok3 = (p_rounded == 5)
results.append(("round(sqrt(Gamma_cl)) = 5", ok3))
print(f"  p = round(sqrt(Gamma_cl)) = {p_rounded}: {'PASS' if ok3 else 'FAIL'}")

# ============================================================================
# SECTION 3: Verify the gain-coherence condition holds
# ============================================================================
print("\n--- SECTION 3: Verify gain-coherence at Gamma_classical ---")

def g0_cl(x):
    return Gamma_cl * math.tanh(x)**n - x

# Find x_u
xs = np.linspace(0.001, 5.0, 2000)
gs = np.array([g0_cl(x) for x in xs])
for i in range(len(gs) - 1):
    if gs[i] < 0 and gs[i + 1] > 0:
        x_u_cl = brentq(g0_cl, xs[i], xs[i + 1])
        break

print(f"  x_u = {x_u_cl:.10f}")

t_u = math.tanh(x_u_cl)
sech2_u = 1.0 - t_u**2
fp_u = n * Gamma_cl * t_u**(n - 1) * sech2_u
print(f"  f_0'(x_u) = {fp_u:.10f}")
print(f"  |f_0'(x_u)|^n = {abs(fp_u)**n:.10f}")
print(f"  Gamma_cl       = {Gamma_cl:.10f}")

ok4 = abs(abs(fp_u)**n - Gamma_cl) < 1e-6
results.append(("|f_0'(x_u)|^n = Gamma_classical (gain-coherence)", ok4))
print(f"  {'PASS' if ok4 else 'FAIL'}")

# ============================================================================
# SECTION 4: Show the Bohr quantization step
# ============================================================================
print("\n--- SECTION 4: The Bohr quantization step ---")
print(f"  Gamma_classical = {Gamma_cl:.4f} (continuous, not a perfect square)")
print(f"  sqrt(Gamma_cl)  = {sqrt_Gamma:.6f} (not an integer)")
print(f"  p = round(sqrt(Gamma_cl)) = {p_rounded} (Bohr quantization)")
print(f"  Gamma = p^2 = {p_rounded**2} (quantized)")
print(f"  lambda = 1/(p^3-1) = 1/{p_rounded**3 - 1} (quantized)")
print()
print(f"  The 'Bohr step' discretizes the continuous Gamma_classical = {Gamma_cl:.4f}")
print(f"  to the integer square Gamma = {p_rounded**2}, analogous to Bohr's")
print(f"  quantization of angular momentum.")

ok5 = (p_rounded**2 == 25)
results.append(("Gamma = p^2 = 25 (quantized)", ok5))
print(f"  {'PASS' if ok5 else 'FAIL'}")

# ============================================================================
# SECTION 5: Quantization basin
# ============================================================================
print("\n--- SECTION 5: Quantization basin ---")
lo = (p_rounded - 0.5)**2
hi = (p_rounded + 0.5)**2
print(f"  For p = {p_rounded}, the quantization basin is:")
print(f"    (p - 0.5)^2 < Gamma < (p + 0.5)^2")
print(f"    {lo} < Gamma < {hi}")
print(f"  Gamma_classical = {Gamma_cl:.4f} is in [{lo}, {hi}]")

ok6 = (lo < Gamma_cl < hi)
results.append(("Gamma_cl in p=5 quantization basin [20.25, 30.25]", ok6))
print(f"  {'PASS' if ok6 else 'FAIL'}")

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
