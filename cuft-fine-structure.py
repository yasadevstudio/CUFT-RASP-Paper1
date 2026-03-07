#!/usr/bin/env python3
"""
CUFT-RASP DIRECTION 3: THE FINE STRUCTURE CONSTANT
=====================================================
YASA PRESENTS — 2026-02-24

α ≈ 1/137.036 — the most famous unexplained dimensionless constant.
Is it hiding in the RASP framework?
"""

import numpy as np
from scipy.optimize import brentq
from fractions import Fraction
from itertools import product as iprod

# ═══════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════

alpha = 1/137.035999177  # CODATA 2022
inv_alpha = 137.035999177

# RASP constants
n, p = 3, 5
G = 25
L = Fraction(1, 124)
X = 60
kappa = Fraction(1, 5)
Phi3 = p**2 + p + 1  # = 31
M = Fraction(853811, 465)

print("="*70)
print("CUFT-RASP DIRECTION 3: THE FINE STRUCTURE CONSTANT")
print("="*70)

print(f"\nα = {alpha:.15f}")
print(f"1/α = {inv_alpha:.10f}")
print(f"\nRASP constants: n={n}, p={p}, Γ={G}, λ=1/{float(1/float(L)):.0f}, X={X}, κ=1/{p}")
print(f"Φ₃(p) = {Phi3}, M = {M} = {float(M):.6f}")

# ═══════════════════════════════════════════════════════════════════
# TEST 1: SIMPLE COMBINATIONS OF RASP CONSTANTS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TEST 1: IS 1/α A SIMPLE FUNCTION OF (n, p)?")
print("="*70)

# Build a dictionary of simple expressions
exprs = {}

# Single constants
for name, val in [('n', 3), ('p', 5), ('G', 25), ('X', 60),
                  ('Phi3', 31), ('p³-1', 124), ('M', float(M))]:
    exprs[name] = val

# Products and powers
for a_name, a_val in [('n', 3), ('p', 5)]:
    for b_name, b_val in [('n', 3), ('p', 5), ('Phi3', 31)]:
        exprs[f'{a_name}*{b_name}'] = a_val * b_val
        exprs[f'{a_name}*{b_name}²'] = a_val * b_val**2
        exprs[f'{a_name}²*{b_name}'] = a_val**2 * b_val
        if a_val != b_val:
            exprs[f'{a_name}^{b_name}'] = a_val**b_val

# More complex
exprs.update({
    'n*p*Phi3': n*p*Phi3,
    'p³': p**3,
    'p³+p': p**3+p,
    'p³+p²': p**3+p**2,
    'n*p³': n*p**3,
    'n*(p³-1)': n*(p**3-1),
    'X+p³': X+p**3,
    '2*X+p': 2*X+p,
    '2*X+n*p': 2*X+n*p,
    'n*p*(p²+1)': n*p*(p**2+1),
    'n*(p²+p+1)': n*(p**2+p+1),
    'p*(p²+p+1)': p*(p**2+p+1),
    '(p+1)*(p²+1)': (p+1)*(p**2+1),
    'Phi3+p³': Phi3+p**3,
    '4*Phi3+n': 4*Phi3+n,
    'n*Phi3+p+1': n*Phi3+p+1,
    'X²/M': X**2/float(M),
    'M/X': float(M)/X,
    'M/(n*X)': float(M)/(n*X),
    'p*Phi3': p*Phi3,
    'n*Phi3': n*Phi3,
    '(n+p)*Phi3': (n+p)*Phi3,
    '2*p*Phi3-n': 2*p*Phi3-n,
    '(p²+p²*n+p*n)': p**2+p**2*n+p*n,
    'n*p*(p+1)': n*p*(p+1),
    'n*(p+1)²': n*(p+1)**2,
    'p*(p+1)²': p*(p+1)**2,
    'n*p²+n*p+n': n*p**2+n*p+n,
    '(n+p)*(n*p+1)': (n+p)*(n*p+1),
    'n⁴+p': n**4+p,
    'n⁴+p²': n**4+p**2,
    'n⁵-p³': n**5-p**3,
    'p⁴-p²+p': p**4-p**2+p,
    '(p-1)*Phi3': (p-1)*Phi3,
})

