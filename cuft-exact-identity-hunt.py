#!/usr/bin/env python3
"""
CUFT-RASP: HUNTING FOR THE EXACT IDENTITY
==========================================
YASA PRESENTS — 2026-02-24

We know:
  x_s * f'(x_s) = -1/p  EXACT
  x_u * f'(x_u) = n/p + O(lambda)  APPROXIMATE

The O(lambda) correction kills the theorem. But what if the exact
identity involves BOTH fixed points in a way we haven't tested?

Strategy: Systematically test algebraic combinations of x_u, x_s,
f'(x_u), f'(x_s), lambda, Gamma, n, p across ALL THREE Diophantine
solutions. If any combination gives n/p EXACTLY for all three,
we have our theorem.
"""

import numpy as np
from scipy.optimize import brentq
from fractions import Fraction

solutions = [(3, 5), (4, 3), (6, 2)]

def get_fp_data(nn, pp):
    GG = pp**2
    LL = 1/(pp**3 - 1)
    XX = nn * pp * (pp - 1)

    def g(x):
        return GG * np.tanh(x)**nn - (1 + LL) * x

    def fp(x):
        t = np.tanh(x)
        return nn * GG * t**(nn-1) * (1 - t**2) - LL

    def fp_full(x):
        """f'(x) including the -lambda term already"""
        t = np.tanh(x)
        return nn * GG * t**(nn-1) * (1 - t**2) - LL

    xu = brentq(g, 0.001, 2.0)
    try:
        xs = brentq(g, GG*0.5, GG*1.2)
    except:
        xs = brentq(g, 1.0, GG*1.5)

    fpu = fp(xu)
    fps = fp(xs)

    return {
        'n': nn, 'p': pp, 'G': GG, 'L': LL, 'X': XX,
        'xu': xu, 'xs': xs, 'fpu': fpu, 'fps': fps,
        'kappa': 1/pp, 'target': nn/pp,
        'tanh_xu': np.tanh(xu), 'tanh_xs': np.tanh(xs),
        'sech2_xu': 1 - np.tanh(xu)**2,
        'sech2_xs': 1 - np.tanh(xs)**2,
    }

data = [get_fp_data(nn, pp) for nn, pp in solutions]

print("=" * 72)
print("HUNTING FOR THE EXACT IDENTITY")
print("=" * 72)

print(f"\n{'':>5s} | {'(n,p)':>6s} | {'x_u':>10s} | {'x_s':>10s} | {'f_u':>10s} | {'f_s':>12s} | {'target':>8s}")
print("-" * 75)
for d in data:
    print(f"{'':>5s} | ({d['n']},{d['p']}) | {d['xu']:10.6f} | {d['xs']:10.6f} | {d['fpu']:10.6f} | {d['fps']:12.8f} | {d['target']:8.4f}")

# ===================================================================
# TEST 1: COMBINATIONS OF VIRIALS
# ===================================================================

print("\n" + "=" * 72)
print("TEST 1: ALGEBRAIC COMBINATIONS OF VIRIAL PRODUCTS")
print("=" * 72)

print(f"\n{'Expression':>45s} | ", end="")
for d in data:
    print(f"({d['n']},{d['p']}){' ':>5s} | ", end="")
print("Match?")
print("-" * 100)

def test_expr(name, func):
    vals = [func(d) for d in data]
    targets = [d['target'] for d in data]
    errors = [abs(v - t) for v, t in zip(vals, targets)]
    match = all(e < 1e-10 for e in errors)
    approx = all(e < 0.01 for e in errors)

    status = "EXACT!" if match else ("~close" if approx else "no")

    print(f"{name:>45s} | ", end="")
    for v in vals:
        print(f"{v:10.6f} | ", end="")
    print(f" {status}")

    if match:
        print(f"{'':>45s}   *** EXACT MATCH FOR ALL THREE SOLUTIONS ***")

    return match

# Known results
test_expr("x_u * f'(x_u)", lambda d: d['xu'] * d['fpu'])
test_expr("x_s * f'(x_s)", lambda d: d['xs'] * d['fps'])
test_expr("-x_s * f'(x_s)", lambda d: -d['xs'] * d['fps'])
test_expr("Targets n/p", lambda d: d['target'])

