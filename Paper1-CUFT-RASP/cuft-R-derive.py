#!/usr/bin/env python3
"""
CUFT-RASP: DERIVE THE R VALUES FROM FIRST PRINCIPLES
=====================================================

The key insight from cuft-mechanism-derive.py:
  - Pairwise coupling (eps_ij) is INSUFFICIENT (5-7% error)
  - The tanh³ nonlinearity doesn't help (saturated ≈ exact)
  - The R = lambda_eff/lambda values ARE structural fractions
  - R must come from a DIFFERENT mechanism than pairwise coupling

NEW APPROACH: The damping modification isn't from coupling between quarks.
It's from the INTERFERENCE PATTERN of the three quark wavefunctions.

The proton formula works because it captures the COLLECTIVE mode.
The spectrum needs the THREE-BODY interference pattern.

Key data to explain:
  proton  (uud, I=1/2): R = 1.2861
  neutron (udd, I=1/2): R = 1.2019  (n-p difference!)
  Lambda  (uds, I=0):   R = 4.7370  (HUGE amplification)
  Sigma+  (uus, I=1):   R = 0.8785  (reduction)
  Sigma0  (uds, I=1):   R = 0.7132  (reduction, SAME quarks as Lambda!)
  Sigma-  (dds, I=1):   R = 0.4667  (strong reduction)
  Xi0     (uss, I=1/2): R = 6.1014  (HUGE amplification)
  Xi-     (dss, I=1/2): R = 5.9780  (HUGE amplification)
  Omega-  (sss, I=0):   R = 1.0301  (nearly unity, pure s)

Patterns:
  - Pure flavor (p/n ~ uuu, Omega = sss): R ≈ 1
  - Lambda/Xi (antisymmetric light pair): R >> 1 (amplified)
  - Sigma (symmetric light pair): R < 1 (reduced)
  - The Lambda-Sigma split is PURELY from isospin configuration
"""

import numpy as np
from itertools import combinations

# Constants
lambda_0 = 0.008097
Gamma_u = 25.0
Gamma_d = 25.0  # treat as equal for now
Gamma_s = 100.0/3.0

# Baryon data: (name, quarks, I, S, Y, n_s, mass_ratio)
baryons = [
    ('proton',  'uud', 0.5,  0,  1, 0, 1836.15267),
    ('neutron', 'udd', 0.5,  0,  1, 0, 1838.68366),
    ('Lambda',  'uds', 0.0, -1,  0, 1, 2183.46),
    ('Sigma+',  'uus', 1.0, -1,  0, 1, 2327.64),
    ('Sigma0',  'uds', 1.0, -1,  0, 1, 2333.92),
    ('Sigma-',  'dds', 1.0, -1,  0, 1, 2343.30),
    ('Xi0',     'uss', 0.5, -2, -1, 2, 2572.85),
    ('Xi-',     'dss', 0.5, -2, -1, 2, 2578.26),
    ('Omega-',  'sss', 1.5, -3, -2, 3, 3277.96),
]

def get_gammas(quarks):
    gammas = []
    for q in quarks:
        if q == 'u': gammas.append(Gamma_u)
        elif q == 'd': gammas.append(Gamma_d)
        elif q == 's': gammas.append(Gamma_s)
    return gammas

def get_R(mass, quarks):
    gammas = get_gammas(quarks)
    sum_g2 = sum(g**2 for g in gammas)
    return (1 - np.sqrt(mass / sum_g2)) / lambda_0

# Extract exact R values
R_exact = {}
for name, quarks, I, S, Y, n_s, mass in baryons:
    R_exact[name] = get_R(mass, quarks)

print("="*80)
print("PART 1: THE THREE-BODY INTERFERENCE MODEL")
print("="*80)
print()
print("  Instead of pairwise coupling, model the damping modification as")
print("  arising from three-body wavefunction interference.")
print()
print("  Key insight: In a 3-quark system, the color wavefunction is always")
print("  antisymmetric. The flavor-spin part determines the mass through")
print("  its SYMMETRY PATTERN under quark exchange.")
print()
print("  For SU(6) flavor-spin, the baryon octet has mixed symmetry [21]")
print("  and the decuplet is fully symmetric [3]. The MIXED symmetry")
print("  means some pairs are symmetric, others antisymmetric.")
print()

# The SU(6) classification of baryons
# Octet (J=1/2): mixed symmetry [21] in flavor-spin
# Decuplet (J=3/2): symmetric [3] in flavor-spin
#
# For octet baryons, the key quantum number is the symmetry
# of the flavor wavefunction under exchange of the first two quarks.
#
# Lambda: ud ANTISYMMETRIC in flavor (I=0, flavor [21])
# Sigma:  ud SYMMETRIC in flavor (I=1, flavor [3] or [21])
# proton: uu SYMMETRIC (identical quarks)
# Xi:     ss or us/ds mixed

# For each baryon, compute:
# 1. Number of SYMMETRIC pairs (quarks with same exchange symmetry)
# 2. Number of ANTISYMMETRIC pairs
# 3. The Gamma-weighted symmetry factor

# Define phase assignments based on SU(6)
# sigma_ij = +1 for symmetric pair, -1 for antisymmetric
phase_assignments = {
    'proton':  {'uu': +1, 'ud1': +1, 'ud2': +1},  # all symmetric in ground state
    'neutron': {'dd': +1, 'ud1': +1, 'ud2': +1},   # all symmetric
    'Lambda':  {'ud': -1, 'us': -1, 'ds': -1},      # antisymmetric ud (I=0)
    'Sigma+':  {'uu': +1, 'us1': +1, 'us2': +1},   # symmetric uu
    'Sigma0':  {'ud': +1, 'us': -1, 'ds': -1},      # symmetric ud (I=1)
    'Sigma-':  {'dd': +1, 'ds1': +1, 'ds2': +1},   # symmetric dd
    'Xi0':     {'ss': +1, 'us': -1},                 # symmetric ss
    'Xi-':     {'ss': +1, 'ds': -1},                 # symmetric ss
    'Omega-':  {'ss1': +1, 'ss2': +1, 'ss3': +1},  # all symmetric
}

# For the three-body model, the damping modification comes from
# the PRODUCT of phase factors times Gamma ratios
#
# R = 1 + sum_pairs sigma_ij * f(Gamma_i, Gamma_j, Gamma_k)
#
# where f encodes how much each pair's symmetry affects the damping

print("  Three-body interference model:")
print("  R = 1 + A * sum(sigma_ij * g_ij)")
print("  where g_ij encodes the Gamma-dependent pair weight")
print()

# Let's think about this differently.
# The R values cluster into groups:
# Group 1: R ≈ 1 (pure flavor: p, n, Omega)
# Group 2: R >> 1 (Lambda ≈ 4.7, Xi ≈ 6)
# Group 3: R < 1 (Sigma ≈ 0.5-0.9)
#
# The pattern is:
# - Antisymmetric cross-flavor pairs AMPLIFY damping
# - Symmetric same-flavor pairs don't modify damping
# - The amplification scales with Gamma_s/Gamma_u

# New model: the three-body correction to damping
# delta_lambda / lambda = sum over pairs: sigma_ij * w(Gamma_i, Gamma_j)
# where w is a weight function

# For pure flavor (all sigmas = +1, all Gammas equal):
# delta_lambda / lambda = 3 * w(G, G) -- should be ≈ 0

# For Lambda (all sigma = -1):
# delta_lambda / lambda = -w(Gu,Gd) - w(Gu,Gs) - w(Gd,Gs)

# The DIFFERENCE between Lambda and Sigma0 (both uds):
# Lambda:  sigma_ud=-1, sigma_us=-1, sigma_ds=-1
# Sigma0:  sigma_ud=+1, sigma_us=-1, sigma_ds=-1
# Difference: 2 * w(Gu, Gd) = (R_Lambda - R_Sigma0) * lambda
#
# R_Lambda - R_Sigma0 = 4.737 - 0.713 = 4.024
# So 2 * w(Gu, Gd) = 4.024
# w(Gu, Gd) = 2.012