# Also fractional expressions
frac_exprs = {}
for name1, val1 in exprs.items():
    if val1 == 0: continue
    for name2, val2 in [('n', 3), ('p', 5), ('n+p', 8), ('p-1', 4),
                         ('n+2', 5), ('n-2', 1), ('2', 2), ('3', 3),
                         ('pi', np.pi), ('e', np.e), ('sqrt2', np.sqrt(2))]:
        if val2 == 0: continue
        frac_exprs[f'{name1}/{name2}'] = val1/val2
        frac_exprs[f'{name1}*{name2}'] = val1*val2

# Test all against 1/α
print(f"\nSearching {len(exprs) + len(frac_exprs)} expressions for 1/α = {inv_alpha:.6f}...")
print(f"\n{'Expression':>35s}  {'Value':>14s}  {'Error %':>10s}")
print("-"*65)

hits = []
for name, val in {**exprs, **frac_exprs}.items():
    if val <= 0 or val > 1e6: continue
    err = abs(val - inv_alpha) / inv_alpha * 100
    if err < 5.0:
        hits.append((name, val, err))

hits.sort(key=lambda x: x[2])
for name, val, err in hits[:20]:
    print(f"{name:>35s}  {val:>14.6f}  {err:>10.4f}%")

if not hits:
    print("  No expression within 5% of 1/α found.")

# ═══════════════════════════════════════════════════════════════════
# TEST 2: α AS A FUNCTION OF RASP DYNAMICAL QUANTITIES
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TEST 2: α FROM DYNAMICAL QUANTITIES")
print("="*70)

# What about α in terms of the recursion's dynamical data?
def f(x): return G * np.tanh(x)**n - float(L) * x
def fp(x):
    t = np.tanh(x)
    return n * G * t**(n-1) * (1-t**2) - float(L)

def g(x): return f(x) - x
xu = brentq(g, 0.001, 2.0)
xs = brentq(g, 20, 26)

print(f"x_u = {xu:.12f}")
print(f"x_s = {xs:.12f}")
print(f"f'(x_u) = {fp(xu):.12f}")
print(f"f'(x_s) = {fp(xs):.12f}")

# Build dynamical atoms
dyn = {
    'xu': xu, 'xs': xs,
    'fpu': fp(xu), 'fps': fp(xs),
    'xu*xs': xu*xs,
    'xs/xu': xs/xu,
    'xu²': xu**2,
    'xs²': xs**2,
    'ln(xs)': np.log(xs),
    'ln(xu)': np.log(xu),
    'ln(xs/xu)': np.log(xs/xu),
    'xs-xu': xs-xu,
    '|fpu|^n': abs(fp(xu))**n,
}

print(f"\n{'Expression':>25s}  {'Value':>14s}  {'vs 1/α':>14s}  {'Error %':>10s}")
print("-"*70)

for dname, dval in dyn.items():
    for cname, cval in [('1', 1), ('n', 3), ('p', 5), ('n*p', 15),
                         ('X', 60), ('Phi3', 31), ('p²', 25)]:
        for op_name, op in [('*', lambda a,b: a*b), ('/', lambda a,b: a/b if b else 0)]:
            val = op(dval, cval)
            if val <= 0 or val > 1e6: continue
            err = abs(val - inv_alpha) / inv_alpha * 100
            if err < 5:
                print(f"  {dname}{op_name}{cname}:  {val:>14.6f}  {inv_alpha:>14.6f}  {err:>10.4f}%")

# ═══════════════════════════════════════════════════════════════════
# TEST 3: RECURSION THAT PRODUCES α
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TEST 3: A SEPARATE RECURSION FOR α?")
print("="*70)

# What if there's a recursion f(x) = Γ'·tanh^m(x) - λ'·x
# where m ≠ 3 and the mass formula gives 1/α = 137.036?

# For each m, find which p gives a mass formula ≈ 137.036
# Using M(m,q) = X²/2 + (m/q)*X + m²/X + 1/(m*(q³-1))
# where X = m*q*(q-1)

print("\nScanning recursions f(x) = Γ·tanh^m(x) - λ·x for M ≈ 137.036:")
print(f"{'m':>4s}  {'q':>4s}  {'X':>6s}  {'M':>14s}  {'Error vs 1/α':>14s}")
print("-"*50)