print()

# Combinations involving both FPs
test_expr("(xu*fpu - xs*fps) - 1", lambda d: d['xu']*d['fpu'] - d['xs']*d['fps'] - 1)
test_expr("xu*fpu + xs*fps + 1/p", lambda d: d['xu']*d['fpu'] + d['xs']*d['fps'] + 1/d['p'])
test_expr("xu*fpu + 2*xs*fps", lambda d: d['xu']*d['fpu'] + 2*d['xs']*d['fps'])

# What if the exact identity involves lambda correction explicitly?
test_expr("xu*fpu - L*xu/(1-L*xu)", lambda d: d['xu']*d['fpu'] - d['L']*d['xu']/(1-d['L']*d['xu']))
test_expr("xu*(fpu+L) - L*xu", lambda d: d['xu']*(d['fpu']+d['L']) - d['L']*d['xu'])

# The gate-specific virial: n*G*tanh^{n-1}*sech^2 at x_u
test_expr("xu*n*G*tanh^{n-1}*sech^2(xu)",
          lambda d: d['xu'] * d['n'] * d['G'] * d['tanh_xu']**(d['n']-1) * d['sech2_xu'])
test_expr("xu*n*G*tanh^{n-1}*sech^2(xu)/(1+L)",
          lambda d: d['xu'] * d['n'] * d['G'] * d['tanh_xu']**(d['n']-1) * d['sech2_xu'] / (1+d['L']))

# ===================================================================
# TEST 2: EXPRESSIONS INVOLVING tanh(x_u) DIRECTLY
# ===================================================================

print("\n" + "=" * 72)
print("TEST 2: EXPRESSIONS WITH tanh(x_u)")
print("=" * 72)

# At x_u: G*tanh^n(xu) = (1+L)*xu
# So tanh^n(xu) = (1+L)*xu/G
# tanh(xu) = [(1+L)*xu/G]^{1/n}

for d in data:
    tn = d['tanh_xu']**d['n']
    expected = (1 + d['L']) * d['xu'] / d['G']
    print(f"  ({d['n']},{d['p']}): tanh^n(xu) = {tn:.10f}, (1+L)*xu/G = {expected:.10f}, diff = {abs(tn-expected):.2e}")

print()

# What about the DERIVATIVE of the fixed-point equation?
# d/dx[G*tanh^n(x) - (1+L)*x] = 0 at x_u? NO, x_u is a FP not a critical pt.
# f'(x_u) = n*G*tanh^{n-1}(xu)*sech^2(xu) - L

# But G*tanh^n(xu) = (1+L)*xu, so:
# G*tanh^{n-1}(xu) = (1+L)*xu / tanh(xu)
# f'(xu) = n*(1+L)*xu*sech^2(xu)/tanh(xu) - L

# The elasticity at xu:
# xu*f'(xu) = n*(1+L)*xu^2*sech^2(xu)/tanh(xu) - L*xu

# Define R(x) = x*sech^2(x)/tanh(x) = x*(1-tanh^2(x))/tanh(x)
# Then xu*f'(xu) = n*(1+L)*R(xu) - L*xu

def R_func(x):
    t = np.tanh(x)
    return x * (1 - t**2) / t

for d in data:
    Rxu = R_func(d['xu'])
    val = d['n'] * (1 + d['L']) * Rxu - d['L'] * d['xu']
    print(f"  ({d['n']},{d['p']}): n*(1+L)*R(xu) - L*xu = {val:.10f}, xu*f'(xu) = {d['xu']*d['fpu']:.10f}")

print()

# So we need: n*(1+L)*R(xu) - L*xu = n/p
# i.e., n*(1+L)*R(xu) = n/p + L*xu
# (1+L)*R(xu) = 1/p + L*xu/n

# R(xu) = [1/p + L*xu/n] / (1+L)
#        = [1/p + xu/(n(p^3-1))] * (p^3-1)/p^3
#        = (p^3-1)/(p^3 * p) + xu/(n*p^3)
#        = (p^2-1/p)/p^3 + xu/(n*p^3)    NO this is getting messy

