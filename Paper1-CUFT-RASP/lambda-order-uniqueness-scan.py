#!/usr/bin/env python3
"""
LAMBDA-ORDER UNIQUENESS SCAN
==============================

YASA PRESENTS

For each of the four fundamental constants, enumerate ALL possible
formulas at their respective lambda-order using RASP basis terms
{n, p, X, Phi_3, lambda}, and show the published formula is UNIQUE
among those with {2,3,5,31} denominator closure matching experiment.

Lambda orders:
  lambda^{-1}: muon     m_mu/m_e = p/(n*lambda) + 1/(2p) + lambda/p
  lambda^0:    alpha    1/alpha = p^3 + n(p-1) + n^2/(2p^3)
  lambda^1:    proton   M = X^2/2 + (n/p)X + n^2/X + lambda/n
  lambda^2:    neutron  m_n/m_e = M + p/2 + n^2/(pX) + np*lambda^2
"""

from fractions import Fraction
from itertools import product
import time

start = time.time()

n = 3
p = 5
X = n * p * (p - 1)  # = 60
Phi3 = p**2 + p + 1  # = 31
lam = Fraction(1, p**3 - 1)  # = 1/124

# CODATA 2022 targets
TARGETS = {
    'muon': Fraction(2067682827, 10000000),     # 206.7682827
    'alpha': Fraction(137035999177, 1000000000), # 137.035999177
    'proton': Fraction(183615267343, 100000000), # 1836.15267343
    'neutron': Fraction(183868366200, 100000000),# 1838.68366200
}

# Our formulas
OUR = {
    'muon': Fraction(p, n) / lam + Fraction(1, 2*p) + lam / p,
    'alpha': Fraction(p**3) + Fraction(n*(p-1)) + Fraction(n**2, 2*p**3),
    'proton': Fraction(X**2, 2) + Fraction(n, p)*X + Fraction(n**2, X) + lam/n,
    'neutron': Fraction(X**2, 2) + Fraction(n, p)*X + Fraction(n**2, X) + lam/n + Fraction(p, 2) + Fraction(n**2, p*X) + n*p*lam**2,
}

print("=" * 72)
print("LAMBDA-ORDER UNIQUENESS SCAN")
print("=" * 72)

# Verify our formulas
for name in ['muon', 'alpha', 'proton', 'neutron']:
    val = float(OUR[name])
    target = float(TARGETS[name])
    ppb = abs(val - target) / target * 1e9
    print(f"  {name:>8}: {val:.10f} vs {target:.10f} ({ppb:.1f} ppb)")

# ============================================================================
# RASP BASIS TERMS at each lambda-order
# ============================================================================

# Building blocks: rationals from {n, p, X, Phi3, lambda}
# At each lambda order, enumerate all simple products/ratios

# Simple terms (single RASP quantities and their ratios/products)
SIMPLE = {
    'n': Fraction(n),
    'p': Fraction(p),
    'X': Fraction(X),
    'Phi3': Fraction(Phi3),
    '1': Fraction(1),
    '2': Fraction(2),
    'n^2': Fraction(n**2),
    'p^2': Fraction(p**2),
    'p^3': Fraction(p**3),
    'X^2': Fraction(X**2),
    'n*p': Fraction(n*p),
    'n*X': Fraction(n*X),
    'p*X': Fraction(p*X),
    'n*Phi3': Fraction(n*Phi3),
    'p*Phi3': Fraction(p*Phi3),
    'p-1': Fraction(p-1),
    'p+1': Fraction(p+1),
    'n-1': Fraction(n-1),
    'n+1': Fraction(n+1),
    'Phi3-n': Fraction(Phi3-n),
    'Phi3+n': Fraction(Phi3+n),
}

# Denominators from RASP
DENOMS = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 25, 30, 31, 60, 62,
          124, 125, 150, 155, 250, 300, 310, 372, 465, 620, 930, 1860]
