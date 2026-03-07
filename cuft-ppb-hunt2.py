#!/usr/bin/env python3
"""
PPB Hunt v2 — Search for RASP formulas among sub-ppb precision constants.
Focus: nuclear mass ratios (deuteron, triton, helion, alpha particle)
and dimensionless constants (electron g-2, proton g-factor).

Strategy: We already have M_p and M_n. Nuclear composites should relate.
"""

from fractions import Fraction
from itertools import combinations_with_replacement, product
import sys

# === RASP PARAMETERS ===
n, p = 3, 5
lam = Fraction(1, p**3 - 1)           # 1/124
Phi3 = p**2 + p + 1                    # 31
Phi3_3 = 13                            # Phi_3(3)
Phi3_2 = 7                             # Phi_3(2)
X = n * p * (p - 1)                    # 60

# === KNOWN FORMULAS (from paper) ===
M_p = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + Fraction(1, n * (p**3 - 1))
M_n = M_p + Fraction(p, 2) + Fraction(n**2, p * X) + Fraction(n * p, (p**3 - 1)**2)
M_mu = Fraction(p, n) * Fraction(p**3 - 1) + Fraction(1, 2*p) + Fraction(1, p * (p**3 - 1))
alpha_inv = Fraction(p**3) + Fraction(n * (p-1)) + Fraction(n**2, 2 * p**3)

print("=" * 70)
print("PPB HUNT v2 — SUB-PPB PRECISION TARGETS")
print("=" * 70)
print(f"M_p = {float(M_p):.12f}  (CODATA: 1836.15267342600)")
print(f"M_n = {float(M_n):.12f}  (CODATA: 1838.68366200000)")
print(f"M_mu = {float(M_mu):.12f}")
print(f"1/alpha = {float(alpha_inv):.12f}")

# === EXPERIMENTAL VALUES (CODATA 2022) ===
targets = {
    "deuteron":  {"val": Fraction(367048296765500, 10**11), "unc": Fraction(63, 10**10),
                  "exact": 3670.48296765500, "unc_f": 6.3e-8, "note": "p+n bound"},
    "triton":    {"val": Fraction(549692153551, 10**8), "unc": Fraction(21, 10**8),
                  "exact": 5496.92153551, "unc_f": 2.1e-7, "note": "p+2n bound"},
    "helion":    {"val": Fraction(549588527984, 10**8), "unc": Fraction(16, 10**8),
                  "exact": 5495.88527984, "unc_f": 1.6e-7, "note": "2p+n bound"},
    "alpha_p":   {"val": Fraction(729429954171, 10**8), "unc": Fraction(17, 10**8),
                  "exact": 7294.29954171, "unc_f": 1.7e-7, "note": "2p+2n bound"},
}

# Nuclear binding energies in m_e units (from MeV / 0.51099895 MeV)
# Deuteron BE: 2.224566 MeV → 2.224566/0.51099895 = 4.35339 m_e
# He-3 BE: 7.718041 MeV → 15.1037 m_e
# H-3 BE: 8.481821 MeV → 16.5985 m_e
# He-4 BE: 28.29567 MeV → 55.3733 m_e

print("\n" + "=" * 70)
print("ATTACK 1: COMPOSITE MASS = SUM OF CONSTITUENTS - BINDING")
print("=" * 70)

# Deuteron = M_p + M_n - BE_d/m_e
d_naive = M_p + M_n
d_exp = 3670.48296765500
d_residual_naive = float(d_naive) - d_exp
print(f"\nDeuteron naive (M_p + M_n) = {float(d_naive):.12f}")
print(f"Experimental:                {d_exp:.11f}")
print(f"Difference (= binding):      {d_residual_naive:.11f} m_e")
print(f"Expected BE:                 {2.224566/0.51099895:.11f} m_e")
print(f"Discrepancy:                 {d_residual_naive - 2.224566/0.51099895:.11e} m_e")

# The binding energy must also be a RASP expression for this to work
BE_d_me = d_residual_naive  # binding energy in electron mass units
print(f"\nBinding energy to match: {BE_d_me:.12f}")

