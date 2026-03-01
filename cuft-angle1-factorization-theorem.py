#!/usr/bin/env python3
"""
CUFT-RASP ANGLE 1: N-QUARK FACTORIZATION THEOREM
==================================================
YASA PRESENTS — 2026-02-24

GOAL: Prove that c₁ = n·κ follows rigorously from the multiplicative
structure tanh^n(x) = [tanh(x)]^n.

APPROACH:
  The recursion f(x) = Γ·tanh^n(x) - λx has tanh^n as a PRODUCT of n
  identical single-quark gates g(x) = tanh(x).

  If we can show that the mass formula M(X) necessarily has a linear
  term equal to n times the single-quark coupling κ, then c₁ = n·κ
  is a THEOREM, not an identification.

  Strategy:
  1. Decompose the fixed-point equation into n single-quark contributions
  2. Show the log-derivative at x_s factorizes into n identical terms
  3. Derive the mass formula's linear term from this factorization
  4. Test: modify the recursion to use tanh^n(x/n) (n distinguishable
     quarks with different arguments) and check if c₁ changes
  5. Test: use [tanh(x)]^a · [tanh(x)]^(n-a) and verify additivity
"""

import numpy as np
from scipy.optimize import brentq
from fractions import Fraction

n = 3
p = 5
GAMMA = p**2
LAMBDA = 1/(p**3 - 1)
kappa = 1/p
X = n * p * (p - 1)

def fp_eq(x, G=GAMMA, lam=LAMBDA, nq=n):
    return G * np.tanh(x)**nq - (1 + lam) * x

x_u = brentq(fp_eq, 0.01, 1.0)
x_s = brentq(fp_eq, 10.0, 30.0)

print("=" * 72)
print("ANGLE 1: N-QUARK FACTORIZATION THEOREM")
print("=" * 72)

# ═══════════════════════════════════════════════════════════════════
# TEST 1: FACTORIZATION OF THE LOG-DERIVATIVE
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("TEST 1: LOG-DERIVATIVE FACTORIZATION AT FIXED POINTS")
print("═" * 72)

# The gating function: G(x) = Γ·tanh^n(x)
# ln G(x) = ln Γ + n·ln(tanh(x))
# d/dx ln G(x) = n · sech²(x)/tanh(x) = n · 2/(sinh(2x))

# At the fixed point: G(x*) = (1+λ)·x*
# So ln G(x*) = ln(1+λ) + ln(x*)

# The log-derivative of the OUTPUT at x*:
# d/dx ln[(1+λ)x] = 1/x

# Setting input log-derivative = output log-derivative at x*:
# n · 2/sinh(2x*) = 1/x*  ... this is NOT generally true

# What IS true: the ELASTICITY (x·d/dx ln G) = x·G'/G

def elasticity(x, nq=n):
    """x · d/dx ln[Γ·tanh^n(x)] = n·x·sech²(x)/tanh(x)"""
    t = np.tanh(x)
    s2 = 1 - t**2
    return nq * x * s2 / t

# At fixed point: G(x*) = (1+λ)x*, so G'(x*) = f'(x*) + λ
# Elasticity = x* · G'(x*) / G(x*) = x* · (f'(x*)+λ) / ((1+λ)·x*)
#            = (f'(x*)+λ) / (1+λ)

elast_u = elasticity(x_u)
elast_s = elasticity(x_s)

# Alternative computation via f'
f_prime_u = n * GAMMA * np.tanh(x_u)**(n-1) * (1 - np.tanh(x_u)**2) - LAMBDA
f_prime_s = n * GAMMA * np.tanh(x_s)**(n-1) * (1 - np.tanh(x_s)**2) - LAMBDA

elast_u_alt = (f_prime_u + LAMBDA) / (1 + LAMBDA)
elast_s_alt = (f_prime_s + LAMBDA) / (1 + LAMBDA)

print(f"\nElasticity x·G'/G at fixed points:")
print(f"  x_u: {elast_u:.10f} (direct), {elast_u_alt:.10f} (via f')")
print(f"  x_s: {elast_s:.15e} (direct), {elast_s_alt:.15e} (via f')")

# Single-quark elasticity: x·d/dx ln[tanh(x)] = x·sech²(x)/tanh(x)
def single_quark_elast(x):
    t = np.tanh(x)
    return x * (1 - t**2) / t

sqe_u = single_quark_elast(x_u)
sqe_s = single_quark_elast(x_s)

print(f"\nSingle-quark elasticity x·g'/g at fixed points:")
print(f"  x_u: {sqe_u:.10f}")
print(f"  x_s: {sqe_s:.15e}")
print(f"\nn × single-quark:")
print(f"  x_u: {n*sqe_u:.10f} (should = total elasticity: {elast_u:.10f})")
print(f"  Match: {abs(n*sqe_u - elast_u):.2e}")

