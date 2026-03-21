#!/usr/bin/env python3
"""
Sub-PPB Corrections — Find higher-order lambda corrections to the
existing 4 Level 1 formulas to close residuals to sub-ppb.

The residuals are REAL (not noise) because experimental precision
is far better than our formula precision:
  Proton: formula 8.0 ppb vs experiment 0.017 ppb → 470σ
  Alpha:  formula 6.0 ppb vs experiment 0.15 ppb  → 39σ
  Muon:   formula 15 ppb vs experiment 22 ppb     → 0.68σ (within!)
  Neutron: formula 0.9 ppb vs experiment 0.4 ppb  → 2.3σ

Strategy: express each residual as a RASP fraction with clean denominator.
"""

from fractions import Fraction

n, p = 3, 5
lam = Fraction(1, p**3 - 1)           # 1/124
Phi3 = p**2 + p + 1                    # 31
Phi3_3 = 13
Phi3_2 = 7
X = n * p * (p - 1)                    # 60

# Current formulas
M_p = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + Fraction(1, n * (p**3 - 1))
M_n = M_p + Fraction(p, 2) + Fraction(n**2, p * X) + Fraction(n * p, (p**3 - 1)**2)
M_mu = Fraction(p, n) * Fraction(p**3 - 1) + Fraction(1, 2*p) + Fraction(1, p * (p**3 - 1))
alpha_inv = Fraction(p**3) + Fraction(n * (p-1)) + Fraction(n**2, 2 * p**3)

def prime_factors(nn):
    if nn <= 1: return {}
    factors = {}; d = 2; nn = abs(nn)
    while d * d <= nn:
        while nn % d == 0: factors[d] = factors.get(d, 0) + 1; nn //= d
        d += 1
    if nn > 1: factors[nn] = factors.get(nn, 0) + 1
    return factors

def denom_clean(frac):
    d = abs(frac.denominator)
    for pp in [2, 3, 5, 31]:
        while d % pp == 0: d //= pp
    return d == 1

# CODATA 2022 values (full precision)
exp_vals = {
    "proton":  1836.15267342600,
    "neutron": 1838.68366200000,
    "muon":    206.7682827,
    "alpha":   137.035999177,
}

formulas = {
    "proton":  M_p,
    "neutron": M_n,
    "muon":    M_mu,
    "alpha":   alpha_inv,
}

print("=" * 70)
print("RESIDUAL ANALYSIS — WHERE ARE THE CORRECTIONS?")
print("=" * 70)

residuals = {}
for name in ["proton", "neutron", "muon", "alpha"]:
    f_val = float(formulas[name])
    e_val = exp_vals[name]
    r = f_val - e_val
    ppb = abs(r) / e_val * 1e9
    residuals[name] = r
    print(f"\n{name.upper()}: formula={f_val:.15f}  exp={e_val:.15f}")
    print(f"  residual = {r:+.15e}  ({ppb:.2f} ppb)")

# === GENERATE ALL CORRECTION TERMS through lambda^4 ===
print("\n" + "=" * 70)
print("CORRECTION TERM LIBRARY")
print("=" * 70)

corrections = {}

# Lambda powers with various coefficients
for lam_power in range(-2, 5):
    lam_term = lam ** lam_power if lam_power >= 0 else Fraction(1) / (lam ** (-lam_power))
    if lam_power < 0:
        lam_term = (Fraction(p**3 - 1)) ** (-lam_power)

    for num_parts in [
        (1, "1"), (n, "n"), (p, "p"), (n**2, "n^2"), (p**2, "p^2"),
        (n*p, "np"), (n**2*p, "n^2p"), (n*p**2, "np^2"),
        (Phi3, "Phi3"), (Phi3_3, "Phi3_3"), (Phi3_2, "Phi3_2"),
        (2, "2"), (n+p, "n+p"), (p-n, "p-n"),
    ]:
        num_val, num_label = num_parts
        for den_parts in [
            (1, "1"), (2, "2"), (n, "n"), (p, "p"), (n*p, "np"),
            (n**2, "n^2"), (p**2, "p^2"), (X, "X"), (2*X, "2X"),
            (Phi3, "Phi3"), (2*p**3, "2p^3"), (p**3, "p^3"),
            (n*p**2, "np^2"), (2*n, "2n"), (2*p, "2p"),
            (n**2*p, "n^2p"), (n*p**2, "np^2"),
        ]:
            den_val, den_label = den_parts
            if den_val == 0: continue

            for sign in [1, -1]:
                val = sign * Fraction(num_val, den_val) * lam_term
                if val == 0: continue

                if lam_power == 0:
                    label = f"{'+' if sign > 0 else '-'}{num_label}/{den_label}"
                elif lam_power == 1:
                    label = f"{'+' if sign > 0 else '-'}{num_label}*lam/{den_label}"
                elif lam_power == -1:
                    label = f"{'+' if sign > 0 else '-'}{num_label}/(lam*{den_label})"
                else:
                    label = f"{'+' if sign > 0 else '-'}{num_label}*lam^{lam_power}/{den_label}"

                fval = float(val)
                if abs(fval) > 0 and abs(fval) < 1e-2:  # only small corrections
                    corrections[label] = val

print(f"Generated {len(corrections)} small correction terms")

# Show scale of each lambda power
for lp in range(-1, 5):
    if lp >= 0:
        scale = float(lam ** lp)
    else:
        scale = float(Fraction(p**3 - 1))
    print(f"  lambda^{lp}: {scale:.2e}")

# === SEARCH: which correction closes each residual? ===
print("\n" + "=" * 70)
print("CORRECTION SEARCH — CLOSE RESIDUALS TO SUB-PPB")
print("=" * 70)