# The DIFFERENCE between Sigma+ and Sigma-:
# Sigma+ (uus): sigma_uu=+1, sigma_us=+1, sigma_us=+1
# Sigma- (dds): sigma_dd=+1, sigma_ds=+1, sigma_ds=+1
# Both have 3 symmetric pairs, but with different Gammas (us vs ds)
# Delta R = 0.879 - 0.467 = 0.412

# Let me be more systematic. Define:
# R = 1 + delta, where delta = sum_{pairs} sigma_ij * w_ij
# w_ij depends on (Gamma_i, Gamma_j)

# We have 6 possible pair types: uu, ud, us, dd, ds, ss
# But same-flavor pairs in PURE baryons have sigma=+1 and should give w≈0
# So the weight function satisfies: w(G,G) ≈ 0

# This means w depends on the DIFFERENCE between Gammas!
# w(Ga, Gb) ≈ c * |Ga - Gb| / (Ga + Gb) * something

print("  SYSTEMATIC EXTRACTION OF PAIR WEIGHTS")
print("  ======================================")
print()
print("  From Lambda vs Sigma0 (both uds, only ud phase differs):")
R_Lam = R_exact['Lambda']
R_Sig0 = R_exact['Sigma0']
w_ud = (R_Lam - R_Sig0) / 2.0  # because sigma_ud flips from -1 to +1
print(f"    2 * w_ud = R_Lambda - R_Sigma0 = {R_Lam - R_Sig0:.6f}")
print(f"    w_ud = {w_ud:.6f}")
print()

# Now from Lambda: R_Lambda = 1 + (-1)*w_ud + (-1)*w_us + (-1)*w_ds
# But wait, this doesn't work because R_Lambda ≈ 4.74, not small
# Better formulation: R - 1 = sum sigma_ij * w_ij

# Actually let me reconsider. R includes the "base" damping.
# For pure flavor baryons (proton, omega), R ≈ 1 but not exactly 1.
# proton R = 1.286, not 1. Neutron R = 1.202. Omega R = 1.030.

# So the "base" R for same-flavor pairs is NOT zero.
# The proton has 3 pairs: uu, ud, ud (all sigma=+1)
# R_p = 1 + w_uu + 2*w_ud_sym

# Hmm, but we defined w_ud from Lambda/Sigma as the CROSS-FLAVOR effect.
# The proton has u-d pairs that are same-flavor-like (Gu ≈ Gd).

# Let me redefine more carefully.
# For each baryon with quarks q1, q2, q3 and phases sigma_12, sigma_13, sigma_23:
# R - 1 = sigma_12 * w(G1, G2) + sigma_13 * w(G1, G3) + sigma_23 * w(G2, G3)
# where w(Ga, Gb) is the pair weight function.

# Since Gamma_u ≈ Gamma_d, we have:
# w(Gu, Gu) ≈ w(Gu, Gd) ≈ w(Gd, Gd) = w_light
# w(Gu, Gs) ≈ w(Gd, Gs) = w_heavy
# w(Gs, Gs) = w_ss

# Three unknowns: w_light, w_heavy, w_ss

# Equations (using sigma phases):
# proton (uud, all +1):  R_p - 1 = 3 * w_light
# Omega (sss, all +1):   R_O - 1 = 3 * w_ss
# Lambda (uds, all -1):  R_L - 1 = -w_light - w_heavy - w_heavy = -w_light - 2*w_heavy
# Sigma+ (uus, all +1):  R_S+ - 1 = w_light + 2*w_heavy
# Sigma0 (uds, +,-,-):   R_S0 - 1 = w_light - 2*w_heavy
# Xi0 (uss, +,-):         R_X0 - 1 = 2*w_ss + (-1)*w_heavy... wait

# I need to be more careful about which pairs have which phases.
# Let me enumerate properly.

print()
print("="*80)
print("PART 2: SYSTEMATIC THREE-BODY MODEL")
print("="*80)
print()
print("  Model: R - 1 = sum_{pairs} sigma_ij * w(Gamma_i, Gamma_j)")
print("  Three weight types: w_ll (light-light), w_ls (light-strange), w_ss (s-s)")
print()

# Phase assignments for each baryon
# Format: list of (pair_type, sigma) where pair_type is 'll', 'ls', or 'ss'
baryon_phases = {
    'proton':  [('ll', +1), ('ll', +1), ('ll', +1)],     # uu(+1), ud(+1), ud(+1)
    'neutron': [('ll', +1), ('ll', +1), ('ll', +1)],     # dd(+1), ud(+1), ud(+1)
    'Lambda':  [('ll', -1), ('ls', -1), ('ls', -1)],     # ud(-1), us(-1), ds(-1)
    'Sigma+':  [('ll', +1), ('ls', +1), ('ls', +1)],     # uu(+1), us(+1), us(+1)
    'Sigma0':  [('ll', +1), ('ls', -1), ('ls', -1)],     # ud(+1), us(-1), ds(-1)
    'Sigma-':  [('ll', +1), ('ls', +1), ('ls', +1)],     # dd(+1), ds(+1), ds(+1)
    'Xi0':     [('ss', +1), ('ls', -1), ('ls', -1)],     # ss(+1), us(-1), us(-1) -- wait
    'Xi-':     [('ss', +1), ('ls', -1), ('ls', -1)],     # ss(+1), ds(-1), ds(-1) -- wait
    'Omega-':  [('ss', +1), ('ss', +1), ('ss', +1)],     # ss(+1), ss(+1), ss(+1)
}

# Wait — I need to think about Xi phases more carefully.
# Xi0 = uss. The ss pair is symmetric (+1). But what about the us pairs?
# In the octet, Xi has mixed symmetry. The strange quarks form a symmetric pair,
# and the light quark is the "odd one out."
# From our previous exhaustive search, the best phases for Xi0 were us=-1.
# So both us pairs have sigma=-1.

# Hmm but actually there's a subtlety. In the proton (uud), the two u quarks
# are identical, so uu must be symmetric. The ud pair symmetry comes from the
# overall wavefunction requirement.
#
# For the octet proton: the flavor wavefunction is mixed symmetry.
# The two u's are symmetric under exchange. The u-d pair has a specific
# symmetry determined by the SU(6) Clebsch-Gordan coefficients.
#
# Actually, for our purposes, the key question is: what sigma values
# reproduce the R data?

# Let me just parameterize and solve.
# Define coefficients: for each baryon, n_ll_plus, n_ll_minus, n_ls_plus, n_ls_minus, n_ss_plus, n_ss_minus
# Then R - 1 = (n_ll+ - n_ll-) * w_ll + (n_ls+ - n_ls-) * w_ls + (n_ss+ - n_ss-) * w_ss

# This gives us 9 equations in 3 unknowns.

# From the phase assignments above:
# proton:   3*w_ll + 0*w_ls + 0*w_ss
# neutron:  3*w_ll + 0*w_ls + 0*w_ss  (same as proton since Gu≈Gd)
# Lambda:   -1*w_ll - 2*w_ls + 0*w_ss
# Sigma+:   1*w_ll + 2*w_ls + 0*w_ss
# Sigma0:   1*w_ll - 2*w_ls + 0*w_ss
# Sigma-:   1*w_ll + 2*w_ls + 0*w_ss  (same as Sigma+ since Gu≈Gd)
# Xi0:      0*w_ll - 2*w_ls + 1*w_ss
# Xi-:      0*w_ll - 2*w_ls + 1*w_ss  (same as Xi0 since Gu≈Gd)
# Omega:    0*w_ll + 0*w_ls + 3*w_ss

# Using Gu=Gd approximation, we have 5 independent equations:
# proton:   3*w_ll = R_p - 1
# Lambda:   -w_ll - 2*w_ls = R_L - 1
# Sigma+:   w_ll + 2*w_ls = R_S+ - 1
# Sigma0:   w_ll - 2*w_ls = R_S0 - 1
# Xi0:      -2*w_ls + w_ss = R_X0 - 1
# Omega:    3*w_ss = R_O - 1

# From proton: w_ll = (R_p - 1)/3
# From Omega: w_ss = (R_O - 1)/3
# From Sigma0: w_ll - 2*w_ls = R_S0 - 1 => w_ls = (w_ll - (R_S0 - 1))/2

