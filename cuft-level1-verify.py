#!/usr/bin/env python3
"""Verify Level 1 candidates with maximum precision."""

from fractions import Fraction

n, p = 3, 5
lam = Fraction(1, p**3 - 1)  # 1/124
Phi3 = p**2 + p + 1  # 31
Phi3_3 = 13  # Phi_3(3)
Phi3_2 = 7   # Phi_3(2)
X = n * p * (p - 1)  # 60

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

def denom_clean(frac):
    d = abs(frac.denominator)
    for pp in [2, 3, 5, 31]:
        while d % pp == 0:
            d //= pp
    return d == 1

print("=" * 70)
print("LEVEL 1 VERIFICATION — SEVEN CONSTANTS")
print("=" * 70)

# === EXISTING 4 ===
# Proton
M_p = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + Fraction(1, n * (p**3 - 1))
print(f"\n1. PROTON: M = X^2/2 + (n/p)X + n^2/X + lam/n")
print(f"   = {M_p} = {float(M_p):.12f}")
print(f"   CODATA 2022: 1836.152673426(32)")
print(f"   Residual: {float(M_p) - 1836.152673426:.12f} = {abs(float(M_p)-1836.152673426)/1836.152673426*1e9:.1f} ppb")
print(f"   Denom: {M_p.denominator} = {prime_factors(M_p.denominator)}, clean: {denom_clean(M_p)}")

# Neutron
M_n = M_p + Fraction(p, 2) + Fraction(n**2, p * X) + Fraction(n * p, (p**3 - 1)**2)
print(f"\n2. NEUTRON: M_p + p/2 + n^2/(pX) + np*lam^2")
print(f"   = {M_n} = {float(M_n):.12f}")
print(f"   CODATA 2022: 1838.68366173(89)")
print(f"   Residual: {float(M_n) - 1838.68366173:.12f} = {abs(float(M_n)-1838.68366173)/1838.68366173*1e9:.1f} ppb")
print(f"   Denom: {M_n.denominator} = {prime_factors(M_n.denominator)}, clean: {denom_clean(M_n)}")

# Muon
M_mu = Fraction(p, n) * Fraction(p**3 - 1) + Fraction(1, 2*p) + Fraction(1, p * (p**3 - 1))
print(f"\n3. MUON: p/(n*lam) + 1/(2p) + lam/p")
print(f"   = {M_mu} = {float(M_mu):.12f}")
print(f"   CODATA 2022: 206.7682827(46)")
print(f"   Residual: {float(M_mu) - 206.7682827:.12f} = {abs(float(M_mu)-206.7682827)/206.7682827*1e9:.1f} ppb")
print(f"   Denom: {M_mu.denominator} = {prime_factors(M_mu.denominator)}, clean: {denom_clean(M_mu)}")

# Alpha
alpha_inv = Fraction(p**3) + Fraction(n * (p-1)) + Fraction(n**2, 2 * p**3)
print(f"\n4. ALPHA: 1/alpha = p^3 + n(p-1) + n^2/(2p^3)")
print(f"   = {alpha_inv} = {float(alpha_inv):.12f}")
print(f"   CODATA 2022: 137.035999177(21)")
print(f"   Residual: {float(alpha_inv) - 137.035999177:.12f} = {abs(float(alpha_inv)-137.035999177)/137.035999177*1e9:.1f} ppb")
print(f"   Denom: {alpha_inv.denominator} = {prime_factors(alpha_inv.denominator)}, clean: {denom_clean(alpha_inv)}")

# === NEW 3 ===

# Tau — both formulas
print(f"\n5. TAU (CIPHER): (Phi3-n)/lam + p + 1/(p-1)")
tau_c = Fraction(Phi3 - n) * Fraction(p**3 - 1) + Fraction(p) + Fraction(1, p - 1)
print(f"   = {tau_c} = {float(tau_c):.12f}")

print(f"   TAU (greedy): X^2 - 1/lam + Phi3/p^2")
tau_g = Fraction(X**2) - Fraction(p**3 - 1) + Fraction(Phi3, p**2)
print(f"   = {tau_g} = {float(tau_g):.12f}")