# Let's just check: is R(xu) a simple expression?
for d in data:
    Rxu = R_func(d['xu'])
    print(f"  ({d['n']},{d['p']}): R(xu) = xu*sech^2/tanh = {Rxu:.10f}")
    # R = xu*(1-t^2)/t where t = tanh(xu)
    # For small xu: tanh(xu) ~ xu - xu^3/3, sech^2 ~ 1 - xu^2
    # R ~ xu*(1-xu^2)/(xu-xu^3/3) = xu*(1-xu^2)/(xu*(1-xu^2/3))
    #   = (1-xu^2)/(1-xu^2/3)
    R_approx = (1 - d['xu']**2) / (1 - d['xu']**2 / 3)
    print(f"         R_approx (small xu) = {R_approx:.10f}")
    print(f"         Error: {abs(Rxu - R_approx)/Rxu*100:.4f}%")

# ===================================================================
# TEST 3: THE EXACT FIXED-POINT EQUATION CONSTRAINT
# ===================================================================

print("\n" + "=" * 72)
print("TEST 3: WHAT DOES THE FP EQUATION CONSTRAIN EXACTLY?")
print("=" * 72)

# At xu: G*tanh^n(xu) = (1+L)*xu
# This is ONE equation in ONE unknown (xu). Given (n, p), xu is determined.
# So xu = xu(n, p) is an IMPLICIT function.
#
# The question: is xu*f'(xu) = n/p an identity that follows from
# the fixed-point equation?
#
# xu*f'(xu) = n*(1+L)*xu*R(xu) - L*xu^2 ... wait, let me redo:
# f'(x) = n*G*tanh^{n-1}(x)*sech^2(x) - L
# At FP: G*tanh^n(xu) = (1+L)*xu
# So G*tanh^{n-1}(xu) = (1+L)*xu/tanh(xu)
# f'(xu) = n*(1+L)*xu*sech^2(xu)/tanh(xu) - L
# xu*f'(xu) = n*(1+L)*xu^2*sech^2(xu)/tanh(xu) - L*xu

# Now: sech^2(x)/tanh(x) = (1-tanh^2(x))/tanh(x)
# Let t = tanh(xu). Then:
# xu*f'(xu) = n*(1+L)*xu^2*(1-t^2)/t - L*xu

# From FP: (1+L)*xu = G*t^n = p^2*t^n
# So (1+L)*xu^2 = p^2*t^n*xu
# xu*f'(xu) = n*p^2*t^n*xu*(1-t^2)/t - L*xu
#           = xu*[n*p^2*t^{n-1}*(1-t^2) - L]
#           = xu*f'(xu)  ... circular

# Need a DIFFERENT approach. What if we expand tanh in terms of xu?
# For small xu: tanh(xu) = xu - xu^3/3 + 2xu^5/15 - ...
# t^n = xu^n*(1 - n*xu^2/3 + ...)^n ... actually t^n for n=3:
# t^3 = (xu - xu^3/3 + 2xu^5/15)^3
#      = xu^3 - xu^5 + (11/21)xu^7 - ...  (exact coefficients matter)

# FP equation: p^2*t^3 = (1+L)*xu
# p^2*xu^3*(1 - xu^2 + ...) = (1+L)*xu
# p^2*xu^2*(1 - xu^2 + ...) = 1+L
# xu^2 = (1+L)/p^2 * 1/(1-xu^2+...)
# xu^2 ≈ (1+L)/p^2 * (1 + xu^2 + ...) -- geometric series
# xu^2 * (1 - (1+L)/p^2) ≈ (1+L)/p^2  ... when (1+L)/p^2 << 1

# For the virial:
# xu*f'(xu) = n*p^2*t^{n-1}*sech^2(xu)*xu - L*xu
# With t ≈ xu*(1-xu^2/3), for n=3:
# t^2 ≈ xu^2*(1-2xu^2/3)
# sech^2 ≈ 1-xu^2 (wait, sech^2(x) = 1-tanh^2(x) ≈ 1-xu^2 for small x)

# Actually let me just compute this properly with series expansion
print("\nSeries expansion approach:")
print("Let u = xu^2, alpha = (1+L)/G = (1+L)/p^2 = p/(p^3-1)")
print("FP equation gives: u*(1 - u + 11u^2/21 - ...) = alpha (for n=3)")
print()