R_p = R_exact['proton']
R_n = R_exact['neutron']
R_L = R_exact['Lambda']
R_Sp = R_exact['Sigma+']
R_S0 = R_exact['Sigma0']
R_Sm = R_exact['Sigma-']
R_X0 = R_exact['Xi0']
R_Xm = R_exact['Xi-']
R_O = R_exact['Omega-']

w_ll = (R_p - 1) / 3
w_ss = (R_O - 1) / 3
w_ls_from_S0 = (w_ll - (R_S0 - 1)) / 2

print(f"  From proton: w_ll = (R_p - 1)/3 = ({R_p:.6f} - 1)/3 = {w_ll:.6f}")
print(f"  From Omega:  w_ss = (R_O - 1)/3 = ({R_O:.6f} - 1)/3 = {w_ss:.6f}")
print(f"  From Sigma0: w_ls = (w_ll - (R_S0 - 1))/2 = {w_ls_from_S0:.6f}")
print()

# Now verify against ALL baryons
print("  Verification of 3-weight model (w_ll, w_ls, w_ss):")
print(f"  w_ll = {w_ll:.6f}, w_ls = {w_ls_from_S0:.6f}, w_ss = {w_ss:.6f}")
print()

# Predict R for each baryon
predictions_3w = {}
# proton: 3*w_ll
predictions_3w['proton'] = 1 + 3*w_ll
predictions_3w['neutron'] = 1 + 3*w_ll  # same in Gu=Gd approx
predictions_3w['Lambda'] = 1 + (-1)*w_ll + (-2)*w_ls_from_S0
predictions_3w['Sigma+'] = 1 + 1*w_ll + 2*w_ls_from_S0
predictions_3w['Sigma0'] = 1 + 1*w_ll + (-2)*w_ls_from_S0
predictions_3w['Sigma-'] = 1 + 1*w_ll + 2*w_ls_from_S0
predictions_3w['Xi0'] = 1 + (-2)*w_ls_from_S0 + 1*w_ss
predictions_3w['Xi-'] = 1 + (-2)*w_ls_from_S0 + 1*w_ss
predictions_3w['Omega-'] = 1 + 3*w_ss

print(f"  {'Baryon':<10} {'R_exact':>10} {'R_pred':>10} {'Error':>10}")
max_R_err = 0
for name, quarks, I, S, Y, n_s, mass in baryons:
    R_ex = R_exact[name]
    R_pr = predictions_3w[name]
    err = (R_pr - R_ex) / R_ex * 100
    max_R_err = max(max_R_err, abs(err))
    print(f"  {name:<10} {R_ex:10.6f} {R_pr:10.6f} {err:+10.4f}%")

print(f"\n  Max R error: {max_R_err:.4f}%")

# Now compute mass predictions
print(f"\n  Mass predictions from 3-weight model:")
print(f"  {'Baryon':<10} {'M_pred':>10} {'M_actual':>10} {'Error':>10}")
max_M_err = 0
for name, quarks, I, S, Y, n_s, mass in baryons:
    gammas = get_gammas(quarks)
    sum_g2 = sum(g**2 for g in gammas)
    R_pr = predictions_3w[name]
    M_pred = sum_g2 * (1 - lambda_0 * R_pr)**2
    err = (M_pred - mass) / mass * 100
    max_M_err = max(max_M_err, abs(err))
    print(f"  {name:<10} {M_pred:10.2f} {mass:10.2f} {err:+10.4f}%")

print(f"\n  Max mass error: {max_M_err:.4f}%")

# Now look for structural fractions in the weights
print()
print("  STRUCTURAL ANALYSIS OF WEIGHTS:")
print(f"  w_ll = {w_ll:.6f}")
print(f"  w_ls = {w_ls_from_S0:.6f}")
print(f"  w_ss = {w_ss:.6f}")
print()
print(f"  w_ls / w_ll = {w_ls_from_S0/w_ll:.6f}")
print(f"  w_ss / w_ll = {w_ss/w_ll:.6f}")
print(f"  w_ls / w_ss = {w_ls_from_S0/w_ss:.6f}")
print()

# Search for rational approximations
from fractions import Fraction
for name, val in [('w_ll', w_ll), ('w_ls', w_ls_from_S0), ('w_ss', w_ss)]:
    frac = Fraction(val).limit_denominator(200)
    print(f"  {name} = {val:.6f} ≈ {frac} = {float(frac):.6f} (error {abs(float(frac)-val)/abs(val)*100:.3f}%)")

for name, val in [('w_ls/w_ll', w_ls_from_S0/w_ll), ('w_ss/w_ll', w_ss/w_ll), ('w_ls/w_ss', w_ls_from_S0/w_ss)]:
    frac = Fraction(val).limit_denominator(100)
    print(f"  {name} = {val:.6f} ≈ {frac} = {float(frac):.6f} (error {abs(float(frac)-val)/abs(val)*100:.3f}%)")


print()
print("="*80)
print("PART 3: BREAKING Gu=Gd DEGENERACY")
print("="*80)
print()
print("  The 3-weight model assumes Gu = Gd. But n-p splitting exists.")
print("  Need to break the degeneracy. Use 4 weights:")
print("  w_uu, w_ud, w_us (=w_ds), w_ss")
print("  Or equivalently: w_ll + delta_w for uu vs ud")
print()

# Now with Gu != Gd (introduce delta_G = Gd - Gu)
# From the proton and neutron difference:
# proton (uud): R_p = 1 + w_uu + 2*w_ud
# neutron (udd): R_n = 1 + w_dd + 2*w_ud (if Gu=Gd then R_p=R_n but they differ)
# The difference comes from BOTH the weight splitting AND the Gamma splitting.

# Actually if Gu ≈ Gd, the main effect is Gamma splitting.
# Let me compute R with EXACT Gammas first.

# For n-p splitting, introduce Gd = 25 + delta
# From cuft-final.py, best fit was Gd = Gu + 1/19 ≈ 25.0526
delta_G = 1.0/19.0
Gd_exact = Gamma_u + delta_G

# Recompute R values with exact Gammas including Gd splitting
R_exact_split = {}
for name, quarks, I, S, Y, n_s, mass in baryons:
    gammas = []
    for q in quarks:
        if q == 'u': gammas.append(Gamma_u)
        elif q == 'd': gammas.append(Gd_exact)
        elif q == 's': gammas.append(Gamma_s)
    sum_g2 = sum(g**2 for g in gammas)
    R = (1 - np.sqrt(mass / sum_g2)) / lambda_0
    R_exact_split[name] = R

print("  R values with Gd = 25 + 1/19:")
print(f"  {'Baryon':<10} {'R(Gu=Gd)':>10} {'R(Gd=25+1/19)':>13} {'Diff':>10}")
for name in [b[0] for b in baryons]:
    R1 = R_exact[name]
    R2 = R_exact_split[name]
    print(f"  {name:<10} {R1:10.6f} {R2:13.6f} {R2-R1:10.6f}")

# The splitting is tiny — let's continue with the Gu=Gd model first and
# fix the BIG errors before worrying about 0.08% n-p effects

print()
print("="*80)
print("PART 4: THE OVERCONSTRAINED SYSTEM — CONSISTENCY CHECK")
print("="*80)
print()
print("  With 3 weights (w_ll, w_ls, w_ss) and the Gu=Gd approximation,")
print("  we used 3 equations (proton, Sigma0, Omega) to fix the weights.")
print("  The remaining 6 baryons are PREDICTIONS.")
print()
print("  But we have OVERCONSTRAINED data! Check consistency:")
print()

# Check: Lambda should give R_L = 1 - w_ll - 2*w_ls
R_L_pred = 1 + (-1)*w_ll + (-2)*w_ls_from_S0
print(f"  Lambda:  predicted R = {R_L_pred:.6f}, actual R = {R_L:.6f}, error = {(R_L_pred-R_L)/R_L*100:+.4f}%")

# Check: Sigma+ should give R_S+ = 1 + w_ll + 2*w_ls
R_Sp_pred = 1 + w_ll + 2*w_ls_from_S0
print(f"  Sigma+:  predicted R = {R_Sp_pred:.6f}, actual R = {R_Sp:.6f}, error = {(R_Sp_pred-R_Sp)/R_Sp*100:+.4f}%")

