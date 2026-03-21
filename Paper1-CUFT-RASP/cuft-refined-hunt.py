#!/usr/bin/env python3
"""
CUFT-RASP: REFINED CONSTANT HUNT
==================================
YASA PRESENTS — 2026-02-24

PURPOSE: Two goals:
  1. Refine neutron mass (530 ppb → sub-100 ppb) by finding 4th correction term
  2. Hunt for NEW third constant candidates across QED, electroweak, and hadronic
     sectors — especially photon/QED constants not adequately tested before

METHOD: Deeper basis, tighter search, more targets including QED anomalous
moments, electroweak mixing, strong coupling, and mass ratios.
"""

from fractions import Fraction
import numpy as np
from itertools import combinations

# ═══════════════════════════════════════════════════════════════════
# RASP CONSTANTS (exact arithmetic where possible)
# ═══════════════════════════════════════════════════════════════════

n, p = 3, 5
G = p**2                      # Gamma = 25
L = Fraction(1, p**3 - 1)     # lambda = 1/124
X = n * p * (p - 1)           # X = 60
kappa = Fraction(1, p)        # 1/5
Phi3 = p**2 + p + 1           # 31
xs = Fraction(p**3 - 1, p)    # 124/5

# Established results (exact fractions)
M = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + L / n
inv_alpha = Fraction(p**3) + n*(p-1) + Fraction(n**2, 2*p**3)
alpha_RASP = 1 / float(inv_alpha)

# Neutron mass (current best)
delta_n = Fraction(p, 2) + Fraction(n**2, p * X)  # = 253/100
M_n = M + delta_n

# Other Diophantine solutions
n4, p4 = 4, 3
X4 = n4*p4*(p4-1)  # 24
L4 = Fraction(1, p4**3 - 1)  # 1/26
M43 = Fraction(X4**2, 2) + Fraction(n4, p4)*X4 + Fraction(n4**2, X4) + L4/n4
Phi3_4 = p4**2 + p4 + 1  # 13

n6, p6 = 6, 2
X6 = n6*p6*(p6-1)  # 12
L6 = Fraction(1, p6**3 - 1)  # 1/7
M62 = Fraction(X6**2, 2) + Fraction(n6, p6)*X6 + Fraction(n6**2, X6) + L6/n6

print("=" * 90)
print("CUFT-RASP: REFINED CONSTANT HUNT")
print("=" * 90)
print(f"n = {n}, p = {p}")
print(f"M     = {M} = {float(M):.12f}  (proton, 8 ppb)")
print(f"1/α   = {inv_alpha} = {float(inv_alpha):.12f}  (fine structure, 6 ppb)")
print(f"M_n   = {M_n} = {float(M_n):.12f}  (neutron, 530 ppb)")
print(f"M(4,3) = {M43} = {float(M43):.6f}")
print(f"M(6,2) = {M62} = {float(M62):.6f}")

# ═══════════════════════════════════════════════════════════════════
# EXPANDED TARGET DATABASE — More QED/photon/electroweak constants
# ═══════════════════════════════════════════════════════════════════

# CODATA 2022 / PDG 2024 values
targets = {
    # === QED / PHOTON CONSTANTS ===
    "a_e (electron g-2)/2":        0.00115965218128,    # Electron anomalous magnetic moment
    "a_μ (muon g-2)/2":            0.00116592061,       # Muon anomalous magnetic moment
    "g_e/2":                       1.00115965218128,    # Electron g-factor / 2
    "α (fine str)":                0.0072973525693,     # Fine structure constant
    "α/(2π) Schwinger":            0.0011614097,        # Leading QED correction
    "α/π":                         0.0023228194,        # alpha/pi
    "α²":                          5.32513e-5,          # alpha squared
    "α³":                          3.887e-7,            # alpha cubed
    "2α/3":                        0.004864902,         # 2/3 alpha
    "r_∞·λ_C (Rydberg×Compton)":   0.00364705,         # α²/2
    "α²/2":                        2.66257e-5,          # half alpha squared

    # === LEPTON MASS RATIOS ===
    "m_μ/m_e":                     206.7682827,
    "m_τ/m_e":                     3477.48,
    "m_e/m_μ":                     0.00483633169,
    "m_μ/m_τ":                     0.059461,
    "m_τ/m_μ":                     16.8170,
    "m_e/m_p":                     0.000544617021487,    # 1/M
    "m_e/m_n":                     0.000543867390,       # 1/M_n

    # === BARYON MASS RATIOS (to m_e) ===
    "m_n/m_e":                     1838.68366173,
    "(m_n-m_p)/m_e":               2.53098830,
    "m_n/m_p":                     1.00137841931,       # neutron/proton ratio
    "m_Δ(1232)/m_e":               2410.2,
    "m_Λ/m_e":                     2183.2,
    "m_Σ⁺/m_e":                    2328.4,
    "m_Ω⁻/m_e":                    3279.0,              # Omega baryon

    # === MESON MASS RATIOS (to m_e) ===
    "m_π⁰/m_e":                    264.14,
    "m_π±/m_e":                    273.13,
    "m_K⁰/m_e":                    974.07,
    "m_K±/m_e":                    965.65,
    "m_ρ/m_e":                     1517.1,
    "m_ω/m_e":                     1531.5,
    "m_η/m_e":                     1071.8,
    "m_η'/m_e":                    1873.3,
    "m_φ/m_e":                     1994.7,
    "m_J/ψ/m_e":                   6057.5,
    "m_D±/m_e":                    3663.5,              # D meson
    "m_B±/m_e":                    10340,               # B meson
    "f_π/m_e":                     256.0,               # Pion decay constant

    # === GAUGE BOSON MASS RATIOS ===
    "m_W/m_e":                     157330,
    "m_Z/m_e":                     178450,
    "m_H/m_e":                     244900,
    "m_W/m_p":                     85.667,              # W/proton
    "m_Z/m_p":                     97.166,              # Z/proton
    "m_H/m_p":                     133.391,             # Higgs/proton
    "m_W/m_Z":                     0.88153,             # cos(θ_W)

    # === ELECTROWEAK CONSTANTS ===
    "sin²θ_W(MS)":                 0.23122,             # Weak mixing angle MS-bar at M_Z
    "sin²θ_W(OS)":                 0.22290,             # On-shell
    "cos²θ_W":                     0.76878,
    "sin(2θ_W)":                   0.83907,             # sin(2·Weinberg)
    "sin(θ_C)":                    0.22500,             # Cabibbo angle
    "cos(θ_C)":                    0.97437,
    "sin²(θ_C)":                   0.05063,             # Cabibbo squared
    "V_us":                        0.2243,              # CKM element
    "V_cb":                        0.0422,              # CKM element
    "V_ub":                        0.00382,             # CKM element

    # === STRONG COUPLING ===
    "α_s(M_Z)":                    0.1180,              # Strong coupling at M_Z
    "α_s(1GeV)":                   0.47,                # Strong coupling at 1 GeV (approx)
    "Λ_QCD/m_p":                   0.226,               # QCD scale / proton mass (approx)

    # === PROTON PROPERTIES ===
    "μ_p/μ_N":                     2.79284734463,       # Proton magnetic moment
    "μ_n/μ_N":                     -1.91304273,         # Neutron magnetic moment
    "|μ_n|/μ_N":                   1.91304273,          # Absolute
    "μ_p/μ_n":                     -1.45989805,         # Ratio
    "|μ_p/μ_n|":                   1.45989805,
    "r_p (fm)":                    0.8414,              # Proton charge radius
    "σ_T/r_p²":                    0.943,               # Thomson / proton-radius²

    # === NUCLEAR PHYSICS ===
    "B_d/m_e":                     4.3567,              # Deuteron binding / m_e
    "B_d/(m_n-m_p)":               1.7208,              # Binding / n-p mass diff
    "m_d/m_p":                     1.99901,             # Deuteron/proton

    # === USEFUL DERIVED RATIOS ===
    "M·α":                         13.39836,            # proton mass × alpha
    "M·α²":                        0.09777,
    "M/α":                         251626,              # proton mass / alpha (too big)
    "sqrt(M)":                     42.850,
    "M^(1/3)":                     12.248,
    "ln(M)":                       7.5152,
    "1/α - M/α²":                  39.308,              # 137.036 - 1836.15/137.036²  (not standard)
    "M/(1/α)":                     13.39836,
    "α·M²":                        24583,

    # === MATHEMATICAL STRUCTURE TESTS ===
    "π":                           3.14159265,
    "e (Euler)":                   2.71828183,
    "π²":                          9.8696,
    "4π²":                         39.478,
    "2π":                          6.28318,
    "π/2":                         1.5708,
    "1/π":                         0.31831,
    "1/(2π)":                      0.15915,
    "e^π":                         23.1407,
    "π^e":                         22.4592,
}