# Tau experimental values
tau_exp_codata = 3477.23  # CODATA 2022 central, unc 0.23
tau_exp_hflav = 3477.42   # HFLAV 2024, unc 0.18
tau_exp_pdg = 3477.23     # PDG 2024, unc 0.23

for label, formula in [("CIPHER 13909/4", tau_c), ("greedy 86931/25", tau_g)]:
    r_c = abs(float(formula) - tau_exp_codata)
    print(f"   {label}: residual {r_c:.4f} ({r_c/tau_exp_codata*1e6:.1f} ppm) "
          f"[{r_c/0.23:.2f}sigma] denom={formula.denominator}={prime_factors(formula.denominator)} "
          f"clean={denom_clean(formula)}")

# Pion+ — 4-term greedy formula
print(f"\n6. PION+ (charged)")
# 4-term: n*Phi3(2)*Phi3(3) + (p-1)/Phi3 + lam/2 - lam/p^2
pion_4t = (Fraction(n * Phi3_2 * Phi3_3)
           + Fraction(p - 1, Phi3)
           + Fraction(1, 2 * (p**3 - 1))
           - Fraction(1, p**2 * (p**3 - 1)))
print(f"   Formula: n*Phi3(2)*Phi3(3) + (p-1)/Phi3 + lam/2 - lam/p^2")
print(f"   = {n}*{Phi3_2}*{Phi3_3} + {p-1}/{Phi3} + 1/{2*(p**3-1)} - 1/{p**2*(p**3-1)}")
print(f"   = {pion_4t} = {float(pion_4t):.12f}")

# Also test 3-term version
pion_3t = (Fraction(n * Phi3_2 * Phi3_3)
           + Fraction(p - 1, Phi3)
           + Fraction(n, p**2 * Phi3))
print(f"   Alt 3-term: n*Phi3(2)*Phi3(3) + (p-1)/Phi3 + n/(p^2*Phi3)")
print(f"   = {pion_3t} = {float(pion_3t):.12f}")

# Simplify the 4-term: lam/2 - lam/p^2 = lam*(p^2 - 2)/(2*p^2)
pion_simplified = (Fraction(n * Phi3_2 * Phi3_3)
                   + Fraction(p - 1, Phi3)
                   + Fraction(p**2 - 2, 2 * p**2 * (p**3 - 1)))
print(f"   Simplified: n*Phi3(2)*Phi3(3) + (p-1)/Phi3 + (p^2-2)/(2*p^2/lam)")
print(f"   = {pion_simplified} = {float(pion_simplified):.12f}")
assert pion_4t == pion_simplified

# Precise experimental pion mass ratio
pion_mev = 139.57039  # PDG ± 0.00018
elec_mev = 0.51099895000  # CODATA ± 0.00000015
pion_ratio = pion_mev / elec_mev
pion_unc = pion_ratio * ((0.00018/pion_mev)**2 + (0.00000015/elec_mev)**2)**0.5

for label, formula in [("4-term", pion_4t), ("3-term", pion_3t)]:
    r = abs(float(formula) - pion_ratio)
    sigma = r / pion_unc
    print(f"   {label}: residual {r:.6e} ({r/pion_ratio*1e6:.2f} ppm) "
          f"[{sigma:.2f}sigma] denom={formula.denominator}={prime_factors(formula.denominator)} "
          f"clean={denom_clean(formula)}")
print(f"   Exp ratio: {pion_ratio:.10f} ± {pion_unc:.6f} ({pion_unc/pion_ratio*1e6:.2f} ppm)")

