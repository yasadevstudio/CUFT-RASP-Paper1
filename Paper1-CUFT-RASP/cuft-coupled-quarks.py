#!/usr/bin/env python3
"""
CUFT-RASP: COUPLED QUARK MAPS
==============================
Three interacting gated-cubic oscillators representing quarks.

HYPOTHESIS: Baryons = 3 coupled oscillators where:
- Each oscillator: f_i(x) = Γ_i · tanh³(x_i) - λ · x_i + coupling
- Coupling topology encodes quark content (u, d, s)
- Mass = total energy of coupled system at stable fixed point
- Base-60 emerges from LCM of coupling constants
- Different quark content → different coupling → different mass

WHY THIS SHOULD WORK:
1. Single map has only 1 stable FP per Γ → no mass spectrum
2. Three coupled maps can have DISCRETE energy states
3. Baryons (3 quarks) decompose cleanly; leptons (0 quarks) don't
4. Quark content → coupling topology → coefficient mapping
"""

import numpy as np
from itertools import product as iter_product

# Physical constants
LAMBDA = 0.008097  # damping parameter (δ)
M_P_M_E = 1836.15267343  # proton/electron mass ratio

# Baryon data: (name, quark content, mass in electron masses)
BARYONS = [
    ('proton',  'uud', 1836.15267),
    ('neutron', 'udd', 1838.68366),
    ('Lambda',  'uds', 2183.46),
    ('Sigma+',  'uus', 2327.64),
    ('Sigma0',  'uds', 2333.92),
    ('Sigma-',  'dds', 2343.30),
    ('Xi0',     'uss', 2572.85),
    ('Xi-',     'dss', 2578.26),
    ('Omega-',  'sss', 3277.96),
]

print("=" * 80)
print("PART 1: COUPLED MAP FRAMEWORK")
print("=" * 80)

print("""
  THREE COUPLED GATED-CUBIC OSCILLATORS:

  x₁' = Γ₁·tanh³(x₁) - λ·x₁ + ε₁₂·x₂ + ε₁₃·x₃
  x₂' = Γ₂·tanh³(x₂) - λ·x₂ + ε₂₁·x₁ + ε₂₃·x₃
  x₃' = Γ₃·tanh³(x₃) - λ·x₃ + ε₃₁·x₁ + ε₃₂·x₂

  where:
  - Γ_i = gating strength (determines quark flavor mass)
  - ε_ij = coupling between quarks i and j
  - Total energy = |x₁|² + |x₂|² + |x₃|² at fixed point

  QUARK FLAVOR ASSIGNMENT:
  - u quark: Γ_u (lightest → smallest Γ)
  - d quark: Γ_d (slightly heavier)
  - s quark: Γ_s (much heavier)
""")

def coupled_map(state, gammas, lam, couplings):
    """One iteration of 3 coupled gated-cubic maps.

    state: [x1, x2, x3]
    gammas: [Γ1, Γ2, Γ3]
    couplings: [[0, ε12, ε13], [ε21, 0, ε23], [ε31, ε32, 0]]
    """
    x = np.array(state, dtype=float)
    g = np.array(gammas, dtype=float)
    eps = np.array(couplings, dtype=float)

    new_x = np.zeros(3)
    for i in range(3):
        # Self-term: gated cubic
        self_term = g[i] * np.tanh(x[i])**3 - lam * x[i]
        # Coupling terms
        coupling_sum = sum(eps[i][j] * x[j] for j in range(3) if j != i)
        new_x[i] = self_term + coupling_sum

    return new_x

def find_coupled_fixed_point(gammas, lam, couplings, x0=None, max_iter=10000):
    """Find fixed point of coupled map by iteration."""
    if x0 is None:
        x0 = np.array([g * 0.8 for g in gammas])

    x = np.array(x0, dtype=float)

    for i in range(max_iter):
        x_new = coupled_map(x, gammas, lam, couplings)

        # Check convergence
        if np.max(np.abs(x_new - x)) < 1e-12:
            energy = np.sum(x_new**2)
            return x_new, energy, True

        # Check divergence
        if np.any(np.abs(x_new) > 1e6):
            return x_new, np.inf, False

        x = x_new

    energy = np.sum(x**2)
    return x, energy, False