print(f"\nTarget constants: {len(targets)}")

# ═══════════════════════════════════════════════════════════════════
# PHASE 1: NEUTRON MASS REFINEMENT
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("PHASE 1: NEUTRON MASS REFINEMENT — Finding 4th correction term")
print("=" * 90)

mn_exp = 1838.68366173   # CODATA 2022
mn_pred = float(M_n)     # Our current prediction
gap = mn_exp - mn_pred    # What we need to add

print(f"\n  Current prediction: {mn_pred:.12f}")
print(f"  Experimental:      {mn_exp:.12f}")
print(f"  Gap (δ₂):          {gap:.12f}")
print(f"  Gap in ppb:        {abs(gap)/mn_exp*1e9:.1f}")

# Build RASP correction terms to close the gap
# Gap ≈ 0.000974 — search for RASP expressions near this value
print(f"\n  Searching for RASP expressions ≈ {gap:.8f} ...")

# Generate candidate corrections from RASP building blocks
corrections = []

# Simple fractions of RASP quantities
for num_label, num in [
    ("1", 1), ("n", n), ("p", p), ("n²", n**2), ("p²", p**2),
    ("n³", n**3), ("np", n*p), ("n(p-1)", n*(p-1)),
    ("(p-1)", p-1), ("(p+1)", p+1), ("(p-1)²", (p-1)**2),
    ("2", 2), ("2n", 2*n), ("2p", 2*p),
]:
    for den_label, den in [
        ("X²", X**2), ("p·X²", p*X**2), ("n·X²", n*X**2),
        ("X·Φ₃", X*Phi3), ("p·X·Φ₃", p*X*Phi3), ("n·X·Φ₃", n*X*Phi3),
        ("p²·X", p**2*X), ("p³·X", p**3*X),
        ("p²·X·n", p**2*X*n), ("p³·X·n", p**3*X*n),
        ("Φ₃·p²", Phi3*p**2), ("Φ₃²", Phi3**2), ("Φ₃²·p", Phi3**2*p),
        ("Φ₃²·n", Phi3**2*n), ("Φ₃·p³", Phi3*p**3),
        ("X³", X**3), ("p·X³", p*X**3),
        ("(p³-1)²", (p**3-1)**2), ("(p³-1)·p", (p**3-1)*p),
        ("(p³-1)·p²", (p**3-1)*p**2), ("(p³-1)·X", (p**3-1)*X),
        ("p²·Φ₃·X", p**2*Phi3*X), ("n·p·Φ₃·X", n*p*Phi3*X),
        ("n²·X²", n**2*X**2), ("p²·X²", p**2*X**2),
        ("n·p²·X", n*p**2*X), ("n·p³", n*p**3),
        ("n²·p²·X", n**2*p**2*X), ("n²·p³", n**2*p**3),
        ("X·Φ₃·p²", X*Phi3*p**2),
        # Lambda-involving denominators
        ("(p³-1)·n²", (p**3-1)*n**2), ("(p³-1)·n·p", (p**3-1)*n*p),
        ("(p³-1)²·n", (p**3-1)**2*n),
        # Larger denominators
        ("X²·Φ₃", X**2*Phi3), ("X²·p²", X**2*p**2),
        ("n·X²·p", n*X**2*p), ("p²·X²·n", p**2*X**2*n),
    ]:
        if den == 0:
            continue
        val = Fraction(num, den)
        fval = float(val)
        if fval > 0 and abs(fval - gap) / gap < 0.05:  # Within 5% of gap
            err_ppb = abs(mn_pred + fval - mn_exp) / mn_exp * 1e9
            corrections.append((err_ppb, f"{num_label}/({den_label})", val, fval))