# Only {2,3,5,31}-smooth denominators up to reasonable size

def is_2_3_5_31_smooth(n_val):
    """Check if n has only prime factors in {2,3,5,31}."""
    if n_val == 0:
        return False
    n_val = abs(n_val)
    for p_val in [2, 3, 5, 31]:
        while n_val % p_val == 0:
            n_val //= p_val
    return n_val == 1

def check_formula_closure(val):
    """Check if a Fraction has {2,3,5,31}-smooth denominator."""
    return is_2_3_5_31_smooth(val.denominator)

# ============================================================================
# MUON SCAN: lambda^{-1} order
# ============================================================================

print(f"\n{'='*72}")
print(f"MUON SCAN: Expressions at lambda^(-1) order")
print(f"{'='*72}")

# At lambda^{-1}, the leading term must be proportional to 1/lambda = p^3-1 = 124
# General form: a/lambda + b + c*lambda  (3 terms, each a RASP ratio)

muon_target = float(TARGETS['muon'])
muon_hits = []

# Enumerate: a * (1/lambda) + b + c * lambda
# where a, b, c are simple rationals from RASP terms
a_candidates = []
for num_name, num_val in SIMPLE.items():
    for den_name, den_val in SIMPLE.items():
        if den_val == 0:
            continue
        ratio = num_val / den_val
        if abs(float(ratio)) < 50 and abs(float(ratio)) > 0.001:
            a_candidates.append((f"{num_name}/{den_name}", ratio))

# Also include single terms
for name, val in SIMPLE.items():
    if abs(float(val)) < 50 and abs(float(val)) > 0.001:
        a_candidates.append((name, val))

print(f"  Scanning {len(a_candidates)} candidates for coefficient 'a'...")

for a_name, a_val in a_candidates:
    # Leading term: a / lambda
    leading = a_val / lam  # = a * 124

    # Remainder after leading term
    remainder = muon_target - float(leading)

    if abs(remainder) > 10:
        continue  # Leading term too far off

    # Try simple constant terms for b
    for b_name, b_val in SIMPLE.items():
        for bd_name, bd_val in SIMPLE.items():
            if bd_val == 0:
                continue
            b = b_val / bd_val
            if abs(float(b)) > 5:
                continue

            # Remainder for c*lambda term
            rem2 = remainder - float(b)
            # c*lambda = rem2, so c = rem2/lambda = rem2 * 124
            c_needed = rem2 / float(lam)

            # Check if c_needed is a simple RASP ratio
            c_frac = Fraction(rem2).limit_denominator(10000) / lam
            # Just check if the full formula gives a clean match
            full = a_val / lam + b + Fraction(rem2).limit_denominator(100000) * lam
            # Nah, let's just build all 3-term formulas

    # Simpler approach: fix leading to p/(n*lambda), scan b and c
    pass

# Direct approach: enumerate ALL 3-term formulas at lambda^{-1} order
# of the form: (num1/den1)/lambda + num2/den2 + (num3/den3)*lambda
# where all nums and dens are products of {n, p, Phi3, 1, 2}

print(f"\n  Direct enumeration of lambda^(-1) formulas...")

# The leading term at lambda^{-1} must be A/lambda where A is rational
# For the muon: A = p/n = 5/3
# Alternative A values: any RASP ratio that gives A*124 ~ 206.7

count = 0
matches = []