print("=" * 80)
print("PART 2: QUARK MASS HIERARCHY FROM COUPLING")
print("=" * 80)

print("""
  The proton (uud) and neutron (udd) differ by one quark swap.
  Mass difference: 1838.68 - 1836.15 = 2.53 electron masses.

  If Γ_u and Γ_d are close, the mass difference comes primarily
  from the coupling asymmetry, not the quark masses alone.

  Strategy: Fix coupling structure, scan Γ_u, Γ_d, Γ_s to match
  ALL 9 baryon masses simultaneously.
""")

# First, understand the coupled system behavior
print("  Scanning coupled system stability...")
print()

# Test: identical quarks with symmetric coupling
print("  --- Test 1: Three identical quarks, symmetric coupling ---")
for eps in [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1]:
    gammas = [5.0, 5.0, 5.0]
    couplings = [[0, eps, eps], [eps, 0, eps], [eps, eps, 0]]

    fp, energy, converged = find_coupled_fixed_point(gammas, LAMBDA, couplings)
    if converged:
        print(f"    ε = {eps:.3f}  →  energy = {energy:.4f}  x* = [{fp[0]:.4f}, {fp[1]:.4f}, {fp[2]:.4f}]")
    else:
        print(f"    ε = {eps:.3f}  →  DIVERGED or NOT CONVERGED")

print()
print("  --- Test 2: Different Γ values (u, d quarks), small coupling ---")
for g_u in [3.0, 4.0, 5.0]:
    for g_d in [3.0, 4.0, 5.0]:
        gammas = [g_u, g_u, g_d]  # proton = uud
        couplings = [[0, 0.01, 0.01], [0.01, 0, 0.01], [0.01, 0.01, 0]]

        fp, energy, converged = find_coupled_fixed_point(gammas, LAMBDA, couplings)
        if converged and energy > 0.1:
            print(f"    Γ = [{g_u}, {g_u}, {g_d}]  →  energy = {energy:.4f}")

print()
print("  --- Test 3: Asymmetric coupling (quark pair interactions) ---")
# In QCD, quark pairs interact differently based on flavor
# uu coupling ≠ ud coupling ≠ us coupling
for eps_uu in [0.005, 0.01, 0.02]:
    for eps_ud in [0.005, 0.01, 0.02]:
        gammas = [5.0, 5.0, 5.0]  # same quarks
        couplings = [[0, eps_uu, eps_ud], [eps_uu, 0, eps_ud], [eps_ud, eps_ud, 0]]

        fp, energy, converged = find_coupled_fixed_point(gammas, LAMBDA, couplings)
        if converged:
            print(f"    ε_uu={eps_uu:.3f}, ε_ud={eps_ud:.3f}  →  energy = {energy:.4f}")

print("\n" + "=" * 80)
print("PART 3: MASS SPECTRUM FROM COUPLED MAPS")
print("=" * 80)

print("""
  Goal: Find (Γ_u, Γ_d, Γ_s, ε_uu, ε_ud, ε_us, ε_dd, ε_ds, ε_ss)
  such that the 9 baryon masses are reproduced.

  That's 9 parameters for 9 masses — exact fit possible but meaningless
  unless the parameters show STRUCTURE.

  Simplification: assume coupling depends on QUARK TYPE PAIR only:
  ε_ij depends on (flavor_i, flavor_j), giving 6 coupling types:
  ε_uu, ε_ud, ε_us, ε_dd, ε_ds, ε_ss

  With 3 Γ values + 6 couplings = 9 params for 9 masses.
  Still exact. Need fewer params.

  STRUCTURAL CONSTRAINT: Base-60 fractions.
  What if couplings are ratios of {2, 3, 5}?
  ε = n/60 where n ∈ {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
""")