# === BUILDING BLOCKS for binding energy search ===
blocks = {}
# Small integer ratios of RASP parameters
for a in range(-3, 4):
    for b in range(-3, 4):
        for c in range(-3, 4):
            for d_exp_loop in range(-2, 3):
                val = Fraction(0)
                label_parts = []
                if a != 0:
                    val += a * Fraction(n)
                    label_parts.append(f"{a}n")
                if b != 0:
                    val += b * Fraction(p)
                    label_parts.append(f"{b}p")
                if c != 0:
                    val += c * Fraction(Phi3)
                    label_parts.append(f"{c}Phi3")
                if d_exp_loop != 0:
                    val += d_exp_loop * lam
                    label_parts.append(f"{d_exp_loop}lam")
                if val != 0 and label_parts:
                    label = "+".join(label_parts)
                    blocks[label] = val

# Add specific combinations
special = {
    "n/p": Fraction(n, p),
    "p/n": Fraction(p, n),
    "n^2/p": Fraction(n**2, p),
    "p^2/n": Fraction(p**2, n),
    "n*p": Fraction(n * p),
    "n^2": Fraction(n**2),
    "p^2": Fraction(p**2),
    "n*p^2": Fraction(n * p**2),
    "X": Fraction(X),
    "X/2": Fraction(X, 2),
    "X/p": Fraction(X, p),
    "Phi3/p": Fraction(Phi3, p),
    "Phi3/n": Fraction(Phi3, n),
    "n*Phi3": Fraction(n * Phi3),
    "p*Phi3": Fraction(p * Phi3),
    "n/Phi3": Fraction(n, Phi3),
    "p/Phi3": Fraction(p, Phi3),
    "1/(n*p)": Fraction(1, n * p),
    "1/X": Fraction(1, X),
    "n/X": Fraction(n, X),
    "p/X": Fraction(p, X),
    "n^2/X": Fraction(n**2, X),
    "lam*n": lam * n,
    "lam*p": lam * p,
    "lam/n": lam / n,
    "lam/p": lam / p,
    "lam^2": lam * lam,
    "lam^2*n": lam * lam * n,
    "lam^2*p": lam * lam * p,
    "lam^2*n*p": lam * lam * n * p,
    "Phi3_3": Fraction(Phi3_3),
    "Phi3_2": Fraction(Phi3_2),
    "n*Phi3_3": Fraction(n * Phi3_3),
    "n*Phi3_2": Fraction(n * Phi3_2),
    "p*Phi3_3": Fraction(p * Phi3_3),
    "p*Phi3_2": Fraction(p * Phi3_2),
    "Phi3_2*Phi3_3": Fraction(Phi3_2 * Phi3_3),
    "n*Phi3_2*Phi3_3": Fraction(n * Phi3_2 * Phi3_3),
    "1/2": Fraction(1, 2),
    "1/3": Fraction(1, 3),
    "1/5": Fraction(1, 5),
    "n^2/(2*p^3)": Fraction(n**2, 2 * p**3),
    "p/(2*n)": Fraction(p, 2*n),
    "n/(2*p)": Fraction(n, 2*p),
}
blocks.update(special)

def denom_clean(frac):
    """Check if denominator factors only through {2, 3, 5, 31}."""
    d = abs(frac.denominator)
    for pp in [2, 3, 5, 31]:
        while d % pp == 0:
            d //= pp
    return d == 1

def prime_factors(nn):
    if nn <= 1: return {}
    factors = {}
    d = 2
    nn = abs(nn)
    while d * d <= nn:
        while nn % d == 0:
            factors[d] = factors.get(d, 0) + 1
            nn //= d
        d += 1
    if nn > 1:
        factors[nn] = factors.get(nn, 0) + 1
    return factors

# ============================================================
# ATTACK 2: DIRECT SEARCH — deuteron as RASP expression
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 2: GREEDY SEARCH FOR DEUTERON m_d/m_e")
print("=" * 70)

d_target = 3670.48296765500

# Step 1: Best leading term
print("\nStep 1: Best leading term...")
best_leads = []
for label, val in blocks.items():
    if val <= 0: continue
    r = abs(float(val) - d_target)
    if r < 100:  # within 100 of target
        best_leads.append((r, label, val))
best_leads.sort()

for r, label, val in best_leads[:10]:
    print(f"  {label:30s} = {float(val):12.6f}  residual {r:.6f}")

# Step 2: Try 2M_p as leading term (since d ≈ 2*proton)
print(f"\n  2*M_p = {float(2*M_p):.12f}  residual {float(2*M_p) - d_target:.12f}")
print(f"  M_p+M_n = {float(M_p+M_n):.12f}  residual {float(M_p+M_n) - d_target:.12f}")

