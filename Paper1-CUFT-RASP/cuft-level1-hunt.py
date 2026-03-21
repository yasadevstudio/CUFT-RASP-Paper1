#!/usr/bin/env python3
"""CUFT-RASP LEVEL 1 EXTENSION HUNT
Find exact rational formulas for 7+ fundamental constants.
Brute-force search over RASP building blocks.
"""

from fractions import Fraction
from math import gcd
import sys

# === RASP PARAMETERS ===
n, p = 3, 5
Gamma = p**2
lam = Fraction(1, p**3 - 1)  # 1/124
Phi3_5 = p**2 + p + 1  # 31
Phi3_3 = 3**2 + 3 + 1  # 13
Phi3_2 = 2**2 + 2 + 1  # 7

# Exact mass formulas for each Diophantine solution
def mass_exact(ni, pi):
    Xi = ni * pi * (pi - 1)
    if Xi == 0:
        return None
    lam_i = Fraction(1, pi**3 - 1)
    c1 = Fraction(ni, pi)
    c0 = Fraction(1, ni * (pi**3 - 1))
    c_neg1 = ni**2
    return Fraction(Xi**2, 2) + c1 * Xi + c0 + Fraction(c_neg1, Xi)

M_35 = mass_exact(3, 5)
M_43 = mass_exact(4, 3)
M_62 = mass_exact(6, 2)

# Neutron formula
M_neutron = M_35 + Fraction(p, 2) + Fraction(n**2, p * 60) + Fraction(n * p, (p**3 - 1)**2)

# Muon formula
M_muon = Fraction(p, n) * Fraction(1, lam) + Fraction(1, 2*p) + lam * Fraction(1, p)

# Alpha formula
alpha_inv = Fraction(p**3) + Fraction(n * (p-1)) + Fraction(n**2, 2 * p**3)

# Tau candidate (CIPHER)
M_tau_candidate = Fraction(Phi3_5 - n, 1) * Fraction(1, lam) + Fraction(p) + Fraction(1, p - 1)

print("=" * 70)
print("CUFT-RASP LEVEL 1 HUNT")
print("=" * 70)

print("\n=== EXACT MASS FORMULAS ===")
for label, val in [("M(3,5) proton", M_35), ("M(4,3)", M_43), ("M(6,2)", M_62),
                   ("Neutron", M_neutron), ("Muon", M_muon),
                   ("1/alpha", alpha_inv), ("Tau candidate", M_tau_candidate)]:
    print(f"  {label:20s} = {float(val):.10f}  [{val}]")

print("\n=== INTER-SOLUTION DIFFERENCES ===")
diffs = {
    "M35-M43": M_35 - M_43,
    "M35-M62": M_35 - M_62,
    "M43-M62": M_43 - M_62,
    "2*M43-M62": 2*M_43 - M_62,
    "n*M43": n * M_43,
    "p*M62": p * M_62,
}
for label, val in diffs.items():
    print(f"  {label:20s} = {float(val):.10f}")

# === TARGET PARTICLES ===
# (name, m/m_e ratio, uncertainty in m_e, notes)
targets = [
    ("tau",          3477.23,    0.23,    "PDG 2024, 66 ppm"),
    ("pion+",        273.13268,  0.00036, "PDG, 1.3 ppm"),
    ("pion0",        264.14,     0.18,    "PDG, 680 ppm"),
    ("rho",          1517.1,     1.0,     "PDG, 660 ppm (width 19%)"),
    ("kaon+",        966.12,     0.50,    "PDG, 520 ppm"),
    ("kaon0",        974.54,     0.50,    "PDG"),
    ("eta",          1072.6,     1.0,     "PDG"),
    ("omega",        1531.6,     1.0,     "PDG"),
    ("phi",          1994.9,     1.0,     "PDG"),
    ("J/psi",        6060.5,     1.0,     "PDG"),
    ("D+",           3661.3,     1.0,     "PDG"),
    ("D0",           3649.1,     1.0,     "PDG"),
    ("Delta",        2410.9,     2.0,     "PDG, width 117 MeV"),
    ("Lambda",       2184.1,     1.0,     "PDG"),
    ("Sigma+",       2327.1,     1.0,     "PDG"),
    ("deuteron",     3670.483,   0.001,   "CODATA, 0.3 ppb"),
    ("sin2thetaW",   0.23122,    0.00004, "PDG 2024"),
    ("alpha_s_MZ",   0.1180,     0.0009,  "PDG 2024"),
]

