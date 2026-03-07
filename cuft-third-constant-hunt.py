#!/usr/bin/env python3
"""
CUFT-RASP: THIRD CONSTANT HUNT
================================
YASA PRESENTS — 2026-02-24

We have TWO fundamental constants from (n,p) = (3,5):
  M     = 853811/465  = 1836.152688... (proton mass ratio, 8 ppb)
  1/α   = 34259/250   = 137.036000     (fine structure constant, 6 ppb)

QUESTION: Is there a THIRD?

METHOD: Exhaustive search over simple rational expressions built from
RASP building blocks, compared to a database of known dimensionless
physical constants.
"""

import numpy as np
from fractions import Fraction
from itertools import combinations_with_replacement

# ═══════════════════════════════════════════════════════════════════
# RASP CONSTANTS
# ═══════════════════════════════════════════════════════════════════

n, p = 3, 5
G = p**2                    # Gamma = 25
L = Fraction(1, p**3 - 1)   # lambda = 1/124
X = n * p * (p - 1)         # X = 60
kappa = Fraction(1, p)      # 1/5
Phi3 = p**2 + p + 1         # 31
xs = Fraction(p**3 - 1, p)  # 124/5 = 24.8

# Our already-found constants
M = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + L / n
inv_alpha = Fraction(p**3) + n*(p-1) + Fraction(n**2, 2*p**3)

print("═" * 80)
print("CUFT-RASP: THIRD CONSTANT HUNT")
print("═" * 80)
print(f"n = {n}, p = {p}")
print(f"Γ = {G}, λ = {L} = {float(L):.8f}")
print(f"X = {X}, κ = {kappa}, Φ₃(p) = {Phi3}")
print(f"x_s = {xs} = {float(xs)}")
print(f"\nAlready found:")
print(f"  M     = {M} = {float(M):.10f}  (proton mass ratio)")
print(f"  1/α   = {inv_alpha} = {float(inv_alpha):.10f}  (fine structure)")

# ═══════════════════════════════════════════════════════════════════
# TARGET DATABASE — Dimensionless physical constants
# ═══════════════════════════════════════════════════════════════════

# All values from CODATA 2022 / PDG 2024 where applicable
targets = {
    # Lepton mass ratios
    "m_μ/m_e": 206.7682827,
    "m_τ/m_e": 3477.48,
    "m_e/m_μ": 0.00483633,
    "m_μ/m_τ": 0.05946,

    # Baryon mass ratios (to m_e)
    "m_n/m_e": 1838.68366173,
    "(m_n-m_p)/m_e": 2.53102720,
    "m_Δ(1232)/m_e": 2410.2,     # Delta baryon
    "m_Λ/m_e": 2183.2,           # Lambda baryon
    "m_Σ⁺/m_e": 2328.4,          # Sigma+ baryon

    # Meson mass ratios (to m_e)
    "m_π⁰/m_e": 264.14,
    "m_π±/m_e": 273.13,
    "m_K⁰/m_e": 974.07,
    "m_K±/m_e": 965.65,
    "m_ρ/m_e": 1517.1,           # rho meson (PDG 2024: 775.26 MeV)
    "m_ω/m_e": 1531.5,           # omega meson (782.66 MeV)
    "m_η/m_e": 1071.8,           # eta meson (547.862 MeV)
    "m_η'/m_e": 1873.3,          # eta prime (957.78 MeV)
    "m_φ/m_e": 1994.7,           # phi meson (1019.461 MeV)
    "m_J/ψ/m_e": 6057.5,         # J/psi (3096.9 MeV)

    # Gauge boson mass ratios
    "m_W/m_e": 157330,            # W boson (80.377 GeV)
    "m_Z/m_e": 178450,            # Z boson (91.1876 GeV)
    "m_H/m_e": 244900,            # Higgs (125.25 GeV)
    "m_W/m_Z": 0.88153,          # cos(θ_W)

    # Coupling constants
    "sin²θ_W(MS)": 0.23122,      # Weak mixing angle (MS-bar at M_Z)
    "sin²θ_W(OS)": 0.22290,      # On-shell
    "α_s(M_Z)": 0.1180,          # Strong coupling at M_Z
    "sin(θ_C)": 0.22500,         # Cabibbo angle

    # Proton properties
    "μ_p/μ_N": 2.79284734463,    # Proton magnetic moment
    "g_p/2": 2.79284734463,      # Same thing
    "r_p(fm)·m_e·c/ℏ": 0.002183, # Proton charge radius in Compton wavelengths

    # Useful combinations
    "α·M": 13.39836,              # alpha * proton mass ratio
    "M·α²": 0.097762,             # M * alpha^2
    "sqrt(M)": 42.850,            # sqrt of proton mass ratio
    "M^(1/3)": 12.248,            # cube root
    "ln(M)": 7.5152,              # natural log

    # QCD scale ratios
    "m_p/m_π±": 6.7226,
    "m_p/m_ρ": 1.2104,
    "f_π/m_e": 256.0,             # Pion decay constant (130.7 MeV)

    # Nuclear physics
    "B_d/m_e": 4.3567,            # Deuteron binding energy / m_e (2.2246 MeV)

    # Mathematical constants (for reference only)
    "π": 3.14159265,
    "e": 2.71828183,
    "π²": 9.8696,
    "4π²": 39.478,
}

