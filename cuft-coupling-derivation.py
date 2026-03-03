#!/usr/bin/env python3
"""
CUFT-RASP: DERIVING κ = 1/√Γ — THE MISSING EQUATION
=====================================================
YASA PRESENTS — 2026-02-12

THE GOAL: Derive κ = 1/√Γ from first principles.
If this works, the ENTIRE chain locks: κ → Γ=25 → X=60 → proton mass.

PREVIOUS FAILED ROUTES:
  A: Single-oscillator fixed point → κ_eff ≈ 0 (tanh saturates)
  B: Marginal stability → κ ≈ 0.67 for all Γ (wrong)
  C: Confinement intuition → physical but unformalized

NEW APPROACHES:
  D: Information-theoretic (mutual information of 3 coupled channels)
  E: Renormalization / scale invariance of the coupling
  F: Topological (winding number / degree of the 3-body map)
  G: Variational (minimize baryon mass w.r.t. coupling)
  H: Dimensional analysis / scaling symmetry
  I: Nonlinear resonance condition
  J: Self-similar fixed point of the RG flow
"""

import numpy as np
from scipy.optimize import brentq, fsolve, minimize_scalar
from scipy.linalg import eigvals
from scipy.integrate import quad
import warnings
warnings.filterwarnings('ignore')

lam = 0.008097  # damping

def f(x, G):
    return G * np.tanh(x)**3 - lam * x

def df_dx(x, G):
    t = np.tanh(x)
    return 3 * G * t**2 * (1 - t**2) - lam

def exact_fp(G):
    """Positive fixed point of f(x) = x."""
    def g(x): return G * np.tanh(x)**3 - lam * x - x
    try:
        return brentq(g, 0.1, G * 1.5)
    except:
        try:
            r = fsolve(g, G * 0.99, full_output=True)
            if r[2] == 1: return r[0][0]
        except:
            pass
    return None

print("=" * 70)
print("CUFT-RASP: DERIVING κ = 1/√Γ — THE MISSING EQUATION")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# ROUTE D: INFORMATION-THEORETIC APPROACH
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE D: INFORMATION-THEORETIC — CHANNEL CAPACITY")
print("=" * 70)

print("""
IDEA: The gated cubic tanh³(x) acts as a COMMUNICATION CHANNEL.
Input: amplitude x. Output: Γ·tanh³(x).
The channel saturates at ±Γ. The "information" that gets through
depends on the operating point.

For a channel y = Γ·tanh³(x), the gain is:
  dy/dx = 3Γ·tanh²(x)·sech²(x)

At the fixed point x*, this gain is the Jacobian: a = f'(x*).

CHANNEL CAPACITY is related to the SNR = (signal)²/(noise)²
  Signal = x* (the fixed-point amplitude)
  Noise = related to the fluctuation around x*

For 3 coupled channels (quarks), the TOTAL information capacity
must be shared. If each channel has capacity C(Γ), then:
  Total capacity = 3·C(Γ)

The coupling κ represents the fraction of capacity LOST to
inter-channel correlation (mutual information between quarks).

IF mutual information scales as √Γ (geometric mean of signal²):
  κ = I_mutual / C_total ∝ 1/√Γ
""")

# Compute the "gain" at fixed point for various Γ
print("Channel gain analysis:")
print(f"{'Γ':>6} {'x*':>10} {'f\'(x*)':>10} {'tanh(x*)':>10} {'sech²(x*)':>12} {'3Γ·t²·s²':>12} {'√Γ':>8}")
print("-" * 75)

for G in [4, 9, 16, 25, 36, 49, 64, 100]:
    xs = exact_fp(G)
    if xs:
        t = np.tanh(xs)
        s2 = 1 - t**2
        gain = 3 * G * t**2 * s2
        fprime = gain - lam
        print(f"{G:6d} {xs:10.4f} {fprime:10.6f} {t:10.8f} {s2:12.2e} {gain:12.6f} {np.sqrt(G):8.4f}")

print()
print("OBSERVATION: f'(x*) → -λ for all large Γ (gain → 0 because sech² → 0).")
print("The channel is SATURATED. Almost no information gets through.")
print("This is WHY Route A failed — the linearized dynamics are trivial.")
print()
print("NEW INSIGHT: The coupling isn't about the LINEAR response.")
print("It's about the NONLINEAR structure — the shape of tanh³ AWAY from x*.")

# ═══════════════════════════════════════════════════════════════
# ROUTE E: RENORMALIZATION GROUP APPROACH
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE E: RENORMALIZATION — SCALE TRANSFORMATION OF THE RECURSION")
print("=" * 70)

print("""
IDEA: Under rescaling x → x/s, the recursion transforms.
Find the scaling s at which the 3-body system is SCALE-INVARIANT.

The recursion: x' = Γ·tanh³(x) - λ·x

Under x → x/s:
  (x'/s) = Γ·tanh³(x/s) - λ·(x/s)

For this to be the SAME recursion with rescaled parameters:
  x'/s = Γ_eff·tanh³(x/s) - λ·(x/s)

For large x (where tanh → 1): x' ≈ Γ - λx
  Rescaled: x'/s ≈ Γ/s - λx/s... only consistent if Γ → Γ/s.

For SMALL x (where tanh(x) ≈ x): x' ≈ Γx³ - λx = (Γx² - λ)x
  Rescaled: x'/s ≈ Γ(x/s)³ - λ(x/s) = Γx³/s³ - λx/s
  For consistency: need Γ/s³ · s = Γ, i.e., s² = 1 → s = 1.

  NO natural scale transformation for the cubic.

ALTERNATIVE: Consider the AMPLITUDE RATIO between scales.
  If the 3-body amplitude is X and each quark is x*, then:
  X = 3x* (uncoupled) or X = 3x*(1-κ) (coupled)

  The coupling κ relates TWO scales: the individual (x*) and collective (X).

  RG: The coupling at scale X should relate to coupling at scale x*:
    κ(X) = κ₀ · (X/x*)^β for some anomalous dimension β.
""")

# Test: what scaling relates x* and X for various Γ?
print("Scale analysis:")
print(f"{'Γ':>6} {'x*':>10} {'X=3x*(1-κ)':>12} {'X/x*':>8} {'ln(X/x*)':>10} {'X/x*-3':>10}")
print("-" * 60)

for G in [4, 9, 16, 25, 36, 49, 64, 100]:
    xs = exact_fp(G)
    p = np.sqrt(G)
    kappa = 1/p
    X = 3 * p * (p - 1)  # = 3Γ(1-1/√Γ)
    if xs:
        print(f"{G:6d} {xs:10.4f} {X:12.4f} {X/xs:8.4f} {np.log(X/xs):10.4f} {X/xs-3:10.4f}")

# ═══════════════════════════════════════════════════════════════
# ROUTE F: TOPOLOGICAL — THE WINDING NUMBER
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE F: TOPOLOGICAL — WINDING NUMBER OF 3-BODY MAP")
print("=" * 70)

print("""
IDEA: The 3-body map F: R³ → R³ defined by:
  F(x₁,x₂,x₃) = (f(x₁)+ε(x₂+x₃), f(x₂)+ε(x₁+x₃), f(x₃)+ε(x₁+x₂))

has a topological degree (winding number) that counts fixed points
with orientation. The DEGREE is an integer invariant.

For the SYMMETRIC restriction (x₁=x₂=x₃=x):
  F_sym(x) = f(x) + 2εx = Γ·tanh³(x) + (2ε-λ)x

The winding number of g(x) = F_sym(x) - x on a large interval
counts the number of signed fixed points.

KEY: The winding number changes at BIFURCATION points where a
fixed point is born/dies. These bifurcations may select specific Γ.
""")