# === BUILDING BLOCKS ===
# Generate labeled exact rationals from RASP parameters

def factorize_denom(frac):
    """Check if denominator factors through {2,3,5,31} only."""
    d = abs(frac.denominator)
    for prime in [2, 3, 5, 31]:
        while d % prime == 0:
            d //= prime
    return d == 1  # True if fully factors through allowed set

def prime_factors(n):
    """Return dict of prime factors."""
    factors = {}
    d = 2
    n = abs(n)
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

# Generate building blocks: exact Fraction values with labels
blocks = []

# Primary single values
primaries = [
    ("1", Fraction(1)),
    ("2", Fraction(2)),
    ("n", Fraction(n)),
    ("p", Fraction(p)),
    ("n^2", Fraction(n**2)),
    ("p^2", Fraction(p**2)),
    ("p^3", Fraction(p**3)),
    ("Phi3", Fraction(Phi3_5)),
    ("Phi3(3)", Fraction(Phi3_3)),
    ("Phi3(2)", Fraction(Phi3_2)),
    ("p-1", Fraction(p-1)),
    ("p+1", Fraction(p+1)),
    ("p+2", Fraction(p+2)),
    ("n*p", Fraction(n*p)),
    ("n*(p-1)", Fraction(n*(p-1))),
    ("X", Fraction(60)),
    ("X43", Fraction(24)),
    ("X62", Fraction(12)),
    ("lam", lam),
    ("1/lam", Fraction(p**3 - 1)),
    ("lam^2", lam**2),
    ("Phi3-n", Fraction(Phi3_5 - n)),   # 28
    ("Phi3*lam", Fraction(Phi3_5) * lam),  # 31/124 = 1/4
    ("M35", M_35),
    ("M43", M_43),
    ("M62", M_62),
]

# Generate products and quotients of primary pairs
atoms_small = [
    ("1", Fraction(1)), ("2", Fraction(2)), ("n", Fraction(n)),
    ("p", Fraction(p)), ("n^2", Fraction(9)), ("p^2", Fraction(25)),
    ("p^3", Fraction(125)), ("Phi3", Fraction(31)), ("Phi3(3)", Fraction(13)),
    ("Phi3(2)", Fraction(7)), ("p-1", Fraction(4)), ("lam", lam),
    ("1/lam", Fraction(124)), ("X", Fraction(60)),
]

seen_vals = set()
for i, (k1, v1) in enumerate(atoms_small):
    for j, (k2, v2) in enumerate(atoms_small):
        if i <= j and v1 * v2 != 0:
            prod = v1 * v2
            if prod not in seen_vals and 0 < abs(float(prod)) < 1e7:
                blocks.append((f"{k1}*{k2}", prod))
                seen_vals.add(prod)
        if v2 != 0:
            quot = v1 / v2
            if quot not in seen_vals and 0 < abs(float(quot)) < 1e7:
                blocks.append((f"{k1}/{k2}", quot))
                seen_vals.add(quot)

# Add mass formulas and inter-solution combos
for label, val in primaries:
    if val not in seen_vals and val != 0:
        blocks.append((label, val))
        seen_vals.add(val)

for label, val in diffs.items():
    if val not in seen_vals:
        blocks.append((label, val))
        seen_vals.add(val)

# Add triple products of small atoms (for larger terms)
key_atoms = [
    ("n", Fraction(3)), ("p", Fraction(5)), ("Phi3", Fraction(31)),
    ("Phi3(3)", Fraction(13)), ("Phi3(2)", Fraction(7)), ("p-1", Fraction(4)),
]
for i, (k1, v1) in enumerate(key_atoms):
    for j, (k2, v2) in enumerate(key_atoms):
        for k, (k3, v3) in enumerate(key_atoms):
            if i <= j <= k:
                prod = v1 * v2 * v3
                if prod not in seen_vals and 0 < float(prod) < 1e7:
                    blocks.append((f"{k1}*{k2}*{k3}", prod))
                    seen_vals.add(prod)