# Also try sums of two small terms
small_terms = []
for num_label, num in [("1",1),("n",n),("p",p),("n²",n**2),("2",2),("(p-1)",p-1)]:
    for den_label, den in [
        ("X²",X**2),("p·X²",p*X**2),("X·Φ₃",X*Phi3),
        ("p²·X",p**2*X),("p³·X",p**3*X),("Φ₃·p²",Phi3*p**2),
        ("Φ₃²",Phi3**2),("X³",X**3),("(p³-1)²",(p**3-1)**2),
        ("(p³-1)·p",(p**3-1)*p),("p²·Φ₃·X",p**2*Phi3*X),
        ("n·p²·X",n*p**2*X),("n·p³",n*p**3),
    ]:
        if den > 0:
            small_terms.append((f"{num_label}/({den_label})", Fraction(num, den)))

# Also include lambda-based corrections
small_terms.extend([
    ("λ·n/p²", L * n / p**2),
    ("λ/p²", L / p**2),
    ("λ·n/(p·Φ₃)", L * n / (p * Phi3)),
    ("λ/(p·Φ₃)", L / (p * Phi3)),
    ("λ²·n", L**2 * n),
    ("λ²·p", L**2 * p),
    ("λ²", L**2),
    ("λ·n²/(p²·X)", L * n**2 / (p**2 * X)),
    ("λ/X", L / X),
    ("λ·n/X", L * n / X),
    ("λ/(n·p)", L / (n * p)),
    ("λ·n²/p³", L * n**2 / p**3),
    ("n²/(Φ₃·p·X)", Fraction(n**2, Phi3 * p * X)),
    ("n·λ/p²", Fraction(n, p**2) * L),
])

# Try single small terms as the correction
for label, val in small_terms:
    fval = float(val)
    if fval > 0 and abs(fval - gap) / gap < 0.1:  # Within 10%
        new_mn = float(M_n) + fval
        err_ppb = abs(new_mn - mn_exp) / mn_exp * 1e9
        corrections.append((err_ppb, label, val, fval))

# Try pairs: current delta + small adjustment
# delta_n = p/2 + n²/(pX), try replacing with slightly different form
alt_deltas = []
for a_label, a_val in [
    ("p/2", Fraction(p, 2)),
    ("(p+1)/2", Fraction(p+1, 2)),
    ("(p-1)/2", Fraction(p-1, 2)),
    ("n", Fraction(n)),
    ("p/2+λ", Fraction(p, 2) + L),
    ("p/2-λ", Fraction(p, 2) - L),
]:
    for b_label, b_val in [
        ("n²/(pX)", Fraction(n**2, p*X)),
        ("1/Φ₃", Fraction(1, Phi3)),
        ("n/X", Fraction(n, X)),
        ("n/(p²(p-1))", Fraction(n, p**2*(p-1))),
        ("n²/(p²·X)", Fraction(n**2, p**2*X)),
        ("n/Φ₃", Fraction(n, Phi3)),
        ("λ", L),
        ("λ/n", L/n),
        ("n²/(X·Φ₃)", Fraction(n**2, X*Phi3)),
        ("n·λ/p", L*n/p),
    ]:
        for c_label, c_val in [
            ("0", Fraction(0)),
            ("λ·n/p²", L*n/p**2),
            ("n²/(Φ₃·p·X)", Fraction(n**2, Phi3*p*X)),
            ("λ/(n·p)", L/(n*p)),
            ("λ²·n", L**2*n),
            ("n/(p²·X)", Fraction(n, p**2*X)),
            ("1/(p²·Φ₃)", Fraction(1, p**2*Phi3)),
            ("n²/(p²·X²)", Fraction(n**2, p**2*X**2)),
            ("λ/p²", L/p**2),
            ("n/(p·X·Φ₃)", Fraction(n, p*X*Phi3)),
            ("-λ·n/p²", -L*n/p**2),
            ("-n²/(Φ₃·p·X)", -Fraction(n**2, Phi3*p*X)),
        ]:
            total = a_val + b_val + c_val
            ftotal = float(total)
            if ftotal <= 0:
                continue
            new_mn = float(M) + ftotal
            err_ppb = abs(new_mn - mn_exp) / mn_exp * 1e9
            if err_ppb < 500:  # Better than current 530 ppb
                label = f"{a_label} + {b_label}"
                if c_label != "0":
                    label += f" + {c_label}"
                alt_deltas.append((err_ppb, label, total, ftotal))

alt_deltas.sort()
corrections.sort()

print(f"\n  === Best 4th correction terms (added to M + p/2 + n²/(pX)) ===")
print(f"  {'ppb':>8s}  {'Correction δ₂':>40s}  {'δ₂ value':>15s}  {'New total ppb':>12s}")
print("  " + "-" * 80)
seen_ppb = set()
for err_ppb, label, val, fval in corrections[:30]:
    rounded = round(err_ppb, 1)
    if rounded in seen_ppb:
        continue
    seen_ppb.add(rounded)
    total_ppb = abs(float(M_n) + fval - mn_exp) / mn_exp * 1e9
    print(f"  {err_ppb:8.1f}  {label:>40s}  {fval:15.12f}  {total_ppb:12.1f}")

print(f"\n  === Alternative delta formulas (replacing p/2 + n²/(pX) entirely) ===")
print(f"  {'ppb':>8s}  {'Formula for Δ':>55s}  {'Δ value':>12s}")
print("  " + "-" * 80)
seen_ppb2 = set()
for err_ppb, label, val, fval in alt_deltas[:30]:
    rounded = round(err_ppb, 1)
    if rounded in seen_ppb2:
        continue
    seen_ppb2.add(rounded)
    print(f"  {err_ppb:8.1f}  {label:>55s}  {fval:12.10f}")


# ═══════════════════════════════════════════════════════════════════
# PHASE 2: QED / PHOTON CONSTANTS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("PHASE 2: QED / PHOTON CONSTANT HUNT")
print("=" * 90)

# Focus targets for this phase
qed_targets = {
    "a_e (g-2)/2":       0.00115965218128,
    "a_μ (g-2)/2":       0.00116592061,
    "α":                 0.0072973525693,
    "α/(2π)":            0.0011614097,
    "α/π":               0.0023228194,
    "α²":                5.32513e-5,
    "m_e/m_μ":           0.00483633169,
    "m_e/m_p":           0.000544617021487,
    "m_e/m_n":           0.000543867390,
}

# Build a comprehensive basis of RASP expressions (small values)
# For QED constants we need values in the range ~10⁻⁷ to ~10⁻²
print("\n  Building RASP expression basis for small-value constants...")