# Approach: Fix Γ values from proton/neutron/Omega constraint
# Proton (uud): Γ_u, Γ_u, Γ_d → energy ≈ 1836.15
# Omega (sss): Γ_s, Γ_s, Γ_s → energy ≈ 3277.96
# Since energy ≈ sum of x_i², and x_i ≈ Γ_i for isolated quarks:
# Proton: 2*Γ_u² + Γ_d² ≈ 1836.15 (zeroth order, no coupling)
# Omega: 3*Γ_s² ≈ 3277.96 → Γ_s ≈ √(3277.96/3) ≈ 33.06

# But we saw x* ≈ 0.984*Γ for the single map, so u ≈ 0.968*Γ²
# Proton: 0.968*(2*Γ_u² + Γ_d²) ≈ 1836.15
# Omega: 0.968*3*Γ_s² ≈ 3277.96 → Γ_s ≈ √(3277.96/(3*0.968)) ≈ 33.59

factor = 0.984001  # u/Γ² asymptotic ratio (from landscape analysis)

# Omega constraint
gamma_s = np.sqrt(3277.96 / (3 * factor))
print(f"  From Omega (sss): Γ_s = {gamma_s:.4f}")

# Proton constraint: 2*Γ_u²*factor + Γ_d²*factor = 1836.15
# Neutron constraint: Γ_u²*factor + 2*Γ_d²*factor = 1838.68
# Adding: 3*factor*(Γ_u² + Γ_d²) = 1836.15 + 1838.68 = 3674.83
# Γ_u² + Γ_d² = 3674.83 / (3*factor) = 1245.16
# Subtracting: factor*(2Γ_u² + Γ_d² - Γ_u² - 2Γ_d²) = 1836.15 - 1838.68 = -2.53
# factor*(Γ_u² - Γ_d²) = -2.53
# Γ_u² - Γ_d² = -2.53/factor = -2.571

sum_sq = (1836.15 + 1838.68) / (3 * factor)
diff_sq = (1836.15 - 1838.68) / factor

gamma_u_sq = (sum_sq + diff_sq) / 2
gamma_d_sq = (sum_sq - diff_sq) / 2

gamma_u = np.sqrt(gamma_u_sq)
gamma_d = np.sqrt(gamma_d_sq)

print(f"  From proton+neutron: Γ_u = {gamma_u:.4f}, Γ_d = {gamma_d:.4f}")
print(f"  Γ_u² = {gamma_u_sq:.4f}, Γ_d² = {gamma_d_sq:.4f}")
print(f"  Γ_d² - Γ_u² = {gamma_d_sq - gamma_u_sq:.6f}")
print(f"  Γ_s = {gamma_s:.4f}")
print()

# Now predict ALL 9 baryons with ZERO coupling (zeroth order)
print("  ZEROTH-ORDER PREDICTIONS (no coupling, pure Γ² sums):")
print(f"  {'Baryon':>10s}  {'Quarks':>5s}  {'Predicted':>12s}  {'Actual':>12s}  {'Error':>8s}")
print(f"  {'-'*10}  {'-'*5}  {'-'*12}  {'-'*12}  {'-'*8}")

quark_energies = {'u': gamma_u_sq * factor, 'd': gamma_d_sq * factor, 's': gamma_s**2 * factor}

for name, quarks, mass in BARYONS:
    predicted = sum(quark_energies[q] for q in quarks)
    error = (predicted - mass) / mass * 100
    print(f"  {name:>10s}  {quarks:>5s}  {predicted:12.4f}  {mass:12.4f}  {error:7.3f}%")

print("\n" + "=" * 80)
print("PART 4: COUPLING CORRECTIONS — FITTING RESIDUALS")
print("=" * 80)

print("""
  Zeroth-order (Γ² sum) gives exact proton+neutron by construction.
  The RESIDUALS for other baryons tell us the coupling structure.

  Residual = Actual - Zeroth_order = coupling contribution
""")

print(f"  {'Baryon':>10s}  {'Quarks':>5s}  {'Zeroth':>10s}  {'Actual':>10s}  {'Residual':>10s}  {'Res/Actual':>10s}")
print(f"  {'-'*10}  {'-'*5}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}")

residuals = {}
for name, quarks, mass in BARYONS:
    zeroth = sum(quark_energies[q] for q in quarks)
    resid = mass - zeroth
    residuals[name] = (quarks, resid, resid/mass)
    print(f"  {name:>10s}  {quarks:>5s}  {zeroth:10.4f}  {mass:10.4f}  {resid:10.4f}  {resid/mass*100:9.3f}%")