# Sort by absolute value for greedy search
blocks.sort(key=lambda x: abs(float(x[1])), reverse=True)

print(f"\n=== BUILDING BLOCKS: {len(blocks)} terms generated ===")

# === GREEDY SEARCH ===
print("\n" + "=" * 70)
print("GREEDY SEARCH RESULTS")
print("=" * 70)

def greedy_search(target_val, target_unc, max_terms=4):
    """Find sum of RASP terms matching target via greedy descent."""
    remaining = Fraction(target_val).limit_denominator(10**15)
    terms_found = []

    for step in range(max_terms):
        best_label = None
        best_val = None
        best_residual = float('inf')

        for label, val in blocks:
            if val == 0:
                continue
            # Try +val and -val
            for sign in [1, -1]:
                r = abs(float(remaining - sign * val))
                if r < best_residual:
                    best_residual = r
                    best_label = label
                    best_val = sign * val

        if best_label is None:
            break

        terms_found.append((best_label, best_val))
        remaining -= best_val

        if abs(float(remaining)) < target_unc:
            break

    total = sum(v for _, v in terms_found)
    return terms_found, float(total), float(remaining)

for name, target, unc, notes in targets:
    terms, total, residual = greedy_search(target, unc)
    frac_err = abs(residual) / target if target != 0 else 0
    within = abs(residual) < unc

    # Check denominator closure of total
    total_frac = sum(v for _, v in terms)
    denom_ok = factorize_denom(total_frac)
    denom_factors = prime_factors(total_frac.denominator)

    print(f"\n--- {name} ---")
    print(f"  Target: {target} ± {unc} ({notes})")
    print(f"  Formula: ", end="")
    for i, (label, val) in enumerate(terms):
        sign = "+" if float(val) >= 0 else "-"
        if i == 0:
            sign = "" if float(val) >= 0 else "-"
        print(f" {sign} {label}", end="")
    print()
    print(f"  Value:  {total:.10f}")
    print(f"  Residual: {residual:.2e} ({frac_err*1e6:.1f} ppm)")
    print(f"  Within uncertainty: {'YES' if within else 'no'}")
    print(f"  Exact fraction: {total_frac}")
    print(f"  Denominator: {total_frac.denominator} = {denom_factors}")
    print(f"  Denom in {{2,3,5,31}}: {'YES' if denom_ok else 'NO'}")

# === FOCUSED SEARCHES ===
print("\n" + "=" * 70)
print("FOCUSED ANALYSIS: KNOWN CANDIDATES")
print("=" * 70)

# TAU validation
print("\n--- TAU (CIPHER formula) ---")
tau_formula = (Fraction(Phi3_5 - n) * Fraction(p**3 - 1)
               + Fraction(p) + Fraction(1, p - 1))
tau_exp = Fraction(347723, 100)  # 3477.23
print(f"  Formula: (Phi3-n)/lam + p + 1/(p-1)")
print(f"  = ({Phi3_5 - n}) * {p**3 - 1} + {p} + 1/{p-1}")
print(f"  = {float(tau_formula):.10f}")
print(f"  = {tau_formula}")
print(f"  Experimental: 3477.23 ± 0.23 (66 ppm)")
print(f"  Residual: {float(tau_formula) - 3477.23:.6f} ({abs(float(tau_formula) - 3477.23)/3477.23*1e6:.1f} ppm)")
print(f"  Denom: {tau_formula.denominator} = {prime_factors(tau_formula.denominator)}")
print(f"  Denom in {{2,3,5,31}}: {factorize_denom(tau_formula)}")

# PION+ candidate
print("\n--- PION+ (new candidate) ---")
pion_formula = (Fraction(n) * Fraction(Phi3_2) * Fraction(Phi3_3)
                + Fraction(p - 1, Phi3_5)
                + Fraction(n, p**2 * Phi3_5))