print(f"\nTarget constants: {len(targets)}")

# ═══════════════════════════════════════════════════════════════════
# BASIS MONOMIALS — Building blocks for expressions
# ═══════════════════════════════════════════════════════════════════

# Each entry: (label, exact Fraction or float value)
# We include both positive and negative versions

def build_basis():
    """Build comprehensive basis of RASP monomials."""
    basis = []

    # Zero (for 2-term within 3-term framework)
    basis.append(("0", 0))

    # Simple integers and fractions
    for c in [1, 2, 3, 4, 6, 8, 9, 12]:
        basis.append((f"{c}", c))
        basis.append((f"-{c}", -c))
    for (num, den) in [(1,2), (1,3), (1,4), (1,6), (3,2), (5,2), (9,2)]:
        basis.append((f"{num}/{den}", num/den))
        basis.append((f"-{num}/{den}", -num/den))

    # Powers of n and p
    for label, val in [
        ("n", n), ("p", p),
        ("n²", n**2), ("p²", p**2),
        ("n³", n**3), ("p³", p**3),
        ("p⁴", p**4),
        ("np", n*p), ("n²p", n**2 * p), ("np²", n*p**2),
        ("n(p-1)", n*(p-1)), ("n²(p-1)", n**2*(p-1)),
        ("p(p-1)", p*(p-1)), ("p²(p-1)", p**2*(p-1)),
        ("n(p-1)²", n*(p-1)**2), ("n²(p-1)²", n**2*(p-1)**2),
        ("(p-1)²", (p-1)**2),
    ]:
        basis.append((label, val))
        basis.append((f"-{label}", -val))

    # Fractions of n and p
    for label, val in [
        ("n/p", n/p), ("p/n", p/n),
        ("n²/p", n**2/p), ("p²/n", p**2/n),
        ("n²/p²", n**2/p**2), ("p²/n²", p**2/n**2),
        ("n²/p³", n**2/p**3), ("n/p²", n/p**2),
        ("n/p³", n/p**3), ("n²/(2p³)", n**2/(2*p**3)),
        ("p/n²", p/n**2),
        ("n³/p", n**3/p), ("n³/p²", n**3/p**2),
        ("1/n", 1/n), ("1/p", 1/p),
        ("1/n²", 1/n**2), ("1/p²", 1/p**2),
        ("1/p³", 1/p**3), ("1/(np)", 1/(n*p)),
    ]:
        basis.append((label, val))
        basis.append((f"-{label}", -val))

    # Derived RASP quantities
    for label, val in [
        ("Γ", G), ("X", X),
        ("X/n", X/n), ("X/p", X/p), ("X/n²", X/n**2),
        ("X²/2", X**2/2),
        ("Γp", G*p), ("Γ/p", G/p), ("Γn", G*n),
        ("λ", float(L)), ("1/λ", float(1/L)),
        ("nλ", n*float(L)), ("pλ", p*float(L)),
        ("λ/n", float(L)/n),
        ("κ", 1/p), ("κ²", 1/p**2), ("κ³", 1/p**3),
        ("Φ₃", Phi3), ("1/Φ₃", 1/Phi3),
        ("n/Φ₃", n/Phi3), ("p/Φ₃", p/Phi3), ("n²/Φ₃", n**2/Phi3),
        ("Φ₃/n", Phi3/n), ("Φ₃/p", Phi3/p),
        ("x_s", float(xs)),
        ("n²/X", n**2/X),
        ("n²/(pX)", n**2/(p*X)),
        ("Φ₃·p", Phi3*p), ("Φ₃·n", Phi3*n),
        ("(p-1)Φ₃", (p-1)*Phi3),
        ("pΦ₃/n", p*Phi3/n),
        ("(p-1)p·Φ₃", (p-1)*p*Phi3),
        ("(p-1)p·Φ₃/n", (p-1)*p*Phi3/n),
    ]:
        basis.append((label, val))
        basis.append((f"-{label}", -val))

    # Filter out duplicates by value (keep first label)
    seen = {}
    unique = []
    for label, val in basis:
        key = round(val, 12)
        if key not in seen:
            seen[key] = label
            unique.append((label, val))
    return unique