rasp_small = []  # (label, Fraction_value)

# Single-ratio terms
for num_l, num_v in [
    ("1", 1), ("n", n), ("p", p), ("n²", n**2), ("p²", p**2),
    ("2", 2), ("(p-1)", p-1), ("(p+1)", p+1), ("2n", 2*n),
    ("np", n*p), ("n(p-1)", n*(p-1)), ("n³", n**3),
]:
    for den_l, den_v in [
        ("X", X), ("X²", X**2), ("Γ", G), ("Γ²", G**2),
        ("p²", p**2), ("p³", p**3), ("p⁴", p**4), ("p⁵", p**5),
        ("Φ₃", Phi3), ("Φ₃·p", Phi3*p), ("Φ₃·n", Phi3*n),
        ("Φ₃·p²", Phi3*p**2), ("Φ₃²", Phi3**2),
        ("nX", n*X), ("pX", p*X), ("npX", n*p*X),
        ("n²X", n**2*X), ("p²X", p**2*X),
        ("(p³-1)", p**3-1), ("n(p³-1)", n*(p**3-1)),
        ("p(p³-1)", p*(p**3-1)),
        ("X·Φ₃", X*Phi3), ("pX·Φ₃", p*X*Phi3),
        ("p²·Φ₃", p**2*Phi3),
        ("Γ·X", G*X), ("Γ·p", G*p), ("Γ·Φ₃", G*Phi3),
        ("n·p²", n*p**2), ("n·p³", n*p**3),
        ("n²·p", n**2*p), ("n²·p²", n**2*p**2), ("n²·p³", n**2*p**3),
        ("M_int", 465),  # denominator of M
        ("2·p³", 2*p**3), ("2·Γ", 2*G),
    ]:
        if den_v == 0:
            continue
        val = Fraction(num_v, den_v)
        fval = float(val)
        if 1e-8 < fval < 1.0:  # Small-value range
            rasp_small.append((f"{num_l}/({den_l})", val))

# Add lambda-based
rasp_small.extend([
    ("λ", L),
    ("λ/n", L/n),
    ("λ/p", L/p),
    ("λ·n", L*n),
    ("λ·p", L*p),
    ("λ·n/p", L*n/p),
    ("λ·n/p²", L*n/p**2),
    ("λ²", L**2),
    ("λ²·n", L**2*n),
    ("λ²·p", L**2*p),
    ("λ/X", L/X),
    ("λ/(nX)", L/(n*X)),
    ("λ/(pX)", L/(p*X)),
    ("λ/Φ₃", L/Phi3),
    ("n²·λ/p³", Fraction(n**2,1)*L/p**3),
    ("λ·n²/p²", L*n**2/p**2),
])

# Deduplicate
seen_vals = {}
rasp_unique = []
for label, val in rasp_small:
    fval = float(val)
    key = round(fval, 15)
    if key not in seen_vals:
        seen_vals[key] = label
        rasp_unique.append((label, val, fval))

print(f"  Small-value basis: {len(rasp_unique)} terms")

# Single-term search
print(f"\n  --- Single-term matches ---")
single_hits = []
for label, val, fval in rasp_unique:
    for tname, tval in qed_targets.items():
        if tval == 0:
            continue
        ppm = abs(fval - tval) / abs(tval) * 1e6
        if ppm < 5000 and ppm > 0.001:
            single_hits.append((ppm, tname, tval, label, fval))

single_hits.sort()
if single_hits:
    print(f"  {'PPM':>10s}  {'Target':>20s}  {'Exper.':>15s}  {'Expression':>35s}  {'Value':>15s}")
    print("  " + "-" * 100)
    for ppm, tname, tval, label, fval in single_hits[:20]:
        marker = " ★★★" if ppm < 10 else (" ★★" if ppm < 100 else (" ★" if ppm < 500 else ""))
        print(f"  {ppm:10.2f}  {tname:>20s}  {tval:15.10f}  {label:>35s}  {fval:15.10f}{marker}")

# Two-term search for QED targets
print(f"\n  --- Two-term sum matches (A + B) ---")
two_hits = []
for i in range(len(rasp_unique)):
    l1, v1, f1 = rasp_unique[i]
    for j in range(i, len(rasp_unique)):
        l2, v2, f2 = rasp_unique[j]
        s = f1 + f2
        if s <= 0:
            continue
        for tname, tval in qed_targets.items():
            if tval == 0:
                continue
            ppm = abs(s - tval) / abs(tval) * 1e6
            if ppm < 500 and ppm > 0.001:
                label = f"{l1} + {l2}"
                two_hits.append((ppm, tname, tval, label, s))
        # Also subtraction
        d = f1 - f2
        if d > 0:
            for tname, tval in qed_targets.items():
                if tval == 0:
                    continue
                ppm = abs(d - tval) / abs(tval) * 1e6
                if ppm < 500 and ppm > 0.001:
                    label = f"{l1} - {l2}"
                    two_hits.append((ppm, tname, tval, label, d))

two_hits.sort()
# Deduplicate per target
best_two = {}
for entry in two_hits:
    tname = entry[1]
    if tname not in best_two or entry[0] < best_two[tname][0]:
        best_two[tname] = entry

if best_two:
    print(f"  {'PPM':>10s}  {'Target':>20s}  {'Exper.':>15s}  {'Expression':>45s}  {'Value':>15s}")
    print("  " + "-" * 110)
    for tname in sorted(best_two, key=lambda t: best_two[t][0]):
        ppm, _, tval, label, fval = best_two[tname]
        marker = " ★★★" if ppm < 10 else (" ★★" if ppm < 100 else " ★")
        print(f"  {ppm:10.2f}  {tname:>20s}  {tval:15.10f}  {label:>45s}  {fval:15.10f}{marker}")


# ═══════════════════════════════════════════════════════════════════
# PHASE 3: ELECTROWEAK / STRONG COUPLING HUNT
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("PHASE 3: ELECTROWEAK & STRONG COUPLING HUNT")
print("=" * 90)