print(f"  Formula: n*Phi3(2)*Phi3(3) + (p-1)/Phi3 + n/(p^2*Phi3)")
print(f"  = {n}*{Phi3_2}*{Phi3_3} + {p-1}/{Phi3_5} + {n}/{p**2 * Phi3_5}")
print(f"  = 273 + 4/31 + 3/775")
print(f"  = {float(pion_formula):.10f}")
print(f"  = {pion_formula}")

# Precise pion mass ratio
pion_mass_mev = 139.57039  # ± 0.00018
electron_mass_mev = 0.51099895000  # ± 0.00000015
pion_ratio_precise = pion_mass_mev / electron_mass_mev
print(f"  Experimental: m_pi+/m_e = {pion_ratio_precise:.8f}")
print(f"  (from {pion_mass_mev} / {electron_mass_mev} MeV)")
residual_pion = float(pion_formula) - pion_ratio_precise
print(f"  Residual: {residual_pion:.6e} ({abs(residual_pion)/pion_ratio_precise*1e6:.2f} ppm)")
exp_unc_pion = 0.00018 / electron_mass_mev  # propagate mass uncertainty
print(f"  Exp uncertainty: ±{exp_unc_pion:.6f} m_e ({exp_unc_pion/pion_ratio_precise*1e6:.2f} ppm)")
print(f"  Within uncertainty: {'YES' if abs(residual_pion) < exp_unc_pion else 'NO'}")
print(f"  Denom: {pion_formula.denominator} = {prime_factors(pion_formula.denominator)}")
print(f"  Denom in {{2,3,5,31}}: {factorize_denom(pion_formula)}")

# RHO with corrections
print("\n--- RHO (inter-solution + corrections) ---")
rho_base = M_35 - M_43
rho_exp = 1517.1  # ± 1.0
rho_width = 291.8  # width in m_e (149.1 MeV)
print(f"  Base: M(3,5) - M(4,3) = {float(rho_base):.6f}")
print(f"  Experimental: {rho_exp} ± {1.0} (width = {rho_width:.0f} m_e = 19%)")
rho_gap = rho_exp - float(rho_base)
print(f"  Gap to close: {rho_gap:.4f} m_e")
# Search for correction
print(f"  Searching corrections near {rho_gap:.4f}...")
best_corr = []
for label, val in blocks:
    fv = float(val)
    if fv == 0:
        continue
    r = abs(fv - rho_gap)
    if r < 2.0:
        best_corr.append((r, label, val))
best_corr.sort()
for r, label, val in best_corr[:5]:
    total = rho_base + val
    err = abs(float(total) - rho_exp)
    ppm = err / rho_exp * 1e6
    print(f"    + {label} = {float(val):.6f} -> total = {float(total):.6f} (err {ppm:.0f} ppm)")

# === EXHAUSTIVE 2-TERM SEARCH for pion ===
print("\n" + "=" * 70)
print("EXHAUSTIVE 2-TERM SEARCH (top candidates)")
print("=" * 70)

# For pion+, search all pairs
pion_target = Fraction(pion_mass_mev * 10**8).limit_denominator(10**15) / Fraction(int(electron_mass_mev * 10**11), 10**11)
# Use float target
pion_target_f = pion_ratio_precise
pion_unc_f = exp_unc_pion

print(f"\nPion+ target: {pion_target_f:.8f} ± {pion_unc_f:.6f}")
best_2term = []
# Only search blocks with value in reasonable range
big_blocks = [(l, v) for l, v in blocks if 200 < abs(float(v)) < 300]
small_blocks = [(l, v) for l, v in blocks if 0 < abs(float(v)) < 50]

for l1, v1 in big_blocks:
    for l2, v2 in small_blocks:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                total = s1 * v1 + s2 * v2
                err = abs(float(total) - pion_target_f)
                if err < 0.5:  # within 0.5 m_e
                    ppm = err / pion_target_f * 1e6
                    denom_ok = factorize_denom(total)
                    best_2term.append((ppm, s1, l1, s2, l2, float(total), denom_ok))