basis = build_basis()
print(f"Basis monomials: {len(basis)}")

# ═══════════════════════════════════════════════════════════════════
# PHASE 1: SINGLE-TERM MATCHES
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("PHASE 1: SINGLE-TERM MATCHES")
print("═" * 80)

def check_match(value, label, threshold_ppm=1000):
    """Check if value matches any target constant."""
    matches = []
    for tname, tval in targets.items():
        if tval == 0:
            continue
        frac_err = abs(value - tval) / abs(tval)
        ppm = frac_err * 1e6
        if ppm < threshold_ppm and ppm > 0.001:  # Exclude exact matches (trivial)
            matches.append((ppm, tname, tval, label, value))
    return matches

all_matches_1 = []
for label, val in basis:
    if val == 0:
        continue
    matches = check_match(val, label, threshold_ppm=500)
    all_matches_1.extend(matches)

all_matches_1.sort()
if all_matches_1:
    print(f"\n{'PPM':>10s}  {'Target':>25s}  {'Target Value':>15s}  {'Expression':>30s}  {'Pred Value':>15s}")
    print("-" * 100)
    for ppm, tname, tval, label, value in all_matches_1[:30]:
        print(f"{ppm:10.1f}  {tname:>25s}  {tval:15.8f}  {label:>30s}  {value:15.8f}")
else:
    print("  No single-term matches below 500 ppm.")

# ═══════════════════════════════════════════════════════════════════
# PHASE 2: TWO-TERM MATCHES
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("PHASE 2: TWO-TERM MATCHES (A + B)")
print("═" * 80)

# Pre-filter: only consider sums in the range of our targets
target_vals = np.array([v for v in targets.values() if abs(v) > 0])
min_target = min(abs(target_vals)) * 0.5
max_target = max(abs(target_vals)) * 2

all_matches_2 = []
basis_vals = [(l, v) for l, v in basis]
N = len(basis_vals)

count = 0
for i in range(N):
    l1, v1 = basis_vals[i]
    if v1 == 0 and l1 == "0":
        continue  # skip 0 + something (that's single-term)
    for j in range(i, N):  # j >= i to avoid duplicates
        l2, v2 = basis_vals[j]
        s = v1 + v2
        if s == 0:
            continue
        # Quick range check
        if abs(s) < min_target * 0.01 or abs(s) > max_target * 10:
            continue
        label = f"{l1} + {l2}" if v2 >= 0 else f"{l1} + ({l2})"
        if l1 == "0":
            label = l2
        matches = check_match(s, label, threshold_ppm=100)
        all_matches_2.extend(matches)
        count += 1

all_matches_2.sort()
print(f"  Checked {count:,} two-term combinations")

# Deduplicate: keep best match per target
best_per_target_2 = {}
for ppm, tname, tval, label, value in all_matches_2:
    if tname not in best_per_target_2 or ppm < best_per_target_2[tname][0]:
        best_per_target_2[tname] = (ppm, tname, tval, label, value)