for m in range(2, 20):
    for q in range(2, 50):
        X_try = m * q * (q - 1)
        L_try = 1 / (q**3 - 1)
        M_try = X_try**2/2 + m/q * X_try + m**2/X_try + L_try/m
        err = abs(M_try - inv_alpha) / inv_alpha * 100
        if err < 1:
            print(f"{m:>4d}  {q:>4d}  {X_try:>6d}  {M_try:>14.6f}  {err:>14.4f}%")

# Also check: is 1/α a mass formula with different structure?
# What about just the dominant term: X²/2 ≈ 137?
# X²/2 = 137 → X ≈ 16.55 → not an integer product
# What about m/q * X = 137? For X=60: 137/60 = 2.28... not n/p for integer n,p

print("\n--- Can 137.036 be expressed as a RASP mass formula? ---")
print(f"  X²/2 = 137 → X = {np.sqrt(274):.4f} (not integer factored)")
print(f"  For small X (X=12): 72 + 36 + 3 + 0.024 = 111.024 [that's M(6,2)]")
print(f"  For X=14: 98 + ... nope")
print(f"  For X=16: 128 + ... already > 137")

# Check: does 137 factor through n*p*(p-1)?
print(f"\n  137 is PRIME. Cannot be factored as n*p*(p-1).")
print(f"  So 1/α cannot be a RASP mass formula with the standard X = n*p*(p-1) structure.")

# ═══════════════════════════════════════════════════════════════════
# TEST 4: α AS RATIO OR FUNCTION OF M
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TEST 4: RELATIONSHIP BETWEEN α AND M")
print("="*70)

M_f = float(M)
print(f"M = {M_f:.6f}")
print(f"1/α = {inv_alpha:.6f}")
print(f"M/α = M * 137.036 = {M_f * inv_alpha:.4f}")
print(f"M*α = M / 137.036 = {M_f * alpha:.8f}")
print(f"M*α = {M_f * alpha:.8f} ≈ {M_f * alpha:.4f}")

# Is M*α close to anything?
Ma = M_f * alpha
print(f"\nM*α = {Ma:.8f}")
print(f"  ≈ 13.4 ≈ n*p - 1/p? = {n*p - 1/p}")
print(f"  ≈ X/p? = {X/p} = 12")
print(f"  ≈ n*(p-1)? = {n*(p-1)} = 12")

# M / (1/α) = M * α
# What about √(M*α)?
print(f"\n√(M*α) = {np.sqrt(Ma):.8f}")
print(f"  ≈ √13.4 ≈ {np.sqrt(13.4):.4f}")

# M / 1/α
print(f"\nM / (1/α) = M*α = {Ma:.8f}")
print(f"log(M)/log(1/α) = {np.log(M_f)/np.log(inv_alpha):.8f}")
print(f"  ≈ {np.log(M_f)/np.log(inv_alpha):.4f} (not a simple ratio)")

# The famous: α * M_proton/M_electron ≈ 13.4
# This is known — it's roughly the strong coupling constant at low energy
print(f"\nα * μ(proton/electron) = α * 1836.153 = {alpha * 1836.153:.6f}")
print(f"  This is known as approximately equal to the QCD coupling α_s at ~1 GeV")
print(f"  α_s(1 GeV) ≈ 0.5, our value = {alpha * 1836.153:.4f}")
print(f"  Not the same. α*M ≈ 13.4, α_s ≈ 0.5.")

# What about n/p / α?
print(f"\n(n/p) / α = {(n/p) / alpha:.6f}")
print(f"  = {n/p} * 137.036 = {n/p * inv_alpha:.4f}")
print(f"  = 82.2 ≈ p⁴/p - p² + 1? = {p**4/p - p**2 + 1}")

# ═══════════════════════════════════════════════════════════════════
# TEST 5: SPECIFIC NUMERICAL INVESTIGATIONS
# ═══════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("TEST 5: NUMERICAL ARCHAEOLOGY")
print("="*70)

# 137 = prime. Known properties:
# 137 = 2^7 + 2^3 + 2^0 = 128 + 8 + 1
# 137 is a Pythagorean prime (137 = 4*34 + 1)
# In the Diophantine: if (n-2)(p-1) = 136 = 8*17 = 2³*17

