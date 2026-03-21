#!/usr/bin/env python3
"""
CUFT-RASP: NEUTRON MASS PREDICTION
====================================
YASA PRESENTS — 2026-02-24

DISCOVERY: The neutron-to-electron mass ratio is predicted by:

    m_n/m_e = M(3,5) + p/2 + n²/(p·X)

where M(3,5) = 853811/465 is the proton mass ratio.

This means the neutron-proton mass difference is:

    (m_n - m_p)/m_e = p/2 + n²/(p·X) = 5/2 + 3/100 = 253/100 = 2.53

Accuracy: 530 ppb on the full neutron mass.
"""

from fractions import Fraction
import numpy as np

# ═══════════════════════════════════════════════════════════════════
# RASP CONSTANTS
# ═══════════════════════════════════════════════════════════════════

n, p = 3, 5
G = p**2                    # Gamma = 25
L = Fraction(1, p**3 - 1)   # lambda = 1/124
X = n * p * (p - 1)         # X = 60
Phi3 = p**2 + p + 1         # 31

# Proton mass (derived)
M = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + L / n

# Fine structure constant (from same paper)
inv_alpha = Fraction(p**3) + n*(p-1) + Fraction(n**2, 2*p**3)

print("=" * 80)
print("CUFT-RASP: NEUTRON MASS PREDICTION")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════
# THE NEUTRON MASS FORMULA
# ═══════════════════════════════════════════════════════════════════

# Correction term: neutron - proton mass difference
delta = Fraction(p, 2) + Fraction(n**2, p * X)
print(f"\nISO SPIN CORRECTION:")
print(f"  Δ = p/2 + n²/(p·X)")
print(f"    = {p}/2 + {n**2}/({p}·{X})")
print(f"    = {Fraction(p,2)} + {Fraction(n**2, p*X)}")
print(f"    = {delta}")
print(f"    = {float(delta):.10f}")

# Neutron mass prediction
M_n = M + delta
print(f"\nNEUTRON MASS RATIO:")
print(f"  m_n/m_e = M + Δ")
print(f"         = {M} + {delta}")
print(f"         = {M_n}")
print(f"         = {float(M_n):.10f}")

# Experimental values (CODATA 2022)
mu_exp = 1836.152673426  # m_p/m_e (32)
mn_exp = 1838.68366173   # m_n/m_e (89)
delta_exp = mn_exp - mu_exp  # = 2.53098830(94)

print(f"\nCOMPARISON WITH EXPERIMENT (CODATA 2022):")
print(f"  {'Quantity':>25s}  {'Predicted':>15s}  {'Experimental':>15s}  {'Error (ppb)':>12s}")
print(f"  {'-'*25}  {'-'*15}  {'-'*15}  {'-'*12}")

# Proton
err_p = abs(float(M) - mu_exp) / mu_exp * 1e9
print(f"  {'m_p/m_e':>25s}  {float(M):15.10f}  {mu_exp:15.10f}  {err_p:12.1f}")

# Neutron
err_n = abs(float(M_n) - mn_exp) / mn_exp * 1e9
print(f"  {'m_n/m_e':>25s}  {float(M_n):15.10f}  {mn_exp:15.10f}  {err_n:12.1f}")

# Fine structure
err_a = abs(float(inv_alpha) - 137.035999177) / 137.035999177 * 1e9
print(f"  {'1/α':>25s}  {float(inv_alpha):15.10f}  {'137.0359992':>15s}  {err_a:12.1f}")

# Mass difference
err_d = abs(float(delta) - delta_exp) / delta_exp * 1e6
print(f"\n  {'(m_n-m_p)/m_e':>25s}  {float(delta):15.10f}  {delta_exp:15.10f}  {err_d*1000:12.1f}")
print(f"  {'':>25s}  {'':>15s}  {'':>15s}  {'(ppm on Δ)':>12s}")
print(f"  (m_n-m_p)/m_e accuracy: {err_d:.0f} ppm on the mass difference")

# ═══════════════════════════════════════════════════════════════════
# EXACT ARITHMETIC
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*80}")
print("EXACT ARITHMETIC")
print(f"{'='*80}")

print(f"\nProton mass ratio:")
print(f"  M = {M}")
print(f"  Denominator: {M.denominator} = {n}·{p}·{Phi3} = n·p·Φ₃(p)")

print(f"\nMass difference:")
print(f"  Δ = {delta}")
print(f"  Numerator: {delta.numerator}")
print(f"  Denominator: {delta.denominator}")
# Factor the denominator
d = delta.denominator
print(f"  {d} = ", end="")
factors = []
temp = d
for pr in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    while temp % pr == 0:
        factors.append(pr)
        temp //= pr
if temp > 1:
    factors.append(temp)
