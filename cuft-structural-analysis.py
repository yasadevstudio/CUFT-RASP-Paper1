#!/usr/bin/env python3
"""
CUFT-RASP: STRUCTURAL ANALYSIS OF ALL FOUR CONSTANTS
======================================================
YASA PRESENTS — 2026-02-24

All four constants from (n,p) = (3,5) share RASP building blocks.
Is there a COMMON STRUCTURE that generates all four?
If so, the search results become derived results.

APPROACH: Decompose each formula and look for:
  1. Common algebraic patterns across all four
  2. A single generating function that produces all four at different inputs
  3. Physical motivation for each term
"""

from fractions import Fraction
import numpy as np

n, p = 3, 5
G = p**2                      # 25
L = Fraction(1, p**3 - 1)     # 1/124
X = n * p * (p - 1)           # 60
Phi3 = p**2 + p + 1           # 31

# The four constants (exact fractions)
M = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + L / n
inv_alpha = Fraction(p**3) + n*(p-1) + Fraction(n**2, 2*p**3)
M_n = M + Fraction(p, 2) + Fraction(n**2, p*X) + Fraction(n*p, (p**3-1)**2)
M_mu = Fraction(p*(p**3-1), n) + Fraction(1, p*(p**3-1)) + Fraction(1, 2*p)

print("=" * 90)
print("STRUCTURAL ANALYSIS: COMMON PATTERNS IN ALL FOUR CONSTANTS")
print("=" * 90)

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 1: Term structure decomposition
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("ANALYSIS 1: TERM STRUCTURE — Large + Medium + Small pattern")
print("─" * 90)