# What Diophantine would give p near 137?
# (n-2)(p-1) = 4 gives p=5 for n=3
# What if we generalize: (n-2)(p-1) = C for other C?
print("Generalized Diophantine (n-2)(p-1) = C:")
print("If p = 137, what C and n?")
for n_try in range(3, 20):
    C = (n_try - 2) * (137 - 1)
    print(f"  n={n_try}: C = {C} = ({n_try}-2)*136")

# Is there a recursion where p itself IS 137?
# f(x) = 137²·tanh^n(x) - λ·x, λ = 1/(137³-1)
print(f"\nIf p = 137:")
print(f"  Γ = p² = {137**2}")
print(f"  λ = 1/(p³-1) = 1/{137**3-1} = {1/(137**3-1):.12f}")
print(f"  For n=3: X = 3*137*136 = {3*137*136}")
print(f"  M = X²/2 + ... = {(3*137*136)**2/2:.0f} + ... ≈ {(3*137*136)**2/2:.2e}")
print(f"  WAY too large. Not the fine structure constant.")

# What if α = κ^something?
# κ = 1/5 = 0.2, α = 1/137 = 0.00730
# κ^k = α → k = log(α)/log(κ)
k_alpha = np.log(alpha) / np.log(1/p)
print(f"\nκ^k = α → k = log(α)/log(κ) = {k_alpha:.8f}")
print(f"  Not a simple integer or fraction.")

# κ^3 = λ/(1+λ) = 1/p^3 = 1/125 = 0.008
# α = 1/137 = 0.0073
# κ^3 / α = 125/137 ≈ 0.912
print(f"\nκ^n / α = (1/p^n) / α = p^n / (1/α) = {p**n}/{inv_alpha:.4f} = {p**n / inv_alpha:.8f}")
print(f"  = {p**n * alpha:.8f} ≈ {p**n * alpha:.4f}")
print(f"  125 * α = {125 * alpha:.8f} ≈ 0.912")
print(f"  p³ * α = {p**3 * alpha:.8f}")
print(f"  (p³-1) * α = {(p**3-1) * alpha:.8f} ≈ {124*alpha:.6f}")
print(f"  = 124/137.036 = {124/137.036:.8f}")

# Interesting: 124/137 ≈ 0.905
# (p³-1)/(1/α) = λ * (1/α) ... hmm
# Actually: 1/λ = p³-1 = 124, and 1/α = 137.036
# 137.036 - 124 = 13.036
print(f"\n  1/α - 1/λ = {inv_alpha} - {1/float(L)} = {inv_alpha - 124:.6f}")
print(f"  ≈ 13.036 ≈ n*p - n + 1? = {n*p - n + 1}")
print(f"  ≈ n*(p-1) + 1 = {n*(p-1)+1}")
print(f"  ≈ (p-1)² + Φ₃(1) = {(p-1)**2 + 3}")
print(f"  Exact: 137.036 - 124 = 13.036")
print(f"  13 is close. 13 = n*p - 2 = {n*p-2}")

# Let's check: 1/α = p³ - 1 + n*p - 2 + 0.036?
val_test = (p**3 - 1) + n*p - 2
print(f"\n  p³ - 1 + n*p - 2 = 124 + 15 - 2 = {val_test}")
print(f"  vs 1/α = 137.036. Off by {inv_alpha - val_test:.6f}")
print(f"  137 = 124 + 13 = (p³-1) + (n*p - 2)")
print(f"  137 exactly! The 0.036 is the fractional part.")

# WHOA. 137 = (p³-1) + (n*p - 2) = 124 + 13
# Let's verify: p=5, n=3
# p³-1 = 124
# n*p - 2 = 13
# Sum = 137
# And 1/α = 137.035999...