if best_per_target_2:
    print(f"\n{'PPM':>10s}  {'Target':>25s}  {'Target Value':>15s}  {'Expression':>40s}  {'Pred Value':>15s}")
    print("-" * 110)
    for tname in sorted(best_per_target_2, key=lambda t: best_per_target_2[t][0]):
        ppm, _, tval, label, value = best_per_target_2[tname]
        print(f"{ppm:10.2f}  {tname:>25s}  {tval:15.8f}  {label:>40s}  {value:15.8f}")
else:
    print("  No two-term matches below 100 ppm.")

# ═══════════════════════════════════════════════════════════════════
# PHASE 3: THREE-TERM MATCHES (focused on top targets)
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("PHASE 3: THREE-TERM MATCHES (A + B + C)")
print("═" * 80)

# For 3-term, focus on the most interesting targets
priority_targets = {
    "m_μ/m_e": 206.7682827,
    "m_n/m_e": 1838.68366173,
    "(m_n-m_p)/m_e": 2.53102720,
    "sin²θ_W(MS)": 0.23122,
    "α_s(M_Z)": 0.1180,
    "m_π⁰/m_e": 264.14,
    "m_π±/m_e": 273.13,
    "μ_p/μ_N": 2.79284734463,
    "m_W/m_Z": 0.88153,
    "m_η/m_e": 1071.8,
    "m_K±/m_e": 965.65,
    "m_Δ(1232)/m_e": 2410.2,
    "m_Λ/m_e": 2183.2,
    "sin(θ_C)": 0.22500,
    "B_d/m_e": 4.3567,
}

# Use a smaller, curated basis for 3-term to keep it tractable
basis_small = []
for label, val in basis:
    # Only positive values and zero (negatives handled by subtraction)
    if val >= 0 and abs(val) < 10000:
        basis_small.append((label, val))

# Precompute all 2-sums
two_sums = {}
for i in range(len(basis_small)):
    for j in range(i, len(basis_small)):
        l1, v1 = basis_small[i]
        l2, v2 = basis_small[j]
        s = v1 + v2
        label = f"{l1} + {l2}" if l1 != "0" else l2
        if label not in two_sums:
            two_sums[label] = s

all_matches_3 = []
count3 = 0

# For each priority target, search for 3-term matches
for tname, tval in priority_targets.items():
    best = (1e9, "", 0, "", 0)

    for i in range(len(basis_small)):
        l1, v1 = basis_small[i]
        for j in range(i, len(basis_small)):
            l2, v2 = basis_small[j]
            for k in range(j, len(basis_small)):
                l3, v3 = basis_small[k]
                s = v1 + v2 + v3
                if s == 0:
                    continue

                frac_err = abs(s - tval) / abs(tval)
                ppm = frac_err * 1e6

                if ppm < best[0] and ppm > 0.001:
                    parts = [l for l, v in [(l1,v1),(l2,v2),(l3,v3)] if l != "0"]
                    label = " + ".join(parts) if parts else "0"
                    best = (ppm, tname, tval, label, s)
                count3 += 1

    if best[0] < 100:  # Only report sub-100 ppm
        all_matches_3.append(best)

all_matches_3.sort()
print(f"  Checked ~{count3:,} three-term combinations")

if all_matches_3:
    print(f"\n{'PPM':>10s}  {'Target':>25s}  {'Target Value':>15s}  {'Expression':>50s}  {'Pred Value':>15s}")
    print("-" * 120)
    for ppm, tname, tval, label, value in all_matches_3:
        print(f"{ppm:10.2f}  {tname:>25s}  {tval:15.8f}  {label:>50s}  {value:15.8f}")
else:
    print("  No three-term matches below 100 ppm for priority targets.")

# ═══════════════════════════════════════════════════════════════════
# PHASE 4: STRUCTURAL TEMPLATES
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("PHASE 4: STRUCTURAL TEMPLATES (Mass/Alpha-like formulas)")
print("═" * 80)

# The mass formula evaluates at scale X: M = X²/2 + (n/p)X + n²/X + λ/n
# The alpha formula evaluates at scale p: 1/α = p³ + n(p-1) + n²/(2p³)
#
# Template 1: "Mass-like" — evaluate at different scales
# F(s) = s²/2 + (n/p)·s + n²/s + λ/n
#
# Template 2: "Alpha-like" — evaluate at different scales
# G(s) = s³ + n(s-1) + n²/(2s³)    [only for integer s]
#
# Template 3: "Polynomial in variable v"
# H(v) = a·v^k + b·v^j + c·v^m