# ═══════════════════════════════════════════════════════════════════
# TEST 2: MASS FORMULA FROM ELASTICITY DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("TEST 2: CAN WE DERIVE M FROM THE ELASTICITY?")
print("═" * 72)

# The mass formula M = X²/2 + c₁X + n²/X + λ/n
# What IS M in terms of the recursion?
#
# Key insight: M is NOT directly computable from a single fixed point.
# M is the proton-to-electron mass RATIO. The recursion gives x_s
# (the saturated amplitude). The connection M ↔ x_s must go through
# the CONSTRUCTION of the mass formula.
#
# The mass formula was CONSTRUCTED as:
#   M = (coherent energy of n quarks in the recursion)
#
# Let's trace: X = n·p·(p-1) = n·κ·x_s·p ... wait:
# x_s = (p³-1)/p, κ = 1/p
# κ·x_s = (p³-1)/p² = (p-1/p²)(p²+p+1)/... let me just compute

print(f"\nx_s = {x_s:.10f}")
print(f"X = {X}")
print(f"X/x_s = {X/x_s:.10f}")
print(f"n·p·(p-1) / ((p³-1)/p) = n·p²·(p-1)/(p³-1)")
ratio_X_xs = n * p**2 * (p-1) / (p**3 - 1)
print(f"  = {ratio_X_xs:.10f}")
print(f"  = n·p²·(p-1)/((p-1)(p²+p+1)) = n·p²/(p²+p+1)")
print(f"  = {n*p**2/(p**2+p+1):.10f}")
print(f"  = 75/31 = {75/31:.10f}")

# So X = (75/31)·x_s. X and x_s are proportional but with an ugly factor.
# The mass formula is in terms of X, not x_s.

# Let me try another approach: what if M comes from the TOTAL energy
# stored in the recursion at the fixed point?

# Energy interpretation:
# At x_s, the recursion balance is: Γ·tanh^n(x_s) = (1+λ)·x_s
# The "potential energy" stored: V = ∫₀^{x_s} [Γ·tanh^n(t) - (1+λ)t] dt + stuff
# But this integral is what we computed before (~280) and doesn't directly give M.

# THE REAL QUESTION: How was the mass formula originally constructed?
# From the paper: M = X²/2 + c₁X + c₀ + c₋₁/X
# This is a POLYNOMIAL ANSATZ in X = n·p·(p-1).
# The coefficients were found by:
#   c₂ = 1/2 from virial
#   c₁, c₀, c₋₁ from Occam scan
#
# So M is NOT derived from the recursion — it's fitted to the
# experimental value with the constraint that c₂ = 1/2.
#
# THIS IS THE GAP. If M is not derived, we can't derive c₁ from M.
# We need to DERIVE M first.

print(f"""
KEY REALIZATION:

The mass formula M = X²/2 + c₁X + n²/X + λ/n is NOT derived from
the recursion. It is a polynomial ANSATZ in X where:
  - c₂ = 1/2 is proved (virial)
  - c₁, c₋₁, c₀ are fitted (Occam selects the simplest)

The factorization argument shows c₁ = n·κ is CONSISTENT with
n identical quarks, but it cannot DERIVE c₁ without first
deriving M itself.

CONCLUSION: The factorization provides a structural explanation
(WHY c₁ = n·κ makes physical sense) but not a mathematical proof.
It strengthens the identification but doesn't close the gap.

The real prize is ANGLE 2: derive M from the recursion.
""")

# ═══════════════════════════════════════════════════════════════════
# TEST 3: MODIFIED RECURSIONS — DOES c₁ TRACK n·κ?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("TEST 3: WHAT IF WE MODIFY THE RECURSION?")
print("═" * 72)

# If we change the recursion to f(x) = Γ·tanh^m(x) - λx for m ≠ n,
# keeping all other parameters the same, and ask "what mass formula
# would reproduce the known proton mass?", does c₁ = m·κ?

# This tests whether c₁ is STRUCTURALLY tied to the exponent.

M_target = 853811/465  # the known mass

print(f"\nTest: for f(x) = Γ·tanh^m(x) - λx with Γ=25, λ=1/124, X=60,")
print(f"what c₁ reproduces M = {M_target:.10f} given c₂=1/2, c₋₁=n², c₀=λ/n?")
print(f"\nNote: c₋₁ and c₀ also depend on n, so this test is about the")
print(f"STRUCTURE of the formula, not the recursion dynamics.")
print()

# M = X²/2 + c₁·X + c₋₁/X + c₀
# c₁ = (M - X²/2 - c₋₁/X - c₀) / X

# For our actual case:
c1_actual = (M_target - X**2/2 - n**2/X - LAMBDA/n) / X
print(f"Actual c₁ = {c1_actual:.15f}")
print(f"n/p = {n/p:.15f}")
print(f"Match: {abs(c1_actual - n/p):.2e}")