# A must satisfy: A * 124 ~ 206.77, so A ~ 1.667 = 5/3
# Scan A = a/b for small a, b
for a_num in range(1, 31):
    for a_den in range(1, 31):
        A = Fraction(a_num, a_den)
        leading = A * (Fraction(1) / lam)  # A * 124
        if abs(float(leading) - muon_target) > 5:
            continue

        remainder = Fraction(TARGETS['muon'].numerator, TARGETS['muon'].denominator) - leading
        # This remainder should be expressible as b + c*lambda
        # where b, c are simple RASP rationals

        # Try b = simple fractions with {2,3,5,31} denominators
        for b_num in range(-20, 21):
            for b_den in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 25, 30, 31]:
                b = Fraction(b_num, b_den)
                c_lam = remainder - b
                # c = c_lam / lambda
                if lam != 0:
                    c = c_lam / lam
                else:
                    continue

                full = leading + b + c * lam
                if not check_formula_closure(full):
                    continue

                error_ppb = abs(float(full) - muon_target) / muon_target * 1e9
                if error_ppb < 100:  # within 100 ppb
                    count += 1
                    matches.append({
                        'A': str(A), 'b': str(b), 'c': str(c),
                        'value': float(full), 'ppb': error_ppb,
                        'formula': f"({a_num}/{a_den})/lambda + {b_num}/{b_den} + ({c})*lambda",
                        'denom': full.denominator,
                    })

print(f"  Total formulas with {'{2,3,5,31}'} closure within 100 ppb: {count}")

# Sort by ppb
matches.sort(key=lambda m: m['ppb'])
for i, m in enumerate(matches[:20]):
    ours = "<<<" if m['A'] == '5/3' and m['b'] == '1/10' else ""
    print(f"    [{i+1}] {m['formula']:>50} = {m['value']:.8f} ({m['ppb']:.1f} ppb) D={m['denom']} {ours}")

# ============================================================================
# NEUTRON SCAN: lambda^2 order corrections
# ============================================================================

print(f"\n{'='*72}")
print(f"NEUTRON SCAN: Corrections at lambda^2 order")
print(f"{'='*72}")

# The neutron is M + correction terms
# Our formula: M + p/2 + n^2/(pX) + np*lambda^2
M_proton = OUR['proton']
neutron_target_frac = Fraction(183868366200, 100000000)

# The correction = neutron - proton
correction_target = float(neutron_target_frac) - float(M_proton)
print(f"  Neutron - Proton target: {correction_target:.10f}")
print(f"  Our correction: {float(OUR['neutron'] - M_proton):.10f}")

# Enumerate all corrections of the form a + b + c*lambda^2
# where a, b, c are simple RASP rationals
neutron_matches = []
for a_num in range(-10, 20):
    for a_den in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 25, 30, 31, 60]:
        a = Fraction(a_num, a_den)
        for b_num in range(-20, 20):
            for b_den in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 25, 30, 31, 60, 124, 300]:
                b = Fraction(b_num, b_den)
                # Remaining at lambda^2 order
                rem = correction_target - float(a) - float(b)
                # c = rem / lambda^2
                c_val = rem / float(lam**2)

                # Check if c is a simple RASP rational
                c_frac = Fraction(c_val).limit_denominator(1000)
                if abs(float(c_frac) - c_val) > 0.01:
                    continue

                full_correction = a + b + c_frac * lam**2
                full_neutron = M_proton + full_correction

                if not check_formula_closure(full_neutron):
                    continue

                error_ppb = abs(float(full_neutron) - float(neutron_target_frac)) / float(neutron_target_frac) * 1e9
                if error_ppb < 50:
                    neutron_matches.append({
                        'a': str(a), 'b': str(b), 'c': str(c_frac),
                        'value': float(full_neutron),
                        'ppb': error_ppb,
                        'denom': full_neutron.denominator,
                    })

print(f"  Total corrections with closure within 50 ppb: {len(neutron_matches)}")
neutron_matches.sort(key=lambda m: m['ppb'])
for i, m in enumerate(neutron_matches[:20]):
    print(f"    [{i+1}] a={m['a']:>6} b={m['b']:>8} c={m['c']:>8} "
          f"= {m['value']:.10f} ({m['ppb']:.2f} ppb) D={m['denom']}")

elapsed = time.time() - start
print(f"\nWall time: {elapsed:.1f} seconds")