def winding_number(G, eps, x_max=500, n_pts=100000):
    """Compute winding number of g(x) = F_sym(x) - x on [-x_max, x_max]."""
    def g(x):
        return G * np.tanh(x)**3 + (2*eps - lam)*x - x

    # Count sign changes
    xs = np.linspace(-x_max, x_max, n_pts)
    gs = np.array([g(x) for x in xs])
    sign_changes = np.sum(np.diff(np.sign(gs)) != 0)

    # Winding = number of zeros with sign of derivative
    return sign_changes // 2  # Each zero-crossing pair = 1 winding

# For κ = 1/√Γ, compute ε and winding number
print("Winding number analysis (κ = 1/√Γ):")
print(f"{'Γ':>6} {'κ':>8} {'ε':>12} {'# FPs':>6}")
print("-" * 40)

for G in [4, 9, 16, 25, 36, 49]:
    p = np.sqrt(G)
    kappa = 1/p
    # From X = 3Γ(1-κ), and x* = Γ/(1+λ_eff):
    # λ_eff = λ - 2ε, and x* = Γ(1-κ)
    # So Γ/(1 + λ - 2ε) = Γ(1-κ)
    # 1 + λ - 2ε = 1/(1-κ)
    # ε = (λ - 1/(1-κ) + 1)/2 = (1 + λ - 1/(1-κ))/2
    eps = (1 + lam - 1/(1-kappa)) / 2
    w = winding_number(G, eps)
    print(f"{G:6d} {kappa:8.4f} {eps:12.6f} {w:6d}")

# ═══════════════════════════════════════════════════════════════
# ROUTE G: VARIATIONAL — MINIMIZE MASS w.r.t. κ
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE G: VARIATIONAL — MINIMIZE BARYON MASS w.r.t. κ")
print("=" * 70)

print("""
IDEA: Nature selects the GROUND STATE — the configuration that
minimizes energy. If the baryon mass M(Γ, κ) depends on κ,
then the physical κ is the one that minimizes M.

This is the VARIATIONAL PRINCIPLE: δM/δκ = 0.

For the 3-body system at given Γ:
  X(κ) = 3Γ(1-κ)
  M(κ) = X²/2 + corrections = 9Γ²(1-κ)²/2 + ...

If we minimize M w.r.t. κ:
  dM/dκ = -9Γ²(1-κ) + d(corrections)/dκ = 0

For the LEADING term only: M ≈ X²/2 → dM/dκ < 0 always.
So the leading term ALWAYS wants κ = 0 (maximum amplitude).

The corrections must provide a RESTORING force at finite κ.
This suggests the corrections grow as κ increases, balancing.

LET'S TRY: M = X²/2 + 3Γ/X (binding energy per quark redistributed)
  = 9Γ²(1-κ)²/2 + 3Γ/(3Γ(1-κ))
  = 9Γ²(1-κ)²/2 + 1/(1-κ)

  dM/dκ = -9Γ²(1-κ) + 1/(1-κ)² = 0
  9Γ²(1-κ)³ = 1
  (1-κ)³ = 1/(9Γ²)
  1-κ = (9Γ²)^(-1/3)
  κ = 1 - 1/(9Γ²)^(1/3)
""")

print("Variational κ from M = X²/2 + 1/(1-κ):")
print(f"{'Γ':>6} {'κ_var':>10} {'1/√Γ':>10} {'Ratio':>10}")
print("-" * 40)
for G in [4, 9, 16, 25, 36, 49, 100]:
    kvar = 1 - 1/(9*G**2)**(1.0/3)
    ktar = 1/np.sqrt(G)
    print(f"{G:6d} {kvar:10.6f} {ktar:10.6f} {kvar/ktar:10.4f}")

print()
print("  Doesn't give κ = 1/√Γ. Wrong correction form.")
print()

# Try different correction forms
print("SYSTEMATIC SEARCH: What correction term gives κ = 1/√Γ from dM/dκ = 0?")
print()
print("M = 9Γ²(1-κ)²/2 + C(Γ)·h(κ)")
print("dM/dκ = -9Γ²(1-κ) + C(Γ)·h'(κ) = 0")
print("At κ = 1/√Γ: 1-κ = 1-1/√Γ = (√Γ-1)/√Γ")
print()
print("So: 9Γ²(√Γ-1)/√Γ = C(Γ)·h'(1/√Γ)")
print("    9Γ^(3/2)(√Γ-1) = C(Γ)·h'(1/√Γ)")
print()

# What if correction = Γ^(3/2)/(1-κ)?
# h(κ) = 1/(1-κ), h'(κ) = 1/(1-κ)²
# C·1/((√Γ-1)/√Γ)² = C·Γ/(√Γ-1)²
# Need: 9Γ^(3/2)(√Γ-1) = C·Γ/(√Γ-1)²
# C = 9Γ^(1/2)(√Γ-1)³ ... Γ-dependent, not structural

# What if correction = Γ·ln(1/(1-κ))?
# h(κ) = -ln(1-κ), h'(κ) = 1/(1-κ)
# C·√Γ/(√Γ-1) = 9Γ^(3/2)(√Γ-1)
# C = 9Γ(√Γ-1)²/√Γ ... still Γ-dependent

# Let's think differently.
# If κ = 1/√Γ minimizes M, what does M(Γ,κ) look like?

print("Let me try: what FORM of M(κ) has minimum at κ = 1/√Γ for ALL Γ?")
print()
print("Require: dM/dκ|_{κ=1/√Γ} = 0 for all Γ")
print()
print("Leading term: M₀ = 9Γ²(1-κ)²/2")
print("  dM₀/dκ = -9Γ²(1-κ)")
print("  At κ=1/√Γ: dM₀/dκ = -9Γ²(√Γ-1)/√Γ = -9Γ^(3/2)(√Γ-1)")
print()
print("The correction M₁ must satisfy: dM₁/dκ = +9Γ^(3/2)(√Γ-1) at κ=1/√Γ")
print()
print("If M₁ = a·Γ^α·κ^β, then dM₁/dκ = a·β·Γ^α·κ^(β-1)")
print("At κ=1/√Γ = Γ^(-1/2):")
print("  a·β·Γ^α·Γ^(-(β-1)/2) = 9Γ^(3/2)(√Γ-1)")
print("  a·β·Γ^(α-(β-1)/2) = 9Γ^(3/2)(√Γ-1)")
print()
print("For large Γ: √Γ-1 ≈ √Γ, so RHS ≈ 9Γ²")
print("  α - (β-1)/2 = 2, and a·β = 9")
print()
print("Example: β = 2, α = 5/2, a = 9/2")
print("  M₁ = (9/2)·Γ^(5/2)·κ²")
print()
print("Check: M = 9Γ²(1-κ)²/2 + (9/2)Γ^(5/2)κ²")

# Verify this variational form
print()
print("Verification — does M = 9Γ²(1-κ)²/2 + (9/2)Γ^(5/2)κ² have min at κ=1/√Γ?")
print()

def M_var(kappa, Gamma):
    return 9*Gamma**2*(1-kappa)**2/2 + 4.5*Gamma**2.5*kappa**2