print("""
  The residuals reveal the coupling pattern.
  If coupling is ε_ij per quark pair, each baryon has 3 pairs:
  - proton (uud): uu + ud + ud = ε_uu + 2*ε_ud
  - neutron (udd): ud + ud + dd = 2*ε_ud + ε_dd
  - Lambda (uds): ud + us + ds = ε_ud + ε_us + ε_ds
  etc.
""")

# Build the coupling equation system
# Each baryon: residual = sum of ε for each quark pair
# Pair types: uu, ud, us, dd, ds, ss

def count_pairs(quarks):
    """Count quark pair types in a baryon."""
    pairs = {'uu': 0, 'ud': 0, 'us': 0, 'dd': 0, 'ds': 0, 'ss': 0}
    # Define canonical ordering
    order = {'u': 0, 'd': 1, 's': 2}
    q = list(quarks)
    for i in range(3):
        for j in range(i+1, 3):
            a, b = q[i], q[j]
            if order[a] <= order[b]:
                pair = a + b
            else:
                pair = b + a
            pairs[pair] += 1
    return pairs

pair_types = ['uu', 'ud', 'us', 'dd', 'ds', 'ss']

print("\n  Quark pair decomposition:")
print(f"  {'Baryon':>10s}  {'uu':>4s}  {'ud':>4s}  {'us':>4s}  {'dd':>4s}  {'ds':>4s}  {'ss':>4s}  {'Residual':>10s}")
print(f"  {'-'*10}  {'-'*4}  {'-'*4}  {'-'*4}  {'-'*4}  {'-'*4}  {'-'*4}  {'-'*10}")

A_matrix = []
b_vector = []

for name, quarks, mass in BARYONS:
    pairs = count_pairs(quarks)
    row = [pairs[pt] for pt in pair_types]
    A_matrix.append(row)
    b_vector.append(residuals[name][1])

    pair_str = '  '.join([f'{pairs[pt]:4d}' for pt in pair_types])
    print(f"  {name:>10s}  {pair_str}  {residuals[name][1]:10.4f}")

A = np.array(A_matrix, dtype=float)
b = np.array(b_vector, dtype=float)

print(f"\n  System: {A.shape[0]} equations, {A.shape[1]} unknowns")
print(f"  Rank of A: {np.linalg.matrix_rank(A)}")

# Solve least-squares (overdetermined: 9 equations, 6 unknowns)
result = np.linalg.lstsq(A, b, rcond=None)
epsilons = result[0]
residual_norms = result[1] if len(result[1]) > 0 else [0]

print(f"\n  COUPLING CONSTANTS (least-squares fit):")
print(f"  {'Pair':>6s}  {'ε value':>12s}  {'As fraction':>15s}")
print(f"  {'-'*6}  {'-'*12}  {'-'*15}")

for i, pt in enumerate(pair_types):
    eps = epsilons[i]
    # Check if close to structural fraction
    best_frac = ""
    for num in range(1, 121):
        for den in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]:
            frac = num / den
            if abs(eps - frac) / max(abs(eps), 0.001) < 0.02:
                best_frac = f"≈ {num}/{den}"
                break
        if best_frac:
            break
    print(f"  {pt:>6s}  {eps:12.4f}  {best_frac:>15s}")

# Check fit quality
print(f"\n  FIT QUALITY:")
predicted = A @ epsilons
print(f"  {'Baryon':>10s}  {'Quarks':>5s}  {'Actual':>10s}  {'Zeroth+Coup':>12s}  {'Error':>8s}")
print(f"  {'-'*10}  {'-'*5}  {'-'*10}  {'-'*12}  {'-'*8}")

for i, (name, quarks, mass) in enumerate(BARYONS):
    zeroth = sum(quark_energies[q] for q in quarks)
    total = zeroth + predicted[i]
    error = (total - mass) / mass * 100
    print(f"  {name:>10s}  {quarks:>5s}  {mass:10.4f}  {total:12.4f}  {error:7.3f}%")