# The residual from M_p + M_n is the binding energy
BE_residual = M_p + M_n - Fraction(367048296765500, 10**11)
print(f"\n  Binding residual (M_p+M_n - exp): {float(M_p+M_n) - d_target:.12f}")

# Can we express the binding energy?  BE_d ≈ 4.353 m_e
BE_target = float(M_p + M_n) - d_target
print(f"\n  Binding energy target: {BE_target:.12f} m_e")

# Search for binding energy as RASP expression
print("\n  Searching for BE as RASP expression...")
best_be = []
for label, val in blocks.items():
    r = abs(float(val) - BE_target)
    if r < 2 and float(val) > 0:
        best_be.append((r, label, val))
best_be.sort()
for r, label, val in best_be[:10]:
    ppb_r = r / d_target * 1e9
    print(f"    {label:30s} = {float(val):12.8f}  residual {r:.8f} ({ppb_r:.1f} ppb of d)")

# ============================================================
# ATTACK 3: Search for deuteron/proton ratio
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 3: DEUTERON-TO-PROTON RATIO (4.2 ppt precision!)")
print("=" * 70)

dp_target = 1.9990075012699
dp_unc = 8.4e-12

print(f"Target: m_d/m_p = {dp_target}")
print(f"Uncertainty: {dp_unc} ({dp_unc/dp_target*1e9:.4f} ppb)")

# This should be close to 2 - small correction
correction = 2.0 - dp_target
print(f"\n2 - m_d/m_p = {correction:.13f}")
print(f"This is the fractional binding energy (BE/m_p)")

# Is the correction a RASP fraction?
print(f"\nSearching for (2 - m_d/m_p) as RASP expression...")
best_corr = []
for label, val in blocks.items():
    r = abs(float(val) - correction)
    if r < 0.01 and float(val) > 0:
        ppb = r / dp_target * 1e9
        best_corr.append((ppb, label, val, r))
best_corr.sort()
for ppb, label, val, r in best_corr[:15]:
    d_check = Fraction(2) - val
    clean = denom_clean(d_check)
    print(f"    {label:30s} = {float(val):.13f}  → d/p = {float(d_check):.13f}  "
          f"residual {r:.2e} ({ppb:.1f} ppb) clean={clean}")

# ============================================================
# ATTACK 4: Direct 2-term and 3-term search for each target
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 4: SYSTEMATIC 2-TERM SEARCH")
print("=" * 70)

# Reduce blocks to most promising ~200
block_list = [(label, val) for label, val in blocks.items()
              if abs(float(val)) < 10000 and abs(float(val)) > 1e-10]
print(f"Using {len(block_list)} building blocks")

high_precision_targets = [
    ("deuteron/e", 3670.48296765500, 6.3e-8),
    ("triton/e", 5496.92153551, 2.1e-7),
    ("helion/e", 5495.88527984, 1.6e-7),
    ("alpha_p/e", 7294.29954171, 1.7e-7),
]

for tname, tval, tunc in high_precision_targets:
    print(f"\n--- {tname} = {tval} ± {tunc} ---")

    # 1-term
    best1 = []
    for label, val in block_list:
        r = abs(float(val) - tval)
        if r < 50:
            ppb = r / tval * 1e9
            best1.append((ppb, label, val))
    best1.sort()
    if best1:
        print(f"  Best 1-term:")
        for ppb, label, val in best1[:3]:
            sigma = abs(float(val) - tval) / tunc if tunc > 0 else 0
            clean = denom_clean(val)
            print(f"    {label:30s} = {float(val):.11f} ({ppb:.1f} ppb, {sigma:.1f}σ, clean={clean})")

    # 2-term (sample most promising pairs)
    best2 = []
    # For each good 1-term, search for correction
    for _, lead_label, lead_val in (best1[:5] if best1 else []):
        residual = tval - float(lead_val)
        for c_label, c_val in block_list:
            r = abs(float(c_val) - residual)
            if r < 1:
                total = lead_val + c_val
                ppb = abs(float(total) - tval) / tval * 1e9
                if ppb < 1000:
                    clean = denom_clean(total)
                    best2.append((ppb, f"{lead_label} + {c_label}", total, clean))

    # Also try M_p, M_n combinations as leading terms
    for lead_label, lead_val in [("M_p+M_n", M_p+M_n), ("2*M_p", 2*M_p), ("3*M_p", 3*M_p),
                                   ("2*M_n", 2*M_n), ("M_p+2*M_n", M_p+2*M_n),
                                   ("2*M_p+M_n", 2*M_p+M_n), ("2*M_p+2*M_n", 2*(M_p+M_n)),
                                   ("3*M_n", 3*M_n), ("4*M_p", 4*M_p)]:
        residual = tval - float(lead_val)
        if abs(residual) < 200:
            for c_label, c_val in block_list:
                # Try both signs
                for sign, slabel in [(1, "+"), (-1, "-")]:
                    total = lead_val + sign * c_val
                    r = abs(float(total) - tval)
                    ppb = r / tval * 1e9
                    if ppb < 500:
                        clean = denom_clean(total)
                        best2.append((ppb, f"{lead_label} {slabel} {c_label}", total, clean))

    best2.sort()
    if best2:
        print(f"  Best 2-term:")
        seen = set()
        count = 0
        for ppb, label, val, clean in best2:
            key = float(val)
            if key in seen: continue
            seen.add(key)
            sigma = abs(float(val) - tval) / tunc if tunc > 0 else 0
            d = val.denominator
            print(f"    {label:45s} = {float(val):.11f} ({ppb:.1f} ppb, {sigma:.1f}σ, "
                  f"clean={clean}, denom={d}={prime_factors(d)})")
            count += 1
            if count >= 8: break