print(f"{'Γ':>6} {'κ_min':>10} {'1/√Γ':>10} {'Match?':>8}")
print("-" * 40)
for G in [4, 9, 16, 25, 36, 49, 100]:
    result = minimize_scalar(lambda k: M_var(k, G), bounds=(0.01, 0.99), method='bounded')
    kmin = result.x
    ktarget = 1/np.sqrt(G)
    match = "YES" if abs(kmin - ktarget) < 0.001 else "no"
    print(f"{G:6d} {kmin:10.6f} {ktarget:10.6f} {match:>8}")

# ═══════════════════════════════════════════════════════════════
# ROUTE G (continued): THE CORRECTION TERM MEANING
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE G RESULT: VARIATIONAL PRINCIPLE WORKS!")
print("=" * 70)

print("""
★ BREAKTHROUGH: M = (9/2)Γ²(1-κ)² + (9/2)Γ^(5/2)κ² has minimum at κ = 1/√Γ!

Let's verify the calculus:
  dM/dκ = -9Γ²(1-κ) + 9Γ^(5/2)κ = 0
  9Γ²(1-κ) = 9Γ^(5/2)κ
  Γ²(1-κ) = Γ^(5/2)κ
  (1-κ)/κ = Γ^(1/2)
  1/κ - 1 = √Γ
  1/κ = √Γ + 1
  κ = 1/(√Γ + 1)

Wait — that gives κ = 1/(√Γ+1), NOT κ = 1/√Γ!

For Γ=25: κ = 1/6 ≈ 0.1667, but we want κ = 1/5 = 0.2.
Close but NOT exact. Let me recalculate.
""")

# The exact minimization gives κ = 1/(√Γ+1), not 1/√Γ!
# But these are CLOSE. Let me find what correction gives EXACT 1/√Γ.

print("RECALCULATION:")
print()
print("For M = A·(1-κ)² + B·κ^α:")
print("  dM/dκ = -2A(1-κ) + Bα·κ^(α-1) = 0")
print("  At κ = 1/√Γ = 1/p:")
print("    2A(1-1/p) = Bα/p^(α-1)")
print("    2A(p-1)/p = Bα/p^(α-1)")
print("    2A(p-1)·p^(α-2) = Bα")
print()
print("  For A = (9/2)Γ² = (9/2)p⁴:")
print("    9p⁴(p-1)p^(α-2) = Bα")
print("    9p^(α+2)(p-1) = Bα")
print()
print("  For this to work for ALL p, B must depend on p (= √Γ).")
print("  Unless we choose α carefully.")
print()

# Let me try M = (9/2)Γ²(1-κ)² + C·Γ^γ·κ^α and solve for α, γ
# such that min is at κ = 1/√Γ for ALL Γ.

# dM/dκ = -9Γ²(1-κ) + Cα·Γ^γ·κ^(α-1) = 0 at κ = Γ^(-1/2)
# 9Γ²(1 - Γ^(-1/2)) = Cα·Γ^γ·Γ^(-(α-1)/2)
# 9Γ²(1 - Γ^(-1/2)) = Cα·Γ^(γ-(α-1)/2)

# LHS = 9Γ² - 9Γ^(3/2)
# RHS = Cα·Γ^(γ-(α-1)/2)

# For this to hold for ALL Γ, we need TWO terms on RHS or a single power match.
# Single power: can only match one of the two terms.

# Match the DOMINANT term (9Γ²):
# γ - (α-1)/2 = 2  →  γ = 2 + (α-1)/2 = (α+3)/2
# Cα = 9

# Then RHS = 9Γ² but LHS = 9Γ² - 9Γ^(3/2)
# Mismatch by -9Γ^(3/2).

# So we need a SECOND correction term to cancel this.

print("INSIGHT: Single power-law correction can't do it.")
print("We need TWO correction terms.")
print()
print("M = (9/2)Γ²(1-κ)² + C₁·Γ^γ₁·κ^α₁ + C₂·Γ^γ₂·κ^α₂")
print()
print("Let's try the PHYSICS more carefully.")
print()

# ═══════════════════════════════════════════════════════════════
# ROUTE H: DIMENSIONAL ANALYSIS / SCALING SYMMETRY
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE H: THE COUPLING AS A GEOMETRIC MEAN")
print("=" * 70)

print("""
GEOMETRIC INSIGHT:

In the 3-body system, each quark has amplitude x* ≈ Γ.
The COLLECTIVE amplitude is X = 3x*(1-κ).

κ represents the fraction of individual amplitude that is
"sacrificed" to form the bound state.

GEOMETRIC MEAN ARGUMENT:
  Individual scale: Γ (the drive strength)
  Collective scale: X/3 = Γ(1-κ) (amplitude per quark in bound state)

  The coupling reduction is the ratio:
    x*_bound / x*_free = (1-κ) = X/(3Γ)

  In the GATED system, the amplitude is gated by tanh³.
  The gating function tanh³(x) ≈ 1 for x ≫ 1.
  The "gate opens" at x ∼ 1 (where tanh ≈ 0.76).

  The FRACTION of the amplitude that is "above the gate":
    (x* - x_gate) / x* ≈ (Γ - 1)/Γ = 1 - 1/Γ

  The fraction "inside the gate":
    x_gate / x* ≈ 1/Γ

  The GEOMETRIC MEAN of "above" and "inside":
    √((1-1/Γ) · (1/Γ)) = √((Γ-1)/Γ²) = √(Γ-1)/Γ

  For large Γ: ≈ 1/√Γ

  So κ = √(Γ-1)/Γ ≈ 1/√Γ !
""")

print("Testing: κ_geometric = √(Γ-1)/Γ vs 1/√Γ")
print(f"{'Γ':>6} {'√(Γ-1)/Γ':>12} {'1/√Γ':>12} {'Ratio':>8} {'Diff':>10}")
print("-" * 50)
for G in [4, 9, 16, 25, 36, 49, 100, 625]:
    kg = np.sqrt(G-1)/G
    kt = 1/np.sqrt(G)
    print(f"{G:6d} {kg:12.6f} {kt:12.6f} {kg/kt:8.4f} {kg-kt:10.6f}")

print()
print("CLOSE but not exact. κ_geo = √(Γ-1)/Γ, not 1/√Γ.")
print("Ratio approaches 1 for large Γ, but differs at small Γ.")
print()

# What if it's not geometric mean of fractions, but of AMPLITUDES?
print("ALTERNATIVE: Geometric mean of amplitudes")
print()
print("  Individual amplitude: x* ≈ Γ")
print("  Gate transition width: ~1 (where tanh' is maximal)")
print("  Geometric mean: √(Γ · 1) = √Γ")
print("  Coupling fraction: (gate width)/(geometric mean) = 1/√Γ")
print()
print("  This gives κ = 1/√Γ EXACTLY.")
print()
print("  PHYSICAL MEANING:")
print("  The 'gate' (tanh³ saturation) operates at scale ~1.")
print("  The oscillator operates at scale ~Γ.")
print("  The coupling between 3 oscillators is determined by the")
print("  GEOMETRIC MEAN of these two scales: √(Γ·1) = √Γ.")
print("  The coupling FRACTION is 1/√Γ.")

# ═══════════════════════════════════════════════════════════════
# ROUTE I: NONLINEAR RESONANCE
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE I: NONLINEAR RESONANCE — MATCHING CONDITION")
print("=" * 70)