# If we changed n to m in the confinement and vacuum terms:
print(f"\n{'m':>4s} | {'c₁ needed':>12s} | {'m/p':>8s} | {'c₁ = m·κ?':>12s} | {'diff':>12s}")
print("-" * 60)
for m in range(1, 8):
    # With m quarks: X_m = m·p·(p-1), c₋₁ = m², c₀ = λ/m
    X_m = m * p * (p - 1)
    c_neg1_m = m**2
    c_0_m = LAMBDA / m
    # What c₁ gives M_target?
    c1_m = (M_target - X_m**2/2 - c_neg1_m/X_m - c_0_m) / X_m
    m_kappa = m / p
    diff = c1_m - m_kappa
    match = "YES" if abs(diff) < 1e-10 else "no"
    print(f"{m:4d} | {c1_m:12.8f} | {m_kappa:8.4f} | {match:>12s} | {diff:12.6e}")

print(f"""
RESULT: c₁ = m/p ONLY for m=3 (our case). For other m values,
the c₁ needed to hit M_target is NOT m·κ.

This means c₁ = n·κ is specific to the (n=3, p=5) solution —
it's not a general identity that works for arbitrary exponent.

BUT this is expected: the mass formula was constructed for (3,5).
The test confirms self-consistency but doesn't prove c₁ = n·κ.
""")

# ═══════════════════════════════════════════════════════════════════
# TEST 4: ADDITIVITY — IS THE LINEAR TERM ADDITIVE IN QUARK COUNT?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("TEST 4: ADDITIVITY OF THE LINEAR TERM")
print("═" * 72)

# If c₁ = n·κ, then the linear contribution c₁·X = n·κ·X = n·(X/p)
# This is n copies of X/p = 12.
#
# Is there a sense in which adding one more quark (n→n+1) adds
# exactly κ to c₁?
#
# For the THREE Diophantine solutions:

solutions = [(3, 5), (4, 3), (6, 2)]

print(f"\n{'n':>4s} {'p':>4s} | {'X':>6s} | {'c₁=n/p':>10s} | {'c₁·X':>10s} | {'(c₁·X)/n':>10s}")
print("-" * 60)
for nn, pp in solutions:
    XX = nn * pp * (pp - 1)
    c1 = nn / pp
    print(f"{nn:4d} {pp:4d} | {XX:6d} | {c1:10.6f} | {c1*XX:10.4f} | {c1*XX/nn:10.4f}")

print(f"""
Per-quark linear contribution c₁·X/n:
  (3,5): 12.0000  = X/p = p·(p-1) = 20... wait, 60/5 = 12. And p·(p-1) = 20.
  (4,3): 8.0000   = X/p = 24/3 = 8. And p·(p-1) = 6.
  (6,2): 6.0000   = X/p = 12/2 = 6. And p·(p-1) = 2.

So per-quark linear = X/p = n·(p-1) for each solution. ✓
And X/p = n·p·(p-1)/p = n·(p-1).

So per-quark linear = n·(p-1)? That's n-dependent.
Actually: c₁·X/n = (n/p)·X/n = X/p = n·p·(p-1)/p = n·(p-1).

Hmm, that's still n-dependent. Per quark = n·(p-1), not (p-1).
That's because X itself depends on n.

Per quark in terms of κ: c₁/n = κ = 1/p. This IS n-independent.
Each quark contributes κ = 1/p to the coefficient. ✓
""")

# ═══════════════════════════════════════════════════════════════════
# FINAL ASSESSMENT
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 72)
print("ANGLE 1: FINAL ASSESSMENT")
print("═" * 72)

print(f"""
FACTORIZATION THEOREM STATUS: STRUCTURAL ARGUMENT, NOT PROOF

What it establishes:
  ✓ c₁ = n·κ decomposes into n identical per-quark contributions
  ✓ Per-quark coupling κ = 1/p is n-independent (universal)
  ✓ The tanh^n = [tanh]^n structure naturally gives n copies
  ✓ Elasticity at fixed points factorizes: n × single-quark
  ✓ All three Diophantine solutions follow c₁ = n/p consistently

What it CANNOT establish:
  ✗ WHY the mass formula has a linear term in the first place
  ✗ WHY the linear coefficient equals the unstable-point coupling
  ✗ The mass formula is an ANSATZ — without deriving M, can't derive c₁

VERDICT: Factorization is the strongest PHYSICAL argument for c₁ = n·κ.
It explains the structure but can't prove it. The proof requires
deriving the mass formula from the recursion (Angle 2).

CONTRIBUTION TO PAPER: Adds to Section 8 as supporting evidence.
Upgrades c₁ from "Occam selection" to "Occam + mean-field +
cross-virial + factorization" — four independent motivations.
But still not a theorem.

Moving to ANGLE 2: Derive M from the recursion.
""")

print("=" * 72)
print("END ANGLE 1")
print("=" * 72)