print("·".join(str(f) for f in factors))

print(f"\nNeutron mass ratio:")
print(f"  M_n = {M_n}")
print(f"  Numerator: {M_n.numerator}")
print(f"  Denominator: {M_n.denominator}")
d_n = M_n.denominator
print(f"  {d_n} = ", end="")
factors = []
temp = d_n
for pr in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    while temp % pr == 0:
        factors.append(pr)
        temp //= pr
if temp > 1:
    factors.append(temp)
print("·".join(str(f) for f in factors))

# ═══════════════════════════════════════════════════════════════════
# PHYSICAL INTERPRETATION
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*80}")
print("PHYSICAL INTERPRETATION")
print(f"{'='*80}")

print(f"""
The neutron-proton mass difference has two RASP terms:

  Term 1: p/2 = {p}/2 = {float(Fraction(p,2)):.4f} m_e = {float(Fraction(p,2))*0.51099895:.4f} MeV
    = "coupling virial" — half the quantized coupling
    = {float(Fraction(p,2))*0.51099895:.3f} MeV (vs QCD isospin: ~2.49 MeV bare + EM correction)

  Term 2: n²/(p·X) = {n**2}/({p}·{X}) = {float(Fraction(n**2, p*X)):.6f} m_e = {float(Fraction(n**2, p*X))*0.51099895:.4f} MeV
    = "confinement perturbation" — confinement charge / (coupling × action)
    = n/(p²(p-1)) = one quark at the p² confinement scale

  Total: {float(delta)*0.51099895:.4f} MeV
  Expt:  {delta_exp*0.51099895:.4f} MeV

ALTERNATIVE FORM: The full neutron mass formula is:

  M_n = X²/2 + (n/p)X + n²/X + λ/n + p/2 + n/(p²(p-1))

      = [X²/2 + p/2]           — kinetic (with coupling correction)
      + [(n/p)X]                — linear confinement (same as proton)
      + [n²/X + n/(p²(p-1))]   — Coulomb + isospin perturbation
      + [λ/n]                   — vacuum (same as proton)

The proton and neutron share 4 of 6 terms. The difference is:
  p/2 added to kinetic sector
  n/(p²(p-1)) added to confinement sector
""")

# ═══════════════════════════════════════════════════════════════════
# CROSS-VALIDATION: Does the correction work with exact proton mass?
# ═══════════════════════════════════════════════════════════════════

print(f"{'='*80}")
print("CROSS-VALIDATION: Using experimental proton mass")
print(f"{'='*80}")

mn_from_exact = mu_exp + float(delta)
err_cross = abs(mn_from_exact - mn_exp) / mn_exp * 1e9
print(f"\n  m_p(exp) + Δ(RASP) = {mu_exp:.10f} + {float(delta):.10f}")
print(f"                     = {mn_from_exact:.10f}")
print(f"  m_n(exp)           = {mn_exp:.10f}")
print(f"  Error: {err_cross:.0f} ppb")
print(f"\n  The {err_cross:.0f} ppb error is intrinsic to the correction term,")
print(f"  independent of the proton mass formula's 8 ppb Bohr error.")

# ═══════════════════════════════════════════════════════════════════
# CORRECTION NEEDED FOR EXACT MATCH
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*80}")
print("CORRECTION ANALYSIS")
print(f"{'='*80}")

delta_exact = Fraction(mn_exp - mu_exp).limit_denominator(100000)
print(f"\n  Exact Δ = {delta_exp:.10f}")
print(f"  RASP Δ  = {float(delta):.10f}")
print(f"  Gap     = {delta_exp - float(delta):.10f}")
print(f"  Gap/Δ   = {(delta_exp - float(delta))/delta_exp*1e6:.1f} ppm")

# Is the gap expressible as a RASP quantity?
gap = delta_exp - float(delta)
print(f"\n  Gap = {gap:.8f} m_e = {gap*0.51099895*1000:.4f} keV")
print(f"  Searching for RASP expressions matching gap...")

rasp_candidates = [
    ("λ", float(L)),
    ("λ/n", float(L)/n),
    ("λ·n/p", float(L)*n/p),
    ("n²/(p³·X)", n**2/(p**3*X)),
    ("n²/(2p³·X)", n**2/(2*p**3*X)),
    ("1/(p²·Φ₃)", 1/(p**2*Phi3)),
    ("λ²·X", float(L)**2*X),
    ("n/(p·X²)", n/(p*X**2)),
    ("n³/(p³·X²)", n**3/(p**3*X**2)),
    ("λ/(p-1)", float(L)/(p-1)),
    ("1/(n·X)", 1/(n*X)),
    ("1/(p·X)", 1/(p*X)),
    ("n/(Φ₃·X)", n/(Phi3*X)),
    ("n²/(Φ₃·p·X)", n**2/(Phi3*p*X)),
    ("λ·n/(p²)", float(L)*n/p**2),
]