ew_targets = {
    "sin²θ_W(MS)":     0.23122,
    "sin²θ_W(OS)":     0.22290,
    "cos²θ_W":         0.76878,
    "sin(θ_C)":        0.22500,
    "cos(θ_C)":        0.97437,
    "sin²(θ_C)":       0.05063,
    "V_us":            0.2243,
    "V_cb":            0.0422,
    "V_ub":            0.00382,
    "α_s(M_Z)":        0.1180,
    "m_W/m_Z":         0.88153,
    "sin(2θ_W)":       0.83907,
    "|μ_n|/μ_N":       1.91304273,
    "μ_p/μ_N":         2.79284734463,
    "|μ_p/μ_n|":       1.45989805,
    "B_d/(m_n-m_p)":   1.7208,
}

# For electroweak we need values in range ~0.01 to ~3
rasp_ew = []
for label, val, fval in rasp_unique:
    if 0.001 < fval < 5.0:
        rasp_ew.append((label, fval))

# Also add expressions specifically designed for this range
ew_special = [
    ("n/(n+p)", n/(n+p)),
    ("p/(n+p)", p/(n+p)),
    ("n²/(n²+p²)", n**2/(n**2+p**2)),
    ("p²/(n²+p²)", p**2/(n**2+p**2)),
    ("n/(2p)", n/(2*p)),
    ("n²/(2p²)", n**2/(2*p**2)),
    ("(p-n)/p²", (p-n)/p**2),
    ("(p-n)/(p²+n)", (p-n)/(p**2+n)),
    ("n/(p²+n)", n/(p**2+n)),
    ("n²/(n²+p²+np)", n**2/(n**2+p**2+n*p)),
    ("(p²-n²)/(p²+n²)", (p**2-n**2)/(p**2+n**2)),
    ("n²/Φ₃", n**2/Phi3),
    ("(p-1)/Φ₃", (p-1)/Phi3),
    ("p/Φ₃", p/Phi3),
    ("n·(p-1)/Φ₃²", n*(p-1)/Phi3**2),
    ("n/Φ₃", n/Phi3),
    ("(n/p)²", (n/p)**2),
    ("(n/p)³", (n/p)**3),
    ("1 - n/p²", 1 - n/p**2),
    ("1 - n/Γ", 1 - n/G),
    ("(Γ-n)/Γ", (G-n)/G),
    ("(Γ-n²)/Γ", (G-n**2)/G),
    ("(p²-n)/(p²+1)", (p**2-n)/(p**2+1)),
    ("n/(n+p+1)", n/(n+p+1)),
    ("p/(n+p+1)", p/(n+p+1)),
    ("(p-n)/(p+n+1)", (p-n)/(p+n+1)),
    ("n·κ²", n/p**2),
    ("n·κ² + κ⁴", n/p**2 + 1/p**4),
    ("n·κ² - λ/n", n/p**2 - float(L)/n),
    ("κ + κ³", 1/p + 1/p**3),
    ("κ² + κ³", 1/p**2 + 1/p**3),
    ("2κ²", 2/p**2),
    ("n·λ", n*float(L)),
    ("p·λ", p*float(L)),
    ("n·p·λ", n*p*float(L)),
    ("1/(2κ+1)", 1/(2/p+1)),
    ("κ/(1+κ)", (1/p)/(1+1/p)),
    ("κ²/(1+κ²)", (1/p**2)/(1+1/p**2)),
    ("n/(2Γ)", n/(2*G)),
    ("n/Γ", n/G),
    ("(p-1)/(2p)", (p-1)/(2*p)),
    ("n²/(Γ+n²)", n**2/(G+n**2)),
    ("n²/(Γ+Φ₃)", n**2/(G+Phi3)),
    ("(p-1)/p²", (p-1)/p**2),
    ("n(p-1)/(p³-1)", n*(p-1)/(p**3-1)),
    ("n²(p-1)/p⁴", n**2*(p-1)/p**4),
    ("n²/(p⁴-p)", n**2/(p**4-p)),
    ("n/(p³-1)·p", n*p/(p**3-1)),
    # Deeper electroweak templates
    ("n²·p/(n²+p²)²", n**2*p/(n**2+p**2)**2),
    ("(p²-n²)/(p²+n)", (p**2-n**2)/(p**2+n)),
    ("n/(p·Φ₃)·p²", n*p/Phi3),
    ("n·(p-1)/(p²+p+n)", n*(p-1)/(p**2+p+n)),
    # Magnetic moment range (1.4-2.8)
    ("p/2 + n²/(pX)", p/2 + n**2/(p*X)),
    ("n - κ", n - 1/p),
    ("n - κ - λ", n - 1/p - float(L)),
    ("n - κ - κ³", n - 1/p - 1/p**3),
    ("n - 1/(p+1)", n - 1/(p+1)),
    ("p/2 + 1/Φ₃", p/2 + 1/Phi3),
    ("p/2 + λ", p/2 + float(L)),
    ("p/2 + n/X", p/2 + n/X),
    ("n - n/p²", n - n/p**2),
    ("n - n/Γ", n - n/G),
    ("n - (p-n)/p²", n - (p-n)/p**2),
    ("n - 1/p - n²/(p²·Φ₃)", n - 1/p - n**2/(p**2*Phi3)),
    ("p-n + n/p - n/(p·Φ₃)", p-n + n/p - n/(p*Phi3)),
    ("2 - n/Γ", 2 - n/G),
    ("2 - 1/(nλ+1)", 2 - 1/(n*float(L)+1)),
    ("p/n + λ·p", p/n + float(L)*p),
    ("p/n - 1/Φ₃", p/n - 1/Phi3),
    ("(p²-n)/Φ₃ + λ", (p**2-n)/Phi3 + float(L)),
    ("3 - n/p", 3 - n/p),
    ("3 - n/p - κ²", 3 - n/p - 1/p**2),
    ("3 - n/p - λ/n", 3 - n/p - float(L)/n),
]

rasp_ew.extend(ew_special)

# Deduplicate
seen_ew = {}
rasp_ew_unique = []
for item in rasp_ew:
    if len(item) == 3:
        label, val, fval = item
    else:
        label, fval = item
    key = round(fval, 12)
    if key not in seen_ew:
        seen_ew[key] = label
        rasp_ew_unique.append((label, fval))

print(f"  Electroweak basis: {len(rasp_ew_unique)} terms")

# Search
ew_hits = []
for label, fval in rasp_ew_unique:
    for tname, tval in ew_targets.items():
        ppm = abs(fval - tval) / abs(tval) * 1e6
        if ppm < 5000 and ppm > 0.001:
            ew_hits.append((ppm, tname, tval, label, fval))