print("""
IDEA: In the coupled 3-body system, the NONLINEAR response of
each oscillator to the coupling signal must satisfy a RESONANCE
condition for stable bound state formation.

The coupling signal each quark receives from the other two:
  s = ε(x₂ + x₃) = 2ε·x*  (at symmetric FP)

The NONLINEAR GAIN of the oscillator at the operating point:
  G_nl = Γ·d(tanh³)/dx|_{x*} = 3Γ·tanh²(x*)·sech²(x*)

For x* large: tanh(x*) → 1, sech²(x*) → 4e^{-2x*}
  G_nl → 12Γ·e^{-2x*}

This is EXPONENTIALLY small — the oscillator is saturated.

But the INTEGRAL gain over a perturbation period is different.
Consider: what happens when x is perturbed from x* to x* - δ?

The response: Δf = f(x*-δ) - f(x*) ≈ f'(x*)·(-δ) + f''(x*)·δ²/2

f''(x*) = d/dx[3Γt²s² - λ] = 3Γ·d(t²s²)/dx
        = 3Γ·[2t·s²·s² + t²·2s·(-2ts²)]  ... complicated

Let me try a different NONLINEAR approach.
""")

# ═══════════════════════════════════════════════════════════════
# ROUTE J: CURVATURE MATCHING — THE SECOND DERIVATIVE
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE J: CURVATURE MATCHING — f''(x*) AND THE COUPLING")
print("=" * 70)

print("""
IDEA: The coupling κ is determined by matching the CURVATURE
(second derivative) of the potential at the fixed point.

f(x) = Γ·tanh³(x) - λx
f'(x) = 3Γ·tanh²(x)·sech²(x) - λ
f''(x) = 3Γ·[2·tanh(x)·sech⁴(x) - 4·tanh³(x)·sech²(x)]
       = 6Γ·tanh(x)·sech²(x)·[sech²(x) - 2·tanh²(x)]
       = 6Γ·tanh(x)·sech²(x)·[1 - 3·tanh²(x)]

At x*: tanh(x*) ≈ 1, sech²(x*) ≈ 4e^{-2x*}
  f''(x*) ≈ 6Γ·1·4e^{-2x*}·[1-3] = -48Γ·e^{-2x*}

Again exponentially small. The curvature doesn't help for large Γ.
""")

# Let's compute f'' at the inflection point instead
print("What about the curvature at the INFLECTION POINT of tanh³?")
print()
print("The inflection of tanh³(x) occurs where d²(tanh³)/dx² = 0.")
print("tanh³ has inflection at x = 0 AND at x where 1 - 3tanh²(x) = 0")
print("  tanh(x) = 1/√3 → x = atanh(1/√3) = 0.6585")
print()

x_infl = np.arctanh(1/np.sqrt(3))
print(f"Inflection point: x_infl = {x_infl:.6f}")
print(f"tanh³(x_infl) = {np.tanh(x_infl)**3:.6f} = (1/√3)³ = {1/3/np.sqrt(3):.6f}")
print()
print(f"For Γ=25: f(x_infl) = 25·{np.tanh(x_infl)**3:.6f} - 0.008097·{x_infl:.4f}")
print(f"         = {25*np.tanh(x_infl)**3 - lam*x_infl:.6f}")
print(f"  x_infl/Γ = {x_infl/25:.6f}")
print(f"  x_infl/√Γ = {x_infl/5:.6f}")
print()

# ═══════════════════════════════════════════════════════════════
# ROUTE K: THE CRITICAL INSIGHT — √Γ AS THE GEOMETRIC SCALE
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE K: √Γ AS THE NATURAL SCALE OF THE GATED CUBIC")
print("=" * 70)

print("""
Let me examine the structure of f(x) = Γ·tanh³(x) more carefully.

The function Γ·tanh³(x) has THREE distinct regimes:
  x ≪ 1:     Γ·tanh³(x) ≈ Γ·x³  (cubic growth)
  x ∼ 1:     Γ·tanh³(x) = transition (the "gate")
  x ≫ 1:     Γ·tanh³(x) ≈ Γ     (saturation)

The fixed point x* ≈ Γ is in the SATURATION regime.

NOW: Consider the ENERGY stored in the gate transition itself.
The gate transition happens over x ∈ [0, ~3] (where tanh goes 0→~0.995).

The "gating energy" = ∫₀^∞ [Γ - Γ·tanh³(x)] dx
                    = Γ · ∫₀^∞ [1 - tanh³(x)] dx

Let me compute this integral.
""")

# Compute ∫₀^∞ [1 - tanh³(x)] dx
def integrand_gate(x):
    return 1 - np.tanh(x)**3

gate_integral, _ = quad(integrand_gate, 0, 50)
print(f"∫₀^∞ [1 - tanh³(x)] dx = {gate_integral:.6f}")
print(f"  = ln(2) + 1/2 = {np.log(2) + 0.5:.6f}")  # Known result
print()

# What about the "gate energy" relative to the total?
print("For Γ = 25:")
print(f"  Gate energy: Γ · ∫[1-tanh³] dx = 25 × {gate_integral:.4f} = {25*gate_integral:.4f}")
print(f"  Total energy: x*² ≈ Γ² = {25**2}")
print(f"  Gate fraction: {25*gate_integral/625:.6f}")
print(f"  √(Gate fraction): {np.sqrt(25*gate_integral/625):.6f}")
print()

# Now: the KEY idea
print("=" * 70)
print("★ THE KEY GEOMETRIC ARGUMENT")
print("=" * 70)
print()
print("Consider the recursion x' = Γ·tanh³(x) - λx")
print("At the fixed point, x* ≈ Γ.")
print()
print("The function tanh³(x) maps [0,∞) → [0,1).")
print("It has a characteristic transition at scale ~1.")
print("The drive Γ amplifies this to [0,Γ).")
print()
print("There are TWO natural scales in the problem:")
print(f"  Scale 1: The DRIVE amplitude = Γ")
print(f"  Scale 2: The GATE width = 1 (from tanh)")
print()
print("The GEOMETRIC MEAN of these scales: √(Γ·1) = √Γ")
print()
print("In the 3-body system, each oscillator 'sees' the others")
print("through the nonlinear gate. The coupling is filtered by tanh³.")
print()
print("The EFFECTIVE coupling strength is determined by the scale at")
print("which the gate can transmit information between oscillators.")
print("This scale is √Γ (geometric mean of drive and gate).")
print()
print("The coupling FRACTION relative to the drive:")
print("  κ = (coupling scale) / (drive scale) = √Γ / Γ = 1/√Γ")
print()
print("This is the GEOMETRIC MEAN ARGUMENT for κ = 1/√Γ.")
print()

# ═══════════════════════════════════════════════════════════════
# ROUTE L: VERIFY NUMERICALLY — THE NONLINEAR COUPLING
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE L: NUMERICAL VERIFICATION — NONLINEAR COUPLING SCALE")
print("=" * 70)

print("""
If κ = 1/√Γ comes from the geometric mean of drive (Γ) and gate (1),
then the NONLINEAR transfer function at scale √Γ should be special.

Test: What is tanh³(√Γ) for various Γ?
""")

