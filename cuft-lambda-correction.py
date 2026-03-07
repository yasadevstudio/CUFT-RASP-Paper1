#!/usr/bin/env python3
"""
CUFT-RASP DIRECTION 1: SECOND-ORDER LAMBDA CORRECTION
=======================================================
YASA PRESENTS — 2026-02-24

The entire 8 ppb residual comes from λ = 1/(p³-1) = 1/124 vs
λ_exact = 0.008020. Can we derive a correction δλ?

The quantization error: Γ_classical = 24.84 → Γ = 25.
This ΔΓ = 0.16 propagates into λ and M.
"""

import numpy as np
from scipy.optimize import brentq
from fractions import Fraction

# ═══════════════════════════════════════════════════════════════════
# EXACT VALUES
# ═══════════════════════════════════════════════════════════════════

n, p = 3, 5
G = p**2  # 25 (quantized)
L = 1/(p**3 - 1)  # 1/124 (derived from quantized Γ)
X = n * p * (p - 1)  # 60

# Mass formula
M_derived = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + Fraction(1, n * (p**3 - 1))
print(f"M_derived = {M_derived} = {float(M_derived):.12f}")

# Experimental
mu_exp = 1836.152673426
print(f"mu_exp    = {mu_exp:.12f}")
print(f"Residual  = {float(M_derived) - mu_exp:.12f}")
print(f"Fractional = {(float(M_derived) - mu_exp) / mu_exp:.4e}")

# Back-calculate λ_exact
# M = X²/2 + (n/p)X + n²/X + λ/n
# λ/n = M - X²/2 - (n/p)X - n²/X
# λ = n * (M - X²/2 - (n/p)X - n²/X)

L_exact = n * (mu_exp - X**2/2 - n/p * X - n**2/X)
print(f"\nλ_derived = {float(L):.12f}")
print(f"λ_exact   = {L_exact:.12f}")
print(f"δλ = λ_exact - λ_derived = {L_exact - float(L):.12f}")
print(f"δλ/λ = {(L_exact - float(L))/float(L):.8f} = {(L_exact - float(L))/float(L)*100:.4f}%")

delta_L = L_exact - float(L)

# ═══════════════════════════════════════════════════════════════════
# GAIN-COHERENCE EXACT VALUE
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("GAIN-COHERENCE ANALYSIS")
print("="*70)

# Solve gain-coherence: |f'(x_u)|^n = Γ with λ=0
def gc_residual(G_try):
    def g0(x): return G_try * np.tanh(x)**3 - x
    try:
        xu = brentq(g0, 0.001, 5.0)
    except:
        return -1.0
    t = np.tanh(xu)
    s = 1 - t**2
    fp = 3 * G_try * t**2 * s
    return fp**3 - G_try

G_class = brentq(gc_residual, 20, 30)
sqrt_G_class = np.sqrt(G_class)

print(f"Γ_classical = {G_class:.12f}")
print(f"√Γ_classical = {sqrt_G_class:.12f}")
print(f"p = round(√Γ) = {round(sqrt_G_class)}")
print(f"ΔΓ = Γ - Γ_class = {G - G_class:.12f}")
print(f"Δ(√Γ) = p - √Γ_class = {p - sqrt_G_class:.12f}")
print(f"ΔΓ/Γ = {(G - G_class)/G:.8f} = {(G - G_class)/G*100:.4f}%")

# ═══════════════════════════════════════════════════════════════════
# PROPAGATE ΔΓ TO δλ
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("PROPAGATING QUANTIZATION ERROR")
print("="*70)

# If we use Γ_classical instead of Γ = p², what λ would we get?
# λ = 1/(Γ^(3/2) - 1) when Γ = p² gives λ = 1/(p³-1)
# But Γ_classical ≠ p², so:
# p_class = √Γ_class (NOT integer)
# λ_class = 1/(Γ_class^(3/2) - 1)

p_class = sqrt_G_class
L_class = 1 / (G_class**(3/2) - 1)
print(f"p_classical = {p_class:.12f}")
print(f"λ from Γ_class^(3/2): {L_class:.12f}")
print(f"λ_exact:              {L_exact:.12f}")
print(f"λ_derived (1/124):    {float(L):.12f}")
print(f"Diff (Γ_class^1.5 vs exact): {abs(L_class - L_exact)/L_exact*100:.6f}%")

# Alternative: what if λ = 1/(p_class³ - 1) using the continuous p?
L_from_pclass = 1 / (p_class**3 - 1)
print(f"\nλ from p_class³: {L_from_pclass:.12f}")
print(f"Diff vs exact:   {abs(L_from_pclass - L_exact)/L_exact*100:.6f}%")

# What if we use Γ_class directly?
# κ = λ·x_s, x_s = Γ/(1+λ), κ = 1/√Γ
# So: 1/√Γ = λ·Γ/(1+λ) → λ = 1/(Γ^(3/2) - 1)
# This is the EXACT relation for continuous Γ.