# Template 1: Mass formula at different scales
print("\n--- Template 1: Mass formula F(s) = s²/2 + (n/p)s + n²/s + λ/n ---")
print(f"{'Scale s':>10s}  {'F(s)':>15s}  {'Closest match':>30s}  {'PPM':>10s}")
print("-"*70)
for s_label, s_val in [
    ("n", n), ("p", p), ("2n", 2*n), ("2p", 2*p),
    ("p-1", p-1), ("p+1", p+1), ("np", n*p), ("n(p-1)", n*(p-1)),
    ("Γ", G), ("Φ₃", Phi3), ("x_s", float(xs)),
    ("X/n", X/n), ("X/p", X/p),
    ("sqrt(X)", np.sqrt(X)), ("sqrt(Γ)", np.sqrt(G)),
]:
    if s_val <= 0:
        continue
    fs = s_val**2/2 + (n/p)*s_val + n**2/s_val + float(L)/n
    # Find closest target
    best_ppm = 1e9
    best_name = "none"
    for tname, tval in targets.items():
        if tval == 0:
            continue
        ppm = abs(fs - tval)/abs(tval) * 1e6
        if ppm < best_ppm:
            best_ppm = ppm
            best_name = tname
    print(f"{s_label:>10s}  {fs:15.6f}  {best_name:>30s}  {best_ppm:10.1f}")

# Template 2: Alpha formula at different integer scales
print("\n--- Template 2: Alpha formula G(s) = s³ + n(s-1) + n²/(2s³) ---")
print(f"{'Scale s':>10s}  {'G(s)':>15s}  {'Closest match':>30s}  {'PPM':>10s}")
print("-"*70)
for s_val in range(2, 15):
    gs = s_val**3 + n*(s_val - 1) + n**2/(2*s_val**3)
    best_ppm = 1e9
    best_name = "none"
    for tname, tval in targets.items():
        if tval == 0:
            continue
        ppm = abs(gs - tval)/abs(tval) * 1e6
        if ppm < best_ppm:
            best_ppm = ppm
            best_name = tname
    if best_ppm < 5000:
        print(f"{s_val:>10d}  {gs:15.6f}  {best_name:>30s}  {best_ppm:10.1f}")

# Template 3: "Coupling formula" — various polynomial forms
print("\n--- Template 3: Custom polynomial forms ---")
print(f"{'Formula':>50s}  {'Value':>15s}  {'Closest match':>25s}  {'PPM':>10s}")
print("-"*105)