# Check: Lambda + Sigma0 = 2 (from the model: -w_ll - 2w_ls + w_ll - 2w_ls + 2 = 2 - 4w_ls)
# Wait: R_Lambda + R_Sigma0 = (1 - w_ll - 2*w_ls) + (1 + w_ll - 2*w_ls) = 2 - 4*w_ls
sum_LS = R_L + R_S0
print(f"\n  Lambda + Sigma0 = {sum_LS:.6f} = 2 - 4*w_ls = {2 - 4*w_ls_from_S0:.6f}")
print(f"  Model predicts: w_ls = (2 - (R_L + R_S0))/4 = {(2 - sum_LS)/4:.6f}")
print(f"  From Sigma0: w_ls = {w_ls_from_S0:.6f}")
# These should agree!

# Also check: Lambda - Sigma0 = -2*w_ll
diff_LS = R_L - R_S0
print(f"\n  Lambda - Sigma0 = {diff_LS:.6f}")
print(f"  Model predicts: -2*w_ll = {-2*w_ll:.6f}")
print(f"  Error: {(diff_LS - (-2*w_ll))/diff_LS*100:.4f}%")

# Check: Sigma+ - Sigma0 = 4*w_ls
diff_SpS0 = R_Sp - R_S0
print(f"\n  Sigma+ - Sigma0 = {diff_SpS0:.6f}")
print(f"  Model predicts: 4*w_ls = {4*w_ls_from_S0:.6f}")
print(f"  Error: {(diff_SpS0 - 4*w_ls_from_S0)/diff_SpS0*100:+.4f}%")

# This IS the real test. If Sigma+ - Sigma0 = 4*w_ls from the Sigma0 equation,
# and Lambda + Sigma0 = 2 - 4*w_ls, then LAMBDA IS PREDICTED.
# And if Sigma+ matches, that's 4/9 constraints satisfied by 3 params.

# The KEY constraint violations tell us WHERE the model breaks:
print()
print("  CONSTRAINT VIOLATIONS (what the 3-weight model gets wrong):")
# Sigma+ vs Sigma-: should be equal (both have w_ll + 2*w_ls) since Gu≈Gd
print(f"  Sigma+ R = {R_Sp:.6f}, Sigma- R = {R_Sm:.6f}, diff = {R_Sp - R_Sm:.6f}")
print(f"  -> Gu≠Gd effect or charge-dependent coupling")

# Xi0 vs Xi-: should be equal
print(f"  Xi0 R = {R_X0:.6f}, Xi- R = {R_Xm:.6f}, diff = {R_X0 - R_Xm:.6f}")
print(f"  -> Same Gu≠Gd effect")

# proton vs neutron:
print(f"  proton R = {R_p:.6f}, neutron R = {R_n:.6f}, diff = {R_p - R_n:.6f}")


print()
print("="*80)
print("PART 5: THE ISOSPIN-CORRECTED MODEL")
print("="*80)
print()
print("  Add isospin correction: R = R_3weight + delta_I * I_z_correction")
print("  where I_z_correction distinguishes u from d quarks")
print()

# The 3-weight model predicts the AVERAGE of charge multiplets perfectly.
# The splitting within multiplets comes from Gu != Gd.
#
# For the mass formula with Gu != Gd:
# M = sum_i Gamma_i^2 * (1 - lambda * R)^2
# When Gd = Gu + delta, the masses shift proportionally to (n_d - n_u) * delta * Gu

# But R itself could also depend on (n_u - n_d) through the couplings.
# Let me add a 4th parameter: w_charge that couples to (n_u - n_d)

# R = 1 + sum sigma_ij * w_type + w_charge * (n_u - n_d) / 3

# From proton (n_u=2, n_d=1): R_p = 1 + 3*w_ll + w_charge * 1/3
# From neutron (n_u=1, n_d=2): R_n = 1 + 3*w_ll - w_charge * 1/3
# Average: R_avg = 1 + 3*w_ll (unchanged)
# Difference: R_p - R_n = 2/3 * w_charge

w_charge = (R_p - R_n) / (2.0/3.0)
print(f"  w_charge = (R_p - R_n) / (2/3) = {w_charge:.6f}")
print()

# Now 4 weights: w_ll, w_ls, w_ss, w_charge
# proton:  1 + 3*w_ll + (1/3)*w_charge
# neutron: 1 + 3*w_ll - (1/3)*w_charge
# Lambda:  1 - w_ll - 2*w_ls + 0*w_charge (I_z = 0)
# Sigma+:  1 + w_ll + 2*w_ls + (1/3)*w_charge (n_u=2,n_d=0 -> (n_u-n_d)/3 = 2/3? no)

# Wait, I need to be careful. (n_u - n_d) for Sigma+ (uus) = 2-0 = 2
# For Sigma0 (uds) = 1-1 = 0
# For Sigma- (dds) = 0-2 = -2

# But actually isospin projection I_z = (n_u - n_d)/2
# So let's use I_z directly

# proton:  I_z = +1/2 -> coefficient = w_charge * I_z
# neutron: I_z = -1/2
# Sigma+:  I_z = +1
# Sigma0:  I_z = 0
# Sigma-:  I_z = -1
# Xi0:     I_z = +1/2
# Xi-:     I_z = -1/2

# R = 1 + pair_terms + w_Iz * I_z

w_Iz = (R_p - R_n)  # since Delta(I_z) = 1
# Actually: R_p has I_z = +1/2, R_n has I_z = -1/2
# R_p - R_n = w_Iz * (1/2 - (-1/2)) = w_Iz
w_Iz = R_p - R_n
print(f"  w_Iz = R_p - R_n = {w_Iz:.6f}")
print()

# Predictions with 4-weight model: w_ll, w_ls, w_ss, w_Iz
predictions_4w = {}
for name, quarks, I, S, Y, n_s, mass in baryons:
    if quarks in ['uud', 'udd']:
        n_ll_pos = 3
        n_ls_pos = 0; n_ls_neg = 0
        n_ss_pos = 0
    elif quarks == 'uds' and I == 0.0:  # Lambda
        n_ll_pos = 0; n_ll_neg = 1
        n_ls_neg = 2; n_ls_pos = 0
        n_ss_pos = 0
    elif quarks == 'uds' and I == 1.0:  # Sigma0
        n_ll_pos = 1; n_ll_neg = 0
        n_ls_neg = 2; n_ls_pos = 0
        n_ss_pos = 0
    elif quarks in ['uus', 'dds']:  # Sigma+, Sigma-
        n_ll_pos = 1; n_ll_neg = 0
        n_ls_pos = 2; n_ls_neg = 0
        n_ss_pos = 0
    elif quarks in ['uss', 'dss']:  # Xi
        n_ll_pos = 0; n_ll_neg = 0
        n_ls_neg = 2; n_ls_pos = 0
        n_ss_pos = 1
    elif quarks == 'sss':  # Omega
        n_ll_pos = 0; n_ll_neg = 0
        n_ls_pos = 0; n_ls_neg = 0
        n_ss_pos = 3
    else:
        continue

    # Compute I_z
    n_u = quarks.count('u')
    n_d = quarks.count('d')
    I_z = (n_u - n_d) / 2.0

    pair_ll = (n_ll_pos if 'n_ll_pos' in dir() else 0) - (n_ll_neg if 'n_ll_neg' in dir() else 0)
    # Recompute properly
    pass

# Let me just do this cleanly
def predict_R_4w(name, I_val, quarks, w_ll, w_ls, w_ss, w_Iz):
    n_u = quarks.count('u')
    n_d = quarks.count('d')
    n_s_q = quarks.count('s')
    I_z = (n_u - n_d) / 2.0

    # Pair structure based on SU(6)
    if name == 'proton':   pair_term = 3*w_ll
    elif name == 'neutron': pair_term = 3*w_ll
    elif name == 'Lambda':  pair_term = -w_ll - 2*w_ls
    elif name == 'Sigma+':  pair_term = w_ll + 2*w_ls
    elif name == 'Sigma0':  pair_term = w_ll - 2*w_ls
    elif name == 'Sigma-':  pair_term = w_ll + 2*w_ls
    elif name == 'Xi0':     pair_term = -2*w_ls + w_ss
    elif name == 'Xi-':     pair_term = -2*w_ls + w_ss
    elif name == 'Omega-':  pair_term = 3*w_ss
    else: return 1.0

    return 1 + pair_term + w_Iz * I_z

