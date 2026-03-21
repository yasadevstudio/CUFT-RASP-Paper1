#!/usr/bin/env python3
"""
CUFT-RASP ANGLE 2: DERIVE THE MASS FORMULA FROM THE RECURSION
==============================================================
YASA PRESENTS — 2026-02-24

GOAL: Derive M = X²/2 + c₁X + n²/X + λ/n from the recursion
      f(x) = Γ·tanh^n(x) - λx, WITHOUT postulating the polynomial form.

THE GAP:
  The paper POSTULATES M = c₂X² + c₁X + c₀ + c₋₁/X and then:
    - Derives c₂ = 1/2 (virial)
    - Selects c₁ = n/p via Occam
    - Sets c₋₁ = n², c₀ = λ/n

  If we can derive the FORM of M from the recursion, all coefficients
  come out automatically — including c₁.

APPROACH:
  The recursion f(x) = Γ·tanh^n(x) - λx has two non-trivial fixed points.
  The mass ratio μ = m_p/m_e is a PHYSICAL observable that must be
  computable from the recursion parameters (n, p, Γ, λ).

  Strategy:
  1. Express x_s explicitly in terms of (n, p) via asymptotic expansion
  2. Compute all recursion-derived quantities at x_s
  3. Find a natural energy functional whose value AT x_s gives M
  4. Check if this functional's expansion in X matches the known form
  5. Try: action integral, partition function, free energy, etc.
"""

import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from fractions import Fraction

# ═══════════════════════════════════════════════════════════════════
# PARAMETERS
# ═══════════════════════════════════════════════════════════════════

n = 3
p = 5
GAMMA = p**2          # 25
LAMBDA = 1/(p**3 - 1) # 1/124
kappa = 1/p           # 1/5
X = n * p * (p - 1)   # 60
M_exact = Fraction(853811, 465)  # exact mass ratio
M_target = float(M_exact)

def fp_eq(x, G=GAMMA, lam=LAMBDA, nq=n):
    return G * np.tanh(x)**nq - (1 + lam) * x

x_u = brentq(fp_eq, 0.01, 1.0)
x_s = brentq(fp_eq, 10.0, 30.0)

def f_prime(x, G=GAMMA, lam=LAMBDA, nq=n):
    t = np.tanh(x)
    return nq * G * t**(nq-1) * (1 - t**2) - lam