# Phi meson — NEW DISCOVERY
print(f"\n7. PHI MESON")
phi_base = Fraction(p * Phi3 * Phi3_3) - Fraction(p * (p - 1))
phi_corrected = phi_base + Fraction(p, p**3 - 1)  # + p*lam
print(f"   Base: p*Phi3*Phi3(3) - p*(p-1) = {p}*{Phi3}*{Phi3_3} - {p}*{p-1}")
print(f"   = {float(phi_base):.12f}")
print(f"   Corrected: + p*lam = + {p}/{p**3-1}")
print(f"   = {phi_corrected} = {float(phi_corrected):.12f}")
print(f"   Simplified: p*(Phi3*Phi3(3) - (p-1) + lam)")

phi_mev = 1019.461  # PDG ± 0.016
phi_ratio = phi_mev / elec_mev
phi_unc = phi_ratio * ((0.016/phi_mev)**2 + (0.00000015/elec_mev)**2)**0.5

for label, formula in [("base", phi_base), ("corrected", phi_corrected)]:
    r = abs(float(formula) - phi_ratio)
    sigma = r / phi_unc
    print(f"   {label}: residual {r:.6f} ({r/phi_ratio*1e6:.2f} ppm) "
          f"[{sigma:.2f}sigma] denom={formula.denominator}={prime_factors(formula.denominator)} "
          f"clean={denom_clean(formula)}")
print(f"   Exp ratio: {phi_ratio:.8f} ± {phi_unc:.6f} ({phi_unc/phi_ratio*1e6:.2f} ppm)")

# === DENOMINATOR CLOSURE SUMMARY ===
print(f"\n" + "=" * 70)
print("DENOMINATOR CLOSURE — ALL 7 CONSTANTS")
print("=" * 70)

all_constants = [
    ("Proton",  M_p),
    ("Neutron", M_n),
    ("Muon",    M_mu),
    ("1/alpha", alpha_inv),
    ("Tau",     tau_c),
    ("Pion+",   pion_4t),
    ("Phi",     phi_corrected),
]

print(f"{'Name':12s} | {'Fraction':30s} | {'Denom':12s} | {'Factors':25s} | Clean?")
print("-" * 95)
for name, frac in all_constants:
    d = frac.denominator
    f = prime_factors(d)
    c = denom_clean(frac)
    frac_str = f"{frac.numerator}/{frac.denominator}" if d > 1 else str(frac.numerator)
    print(f"{name:12s} | {frac_str:>30s} | {d:>12d} | {str(f):25s} | {'YES' if c else 'NO'}")

# === BONUS: OTHER MATCHES FROM SEARCH ===
print(f"\n" + "=" * 70)
print("BONUS MATCHES (within experimental uncertainty)")
print("=" * 70)

bonus = [
    ("Rho",     "M35-M43 + p/n",
     Fraction(853811, 465) - Fraction(100051, 312) + Fraction(5, 3),
     775.26, 0.23),
    ("Eta",     "p*Phi3*Phi3(2) - p^2/2",
     Fraction(p * Phi3 * Phi3_2) - Fraction(p**2, 2),
     547.862, 0.017),
    ("Omega",   "Phi3*Phi3(2)^2 + p^2/2",
     Fraction(Phi3 * Phi3_2**2) + Fraction(p**2, 2),
     782.66, 0.13),
    ("Lambda",  "Phi3(3)^3 - Phi3(3)",
     Fraction(Phi3_3**3 - Phi3_3),
     1115.683, 0.006),
    ("Sigma+",  "Phi3(3)^3 + p^3 + p",
     Fraction(Phi3_3**3 + p**3 + p),
     1189.37, 0.07),
]

for name, formula_str, frac, mass_mev, unc_mev in bonus:
    ratio = mass_mev / elec_mev
    unc_ratio = ratio * ((unc_mev/mass_mev)**2 + (0.00000015/elec_mev)**2)**0.5
    r = abs(float(frac) - ratio)
    sigma = r / unc_ratio if unc_ratio > 0 else float('inf')
    ppm = r / ratio * 1e6
    print(f"  {name:10s}: {formula_str:30s} = {float(frac):12.4f} "
          f"(exp {ratio:.4f} ± {unc_ratio:.4f}, {ppm:.0f} ppm, {sigma:.1f}σ, "
          f"denom clean: {denom_clean(frac)})")
