#!/usr/bin/env python3
"""CUFT-RASP PPB HUNT
Find correction terms that close ppm-level candidates to ppb.
Strategy: the RESIDUAL is the signal. Express it as exact RASP rational.

The neutron pattern: M_n = M_p + p/2 + n^2/(pX) + np*lam^2
Each correction was found by matching the residual to RASP expressions.
Apply same methodology to tau, pion+, phi.
"""

from fractions import Fraction
from itertools import product as cartprod
import sys

# === RASP PARAMETERS (exact) ===
n, p = 3, 5
lam = Fraction(1, p**3 - 1)  # 1/124
Phi3 = p**2 + p + 1  # 31
Phi3_3 = 13
Phi3_2 = 7
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

# === CORRECTION TERM LIBRARY ===
# Generate ALL single rational terms from RASP parameters
# that could serve as corrections (range ~1e-8 to ~100)

def generate_corrections():
    """Generate labeled RASP correction terms."""
    terms = []

    # Basic atoms for numerator/denominator building
    num_atoms = [
        ("1", 1), ("2", 2), ("n", 3), ("p", 5), ("n^2", 9),
        ("p^2", 25), ("p^3", 125), ("Phi3", 31), ("Phi3_3", 13),
        ("Phi3_2", 7), ("p-1", 4), ("p+1", 6), ("p+2", 7),
        ("n+p", 8), ("X", 60), ("n*p", 15), ("n*(p-1)", 12),
    ]

    den_atoms = [
        ("1", 1), ("2", 2), ("n", 3), ("p", 5), ("n^2", 9),
        ("p^2", 25), ("p^3", 125), ("Phi3", 31), ("Phi3_3", 13),
        ("Phi3_2", 7), ("p-1", 4), ("p+1", 6), ("X", 60),
        ("n*p", 15), ("lam_inv", 124), ("lam_inv^2", 15376),
        ("p^2*Phi3", 775), ("n*Phi3", 93), ("p*Phi3", 155),
        ("n*p*Phi3", 465), ("2*p^3", 250), ("Phi3^2", 961),
        ("Phi3_3^2", 169), ("Phi3_2^2", 49), ("X^2", 3600),
        ("p*lam_inv", 620), ("n*lam_inv", 372), ("p^2*lam_inv", 3100),
        ("n*p*lam_inv", 1860), ("Phi3*lam_inv", 3844),
        ("2*Phi3", 62), ("2*n*p*Phi3", 930),
        ("n^2*Phi3", 279), ("p^3*Phi3", 3875),
        ("lam_inv^3", 1906624),
    ]

    seen = set()
    for n_label, n_val in num_atoms:
        for d_label, d_val in den_atoms:
            if d_val == 0:
                continue
            frac = Fraction(n_val, d_val)
            if frac not in seen and frac != 0:
                label = f"{n_label}/({d_label})" if d_val != 1 else n_label
                terms.append((label, frac))
                seen.add(frac)
                # Also negative
                if -frac not in seen:
                    terms.append((f"-{n_label}/({d_label})" if d_val != 1 else f"-{n_label}", -frac))
                    seen.add(-frac)

    # Add products of two atoms / single denominator
    for (n1_l, n1_v), (n2_l, n2_v) in [(a, b) for a in num_atoms for b in num_atoms]:
        for d_label, d_val in den_atoms:
            if d_val == 0:
                continue
            frac = Fraction(n1_v * n2_v, d_val)
            if frac not in seen and frac != 0 and abs(float(frac)) < 1000:
                label = f"{n1_l}*{n2_l}/({d_label})"
                terms.append((label, frac))
                seen.add(frac)

    # Lambda powers
    for k in range(1, 5):
        val = lam**k
        if val not in seen:
            terms.append((f"lam^{k}", val))
            seen.add(val)
        val2 = (-1)**k * lam**k
        if val2 not in seen:
            terms.append((f"(-lam)^{k}", val2))
            seen.add(val2)

    # Products with lambda
    for n_label, n_val in num_atoms:
        for k in range(1, 4):
            val = Fraction(n_val) * lam**k
            if val not in seen and val != 0:
                terms.append((f"{n_label}*lam^{k}", val))
                seen.add(val)
            val2 = -Fraction(n_val) * lam**k
            if val2 not in seen:
                terms.append((f"-{n_label}*lam^{k}", val2))
                seen.add(val2)

    # Products of two atoms times lambda
    key_pairs = [
        ("n*p", 15), ("n^2", 9), ("p^2", 25), ("n*Phi3", 93),
        ("p*Phi3", 155), ("Phi3_2*Phi3_3", 91), ("n*Phi3_2", 21),
        ("n*Phi3_3", 39), ("p*Phi3_2", 35), ("p*Phi3_3", 65),
        ("Phi3*Phi3_3", 403), ("Phi3*Phi3_2", 217),
    ]
    for label, val in key_pairs:
        for k in range(1, 3):
            frac = Fraction(val) * lam**k
            if frac not in seen:
                terms.append((f"{label}*lam^{k}", frac))
                seen.add(frac)
            frac2 = -frac
            if frac2 not in seen:
                terms.append((f"-{label}*lam^{k}", frac2))
                seen.add(frac2)

    return terms