print(f"\n--- The exact continuous relation ---")
print(f"λ = 1/(Γ^(3/2) - 1)")
print(f"  At Γ=25:       λ = 1/(125-1) = 1/124 = {1/124:.12f}")
print(f"  At Γ=24.8377:  λ = 1/({G_class**1.5:.4f}-1) = {L_class:.12f}")
print(f"  λ_exact:       λ = {L_exact:.12f}")

# ═══════════════════════════════════════════════════════════════════
# CORRECTION FORMULA SEARCH
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("SEARCHING FOR CORRECTION FORMULA")
print("="*70)

epsilon = G - G_class  # = 0.1623... (quantization error in Γ)
delta_p = p - sqrt_G_class  # = 0.01626... (error in √Γ)

print(f"\nε = ΔΓ = {epsilon:.12f}")
print(f"δp = Δ√Γ = {delta_p:.12f}")

# First-order Taylor: λ(Γ) = 1/(Γ^{3/2}-1)
# dλ/dΓ = -(3/2)·Γ^{1/2} / (Γ^{3/2}-1)²
dLdG = -1.5 * G**0.5 / (G**1.5 - 1)**2
delta_L_taylor1 = dLdG * (-epsilon)  # correction from using Γ_class instead of 25
print(f"\nFirst-order Taylor correction:")
print(f"  dλ/dΓ at Γ=25 = {dLdG:.12f}")
print(f"  δλ_Taylor1 = dλ/dΓ · (-ε) = {delta_L_taylor1:.12f}")
print(f"  λ_corrected = λ + δλ = {float(L) + delta_L_taylor1:.12f}")
print(f"  λ_exact =               {L_exact:.12f}")
print(f"  Remaining error: {abs(float(L) + delta_L_taylor1 - L_exact)/L_exact*100:.8f}%")

# Second-order Taylor
d2LdG2 = (-1.5 * 0.5 * G**(-0.5) * (G**1.5 - 1)**2 - (-1.5 * G**0.5) * 2 * (G**1.5 - 1) * 1.5 * G**0.5) / (G**1.5 - 1)**4
delta_L_taylor2 = dLdG * (-epsilon) + 0.5 * d2LdG2 * epsilon**2
print(f"\nSecond-order Taylor correction:")
print(f"  d²λ/dΓ² at Γ=25 = {d2LdG2:.12f}")
print(f"  δλ_Taylor2 = {delta_L_taylor2:.12f}")
print(f"  λ_corrected = {float(L) + delta_L_taylor2:.12f}")
print(f"  Remaining error: {abs(float(L) + delta_L_taylor2 - L_exact)/L_exact*100:.8f}%")

# Exact correction: use Γ_classical directly
delta_L_exact = L_class - float(L)
L_corrected = float(L) + delta_L_exact
M_corrected = X**2/2 + n/p * X + n**2/X + L_corrected/n
print(f"\nExact correction (use Γ_classical in λ formula):")
print(f"  δλ_exact = {delta_L_exact:.12f}")
print(f"  λ_corrected = {L_corrected:.12f}")
print(f"  M_corrected = {M_corrected:.12f}")
print(f"  mu_exp      = {mu_exp:.12f}")
print(f"  New residual = {M_corrected - mu_exp:.12f}")
print(f"  New fractional = {abs(M_corrected - mu_exp)/mu_exp:.4e}")
print(f"  Improvement: {abs(float(M_derived) - mu_exp) / abs(M_corrected - mu_exp):.1f}x better")

# ═══════════════════════════════════════════════════════════════════
# WHAT IF WE CORRECT EVERYTHING WITH Γ_CLASSICAL?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("FULL CORRECTION: USE Γ_CLASSICAL THROUGHOUT")
print("="*70)

# If Γ = Γ_classical (not quantized):
G_c = G_class
p_c = np.sqrt(G_c)
L_c = 1 / (G_c**(3/2) - 1)
X_c = n * p_c * (p_c - 1)
c1_c = n / p_c
c2_c = (p_c + 1) / (n * (p_c - 1))

M_full_corrected = c2_c * X_c**2 + c1_c * X_c + n**2 / X_c + L_c / n

print(f"Using Γ_classical = {G_c:.8f} throughout:")
print(f"  p = √Γ = {p_c:.8f} (continuous)")
print(f"  λ = 1/(Γ^1.5 - 1) = {L_c:.12f}")
print(f"  X = np(p-1) = {X_c:.8f}")
print(f"  c₁ = n/p = {c1_c:.12f}")
print(f"  c₂ = (p+1)/(n(p-1)) = {c2_c:.12f} (vs 1/2 = 0.5)")
print(f"  M_full = {M_full_corrected:.12f}")
print(f"  mu_exp = {mu_exp:.12f}")
print(f"  Residual = {M_full_corrected - mu_exp:.6e}")
print(f"  Fractional = {abs(M_full_corrected - mu_exp)/mu_exp:.4e}")

# ═══════════════════════════════════════════════════════════════════
# THE KEY INSIGHT: MIXED CORRECTION
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("MIXED CORRECTION: QUANTIZED STRUCTURE + CLASSICAL λ")
print("="*70)

# Keep the quantized structural parameters (p=5, X=60, c₁=3/5, c₂=1/2)
# but correct ONLY λ using Γ_classical

