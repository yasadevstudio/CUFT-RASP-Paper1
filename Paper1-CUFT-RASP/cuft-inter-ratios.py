#!/usr/bin/env python3
"""
CUFT-RASP DIRECTION 2: INTER-SOLUTION MASS RATIOS
===================================================
YASA PRESENTS — 2026-02-24

M(3,5)=1836.153, M(4,3)=320.676, M(6,2)=111.024 don't individually
match particles (except proton). But do RATIOS between them match
ratios between known particles?
"""

import numpy as np
from fractions import Fraction

# ═══════════════════════════════════════════════════════════════════
# THE THREE PREDICTIONS
# ═══════════════════════════════════════════════════════════════════

solutions = {
    '(3,5)': float(Fraction(853811, 465)),    # 1836.152688
    '(4,3)': None,
    '(6,2)': None,
}

# Compute M(4,3) and M(6,2)
for nn, pp in [(4,3), (6,2)]:
    X = nn * pp * (pp - 1)
    L = Fraction(1, pp**3 - 1)
    M = Fraction(X**2, 2) + Fraction(nn, pp) * X + Fraction(nn**2, X) + L / nn
    solutions[f'({nn},{pp})'] = float(M)
    print(f"M({nn},{pp}) = {M} = {float(M):.10f}")

M35, M43, M62 = solutions['(3,5)'], solutions['(4,3)'], solutions['(6,2)']
print(f"M(3,5) = {M35:.10f}")

# ═══════════════════════════════════════════════════════════════════
# KNOWN PARTICLE MASSES (in m_e units)
# ═══════════════════════════════════════════════════════════════════

# Source: PDG 2024, converted via m_e = 0.51099895 MeV

particles = {
    # Leptons
    'electron': 1.0,
    'muon': 206.7682830,
    'tau': 3477.48,
    # Light mesons
    'pi±': 273.132,
    'pi0': 264.137,
    'K±': 966.12,
    'K0': 974.55,
    'eta': 1073.22,
    "eta'": 1873.99,
    # Vector mesons
    'rho': 1515.35,
    'omega': 1530.15,
    'phi': 1995.99,
    # Baryons
    'proton': 1836.15267,
    'neutron': 1838.68366,
    'Lambda': 2183.3,
    'Sigma+': 2330.6,
    'Xi0': 2573.0,
    'Omega-': 3271.1,
    'Delta': 2408.8,
    # Heavy mesons
    'D±': 3654.8,
    'D0': 3649.1,
    'Ds': 3853.0,
    'J/psi': 6057.1,
    'B±': 10340,
    'Upsilon': 18491,
    # Bosons
    'W': 157326,
    'Z': 178450,
    'Higgs': 245050,
}

# ═══════════════════════════════════════════════════════════════════
# INTER-SOLUTION RATIOS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("INTER-SOLUTION RATIOS")
print("="*70)

ratios_pred = {
    'M(3,5)/M(4,3)': M35/M43,
    'M(3,5)/M(6,2)': M35/M62,
    'M(4,3)/M(6,2)': M43/M62,
    'M(4,3)/M(3,5)': M43/M35,
    'M(6,2)/M(3,5)': M62/M35,
    'M(6,2)/M(4,3)': M62/M43,
}

for name, val in ratios_pred.items():
    print(f"  {name} = {val:.8f}")

# ═══════════════════════════════════════════════════════════════════
# SEARCH: DO ANY PARTICLE RATIOS MATCH?
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("SEARCHING ALL PARTICLE RATIOS FOR MATCHES")
print("="*70)

pnames = list(particles.keys())
matches = []

for pred_name, pred_val in ratios_pred.items():
    print(f"\n--- {pred_name} = {pred_val:.6f} ---")
    closest = []
    for i in range(len(pnames)):
        for j in range(len(pnames)):
            if i == j:
                continue
            r = particles[pnames[i]] / particles[pnames[j]]
            err = abs(r - pred_val) / pred_val
            if err < 0.05:  # within 5%
                closest.append((pnames[i], pnames[j], r, err))
                matches.append((pred_name, pnames[i], pnames[j], r, pred_val, err))

    closest.sort(key=lambda x: x[3])
    if closest:
        for a, b, r, err in closest[:5]:
            print(f"  {a}/{b} = {r:.6f}  (err: {err*100:.2f}%)")
    else:
        # Show closest misses
        all_ratios = []
        for i in range(len(pnames)):
            for j in range(len(pnames)):
                if i == j: continue
                r = particles[pnames[i]] / particles[pnames[j]]
                err = abs(r - pred_val) / pred_val
                all_ratios.append((pnames[i], pnames[j], r, err))
        all_ratios.sort(key=lambda x: x[3])
        print(f"  No match within 5%. Closest:")
        for a, b, r, err in all_ratios[:3]:
            print(f"    {a}/{b} = {r:.6f}  (err: {err*100:.2f}%)")