corrections = generate_corrections()
print(f"Generated {len(corrections)} correction terms")

# Filter to reasonable magnitude range for corrections
corrections_small = [(l, v) for l, v in corrections if 1e-10 < abs(float(v)) < 100]
corrections_tiny = [(l, v) for l, v in corrections if 1e-10 < abs(float(v)) < 1]
print(f"Small corrections (< 100): {len(corrections_small)}")
print(f"Tiny corrections (< 1): {len(corrections_tiny)}")

# === TARGET RESIDUALS ===
# For each candidate, compute the EXACT residual from experimental value

# Experimental values (CODATA 2022 / PDG 2024)
# Using the most precise available values
exp = {
    'tau_codata': Fraction(347723, 100),     # 3477.23 ± 0.23
    'tau_hflav':  Fraction(347742, 100),     # 3477.42 ± 0.18
    'pion_pdg':   Fraction(27313268, 100000), # 273.13268 (from 139.57039/0.51099895)
    'phi_pdg':    Fraction(199504, 100),      # 1995.04 (from 1019.461/0.51099895)
}

# Current formulas
tau_cipher = Fraction(Phi3 - n) * Fraction(p**3 - 1) + Fraction(p) + Fraction(1, p - 1)
tau_greedy = Fraction(X**2) - Fraction(p**3 - 1) + Fraction(Phi3, p**2)

pion_4t = (Fraction(n * Phi3_2 * Phi3_3)
           + Fraction(p - 1, Phi3)
           + Fraction(p**2 - 2, 2 * p**2 * (p**3 - 1)))

phi_corr = Fraction(p) * (Fraction(Phi3 * Phi3_3) - Fraction(p - 1) + lam)

print("\n" + "=" * 70)
print("CURRENT RESIDUALS")
print("=" * 70)

# More precise pion ratio
pion_mev = 139.57039  # ± 0.00018
elec_mev = 0.51099895000
pion_precise = pion_mev / elec_mev
phi_mev = 1019.461  # ± 0.016
phi_precise = phi_mev / elec_mev

residuals = {
    'tau_cipher': float(tau_cipher) - 3477.23,
    'tau_greedy': float(tau_greedy) - 3477.23,
    'pion_4t': float(pion_4t) - pion_precise,
    'phi_corr': float(phi_corr) - phi_precise,
}

for name, r in residuals.items():
    print(f"  {name:15s}: residual = {r:+.10f}")

# === PPB HUNT: Find correction terms that match residuals ===
print("\n" + "=" * 70)
print("PPB HUNT: MATCHING CORRECTIONS TO RESIDUALS")
print("=" * 70)

def hunt_corrections(base_label, base_formula, target_float, target_unc, max_terms=3):
    """Find correction terms that close residual to ppb."""
    print(f"\n--- {base_label} ---")
    print(f"  Base: {float(base_formula):.12f}")
    print(f"  Target: {target_float:.12f} ± {target_unc:.2e}")

    remaining = target_float - float(base_formula)
    print(f"  Residual to close: {remaining:+.10e}")

    if abs(remaining) < target_unc:
        print(f"  ALREADY within uncertainty!")
        return

    # 1-term corrections
    print(f"\n  Best 1-term corrections:")
    best_1 = []
    for label, val in corrections_small:
        r = abs(remaining - float(val))
        if r < abs(remaining) * 0.5:  # must improve by at least 50%
            ppm = r / abs(target_float) * 1e6
            best_1.append((r, ppm, label, val))
    best_1.sort()

    for r, ppm, label, val in best_1[:10]:
        total = base_formula + val
        dok = denom_clean(total)
        new_residual = target_float - float(total)
        print(f"    + {label:40s} = {float(val):+.10e} -> residual {new_residual:+.6e} ({ppm:.3f} ppm) denom_ok={dok}")

    # 2-term corrections (using tiny terms only for speed)
    if abs(remaining) > target_unc:
        print(f"\n  Best 2-term corrections:")
        best_2 = []
        # First find the best 1-term, then search for 2nd term on residual
        if best_1:
            for _, _, l1, v1 in best_1[:20]:  # top 20 first terms
                r1 = remaining - float(v1)
                for l2, v2 in corrections_tiny:
                    r2 = abs(r1 - float(v2))
                    if r2 < abs(remaining) * 0.01:  # 100x improvement
                        ppm = r2 / abs(target_float) * 1e6
                        best_2.append((r2, ppm, l1, v1, l2, v2))
        best_2.sort()

        for r, ppm, l1, v1, l2, v2 in best_2[:10]:
            total = base_formula + v1 + v2
            dok = denom_clean(total)
            new_residual = target_float - float(total)
            ppb = abs(new_residual) / abs(target_float) * 1e9
            print(f"    + {l1:30s} + {l2:30s} -> residual {new_residual:+.6e} ({ppb:.1f} ppb) denom_ok={dok}")