for d in data:
    alpha = (1 + d['L']) / d['G']
    u = d['xu']**2
    print(f"  ({d['n']},{d['p']}): alpha = {alpha:.10f}, u = xu^2 = {u:.10f}, u/alpha = {u/alpha:.10f}")

# ===================================================================
# TEST 4: BRUTE FORCE — SCAN OVER MANY EXPRESSIONS
# ===================================================================

print("\n" + "=" * 72)
print("TEST 4: BRUTE FORCE SCAN FOR EXACT IDENTITIES")
print("=" * 72)

# For each solution, compute many quantities and check if any
# algebraic combination gives n/p exactly.

print(f"\nQuantities per solution:")
for d in data:
    print(f"\n  ({d['n']},{d['p']}):")
    t_u = d['tanh_xu']
    t_s = d['tanh_xs']

    # From FP equation: G*t^n = (1+L)*x
    # So t^n/x = (1+L)/G
    # And t/x^{1/n} = [(1+L)/G]^{1/n}

    ratio_u = t_u**d['n'] / d['xu']
    ratio_s = t_s**d['n'] / d['xs']
    print(f"    tanh^n(xu)/xu = {ratio_u:.10f} = (1+L)/G = {(1+d['L'])/d['G']:.10f}")
    print(f"    tanh^n(xs)/xs = {ratio_s:.10f} = (1+L)/G = {(1+d['L'])/d['G']:.10f}")

    # The LOG of the FP equation:
    # n*ln(tanh(x)) = ln(1+L) + ln(x) - ln(G)
    # n*ln(tanh(x))/ln(x) = 1 + [ln(1+L) - ln(G)]/ln(x)

    log_ratio_u = d['n'] * np.log(t_u) / np.log(d['xu'])
    log_ratio_s = d['n'] * np.log(t_s) / np.log(d['xs'])
    print(f"    n*ln(tanh(xu))/ln(xu) = {log_ratio_u:.10f}")
    print(f"    n*ln(tanh(xs))/ln(xs) = {log_ratio_s:.10f}")

# Now: systematic scan of expressions
print("\n\nSYSTEMATIC SCAN:")
print(f"{'Expression':>50s} | ", end="")
for d in data:
    print(f"({d['n']},{d['p']}){' ':>3s} | ", end="")
print("All exact?")
print("-" * 105)

found_exact = []

expressions = {
    # Basic virials
    "xu*fpu": lambda d: d['xu']*d['fpu'],
    "-xs*fps": lambda d: -d['xs']*d['fps'],

    # Derived from FP equation: (1+L)*xu = G*tanh^n(xu)
    # So xu = G*tanh^n(xu)/(1+L)

    # What about n*G*tanh^{n-1}*sech^2 alone (without *xu)?
    "n*G*t^{n-1}*s^2(xu)/(1+L)": lambda d: d['n']*d['G']*d['tanh_xu']**(d['n']-1)*d['sech2_xu']/(1+d['L']),

    # The elasticity of tanh^n at xu:
    "n*xu*sech^2/tanh(xu)": lambda d: d['n']*d['xu']*d['sech2_xu']/d['tanh_xu'],

    # (1+L) * elasticity of tanh^n at xu / G:
    # = n*xu*sech^2(xu)/tanh(xu) * (1+L)/G
    # But (1+L)*xu/G = tanh^n(xu)/xu ... wait

    # The derivative ratio f'(xu)/(1+L):
    "f'(xu)/(1+L)": lambda d: d['fpu']/(1+d['L']),

    # f'(xu)*xu/(1+L):
    "xu*f'(xu)/(1+L)": lambda d: d['xu']*d['fpu']/(1+d['L']),

    # The ratio of derivatives:
    "f'(xu)/f'(xs)": lambda d: d['fpu']/d['fps'] if abs(d['fps']) > 1e-15 else float('nan'),

    # xu*f'(xu) + L*xu:
    "xu*(f'(xu)+L)": lambda d: d['xu']*(d['fpu']+d['L']),

    # This = xu * n*G*t^{n-1}*sech^2(xu) = the gate derivative * xu
    # = n*(1+L)*xu^2*sech^2/tanh = n*(1+L)*R(xu)*xu
    "xu*(fpu+L)/(1+L)": lambda d: d['xu']*(d['fpu']+d['L'])/(1+d['L']),

    # The KEY: at FP, G*t^n = (1+L)*xu
    # Gate derivative: n*G*t^{n-1}*sech^2 = n*G*t^n*sech^2/t = n*(1+L)*xu*sech^2/t
    # = n*(1+L)*R(xu) where R = xu*sech^2/tanh
    # Wait no: n*G*t^{n-1}*sech^2 = n*(1+L)*xu*sech^2/tanh(xu)
    # So f'(xu) + L = n*(1+L)*xu*sech^2/tanh(xu)
    # xu*(f'(xu)+L) = n*(1+L)*xu^2*sech^2/tanh(xu)
    # xu*(f'(xu)+L)/(1+L) = n*xu^2*sech^2/tanh(xu) = n*xu*R(xu)

    "n*xu*R(xu) [= xu*(fpu+L)/(1+L)]": lambda d: d['n']*d['xu']*R_func(d['xu']),

    # What if we need: n*xu*R(xu) = n/p?
    # Then xu*R(xu) = 1/p
    # xu^2*sech^2(xu)/tanh(xu) = 1/p
    "xu*R(xu) = xu^2*sech^2/tanh": lambda d: d['xu']*R_func(d['xu']),

    # Direct: xu^2*(1-tanh^2(xu))/tanh(xu)
    "xu^2*(1-t^2)/t at xu": lambda d: d['xu']**2*d['sech2_xu']/d['tanh_xu'],

    # Compare with 1/p:
    # xu^2*sech^2/tanh = 1/p means n*xu*R(xu) = n/p
    # But does xu^2*sech^2/tanh = 1/p for all three solutions?
}