print(f"{'Γ':>6} {'√Γ':>8} {'tanh³(√Γ)':>12} {'1-tanh³(√Γ)':>14} {'1/√Γ':>10} {'Ratio':>10}")
print("-" * 65)
for G in [4, 9, 16, 25, 36, 49, 100]:
    p = np.sqrt(G)
    t3 = np.tanh(p)**3
    deficit = 1 - t3
    kappa = 1/p
    print(f"{G:6d} {p:8.2f} {t3:12.8f} {deficit:14.2e} {kappa:10.4f} {deficit/kappa:10.4e}")

print()
print("tanh³(√Γ) ≈ 1 for all Γ ≥ 4. The nonlinear transfer is saturated")
print("at scale √Γ. This doesn't directly give the coupling.")
print()

# But what about the DERIVATIVE at scale √Γ?
print("What about the gain (derivative) at scale √Γ?")
print(f"{'Γ':>6} {'√Γ':>8} {'f\'(√Γ,Γ)':>12} {'Γ·f\'(√Γ)':>12} {'1/√Γ':>10}")
print("-" * 55)
for G in [4, 9, 16, 25, 36, 49, 100]:
    p = np.sqrt(G)
    fp = df_dx(p, G)
    print(f"{G:6d} {p:8.2f} {fp:12.6f} {G*fp:12.4f} {1/p:10.4f}")

print()

# What about the TRANSFER FUNCTION: output/input at x = √Γ?
print("Transfer function T(√Γ) = f(√Γ)/√Γ:")
print(f"{'Γ':>6} {'√Γ':>8} {'f(√Γ)':>10} {'T=f(√Γ)/√Γ':>12} {'T/Γ':>10} {'1-T/Γ':>10} {'1/√Γ':>10}")
print("-" * 75)
for G in [4, 9, 16, 25, 36, 49, 100]:
    p = np.sqrt(G)
    fx = f(p, G)
    T = fx / p
    print(f"{G:6d} {p:8.2f} {fx:10.4f} {T:12.4f} {T/G:10.6f} {1-T/G:10.6f} {1/p:10.4f}")

print()
print("INTERESTING: 1 - T(√Γ)/Γ approaches 1/√Γ for large Γ!")
print("  T(√Γ)/Γ = f(√Γ)/(√Γ·Γ)")
print("  = [Γ·tanh³(√Γ) - λ·√Γ] / (Γ^(3/2))")
print("  ≈ [Γ·1 - λ·√Γ] / (Γ^(3/2))")
print("  = 1/√Γ - λ/Γ")
print("  = (1 - λ/√Γ)/√Γ")
print()
print("  So 1 - T/Γ ≈ 1 - 1/√Γ + λ/Γ ≈ 1 - 1/√Γ")
print("  This means 1 - f(√Γ)/(Γ·√Γ) ≈ 1 - 1/√Γ = 1 - κ")
print()
print("  NOT quite the relation we need.")

# ═══════════════════════════════════════════════════════════════
# ROUTE M: ENERGY PARTITION — 3 QUARKS SHARING NONLINEARITY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE M: ENERGY PARTITION IN THE 3-BODY NONLINEAR SYSTEM")
print("=" * 70)

print("""
DIFFERENT APPROACH: Instead of deriving κ from local properties,
derive it from a GLOBAL constraint on the 3-body system.

CONSTRAINT: The total "nonlinear action" of the 3-body system
must be self-consistent.

For a single oscillator at fixed point x*:
  Drive:    Γ·tanh³(x*) ≈ Γ  (saturated)
  Damping:  (1+λ)·x* ≈ (1+λ)·Γ ≈ Γ + λΓ
  Balance:  Γ = Γ + λΓ... wait, this is just x* = Γ/(1+λ).

For the 3-body COUPLED system at symmetric FP (each oscillator at x_b):
  Per oscillator: Γ·tanh³(x_b) - λ·x_b + 2ε·x_b = x_b
  → Γ·tanh³(x_b) = (1 + λ - 2ε)·x_b

  For large x_b: x_b ≈ Γ/(1 + λ - 2ε)

  X = 3x_b ≈ 3Γ/(1 + λ - 2ε) = 3Γ(1-κ) where 1-κ = 1/(1+λ-2ε)

SO: κ = 1 - 1/(1 + λ - 2ε). The coupling κ is set by ε.

THE QUESTION BECOMES: What determines ε?

IN QCD: The coupling constant αs ~ 1 at the confinement scale.
The coupling is NOT perturbative — it's ORDER 1.

ANALOGY: In our system, ε should be of order comparable to the
other scales in the problem.

The scales available:
  λ ≈ 0.008  (damping)
  Γ = 25     (drive)
  1          (tanh gate)

If ε is determined by the RATIO of gate to drive:
  ε ~ 1/Γ?  → κ ~ 2/Γ (too small)
  ε ~ 1/√Γ? → κ ~ 2/√Γ (close!)
  ε ~ √Γ?   → κ ~ 2√Γ  (too big, unstable)
""")

# What value of ε gives κ = 1/√Γ?
print("Required ε for κ = 1/√Γ:")
print(f"{'Γ':>6} {'κ=1/√Γ':>10} {'1/(1-κ)':>10} {'1+λ-2ε':>10} {'ε':>12} {'ε/Γ':>10} {'ε·√Γ':>10}")
print("-" * 75)
for G in [4, 9, 16, 25, 36, 49, 100]:
    p = np.sqrt(G)
    kappa = 1/p
    inv_1mk = 1/(1-kappa)
    eff = inv_1mk
    eps = (1 + lam - eff)/2
    print(f"{G:6d} {kappa:10.4f} {inv_1mk:10.4f} {eff:10.4f} {eps:12.6f} {eps/G:10.6f} {eps*p:10.4f}")

print()
print("NOTE: ε is NEGATIVE (attractive coupling) and its magnitude grows with Γ.")
print("  |ε|·√Γ is roughly constant for large Γ.")
print()

# The key: ε ≈ -(√Γ)/(2Γ) = -1/(2√Γ)? Let's check.
print("Check: is ε ≈ -1/(2(√Γ-1))?")
print(f"{'Γ':>6} {'ε_actual':>12} {'-1/(2(√Γ-1))':>14} {'Ratio':>10}")
print("-" * 45)
for G in [4, 9, 16, 25, 36, 49, 100]:
    p = np.sqrt(G)
    kappa = 1/p
    eff = 1/(1-kappa)
    eps_actual = (1 + lam - eff)/2
    eps_guess = -1/(2*(p-1))
    print(f"{G:6d} {eps_actual:12.6f} {eps_guess:14.6f} {eps_actual/eps_guess:10.4f}")

print()
print("YES! ε ≈ -1/(2(√Γ-1)) for all Γ (ratio → 1 as Γ → ∞)")
print("The exact relation (ignoring λ):")
print("  ε = (1 - √Γ/(√Γ-1))/2 = (√Γ-1-√Γ)/(2(√Γ-1)) = -1/(2(√Γ-1))")
print()
print("So the coupling ε = -1/(2(p-1)) where p = √Γ.")
print("  p=5: ε = -1/8 = -0.125")
print("  Actual: ", (1 + lam - 1/(1-1/5))/2)
print()

# ═══════════════════════════════════════════════════════════════
# ROUTE N: THE SELF-CONSISTENT COUPLING FROM SATURATION
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE N: SELF-CONSISTENT COUPLING FROM NONLINEAR SATURATION")
print("=" * 70)