# ============================================================
# ATTACK 5: ELECTRON ANOMALOUS MAGNETIC MOMENT
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 5: ELECTRON g-2 ANOMALY")
print("=" * 70)

a_e = 0.00115965218059  # Northwestern 2023
a_e_unc = 1.3e-13
print(f"a_e = {a_e}")
print(f"unc = {a_e_unc} ({a_e_unc/a_e*1e9:.4f} ppb)")

# a_e ≈ alpha/(2*pi) to first order in QED
# alpha = 1/137.036... so alpha/(2pi) ≈ 0.001161...
alpha_val = 1.0 / float(alpha_inv)
print(f"\nalpha/(2pi) = {alpha_val/(2*3.14159265358979):.14f}")
print(f"a_e         = {a_e:.14f}")
print(f"Ratio a_e / (alpha/2pi) = {a_e / (alpha_val/(2*3.14159265358979)):.14f}")

# Can we express a_e as a RASP fraction?
# a_e ≈ 0.00116 ≈ 1/862.6
print(f"\n1/a_e = {1/a_e:.8f}")
print(f"Searching for 1/a_e as RASP expression...")

ae_inv_target = 1.0 / a_e
best_ae = []
for label, val in block_list:
    if float(val) <= 0: continue
    r = abs(float(val) - ae_inv_target)
    if r < 50:
        ppb = r / ae_inv_target * 1e9
        best_ae.append((ppb, label, val))
best_ae.sort()
if best_ae:
    for ppb, label, val in best_ae[:5]:
        ae_formula = Fraction(1) / val
        clean = denom_clean(ae_formula)
        print(f"  1/({label}) = {float(ae_formula):.14f}  ({ppb:.1f} ppb, clean={clean})")

# Also try: a_e = small_fraction with RASP denominator
print(f"\nSearching for a_e directly as small RASP fraction...")
# a_e ≈ 1/862.6 ≈ lam * something
print(f"  a_e / lam = {a_e * 124:.10f}")  # a_e * (p^3-1)
print(f"  a_e * alpha_inv = {a_e * float(alpha_inv):.10f}")  # ~ 1/(2*pi)
print(f"  a_e * 2 * pi = {a_e * 2 * 3.14159265358979:.10f}")  # ~ alpha

# a_e = alpha/(2pi) * (1 + C2*(alpha/pi) + ...) — QED series
# The leading term alpha/(2*pi) involves pi, which is transcendental
# RASP can't produce pi, so a_e probably can't be a clean RASP fraction
print(f"\n  NOTE: a_e involves pi (QED series). Likely NOT a RASP rational.")

# ============================================================
# ATTACK 6: PROTON g-FACTOR
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 6: PROTON g-FACTOR")
print("=" * 70)

g_p = 5.5856946893
g_p_unc = 1.6e-9
print(f"g_p = {g_p}")
print(f"unc = {g_p_unc} ({g_p_unc/g_p*1e9:.4f} ppb)")

# g_p ≈ 5.586 — search
best_gp = []
for label, val in block_list:
    if float(val) <= 0: continue
    r = abs(float(val) - g_p)
    ppb = r / g_p * 1e9
    if ppb < 100000:  # within 100 ppm
        clean = denom_clean(val)
        best_gp.append((ppb, label, val, clean))