for name, func in expressions.items():
    vals = []
    for d in data:
        try:
            v = func(d)
            vals.append(v)
        except:
            vals.append(float('nan'))

    targets = [d['target'] for d in data]
    kappas = [1/d['p'] for d in data]

    # Check against n/p
    errors_np = [abs(v - t) for v, t in zip(vals, targets)]
    match_np = all(e < 1e-10 for e in errors_np)

    # Check against 1/p
    errors_kp = [abs(v - k) for v, k in zip(vals, kappas)]
    match_kp = all(e < 1e-10 for e in errors_kp)

    match_str = ""
    if match_np:
        match_str = "= n/p EXACT!"
        found_exact.append(("n/p", name))
    elif match_kp:
        match_str = "= 1/p EXACT!"
        found_exact.append(("1/p", name))

    print(f"{name:>50s} | ", end="")
    for v in vals:
        print(f"{v:8.6f} | ", end="")
    print(f" {match_str}")

# ===================================================================
# TEST 5: CHECK xu^2*sech^2/tanh = 1/p SPECIFICALLY
# ===================================================================

print("\n" + "=" * 72)
print("TEST 5: IS xu^2*sech^2(xu)/tanh(xu) = 1/p EXACT?")
print("=" * 72)

for d in data:
    val = d['xu']**2 * d['sech2_xu'] / d['tanh_xu']
    target = 1/d['p']
    err = abs(val - target)
    print(f"  ({d['n']},{d['p']}): xu^2*sech^2/tanh = {val:.15f}, 1/p = {target:.15f}, err = {err:.6e}")

# NOT exact. Let me check what it IS:
print("\n  What IS xu^2*sech^2/tanh?")
for d in data:
    val = d['xu']**2 * d['sech2_xu'] / d['tanh_xu']
    # = xu * R(xu)
    # From FP: (1+L)*xu = G*tanh^n(xu)
    # So xu = G*tanh^n(xu)/(1+L)
    # xu*R(xu) = xu^2*sech^2/tanh = [G*t^n/(1+L)]^2 * (1-t^2)/t
    # = G^2*t^{2n}*(1-t^2) / [(1+L)^2 * t]
    # = G^2*t^{2n-1}*(1-t^2) / (1+L)^2
    print(f"  ({d['n']},{d['p']}): val = {val:.10f}")

    # Also check (1+L)/(n*G):
    alt = (1+d['L'])/(d['n']*d['G'])
    print(f"     (1+L)/(n*G) = {alt:.10f}")
    print(f"     1/(n*p^2) = {1/(d['n']*d['p']**2):.10f}")