best_2term.sort()
print(f"Found {len(best_2term)} candidates within 0.5 m_e")
for ppm, s1, l1, s2, l2, val, dok in best_2term[:10]:
    sign1 = "+" if s1 > 0 else "-"
    sign2 = "+" if s2 > 0 else "-"
    print(f"  {sign1}{l1} {sign2}{l2} = {val:.8f} ({ppm:.1f} ppm, denom ok: {dok})")

# === DENOMINATOR SCAN ===
print("\n" + "=" * 70)
print("DENOMINATOR SCAN: What denominators make pion+ an integer?")
print("=" * 70)

# Check which {2,3,5,31}-smooth denominators make pion_target * d close to integer
smooth_denoms = []
for a2 in range(7):
    for a3 in range(5):
        for a5 in range(5):
            for a31 in range(3):
                d = (2**a2) * (3**a3) * (5**a5) * (31**a31)
                if 1 <= d <= 100000:
                    smooth_denoms.append(d)
smooth_denoms = sorted(set(smooth_denoms))

print(f"Testing {len(smooth_denoms)} smooth denominators...")
best_denom = []
for d in smooth_denoms:
    prod = pion_target_f * d
    nearest_int = round(prod)
    frac_part = abs(prod - nearest_int)
    if frac_part < 0.01:  # very close to integer
        candidate = Fraction(nearest_int, d)
        err = abs(float(candidate) - pion_target_f)
        ppm = err / pion_target_f * 1e6
        if ppm < 50:  # within 50 ppm
            best_denom.append((ppm, d, nearest_int, candidate))

best_denom.sort()
for ppm, d, num, frac in best_denom[:15]:
    denom_factors = prime_factors(d)
    num_factors = prime_factors(num) if num > 1 else {}
    print(f"  {num}/{d} = {float(frac):.10f} ({ppm:.2f} ppm) "
          f"denom={denom_factors}")

# === SCAN ALL TARGETS AGAINST SMOOTH FRACTIONS ===
print("\n" + "=" * 70)
print("ALL TARGETS: BEST SMOOTH-DENOMINATOR MATCHES")
print("=" * 70)

for name, target, unc, notes in targets:
    if target < 1e-3:  # skip tiny values like sin2theta
        continue
    best = []
    for d in smooth_denoms:
        if d > 10000:
            continue
        prod = target * d
        nearest_int = round(prod)
        frac_part = abs(prod - nearest_int)
        candidate = Fraction(nearest_int, d)
        err = abs(float(candidate) - target)
        ppm = err / target * 1e6 if target != 0 else 0
        if ppm < max(50, unc/target*1e6):
            best.append((ppm, d, nearest_int, candidate))
    best.sort()
    if best:
        ppm, d, num, frac = best[0]
        print(f"  {name:12s}: {num}/{d} = {float(frac):.8f} ({ppm:.2f} ppm) "
              f"denom={prime_factors(d)}")

# === COUPLING CONSTANT SEARCH ===
print("\n" + "=" * 70)
print("COUPLING CONSTANTS")
print("=" * 70)

# sin^2(theta_W)
sin2tw = Fraction(23122, 100000)  # 0.23122
candidates_sw = [
    ("n/Phi3(3)", Fraction(n, Phi3_3)),
    ("n/Phi3(3) + lam^2*Phi3", Fraction(n, Phi3_3) + lam**2 * Phi3_5),
    ("n/Phi3(3) + 1/(Phi3(3)*Phi3*p)", Fraction(n, Phi3_3) + Fraction(1, Phi3_3*Phi3_5*p)),
    ("n/(n*p-2)", Fraction(n, n*p - 2)),
    ("(n*p-1)/(n*p^2-n)", Fraction(n*p-1, n*p**2 - n)),
]
print("\nsin^2(theta_W) = 0.23122(4)")
for label, val in candidates_sw:
    err = abs(float(val) - 0.23122)
    ppm = err / 0.23122 * 1e6
    dok = factorize_denom(val)
    print(f"  {label:40s} = {float(val):.8f} ({ppm:.0f} ppm, denom ok: {dok})")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