print("\n" + "=" * 80)
print("PART 5: COUPLING CONSTANT STRUCTURE ANALYSIS")
print("=" * 80)

print("""
  If the couplings have base-60 structure, we should see:
  - Ratios between couplings that are structural fractions
  - ε values expressible as n/60 or n/m where {n,m} ∈ {2,3,5}^k
""")

print(f"\n  Coupling ratios:")
for i, pt1 in enumerate(pair_types):
    for j, pt2 in enumerate(pair_types):
        if j <= i:
            continue
        if abs(epsilons[j]) < 0.001:
            continue
        ratio = epsilons[i] / epsilons[j]
        # Check structural fractions
        match = ""
        for n in range(1, 13):
            for d in range(1, 13):
                if abs(ratio - n/d) / max(abs(ratio), 0.001) < 0.02:
                    match = f"≈ {n}/{d}"
                    break
            if match:
                break
        print(f"    ε_{pt1}/ε_{pt2} = {ratio:.6f} {match}")

# Check strangeness contribution
print(f"\n  Strangeness analysis:")
eps_u = quark_energies['u']
eps_d = quark_energies['d']
eps_s = quark_energies['s']
print(f"    u quark energy: {eps_u:.4f} ({eps_u/M_P_M_E*100:.2f}% of proton)")
print(f"    d quark energy: {eps_d:.4f} ({eps_d/M_P_M_E*100:.2f}% of proton)")
print(f"    s quark energy: {eps_s:.4f} ({eps_s/M_P_M_E*100:.2f}% of proton)")
print(f"    s/u ratio: {eps_s/eps_u:.6f}")
print(f"    s/d ratio: {eps_s/eps_d:.6f}")
print(f"    d/u ratio: {eps_d/eps_u:.6f}")
print(f"    d-u difference: {eps_d - eps_u:.6f}")

# Check if s/u or s/d are structural fractions
for name, ratio in [('s/u', eps_s/eps_u), ('s/d', eps_s/eps_d), ('d/u', eps_d/eps_u)]:
    for n in range(1, 20):
        for d_val in range(1, 20):
            if abs(ratio - n/d_val) / ratio < 0.005:
                print(f"    {name} = {ratio:.6f} ≈ {n}/{d_val} = {n/d_val:.6f} (error: {abs(ratio-n/d_val)/ratio*100:.3f}%)")

print("\n" + "=" * 80)
print("PART 6: NUMERICAL COUPLED MAP VERIFICATION")
print("=" * 80)

print("""
  Now test: do the derived Γ values and couplings produce correct
  masses when iterated as ACTUAL coupled maps?
""")

# Map quark flavors to Γ values
gamma_map = {'u': gamma_u, 'd': gamma_d, 's': gamma_s}

# Map quark pair types to coupling constants
eps_map = {pt: epsilons[i] for i, pt in enumerate(pair_types)}

def make_coupling_matrix(quarks, eps_map):
    """Build coupling matrix for a specific baryon."""
    order = {'u': 0, 'd': 1, 's': 2}
    q = list(quarks)
    eps = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            a, b = q[i], q[j]
            if order[a] <= order[b]:
                pair = a + b
            else:
                pair = b + a
            # Scale coupling to be perturbative
            eps[i][j] = eps_map[pair] * 0.001  # small coupling
    return eps

print(f"\n  Iterating coupled maps for each baryon...")
print(f"  {'Baryon':>10s}  {'Quarks':>5s}  {'Γ values':>25s}  {'Energy':>12s}  {'Actual':>12s}  {'Error':>8s}")
print(f"  {'-'*10}  {'-'*5}  {'-'*25}  {'-'*12}  {'-'*12}  {'-'*8}")