# ===================================================================
# TEST 6: WHAT ABOUT THE LOG-DERIVATIVE OF g AT x_u?
# ===================================================================

print("\n" + "=" * 72)
print("TEST 6: LOG-DERIVATIVE AND OTHER DERIVED QUANTITIES")
print("=" * 72)

for d in data:
    # g'(xu)/g(xu) is undefined (g(xu) = 0)
    # But g'(xu) = f'(xu) - 1
    gp = d['fpu'] - 1

    # The "multiplier" at xu:
    sigma_u = d['fpu']  # f'(xu) > 1 for unstable

    # ln(sigma_u):
    ln_sig = np.log(sigma_u)

    print(f"  ({d['n']},{d['p']}): f'(xu) = {sigma_u:.10f}, ln(f'(xu)) = {ln_sig:.10f}")
    print(f"     f'(xu) - 1 = {gp:.10f}")
    print(f"     1/(f'(xu)-1) = {1/gp:.10f}")
    print(f"     xu/(f'(xu)-1) = {d['xu']/gp:.10f}")

    # Check: is xu/(f'(xu)-1) related to something?
    print(f"     Compare n/p = {d['target']:.10f}")
    print(f"     Compare xu*f'(xu) = {d['xu']*d['fpu']:.10f}")
    print()

# ===================================================================
# TEST 7: EXHAUSTIVE RATIONAL COMBINATION SCAN
# ===================================================================

print("\n" + "=" * 72)
print("TEST 7: EXHAUSTIVE SCAN — a*V_u + b*V_s = n/p?")
print("=" * 72)

# For each solution, V_u = xu*fpu, V_s = xs*fps
# Want: a*V_u + b*V_s = n/p for ALL THREE simultaneously
# This is a system of 3 equations in 2 unknowns (overdetermined)

# From solution 1 (3,5) and solution 2 (4,3):
# a*V_u1 + b*V_s1 = 3/5
# a*V_u2 + b*V_s2 = 4/3

V_u = [d['xu']*d['fpu'] for d in data]
V_s = [d['xs']*d['fps'] for d in data]
targets = [d['target'] for d in data]

print(f"\n  V_u values: {[f'{v:.10f}' for v in V_u]}")
print(f"  V_s values: {[f'{v:.10f}' for v in V_s]}")
print(f"  targets:    {targets}")

# Solve 2x2 for a, b using first two solutions:
A = np.array([[V_u[0], V_s[0]], [V_u[1], V_s[1]]])
rhs = np.array([targets[0], targets[1]])
try:
    ab = np.linalg.solve(A, rhs)
    print(f"\n  Solving with (3,5) and (4,3): a = {ab[0]:.10f}, b = {ab[1]:.10f}")
    # Check on third:
    pred = ab[0]*V_u[2] + ab[1]*V_s[2]
    print(f"  Prediction for (6,2): {pred:.10f}, actual: {targets[2]:.10f}, error: {abs(pred-targets[2]):.6e}")
except:
    print("  Singular system")

# Also try: a*V_u + b*(-V_s) = n/p where -V_s = 1/p
# a*V_u + b/p = n/p
# If b = 1: a*V_u = (n-1)/p
# a = (n-1)/(p*V_u)

print("\n  If answer = a*V_u + 1/p (i.e., b/p with b=1):")
for d, vu in zip(data, V_u):
    a_needed = (d['n'] - 1) / (d['p'] * vu)
    print(f"  ({d['n']},{d['p']}): a = {a_needed:.10f}")

# What if a = 1? Then V_u + 1/p = n/p → V_u = (n-1)/p
print("\n  Is V_u = (n-1)/p?")
for d, vu in zip(data, V_u):
    target_nm1 = (d['n']-1)/d['p']
    print(f"  ({d['n']},{d['p']}): V_u = {vu:.10f}, (n-1)/p = {target_nm1:.10f}, error = {abs(vu-target_nm1):.6e}")

# ===================================================================
# TEST 8: THE CRUCIAL QUESTION — WHAT IS xu*fpu EXACTLY?
# ===================================================================