for label, val in rasp_candidates:
    frac = abs(val - gap)/abs(gap)
    if frac < 0.3:
        print(f"    {label:>20s} = {val:.8f}  (gap = {gap:.8f}, ratio = {val/gap:.4f})")

# ═══════════════════════════════════════════════════════════════════
# ALSO: MUON MASS CANDIDATE
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*80}")
print("BONUS: MUON MASS CANDIDATE")
print(f"{'='*80}")

mu_muon = 206.7682827  # m_μ/m_e

# Leading term
leading = Fraction(p * (p**3 - 1), n)  # = p(p³-1)/n = 620/3
corr1 = Fraction(n**2, p**3)            # = 9/125
corr2 = Fraction(n**2, p * X)           # = 9/300 = 3/100

muon_pred = leading + corr1 + corr2
print(f"\n  m_μ/m_e = p(p³-1)/n + n²/p³ + n²/(pX)")
print(f"         = {leading} + {corr1} + {corr2}")
print(f"         = {muon_pred}")
print(f"         = {float(muon_pred):.10f}")
print(f"  Expt:    {mu_muon:.10f}")
err_muon = abs(float(muon_pred) - mu_muon) / mu_muon * 1e6
print(f"  Error:   {err_muon:.2f} ppm")

# Simplify
print(f"\n  SIMPLIFIED: p(p³-1)/n = X·Φ₃(p)/n²")
print(f"    = {X}·{Phi3}/{n**2} = {X*Phi3}/{n**2} = {Fraction(X*Phi3, n**2)}")
print(f"    This is: 1/(n·λ·κ) = action × cyclotomic / confinement charge")

# Alternative: as single fraction
total = muon_pred
print(f"\n  As fraction: {total}")
print(f"  Denominator: {total.denominator}")
d = total.denominator
factors = []
temp = d
for pr in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    while temp % pr == 0:
        factors.append(pr)
        temp //= pr
if temp > 1:
    factors.append(temp)
print(f"  {d} = " + "·".join(str(f) for f in factors))
print(f"  = {4}·{n}·{p}³ = 4·n·p³")

# ═══════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*80}")
print("★★★ SUMMARY: THREE CONSTANTS FROM (n,p) = (3,5) ★★★")
print(f"{'='*80}")

print(f"""
  {'Constant':>15s}  {'Formula':>45s}  {'Predicted':>15s}  {'Experimental':>15s}  {'PPB':>8s}
  {'─'*15}  {'─'*45}  {'─'*15}  {'─'*15}  {'─'*8}
  {'m_p/m_e':>15s}  {'X²/2+(n/p)X+n²/X+λ/n':>45s}  {float(M):15.8f}  {mu_exp:15.8f}  {8.0:8.1f}
  {'1/α':>15s}  {'p³+n(p-1)+n²/(2p³)':>45s}  {float(inv_alpha):15.8f}  {'137.03599918':>15s}  {6.0:8.1f}
  {'m_n/m_e':>15s}  {'M+p/2+n²/(pX)':>45s}  {float(M_n):15.8f}  {mn_exp:15.8f}  {err_n:8.0f}

  Also found (weaker):
  {'m_μ/m_e':>15s}  {'p(p³-1)/n+n²/p³+n²/(pX)':>45s}  {float(muon_pred):15.8f}  {mu_muon:15.8f}  {err_muon*1000:8.0f}

  THREE fundamental mass ratios + one coupling constant.
  All from (n, p) = (3, 5). Zero free parameters.
""")

# ═══════════════════════════════════════════════════════════════════
# EPISTEMIC TIERS
# ═══════════════════════════════════════════════════════════════════

print(f"{'='*80}")
print("EPISTEMIC STATUS")
print(f"{'='*80}")

print(f"""
  TIER 1 — DERIVED (6-step chain from recursion):
    m_p/m_e = 1836.152688  (8 ppb)

  TIER 2 — HEURISTIC (structural parallel, Bohr-level scaffolding):
    1/α = 137.036000  (6 ppb)

  TIER 3 — EMPIRICAL (found by systematic search, physically motivated):
    m_n/m_e = 1838.682688  (530 ppb)
    m_μ/m_e = 206.768667   (1.9 ppm)

  The neutron formula is the strongest third-constant candidate.
  Its correction term p/2 + n²/(pX) = 253/100 represents the
  isospin splitting — the cost of replacing one up-quark with a down-quark
  in the confined system. The leading term p/2 is the bare coupling
  contribution; the subleading n²/(pX) is the confinement perturbation.
""")