print("  4-weight model: R = 1 + pair_terms + w_Iz * I_z")
print(f"  w_ll = {w_ll:.6f}, w_ls = {w_ls_from_S0:.6f}, w_ss = {w_ss:.6f}, w_Iz = {w_Iz:.6f}")
print()
print(f"  {'Baryon':<10} {'R_exact':>10} {'R_pred':>10} {'R_err%':>10} {'M_pred':>10} {'M_actual':>10} {'M_err%':>10}")

max_M_err_4w = 0
for name, quarks, I, S, Y, n_s, mass in baryons:
    R_pr = predict_R_4w(name, I, quarks, w_ll, w_ls_from_S0, w_ss, w_Iz)
    R_ex = R_exact[name]
    R_err = (R_pr - R_ex) / R_ex * 100

    gammas = get_gammas(quarks)
    sum_g2 = sum(g**2 for g in gammas)
    M_pred = sum_g2 * (1 - lambda_0 * R_pr)**2
    M_err = (M_pred - mass) / mass * 100
    max_M_err_4w = max(max_M_err_4w, abs(M_err))
    print(f"  {name:<10} {R_ex:10.6f} {R_pr:10.6f} {R_err:+10.4f}% {M_pred:10.2f} {mass:10.2f} {M_err:+10.4f}%")

print(f"\n  Max mass error: {max_M_err_4w:.4f}%")

# The remaining errors come from:
# 1. Sigma+ vs Sigma-: model predicts same R but they differ (Gu != Gd effect)
# 2. Xi0 vs Xi-: same issue

# Now let's see what the ERRORS look like and whether they're explained
# by a 5th parameter that depends on n_s * I_z or something

print()
print("  RESIDUAL ANALYSIS (what's left after 4-weight model):")
residuals = {}
for name, quarks, I, S, Y, n_s, mass in baryons:
    R_pr = predict_R_4w(name, I, quarks, w_ll, w_ls_from_S0, w_ss, w_Iz)
    R_ex = R_exact[name]
    residuals[name] = R_ex - R_pr
    n_u = quarks.count('u')
    n_d = quarks.count('d')
    n_sq = quarks.count('s')
    I_z = (n_u - n_d) / 2.0
    print(f"  {name:<10} residual = {R_ex - R_pr:+.6f}  I={I}  I_z={I_z:+.1f}  n_s={n_sq}  Y={Y}")

# Look for patterns in residuals
# Sigma+: positive residual
# Sigma-: negative residual (equal magnitude?)
print(f"\n  Sigma+ + Sigma- residuals: {residuals['Sigma+'] + residuals['Sigma-']:.6f}")
print(f"  Sigma+ - Sigma- residuals: {residuals['Sigma+'] - residuals['Sigma-']:.6f}")
print(f"  Xi0 + Xi- residuals: {residuals['Xi0'] + residuals['Xi-']:.6f}")
print(f"  Xi0 - Xi- residuals: {residuals['Xi0'] - residuals['Xi-']:.6f}")


print()
print("="*80)
print("PART 6: OPTIMAL LEAST-SQUARES FIT WITH STRUCTURAL WEIGHTS")
print("="*80)
print()
print("  Fit the full R data with the minimum number of parameters")
print("  using a physics-motivated basis.")
print()

# Set up least-squares problem
# R_i = 1 + sum_k c_k * F_k(i)
# where F_k are basis functions of quantum numbers

# Define the feature matrix
features = []
labels = []
weights_data = []

for name, quarks, I, S, Y, n_s, mass in baryons:
    n_u = quarks.count('u')
    n_d = quarks.count('d')
    n_sq = quarks.count('s')
    I_z = (n_u - n_d) / 2.0
    R_ex = R_exact[name]

    # Pair symmetry sums
    # sigma_ll_net: +1 for symmetric ll, -1 for antisymmetric
    if name == 'proton':   s_ll, s_ls = 3, 0
    elif name == 'neutron': s_ll, s_ls = 3, 0
    elif name == 'Lambda':  s_ll, s_ls = -1, -2
    elif name == 'Sigma+':  s_ll, s_ls = 1, 2
    elif name == 'Sigma0':  s_ll, s_ls = 1, -2
    elif name == 'Sigma-':  s_ll, s_ls = 1, 2
    elif name == 'Xi0':     s_ll, s_ls = 0, -2
    elif name == 'Xi-':     s_ll, s_ls = 0, -2
    elif name == 'Omega-':  s_ll, s_ls = 0, 0

    s_ss = 3 if name == 'Omega-' else (1 if name in ['Xi0', 'Xi-'] else 0)

    # Build feature vector: [s_ll, s_ls, s_ss, I_z, n_s*I_z]
    features.append([s_ll, s_ls, s_ss, I_z, n_sq * I_z])
    labels.append(R_ex - 1)

F = np.array(features)
y = np.array(labels)

# Solve least squares
from numpy.linalg import lstsq
coeffs, residual, rank, sv = lstsq(F, y, rcond=None)

print("  5-parameter model: R - 1 = c1*s_ll + c2*s_ls + c3*s_ss + c4*I_z + c5*n_s*I_z")
print()
for i, name in enumerate(['s_ll (pair symmetry, light-light)',
                           's_ls (pair symmetry, light-strange)',
                           's_ss (pair symmetry, strange-strange)',
                           'I_z (isospin projection)',
                           'n_s * I_z (strangeness-isospin cross)']):
    print(f"  c_{i+1} = {coeffs[i]:+.6f}  [{name}]")

# Predict
print()
print(f"  {'Baryon':<10} {'R_exact':>10} {'R_pred':>10} {'R_err%':>10} {'M_pred':>10} {'M_actual':>10} {'M_err%':>10}")
max_M_err_5p = 0
for idx, (name, quarks, I, S, Y, n_s, mass) in enumerate(baryons):
    R_pr = 1 + F[idx] @ coeffs
    R_ex = R_exact[name]
    R_err = (R_pr - R_ex) / R_ex * 100

    gammas = get_gammas(quarks)
    sum_g2 = sum(g**2 for g in gammas)
    M_pred = sum_g2 * (1 - lambda_0 * R_pr)**2
    M_err = (M_pred - mass) / mass * 100
    max_M_err_5p = max(max_M_err_5p, abs(M_err))
    print(f"  {name:<10} {R_ex:10.6f} {R_pr:10.6f} {R_err:+10.4f}% {M_pred:10.2f} {mass:10.2f} {M_err:+10.4f}%")

print(f"\n  Max mass error: {max_M_err_5p:.4f}%")

# Look for structural fractions in the coefficients
print()
print("  STRUCTURAL FRACTIONS IN COEFFICIENTS:")
for i, (cname, c) in enumerate(zip(['c_ll', 'c_ls', 'c_ss', 'c_Iz', 'c_ns_Iz'], coeffs)):
    frac = Fraction(c).limit_denominator(100)
    print(f"  {cname} = {c:+.6f} ≈ {frac} = {float(frac):.6f} (error {abs(float(frac)-c)/abs(c)*100:.2f}%)")

# Ratios
print()
print("  Coefficient ratios:")
if abs(coeffs[0]) > 0:
    for i in range(1, len(coeffs)):
        ratio = coeffs[i] / coeffs[0]
        frac = Fraction(ratio).limit_denominator(50)
        names = ['c_ll', 'c_ls', 'c_ss', 'c_Iz', 'c_ns_Iz']
        print(f"  {names[i]}/{names[0]} = {ratio:.4f} ≈ {frac}")


print()
print("="*80)
print("PART 7: CONNECTION TO PHYSICAL CONSTANTS")
print("="*80)
print()
print("  The weights w_ll, w_ls, w_ss should be expressible in terms of")
print("  Gamma_u, Gamma_s, and lambda_0.")
print()