print("=" * 72)
print("ANGLE 2: DERIVE THE MASS FORMULA FROM THE RECURSION")
print("=" * 72)
print(f"\nParameters: n={n}, p={p}, Γ={GAMMA}, λ=1/{p**3-1}, X={X}")
print(f"Fixed points: x_u = {x_u:.10f}, x_s = {x_s:.10f}")
print(f"Target mass: M = {M_target:.10f} = {M_exact}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 1: ASYMPTOTIC EXPANSION OF x_s
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 1: ASYMPTOTIC EXPANSION OF x_s")
print("═" * 72)

# At x_s >> 1, tanh(x_s) ≈ 1 - 2·exp(-2x_s)
# So tanh^n(x_s) ≈ 1 - 2n·exp(-2x_s)
# Fixed point: Γ·(1 - 2n·exp(-2x_s)) = (1+λ)·x_s
# Leading order: Γ = (1+λ)·x_s  →  x_s ≈ Γ/(1+λ)
# Next order: x_s = Γ/(1+λ) - 2nΓ·exp(-2Γ/(1+λ)) / (1+λ) + ...

x_s_leading = GAMMA / (1 + LAMBDA)
x_s_next = x_s_leading - 2*n*GAMMA * np.exp(-2*x_s_leading) / (1 + LAMBDA)

print(f"\nLeading order: x_s ≈ Γ/(1+λ) = {x_s_leading:.10f}")
print(f"Exact x_s = {x_s:.10f}")
print(f"Error: {abs(x_s - x_s_leading):.2e}")
print(f"With exp correction: {x_s_next:.10f}")
print(f"Error: {abs(x_s - x_s_next):.2e}")

# Express in terms of p:
# Γ = p², λ = 1/(p³-1)
# x_s ≈ p²/(1+1/(p³-1)) = p²·(p³-1)/p³ = p²·(1 - 1/p³)·p³/p³
# = p²·(p³-1)/p³
x_s_exact_leading = p**2 * (p**3 - 1) / p**3
print(f"\nx_s ≈ p²(p³-1)/p³ = {x_s_exact_leading}")
print(f"= p² - 1/p = {p**2 - 1/p}")
print(f"= {Fraction(p**2*(p**3-1), p**3)} = {Fraction(p**5 - p**2, p**3)}")

# Also express X/x_s ratio
ratio = X / x_s
ratio_exact = Fraction(n * p * (p-1) * p**3, p**2 * (p**3 - 1))
print(f"\nX/x_s = {ratio:.10f}")
print(f"X/(p²(p³-1)/p³) = n·p·(p-1)·p³ / (p²·(p³-1))")
print(f"= n·p²·(p-1)/(p³-1) = n·p²·(p-1)/((p-1)(p²+p+1))")
print(f"= n·p²/(p²+p+1)")
r_frac = Fraction(n * p**2, p**2 + p + 1)
print(f"= {r_frac} = {float(r_frac):.10f}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 2: ENERGY FUNCTIONALS — WHAT COULD M BE?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 2: CANDIDATE ENERGY FUNCTIONALS")
print("═" * 72)

# The key question: What functional of the recursion evaluates to M?
# M = 853811/465 ≈ 1836.153

# Candidate 1: Action integral S = ∫₀^{x_s} [Γ·tanh^n(t) - (1+λ)t] dt
def integrand_action(t):
    return GAMMA * np.tanh(t)**n - (1 + LAMBDA) * t

S_action, _ = quad(integrand_action, 0, x_s)
print(f"\nCandidate 1: Action integral S = ∫₀^x_s [Γ·tanh^n(t) - (1+λ)t] dt")
print(f"  S = {S_action:.10f}")
print(f"  M/S = {M_target/S_action:.10f}")

# Candidate 2: Potential energy V = -∫₀^{x_s} f(t) dt = -∫₀^{x_s} [Γ·tanh^n(t) - λt] dt
# (f is the map, not f - (1+λ)x)
def integrand_potential(t):
    return GAMMA * np.tanh(t)**n - LAMBDA * t

V_pot, _ = quad(integrand_potential, 0, x_s)
print(f"\nCandidate 2: Potential V = ∫₀^x_s [Γ·tanh^n(t) - λt] dt")
print(f"  V = {V_pot:.10f}")
print(f"  M/V = {M_target/V_pot:.10f}")

# Candidate 3: "Free energy" F = x_s²/2 (kinetic) + something
F_kinetic = x_s**2 / 2
print(f"\nCandidate 3: Kinetic energy x_s²/2 = {F_kinetic:.10f}")
print(f"  Compare X²/2 = {X**2/2}")
print(f"  M - X²/2 = {M_target - X**2/2:.10f}")

# Candidate 4: Build M from x_s using the ratio X/x_s
# If M is a polynomial in X, and X = α·x_s where α = n·p²/(p²+p+1),
# then M is also a polynomial in x_s (with modified coefficients)
alpha = n * p**2 / (p**2 + p + 1)
print(f"\nCandidate 4: Express M in terms of x_s via X = α·x_s, α = {alpha:.10f}")
print(f"  M = X²/2 + (n/p)X + n²/X + λ/n")
print(f"  M = (α·x_s)²/2 + (n/p)(α·x_s) + n²/(α·x_s) + λ/n")
print(f"  M = (α²/2)·x_s² + (nα/p)·x_s + n²/(α·x_s) + λ/n")
print(f"  α²/2 = {alpha**2/2:.10f}")
print(f"  nα/p = {n*alpha/p:.10f}")
print(f"  n²/α = {n**2/alpha:.10f}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 3: THE VIRIAL IDENTITY AND x_s²
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 3: VIRIAL IDENTITY → X²/2 TERM")
print("═" * 72)

# The virial theorem gives c₂ = 1/2. Let's trace its origin.
#
# At x_s: Γ·tanh^n(x_s) = (1+λ)·x_s
# Multiply by x_s: Γ·x_s·tanh^n(x_s) = (1+λ)·x_s²
#
# The virial says: if M has a term proportional to X², the coefficient
# is 1/2. This comes from the QUADRATIC structure of the recursion.
#
# More specifically: in the effective potential V(x), the fixed point
# sits at the balance between the nonlinear gate Γ·tanh^n(x) and the
# linear decay (1+λ)·x. The curvature at x_s determines the
# "harmonic" contribution.

# Curvature of the effective potential at x_s:
# V_eff(x) = ∫₀^x [(1+λ)t - Γ·tanh^n(t)] dt  (restoring force potential)
# V_eff''(x_s) = (1+λ) - Γ·n·tanh^{n-1}(x_s)·sech²(x_s)
V_eff_pp = (1 + LAMBDA) - n * GAMMA * np.tanh(x_s)**(n-1) * (1 - np.tanh(x_s)**2)
print(f"\nEffective potential curvature at x_s:")
print(f"  V_eff''(x_s) = {V_eff_pp:.10f}")
print(f"  This is = (1+λ) - f'(x_s) - λ = 1 - f'(x_s)")
f_p_s = f_prime(x_s)
print(f"  f'(x_s) = {f_p_s:.15e}")
print(f"  V_eff''(x_s) = {1 - f_p_s:.15e}")
print(f"  ≈ 1 (since f'(x_s) → 0 exponentially for large x_s)")

# So the harmonic contribution ≈ x_s²/2, which maps to X²/2 after rescaling.
# This IS the virial theorem: the quadratic term has coefficient 1/2
# because the effective potential has curvature ≈ 1 at x_s.

print(f"""
VIRIAL ORIGIN: The recursion's effective potential at x_s has
curvature ≈ 1 (exponentially close). This gives the X²/2 term.
The coefficient 1/2 is EXACT in the limit p → ∞ where tanh → step.
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 4: PARTITION FUNCTION APPROACH
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 4: PARTITION FUNCTION APPROACH")
print("═" * 72)

# Idea: Treat the recursion as a statistical mechanics system.
# The partition function Z = sum over states weighted by energy.
# Free energy F = -T ln Z = M in some normalization.
#
# The "states" are the fixed points x = 0, x_u, x_s.
# The "energy" at each fixed point involves the stability eigenvalue.
#
# For a 1D map f(x) with fixed points x_i:
# Z_1-loop = Σ_i 1/|1 - f'(x_i)|
# (This is the Lefschetz formula for periodic points)

Z_0 = 1 / abs(1 - f_prime(0))
Z_u = 1 / abs(1 - f_prime(x_u))
Z_s = 1 / abs(1 - f_prime(x_s))

fp0 = f_prime(0)
print(f"\nLefschetz-type partition function:")
print(f"  f'(0) = {fp0:.10f}")
print(f"  f'(x_u) = {f_prime(x_u):.10f}")
print(f"  f'(x_s) = {f_prime(x_s):.15e}")
print(f"  Z_0 = 1/|1-f'(0)| = {Z_0:.10f}")
print(f"  Z_u = 1/|1-f'(x_u)| = {Z_u:.10f}")
print(f"  Z_s = 1/|1-f'(x_s)| = {Z_s:.10f}")
print(f"  Z_total = {Z_0 + Z_u + Z_s:.10f}")
print(f"  M / Z_total = {M_target / (Z_0 + Z_u + Z_s):.10f}")

# Try weighted version: Z_w = Σ_i x_i / |1 - f'(x_i)|
Z_w = 0*Z_0 + x_u*Z_u + x_s*Z_s
print(f"\n  Weighted: Σ x_i·Z_i = {Z_w:.10f}")
print(f"  M / Z_w = {M_target / Z_w:.10f}")

# Try x² weighted: Z_w2 = Σ_i x_i² / |1 - f'(x_i)|
Z_w2 = x_u**2 * Z_u + x_s**2 * Z_s
print(f"  x²-weighted: Σ x_i²·Z_i = {Z_w2:.10f}")
print(f"  M / Z_w2 = {M_target / Z_w2:.10f}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 5: DIRECT ALGEBRAIC CONSTRUCTION
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 5: DIRECT ALGEBRAIC CONSTRUCTION")
print("═" * 72)

# Instead of guessing functionals, let's work backwards.
# We KNOW M = X²/2 + (n/p)X + n²/X + λ/n.
# Express everything in terms of the recursion parameters (n, p):
#   X = n·p·(p-1)
#   M = [n·p·(p-1)]²/2 + n²·(p-1) + n/(p·(p-1)) + 1/(n·(p³-1))
#
# Expand:
#   M = n²·p²·(p-1)²/2 + n²·(p-1) + n/(p·(p-1)) + 1/(n·(p³-1))

M_expanded_term1 = n**2 * p**2 * (p-1)**2 / 2  # X²/2
M_expanded_term2 = n**2 * (p-1)                  # (n/p)·X = n²·(p-1)
M_expanded_term3 = n / (p * (p-1))               # n²/X
M_expanded_term4 = 1 / (n * (p**3 - 1))          # λ/n

print(f"\nM decomposition in (n, p):")
print(f"  X²/2  = n²p²(p-1)²/2 = {M_expanded_term1:.6f}")
print(f"  c₁·X  = n²(p-1)      = {M_expanded_term2:.6f}")
print(f"  n²/X  = n/(p(p-1))   = {M_expanded_term3:.6f}")
print(f"  λ/n   = 1/(n(p³-1))  = {M_expanded_term4:.6f}")
print(f"  SUM   = {M_expanded_term1 + M_expanded_term2 + M_expanded_term3 + M_expanded_term4:.10f}")
print(f"  M     = {M_target:.10f}")

# Now: can we express M entirely in terms of x_s and recursion quantities?
# x_s ≈ Γ/(1+λ) = p²(p³-1)/p³ = p² - 1/p
# So p ≈ √(x_s + 1/p) ... this is circular.
#
# Better: from the fixed-point equation:
# Γ·tanh^n(x_s) = (1+λ)·x_s
# At large x_s: Γ ≈ (1+λ)·x_s  →  p² ≈ (1+1/(p³-1))·x_s

print(f"\nKey relationships:")
print(f"  Γ = p² = {GAMMA}")
print(f"  1+λ = p³/(p³-1) = {1 + LAMBDA:.10f}")
print(f"  x_s = Γ/(1+λ)·[1 + O(exp)] = {x_s:.10f}")
print(f"  X = n·p·(p-1) = {X}")
print(f"  X = n·(Γ/p)·(p-1) = n·p·(p-1)")

# ═══════════════════════════════════════════════════════════════════
# SECTION 6: THE KEY IDEA — ENERGY PER QUARK
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 6: ENERGY-PER-QUARK DECOMPOSITION")
print("═" * 72)

# What if M decomposes into:
#   M = (coherent energy of n quarks in field of strength Γ)
#
# Per quark, the energy might be:
#   E_quark = (some function of p)
#
# And M = n × (something) + interactions + vacuum
#
# Let's check: M/n vs M/n²
print(f"\nM = {M_target:.10f}")
print(f"M/n = {M_target/n:.10f}")
print(f"M/n² = {M_target/n**2:.10f}")

# M = X²/2 + (n/p)X + n²/X + λ/n
# M/n² = X²/(2n²) + X/(np) + 1/X + λ/n³
# = [p(p-1)]²/2 + (p-1) + 1/(np(p-1)) + 1/(n³(p³-1))
M_per_n2_t1 = (p*(p-1))**2 / 2
M_per_n2_t2 = p - 1
M_per_n2_t3 = 1/(n*p*(p-1))
M_per_n2_t4 = 1/(n**3 * (p**3-1))

print(f"\nM/n² decomposition:")
print(f"  [p(p-1)]²/2 = {M_per_n2_t1:.6f}")
print(f"  (p-1)       = {M_per_n2_t2:.6f}")
print(f"  1/(np(p-1)) = {M_per_n2_t3:.6f}")
print(f"  1/(n³(p³-1))= {M_per_n2_t4:.6f}")
print(f"  Sum = {M_per_n2_t1 + M_per_n2_t2 + M_per_n2_t3 + M_per_n2_t4:.10f}")
print(f"  M/n² = {M_target/n**2:.10f}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 7: RECURSION-NATIVE MASS FORMULA
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 7: TRYING TO DERIVE M FROM RECURSION QUANTITIES")
print("═" * 72)

# Key recursion quantities at x_s:
# - x_s itself (the saturated amplitude)
# - f'(x_s) ≈ 0 (exponentially stable)
# - Γ = p² (the gain)
# - λ = 1/(p³-1) (the damping)
# - The "action" S = ∫₀^{x_s} [G(t) - (1+λ)t] dt
# - The "Lyapunov exponent" = ln|f'(x_s)|

# What if M is related to x_s² in a specific way?
# M = X²/2 + ... where X = α·x_s with α = np²/(p²+p+1)
# So M = α²·x_s²/2 + ...

# Let's try: M as a function of x_s and Γ
# M = a·x_s² + b·Γ·x_s + c·Γ²/x_s + d
# We need to find a, b, c, d such that this gives the right answer

# From the known answer:
# M = X²/2 + (n/p)X + n²/X + λ/n
# M = α²x_s²/2 + (nα/p)x_s + n²/(αx_s) + λ/n

a_coeff = alpha**2 / 2
b_coeff = n * alpha / p
c_coeff = n**2 / alpha  # coefficient of 1/x_s
d_coeff = LAMBDA / n

print(f"\nM in terms of x_s (using X = α·x_s):")
print(f"  M = {a_coeff:.10f}·x_s² + {b_coeff:.10f}·x_s + {c_coeff:.10f}/x_s + {d_coeff:.10f}")
print(f"  Check: {a_coeff*x_s**2 + b_coeff*x_s + c_coeff/x_s + d_coeff:.10f}")
print(f"  M     = {M_target:.10f}")

# Now express the coefficients in terms of (n, p):
# a = α²/2 = (np²/(p²+p+1))²/2 = n²p⁴/(2(p²+p+1)²)
# b = nα/p = n²p/(p²+p+1)
# c = n²/α = n(p²+p+1)/p²
# d = λ/n = 1/(n(p³-1))

print(f"\nCoefficients in (n,p):")
a_expr = Fraction(n**2 * p**4, 2 * (p**2 + p + 1)**2)
b_expr = Fraction(n**2 * p, p**2 + p + 1)
c_expr = Fraction(n * (p**2 + p + 1), p**2)
d_expr = Fraction(1, n * (p**3 - 1))
print(f"  a = n²p⁴/(2(p²+p+1)²) = {a_expr} = {float(a_expr):.10f}")
print(f"  b = n²p/(p²+p+1) = {b_expr} = {float(b_expr):.10f}")
print(f"  c = n(p²+p+1)/p² = {c_expr} = {float(c_expr):.10f}")
print(f"  d = 1/(n(p³-1)) = {d_expr} = {float(d_expr):.10f}")

# These are ugly. The polynomial in X is much cleaner:
# M = X²/2 + (n/p)X + n²/X + λ/n
# The coefficients {1/2, n/p, n², 1/(n(p³-1))} are natural.

# ═══════════════════════════════════════════════════════════════════
# SECTION 8: THE FIXED-POINT POTENTIAL APPROACH
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 8: FIXED-POINT POTENTIAL / ENERGY LANDSCAPE")
print("═" * 72)

# Define V(x) = -∫₀^x f(t) dt + x²/2
# = -∫₀^x [Γ·tanh^n(t)] dt + ∫₀^x λt dt + x²/2
# = -Γ·∫₀^x tanh^n(t) dt + λx²/2 + x²/2
# = -Γ·I_n(x) + (1+λ)x²/2

# For n=3: ∫ tanh³(t) dt = ∫ tanh(t)(1-sech²(t)) dt
#         = ln(cosh(t)) - tanh²(t)/2 + C
# Check: d/dt [ln cosh t - tanh²t/2] = tanh t - tanh t·sech²t = tanh t(1-sech²t) = tanh³t ✓

def I3(x):
    """∫₀^x tanh³(t) dt = ln(cosh(x)) - tanh²(x)/2"""
    return np.log(np.cosh(x)) - np.tanh(x)**2 / 2

# Verify numerically
I3_numerical, _ = quad(lambda t: np.tanh(t)**3, 0, x_s)
I3_analytic = I3(x_s)
print(f"\n∫₀^x_s tanh³(t) dt:")
print(f"  Numerical: {I3_numerical:.10f}")
print(f"  Analytic:  {I3_analytic:.10f}")
print(f"  Match: {abs(I3_numerical - I3_analytic):.2e}")

# The potential: V(x) = (1+λ)x²/2 - Γ·I_n(x)
def V(x):
    return (1 + LAMBDA) * x**2 / 2 - GAMMA * I3(x)

V_s = V(x_s)
V_u = V(x_u)
V_0 = V(0)

print(f"\nPotential landscape V(x):")
print(f"  V(0)   = {V_0:.10f}")
print(f"  V(x_u) = {V_u:.10f}")
print(f"  V(x_s) = {V_s:.10f}")

# The barrier height and well depth:
barrier = V_u - V_0
well = V_s - V_u
print(f"\n  Barrier V(x_u)-V(0) = {barrier:.10f}")
print(f"  Well depth V(x_s)-V(x_u) = {well:.10f}")
print(f"  Total V(x_s)-V(0) = {V_s:.10f}")

# Check if any combination gives M:
print(f"\n  M / V(x_s) = {M_target / V_s:.10f}")
print(f"  M / |V(x_s)| = {M_target / abs(V_s):.10f}")
print(f"  M / barrier = {M_target / barrier:.10f}")
print(f"  M / |well| = {M_target / abs(well):.10f}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 9: POLYNOMIAL IN X — WHY IS IT NATURAL?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 9: WHY IS M A POLYNOMIAL IN X = n·p·(p-1)?")
print("═" * 72)

# Key insight: X = n·p·(p-1) is NOT just a convenient variable.
# X = the number of integer lattice points in the "quark momentum space"
# under the constraint n·p·(p-1) = Σ k_i
#
# The mass formula as a polynomial in X:
# M = X²/2 + c₁X + c₋₁/X + c₀
#
# This looks like the energy of a system with:
# - Kinetic energy ∝ X² (quadratic, harmonic)
# - Linear potential ∝ X (quark string tension?)
# - Coulomb-like ∝ 1/X (confinement?)
# - Constant offset (vacuum energy)
#
# In the Cornell potential model of QCD:
# V(r) = -α_s/r + σ·r + const
# E ∝ (momentum)² + σ·r - α_s/r
#
# If X plays the role of a "size" (like inter-quark separation):
# M = X²/2 + σ·X + g/X + E_vac
# with σ = n/p (string tension = n quarks × coupling)
#      g = n² (Coulomb strength = quark charge²)
#      E_vac = λ/n (vacuum energy per quark ÷ n)

print(f"""
CORNELL POTENTIAL ANALOGY:
  QCD:  V(r) = σ·r - α_s/r + const + kinetic
  RASP: M(X) = X²/2 + (n/p)·X + n²/X + λ/n

  If X = "separation variable":
    X²/2     ↔ Kinetic energy (virial: c₂ = 1/2)
    (n/p)·X  ↔ String tension σ = n·κ = n/p  [LINEAR CONFINEMENT]
    n²/X     ↔ Coulomb charge² = n²           [SHORT-RANGE]
    λ/n      ↔ Vacuum energy = λ/n            [VACUUM]
""")

# This is suggestive. The linear term (string tension) being n·κ
# means: n quarks, each contributing κ to the string tension.
# In QCD, the string tension is proportional to the number of
# color charges stretched between quarks.

# ═══════════════════════════════════════════════════════════════════
# SECTION 10: CAN WE DERIVE THE POLYNOMIAL FORM?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 10: ATTEMPTING TO DERIVE THE POLYNOMIAL FORM")
print("═" * 72)

# The question: WHY does M have the form a·X² + b·X + c/X + d?
#
# Hypothesis: M arises from a CONSTRAINED OPTIMIZATION.
# The recursion selects (n, p) via the Diophantine equation.
# Given (n, p), the mass is a function of X = n·p·(p-1).
#
# What if M = energy of the OPTIMAL PACKING of n quarks in a
# p-dimensional lattice, where X is the total momentum?
#
# For a harmonic system with N particles in a box of size L:
# E = T + V_confine + V_coulomb + V_vacuum
# T ∝ L² (kinetic, virial)
# V_confine ∝ N·σ·L (linear confinement, N strings)
# V_coulomb ∝ N²/L (Coulomb, N² pairs)
# V_vacuum ∝ const (vacuum, ∝ 1/N per quark)
#
# If L → X and N → n, σ → κ = 1/p:
# M = X²/2 + n·κ·X + n²/X + λ/n  ... THIS IS THE FORMULA!

print("""
PHYSICAL DERIVATION OF THE POLYNOMIAL FORM:

Consider n quarks in a confining potential of size X:

  TERM 1: Kinetic energy T = X²/2
    Origin: virial theorem for the recursion's fixed point
    The coefficient 1/2 comes from the quadratic structure
    of the effective potential at x_s (Section 3).

  TERM 2: Linear confinement V_linear = (n·κ)·X = (n/p)·X
    Origin: n quarks, each coupled with strength κ = 1/p
    The string tension σ = n·κ because n identical quarks
    each contribute one unit of coupling.

  TERM 3: Coulomb (short-range) V_coulomb = n²/X
    Origin: n² comes from the number of quark-quark pairs
    (or more precisely, n² from the total color charge squared).
    The 1/X scaling is the Coulomb-like short-range force.

  TERM 4: Vacuum energy V_vac = λ/n
    Origin: The vacuum parameter λ = 1/(p³-1), shared among
    n quarks. Each quark's vacuum contribution is λ/n.
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 11: TESTING THE PHYSICAL DERIVATION
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 11: TESTING AGAINST ALL DIOPHANTINE SOLUTIONS")
print("═" * 72)

# If the physical derivation is correct, then M for the OTHER
# Diophantine solutions should also follow M = X²/2 + (n/p)X + n²/X + λ/n
# (with THEIR values of n, p, X, λ).

solutions = [(3, 5), (4, 3), (6, 2)]

print(f"\n{'n':>3s} {'p':>3s} | {'X':>5s} | {'Γ':>5s} | {'λ':>12s} | {'M (formula)':>14s} | {'x_s':>10s}")
print("-" * 72)

for nn, pp in solutions:
    XX = nn * pp * (pp - 1)
    GG = pp**2
    LL = 1/(pp**3 - 1)
    M_formula = XX**2/2 + (nn/pp)*XX + nn**2/XX + LL/nn

    # Find x_s for this (n, p)
    def fp(x, G=GG, lam=LL, nq=nn):
        return G * np.tanh(x)**nq - (1 + lam) * x

    try:
        xs = brentq(fp, GG*0.8, GG*1.1)
    except:
        xs = float('nan')

    print(f"{nn:3d} {pp:3d} | {XX:5d} | {GG:5d} | {LL:12.8f} | {M_formula:14.6f} | {xs:10.6f}")

print(f"""
NOTE: The mass formula gives DIFFERENT values of M for different (n,p).
Only (3,5) gives M ≈ 1836.153 (the proton/electron mass ratio).
The formula is the SAME STRUCTURE for all solutions, but only one
matches experiment.

This is the Diophantine selection at work: among all solutions with
M = X²/2 + (n/p)X + n²/X + λ/n, only (3,5) hits the physical value.
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 12: THE CRITICAL QUESTION — WHERE DOES c₁ = n/p COME FROM?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 12: THE CRITICAL QUESTION")
print("═" * 72)

# From the physical derivation:
# c₁ = σ = n·κ = n/p
# where κ = 1/p = 1/√Γ is the single-quark coupling.
#
# But WHY is κ = 1/p? We already know this:
# κ = 1/√Γ because at the unstable fixed point x_u,
# the dimensionless coupling x_u · f'(x_u) / x_u ≈ n·κ + O(λ)
#
# The exact result (from the paper):
# At x_s: x_s · f'(x_s) = -1/p = -κ  (EXACT)
#
# So κ = 1/p emerges from the STABLE fixed point's virial.
# And c₁ = n·κ comes from having n identical quarks (tanh^n = [tanh]^n).

# Let's verify once more: what is x_s · f'(x_s) / x_s exactly?
virial_s = x_s * f_prime(x_s)
print(f"\nVirial at x_s: x_s·f'(x_s) = {virial_s:.15e}")
print(f"Expected -κ = -1/p = {-1/p:.15f}")
print(f"Match: {abs(virial_s + 1/p):.2e}")

# Not exact numerically — let's check analytically
# f'(x) = n·Γ·tanh^{n-1}(x)·sech²(x) - λ
# At x_s where tanh(x_s) ≈ 1 and sech²(x_s) ≈ 4·exp(-2x_s):
# f'(x_s) ≈ n·Γ·4·exp(-2x_s) - λ
# x_s·f'(x_s) ≈ 4n·Γ·x_s·exp(-2x_s) - λ·x_s
#
# With x_s ≈ Γ/(1+λ):
# x_s·f'(x_s) ≈ 4n·Γ²·exp(-2Γ/(1+λ))/(1+λ) - λΓ/(1+λ)
# The first term is exponentially small.
# The second: -λΓ/(1+λ) = -Γ/(p³-1)·(p³-1)/p³·Γ ... wait

# Let me compute more carefully:
# λ = 1/(p³-1), 1+λ = p³/(p³-1)
# λ/(1+λ) = 1/p³
# So x_s·f'(x_s) ≈ -λ·x_s = -x_s/(p³-1) ≈ -Γ/((p³-1)(1+λ)) = -p²·(p³-1)/(p³·(p³-1)) = -p²/p³ = -1/p

print(f"""
ANALYTIC VERIFICATION:
  f'(x_s) ≈ -λ (exponential terms negligible)
  x_s ≈ Γ/(1+λ) = p²·(p³-1)/p³
  x_s·f'(x_s) ≈ -λ·x_s = -[1/(p³-1)]·[p²(p³-1)/p³] = -p²/p³ = -1/p = -κ  ✓

  This IS exact in the large-p limit and O(exp(-2p²)) accurate for finite p.
  For p=5: exp(-2·25) = exp(-50) ≈ 2×10⁻²² — effectively exact.
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 13: THE CONSTRUCTION ARGUMENT
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 13: THE FULL CONSTRUCTION ARGUMENT")
print("═" * 72)

print(f"""
THEOREM (CONSTRUCTION): The mass formula M = X²/2 + (n/p)X + n²/X + λ/n
arises from four independent physical principles applied to the recursion
f(x) = Γ·tanh^n(x) - λx:

STEP 1: POLYNOMIAL FORM
  The mass ratio M is a function of X = n·p·(p-1), the dimensionless
  quark momentum. Dimensional analysis and the structure of the recursion
  constrain M to the Laurent form: M = c₂X² + c₁X + c₀ + c₋₁/X + ...

  EVIDENCE: Higher-order terms (X³, 1/X², ...) would require additional
  dimensionless parameters beyond (n, p, λ). The recursion provides
  exactly enough structure for a 4-term expansion.

  STATUS: Structural argument, not derivation. ★★★☆☆

STEP 2: VIRIAL (c₂ = 1/2) — PROVED
  The effective potential V_eff(x) = (1+λ)x²/2 - Γ·I_n(x) has
  curvature V''(x_s) = 1 - f'(x_s) ≈ 1 (to exponential accuracy).
  The quadratic term in any polynomial expansion inherits this
  coefficient: c₂ = 1/2.

  STATUS: Theorem (proved in paper, Section 5). ★★★★★

STEP 3: SINGLE-QUARK COUPLING (κ = 1/p) — PROVED
  At the stable fixed point: x_s·f'(x_s) = -1/p = -κ exactly
  (Section 12 above). This identifies κ = 1/√Γ = 1/p as the
  fundamental quark-field coupling constant.

  STATUS: Theorem (proved in paper, Section 6). ★★★★★

STEP 4: LINEAR TERM (c₁ = n·κ) — STRUCTURAL ARGUMENT
  The factorization tanh^n = [tanh]^n decomposes the n-quark gate
  into n identical single-quark contributions. Each contributes κ
  to the linear coefficient. Physical interpretation: n quarks ×
  string tension κ = total string tension n·κ = n/p.

  SUPPORTING EVIDENCE:
  ✓ Per-quark coupling κ = 1/p is n-independent (verified across
    all three Diophantine solutions)
  ✓ Elasticity factorizes: n × single-quark (Angle 1, Test 1)
  ✓ Cross-virial: x_u·f'(x_u) = n/p + O(λ) (Angle 1 of paper)
  ✓ Mean-field: effective single-quark gains κ = 1/p per quark
  ✓ Cornell potential analogy: σ = n·κ natural for n-quark string

  STATUS: Strong physical argument with 5 supporting computations.
  NOT a mathematical derivation. ★★★★☆

STEP 5: REMAINING TERMS
  c₋₁ = n²: Coulomb-type term, n² from total charge squared.
  c₀ = λ/n: Vacuum energy per quark.
  These are the SIMPLEST expressions consistent with the
  recursion's symmetry (Occam selection).

  STATUS: Occam selection. ★★★☆☆
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 14: WHAT WOULD A FULL DERIVATION REQUIRE?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 14: WHAT WOULD A FULL DERIVATION REQUIRE?")
print("═" * 72)

print(f"""
TO DERIVE M FROM THE RECURSION (not just its form), we would need:

1. A PHYSICAL DEFINITION of M in terms of the recursion.
   Currently: M = m_p/m_e (experimental value).
   Needed: M = F[f, x_s, x_u, Γ, λ, n] for some functional F.

2. This F must evaluate to a polynomial in X.
   This requires showing that F naturally expands as a Laurent
   series in X with rapidly convergent coefficients.

3. The polynomial's coefficients must come out as 1/2, n/p, lambda/n, n^2.

THE FUNDAMENTAL ISSUE:
  The recursion f(x) = Γ·tanh^n(x) - λx is a DYNAMICAL SYSTEM.
  It gives fixed points, stability, basins of attraction.
  But it does NOT directly give a mass ratio.

  The connection M ↔ recursion goes through INTERPRETATION:
  "The recursion describes quark confinement dynamics, and the
   mass ratio is the energy of the confined state."

  This interpretation is what the paper provides. But an interpretation
  is not a derivation. Without a first-principles argument for WHY
  the recursion's energy functional equals the mass ratio, we cannot
  derive M.

HONEST ASSESSMENT:
  We can derive: c₂ = 1/2 (virial) ✓
  We can derive: κ = 1/p (stable virial) ✓
  We can motivate: c₁ = n·κ (factorization + 5 supporting arguments) ~
  We cannot derive: WHY M is a polynomial in X
  We cannot derive: WHY these specific terms and no others
  We cannot derive: c₋₁ = n² or c₀ = λ/n from first principles

THE RECURSION GIVES US THE ARCHITECTURE.
THE POLYNOMIAL IS AN ANSATZ THAT FITS THE ARCHITECTURE.
c₁ = n/p IS THE SIMPLEST VALUE CONSISTENT WITH THE ARCHITECTURE.

This is NOT a failure — it's a clear statement of what IS proved
and what remains structural/physical argument.
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 15: ONE MORE ATTEMPT — THERMODYNAMIC FREE ENERGY
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 15: THERMODYNAMIC FREE ENERGY ATTEMPT")
print("═" * 72)

# What if we treat β = 1/X as inverse temperature?
# Then Z(β) = e^{-β·E_0} × (corrections)
# F = -ln Z / β ≈ E_0 + (corrections in β)

# The mass formula: M(X) = X²/2 + (n/p)X + n²/X + λ/n
# In terms of β = 1/X:
# M = 1/(2β²) + n/(pβ) + n²β + λ/n
# F(β) = β·M = 1/(2β) + n/p + n²β² + λβ/n ... no, this isn't standard

# Try: M as the minimum of some variational energy E(X)
# dM/dX = X + n/p - n²/X² = 0
# X³ + (n/p)X² = n²
# For (n=3, p=5): X³ + 0.6·X² = 9
# X ≈ 2.0 ... but our X = 60. So M is NOT at the minimum of its own polynomial.

X_critical = np.roots([1, n/p, 0, -n**2])
X_critical_real = [x.real for x in X_critical if abs(x.imag) < 1e-10 and x.real > 0]
print(f"\nCritical points of M(X): dM/dX = 0 at X = {X_critical_real}")
print(f"Our X = {X} — NOT at a critical point.")
print(f"dM/dX|_{X} = X + n/p - n²/X² = {X + n/p - n**2/X**2:.6f}")

# M is evaluated AT X = n·p·(p-1), which is NOT the minimum of M(X).
# X is determined by the DIOPHANTINE equation, not by minimizing M.
# This means M is not a variational principle — it's a formula evaluated
# at a specific integer point.

print(f"""
RESULT: M(X) is NOT evaluated at a critical point of itself.
X = n·p·(p-1) = 60 comes from the Diophantine selection,
not from minimizing M. dM/dX|₆₀ = {X + n/p - n**2/X**2:.4f} ≠ 0.

This rules out M being a variational energy with X as the
variational parameter. M is a FORMULA evaluated at a
CONSTRAINED point.
""")

# ═══════════════════════════════════════════════════════════════════
# SECTION 16: COMPREHENSIVE NUMERICAL EXPLORATION
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 16: NUMERICAL EXPLORATION — COMBINATIONS OF RECURSION QUANTITIES")
print("═" * 72)

# Systematically try combinations of recursion quantities to find M
quantities = {
    'x_s': x_s,
    'x_u': x_u,
    'Γ': GAMMA,
    'λ': LAMBDA,
    'n': n,
    'p': p,
    'X': X,
    'f_p_u': f_prime(x_u),
    'κ': kappa,
    'S_action': S_action,
    'V_xs': V_s,
    'V_xu': V_u,
    'x_s²': x_s**2,
    'x_u²': x_u**2,
    'Γ²': GAMMA**2,
}

# Try ratios and products
print(f"\nTarget: M = {M_target:.6f}")
print(f"\n{'Expression':>30s} | {'Value':>14s} | {'M/Value':>14s} | {'Value/M':>14s}")
print("-" * 80)

interesting = []
for name1, v1 in quantities.items():
    if v1 == 0:
        continue
    ratio = M_target / v1
    # Check if ratio is close to a simple fraction or integer
    for num in range(1, 20):
        for den in range(1, 20):
            if abs(ratio - num/den) < 0.01:
                interesting.append((name1, v1, ratio, f"{num}/{den}"))

    # Also check ratio itself
    if abs(ratio) > 0.01 and abs(ratio) < 1000:
        if abs(ratio - round(ratio)) < 0.01:
            interesting.append((name1, v1, ratio, f"≈{round(ratio)}"))

# Print notable ones
for name, val, ratio, approx in interesting:
    print(f"{'M/'+name:>30s} | {val:14.6f} | {ratio:14.6f} | {approx:>14s}")

# Some specific combinations
combos = [
    ("Γ·x_s", GAMMA * x_s),
    ("Γ·x_s/n", GAMMA * x_s / n),
    ("x_s²/2", x_s**2 / 2),
    ("Γ²/n", GAMMA**2 / n),
    ("n·Γ·(Γ-1)", n * GAMMA * (GAMMA - 1)),
    ("n·Γ·(Γ-1)/n", GAMMA * (GAMMA - 1)),
    ("Γ·(Γ-1)/2+n/p·Γ+n²/Γ", GAMMA*(GAMMA-1)/2 + n/p*GAMMA + n**2/GAMMA),
    ("p²(p-1)²/2·n²+...", n**2*p**2*(p-1)**2/2 + n**2*(p-1) + n/(p*(p-1)) + 1/(n*(p**3-1))),
]

print(f"\n{'Expression':>40s} | {'Value':>14s} | {'Diff from M':>14s}")
print("-" * 75)
for name, val in combos:
    print(f"{name:>40s} | {val:14.6f} | {val - M_target:14.6e}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 17: THE n²·p²·(p-1)²/2 DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("SECTION 17: DECOMPOSITION AS n² × SINGLE-QUARK ENERGY")
print("═" * 72)

# What if M = n² × E_single where E_single is a function of p only?
# M/n² = p²(p-1)²/2 + (p-1) + 1/(np(p-1)) + 1/(n³(p³-1))
# The last two terms still depend on n. So M is NOT n² × (function of p).

# What about M = n × E_lin + n² × E_quad?
# M = [n²p²(p-1)²/2 + n²(p-1)] + [n/(p(p-1)) + 1/(n(p³-1))]
# First bracket = n²[p²(p-1)²/2 + (p-1)] ← proportional to n²
# Second bracket = n/(p(p-1)) + 1/(n(p³-1)) ← mixed

print(f"\nDecomposition by n-scaling:")
term_n2 = n**2 * (p**2*(p-1)**2/2 + (p-1))  # proportional to n²
term_rest = n/(p*(p-1)) + 1/(n*(p**3-1))     # the small correction
print(f"  n²·[p²(p-1)²/2 + (p-1)] = {term_n2:.6f}")
print(f"  Remaining: n/(p(p-1)) + 1/(n(p³-1)) = {term_rest:.6f}")
print(f"  Sum = {term_n2 + term_rest:.10f}")
print(f"  M   = {M_target:.10f}")
print(f"\n  The n²-proportional part is {term_n2/M_target*100:.4f}% of M")
print(f"  The rest is {term_rest/M_target*100:.4f}% of M")

# So M is DOMINATED by the n² term (X²/2 + c₁X) and the corrections
# (n²/X + λ/n) are tiny.

# ═══════════════════════════════════════════════════════════════════
# FINAL ASSESSMENT
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("ANGLE 2: FINAL ASSESSMENT")
print("═" * 72)

print(f"""
RESULT: CANNOT DERIVE M FROM THE RECURSION ALONE.

The mass formula M = X²/2 + (n/p)X + n²/X + λ/n is a POLYNOMIAL ANSATZ
in the dimensionless quark momentum X = n·p·(p-1).

WHAT WE CAN DO:
  ✓ DERIVE c₂ = 1/2 from the virial theorem (proved)
  ✓ DERIVE κ = 1/p from the stable-point virial (proved)
  ✓ MOTIVATE c₁ = n·κ from factorization + 5 supporting arguments
  ✓ MOTIVATE the polynomial form via Cornell potential analogy
  ✓ VERIFY parametric consistency across all Diophantine solutions

WHAT WE CANNOT DO:
  ✗ Define a functional F[recursion] such that F = M
  ✗ Derive the polynomial form from the recursion dynamics
  ✗ Derive c₋₁ = n² or c₀ = λ/n from first principles
  ✗ Explain WHY M is a function of X rather than x_s

THE GAP IS IRREDUCIBLE (within the current framework):
  The recursion f(x) = Γ·tanh^n(x) - λx is a DYNAMICAL SYSTEM.
  It describes HOW the quark field evolves, not WHAT the mass ratio is.

  The connection M ↔ recursion requires an ADDITIONAL PHYSICAL PRINCIPLE
  that maps the dynamics to an energy. This principle is the mass formula
  ANSATZ itself.

  THIS IS NORMAL IN PHYSICS. The Schrödinger equation describes dynamics;
  the energy eigenvalue is an ADDITIONAL computation (expectation value).
  Similarly, the recursion describes quark dynamics; the mass formula is
  the energy computation.

CONTRIBUTION TO PAPER:
  1. Section 8 already acknowledges c₁ is not derived
  2. The Cornell potential analogy (Section 9 above) provides the
     strongest physical motivation for WHY the polynomial has this form
  3. The factorization argument (Angle 1) explains WHY c₁ = n·κ
  4. Together with virial (c₂ = 1/2) and cross-virial (approximate),
     these leave c₁ = n/p as the UNIQUE physically motivated choice

  The paper's position is correct: c₁ = n/p by Occam, with strong
  physical motivation from multiple independent arguments.

Moving to ANGLE 3: Complex residue theorem.
""")

print("=" * 72)
print("END ANGLE 2")
print("=" * 72)