# TAU (experimental uncertainty: 66 ppm = 0.23 m_e)
# Both formulas already within 0.1sigma, but can we get ppb?
# The tau experimental value is only known to 66 ppm, so ppb
# would be 1000x MORE precise than measurement. Still, find the formula.
hunt_corrections("TAU (CIPHER)", tau_cipher, 3477.23, 0.23)
hunt_corrections("TAU (greedy)", tau_greedy, 3477.23, 0.23)

# PION+ (experimental uncertainty: 1.3 ppm = 0.000361 m_e)
hunt_corrections("PION+ (4-term)", pion_4t, pion_precise, 0.000361)

# PHI (experimental uncertainty: 15.7 ppm = 0.0313 m_e)
hunt_corrections("PHI (corrected)", phi_corr, phi_precise, 0.0313)

# === ALTERNATIVE APPROACH: Direct rational approximation ===
print("\n" + "=" * 70)
print("DIRECT RATIONAL HUNT: What exact fraction matches each target?")
print("=" * 70)

# For pion+, which has the tightest constraint:
# Find fractions with {2,3,5,31}-smooth denominators that match to ppb
print(f"\nPION+ = {pion_precise:.12f}")
print(f"Hunting fractions with smooth denominators...")

# Generate smooth denominators up to 10^8
smooth_denoms = set()
for a2 in range(25):
    for a3 in range(16):
        for a5 in range(11):
            for a31 in range(6):
                d = (2**a2) * (3**a3) * (5**a5) * (31**a31)
                if d <= 10**8:
                    smooth_denoms.add(d)

smooth_denoms = sorted(smooth_denoms)
print(f"Testing {len(smooth_denoms)} smooth denominators up to 10^8...")

best_pion = []
for d in smooth_denoms:
    prod = pion_precise * d
    nearest = round(prod)
    frac_part = abs(prod - nearest)
    if frac_part < 0.001:  # very close to integer
        candidate = Fraction(nearest, d)
        err = abs(float(candidate) - pion_precise)
        ppb = err / pion_precise * 1e9
        if ppb < 100:  # sub-100 ppb
            best_pion.append((ppb, d, nearest, candidate))

best_pion.sort()
print(f"\nSub-100 ppb matches for pion+:")
for ppb, d, num, frac in best_pion[:20]:
    df = prime_factors(d)
    nf = prime_factors(num)
    print(f"  {num}/{d} = {float(frac):.12f} ({ppb:.2f} ppb) denom={df}")

# Same for phi
print(f"\nPHI = {phi_precise:.12f}")
best_phi = []
for d in smooth_denoms:
    if d > 10**7:
        continue
    prod = phi_precise * d
    nearest = round(prod)
    frac_part = abs(prod - nearest)
    if frac_part < 0.01:
        candidate = Fraction(nearest, d)
        err = abs(float(candidate) - phi_precise)
        ppb = err / phi_precise * 1e9
        if ppb < 1000:  # sub-1000 ppb for phi (less precise exp)
            best_phi.append((ppb, d, nearest, candidate))

best_phi.sort()
print(f"Sub-1000 ppb matches for phi:")
for ppb, d, num, frac in best_phi[:20]:
    df = prime_factors(d)
    print(f"  {num}/{d} = {float(frac):.12f} ({ppb:.1f} ppb) denom={df}")

# === STRUCTURAL DECOMPOSITION ===
# For any promising fraction, try to decompose numerator into RASP terms
print("\n" + "=" * 70)
print("STRUCTURAL DECOMPOSITION OF BEST MATCHES")
print("=" * 70)

def decompose_numerator(num, denom):
    """Try to express numerator as sum of products of RASP atoms."""
    # Key RASP values that could appear in numerator
    rasp_vals = {
        'n': 3, 'p': 5, 'n^2': 9, 'p^2': 25, 'p^3': 125,
        'Phi3': 31, 'Phi3_3': 13, 'Phi3_2': 7,
        'p-1': 4, 'X': 60, 'n*p': 15, '1/lam': 124,
        'Phi3-n': 28, 'n*Phi3_2': 21, 'n*Phi3_3': 39,
        'p*Phi3_2': 35, 'p*Phi3_3': 65,
        'Phi3*Phi3_3': 403, 'Phi3*Phi3_2': 217,
        'Phi3_2*Phi3_3': 91, 'n*Phi3_2*Phi3_3': 273,
        'X^2': 3600, 'X*p': 300, 'X*n': 180,
    }

    print(f"  Decomposing {num} (denom={denom}):")
    # Try: num = a * denom_factor + remainder
    for label, val in sorted(rasp_vals.items(), key=lambda x: -x[1]):
        if num > val and val > 0:
            q, r = divmod(num, val)
            if r == 0:
                print(f"    {num} = {q} * {label}({val})")
            elif abs(r) < 100:
                print(f"    {num} = {q} * {label}({val}) + {r}")

if best_pion:
    ppb, d, num, frac = best_pion[0]
    decompose_numerator(num, d)

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