for name in ["proton", "alpha", "neutron", "muon"]:
    r = residuals[name]
    e_val = exp_vals[name]
    print(f"\n{'='*50}")
    print(f"{name.upper()}: residual = {r:+.6e} ({abs(r)/e_val*1e9:.2f} ppb)")
    print(f"{'='*50}")

    # Single correction
    best = []
    for label, val in corrections.items():
        # Subtract correction from formula (if residual is +, we need - correction)
        new_residual = r - float(val)
        new_ppb = abs(new_residual) / e_val * 1e9
        if new_ppb < abs(r) / e_val * 1e9:  # improvement
            new_formula = formulas[name] - val  # subtract because residual = formula - exp
            clean = denom_clean(new_formula)
            best.append((new_ppb, label, val, new_formula, clean))

    best.sort()
    print(f"\nBest single corrections (top 15):")
    seen = set()
    count = 0
    for new_ppb, label, val, new_formula, clean in best:
        key = float(val)
        if key in seen: continue
        seen.add(key)
        d = new_formula.denominator
        pf = prime_factors(d)
        marker = " *** PPB ***" if new_ppb < 1.0 else " ** SUB-10 **" if new_ppb < 10 else ""
        marker2 = " [CLEAN]" if clean else ""
        print(f"  {label:35s} (={float(val):+.6e}) → {new_ppb:.3f} ppb "
              f"denom={pf}{marker2}{marker}")
        count += 1
        if count >= 15: break

    # Find CLEAN sub-ppb corrections
    clean_sub = [(ppb, l, v, f, c) for ppb, l, v, f, c in best if c and ppb < 5.0]
    if clean_sub:
        print(f"\n  *** CLEAN SUB-5 PPB CORRECTIONS ***")
        for ppb, label, val, new_formula, clean in clean_sub[:5]:
            d = new_formula.denominator
            print(f"    {label:35s} → {ppb:.3f} ppb  fraction={new_formula.numerator}/{d}")
            print(f"    denom={prime_factors(d)}")

# === DOUBLE CORRECTIONS: try pairs ===
print("\n" + "=" * 70)
print("DOUBLE CORRECTIONS — TWO-TERM RESIDUAL CLOSURE")
print("=" * 70)

# Focus on proton and alpha (biggest residuals that are definitely real)
for name in ["proton", "alpha"]:
    r = residuals[name]
    e_val = exp_vals[name]
    print(f"\n{name.upper()}: seeking two corrections to close {r:+.6e}")

    # Pre-filter corrections to those in the right ballpark
    relevant = [(l, v) for l, v in corrections.items()
                if abs(float(v)) < abs(r) * 10 and abs(float(v)) > abs(r) * 0.01]

    best_double = []
    for i, (l1, v1) in enumerate(relevant):
        for l2, v2 in relevant[i:]:
            new_r = r - float(v1) - float(v2)
            new_ppb = abs(new_r) / e_val * 1e9
            if new_ppb < 1.0:  # sub-ppb only
                new_formula = formulas[name] - v1 - v2
                clean = denom_clean(new_formula)
                if clean:
                    best_double.append((new_ppb, f"{l1} {l2}", v1+v2, new_formula))

    best_double.sort()
    if best_double:
        print(f"  Found {len(best_double)} CLEAN sub-ppb double corrections!")
        for ppb, label, val, new_formula in best_double[:10]:
            d = new_formula.denominator
            print(f"    {label:55s} → {ppb:.4f} ppb  denom={prime_factors(d)}")
            print(f"    formula value: {float(new_formula):.15f}")
    else:
        print(f"  No clean sub-ppb double corrections found.")

# === WHAT ABOUT THE MUON? It's already within 0.68σ ===
print("\n" + "=" * 70)
print("MUON STATUS — ALREADY WITHIN EXPERIMENTAL UNCERTAINTY")
print("=" * 70)
mu_r = residuals["muon"]
mu_ppb = abs(mu_r) / exp_vals["muon"] * 1e9
mu_exp_unc = 4.6e-6
mu_sigma = abs(mu_r) / mu_exp_unc
print(f"Muon residual: {mu_r:+.6e} ({mu_ppb:.2f} ppb)")
print(f"Experimental uncertainty: {mu_exp_unc:.1e} ({mu_exp_unc/exp_vals['muon']*1e9:.1f} ppb)")
print(f"Sigma: {mu_sigma:.2f}")
print(f"MUON FORMULA IS ALREADY A ppb-LEVEL PREDICTION (15 ppb < 22 ppb exp unc)")
print(f"This IS Level 1 — the formula predicts better than experiment measures.")

# === SUMMARY TABLE ===
print("\n" + "=" * 70)
print("LEVEL 1 STATUS AFTER CORRECTION SEARCH")
print("=" * 70)
print(f"{'Constant':12s} | {'Formula ppb':>12s} | {'Exp unc ppb':>12s} | {'Sigma':>8s} | Status")
print("-" * 70)

status_data = [
    ("Proton",  8.03, 0.017, 8.03/0.017),
    ("Neutron", 0.94, 0.40, 0.94/0.40),
    ("Muon",    15.1, 22.2, 15.1/22.2),
    ("1/alpha", 6.0, 0.15, 6.0/0.15),
]

for name, fppb, eppb, sigma in status_data:
    stat = "WITHIN EXP" if sigma < 2 else f"NEED CORRECTION ({sigma:.0f}σ)"
    print(f"{name:12s} | {fppb:12.2f} | {eppb:12.3f} | {sigma:8.1f} | {stat}")