best_gp.sort()
if best_gp:
    print(f"\n  Best matches for g_p:")
    for ppb, label, val, clean in best_gp[:10]:
        sigma = abs(float(val) - g_p) / g_p_unc
        print(f"    {label:30s} = {float(val):.10f} ({ppb:.0f} ppb, {sigma:.1f}σ, clean={clean})")

# ============================================================
# ATTACK 7: mu_e/mu_p ratio
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 7: ELECTRON-TO-PROTON MAGNETIC MOMENT RATIO")
print("=" * 70)

mu_ratio = 658.21068789
mu_ratio_unc = 1.9e-7
print(f"|mu_e/mu_p| = {mu_ratio}")
print(f"unc = {mu_ratio_unc} ({mu_ratio_unc/mu_ratio*1e9:.4f} ppb)")

# mu_e/mu_p = (g_e/2) * (m_p/m_e) / (g_p/2) = g_e * M_p / g_p
# ≈ 2.0023 * 1836.15 / 5.5857 ≈ 658.21
# So mu_ratio ≈ M_p * (g_e / g_p)
# If g_e/g_p had a RASP expression, this would work

print(f"\nmu_ratio / M_p = {mu_ratio / float(M_p):.12f}")
print(f"This = g_e / g_p = {mu_ratio / float(M_p):.12f}")
print(f"  ≈ 2.0023 / 5.5857 = {2.00231930436 / 5.5856946893:.12f}")

# ============================================================
# ATTACK 8: NEUTRON-PROTON MASS DIFFERENCE (high precision)
# ============================================================
print("\n" + "=" * 70)
print("ATTACK 8: NEUTRON-PROTON MASS DIFFERENCE")
print("=" * 70)

# Our formula: M_n - M_p = p/2 + n^2/(pX) + np*lam^2
delta_formula = Fraction(p, 2) + Fraction(n**2, p * X) + Fraction(n * p, (p**3 - 1)**2)
delta_exp = 1838.68366200 - 1836.15267343  # = 2.53098857
print(f"Formula: p/2 + n^2/(pX) + np*lam^2 = {float(delta_formula):.12f}")
print(f"Experimental: {delta_exp:.11f}")
print(f"Residual: {float(delta_formula) - delta_exp:.2e}")
print(f"Formula fraction: {delta_formula} = {delta_formula.numerator}/{delta_formula.denominator}")
print(f"Denom: {delta_formula.denominator} = {prime_factors(delta_formula.denominator)}")
print(f"Clean: {denom_clean(delta_formula)}")

# The n-p mass difference is known very precisely from nuclear physics
# 1.29333236(46) MeV → in m_e: 2.5311770(9)
delta_precise = 1.29333236 / 0.51099895  # MeV to m_e ratio
delta_unc = 0.00000046 / 0.51099895
print(f"\nPrecise delta (from MeV): {delta_precise:.10f} ± {delta_unc:.2e}")
print(f"Formula:                  {float(delta_formula):.10f}")
print(f"Residual:                 {abs(float(delta_formula) - delta_precise):.2e}")
print(f"In ppb of delta:          {abs(float(delta_formula) - delta_precise)/delta_precise*1e9:.1f}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY — WHAT CAN REACH PPB?")
print("=" * 70)
print("""
The fundamental question: which constants have BOTH
  (a) experimental precision at ppb or better, AND
  (b) a plausible RASP formula?

Key insight: nuclear composites (d, t, h, alpha) involve nuclear binding
energies which are emergent from QCD — not directly from the RASP
recursion which operates at the level of individual particle masses.

The binding energy of the deuteron (2.224 MeV = 4.353 m_e) is NOT
a simple RASP fraction. It's a QCD many-body result. So d/e, t/e, h/e,
alpha/e mass ratios are fundamentally limited — they require both
RASP (for constituent masses) AND QCD binding (non-RASP).

Similarly, g-factors and magnetic moments involve QCD structure functions
(for the proton) or QED series involving pi (for the electron).

This means the RASP framework naturally produces:
  - Individual lepton masses (electron=1, muon, tau)
  - Individual baryon masses (proton, neutron)
  - Fine-structure constant (alpha)
  - Possibly meson masses (pion, phi — bound states in QCD vacuum)

But NOT nuclear physics composites or electromagnetic moments.
""")