ew_hits.sort()
# Best per target
best_ew = {}
for entry in ew_hits:
    tname = entry[1]
    if tname not in best_ew or entry[0] < best_ew[tname][0]:
        best_ew[tname] = entry

print(f"\n  {'PPM':>10s}  {'Target':>20s}  {'Exper.':>12s}  {'Expression':>45s}  {'Value':>12s}")
print("  " + "-" * 105)
for tname in sorted(best_ew, key=lambda t: best_ew[t][0]):
    ppm, _, tval, label, fval = best_ew[tname]
    marker = " ★★★" if ppm < 10 else (" ★★" if ppm < 100 else (" ★" if ppm < 1000 else ""))
    print(f"  {ppm:10.2f}  {tname:>20s}  {tval:12.8f}  {label:>45s}  {fval:12.8f}{marker}")

# Two-term sums for electroweak
print(f"\n  --- Two-term sums for electroweak targets ---")
ew_two_hits = []
for i in range(len(rasp_ew_unique)):
    l1, f1 = rasp_ew_unique[i]
    for j in range(i, len(rasp_ew_unique)):
        l2, f2 = rasp_ew_unique[j]
        for s, op in [(f1+f2, "+"), (f1-f2, "-"), (f2-f1, "r-")]:
            if s <= 0.001 or s > 5:
                continue
            for tname, tval in ew_targets.items():
                ppm = abs(s - tval) / abs(tval) * 1e6
                if ppm < 100 and ppm > 0.001:
                    if op == "r-":
                        label = f"{l2} - {l1}"
                    else:
                        label = f"{l1} {op} {l2}"
                    ew_two_hits.append((ppm, tname, tval, label, s))

ew_two_hits.sort()
best_ew2 = {}
for entry in ew_two_hits:
    tname = entry[1]
    if tname not in best_ew2 or entry[0] < best_ew2[tname][0]:
        best_ew2[tname] = entry

if best_ew2:
    print(f"  {'PPM':>10s}  {'Target':>20s}  {'Exper.':>12s}  {'Expression':>50s}  {'Value':>12s}")
    print("  " + "-" * 110)
    for tname in sorted(best_ew2, key=lambda t: best_ew2[t][0]):
        ppm, _, tval, label, fval = best_ew2[tname]
        marker = " ★★★" if ppm < 10 else (" ★★" if ppm < 100 else " ★")
        print(f"  {ppm:10.2f}  {tname:>20s}  {tval:12.8f}  {label:>50s}  {fval:12.8f}{marker}")


# ═══════════════════════════════════════════════════════════════════
# PHASE 4: BROADER MASS RATIO HUNT (deeper templates)
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("PHASE 4: MASS RATIO HUNT — Deeper templates")
print("=" * 90)

mass_targets = {
    "m_μ/m_e":         206.7682827,
    "m_τ/m_e":         3477.48,
    "m_π⁰/m_e":        264.14,
    "m_π±/m_e":        273.13,
    "m_K⁰/m_e":        974.07,
    "m_K±/m_e":        965.65,
    "m_ρ/m_e":         1517.1,
    "m_η/m_e":         1071.8,
    "f_π/m_e":         256.0,
    "m_Δ(1232)/m_e":   2410.2,
    "m_Λ/m_e":         2183.2,
    "m_W/m_p":         85.667,
    "m_Z/m_p":         97.166,
    "m_H/m_p":         133.391,
    "m_τ/m_μ":         16.8170,
}

# Templates: evaluate mass-like and alpha-like formulas at various scales
# ALSO: try formulas involving both M and 1/α

print("\n  --- Mass formula F(s) = s²/2 + (n/p)s + n²/s + λ/n at all RASP scales ---")
mass_formula_hits = []
for s_label, s_val in [
    ("1", 1), ("2", 2), ("n", n), ("p", p), ("n+1", n+1), ("p-1", p-1),
    ("p+1", p+1), ("2n", 2*n), ("2p", 2*p), ("np", n*p),
    ("n(p-1)", n*(p-1)), ("Φ₃", Phi3), ("p²", p**2), ("x_s", float(xs)),
    ("X/n", X/n), ("X/p", X/p), ("n²", n**2), ("sqrt(X)", np.sqrt(X)),
    ("X/(np)", X/(n*p)), ("(p-1)²", (p-1)**2), ("2(p-1)", 2*(p-1)),
    ("n+p", n+p), ("2n+1", 2*n+1), ("3n", 3*n), ("Φ₃/p", Phi3/p),
    ("sqrt(np)", np.sqrt(n*p)), ("(p³-1)/p²", (p**3-1)/p**2),
    ("n·(p-1)", n*(p-1)), ("p·(p-1)/n", p*(p-1)/n),
]:
    if s_val <= 0:
        continue
    fs = s_val**2/2 + (n/p)*s_val + n**2/s_val + float(L)/n
    for tname, tval in mass_targets.items():
        ppm = abs(fs - tval)/abs(tval) * 1e6
        if ppm < 5000:
            mass_formula_hits.append((ppm, tname, tval, f"F({s_label})", fs))

# Alpha formula at various scales
print("  --- Alpha formula G(s) = s³ + n(s-1) + n²/(2s³) at integer/rational scales ---")
for s_label, s_val in [
    ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8),
    ("9", 9), ("10", 10), ("n", n), ("p", p), ("n+p", n+p),
    ("2n", 2*n), ("2p", 2*p),
]:
    if s_val <= 1:
        continue
    gs = s_val**3 + n*(s_val - 1) + n**2/(2*s_val**3)
    for tname, tval in mass_targets.items():
        ppm = abs(gs - tval)/abs(tval) * 1e6
        if ppm < 5000:
            mass_formula_hits.append((ppm, tname, tval, f"G({s_label})", gs))

# M and α combinations
print("  --- M and α combined expressions ---")
Mf = float(M)
af = float(inv_alpha)
alpha = 1/af