print("""
★★★ THE DERIVATION ATTEMPT ★★★

SETUP: 3 identical oscillators coupled symmetrically:
  xᵢ' = Γ·tanh³(xᵢ) - λ·xᵢ + ε·Σⱼ≠ᵢ xⱼ

At symmetric fixed point (all xᵢ = x_b):
  Γ·tanh³(x_b) = (1 + λ - 2ε)·x_b                    ... (1)

For the UNCOUPLED system (ε=0):
  Γ·tanh³(x_f) = (1 + λ)·x_f → x_f = Γ/(1+λ)        ... (2)

The coupling ε modifies the effective restoring force.

NOW: The SELF-CONSISTENCY condition.

Each oscillator is driven by the coupling signal s = 2ε·x_b.
The oscillator's NONLINEAR response to this signal is:
  Δx = ∂x*/∂(effective_λ) · Δ(effective_λ)

But this is linear response, which we showed doesn't work.

INSTEAD: Consider the RATIO of nonlinear outputs.

The output of oscillator i is Γ·tanh³(xᵢ).
In the coupled system, the total output summed over 3 quarks is:
  F_total = 3·Γ·tanh³(x_b)

The INPUT (from fixed-point condition):
  F_total = 3·(1 + λ - 2ε)·x_b = 3·x_b + 3(λ-2ε)·x_b

The "bare" output without coupling would be:
  F_free = 3·Γ·tanh³(x_f) = 3·(1+λ)·x_f

The COUPLING RATIO:
  κ = 1 - F_total/F_free = 1 - [(1+λ-2ε)·x_b]/[(1+λ)·x_f]

For large Γ (tanh → 1): x_b ≈ Γ/(1+λ-2ε), x_f ≈ Γ/(1+λ)
  κ = 1 - [(1+λ-2ε) · Γ/(1+λ-2ε)] / [(1+λ) · Γ/(1+λ)]
    = 1 - 1 = 0

This is the SAME result as before — in the saturated regime,
the coupling drops out. κ_eff = 0.

THE FUNDAMENTAL PROBLEM:
tanh³ saturates at 1 for large x, so ALL large-Γ oscillators
look identical. The coupling can't distinguish Γ = 25 from Γ = 100.

CONCLUSION: The coupling κ = 1/√Γ CANNOT come from the
large-amplitude (saturated) regime of the recursion.

It must come from FINITE-SIZE CORRECTIONS to the saturation.
""")

# ═══════════════════════════════════════════════════════════════
# ROUTE O: FINITE-SIZE CORRECTIONS — THE SECH² TAIL
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE O: FINITE-SIZE CORRECTIONS — THE SECH² TAIL")
print("=" * 70)

print("""
The saturation of tanh³ is not EXACT — there's an exponential tail:
  tanh³(x) = 1 - 6·e^{-2x} + ...   for large x

The DEVIATION from saturation: δ(x) = 1 - tanh³(x) ≈ 6·e^{-2x}

At the FREE fixed point x_f ≈ Γ:
  δ_f = 6·e^{-2Γ} (NEGLIGIBLE for Γ = 25)

But at the GATE SCALE x ~ √Γ:
  δ_gate = 6·e^{-2√Γ}

For Γ = 25: δ_gate = 6·e^{-10} ≈ 2.7×10⁻⁴ (small but finite)
For Γ = 4:  δ_gate = 6·e^{-4}  ≈ 0.11 (significant!)

The PHYSICAL PICTURE:
  Each oscillator is at amplitude x_b ≈ Γ (deeply saturated).
  The coupling signal from other quarks is at amplitude √Γ (the gate).
  The SENSITIVITY to the coupling signal is determined by δ_gate.
""")

# Compute the deviation and its relation to κ
print("Finite-size correction at the geometric mean scale:")
print(f"{'Γ':>6} {'√Γ':>8} {'δ=6e^(-2√Γ)':>14} {'κ=1/√Γ':>10} {'δ·Γ':>10} {'δ·Γ^(3/2)':>12}")
print("-" * 65)
for G in [4, 9, 16, 25, 36, 49, 100]:
    p = np.sqrt(G)
    delta = 6*np.exp(-2*p)
    kappa = 1/p
    print(f"{G:6d} {p:8.2f} {delta:14.6e} {kappa:10.4f} {delta*G:10.4e} {delta*G**1.5:12.4e}")

print()
print("The exponential corrections don't scale as 1/√Γ.")
print("The sech² tail is too fast — it dies exponentially, not algebraically.")
print()

# ═══════════════════════════════════════════════════════════════
# ROUTE P: THE INTEGRAL APPROACH — AVERAGE COUPLING
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE P: INTEGRAL COUPLING — AVERAGED OVER THE ATTRACTOR")
print("=" * 70)

print("""
KEY INSIGHT: Instead of evaluating the coupling at the FIXED POINT,
evaluate it as an AVERAGE over the approach to the fixed point.

When the oscillator is converging to x*, it passes through ALL
amplitudes from 0 to x*. The coupling "felt" at each amplitude
is different because tanh³ is nonlinear.

The EFFECTIVE coupling is the AVERAGE nonlinear gain along the path:
  κ_eff = 1 - (1/x*) ∫₀^x* [tanh³(t)/t] dt

This is the average of tanh³(t)/t, which measures how much the
nonlinear gate "reduces" the drive at each scale.

If tanh³(t)/t is weighted by time spent at each scale, this gives
the effective coupling.
""")

# Compute the integral average of tanh³(t)/t
print("Average of tanh³(t)/t from 0 to x*:")
print(f"{'Γ':>6} {'x*':>10} {'<tanh³/t>':>12} {'1-<tanh³/t>':>14} {'1/√Γ':>10} {'Ratio':>10}")
print("-" * 65)

for G in [4, 9, 16, 25, 36, 49, 100]:
    xs = exact_fp(G)
    if xs and xs > 0.1:
        def integrand(t):
            if abs(t) < 1e-10:
                return 1.0  # tanh(t)/t → 1, so tanh³(t)/t → t²
            return np.tanh(t)**3 / t

        avg, _ = quad(integrand, 0.001, xs)
        avg /= xs

        kappa_int = 1 - avg
        kappa_target = 1/np.sqrt(G)

        ratio = kappa_int / kappa_target if kappa_target > 0 else 0
        print(f"{G:6d} {xs:10.4f} {avg:12.6f} {kappa_int:14.6f} {kappa_target:10.6f} {ratio:10.4f}")

print()

# Try different integrals
print()
print("Try: (1/x*²) ∫₀^x* t·[1-tanh³(t)] dt  (weighted deviation):")
print(f"{'Γ':>6} {'x*':>10} {'Integral':>12} {'1/√Γ':>10} {'Ratio':>10}")
print("-" * 55)

for G in [4, 9, 16, 25, 36, 49, 100]:
    xs = exact_fp(G)
    if xs and xs > 0.1:
        def integrand2(t):
            return t * (1 - np.tanh(t)**3)

        integral, _ = quad(integrand2, 0, xs)
        normalized = integral / xs**2
        kappa_target = 1/np.sqrt(G)

        ratio = normalized / kappa_target if kappa_target > 0 else 0
        print(f"{G:6d} {xs:10.4f} {normalized:12.6f} {kappa_target:10.6f} {ratio:10.4f}")

print()
print("Try: √(2/x* ∫₀^x* [1-tanh³(t)] dt)  (RMS deviation):")
print(f"{'Γ':>6} {'x*':>10} {'√integral':>12} {'1/√Γ':>10} {'Ratio':>10}")
print("-" * 55)