# Test: w = A * (Ga - Gb)^2 / (Ga * Gb) + B
# For w_ll (Ga = Gb = 25): w_ll = B
# For w_ls (Ga = 25, Gb = 100/3): w_ls = A * (25 - 100/3)^2 / (25 * 100/3) + B
# For w_ss (Ga = Gb = 100/3): w_ss = B (same as w_ll if this form)

# But w_ll != w_ss! So this form doesn't work.

# Try: w(Ga, Gb) = A * Ga * Gb / (Ga + Gb)^2 + B
# w_ll = A * 25*25 / (50)^2 + B = A/4 + B
# w_ss = A * (100/3)^2 / (200/3)^2 + B = A/4 + B ... same again

# Try: w depends on the TOTAL Gamma of the pair
# w(Ga, Gb) = A * (Ga + Gb) + B
# w_ll = A * 50 + B = 0.095365
# w_ss = A * 200/3 + B = 0.010036
# w_ls = A * (25 + 100/3) + B = A * 175/3 + B

# From w_ll and w_ss:
# 50A + B = 0.095365
# 66.667A + B = 0.010036
# => 16.667A = 0.010036 - 0.095365 = -0.085330
# A = -0.005120, B = 0.351365
A_sum = (w_ss - w_ll) / (200.0/3 - 50)
B_sum = w_ll - A_sum * 50
w_ls_pred_sum = A_sum * (25 + 100.0/3) + B_sum
print(f"  Linear in (Ga + Gb):")
print(f"  A = {A_sum:.6f}, B = {B_sum:.6f}")
print(f"  w_ls predicted = {w_ls_pred_sum:.6f}, actual = {w_ls_from_S0:.6f}")
print(f"  Error: {abs(w_ls_pred_sum - w_ls_from_S0)/abs(w_ls_from_S0)*100:.2f}%")
print()

# Try: w depends on Ga * Gb
# w_ll = A * 625 + B
# w_ss = A * (100/3)^2 + B = A * 10000/9 + B
# w_ls = A * 25 * 100/3 + B = A * 2500/3 + B

A_prod = (w_ss - w_ll) / (10000.0/9 - 625)
B_prod = w_ll - A_prod * 625
w_ls_pred_prod = A_prod * 2500.0/3 + B_prod
print(f"  Linear in (Ga * Gb):")
print(f"  A = {A_prod:.9f}, B = {B_prod:.6f}")
print(f"  w_ls predicted = {w_ls_pred_prod:.6f}, actual = {w_ls_from_S0:.6f}")
print(f"  Error: {abs(w_ls_pred_prod - w_ls_from_S0)/abs(w_ls_from_S0)*100:.2f}%")
print()

# Try: w = A * (Ga - Gb)^2 / (Ga + Gb)^2 + B * (Ga + Gb) / (Ga * Gb)
# This has the property that flavor-symmetric pairs get w = B/(G/2)
# and cross-flavor pairs get additional contribution from (Ga-Gb)

# Let's try the simplest: w = c / (1 + k * (Ga - Gb)^2 / (Ga * Gb))
# For same flavor: w = c (since Ga = Gb)
# But w_ll != w_ss...

# Different approach: w_type = w_base(Ga, Gb) where the type is determined by Gammas
# w_ll = f(25, 25)
# w_ls = f(25, 100/3)
# w_ss = f(100/3, 100/3)

# Key observation: w_ll >> w_ls > w_ss > 0
# And Gamma_u < Gamma_s
# So SMALLER Gamma pairs have LARGER weights
# w ~ 1/G^n ?

# Test: w = C / (Ga * Gb)
# w_ll = C / 625
# w_ls = C / (25 * 100/3) = C / 833.33
# w_ss = C / (100/3)^2 = C / 1111.11

# From w_ll: C = w_ll * 625 = 59.60
# w_ls_pred = 59.60 / 833.33 = 0.07152
# w_ss_pred = 59.60 / 1111.11 = 0.05364

C_inv_prod = w_ll * 625
w_ls_pred_inv = C_inv_prod / (25 * 100.0/3)
w_ss_pred_inv = C_inv_prod / (100.0/3)**2
print(f"  Inverse product: w = C / (Ga * Gb)")
print(f"  C = {C_inv_prod:.4f}")
print(f"  w_ls predicted = {w_ls_pred_inv:.6f}, actual = {w_ls_from_S0:.6f} (error {abs(w_ls_pred_inv-w_ls_from_S0)/abs(w_ls_from_S0)*100:.1f}%)")
print(f"  w_ss predicted = {w_ss_pred_inv:.6f}, actual = {w_ss:.6f} (error {abs(w_ss_pred_inv-w_ss)/abs(w_ss)*100:.1f}%)")
print()

# Not great. Try w = C / (Ga + Gb)^2
C_inv_sum2 = w_ll * 50**2
w_ls_pred_is2 = C_inv_sum2 / (25 + 100.0/3)**2
w_ss_pred_is2 = C_inv_sum2 / (200.0/3)**2
print(f"  Inverse square sum: w = C / (Ga + Gb)^2")
print(f"  C = {C_inv_sum2:.4f}")
print(f"  w_ls predicted = {w_ls_pred_is2:.6f}, actual = {w_ls_from_S0:.6f} (error {abs(w_ls_pred_is2-w_ls_from_S0)/abs(w_ls_from_S0)*100:.1f}%)")
print(f"  w_ss predicted = {w_ss_pred_is2:.6f}, actual = {w_ss:.6f} (error {abs(w_ss_pred_is2-w_ss)/abs(w_ss)*100:.1f}%)")
print()

# Try: w = A / Ga^2 + B / Gb^2 (separable)
# w_ll = 2A / 25^2 = 2A/625
# w_ls = A/625 + A/(100/3)^2 = A/625 + 9A/10000 = A(16/10000 + 9/10000) = A*25/10000 = A/400
# wait, that's not right
# w_ls = A/25^2 + A/(100/3)^2 = A/625 + 9A/10000 = A(16+9)/10000 = 25A/10000 = A/400
# w_ss = 2A/(100/3)^2 = 18A/10000 = 9A/5000

# Hmm wait, "A/Ga^2 + B/Gb^2" isn't symmetric unless A=B.
# If A=B: w = A * (1/Ga^2 + 1/Gb^2)
# w_ll = 2A/625
# w_ls = A*(1/625 + 9/10000) = A*(16/10000 + 9/10000) = 25A/10000 = A/400
# w_ss = 2A*9/10000 = 18A/10000 = 9A/5000

A_sep = w_ll * 625 / 2
w_ls_sep = A_sep / 400
w_ss_sep = 9 * A_sep / 5000
print(f"  Separable: w = A * (1/Ga² + 1/Gb²)")
print(f"  A = {A_sep:.4f}")
print(f"  w_ls predicted = {w_ls_sep:.6f}, actual = {w_ls_from_S0:.6f} (error {abs(w_ls_sep-w_ls_from_S0)/abs(w_ls_from_S0)*100:.1f}%)")
print(f"  w_ss predicted = {w_ss_sep:.6f}, actual = {w_ss:.6f} (error {abs(w_ss_sep-w_ss)/abs(w_ss)*100:.1f}%)")
print()

# Let's try a 2-parameter model for w
# w(Ga, Gb) = alpha / (Ga * Gb)^n
# Three equations, one unknown (n, then alpha from normalization)
# w_ll/w_ss = (Gs^2 / Gu^2)^n
ratio_ll_ss = w_ll / w_ss
print(f"  w_ll / w_ss = {ratio_ll_ss:.6f}")
print(f"  (Gs/Gu)^2 = {(Gamma_s/Gamma_u)**2:.6f}")
n_power = np.log(ratio_ll_ss) / np.log((Gamma_s/Gamma_u)**2)
print(f"  => n = {n_power:.4f} (for w ~ 1/(Ga*Gb)^n)")
print()

# Check with w_ls
# w_ll/w_ls = (Gu*Gs / Gu^2)^n = (Gs/Gu)^n
ratio_ll_ls = w_ll / w_ls_from_S0
n_from_ls = np.log(ratio_ll_ls) / np.log(Gamma_s/Gamma_u)
print(f"  w_ll / w_ls = {ratio_ll_ls:.6f}")
print(f"  (Gs/Gu) = {Gamma_s/Gamma_u:.6f}")
print(f"  => n = {n_from_ls:.4f} (from w_ll/w_ls)")
print()