custom_formulas = [
    # Muon-hunting formulas
    ("M/n²", float(M)/n**2),
    ("M/n² + n/p", float(M)/n**2 + n/p),
    ("M/n² + p/2", float(M)/n**2 + p/2),
    ("M/n² + n(p-1)/p²", float(M)/n**2 + n*(p-1)/p**2),
    ("(p-1)pΦ₃/n", (p-1)*p*Phi3/n),
    ("X²/(2n) + X/p + n/X", X**2/(2*n) + X/p + n/X),
    ("X²/(2p) + (n/p²)X + n²/(pX)", X**2/(2*p) + (n/p**2)*X + n**2/(p*X)),

    # Neutron-hunting formulas
    ("M + p/2 + n²/(pX)", float(M) + p/2 + n**2/(p*X)),
    ("M + p/2 + 1/Φ₃", float(M) + p/2 + 1/Phi3),
    ("M + p/2 + n/X", float(M) + p/2 + n/X),
    ("M + n²/p + λ", float(M) + n**2/p + float(L)),

    # Pion-hunting formulas
    ("2p³ + n(p-1) + 2", 2*p**3 + n*(p-1) + 2),
    ("2p³ + n(p-1) + n²/(p³)", 2*p**3 + n*(p-1) + n**2/p**3),
    ("2(1/α)", 2*float(inv_alpha)),
    ("n²·X/2 + n/p", n**2*X/2 + n/p),
    ("p²(p-1) + n(p-1) + n/p", p**2*(p-1) + n*(p-1) + n/p),
    ("2p³ + 2(p+1) + n²/(p³)", 2*p**3 + 2*(p+1) + n**2/p**3),

    # Weinberg angle hunting
    ("n/(2p+n)", n/(2*p+n)),
    ("n²/(n²+p²+np)", n**2/(n**2+p**2+n*p)),
    ("n/(2p+n) + n²/(2(2p+n)³)", n/(2*p+n) + n**2/(2*(2*p+n)**3)),
    ("1/p + λ", 1/p + float(L)),
    ("κ² + κ³", 1/p**2 + 1/p**3),
    ("n²/(n²+p²+n)", n**2/(n**2+p**2+n)),
    ("(p-n)/(p²-n)", (p-n)/(p**2-n)),

    # Strong coupling hunting
    ("n/p² - λ/n", n/p**2 - float(L)/n),
    ("n/p² - λ", n/p**2 - float(L)),
    ("n·κ²", n/p**2),
    ("κ² + κ⁴", 1/p**2 + 1/p**4),
    ("n·λ", n*float(L)),

    # Proton magnetic moment hunting
    ("n - κ", n - 1/p),
    ("n - κ - λ", n - 1/p - float(L)),
    ("n - κ - κ³", n - 1/p - 1/p**3),
    ("n - 1/p - 1/(pΦ₃)", n - 1/p - 1/(p*Phi3)),
    ("n - κ + κ²/(2n)", n - 1/p + 1/(2*n*p**2)),
    ("n - 1/(p+λ)", n - 1/(p + float(L))),

    # W/Z ratio hunting
    ("(Γ-n)/Γ", (G-n)/G),
    ("(p²-n)/p²+n/(2p³X)", (p**2-n)/p**2 + n/(2*p**3*X)),
    ("1-n/p²", 1-n/p**2),
    ("(p²-n+κ)/p²", (p**2-n+1/p)/p**2),

    # Deuteron binding
    ("(p-1)/n + λ", (p-1)/n + float(L)),
    ("p/n + λ/κ", p/n + float(L)*p),
    ("n - κ²", n - 1/p**2),
    ("p/2 + n²/(pX)", p/2 + n**2/(p*X)),

    # Scale-shifted alpha formulas
    ("n³ + p(n-1) + p²/(2n³)", n**3 + p*(n-1) + p**2/(2*n**3)),
    ("Γ + n(p-1) + n²/(2Γ)", G + n*(p-1) + n**2/(2*G)),

    # Mixed M and α expressions
    ("M/α (= M·(1/α))", float(M) * float(inv_alpha)),
    ("M·α", float(M) / float(inv_alpha)),
    ("M + 1/α", float(M) + float(inv_alpha)),
    ("M - 1/α", float(M) - float(inv_alpha)),
    ("M/(1/α)", float(M) / float(inv_alpha)),
    ("(1/α)²/M", float(inv_alpha)**2 / float(M)),
    ("sqrt(M·(1/α))", np.sqrt(float(M) * float(inv_alpha))),
    ("M/(1/α)²", float(M) / float(inv_alpha)**2),

    # Cabibbo angle
    ("n/(n+p+n+2)", n/(n+p+n+2)),
    ("κ + κ³", 1/p + 1/p**3),
    ("n²/Φ₃² · p", n**2/Phi3**2 * p),

    # Ratio-based (M divided by RASP quantities)
    ("M/n", float(M)/n),
    ("M/p", float(M)/p),
    ("M/(np)", float(M)/(n*p)),
    ("M/X", float(M)/X),
    ("M/Γ", float(M)/G),
    ("M/Φ₃", float(M)/Phi3),
    ("M/(n·Φ₃)", float(M)/(n*Phi3)),
    ("M/(p·Φ₃)", float(M)/(p*Phi3)),
    ("(1/α)/n", float(inv_alpha)/n),
    ("(1/α)/p", float(inv_alpha)/p),
    ("(1/α)·n", float(inv_alpha)*n),
    ("(1/α)·p", float(inv_alpha)*p),

    # Inter-solution based
    ("M(3,5)-M(4,3)", float(M) - (Fraction(24**2,2) + Fraction(4,3)*24 + Fraction(16,24) + Fraction(1,4*26))),
    # M(4,3) computed exactly
]