for G in [4, 9, 16, 25, 36, 49, 100]:
    xs = exact_fp(G)
    if xs and xs > 0.1:
        def integrand3(t):
            return 1 - np.tanh(t)**3

        integral, _ = quad(integrand3, 0, xs)
        sqrt_norm = np.sqrt(2*integral/xs)
        kappa_target = 1/np.sqrt(G)

        ratio = sqrt_norm / kappa_target if kappa_target > 0 else 0
        print(f"{G:6d} {xs:10.4f} {sqrt_norm:12.6f} {kappa_target:10.6f} {ratio:10.4f}")

# ═══════════════════════════════════════════════════════════════
# ROUTE Q: THE AREA RATIO
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE Q: THE AREA RATIO — GATED vs UNGATED")
print("=" * 70)

print("""
SIMPLE GEOMETRIC ARGUMENT:

The "ungated" linear drive from 0 to x* has area A_linear = x*²/2
The "gated" cubic tanh³ drive from 0 to x* has area:
  A_gated = Γ·∫₀^x* tanh³(t) dt

The RATIO A_gated/A_linear tells us how much the gate reduces
the total drive. The COUPLING REDUCTION κ should relate to this ratio.

Using ∫tanh³(t)dt = ln(cosh(t)) - tanh²(t)/2:
  A_gated = Γ[ln(cosh(x*)) - tanh²(x*)/2]

For large x*: ln(cosh(x*)) ≈ x* - ln(2), tanh²(x*) ≈ 1
  A_gated ≈ Γ(x* - ln(2) - 1/2) ≈ Γ·x* = Γ²/(1+λ) ≈ Γ²

  A_linear = x*²/2 ≈ Γ²/2

So: A_gated/A_linear ≈ 2 for large Γ.
The gate barely matters because x* is so deep in saturation.

WHAT IF we compare to the UNCOUPLED SYSTEM instead?
  ΔA = A_free - A_coupled = ?
""")

# Direct computation of area ratios
print("Area analysis:")
print(f"{'Γ':>6} {'A_gated':>12} {'A_linear':>12} {'Ratio':>10} {'1-1/ratio':>12}")
print("-" * 55)

for G in [4, 9, 16, 25, 36, 49, 100]:
    xs = exact_fp(G)
    if xs:
        A_gated = G * (np.log(np.cosh(xs)) - np.tanh(xs)**2/2)
        A_linear = xs**2 / 2
        ratio = A_gated / A_linear
        print(f"{G:6d} {A_gated:12.4f} {A_linear:12.4f} {ratio:10.6f} {1-1/ratio:12.6f}")

# ═══════════════════════════════════════════════════════════════
# ROUTE R: THE DEFINITIVE ATTEMPT — COUPLING FROM 3-BODY
# NONLINEAR FEEDBACK
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ROUTE R: NONLINEAR FEEDBACK SELF-CONSISTENCY")
print("=" * 70)

print("""
★★★ THE MOST PROMISING APPROACH ★★★

In the 3-body system, oscillator i receives feedback from j,k:
  feedback_i = ε·(x_j + x_k)

This feedback is PROCESSED through the nonlinear gate tanh³:
  x_i → f(x_i + feedback_i)

The key insight: the EFFECTIVE feedback is not ε·(x_j+x_k)
but rather the change in output DUE TO the feedback:
  Δ_output = Γ·tanh³(x + s) - Γ·tanh³(x) where s = ε(x_j+x_k)

At the fixed point (x_b, s = 2ε·x_b):
  Δ = Γ·[tanh³(x_b + 2ε·x_b) - tanh³(x_b)]
  ≈ Γ·f'(x_b)·2ε·x_b = [3Γ·tanh²·sech²]·2ε·x_b

Since f'(x_b) ≈ -λ (saturated), this is tiny.

BUT: The feedback doesn't just shift x. It changes the DYNAMICS.
In the FULL nonlinear system, the 3-body map is:

  xᵢ → Γ·tanh³(xᵢ) + ε·Σⱼ≠ᵢ [Γ·tanh³(xⱼ) - (1+λ)xⱼ + xⱼ]

No wait. Let me reconsider the PHYSICAL model.

Actually, in the coupled oscillator picture:
  The quarks exchange GLUONS (in QCD) or COHERENCE QUANTA (in CUFT).
  Each exchange transfers energy of order √(E_q) where E_q is the quark energy.

  ENERGY TRANSFER per exchange: ~√E_q ∝ √(Γ²) = Γ
  NUMBER of exchanges per cycle: ~1/Γ (probability decreases with energy)
  NET COUPLING: ~Γ·(1/Γ) = 1 ... constant? No.

  Actually:
    E_q ~ Γ² (quark energy)
    Exchange amplitude: ~Γ (linear in quark amplitude x* ≈ Γ)
    Exchange probability (from gate): ~tanh³(amplitude)/amplitude
    For the GATE contribution: ~1/Γ (high amplitude → saturated → unit/Γ)

    Net: Γ · (1/Γ) = 1 ... hmm.

    More carefully:
    Exchange amplitude: ~x* ≈ Γ
    Gate factor: tanh³(x*)/x* = 1/x* ≈ 1/Γ for large x*
    Per-quark coupling: Γ · (1/Γ) = 1 = const

    But the RELATIVE coupling (fraction of total):
    κ = coupling / total_amplitude = 1/x* ≈ 1/Γ ???

    No, that gives κ = 1/Γ, not 1/√Γ.

TRYING ANOTHER WAY:
  The coupling between quarks involves PAIR interactions.
  For a pair at amplitudes (x*, x*), the interaction goes through
  the PRODUCT of their gates: tanh³(x₁)·tanh³(x₂) ≈ 1.

  But the EXCHANGE involves one quark emitting and another absorbing.
  The emission amplitude: √(drive) = √Γ
  The absorption amplitude: √(response) = √(1/Γ) = 1/√Γ

  Net exchange: √Γ · (1/√Γ) = 1? Or √Γ per exchange?

  If each of the 3 pairs contributes √Γ to the coupling:
    Total coupling: 3·√Γ
    Relative: 3·√Γ / (3·Γ) = 1/√Γ = κ !!!

  THIS GIVES κ = 1/√Γ !!!
""")

print("★★★ CANDIDATE DERIVATION ★★★")
print()
print("In the 3-body gated cubic system:")
print("  Each oscillator has amplitude x* ≈ Γ")
print("  The EMISSION amplitude for coupling: √(Γ)")
print("    (geometric mean of drive Γ and gate width 1)")
print("  The ABSORPTION amplitude: also √(Γ)")
print("    (by reciprocity)")
print()
print("  Each PAIR exchanges coupling of magnitude: √Γ · (1/Γ)")
print("    = √Γ/Γ = 1/√Γ")
print("  (emission √Γ divided by the target amplitude Γ)")
print()
print("  With 3 pairs, but each quark participates in 2 pairs:")
print("  Total coupling fraction per quark: 2 × (1/√Γ) / 2 = 1/√Γ")
print()
print("  Therefore: κ = 1/√Γ")
print()