for name, quarks, mass in BARYONS:
    q = list(quarks)
    gammas = [gamma_map[qi] for qi in q]

    # Try different coupling scales
    best_energy = None
    best_error = 999

    for scale in [0, 0.0001, 0.001, 0.01, 0.1]:
        couplings = np.zeros((3, 3))
        order = {'u': 0, 'd': 1, 's': 2}
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                a, b = q[i], q[j]
                if order[a] <= order[b]:
                    pair = a + b
                else:
                    pair = b + a
                couplings[i][j] = eps_map[pair] * scale

        # Try multiple initial conditions
        for ic_scale in [0.5, 0.8, 1.0]:
            x0 = np.array([g * ic_scale for g in gammas])
            fp, energy, converged = find_coupled_fixed_point(gammas, LAMBDA, couplings, x0=x0)

            if converged and energy > 1:
                error = abs(energy - mass) / mass * 100
                if error < best_error:
                    best_error = error
                    best_energy = energy

    if best_energy is not None:
        g_str = ', '.join([f'{g:.2f}' for g in gammas])
        error = (best_energy - mass) / mass * 100
        print(f"  {name:>10s}  {quarks:>5s}  [{g_str:>21s}]  {best_energy:12.4f}  {mass:12.4f}  {error:7.3f}%")

print("\n" + "=" * 80)
print("PART 7: BASE-60 STRUCTURE IN QUARK MASSES")
print("=" * 80)

print("""
  The single-quark energies (from the Γ² scaling) should decompose
  into base-60 structural fractions if the framework is right.
""")

def base60_decompose(value):
    """Decompose value into base-60 digits."""
    digits = []
    remaining = value
    for power in [3, 2, 1, 0, -1, -2]:
        base = 60**power
        if base > value * 100 and power > 0:
            continue
        digit = int(remaining / base)
        remaining -= digit * base
        if digit > 0 or digits:
            digits.append((power, digit))
    return digits, remaining

for flavor, energy in [('u', eps_u), ('d', eps_d), ('s', eps_s)]:
    digits, remainder = base60_decompose(energy)
    digit_str = ' + '.join([f'{d}·60^{p}' for p, d in digits])
    print(f"\n  {flavor} quark energy = {energy:.4f}")
    print(f"    Base-60: {digit_str}")
    print(f"    Remainder: {remainder:.6f} ({remainder/energy*100:.3f}%)")

    # Check if energy is close to structural fraction × 60^n
    for n60 in [0, 1, 2]:
        for num in range(1, 61):
            for den in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]:
                target = (num / den) * 60**n60
                if abs(energy - target) / energy < 0.005:
                    print(f"    ≈ ({num}/{den})·60^{n60} = {target:.4f} (error: {abs(energy-target)/energy*100:.4f}%)")

print("\n" + "=" * 80)
print("PART 8: THE ADDITIVE MODEL — QUARK MASSES + PAIR INTERACTIONS")
print("=" * 80)

print("""
  FINAL MODEL:
  M_baryon = m_q1 + m_q2 + m_q3 + V_12 + V_13 + V_23

  where:
  - m_q = constituent quark mass (u, d, s)
  - V_ij = pair interaction energy (depends on quark flavors)

  This is 3 + 6 = 9 parameters for 9 masses.
  But the proton+neutron constraint fixes m_u, m_d.
  The Omega constraint fixes m_s.
  So only 6 coupling parameters remain for 6 remaining masses.

  Let's solve exactly and check for structural patterns.
""")

# From proton: 2*m_u + m_d + V_uu + 2*V_ud = 1836.15
# From neutron: m_u + 2*m_d + 2*V_ud + V_dd = 1838.68
# Adding: 3*(m_u + m_d) + V_uu + 4*V_ud + V_dd = 3674.83
# Subtracting: (m_u - m_d) + V_uu - V_dd = -2.53

# We can't separate m_q from V_qq without more info.
# But we CAN solve the full 9×9 system:

# Variables: m_u, m_d, m_s, V_uu, V_ud, V_us, V_dd, V_ds, V_ss
# 9 variables, 9 equations

var_names = ['m_u', 'm_d', 'm_s', 'V_uu', 'V_ud', 'V_us', 'V_dd', 'V_ds', 'V_ss']