# Compute M(4,3) and M(6,2) exactly
n4, p4 = 4, 3
X4 = n4*p4*(p4-1)  # 24
L4 = Fraction(1, p4**3 - 1)  # 1/26
M43 = Fraction(X4**2, 2) + Fraction(n4, p4)*X4 + Fraction(n4**2, X4) + L4/n4
n6, p6 = 6, 2
X6 = n6*p6*(p6-1)  # 12
L6 = Fraction(1, p6**3 - 1)  # 1/7
M62 = Fraction(X6**2, 2) + Fraction(n6, p6)*X6 + Fraction(n6**2, X6) + L6/n6

# Add inter-solution formulas
custom_formulas.extend([
    ("M(3,5)+M(4,3)", float(M) + float(M43)),
    ("M(3,5)+M(6,2)", float(M) + float(M62)),
    ("M(4,3)+M(6,2)", float(M43) + float(M62)),
    ("M(3,5)-M(6,2)", float(M) - float(M62)),
    ("M(3,5)/M(4,3)", float(M) / float(M43)),
    ("M(3,5)/M(6,2)", float(M) / float(M62)),
    ("M(4,3)/M(6,2)", float(M43) / float(M62)),
    ("M(4,3)-M(6,2)", float(M43) - float(M62)),
    ("M(4,3)", float(M43)),
    ("M(6,2)", float(M62)),
    ("2·M(6,2)", 2*float(M62)),
    ("3·M(6,2)", 3*float(M62)),
    ("M(4,3)/2", float(M43)/2),
    ("M(4,3)·2", float(M43)*2),
])

for formula, value in custom_formulas:
    best_ppm = 1e9
    best_name = "none"
    for tname, tval in targets.items():
        if tval == 0:
            continue
        ppm = abs(value - tval)/abs(tval) * 1e6
        if ppm < best_ppm:
            best_ppm = ppm
            best_name = tname
    if best_ppm < 5000:
        marker = "  ★★★" if best_ppm < 100 else ("  ★★" if best_ppm < 500 else ("  ★" if best_ppm < 1000 else ""))
        print(f"{formula:>50s}  {value:15.8f}  {best_name:>25s}  {best_ppm:10.1f}{marker}")

# ═══════════════════════════════════════════════════════════════════
# PHASE 5: RATIO/PRODUCT SCAN
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("PHASE 5: RATIO/PRODUCT SCAN (A·B, A/B, A^k)")
print("═" * 80)

# Build value list from basis (nonzero, positive)
vals_for_ratio = [(l, v) for l, v in basis if v > 0.001]

all_matches_5 = []
for i in range(len(vals_for_ratio)):
    l1, v1 = vals_for_ratio[i]
    for j in range(len(vals_for_ratio)):
        l2, v2 = vals_for_ratio[j]
        if i == j:
            continue
        # Ratio
        ratio = v1 / v2
        label = f"{l1}/{l2}"
        for tname, tval in targets.items():
            if tval == 0:
                continue
            ppm = abs(ratio - tval)/abs(tval) * 1e6
            if ppm < 50 and ppm > 0.001:
                all_matches_5.append((ppm, tname, tval, label, ratio))

        # Product
        prod = v1 * v2
        label = f"{l1}·{l2}"
        for tname, tval in targets.items():
            if tval == 0:
                continue
            ppm = abs(prod - tval)/abs(tval) * 1e6
            if ppm < 50 and ppm > 0.001:
                all_matches_5.append((ppm, tname, tval, label, prod))

all_matches_5.sort()
# Deduplicate per target
best_per_target_5 = {}
for entry in all_matches_5:
    ppm, tname = entry[0], entry[1]
    if tname not in best_per_target_5 or ppm < best_per_target_5[tname][0]:
        best_per_target_5[tname] = entry

if best_per_target_5:
    print(f"\n{'PPM':>10s}  {'Target':>25s}  {'Target Value':>15s}  {'Expression':>40s}  {'Pred Value':>15s}")
    print("-" * 110)
    for tname in sorted(best_per_target_5, key=lambda t: best_per_target_5[t][0]):
        ppm, _, tval, label, value = best_per_target_5[tname]
        print(f"{ppm:10.2f}  {tname:>25s}  {tval:15.8f}  {label:>40s}  {value:15.8f}")