combinations_ma = [
    ("M/n²", Mf/n**2),
    ("M/n² + n/p", Mf/n**2 + n/p),
    ("M/n² + p/2", Mf/n**2 + p/2),
    ("M/(2n)", Mf/(2*n)),
    ("M/(n+p)", Mf/(n+p)),
    ("M/Φ₃", Mf/Phi3),
    ("M/p", Mf/p),
    ("M/n", Mf/n),
    ("M/p + 1/α", Mf/p + af),
    ("M/n - 1/α", Mf/n - af),
    ("M·n/(1/α)", Mf*n/af),
    ("M·p/(1/α)", Mf*p/af),
    ("M/(1/α)", Mf/af),  # = M·α
    ("M·α + p", Mf*alpha + p),
    ("M·α + n", Mf*alpha + n),
    ("M·α + 1", Mf*alpha + 1),
    ("M·α - 1", Mf*alpha - 1),
    ("(1/α)² - M", af**2 - Mf),
    ("(1/α)² + M", af**2 + Mf),
    ("(1/α)² / n", af**2 / n),
    ("(1/α)² / p", af**2 / p),
    ("(1/α)² / (np)", af**2 / (n*p)),
    ("(1/α)·n", af*n),
    ("(1/α)·p", af*p),
    ("(1/α)·(p-1)", af*(p-1)),
    ("(1/α)·n/p", af*n/p),
    ("(1/α)·p/n", af*p/n),
    ("(1/α)·n²", af*n**2),
    ("(1/α) + M/n", af + Mf/n),
    ("(1/α) + M/p", af + Mf/p),
    ("(1/α) + M/(np)", af + Mf/(n*p)),
    ("M - (1/α)·n", Mf - af*n),
    ("M + (1/α)", Mf + af),
    ("M - (1/α)", Mf - af),
    ("M - n·(1/α)", Mf - n*af),
    ("sqrt(M·(1/α))", np.sqrt(Mf*af)),
    ("sqrt(M)·n", np.sqrt(Mf)*n),
    ("sqrt(M)·p", np.sqrt(Mf)*p),
    ("sqrt(M)·(p-1)", np.sqrt(Mf)*(p-1)),
    ("M^(1/3)·n", Mf**(1/3)*n),
    ("M^(1/3)·p", Mf**(1/3)*p),
    ("M^(1/3)·(p-1)", Mf**(1/3)*(p-1)),
    ("M^(1/3)·n²", Mf**(1/3)*n**2),
    ("M^(2/3)", Mf**(2/3)),
    ("M^(2/3)·n", Mf**(2/3)*n),
    ("M^(2/3)/n", Mf**(2/3)/n),
    # Cross-solution combinations
    ("M(3,5)/M(4,3)·X", float(M)/float(M43)*X),
    ("M(3,5)/M(6,2)", float(M)/float(M62)),
    ("M(3,5)-M(4,3)", float(M)-float(M43)),
    ("M(4,3)/n", float(M43)/n),
    ("M(4,3)/p", float(M43)/p),
    ("M(6,2)·n", float(M62)*n),
    ("M(6,2)·p", float(M62)*p),
    ("M(4,3)-M(6,2)", float(M43)-float(M62)),
    ("M(6,2)²/M(3,5)", float(M62)**2/float(M)),
    ("M(4,3)·M(6,2)/M(3,5)", float(M43)*float(M62)/float(M)),
]

for formula, value in combinations_ma:
    for tname, tval in mass_targets.items():
        ppm = abs(value - tval)/abs(tval) * 1e6
        if ppm < 5000:
            mass_formula_hits.append((ppm, tname, tval, formula, value))

mass_formula_hits.sort()

# Best per target
best_mass = {}
for entry in mass_formula_hits:
    tname = entry[1]
    if tname not in best_mass or entry[0] < best_mass[tname][0]:
        best_mass[tname] = entry

print(f"\n  {'PPM':>10s}  {'Target':>20s}  {'Exper.':>12s}  {'Expression':>40s}  {'Value':>12s}")
print("  " + "-" * 100)
for tname in sorted(best_mass, key=lambda t: best_mass[t][0]):
    ppm, _, tval, label, fval = best_mass[tname]
    marker = " ★★★" if ppm < 10 else (" ★★" if ppm < 100 else (" ★" if ppm < 1000 else ""))
    print(f"  {ppm:10.2f}  {tname:>20s}  {tval:12.6f}  {label:>40s}  {fval:12.6f}{marker}")


# ═══════════════════════════════════════════════════════════════════
# PHASE 5: ALPHA-DERIVED CONSTANTS
# Using our exact α to compute QED predictions
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("PHASE 5: ALPHA-DERIVED PREDICTIONS")
print("=" * 90)

# Using α_RASP = 250/34259, compute known QED formulas
alpha_exact = Fraction(250, 34259)
print(f"\n  α_RASP = {alpha_exact} = {float(alpha_exact):.15f}")
print(f"  α_exp  = 0.007297352569...3")
print(f"  α error = {abs(float(alpha_exact) - 0.0072973525693)/0.0072973525693*1e9:.1f} ppb")

# Schwinger: a_e ≈ α/(2π) - (α/π)²·0.328... + ...
a_e_schwinger_1 = float(alpha_exact) / (2 * np.pi)
a_e_schwinger_2 = a_e_schwinger_1 - 0.328478965 * (float(alpha_exact)/np.pi)**2
a_e_exp = 0.00115965218128

print(f"\n  Electron anomalous magnetic moment (g-2)/2:")
print(f"    Experimental:           {a_e_exp:.15f}")
print(f"    α/(2π) [1-loop]:        {a_e_schwinger_1:.15f}  ({abs(a_e_schwinger_1-a_e_exp)/a_e_exp*1e6:.1f} ppm)")
print(f"    + 2-loop correction:    {a_e_schwinger_2:.15f}  ({abs(a_e_schwinger_2-a_e_exp)/a_e_exp*1e6:.1f} ppm)")

# Can we express a_e directly as RASP quantity?
# a_e ≈ 0.00115965 ≈ n²/(p²·(p³-1)) + small correction
rasp_ae_test = Fraction(n**2, p**2*(p**3-1))  # 9/3100 = 0.002903...
print(f"\n  n²/(p²·(p³-1)) = {rasp_ae_test} = {float(rasp_ae_test):.10f}  (not close)")

# Try: λ·n/p = (1/124)·(3/5) = 3/620 = 0.004839 — that's m_e/m_μ!
me_mmu_rasp = Fraction(n, p) * L  # = 3/(5·124) = 3/620
print(f"\n  INTERESTING: λ·n/p = {me_mmu_rasp} = {float(me_mmu_rasp):.10f}")
print(f"  m_e/m_μ (exp) = 0.00483633169")
print(f"  Error: {abs(float(me_mmu_rasp) - 0.00483633169)/0.00483633169*1e6:.1f} ppm")