# The fractional part 0.035999... ≈ 0.036
# What is 0.036 in terms of (n,p)?
frac_part = inv_alpha - 137
print(f"\n  ★ 137 = (p³-1) + (n*p-2) = 124 + 13  EXACT INTEGER MATCH")
print(f"  ★ Fractional part: 1/α - 137 = {frac_part:.10f}")
print(f"    ≈ 1/(n*p² + n) = 1/{n*p**2+n} = {1/(n*p**2+n):.10f}  err: {abs(frac_part - 1/(n*p**2+n))/frac_part*100:.4f}%")
print(f"    ≈ n/(n*p³) = 1/p³ = {1/p**3:.10f}  err: {abs(frac_part - 1/p**3)/frac_part*100:.4f}%")
print(f"    ≈ 1/(p*Phi3 - n) = 1/{p*Phi3-n} = {1/(p*Phi3-n):.10f}  err: {abs(frac_part - 1/(p*Phi3-n))/frac_part*100:.4f}%")
print(f"    ≈ λ*p = {float(L)*p:.10f}  err: {abs(frac_part - float(L)*p)/frac_part*100:.4f}%")
print(f"    ≈ 1/(n*p*p) = 1/75 = {1/75:.10f}  err: {abs(frac_part - 1/75)/frac_part*100:.4f}%")

# Does 1/α = (p³-1) + n*p - 2 + correction?
# = p³ + n*p - 3
# = p*(p² + n) - 3
# = 5*(25+3) - 3 = 5*28 - 3 = 140 - 3 = 137. YES.

print(f"\n  ★★ SIMPLIFIED: 137 = p*(p² + n) - n = {p*(p**2+n) - n}")
print(f"      = p³ + n*p - n = {p**3 + n*p - n}")
print(f"      = p³ + n*(p-1) = {p**3 + n*(p-1)}")

# ALL EQUIVALENT:
# 137 = p³ + n*(p-1) = 125 + 12
# 137 = p*(p²+n) - n = 140 - 3
# 137 = (p³-1) + (n*p-2) = 124 + 13

# VERIFY for other Diophantine solutions
print(f"\n  Verification across Diophantine solutions:")
for nn, pp in [(3,5), (4,3), (6,2)]:
    val_137 = pp**3 + nn*(pp-1)
    print(f"    ({nn},{pp}): p³ + n(p-1) = {pp**3} + {nn*(pp-1)} = {val_137}")

# Only (3,5) gives 137! The others give 35 and 14.

print(f"\n  (3,5) → 137  ← ONLY THIS ONE")
print(f"  (4,3) → 35")
print(f"  (6,2) → 14")
print(f"  This is SPECIFIC to the proton solution.")

# Now the fractional part
print(f"\n" + "="*70)
print(f"THE FRACTIONAL PART: 1/α - 137 = {frac_part:.12f}")
print("="*70)

# 0.035999...
# Is this 9/250? 9/250 = 0.036
print(f"  9/250 = {9/250:.12f}  err: {abs(frac_part - 9/250)/frac_part*100:.6f}%")
print(f"  9/(n*p)³ = 9/3375 = {9/3375:.12f}")
print(f"  n²/p³ = 9/125 = {9/125:.12f}")
print(f"  1/(n*p²-n+1) = 1/{n*p**2-n+1} = {1/(n*p**2-n+1):.12f}")

# Brute force: find a/b closest to 0.035999917...
print(f"\n  Searching for simple fraction ≈ {frac_part:.10f}:")
best_err = 1
best_frac = None
for b in range(1, 1000):
    a = round(frac_part * b)
    if a <= 0: continue
    err = abs(a/b - frac_part)
    if err < best_err:
        best_err = err
        best_frac = (a, b)
        if err < 1e-8:
            print(f"    ★ {a}/{b} = {a/b:.12f}  err: {err:.2e}")

print(f"\n  Best simple fraction: {best_frac[0]}/{best_frac[1]} = {best_frac[0]/best_frac[1]:.12f}")

# Summary
print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"""
  THE INTEGER PART OF 1/α:
    137 = p³ + n*(p-1) = 125 + 12

  This is a function of the SAME (n,p) = (3,5) that gives M = 1836.153.
  It holds ONLY for the proton solution — (4,3) gives 35, (6,2) gives 14.

  DECOMPOSITION:
    1/α = [p³ + n*(p-1)] + fractional correction
    1/α = 137 + 0.03600...

  THE FRACTIONAL PART:
    0.035999917... needs further investigation.

  SIGNIFICANCE:
    If 1/α = p³ + n*(p-1) + f(n,p) for some derivable f,
    then RASP produces BOTH the proton mass ratio AND the
    fine structure constant from (n,p) = (3,5).

    That would be... extraordinary.
""")