# These n values should match if the model is correct
print(f"  n from w_ll/w_ss: {n_power:.4f}")
print(f"  n from w_ll/w_ls: {n_from_ls:.4f}")
print(f"  Match: {'YES' if abs(n_power - n_from_ls) < 0.05 else 'NO'} (diff = {abs(n_power - n_from_ls):.4f})")


print()
print("="*80)
print("PART 8: THE COMPLETE 5-PARAMETER DERIVATION")
print("="*80)
print()

# Let me try the most elegant model.
# The mass formula is:
# M_baryon = Sum_i Gamma_i^2 * (1 - lambda * R)^2
#
# R = 1 + sum_{pairs} sigma_ij * w(Gamma_i, Gamma_j) + w_Iz * I_z
#
# If w(Ga, Gb) has 2 parameters (alpha, n):
#   w(Ga, Gb) = alpha / (Ga * Gb)^n
# Plus w_Iz, that's 3 free parameters total.
# But Gamma_u, Gamma_s, and lambda are DERIVED (from proton formula).
# So this is a 3-parameter model for the FULL 9-baryon spectrum!

# Let me fit it optimally
from scipy.optimize import minimize

def model_mass(params, baryon_data, return_details=False):
    alpha, n, w_iz = params
    predictions = []
    for name, quarks, I, S, Y, n_s, mass in baryon_data:
        gammas = get_gammas(quarks)
        sum_g2 = sum(g**2 for g in gammas)

        n_u = quarks.count('u')
        n_d = quarks.count('d')
        I_z = (n_u - n_d) / 2.0

        # Pair weights
        pairs = [(gammas[0], gammas[1]), (gammas[0], gammas[2]), (gammas[1], gammas[2])]

        # Phase assignments
        if name == 'proton':   sigmas = [+1, +1, +1]
        elif name == 'neutron': sigmas = [+1, +1, +1]
        elif name == 'Lambda':  sigmas = [-1, -1, -1]
        elif name == 'Sigma+':  sigmas = [+1, +1, +1]
        elif name == 'Sigma0':  sigmas = [+1, -1, -1]
        elif name == 'Sigma-':  sigmas = [+1, +1, +1]
        elif name == 'Xi0':     sigmas = [+1, -1, -1]
        elif name == 'Xi-':     sigmas = [+1, -1, -1]
        elif name == 'Omega-':  sigmas = [+1, +1, +1]

        R = 1.0
        for (Ga, Gb), sigma in zip(pairs, sigmas):
            w = alpha / (Ga * Gb)**n
            R += sigma * w
        R += w_iz * I_z

        M_pred = sum_g2 * (1 - lambda_0 * R)**2
        predictions.append(M_pred)

    if return_details:
        return predictions

    masses = [b[6] for b in baryon_data]
    errors = [(p - m)/m for p, m in zip(predictions, masses)]
    return max(abs(e) for e in errors)

from scipy.optimize import differential_evolution

# Optimize
bounds = [(0, 200), (0.5, 3.0), (-0.5, 0.5)]
result = differential_evolution(lambda p: model_mass(p, baryons), bounds, seed=42, maxiter=1000, tol=1e-12)

alpha_opt, n_opt, wIz_opt = result.x
print(f"  OPTIMAL 3-PARAM POWER-LAW MODEL:")
print(f"  alpha = {alpha_opt:.6f}")
print(f"  n = {n_opt:.6f}")
print(f"  w_Iz = {wIz_opt:.6f}")
print(f"  Max error: {result.fun*100:.4f}%")
print()

# Verify
preds = model_mass(result.x, baryons, return_details=True)
print(f"  {'Baryon':<10} {'M_pred':>10} {'M_actual':>10} {'Error':>10}")
for (name, quarks, I, S, Y, n_s, mass), M_pred in zip(baryons, preds):
    err = (M_pred - mass) / mass * 100
    print(f"  {name:<10} {M_pred:10.2f} {mass:10.2f} {err:+10.4f}%")

# Now try with the 3-weight model exactly (no power law assumption)
# This is 4 parameters: w_ll, w_ls, w_ss, w_Iz
print()
print()

def model_mass_4w(params, baryon_data, return_details=False):
    w_ll, w_ls, w_ss, w_iz = params
    predictions = []
    for name, quarks, I, S, Y, n_s, mass in baryon_data:
        gammas = get_gammas(quarks)
        sum_g2 = sum(g**2 for g in gammas)

        n_u = quarks.count('u')
        n_d = quarks.count('d')
        I_z = (n_u - n_d) / 2.0

        R = predict_R_4w(name, I, quarks, w_ll, w_ls, w_ss, w_iz)

        M_pred = sum_g2 * (1 - lambda_0 * R)**2
        predictions.append(M_pred)

    if return_details:
        return predictions

    masses = [b[6] for b in baryon_data]
    errors = [(p - m)/m for p, m in zip(predictions, masses)]
    return max(abs(e) for e in errors)

bounds_4w = [(-1, 1), (-5, 5), (-1, 1), (-1, 1)]
result_4w = differential_evolution(lambda p: model_mass_4w(p, baryons), bounds_4w, seed=42, maxiter=1000, tol=1e-12)

w_ll_opt, w_ls_opt, w_ss_opt, wIz_opt4 = result_4w.x
print(f"  OPTIMAL 4-PARAM (w_ll, w_ls, w_ss, w_Iz):")
print(f"  w_ll = {w_ll_opt:.6f}")
print(f"  w_ls = {w_ls_opt:.6f}")
print(f"  w_ss = {w_ss_opt:.6f}")
print(f"  w_Iz = {wIz_opt4:.6f}")
print(f"  Max error: {result_4w.fun*100:.4f}%")
print()

preds_4w = model_mass_4w(result_4w.x, baryons, return_details=True)
print(f"  {'Baryon':<10} {'M_pred':>10} {'M_actual':>10} {'Error':>10}")
for (name, quarks, I, S, Y, n_s, mass), M_pred in zip(baryons, preds_4w):
    err = (M_pred - mass) / mass * 100
    print(f"  {name:<10} {M_pred:10.2f} {mass:10.2f} {err:+10.4f}%")

# Structural fractions for optimal weights
print()
print("  STRUCTURAL FRACTIONS (optimal weights):")
for cname, c in [('w_ll', w_ll_opt), ('w_ls', w_ls_opt), ('w_ss', w_ss_opt), ('w_Iz', wIz_opt4)]:
    frac = Fraction(c).limit_denominator(100)
    print(f"  {cname} = {c:+.6f} ≈ {frac}")

# Ratios
if abs(w_ll_opt) > 0.001:
    print()
    print("  Weight ratios:")
    for cname, c in [('w_ls/w_ll', w_ls_opt/w_ll_opt), ('w_ss/w_ll', w_ss_opt/w_ll_opt)]:
        frac = Fraction(c).limit_denominator(50)
        print(f"  {cname} = {c:.4f} ≈ {frac}")


print()
print("="*80)
print("PART 9: THE FINAL MODEL — CONNECTING EVERYTHING")
print("="*80)
print()

# The complete CUFT-RASP baryon mass formula is:
#
# M_baryon / m_e = Sum_i Gamma_i^2 * (1 - lambda * R)^2
#
# where:
#   Gamma_u = 25, Gamma_d ≈ 25, Gamma_s = 100/3
#   lambda = alpha^2 * m_e/m_p (iterative) ≈ 0.008097
#   R = 1 + sum_pairs sigma_ij * w_type + w_Iz * I_z
#   w_ll, w_ls, w_ss = pair interference weights from SU(6) flavor-spin
#   sigma_ij = ±1 from baryon wavefunction symmetry
#
# With 0 free parameters (proton):   m_p/m_e = 60²/2 + 60(3/5) + 9/60 + lambda/3
# With 4 free parameters (spectrum): 9 baryons to ??? error

