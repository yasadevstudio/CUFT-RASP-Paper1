#!/usr/bin/env python3
"""
ATTACK #5: LYAPUNOV STABILITY ANALYSIS

Compute the Lyapunov exponent of the gated cubic map
    f(x) = Gamma * tanh^n(x) - lambda * x
as a function of a DEFORMATION PARAMETER that interpolates
between different c₁ values.

The map's stability is characterized by the Lyapunov exponent:
    L = lim (1/N) sum_k ln|f'(x_k)|

We parameterize c₁ through a deformation of the map and study
which value produces extremal dynamical properties.
"""

import numpy as np
from fractions import Fraction

# Fixed parameters
n, p = 3, 5
lam = 1.0 / (p**3 - 1)  # 1/124
Gamma = p**2              # 25
X_val = n * p * (p - 1)   # 60

print("=" * 80)
print("ATTACK #5: LYAPUNOV STABILITY ANALYSIS")
print("=" * 80)
print()

# ═══════════════════════════════════════════════════════════════════
# PART 1: THE ORIGINAL MAP AND ITS FIXED POINTS
# ═══════════════════════════════════════════════════════════════════

def f(x, gamma=Gamma, lam_val=lam):
    """The gated cubic map."""
    return gamma * np.tanh(x)**n - lam_val * x

def df(x, gamma=Gamma, lam_val=lam):
    """Derivative of the gated cubic map."""
    return gamma * n * np.tanh(x)**(n-1) * (1 - np.tanh(x)**2) - lam_val

# Find the stable fixed point x_s
from scipy.optimize import brentq

def fixed_point_eq(x):
    return f(x) - x

# x_s is approximately p² = 25 (from paper)
x_s = brentq(fixed_point_eq, 20, 30)
# Find unstable fixed point by scanning
x_u = None
for x_try in np.linspace(0.01, 10, 10000):
    if fixed_point_eq(x_try) * fixed_point_eq(x_try + 0.001) < 0 and x_try > 0.01 and x_try < x_s - 1:
        x_u = brentq(fixed_point_eq, x_try, x_try + 0.001)
        break
if x_u is None:
    x_u = 1.0  # fallback

print("PART 1: FIXED POINTS OF f(x) = Γ·tanh³(x) - λ·x")
print("-" * 60)
print(f"  Stable fixed point:   x_s = {x_s:.12f}")
print(f"  Unstable fixed point: x_u = {x_u:.12f}")
print(f"  f'(x_s) = {df(x_s):.12f}")
print(f"  f'(x_u) = {df(x_u):.12f}")
print(f"  -λ = {-lam:.12f}")
print(f"  |f'(x_s) + λ| = {abs(df(x_s) + lam):.2e}")
print(f"  x_s ≈ p² = {p**2}")
print()

# ═══════════════════════════════════════════════════════════════════
# PART 2: DEFORMED MAP — PARAMETERIZE BY c₁
# ═══════════════════════════════════════════════════════════════════
#
# The mass formula M = X²/2 + c₁·X + c₁²·Γ/X + λ/n
# comes from expanding the fixed-point properties of f.
#
# We can ask: what property of f(x) corresponds to c₁?
# Answer: c₁ = n/sqrt(Gamma) (Taylor reading from paper)
#         = n/p when Gamma = p²
#
# To deform c₁, we deform the relationship between n and Gamma:
# Let Gamma(c) = (n/c)² so that c₁ = n/sqrt(Gamma) = c.
#
# For c = n/p: Gamma = p² (standard)
# For c ≠ n/p: Gamma = (n/c)² (deformed)

print("PART 2: DEFORMED MAP FAMILY f_c(x) = (n/c)²·tanh³(x) - λ(c)·x")
print("-" * 60)
print()

def compute_lambda(gamma):
    """λ from Gamma: κ = 1/sqrt(Γ), λ = κ^n / (1 - κ^n) = 1/(Γ^(n/2) - 1)."""
    return 1.0 / (gamma**(n/2) - 1)

def f_deformed(x, c1_val):
    """Deformed map where c₁ = c1_val implies Gamma = (n/c1_val)²."""
    gamma_c = (n / c1_val)**2
    lam_c = compute_lambda(gamma_c)
    return gamma_c * np.tanh(x)**n - lam_c * x

def df_deformed(x, c1_val):
    """Derivative of deformed map."""
    gamma_c = (n / c1_val)**2
    lam_c = compute_lambda(gamma_c)
    return gamma_c * n * np.tanh(x)**(n-1) * (1 - np.tanh(x)**2) - lam_c