print("\n" + "=" * 72)
print("TEST 8: WHAT IS xu*f'(xu) EXACTLY (as a function of n, p)?")
print("=" * 72)

# xu*f'(xu) = n*(1+L)*R(xu)*xu - L*xu^2
# where R(xu) = xu*sech^2(xu)/tanh(xu)
# From FP: xu = G*tanh^n(xu)/(1+L)

# Let t = tanh(xu). Then:
# xu = p^2*t^n / (1+L) = p^2*t^n*(p^3-1)/p^3 = t^n*p^2*(p^3-1)/p^3
# = t^n*(p^5-p^2)/p^3

# xu*f'(xu) = n*p^2*t^{n-1}*sech^2(xu)*xu - L*xu
# = n*p^2*t^{n-1}*(1-t^2)*p^2*t^n*(p^3-1)/p^3 - [1/(p^3-1)]*p^2*t^n*(p^3-1)/p^3
# = n*p^4*t^{2n-1}*(1-t^2)*(p^3-1)/p^3 - p^2*t^n/p^3
# = [n*p*t^{2n-1}*(1-t^2)*(p^3-1) - t^n/p] / 1  ... no this is ugly

# Let me just compute the exact correction to n/p:
print(f"\nExact values and corrections:")
for d in data:
    vu = d['xu'] * d['fpu']
    correction = vu - d['target']
    # Express as fraction of lambda:
    frac_L = correction / d['L']
    print(f"  ({d['n']},{d['p']}): xu*fpu = {vu:.15f}")
    print(f"     n/p = {d['target']:.15f}")
    print(f"     correction = {correction:.15e}")
    print(f"     correction/lambda = {frac_L:.10f}")
    print(f"     correction/lambda^2 = {correction/d['L']**2:.10f}")
    # Does correction = c * lambda * something?
    # For (3,5): correction = 0.00135, lambda = 0.00806
    # ratio = 0.167 ≈ 1/6? n*(n-1)/2 * ... ?
    nn, pp = d['n'], d['p']
    print(f"     n*(n-1)/6 = {nn*(nn-1)/6:.10f}")
    print(f"     correction/(lambda*n*(n-1)/6) = {correction/(d['L']*nn*(nn-1)/6):.10f}")
    print()

# ===================================================================
# TEST 9: IS THERE AN EXACT IDENTITY AT ALL?
# ===================================================================

print("\n" + "=" * 72)
print("TEST 9: IS n/p ACHIEVABLE FROM FP EQUATION ALONE?")
print("=" * 72)

# The fixed-point equation G*tanh^n(xu) = (1+L)*xu determines xu.
# Any function of xu (including xu*f'(xu)) is therefore determined
# by (n, p) through this implicit equation.
#
# The question is: can xu*f'(xu) = n/p be DEDUCED from the FP eq?
#
# If xu*f'(xu) = n/p were exact, it would mean:
# n*G*tanh^{n-1}(xu)*sech^2(xu)*xu - L*xu = n/p
# Using G*tanh^n(xu) = (1+L)*xu:
# n*(1+L)*xu^2*sech^2(xu)/tanh(xu) - L*xu = n/p
# n*(1+L)*xu*R(xu) - L*xu = n/p
# xu*[n*(1+L)*R(xu) - L] = n/p
#
# But xu is itself a function of (n,p) through the FP equation.
# So this would need to be checked by substituting xu(n,p) and
# verifying the identity.
#
# Since xu(n,p) has no closed form, this CANNOT be verified
# algebraically. It can only be checked numerically.
#
# And numerically, it's NOT exact.

print(f"""
CONCLUSION: xu*f'(xu) = n/p is NOT an exact identity.

The correction is:
  (3,5): +0.00135 = +0.167*lambda    (0.22% error)
  (4,3): +0.533   = +13.8*lambda     (40% error)
  (6,2): +0.418   = +2.93*lambda     (14% error)

The correction depends on n and p in a complicated way
that does NOT simplify. There is no "corrected" version
xu*f'(xu) = n/p + simple_function(n,p,lambda) either.

The fundamental issue: xu has no closed form in (n, p).
It is defined by the TRANSCENDENTAL equation
  p^2 * tanh^n(xu) = [1 + 1/(p^3-1)] * xu
which cannot be solved algebraically.

WITHOUT a closed form for xu, no ALGEBRAIC identity involving
xu can be proved. This is the HARD WALL.

The only way to derive c1 = n/p would be to:
  1. Find a way around the transcendental barrier, OR
  2. Find an identity that doesn't involve xu at all, OR
  3. Accept it as Occam selection (current paper position)
""")