# ═══════════════════════════════════════════════════════════════════
# PHASE 6: DEEP DIVE — Specific high-value targets
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("PHASE 6: DEEP DIVE — Focused searches for highest-value targets")
print("═" * 80)

# For each high-value target, try many forms
deep_targets = {
    "m_μ/m_e": 206.7682827,
    "(m_n-m_p)/m_e": 2.53102720,
    "sin²θ_W(MS)": 0.23122,
    "μ_p/μ_N": 2.79284734463,
    "α_s(M_Z)": 0.1180,
}

for dtname, dtval in deep_targets.items():
    print(f"\n--- Hunting: {dtname} = {dtval} ---")
    hits = []

    # Try: a·n^i · p^j + b·n^k · p^l + c·n^m · p^o
    # with coefficients from {1, 1/2, 1/3, 2, 3, n, p}
    coeffs = [1, 0.5, 1/3, 2, 3, n, p, n/p, p/n, 1/n, 1/p, n**2, p**2,
              1/n**2, 1/p**2, n**2/p, n/p**2, n**2/p**2, n**2/p**3]
    powers_np = []
    for i in range(-3, 5):
        for j in range(-3, 5):
            val = n**i * p**j
            if abs(val) < 1e8 and abs(val) > 1e-8:
                powers_np.append((i, j, val))

    # 2-term: c1·n^i·p^j + c2·n^k·p^l
    for pi, pj, v1 in powers_np:
        residual = dtval - v1
        for pk, pl, v2 in powers_np:
            if (pi, pj) >= (pk, pl):  # Avoid counting twice
                continue
            if abs(v2) < abs(residual) * 0.001:
                continue
            frac = abs(v1 + v2 - dtval) / abs(dtval)
            if frac < 50e-6:  # 50 ppm
                hits.append((frac*1e6,
                    f"n^{pi}·p^{pj} + n^{pk}·p^{pl}",
                    v1 + v2))
            # Also try subtraction
            frac2 = abs(v1 - v2 - dtval) / abs(dtval)
            if frac2 < 50e-6:
                hits.append((frac2*1e6,
                    f"n^{pi}·p^{pj} - n^{pk}·p^{pl}",
                    v1 - v2))

    # Also try with Phi3 and lambda
    special_vals = [
        ("1/Φ₃", 1/Phi3), ("n/Φ₃", n/Phi3), ("p/Φ₃", p/Phi3),
        ("Φ₃", Phi3), ("λ", float(L)), ("nλ", n*float(L)),
        ("λ/n", float(L)/n), ("n²/X", n**2/X),
        ("n²/(pX)", n**2/(p*X)), ("1/(nΦ₃)", 1/(n*Phi3)),
        ("n/(pΦ₃)", n/(p*Phi3)),
    ]

    for pi, pj, v1 in powers_np:
        for sl, sv in special_vals:
            s = v1 + sv
            frac = abs(s - dtval) / abs(dtval)
            if frac < 50e-6:
                hits.append((frac*1e6,
                    f"n^{pi}·p^{pj} + {sl}",
                    s))
            s2 = v1 - sv
            frac2 = abs(s2 - dtval) / abs(dtval)
            if frac2 < 50e-6:
                hits.append((frac2*1e6,
                    f"n^{pi}·p^{pj} - {sl}",
                    s2))

    hits.sort()
    if hits:
        for ppm, formula, val in hits[:10]:
            marker = "  ★★★" if ppm < 1 else ("  ★★" if ppm < 10 else "  ★")
            print(f"  {ppm:8.2f} ppm  {formula:>40s}  = {val:.10f}{marker}")
    else:
        print(f"  No matches below 50 ppm.")

# ═══════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════

print("\n" + "═" * 80)
print("SUMMARY: BEST CANDIDATES FOR THIRD CONSTANT")
print("═" * 80)

print(f"""
ESTABLISHED RESULTS:
  M     = 853811/465  = 1836.152688...  (8.0 ppb)  — proton mass ratio
  1/α   = 34259/250   = 137.036000       (6.0 ppb)  — fine structure constant

Review the output above for the most promising third constant candidates.
Priority: any match below 10 ppm from a structurally clean RASP expression.
""")