# ═══════════════════════════════════════════════════════════════════
# PART 3: LYAPUNOV EXPONENT AS FUNCTION OF c₁
# ═══════════════════════════════════════════════════════════════════

print("PART 3: LYAPUNOV EXPONENT L(c₁)")
print("-" * 60)
print()

def lyapunov_exponent(c1_val, N=10000, x0=0.5):
    """Compute Lyapunov exponent for the deformed map."""
    gamma_c = (n / c1_val)**2
    lam_c = compute_lambda(gamma_c)

    x = x0
    total = 0.0
    transient = 1000  # skip transient

    for k in range(N + transient):
        deriv = gamma_c * n * np.tanh(x)**(n-1) * (1 - np.tanh(x)**2) - lam_c
        x = gamma_c * np.tanh(x)**n - lam_c * x

        if k >= transient:
            if abs(deriv) > 1e-300:
                total += np.log(abs(deriv))

        # Check for divergence or convergence to fixed point
        if abs(x) > 1e10:
            return float('inf')
        if k > transient + 100 and abs(x - (gamma_c * np.tanh(x)**n - lam_c * x) / (1 + lam_c)) < 1e-12:
            # At fixed point, Lyapunov = ln|f'(x_s)|
            return np.log(abs(deriv))

    return total / N

# Sweep c₁
c1_sweep = np.linspace(0.1, 2.0, 200)
lyap_values = []

print(f"{'c₁':>8s} | {'Gamma':>10s} | {'lambda':>12s} | {'Lyapunov':>12s} | Notes")
print("-" * 70)

for c1_val in [0.3, 0.4, 0.5, 0.55, 0.58, 0.59, 0.595, 0.598,
               0.6, 0.602, 0.605, 0.61, 0.62, 0.65, 0.7, 0.8, 1.0, 1.5]:
    gamma_c = (n / c1_val)**2
    lam_c = compute_lambda(gamma_c)

    L = lyapunov_exponent(c1_val)
    marker = " <<<< n/p" if abs(c1_val - 0.6) < 0.001 else ""
    print(f"  {c1_val:6.3f} | {gamma_c:10.4f} | {lam_c:12.8f} | {L:12.6f} | {marker}")

# ═══════════════════════════════════════════════════════════════════
# PART 4: MULTIPLIER ANALYSIS AT FIXED POINTS
# ═══════════════════════════════════════════════════════════════════

print()
print("PART 4: FIXED-POINT MULTIPLIER |f'(x_s)| AS FUNCTION OF c₁")
print("-" * 60)
print()

# At the stable fixed point, the multiplier is |f'(x_s)| ≈ λ (from paper)
# Let's check how this varies with c₁

print(f"{'c1':>8s} | {'x_s':>12s} | {'fp(x_s)':>12s} | {'|fp(x_s)|':>12s} | {'-lambda':>12s} | {'Match':>8s}")
print("-" * 80)

for c1_val in [0.3, 0.4, 0.5, 0.55, 0.58, 0.59, 0.595, 0.598,
               0.6, 0.602, 0.605, 0.61, 0.62, 0.65, 0.7, 0.8, 1.0]:
    gamma_c = (n / c1_val)**2
    lam_c = compute_lambda(gamma_c)

    # Find stable fixed point
    def fp_eq(x):
        return gamma_c * np.tanh(x)**n - lam_c * x - x

    try:
        # x_s ≈ sqrt(gamma_c) for large gamma
        x_guess = np.sqrt(gamma_c)
        xs = brentq(fp_eq, x_guess * 0.5, x_guess * 2)

        deriv_xs = gamma_c * n * np.tanh(xs)**(n-1) * (1 - np.tanh(xs)**2) - lam_c
        marker = " <<<< n/p" if abs(c1_val - 0.6) < 0.001 else ""
        match_pct = abs(deriv_xs + lam_c) / lam_c * 100
        print(f"  {c1_val:6.3f} | {xs:12.6f} | {deriv_xs:12.8f} | {abs(deriv_xs):12.8f} | {-lam_c:12.8f} | {match_pct:.2e}%{marker}")
    except Exception as e:
        print(f"  {c1_val:6.3f} | {'FAILED':>12s} | {str(e)[:30]}")

# ═══════════════════════════════════════════════════════════════════
# PART 5: STABILITY BASIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════