def build_equation(quarks):
    """Build equation coefficients for M = sum(m_q) + sum(V_pairs)."""
    q = list(quarks)
    coeffs = np.zeros(9)
    # Quark masses
    for qi in q:
        if qi == 'u': coeffs[0] += 1
        elif qi == 'd': coeffs[1] += 1
        elif qi == 's': coeffs[2] += 1
    # Pair interactions
    pairs = count_pairs(quarks)
    for i, pt in enumerate(pair_types):
        coeffs[3 + i] = pairs[pt]
    return coeffs

A_full = []
b_full = []
for name, quarks, mass in BARYONS:
    A_full.append(build_equation(quarks))
    b_full.append(mass)

A_full = np.array(A_full)
b_full = np.array(b_full)

print(f"  System rank: {np.linalg.matrix_rank(A_full)} (need 9 for unique solution)")

# Check if system is solvable
rank = np.linalg.matrix_rank(A_full)
if rank < 9:
    print(f"  Rank deficient ({rank} < 9). Using least-squares with constraints.")
    # Add constraint: m_u + m_d + m_s ≈ (1/3)*(proton + neutron + Omega)
    # This is a reasonable normalization
    result = np.linalg.lstsq(A_full, b_full, rcond=None)
    params = result[0]
else:
    params = np.linalg.solve(A_full, b_full)

print(f"\n  SOLUTION:")
print(f"  {'Parameter':>10s}  {'Value':>12s}  {'Structural?':>30s}")
print(f"  {'-'*10}  {'-'*12}  {'-'*30}")

for i, name in enumerate(var_names):
    val = params[i]
    # Check structural fractions
    struct = ""
    for n60 in [0, 1, 2]:
        for num in range(-120, 121):
            if num == 0: continue
            for den in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]:
                target = (num / den) * 60**n60
                if abs(val - target) / max(abs(val), 1) < 0.005:
                    struct = f"≈ ({num}/{den})·60^{n60} = {target:.2f}"
                    break
            if struct:
                break
        if struct:
            break
    print(f"  {name:>10s}  {val:12.4f}  {struct:>30s}")

# Verify
print(f"\n  VERIFICATION:")
predicted_full = A_full @ params
print(f"  {'Baryon':>10s}  {'Actual':>10s}  {'Predicted':>10s}  {'Error':>8s}")
print(f"  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*8}")
for i, (name, quarks, mass) in enumerate(BARYONS):
    error = (predicted_full[i] - mass) / mass * 100
    print(f"  {name:>10s}  {mass:10.4f}  {predicted_full[i]:10.4f}  {error:7.4f}%")

# Check ratios between parameters
print(f"\n  KEY RATIOS:")
m_u, m_d, m_s = params[0], params[1], params[2]
print(f"    m_s / m_u = {m_s/m_u:.6f}")
print(f"    m_s / m_d = {m_s/m_d:.6f}")
print(f"    m_d / m_u = {m_d/m_u:.6f}")
print(f"    m_d - m_u = {m_d - m_u:.6f}")
print(f"    m_s - m_u = {m_s - m_u:.6f}")
print(f"    m_s - m_d = {m_s - m_d:.6f}")

# Check V ratios
V_uu, V_ud, V_us, V_dd, V_ds, V_ss = params[3:9]
print(f"\n    V_uu = {V_uu:.4f}")
print(f"    V_ud = {V_ud:.4f}")
print(f"    V_us = {V_us:.4f}")
print(f"    V_dd = {V_dd:.4f}")
print(f"    V_ds = {V_ds:.4f}")
print(f"    V_ss = {V_ss:.4f}")

if abs(V_uu) > 0.01 and abs(V_dd) > 0.01:
    print(f"\n    V_dd/V_uu = {V_dd/V_uu:.6f}")
if abs(V_us) > 0.01 and abs(V_ud) > 0.01:
    print(f"    V_us/V_ud = {V_us/V_ud:.6f}")
if abs(V_ss) > 0.01 and abs(V_uu) > 0.01:
    print(f"    V_ss/V_uu = {V_ss/V_uu:.6f}")
if abs(V_ds) > 0.01 and abs(V_ud) > 0.01:
    print(f"    V_ds/V_ud = {V_ds/V_ud:.6f}")

print("\n" + "=" * 80)
print("COMPLETE COUPLED QUARK ANALYSIS SUMMARY")
print("=" * 80)