# Check: does the emission = √Γ idea have a basis in the recursion?
print("VERIFICATION: Is √Γ a natural scale in f(x) = Γ·tanh³(x) - λx?")
print()
print("1. The inflection point of Γ·tanh³(x) occurs at x_infl = atanh(1/√3) = 0.659")
print("   Not √Γ. But this is scale-independent.")
print()
print("2. The point where Γ·tanh³(x) = x (without damping, not the FP):")
for G in [25]:
    def g(x): return G*np.tanh(x)**3 - x
    try:
        xc = brentq(g, 0.01, G)
        print(f"   Γ={G}: Γ·tanh³(x)=x at x={xc:.4f}, √Γ={np.sqrt(G):.4f}, ratio={xc/np.sqrt(G):.4f}")
    except:
        print(f"   Γ={G}: No crossing found")

print()
print("3. The point where d/dx[Γ·tanh³(x)] = 1 (unity gain):")
for G in [4, 9, 16, 25, 36, 49, 100]:
    def dg(x): return 3*G*np.tanh(x)**2*(1-np.tanh(x)**2) - 1
    try:
        xug = brentq(dg, 0.01, 5)
        print(f"   Γ={G:3d}: unity gain at x={xug:.4f}, √Γ={np.sqrt(G):.4f}, ratio={xug/np.sqrt(G):.4f}")
    except:
        print(f"   Γ={G:3d}: No unity gain point found")

print()
print("4. The scale where f(x) makes its transition from cubic to saturated:")
print("   This is where tanh(x) ≈ 0.76, i.e., x ≈ 1. Independent of Γ.")
print()

# ═══════════════════════════════════════════════════════════════
# ROUTE S: THE UNITY GAIN SCALE
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("ROUTE S: THE UNITY GAIN SCALE")
print("=" * 70)

print("""
★ INTERESTING from Route R, test 3:

The UNITY GAIN POINT x_ug where |f'(x)| = 1 (without the -λ part):
  3Γ·tanh²(x)·sech²(x) = 1

This defines the scale at which the oscillator can transmit
information without amplifying or attenuating.

For the COUPLING: if the coupling signal passes through the gate
at the unity gain scale, it's transmitted exactly. Above this scale,
it's attenuated (saturated). Below, it's amplified (cubic growth).

The unity gain scale x_ug depends on Γ.
""")

print("Unity gain analysis: 3Γ·tanh²(x)·sech²(x) = 1")
print(f"{'Γ':>6} {'x_ug':>10} {'√(ln(3Γ)/2)':>14} {'ratio':>8}")
print("-" * 45)

ug_data = []
for G in [4, 9, 16, 25, 36, 49, 64, 81, 100, 144, 196, 400, 625]:
    def gain_eq(x):
        t = np.tanh(x)
        return 3*G*t**2*(1-t**2) - 1
    try:
        xug = brentq(gain_eq, 0.01, 10)
        # Approximate: for tanh(x) ≈ 1-2e^{-2x}, sech² ≈ 4e^{-2x}
        # 3Γ·1·4e^{-2x} = 1 → e^{-2x} = 1/(12Γ) → x = ln(12Γ)/2
        x_approx = np.log(12*G)/2
        ug_data.append((G, xug))
        print(f"{G:6d} {xug:10.4f} {x_approx:14.4f} {xug/x_approx:8.4f}")
    except:
        pass

# Check scaling of x_ug with Γ
print()
print("How does x_ug scale with Γ?")
print(f"{'Γ':>6} {'x_ug':>10} {'ln(Γ)/2':>10} {'√(ln(Γ))':>10} {'x_ug/√Γ':>10}")
print("-" * 50)
for G, xug in ug_data:
    print(f"{G:6d} {xug:10.4f} {np.log(G)/2:10.4f} {np.sqrt(np.log(G)):10.4f} {xug/np.sqrt(G):10.4f}")

print()
print("x_ug ≈ ln(12Γ)/2 — logarithmic, NOT √Γ.")
print("The unity gain scale doesn't give 1/√Γ either.")

# ═══════════════════════════════════════════════════════════════
# SYNTHESIS
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SYNTHESIS: STATE OF THE COUPLING DERIVATION")
print("=" * 70)

print("""
ROUTES ATTEMPTED AND RESULTS:

Route D (Information): f'(x*) → -λ for all Γ. Channel is saturated.
                       Linear information theory doesn't distinguish Γ.

Route E (RG/Scale):    No natural scale transformation for tanh³.

Route F (Topological): Winding number counts fixed points but doesn't
                       constrain coupling.

Route G (Variational): M = A(1-κ)² + Bκ² CAN give κ ∝ 1/√Γ from δM/δκ = 0
                       BUT requires B = A·√Γ which must be justified.
                       ★ PARTIAL SUCCESS — needs physical meaning of B term.

Route H (Geometric):   κ = √Γ/Γ = 1/√Γ from geometric mean of drive (Γ)
                       and gate (1) scales.
                       ★ PROMISING — clean argument, right answer.
                       But needs formalization.

Route I (Resonance):   Incomplete — nonlinear resonance too complex.

Route J (Curvature):   f''(x*) is exponentially small. Dead end.

Route K (Scale of Γ):  √Γ as geometric mean. Same as H.

Route L (Numerical):   tanh³(√Γ) ≈ 1 (saturated). Doesn't directly work.

Route M (Partition):   ε ≈ -1/(2(√Γ-1)), confirmed numerically.
                       ★ Exact relation derived, but ε is a consequence of κ,
                       not an independent derivation of it.

Route N (Saturation):  Linear analysis gives κ_eff = 0. Dead end for large Γ.

Route O (Finite-size): Exponential corrections, wrong scaling.

Route P (Integral):    Various integral averages tested.
                       Some approach 1/√Γ but with wrong constants.
                       ★ SUGGESTIVE — the path integral approach has potential.

Route Q (Area ratio):  A_gated/A_linear → 2 for large Γ. Not directly useful.

Route R (3-body NL):   Emission amplitude √Γ, absorption 1/√Γ.
                       ★ PROMISING — gives κ = 1/√Γ from exchange picture.
                       But the "emission = √Γ" step needs justification.

Route S (Unity gain):  x_ug ≈ ln(Γ)/2 — logarithmic, not √Γ.

═══════════════════════════════════════════════════════════════

THE TWO MOST PROMISING ROUTES:

1. ROUTE G (Variational): If the baryon mass includes a "confinement
   energy" term proportional to √Γ·κ², then minimizing total energy
   gives κ = 1/√Γ. This is the STANDARD physics approach (variational
   principle). The open question: what IS the confinement energy?

2. ROUTE H/R (Geometric Mean): The coupling scale is the geometric
   mean of the drive scale Γ and the gate scale 1, giving √Γ.
   The coupling fraction is √Γ/Γ = 1/√Γ.
   This is ELEGANT but needs formalization.

NEITHER IS A COMPLETE DERIVATION YET.

Both reduce the question to: "Why does the coupling involve √Γ?"
The answer seems to be: because √Γ is the geometric mean of the
two fundamental scales (drive Γ and nonlinear gate 1), and the
coupling between oscillators occurs at this intermediate scale.

This is PHYSICALLY REASONABLE (coupling at the geometric mean of
interacting scales is common in physics — cf. Debye screening length,
geometric mean of electron/proton masses in atomic physics, etc.)
but not yet a rigorous derivation from the recursion equation.

THE GAP NARROWED BUT NOT CLOSED.
""")

print("=" * 70)
print("END — COUPLING DERIVATION ATTEMPTS")
print("YASA PRESENTS — 2026-02-12")
print("=" * 70)