# Try: n/(p·(p³-1)) = 3/(5·124) = same thing
print(f"  n/(p·(p³-1)) = {Fraction(n, p*(p**3-1))} = {float(Fraction(n, p*(p**3-1))):.10f}  (same)")

# What about 1/α in terms of M?
print(f"\n  Ratio tests:")
print(f"  M/(1/α) = {Mf/af:.10f}  = M·α")
print(f"  (1/α)/M·1000 = {af/Mf*1000:.10f}")
print(f"  M/(1/α)² = {Mf/af**2:.10f}")
print(f"  (M·(1/α))^(1/2) = {np.sqrt(Mf*af):.10f}")
print(f"  M + (1/α) = {Mf+af:.10f}")
print(f"  M - (1/α) = {Mf-af:.10f}")
print(f"  M - n·(1/α) = {Mf-n*af:.10f}")
print(f"  M/(1/α) - n = {Mf/af-n:.10f}")

# Check: is m_e/m_μ = λ·n/p = 3/620?
# If so, then m_μ/m_e = 620/3 = 206.6667 — error 490 ppm
# But m_μ/m_e experimental = 206.7682827
# So the correction is 206.7682827 - 206.6667 = 0.1016
# = 0.1016 ≈ n²/(pX) + n²/(p²Φ₃)?
mu_base = Fraction(p*(p**3-1), n)  # = 5·124/3 = 620/3
mu_gap = 206.7682827 - float(mu_base)
print(f"\n  MUON ANALYSIS:")
print(f"  Base: p(p³-1)/n = {mu_base} = {float(mu_base):.10f}")
print(f"  Experimental: 206.7682827")
print(f"  Gap: {mu_gap:.10f}")
print(f"  Gap/base: {mu_gap/float(mu_base)*1e6:.1f} ppm")

# Search for RASP expression matching the muon gap
print(f"\n  Searching for RASP expressions ≈ {mu_gap:.8f} ...")
mu_corrections = []
for label, val, fval in rasp_unique:
    if abs(fval - mu_gap) / mu_gap < 0.05:
        err = abs(float(mu_base) + fval - 206.7682827) / 206.7682827 * 1e6
        mu_corrections.append((err, label, fval))

# Also try combinations
for i in range(len(rasp_unique)):
    l1, v1, f1 = rasp_unique[i]
    if f1 > 0.5 or f1 < 0.001:
        continue
    for j in range(len(rasp_unique)):
        l2, v2, f2 = rasp_unique[j]
        if f2 > 0.5 or f2 < -0.5:
            continue
        s = f1 + f2
        if abs(s - mu_gap) / mu_gap < 0.01:
            err = abs(float(mu_base) + s - 206.7682827) / 206.7682827 * 1e6
            mu_corrections.append((err, f"{l1} + {l2}", s))

mu_corrections.sort()
if mu_corrections:
    print(f"  {'PPM':>10s}  {'Correction':>45s}  {'Value':>12s}")
    print("  " + "-" * 75)
    seen = set()
    for err, label, fval in mu_corrections[:20]:
        r = round(err, 1)
        if r in seen:
            continue
        seen.add(r)
        print(f"  {err:10.2f}  {label:>45s}  {fval:12.10f}")


# ═══════════════════════════════════════════════════════════════════
# PHASE 6: EXACT FRACTION VERIFICATION FOR TOP HITS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("PHASE 6: EXACT FRACTION VERIFICATION — Top candidates")
print("=" * 90)

# Verify the best hits with exact Fraction arithmetic
def factorize(n):
    """Simple factorization."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

print("\n  === ESTABLISHED ===")
print(f"  m_p/m_e = {M} = {float(M):.12f}")
print(f"    Denom: {M.denominator} = {' × '.join(f'{f}' for f in factorize(M.denominator))}")
print(f"    Error: {abs(float(M) - 1836.152673426)/1836.152673426*1e9:.1f} ppb")

print(f"\n  1/α = {inv_alpha} = {float(inv_alpha):.12f}")
print(f"    Denom: {inv_alpha.denominator} = 2·p³ = {2*p**3}")
print(f"    Error: {abs(float(inv_alpha) - 137.035999177)/137.035999177*1e9:.1f} ppb")

# Check: m_e/m_μ = λn/p?
me_mmu = Fraction(n, p) * L
print(f"\n  === CANDIDATE: m_e/m_μ ===")
print(f"  Formula: λ·n/p = n/(p(p³-1)) = {me_mmu}")
print(f"  Value: {float(me_mmu):.12f}")
print(f"  Denom: {me_mmu.denominator}")
print(f"  Experimental: 0.00483633169")
print(f"  Error: {abs(float(me_mmu) - 0.00483633169)/0.00483633169*1e6:.1f} ppm")
print(f"  → Inverted: m_μ/m_e = {1/me_mmu} = {float(1/me_mmu):.6f}")
print(f"  → Inverted error: {abs(float(1/me_mmu) - 206.7682827)/206.7682827*1e6:.1f} ppm")

# Neutron with best correction
M_n_best = M + Fraction(p, 2) + Fraction(n**2, p*X)
print(f"\n  === CANDIDATE: m_n/m_e ===")
print(f"  Formula: M + p/2 + n²/(pX) = {M_n_best}")
print(f"  Value: {float(M_n_best):.12f}")
print(f"  Denom: {M_n_best.denominator}")
print(f"  Experimental: 1838.68366173")
print(f"  Error: {abs(float(M_n_best) - 1838.68366173)/1838.68366173*1e9:.1f} ppb")


# ═══════════════════════════════════════════════════════════════════
# GRAND SUMMARY
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("GRAND SUMMARY")
print("=" * 90)

print(f"""
TIER 1 — Derived from dynamics (6-step chain):
  m_p/m_e = {M} = {float(M):.10f}   (8 ppb)

TIER 2 — Heuristic with structural motivation:
  1/α     = {inv_alpha} = {float(inv_alpha):.10f}   (6 ppb)

TIER 3 — Found by systematic search:
  m_n/m_e = {M_n} = {float(M_n):.10f}   (530 ppb)

Review Phase 1 output for neutron refinement results.
Review Phase 2-3 for new QED/electroweak candidates.
Review Phase 4 for mass ratio candidates.
Review Phase 5 for α-derived predictions and muon analysis.
""")