# This is physically motivated: the integer structure IS real
# (Diophantine, virial, etc.), but λ carries the quantization residual

L_mixed = 1 / (G_class**(3/2) - 1)
M_mixed = X**2/2 + Fraction(n, p) * X + Fraction(n**2, X) + L_mixed / n
M_mixed = float(M_mixed)

print(f"Keep: p=5, X=60, c₁=3/5, c₂=1/2")
print(f"Correct: λ = 1/(Γ_class^1.5 - 1) = {L_mixed:.12f}")
print(f"  M_mixed = {M_mixed:.12f}")
print(f"  mu_exp  = {mu_exp:.12f}")
print(f"  Residual = {M_mixed - mu_exp:.6e}")
print(f"  Fractional = {abs(M_mixed - mu_exp)/mu_exp:.4e}")

# Also try: λ = 1/(Γ_class · p - 1) and other forms
print("\n--- Testing various λ correction forms ---")
forms = {
    'λ = 1/(p³-1)  [current]': 1/(p**3 - 1),
    'λ = 1/(Γ_c^1.5 - 1)': 1/(G_class**1.5 - 1),
    'λ = 1/(Γ_c·p - 1)': 1/(G_class * p - 1),
    'λ = 1/(p²·√Γ_c - 1)': 1/(p**2 * np.sqrt(G_class) - 1),
    'λ = 1/(√Γ_c³ - 1)': 1/(np.sqrt(G_class)**3 - 1),
    'λ = 1/((√Γ_c)^3 - 1)': 1/(np.sqrt(G_class)**3 - 1),
    'λ = κ_c/(Γ_c - κ_c)': (1/np.sqrt(G_class)) / (G_class - 1/np.sqrt(G_class)),
}

print(f"{'Form':>35s}  {'λ':>14s}  {'M':>16s}  {'ppb':>10s}")
print("-" * 80)
for name, L_try in forms.items():
    M_try = X**2/2 + n/p * X + n**2/X + L_try/n
    ppb = abs(M_try - mu_exp) / mu_exp * 1e9
    print(f"{name:>35s}  {L_try:.12f}  {M_try:.12f}  {ppb:.2f}")

print(f"{'λ_exact (back-calc)':>35s}  {L_exact:.12f}  {mu_exp:.12f}  {'0.00':>10s}")

# ═══════════════════════════════════════════════════════════════════
# CAN WE EXPRESS λ_exact AS A SIMPLE FUNCTION?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("IS λ_EXACT A SIMPLE FUNCTION OF (n, p, Γ_classical)?")
print("="*70)

# λ_exact = 0.008020...
# What simple expressions give this?

print(f"\nλ_exact = {L_exact:.15f}")
print(f"1/λ_exact = {1/L_exact:.10f}")

# Check integer-related forms
tests = {
    '1/124': 1/124,
    '1/124.7': 1/124.7,
    '1/125': 1/125,
    '1/(p³)': 1/p**3,
    '1/(p³-1)': 1/(p**3-1),
    'n/(n·p³-n)': n/(n*p**3-n),
    '(p-√Γ_c)/p²': (p - np.sqrt(G_class))/p**2,
    '1/(Γ_c·p-1)': 1/(G_class*p-1),
    'π/(n·p³)': np.pi/(n*p**3),
}

for name, val in tests.items():
    err_pct = (val - L_exact)/L_exact * 100
    print(f"  {name:>20s} = {val:.12f}  err: {err_pct:+.6f}%")

# What is 1/λ_exact exactly?
inv_L_exact = 1/L_exact
print(f"\n1/λ_exact = {inv_L_exact:.10f}")
print(f"  Nearest integers: {int(inv_L_exact)} and {int(inv_L_exact)+1}")
print(f"  Fractional part: {inv_L_exact - int(inv_L_exact):.10f}")
print(f"  p³ = {p**3}, p³-1 = {p**3-1}")
print(f"  inv_L_exact - 124 = {inv_L_exact - 124:.10f}")
print(f"  This excess is: {(inv_L_exact - 124):.10f}")
print(f"  = {(inv_L_exact - 124)} ≈ {(inv_L_exact - 124)/124:.8f} * 124")

# Is the excess related to ΔΓ?
excess = inv_L_exact - 124
print(f"\n  Excess {excess:.10f} vs:")
print(f"    ΔΓ = {epsilon:.10f}")
print(f"    ΔΓ/Γ = {epsilon/G:.10f}")
print(f"    3/2·ΔΓ/Γ·(p³-1) = {1.5*epsilon/G*(p**3-1):.10f}")  # from Taylor
print(f"    3/2·δp/p·(p³-1) = {1.5*delta_p/p*(p**3-1):.10f}")

# The Taylor relation: 1/λ ≈ (p³-1)(1 + 3δp/p)
inv_L_taylor = (p**3-1) * (1 + 3*delta_p/p)
print(f"\n  Taylor: 1/λ ≈ (p³-1)(1 + 3δp/p) = {inv_L_taylor:.10f}")
print(f"  Actual:                              {inv_L_exact:.10f}")
print(f"  Error: {abs(inv_L_taylor - inv_L_exact)/inv_L_exact*100:.8f}%")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