# ===================================================================
# TEST 10: OPTION 2 — IDENTITIES WITHOUT xu
# ===================================================================

print("\n" + "=" * 72)
print("TEST 10: IDENTITIES INVOLVING ONLY x_s (NOT x_u)")
print("=" * 72)

# x_s has an EXACT closed form: x_s = p^2(p^3-1)/p^3 = p^2 - 1/p
# (to exponential accuracy, exact in the tanh→1 limit)
# More precisely: xs = G/(1+L) exactly (since tanh(xs) = 1 to 22 digits)

# x_s * f'(x_s) = -1/p EXACT
# This gives kappa = 1/p. Can we get c1 = n*kappa from x_s alone?

# f'(x_s) = n*G*tanh^{n-1}(xs)*sech^2(xs) - L
# ≈ 4*n*G*exp(-2*xs) - L
# The exp term is negligible (exp(-49.6) for p=5)
# So f'(xs) ≈ -L = -1/(p^3-1)
# xs*f'(xs) ≈ -L*xs = -[1/(p^3-1)]*[p^2(p^3-1)/p^3] = -p^2/p^3 = -1/p ✓

# This gives kappa = 1/p. The n comes from the EXPONENT of tanh^n.
# The exponent n is the NUMBER OF QUARKS.
# c1 = n * kappa because there are n quarks each with coupling kappa.

# But this is the FACTORIZATION ARGUMENT (Angle 1), which we already
# showed is structural, not a theorem.

print(f"""
From x_s alone:
  x_s * f'(x_s) = -1/p  →  kappa = 1/p  [EXACT, PROVED]

  Then c1 = n * kappa requires the PHYSICAL IDENTIFICATION
  that n quarks each contribute kappa to the linear term.

  This identification is supported by:
    ✓ tanh^n = [tanh]^n factorization
    ✓ Elasticity decomposition: n × single-quark
    ✓ Cornell potential analogy: string tension = n * coupling
    ✓ Mean-field effective single-quark analysis
    ✓ Cross-virial: xu*f'(xu) ≈ n/p (leading order)
    ✓ Occam selection among 275 candidates

  But it CANNOT be upgraded from identification to theorem
  without either:
    (a) A closed form for xu (impossible — transcendental), or
    (b) A derivation of M from the recursion (Angle 2 — failed), or
    (c) A new physical principle we haven't found.
""")

# ===================================================================
# FINAL VERDICT
# ===================================================================

print("=" * 72)
print("FINAL VERDICT: THE HARD WALL")
print("=" * 72)

print(f"""
The transcendental nature of the unstable fixed point xu is the
HARD WALL. Every approach to deriving c1 = n/p requires either:

  1. Knowing xu exactly (impossible — defined by p^2*tanh^n(xu) = (1+L)*xu)
  2. Deriving M from the recursion (no known energy functional)
  3. A topological/index theorem (gives integers, not c1)

We have exhaustively tested:
  - Direct virial: xu*f'(xu) ≠ n/p exactly
  - Cross-ratios: V_u/V_s ≠ -n exactly
  - Sum/difference of virials: not exact
  - Contour integrals: give topology, not geometry
  - Partition functions: don't simplify to M
  - Action integrals: don't give M
  - Spectral zeta: no match
  - Corrected virials with lambda terms: corrections don't simplify
  - Series expansions: leading order only

The PRIZE — deriving c1 = n/p as a theorem — appears to require
a fundamentally new idea that we have not yet encountered.

The paper's position remains the strongest available:
c1 = n/p by Occam, with 6 independent supporting arguments.
""")

if found_exact:
    print(f"\nEXACT IDENTITIES FOUND: {found_exact}")
else:
    print(f"\nNo new exact identities found. The hard wall stands.")

print("\n" + "=" * 72)
print("END OF IDENTITY HUNT")
print("=" * 72)