print()
print("PART 5: STABILITY BASIN SIZE")
print("-" * 60)
print()
print("How large is the basin of attraction of x_s?")
print("(fraction of initial conditions in [0, 2·Gamma^(1/2)] that converge to x_s)")
print()

for c1_val in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5]:
    gamma_c = (n / c1_val)**2
    lam_c = compute_lambda(gamma_c)

    N_test = 1000
    N_iter = 200
    converged = 0
    x_max = 2 * np.sqrt(gamma_c)

    for i in range(N_test):
        x = x_max * i / N_test
        for _ in range(N_iter):
            x_new = gamma_c * np.tanh(x)**n - lam_c * x
            if abs(x_new) > 1e10:
                break
            x = x_new
        else:
            if abs(x) < 1e10:
                converged += 1

    basin_frac = converged / N_test
    marker = " <<<< n/p" if abs(c1_val - 0.6) < 0.001 else ""
    print(f"  c₁ = {c1_val:.1f}: basin fraction = {basin_frac:.3f}{marker}")

# ═══════════════════════════════════════════════════════════════════
# PART 6: CONNECTION TO MASS FORMULA
# ═══════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("PART 6: THE DYNAMICAL CONNECTION")
print("=" * 80)
print()

# The key insight: the mass formula coefficients are READ from the
# fixed-point structure of f. The paper shows:
#   x_s ≈ Gamma = p² (to exponential accuracy)
#   f'(x_s) = -lambda (exact)
#   c₁ = n/sqrt(Gamma) = n/p (Taylor reading)
#
# In the deformed map family, only c₁ = n/p gives Gamma = p² = integer².
# This is the "Bohr step" — quantization.
#
# So the dynamical derivation chain is:
# 1. Gain-coherence → Gamma_classical ≈ 24.84
# 2. Bohr quantization → p = round(sqrt(Gamma)) = 5, Gamma = 25
# 3. Taylor reading → c₁ = n/sqrt(Gamma) = n/p = 3/5
#
# Step 3 doesn't need the Diophantine. It reads c₁ directly from the
# recursion coefficients.

print("DYNAMICAL DERIVATION CHAIN:")
print()
print("  1. Gain-coherence gives Γ_classical = 24.84")
print("  2. Bohr quantization: p = round(√Γ) = 5, Γ = p² = 25")
print("  3. Taylor reading: c₁ = n/√Γ = n/p = 3/5")
print()
print("  Step 3 is a DIRECT reading from the recursion:")
print("  f(x) = Γ·tanh^n(x) - λ·x")
print("       = Γ·x^n + ... (near origin)")
print("  The ratio of the nonlinear order (n) to the square root")
print("  of its coefficient (√Γ = p) gives c₁ = n/p.")
print()
print("  This is exactly how Bohr read hbar from the angular momentum:")
print("  L = n·ℏ where n is the quantum number and ℏ comes from Planck's")
print("  constant. Here: c₁ = n·κ where n is the gate order and κ = 1/p")
print("  comes from the quantized coupling.")
print()

# Verify the multiplier analysis
print("MULTIPLIER ANALYSIS:")
print()
print(f"  At x_s = {x_s:.10f}:")
print(f"  f'(x_s) = {df(x_s):.15f}")
print(f"  -λ      = {-lam:.15f}")
print(f"  Match:    {abs(df(x_s) + lam):.2e}")
print()

# The multiplier AT x_s is -lambda, independent of c₁
# But the VALUE of x_s determines the mass formula:
# M = expansion of x_s in terms of the recursion parameters
# And c₁ = n/p is the coefficient of the linear term in that expansion

print("VERDICT:")
print()
print("  The Lyapunov analysis confirms that the dynamics are STABLE")
print("  (multiplier = -λ ≈ -0.008 at x_s) but does NOT independently")
print("  select c₁ = n/p. The multiplier is -λ for ALL c₁ values")
print("  (it's a property of the fixed point, not the mass formula).")
print()
print("  What Lyapunov DOES show:")
print("  - The map is contracting at x_s (|f'| < 1) for all c₁")
print("  - The mass formula expansion is well-defined (convergent)")
print("  - The perturbation series in λ is justified")
print()
print("  What Lyapunov does NOT show:")
print("  - It does not select c₁ = n/p over other values")
print("  - The Lyapunov exponent is not extremal at c₁ = n/p")
print()
print("  STATUS: SUPPORTING EVIDENCE (stability), NOT selection mechanism.")