# Print the complete derivation chain
print("  ═══════════════════════════════════════════════════════════════")
print("  CUFT-RASP: COMPLETE BARYON MASS FORMULA")
print("  ═══════════════════════════════════════════════════════════════")
print()
print("  AXIOMS:")
print("  1. Recursion: f(x) = Gamma * tanh³(x) - lambda * x")
print("  2. lambda = alpha² * m_e/m_p (iterative) = 0.008097")
print("  3. Gamma_u = 5² = 25 (prime² gating coherence)")
print("     Gamma_s = (4/3) * Gamma_u = 100/3 (SU(3) breaking)")
print()
print("  PROTON (0 free parameters):")
print("  m_p/m_e = X²/2 + X(3/5) + 3²/X + lambda/3")
print("  where X = 3 * Gamma_u * (1 - 1/5) = 60")
print("  = 1800 + 36 + 0.15 + 0.002699 = 1836.152699")
print("  Error: 0.0000014%")
print()
print("  BARYON SPECTRUM (4 free parameters):")
print("  M_baryon = Sum_i Gamma_i² * (1 - lambda * R)²")
print(f"  R = 1 + Sum_pairs sigma_ij * w_type + {wIz_opt4:.6f} * I_z")
print(f"  w_ll = {w_ll_opt:.6f} (light-light pair interference)")
print(f"  w_ls = {w_ls_opt:.6f} (light-strange pair interference)")
print(f"  w_ss = {w_ss_opt:.6f} (strange-strange pair interference)")
print()

# COMPARE with standard GMO
print("  COMPARISON WITH GELL-MANN-OKUBO:")
print()
print("  | Model                        | Params | Max Error | Type     |")
print("  |------------------------------|--------|-----------|----------|")
print(f"  | CUFT proton formula          | 0      | 0.00%     | DERIVED  |")
print(f"  | CUFT 4-weight R model        | 4      | {result_4w.fun*100:.2f}%     | FIT      |")
print(f"  | CUFT 3-param power law       | 3      | {result.fun*100:.2f}%     | FIT      |")
print(f"  | Extended isospin (prev)      | 6      | 0.25%     | FIT      |")
print(f"  | Standard GMO                 | 3      | 1.62%     | EMPIRICAL|")
print(f"  | Extended GMO                 | 5      | 0.36%     | EMPIRICAL|")

# Try 5-param: add I(I+1) correction
print()
print()
print("  Testing 5-param: add I(I+1) correction...")

def model_mass_5w(params, baryon_data, return_details=False):
    w_ll, w_ls, w_ss, w_iz, w_ii = params
    predictions = []
    for name, quarks, I, S, Y, n_s, mass in baryon_data:
        gammas = get_gammas(quarks)
        sum_g2 = sum(g**2 for g in gammas)

        n_u = quarks.count('u')
        n_d = quarks.count('d')
        I_z = (n_u - n_d) / 2.0

        R = predict_R_4w(name, I, quarks, w_ll, w_ls, w_ss, w_iz)
        R += w_ii * I*(I+1)

        M_pred = sum_g2 * (1 - lambda_0 * R)**2
        predictions.append(M_pred)

    if return_details:
        return predictions

    masses = [b[6] for b in baryon_data]
    errors = [(p - m)/m for p, m in zip(predictions, masses)]
    return max(abs(e) for e in errors)

bounds_5w = [(-1, 1), (-5, 5), (-1, 1), (-1, 1), (-1, 1)]
result_5w = differential_evolution(lambda p: model_mass_5w(p, baryons), bounds_5w, seed=42, maxiter=2000, tol=1e-12)

print(f"  5-PARAM (+ I(I+1)): max error = {result_5w.fun*100:.4f}%")
print(f"  w_ll={result_5w.x[0]:.6f}, w_ls={result_5w.x[1]:.6f}, w_ss={result_5w.x[2]:.6f}")
print(f"  w_Iz={result_5w.x[3]:.6f}, w_I(I+1)={result_5w.x[4]:.6f}")
print()

preds_5w = model_mass_5w(result_5w.x, baryons, return_details=True)
print(f"  {'Baryon':<10} {'M_pred':>10} {'M_actual':>10} {'Error':>10}")
for (name, quarks, I, S, Y, n_s, mass), M_pred in zip(baryons, preds_5w):
    err = (M_pred - mass) / mass * 100
    print(f"  {name:<10} {M_pred:10.2f} {mass:10.2f} {err:+10.4f}%")

# Final: 6-param with n_s*I_z cross term
def model_mass_6w(params, baryon_data, return_details=False):
    w_ll, w_ls, w_ss, w_iz, w_ii, w_ns_iz = params
    predictions = []
    for name, quarks, I, S, Y, n_s, mass in baryon_data:
        gammas = get_gammas(quarks)
        sum_g2 = sum(g**2 for g in gammas)

        n_u = quarks.count('u')
        n_d = quarks.count('d')
        n_sq = quarks.count('s')
        I_z = (n_u - n_d) / 2.0

        R = predict_R_4w(name, I, quarks, w_ll, w_ls, w_ss, w_iz)
        R += w_ii * I*(I+1)
        R += w_ns_iz * n_sq * I_z

        M_pred = sum_g2 * (1 - lambda_0 * R)**2
        predictions.append(M_pred)

    if return_details:
        return predictions

    masses = [b[6] for b in baryon_data]
    errors = [(p - m)/m for p, m in zip(predictions, masses)]
    return max(abs(e) for e in errors)

bounds_6w = [(-1, 1), (-5, 5), (-1, 1), (-1, 1), (-1, 1), (-1, 1)]
result_6w = differential_evolution(lambda p: model_mass_6w(p, baryons), bounds_6w, seed=42, maxiter=2000, tol=1e-12)

print()
print(f"  6-PARAM (+ I(I+1) + n_s*I_z): max error = {result_6w.fun*100:.4f}%")
print(f"  w_ll={result_6w.x[0]:.6f}, w_ls={result_6w.x[1]:.6f}, w_ss={result_6w.x[2]:.6f}")
print(f"  w_Iz={result_6w.x[3]:.6f}, w_I(I+1)={result_6w.x[4]:.6f}, w_ns*Iz={result_6w.x[5]:.6f}")
print()

preds_6w = model_mass_6w(result_6w.x, baryons, return_details=True)
print(f"  {'Baryon':<10} {'M_pred':>10} {'M_actual':>10} {'Error':>10}")
max_err_6 = 0
for (name, quarks, I, S, Y, n_s, mass), M_pred in zip(baryons, preds_6w):
    err = (M_pred - mass) / mass * 100
    max_err_6 = max(max_err_6, abs(err))
    print(f"  {name:<10} {M_pred:10.2f} {mass:10.2f} {err:+10.4f}%")


print()
print("="*80)
print("FINAL COMPARISON TABLE")
print("="*80)
print()
print("  | Model                        | Params | Max Error | Type     |")
print("  |------------------------------|--------|-----------|----------|")
print(f"  | CUFT proton formula          | 0      | 0.0000%   | DERIVED  |")
print(f"  | CUFT 6-param R model         | 6      | {result_6w.fun*100:.4f}%  | FIT      |")
print(f"  | CUFT 5-param R model         | 5      | {result_5w.fun*100:.4f}%  | FIT      |")
print(f"  | CUFT 4-param R model         | 4      | {result_4w.fun*100:.4f}%  | FIT      |")
print(f"  | CUFT 3-param power law       | 3      | {result.fun*100:.4f}%  | FIT      |")
print(f"  | Extended isospin (prev)      | 6      | 0.2500%   | FIT      |")
print(f"  | Standard GMO                 | 3      | 1.6200%   | EMPIRICAL|")
print(f"  | Extended GMO                 | 5      | 0.3600%   | EMPIRICAL|")
print(f"  | Coupled oscillator (prev)    | 6      | 2.7100%   | FIT      |")
print()

# Check if the 3-weight model can be derived from the axioms
print("  WHAT THIS MEANS:")
print("  ─────────────────")
print("  The 4-weight R model is the PHYSICAL model (pair interference + I_z).")
print("  If the weights can be expressed as functions of Gamma_u, Gamma_s,")
print("  and lambda, then the entire 9-baryon spectrum is derived from")
print("  the SAME 3 axioms as the proton.")
print()
print("  The key is to derive w_ll, w_ls, w_ss from oscillator theory")
print("  and w_Iz from the Gu-Gd splitting (already known to be ~1/19).")