# ═══════════════════════════════════════════════════════════════════
# ALSO: DIFFERENCES AND PRODUCTS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("ALSO CHECKING: DIFFERENCES AND SUMS")
print("="*70)

combos = {
    'M(3,5) - M(4,3)': M35 - M43,
    'M(3,5) - M(6,2)': M35 - M62,
    'M(4,3) - M(6,2)': M43 - M62,
    'M(4,3) + M(6,2)': M43 + M62,
    'M(3,5) - M(4,3) - M(6,2)': M35 - M43 - M62,
    '2*M(4,3) - M(6,2)': 2*M43 - M62,
    'M(3,5)/M(4,3)/M(6,2)*something': M35/(M43*M62),
}

for name, val in combos.items():
    print(f"\n{name} = {val:.6f} m_e = {val*0.511:.2f} MeV")
    # Find closest particle
    closest = min(particles.items(), key=lambda x: abs(x[1] - val))
    err = (closest[1] - val) / val * 100
    print(f"  Closest: {closest[0]} = {closest[1]:.3f} m_e  (err: {err:+.2f}%)")

# ═══════════════════════════════════════════════════════════════════
# ALGEBRAIC RATIOS BETWEEN SOLUTIONS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("EXACT ALGEBRAIC RATIOS")
print("="*70)

# M(3,5) = 853811/465
# M(4,3) exact:
M43_frac = Fraction(24**2, 2) + Fraction(4, 3)*24 + Fraction(16, 24) + Fraction(1, 4*26)
# M(6,2) exact:
M62_frac = Fraction(12**2, 2) + Fraction(6, 2)*12 + Fraction(36, 12) + Fraction(1, 6*7)

print(f"M(3,5) = {Fraction(853811, 465)} = {float(Fraction(853811, 465)):.10f}")
print(f"M(4,3) = {M43_frac} = {float(M43_frac):.10f}")
print(f"M(6,2) = {M62_frac} = {float(M62_frac):.10f}")

R_35_43 = Fraction(853811, 465) / M43_frac
R_35_62 = Fraction(853811, 465) / M62_frac
R_43_62 = M43_frac / M62_frac

print(f"\nM(3,5)/M(4,3) = {R_35_43} = {float(R_35_43):.10f}")
print(f"M(3,5)/M(6,2) = {R_35_62} = {float(R_35_62):.10f}")
print(f"M(4,3)/M(6,2) = {R_43_62} = {float(R_43_62):.10f}")

# Simple approximations?
print(f"\nSimple approximation check:")
print(f"  M(3,5)/M(4,3) ≈ {float(R_35_43):.4f}  vs 5.75 = 23/4")
print(f"  M(3,5)/M(6,2) ≈ {float(R_35_62):.4f}  vs 16.5 = 33/2")
print(f"  M(4,3)/M(6,2) ≈ {float(R_43_62):.4f}  vs 2.888... ≈ 26/9")
print(f"    26/9 = {26/9:.10f}, actual = {float(R_43_62):.10f}, err = {abs(26/9 - float(R_43_62))/float(R_43_62)*100:.4f}%")

# Check: are these related to Diophantine structure?
print(f"\n--- Structural ratios from (n,p) ---")
print(f"  X(3,5)/X(4,3) = 60/24 = {60/24}")
print(f"  X(3,5)/X(6,2) = 60/12 = {60/12}")
print(f"  X(4,3)/X(6,2) = 24/12 = {24/12}")
print(f"  (X ratio)² / 2 ≈ M ratio? ")
print(f"    (60/24)² / 2 = {(60/24)**2/2:.4f} vs {float(R_35_43):.4f}")
print(f"    (60/12)² / 2 = {(60/12)**2/2:.4f} vs {float(R_35_62):.4f}")
print(f"    (24/12)² / 2 = {(24/12)**2/2:.4f} vs {float(R_43_62):.4f}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