print(f"""
Each constant has a dominant term, a middle correction, and small corrections:

  m_p/m_e = X²/2        + (n/p)X       + n²/X        + λ/n
          = {float(Fraction(X**2,2)):10.4f}  + {float(Fraction(n,p)*X):10.4f}  + {float(Fraction(n**2,X)):10.6f}  + {float(L/n):12.8f}
  Scale:    ~1800           ~36             ~0.15           ~0.003

  1/α     = p³           + n(p-1)       + n²/(2p³)
          = {p**3:10.4f}  + {n*(p-1):10.4f}  + {float(Fraction(n**2,2*p**3)):10.6f}
  Scale:    ~125            ~12             ~0.036

  m_μ/m_e = 4pΦ₃/n      + 1/(2p)       + 1/(4pΦ₃)
          = {float(Fraction(4*p*Phi3,n)):10.4f}  + {float(Fraction(1,2*p)):10.4f}  + {float(Fraction(1,4*p*Phi3)):10.6f}
  Scale:    ~207            ~0.1            ~0.002

  m_n/m_e = M            + p/2          + n²/(pX)     + np/(p³-1)²
          = {float(M):10.4f}  + {float(Fraction(p,2)):10.4f}  + {float(Fraction(n**2,p*X)):10.6f}  + {float(Fraction(n*p,(p**3-1)**2)):12.8f}
  Scale:    ~1836           ~2.5            ~0.03           ~0.001
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 2: The "scale parameter" pattern
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 2: GENERATING FUNCTION HYPOTHESIS")
print("─" * 90)

# The proton mass formula F(s) = s²/2 + (n/p)s + n²/s + λ/n
# evaluated at s = X = np(p-1) = 60
# What if ALL four come from evaluating RELATED functions at RELATED scales?

# Let's check: does the α formula fit a similar template?
# 1/α = p³ + n(p-1) + n²/(2p³)
# Compare to F(s) = s²/2 + (n/p)s + n²/s + λ/n
# At s = p: F(p) = p²/2 + n + n²/p + λ/n = 12.5 + 3 + 1.8 + 0.003 = 17.3
# Not 137. So α is NOT F(p).

# But what about G(s) = s³ + n(s-1) + n²/(2s³)?
# G(p) = 125 + 12 + 0.036 = 137.036 ✓
# G(X) = 216000 + 177 + ... nope.

# What about the muon?
# M_mu = 4pΦ₃/n + 1/(4pΦ₃) + 1/(2p)
# = 620/3 + 1/620 + 1/10

# Can we write this as some function evaluated at a scale?
# 4pΦ₃ = p(p³-1) = 620
# So: M_mu = (4pΦ₃)/n + 1/(4pΦ₃) + 1/(2p)
# Let S = 4pΦ₃ = p(p³-1) = 620
# Then: M_mu = S/n + 1/S + 1/(2p)

# Interesting: S/n + 1/S is like a "reciprocal pair"
# Compare to proton: X²/2 + n²/X is also a pair (X² and 1/X)

print(f"""
PROTON: evaluated at scale X = np(p-1) = {X}
  F(X) = X²/2 + (n/p)X + n²/X + λ/n

ALPHA: evaluated at scale p = {p}
  G(p) = p³ + n(p-1) + n²/(2p³)

MUON: evaluated at scale S = p(p³-1) = {p*(p**3-1)}
  Let S = p(p³-1) = 4pΦ₃
  M_mu = S/n + 1/S + 1/(2p)

KEY OBSERVATION: The muon's dominant term S/n involves:
  S = p(p³-1) = p·(p-1)·Φ₃·(p²+p+1)... wait, p³-1 = (p-1)(p²+p+1) = (p-1)Φ₃
  So S = p(p-1)Φ₃ = 4·5·31 = 620

  But X = np(p-1) = 3·5·4 = 60
  So S = X·Φ₃/n = 60·31/3 = 620  ✓
  Or S = X·Φ₃/n

  Therefore: M_mu = X·Φ₃/n² + n/(X·Φ₃) + 1/(2p)

  The dominant terms are:
  Proton:  X²/2        (scale X, power 2)
  Alpha:   p³          (scale p, power 3)
  Muon:    X·Φ₃/n²     (scale X·Φ₃/n, power 1... or X²·Φ₃/(X·n²))
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 3: Denominator structure
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 3: DENOMINATOR FACTORIZATION")
print("─" * 90)

def full_factorize(frac):
    """Show full RASP factorization of a Fraction."""
    num = frac.numerator
    den = frac.denominator

    def rasp_factor(n):
        temp = abs(n)
        parts = {}
        for base, name in [(2,"2"), (3,"n"), (5,"p"), (31,"Φ₃")]:
            count = 0
            while temp % base == 0:
                count += 1
                temp //= base
            if count > 0:
                parts[name] = count
        if temp > 1:
            parts[str(temp)] = 1
        return parts

    num_parts = rasp_factor(num)
    den_parts = rasp_factor(den)

    num_str = "·".join(f"{k}^{v}" if v > 1 else k for k, v in num_parts.items())
    den_str = "·".join(f"{k}^{v}" if v > 1 else k for k, v in den_parts.items())

    return f"{num} / {den} = ({num_str}) / ({den_str})"

print(f"\n  m_p/m_e = {full_factorize(M)}")
print(f"  1/α     = {full_factorize(inv_alpha)}")
print(f"  m_n/m_e = {full_factorize(M_n)}")
print(f"  m_μ/m_e = {full_factorize(M_mu)}")

print(f"""
  ALL denominators factor into {{2, n=3, p=5, Φ₃=31}} exclusively.

  m_p/m_e denom: {M.denominator} = n·p·Φ₃
  1/α denom:     {inv_alpha.denominator} = 2·p³
  m_n/m_e denom: {M_n.denominator} = 2⁴·n·p²·Φ₃²
  m_μ/m_e denom: {M_mu.denominator} = 2²·n·p·Φ₃
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 4: The A + 1/A pattern (reciprocal duality)
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 4: RECIPROCAL PAIR STRUCTURE")
print("─" * 90)

# The muon has a beautiful A + 1/A structure:
# M_mu = S/n + 1/S + 1/(2p)  where S = p(p³-1) = 620
# = (S² + n)/(nS) + 1/(2p)

# Does the proton have this too?
# M = X²/2 + (n/p)X + n²/X + λ/n
# The dominant pair: X²/2 and n²/X
# X²/2 + n²/X = (X³ + 2n²)/(2X)

# The middle pair: (n/p)X and λ/n = 1/(n(p³-1))
# (n/p)X = n²(p-1) = 36
# λ/n = 1/(n(p³-1)) = 1/372

# So proton = (X³+2n²)/(2X) + n²(p-1) + 1/(n(p³-1))
# Hmm, the "reciprocal" isn't as clean

# Let me look at it differently.
# M = X²/2 + (n/p)·X + n²/X + λ/n
# Let's factor out X from first and third terms:
# = X(X/2 + n²/X²) + (n/p)X + λ/n    ... no, that's not right

# Actually: X²/2 + n²/X = (X³ + 2n²)/(2X)
# For X=60: (216000 + 18)/120 = 216018/120 = 1800.15

print(f"""
PROTON mass dominant terms: X²/2 + n²/X
  = {float(Fraction(X**2,2) + Fraction(n**2,X)):.6f}
  = (X³ + 2n²)/(2X)
  These are a "virial pair": kinetic (X²) and potential (n²/X) sectors

PROTON mass correction terms: (n/p)X + λ/n
  = {float(Fraction(n,p)*X + L/n):.8f}
  = n²(p-1) + 1/(n(p³-1))

  NOTE: n²(p-1) = {n**2*(p-1)}
        n(p³-1) = {n*(p**3-1)}
        Product: n²(p-1) · 1/(n(p³-1)) = n(p-1)/(p³-1) = n/(p²+p+1) = n/Φ₃ = {n}/{Phi3}

  The correction terms are NOT a reciprocal pair, but their product is n/Φ₃.

MUON dominant terms: S/n + 1/S where S = p(p³-1)
  = {float(Fraction(p*(p**3-1),n) + Fraction(1,p*(p**3-1))):.10f}
  These ARE a reciprocal pair: S/n and n/S would be perfect,
  but it's S/n and 1/S (not n/S).

  Product: (S/n)·(1/S) = 1/n
  So S/n · (1/S) = 1/n = 1/3

ALPHA: p³ + n(p-1) + n²/(2p³)
  = p³ + n²/(2p³) + n(p-1)
  Pair: p³ and n²/(2p³)
  Product: p³ · n²/(2p³) = n²/2 = 9/2

  So p³ and n²/(2p³) form a pair with product n²/2.
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 5: Mass formula as generating function
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 5: CAN ONE FUNCTION GENERATE ALL FOUR?")
print("─" * 90)

# The mass formula is: F(s) = s²/2 + (n/p)s + n²/s + λ/n
# At s=X=60: proton mass ✓

# What if we generalize to: F_k(s) = A·s^k + B·s^(k-1) + C·s^(-k+1) + D·s^(-k)
# with some k-dependent coefficients?

# Proton: k=2, F_2(X) = X²/2 + (n/p)X + n²/X + λ/n
# Alpha:  k=3, G(p) = p³ + n(p-1) + n²/(2p³)
#   But this isn't F_3(p) = p³/2 + (n/p)p² + n²/p² + λ/n = 62.5 + 15 + 1.8 + 0.003 = 79.3

# The alpha formula has DIFFERENT coefficients from the mass formula.
# So it's not the same function at a different scale.

# Let me tabulate what coefficients each formula uses:
print(f"""
  COEFFICIENT COMPARISON:

  F(s) = a·s^k  +  b·s^(k-1)  +  c·s^(-k+1)  +  d·s^(-k)  [+ corrections]

  Proton at (s=X, k=2):
    a = 1/2,  b = n/p,  c = n²,  d = λ/n
    → X²/2 + (n/p)X + n²/X + λ/n = {float(M):.6f}

  Alpha at (s=p, k=3):
    a = 1,  b = n,  c = 0,  d = n²/2
    → p³ + n(p-1) + n²/(2p³)  [middle term is n(p-1), not n·p²]

  Muon at (s=S, k=1) where S = p(p³-1):
    a = 1/n,  b = 0,  c = 0,  d = 1
    → S/n + 1/S + 1/(2p)  [last term doesn't fit the pattern]
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 6: Polynomial in X with different powers
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 6: ALL FORMULAS IN TERMS OF X = np(p-1)")
print("─" * 90)

# Express everything in terms of X = 60

print(f"\n  X = np(p-1) = {X}")
print(f"  p = {p}, n = {n}, Φ₃ = {Phi3}")
print(f"  p³-1 = (p-1)Φ₃ = {(p-1)*Phi3} = {p**3-1}")

# Proton in X:
# M = X²/2 + (n/p)X + n²/X + 1/(n(p³-1))
print(f"\n  PROTON: M = X²/2 + (n/p)X + n²/X + 1/(n(p³-1))")
print(f"    = X²/2 + (n/p)X + n²/X + 1/((p-1)nΦ₃)")

# Alpha in X:
# 1/α = p³ + n(p-1) + n²/(2p³)
# Now p = X/(n(p-1)) ... well, p isn't cleanly expressed as X
# But p³ = X³/(n³(p-1)³) = X³/(n³·64) ... not clean
# p³-1 = (p-1)Φ₃, and X = np(p-1), so p = X/(n(p-1))

# Let me try expressing in terms of the UV threshold
# In the paper, the UV threshold is p³. Everything above p³ is the mass hierarchy.
# Below p³ is confinement.

print(f"\n  UV THRESHOLD: p³ = {p**3}")
print(f"  X/p = n(p-1) = {n*(p-1)} = virial scale")
print(f"  X/(np) = (p-1) = {p-1} = coupling order")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 7: The (p³-1) connection
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("ANALYSIS 7: THE (p³-1) = (p-1)·Φ₃ CONNECTION")
print("─" * 90)

# λ = 1/(p³-1) appears in the proton mass
# p(p³-1) = 4pΦ₃ appears as the muon scale
# (p³-1)² appears in the neutron correction
# p³ appears in alpha

print(f"""
  λ = 1/(p³-1) = 1/{p**3-1}

  PROTON uses λ/n = 1/(n(p³-1)):
    Last term = {float(L/n):.10f}

  ALPHA uses p³ and p³ in denominator:
    First term = p³ = {p**3}
    Last term denominator = 2p³ = {2*p**3}

  MUON uses p(p³-1) = {p*(p**3-1)} as its scale:
    S = p(p³-1) = {p*(p**3-1)}
    = p(p-1)Φ₃ = {p}·{p-1}·{Phi3}
    Note: S = (p-1)·(pΦ₃) = X/n · pΦ₃ ...
    Or: S = X·Φ₃/n since X = np(p-1), so X/n = p(p-1), and p(p-1)·Φ₃ = S ✓

  NEUTRON uses (p³-1)² in denominator:
    np/(p³-1)² = {n*p}/{(p**3-1)**2}
    = np/((p-1)²Φ₃²)

  PATTERN: p³-1 = (p-1)Φ₃ is the MASTER SCALE.
    Proton: 1st power in denominator (λ = 1/(p³-1))
    Alpha:  p³ = (p³-1) + 1, so alpha "lives" at the UV cutoff
    Muon:   1st power × p as the evaluation scale
    Neutron: 2nd power in the correction term
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 8: Virial theorem connection
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 8: VIRIAL THEOREM STRUCTURE")
print("─" * 90)

# In the α heuristic derivation, we found that n(p-1) = 2(p+1) for (n,p)=(3,5)
# This is a virial-like relation: kinetic energy = 2 × potential for 1/r potential

# Does this extend to the muon?
# Muon: 4pΦ₃/n + 1/(4pΦ₃) + 1/(2p)
# If the first two terms are a "virial pair":
# Kinetic: S/n = 4pΦ₃/n
# Potential: 1/S = 1/(4pΦ₃)
# Ratio: (S/n)/(1/S) = S²/n = (4pΦ₃)²/n = (620)²/3 = 128133

print(f"""
  VIRIAL RATIOS (dominant/correction term ratios):

  Proton: (X²/2) / (n²/X) = X³/(2n²) = {X**3/(2*n**2):.1f}
  Alpha:  p³ / (n²/(2p³)) = 2p⁶/n² = {2*p**6/n**2:.1f}
  Muon:   (S/n) / (1/S) = S²/n = {(p*(p**3-1))**2/n:.1f}

  These are NOT constant — the virial ratio depends on the scale.
  But the STRUCTURE is the same: large term × small term = fixed RASP quantity.

  Proton pair product: (X²/2)·(n²/X) = n²X/2 = {n**2*X//2}
  Alpha pair product:  p³·(n²/(2p³)) = n²/2 = {Fraction(n**2,2)}
  Muon pair product:   (S/n)·(1/S) = 1/n = {Fraction(1,n)}

  Products: {n**2*X//2}, {Fraction(n**2,2)}, {Fraction(1,n)}
    = n²X/2, n²/2, 1/n
    = (n²/2)·X, (n²/2)·1, (n²/2)·(2/(n³X))

  Hmm... the ratio between proton and alpha pair products:
    (n²X/2) / (n²/2) = X = {X} ✓

  Between alpha and muon pair products:
    (n²/2) / (1/n) = n³/2 = {n**3/2}
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 9: Template function approach
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 9: UNIFIED TEMPLATE — f(s,k) = s^k/a + b·s^(k-2) + c/s^k + d")
print("─" * 90)

# What if there's a template:
# T(s, k) = (1/a)·s^k + b·s^(k-2) + c·s^(-k) + small_corrections
# where a, b, c depend on n, p?

# Proton: T(X, 2) = X²/2 + (n/p)X + n²/X + λ/n
#   k=2: s²/2 + (n/p)s^0 · s + n²·s^(-1) + λ/n
#   = (1/2)s² + (n/p)s¹ + n²s⁻¹ + (1/n)·s⁰/(p³-1)
#   Powers: 2, 1, -1, 0  (spaced by 1, then 2, then 1)

# Alpha: T(p, 3) = p³ + n(p-1) + n²/(2p³)
#   = 1·p³ + n·p¹ - n·p⁰ + (n²/2)·p⁻³
#   Powers: 3, 1, 0, -3  (spaced by 2, then 1, then 3)

# The power structures don't match with a simple template.
# Let me try a different decomposition.

# What if the formula is f(s) = s²/2 + correction(s)?
# And the correction depends on the PHYSICS being described?

print(f"""
  TEMPLATE ATTEMPT — Polynomial in s:

  Proton at s=X:  X^2/2 + (n/p)X^1 + n²X^(-1) + (1/n)X^0/(p³-1)
  Powers used:     +2     +1          -1           0

  Alpha at s=p:   p^3 + n·p^1 - n·p^0 + (n²/2)p^(-3)
  Powers used:     +3    +1      0         -3

  OBSERVATION: Both have a "positive power" and its negative mirror:
    Proton: +2 and -1 (not mirror)
    Alpha:  +3 and -3 (EXACT mirror!)

  Alpha's structure p^3 + n²/(2p³) is a SYMMETRIC pair around p^0.
  Proton's structure X²/2 + n²/X is NOT symmetric (would need n²/X²).

  BUT: In the proton formula, the scale is X = np(p-1) = 60.
  What if we rescale? Let u = X/√(2n²) = X/(n√2) = 60/(3√2) = 20/√2
  Then X²/2 = n²u² and n²/X = n²/(n√2·u) = n/(√2·u)... not clean.

  The power asymmetry in the proton formula (2 vs -1) comes from the cubic
  recursion: f(x) = Γtanh³(x) - λx. The third power of tanh generates
  the quadratic dominant behavior at the fixed point.
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 10: The MUON as inverse proton
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 10: MUON-PROTON RELATIONSHIP")
print("─" * 90)

# m_e/m_μ ≈ λn/p = n/(p(p³-1)) = 3/620
# But m_e/m_p ≈ 1/M = 465/853811
# Ratio: (m_e/m_μ)/(m_e/m_p) = m_p/m_μ = M·n/(p(p³-1)) ... no,
# = M / (p(p³-1)/n) = M·n/(p(p³-1))

mp_mu = float(M) / float(M_mu)
mu_mp = float(M_mu) / float(M)

print(f"""
  m_p/m_μ = {mp_mu:.10f} = {Fraction(M.numerator * M_mu.denominator, M.denominator * M_mu.numerator)}
  m_μ/m_p = {mu_mp:.10f}

  Experimental m_μ/m_p = 206.7682827/1836.152673 = {206.7682827/1836.152673426:.10f}

  M/M_mu = {float(M)/float(M_mu):.10f}

  Note: M_mu ≈ p(p³-1)/n = X·Φ₃/n²
        M ≈ X²/2
        Ratio: M/M_mu ≈ (X²/2)/(X·Φ₃/n²) = n²X/(2Φ₃) = {n**2*X/(2*Phi3):.6f}

  n²X/(2Φ₃) = {n**2*X}/(2·{Phi3}) = {n**2*X}/{2*Phi3} = {Fraction(n**2*X, 2*Phi3)}
  = {float(Fraction(n**2*X, 2*Phi3)):.10f}

  Actual ratio: {float(M)/float(M_mu):.10f}
  Approx ratio: {float(Fraction(n**2*X, 2*Phi3)):.10f}
  Error: {abs(float(M)/float(M_mu) - float(Fraction(n**2*X, 2*Phi3)))/(float(M)/float(M_mu))*1e6:.1f} ppm
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 11: Are the corrections PERTURBATIVE?
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 11: PERTURBATIVE HIERARCHY")
print("─" * 90)

# For each formula, compute correction/dominant ratios
print(f"""
  Each formula has terms of decreasing magnitude.
  Is the ratio between successive terms a FIXED expansion parameter?

  PROTON:
    Term 1: X²/2 = {float(Fraction(X**2,2)):.4f}
    Term 2: (n/p)X = {float(Fraction(n,p)*X):.4f}     ratio to T1: {float(Fraction(n,p)*X)/float(Fraction(X**2,2)):.6f} = 2n/(pX) = {2*n/(p*X):.6f}
    Term 3: n²/X = {float(Fraction(n**2,X)):.6f}     ratio to T2: {float(Fraction(n**2,X))/float(Fraction(n,p)*X):.6f} = n/(p·(n/p)·X) = np/(p²X)... = n²/(X·(n/p)X) = n/(X²/p) = np/X² = {n*p/X**2:.6f}
    Term 4: λ/n = {float(L/n):.8f}   ratio to T3: {float(L/n)/float(Fraction(n**2,X)):.6f}

    Expansion parameter ε = 2n/(pX) = {2*n/(p*X):.6f}
    Expected T2/T1 ≈ ε: {2*n/(p*X):.6f} ✓
    Expected T3/T1 ≈ ε²: {(2*n/(p*X))**2:.6f} vs actual {float(Fraction(n**2,X))/float(Fraction(X**2,2)):.6f}
    Hmm, {float(Fraction(n**2,X))/float(Fraction(X**2,2)):.6f} vs {(2*n/(p*X))**2:.8f} — off by ~{float(Fraction(n**2,X))/float(Fraction(X**2,2))/(2*n/(p*X))**2:.1f}x

  ALPHA:
    Term 1: p³ = {p**3:.4f}
    Term 2: n(p-1) = {n*(p-1):.4f}    ratio to T1: {n*(p-1)/p**3:.6f} = n(p-1)/p³
    Term 3: n²/(2p³) = {float(Fraction(n**2,2*p**3)):.6f}    ratio to T2: {float(Fraction(n**2,2*p**3))/(n*(p-1)):.6f}

    Expansion parameter ε_α = n(p-1)/p³ = {n*(p-1)/p**3:.6f}
    T3/T2: {float(Fraction(n**2,2*p**3))/(n*(p-1)):.6f}
    T3/T1: {float(Fraction(n**2,2*p**3))/p**3:.8f} = n²/(2p⁶) = {n**2/(2*p**6):.8f}
    ε_α²: {(n*(p-1)/p**3)**2:.8f}

  MUON:
    Term 1: S/n = {float(Fraction(p*(p**3-1),n)):.4f}
    Term 2: 1/(2p) = {float(Fraction(1,2*p)):.6f}    ratio to T1: {float(Fraction(1,2*p))/float(Fraction(p*(p**3-1),n)):.8f}
    Term 3: 1/S = {float(Fraction(1,p*(p**3-1))):.8f}    ratio to T2: {float(Fraction(1,p*(p**3-1)))/float(Fraction(1,2*p)):.6f}

    Expansion parameter ε_μ = n/(2p·S) = n/(2p²(p³-1)) = {n/(2*p**2*(p**3-1)):.8f}
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 12: The λ-expansion interpretation for muon
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 12: λ-EXPANSION FOR MUON")
print("─" * 90)

# The proton mass comes from a λ-expansion of the fixed-point equation
# Can the muon also be expressed as a λ-expansion?

# M_mu = p(p³-1)/n + 1/(p(p³-1)) + 1/(2p)
# = p(p³-1)/n + 1/(2p) + 1/(p(p³-1))

# Note: p(p³-1) = p⁴ - p = 625 - 5 = 620
# p(p³-1)/n = (p⁴-p)/n

# In terms of λ = 1/(p³-1):
# p(p³-1)/n = p/(nλ)
# 1/(p(p³-1)) = λ/p
# 1/(2p) = κ/2

# So: M_mu = p/(nλ) + κ/2 + λ/p

# This is EXTREMELY interesting!
# M_mu = p/(nλ) + κ/2 + λ/p

# Compare to: M ≈ ... which involves λ only in the last term as λ/n

# The muon has a BEAUTIFUL structure in terms of λ:
# Term 1: p/(nλ) — proportional to 1/λ (leading order)
# Term 2: 1/(2p) — independent of λ (constant)
# Term 3: λ/p — proportional to λ (first correction)

# This is a Laurent expansion in λ around λ=0!
# M_mu(λ) = p/(nλ) + 1/(2p) + λ/p + O(λ²)

print(f"""
  MUON IN TERMS OF λ = 1/(p³-1):

  m_μ/m_e = p/(nλ) + 1/(2p) + λ/p

  Term 1: p/(nλ) = p(p³-1)/n = {p}·{p**3-1}/{n} = {p*(p**3-1)/n:.4f}   [order 1/λ]
  Term 2: 1/(2p) = {Fraction(1,2*p)}  = {float(Fraction(1,2*p)):.4f}    [order λ⁰]
  Term 3: λ/p    = {L/p} = {float(L/p):.8f}    [order λ¹]

  This is a LAURENT SERIES in λ:
    m_μ/m_e = c₋₁/λ + c₀ + c₁·λ
  where c₋₁ = p/n, c₀ = 1/(2p), c₁ = 1/p

  Total = {float(Fraction(p*(p**3-1),n) + Fraction(1,2*p) + L/p):.15f}
  Exper = 206.768282700000
  Error = {abs(float(Fraction(p*(p**3-1),n) + Fraction(1,2*p) + L/p) - 206.7682827)/206.7682827*1e9:.1f} ppb

  COMPARE TO PROTON in terms of λ:
  m_p/m_e = X²/2 + (n/p)X + n²/X + λ/n

  Only the LAST term depends on λ (and it's order λ¹).
  The first three terms are all λ-independent.

  So: Proton mass is WEAKLY λ-dependent (λ appears only at 4th order)
      Muon mass is STRONGLY λ-dependent (λ appears at LEADING order)

  PHYSICAL INTERPRETATION:
  λ = 1/(p³-1) controls the coupling strength of the cubic recursion.
  The proton, being at the confinement scale X, is mostly set by X.
  The muon, being a lepton, "sees" the coupling directly — its mass
  is essentially p/(nλ) = p(p³-1)/n, which is the coupling scale itself.

  The muon is the COUPLING CONSTANT EXPRESSED AS A MASS.
""")

# Verify the exact muon formula
mu_lambda = Fraction(p, n) * (p**3 - 1) + Fraction(1, 2*p) + L * Fraction(1, p)
print(f"\n  EXACT: p/(nλ) + 1/(2p) + λ/p")
print(f"       = p(p³-1)/n + 1/(2p) + 1/(p(p³-1))")
print(f"       = {mu_lambda}")
print(f"       = {float(mu_lambda):.15f}")
print(f"  Match with M_mu = {float(M_mu):.15f}")
print(f"  Same? {mu_lambda == M_mu}")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 13: Can neutron also be expressed in λ?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("ANALYSIS 13: NEUTRON IN TERMS OF λ")
print("─" * 90)

# M_n = M + p/2 + n²/(pX) + np/(p³-1)²
# = M + p/2 + n²/(pX) + npλ²

# The correction to go from proton to neutron is:
# Δ = p/2 + n²/(pX) + npλ²
# = p/2 + n/(p²(p-1)) + npλ²

# In terms of λ:
# Δ = p/2 + n/(p²(p-1)) + np·λ²

# Note: n/(p²(p-1)) = n/(p²(p-1))
# And X = np(p-1), so n/(p²(p-1)) = 1/(p·X/n) = n/(pX) ... wait, n²/(pX) = n·n/(pX)
# n/(p²(p-1)) = n/(p²·4) = 3/100 for our values

# The neutron correction is: p/2 + n²/(pX) + npλ²
# Term 1: p/2 — λ-independent
# Term 2: n²/(pX) — λ-independent
# Term 3: npλ² — order λ²

delta_check = Fraction(p, 2) + Fraction(n**2, p*X) + n*p*L**2
M_n_check = M + delta_check

print(f"""
  NEUTRON-PROTON MASS DIFFERENCE in terms of λ:

  Δ = p/2 + n²/(pX) + np·λ²

  Term 1: p/2      = {Fraction(p,2)}     [λ-independent, isospin]
  Term 2: n²/(pX)  = {Fraction(n**2,p*X)}     [λ-independent, confinement]
  Term 3: np·λ²    = {n*p*L**2} = {float(n*p*L**2):.12f}  [order λ²]

  np/(p³-1)² = np·λ² ✓  (since λ = 1/(p³-1))

  Total Δ = {delta_check} = {float(delta_check):.12f}

  m_n/m_e = M + p/2 + n²/(pX) + npλ²
          = {M_n_check}
          = {float(M_n_check):.15f}

  Match with previous: {M_n_check == M_n}

  SIGNIFICANCE:
  The neutron correction is a PERTURBATION SERIES in λ:
    Δ = Δ₀ + Δ₁·λ + Δ₂·λ² + ...
    = (p/2 + n²/(pX)) + 0·λ + np·λ²

  The λ¹ term is ZERO (or absorbed into the proton mass).
  The leading λ-dependent correction is npλ² — second order.

  This is consistent with isospin being a λ-perturbation:
  the neutron is the proton with a 2nd-order coupling correction.
""")

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS 14: ALL FOUR AS λ-SERIES
# ═══════════════════════════════════════════════════════════════════

print("─" * 90)
print("ANALYSIS 14: ALL FOUR CONSTANTS AS λ-SERIES")
print("─" * 90)

print(f"""
  λ = 1/(p³-1) = {float(L):.10f}

  PROTON:  m_p/m_e = [X²/2 + (n/p)X + n²/X] + (1/n)·λ
           = {float(M):.10f}
           λ-dependence: WEAK (last term, order λ¹, contributes {float(L/n)/float(M)*1e6:.1f} ppm)

  ALPHA:   1/α = [p³ + n(p-1)] + [n²/(2p³)]
           Note: n²/(2p³) does NOT depend on λ
           λ-dependence: NONE (α is λ-independent!)
           This makes physical sense: α is the ELECTROMAGNETIC coupling,
           which shouldn't depend on the CONFINEMENT coupling λ.

  NEUTRON: m_n/m_e = m_p/m_e + [p/2 + n²/(pX)] + np·λ²
           = {float(M_n):.10f}
           λ-dependence: WEAK (correction term, order λ², contributes {float(n*p*L**2)/float(M_n)*1e6:.2f} ppm)

  MUON:    m_μ/m_e = (p/n)·λ⁻¹ + 1/(2p) + (1/p)·λ
           = {float(M_mu):.10f}
           λ-dependence: STRONG (leading term is order λ⁻¹!)
           The muon mass IS the coupling constant expressed as a mass.

  HIERARCHY OF λ-DEPENDENCE:

  | Constant | λ order | Physical meaning |
  |----------|---------|-----------------|
  | 1/α      | λ⁰     | EM coupling — independent of confinement |
  | m_p/m_e  | λ¹     | Baryon — weakly coupled to λ |
  | m_n/m_e  | λ²     | Isospin partner — 2nd order correction |
  | m_μ/m_e  | λ⁻¹    | Lepton — mass IS the coupling scale |
""")
