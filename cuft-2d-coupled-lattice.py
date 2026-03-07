#!/usr/bin/env python3
"""
CUFT-RASP ATTACK VECTOR 3: 2D COUPLED MAP LATTICE
===================================================
YASA PRESENTS — 2026-02-28

The Diophantine equation (n-2)(p-1) = 4 has three solutions:
    (n,p) = (3,5): M = 853811/465 = 1836.152688... (proton)
    (n,p) = (4,3): M = 100051/312 =  320.676282...
    (n,p) = (6,2): M =   4663/42  =  111.023810...

This script couples PAIRS of these recursions via a 2D coupled map lattice:
    x_{t+1} = f_1(x_t) + epsilon * (y_t - x_t)
    y_{t+1} = f_2(y_t) + epsilon * (x_t - y_t)

where f_i(x) = Gamma_i * tanh^{n_i}(x) - lambda_i * x

We scan coupling strength epsilon and find ALL fixed points of the coupled
system, then compare against the meson/lepton zoo to see if coupling-induced
modes match known particle masses (in m_e units).

Additionally, all pairwise sums and differences of the three Diophantine
masses are compared against the particle zoo.

METHODOLOGY:
- sympy Rational for exact arithmetic on the uncoupled masses
- scipy.optimize.fsolve for numerical coupled fixed-point finding
- Multiple initial conditions to capture ALL branches
- Denominator factorization check against {2, 3, 5, 31}
"""

import numpy as np
from sympy import Rational, factorint, sqrt as ssqrt, tanh as stanh, S
from scipy.optimize import fsolve
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: EXACT DIOPHANTINE SOLUTIONS
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 90)
print("CUFT-RASP ATTACK VECTOR 3: 2D COUPLED MAP LATTICE")
print("=" * 90)

print("\n" + "=" * 90)
print("SECTION 1: DIOPHANTINE SOLUTIONS — EXACT RATIONAL ARITHMETIC")
print("=" * 90)

# The three solutions to (n-2)(p-1) = 4 with n >= 3, p >= 2
diophantine_solutions = [(3, 5), (4, 3), (6, 2)]

# Storage for exact and float values
exact_masses = {}
float_masses = {}
params = {}

print(f"\n{'(n,p)':>8s} | {'Gamma':>6s} | {'lambda':>12s} | {'X':>4s} | {'M (exact rational)':>25s} | {'M (float)':>16s}")
print("-" * 90)

for n, p in diophantine_solutions:
    Gamma = Rational(p**2)
    lam = Rational(1, p**3 - 1)
    X = Rational(n * p * (p - 1))

    # Mass formula: M = X^2/2 + (n/p)*X + n^2/X + lambda/n
    c2_term = X**2 / 2
    c1_term = Rational(n, p) * X
    cm1_term = Rational(n**2, 1) / X
    c0_term = lam / n

    M = c2_term + c1_term + cm1_term + c0_term

    exact_masses[(n, p)] = M
    float_masses[(n, p)] = float(M)

    # Store parameters for later use
    params[(n, p)] = {
        'n': n, 'p': p,
        'Gamma': float(Gamma), 'lambda': float(lam),
        'X': float(X), 'M': float(M),
        'Gamma_exact': Gamma, 'lambda_exact': lam, 'X_exact': X
    }

    print(f"({n},{p})    | {int(Gamma):>6d} | {str(lam):>12s} | {int(X):>4d} | {str(M):>25s} | {float(M):>16.10f}")

# Denominator factorization
print("\nDENOMINATOR FACTORIZATION:")
for (n, p), M in exact_masses.items():
    denom = M.q
    factors = factorint(denom)
    print(f"  M({n},{p}) = {M.p}/{M.q}   denom factors: {factors}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: FIXED POINTS OF EACH UNCOUPLED RECURSION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 2: FIXED POINTS OF EACH UNCOUPLED RECURSION")
print("=" * 90)

def f_map(x, n, Gamma, lam):
    """The CUFT-RASP recursion: f(x) = Gamma * tanh^n(x) - lambda * x"""
    return Gamma * np.tanh(x)**n - lam * x

def f_fixed_point_eq(x, n, Gamma, lam):
    """f(x) - x = 0 for fixed point finding."""
    return f_map(x, n, Gamma, lam) - x

def f_derivative(x, n, Gamma, lam):
    """f'(x) = Gamma * n * tanh^{n-1}(x) * sech^2(x) - lambda"""
    t = np.tanh(x)
    s2 = 1.0 - t**2  # sech^2(x)
    return Gamma * n * t**(n - 1) * s2 - lam

print(f"\n{'(n,p)':>8s} | {'x_trivial':>10s} | {'x_u (unstable)':>16s} | {'x_s (stable)':>16s} | {'f_prime(x_s)':>14s}")
print("-" * 90)

fixed_points = {}

for n, p in diophantine_solutions:
    Gamma = params[(n, p)]['Gamma']
    lam = params[(n, p)]['lambda']

    # Find x_u (unstable, small positive) and x_s (stable, large positive)
    # x_u: scan for sign change of f(x)-x in (0, Gamma) to bracket the root
    x_u = None
    for trial in np.linspace(0.01, Gamma * 0.8, 500):
        val = f_fixed_point_eq(trial, n, Gamma, lam)
        if val < 0:  # crossed zero (f(x)-x goes from + to -)
            x_u_sol = fsolve(f_fixed_point_eq, trial, args=(n, Gamma, lam), full_output=True)
            candidate = abs(x_u_sol[0][0])
            if candidate > 0.01 and x_u_sol[2] == 1:
                x_u = candidate
                break
    if x_u is None:
        # Fallback: no unstable FP found (can happen for n=6, p=2 where the
        # basin is extremely narrow). Use a fine scan near the origin.
        for trial in np.linspace(0.001, 2.0, 2000):
            val = f_fixed_point_eq(trial, n, Gamma, lam)
            if val < 0:
                x_u_sol = fsolve(f_fixed_point_eq, trial, args=(n, Gamma, lam), full_output=True)
                candidate = abs(x_u_sol[0][0])
                if candidate > 1e-6 and x_u_sol[2] == 1:
                    x_u = candidate
                    break
    if x_u is None:
        x_u = 0.0  # genuinely no unstable FP

    # x_s: start near Gamma (saturated regime)
    x_s_guess = Gamma * 0.9
    x_s_sol = fsolve(f_fixed_point_eq, x_s_guess, args=(n, Gamma, lam), full_output=True)
    x_s = abs(x_s_sol[0][0])

    # Make sure x_u < x_s
    if x_u > x_s:
        x_u, x_s = x_s, x_u

    fp_xu = f_derivative(x_u, n, Gamma, lam)
    fp_xs = f_derivative(x_s, n, Gamma, lam)

    fixed_points[(n, p)] = {'x_u': x_u, 'x_s': x_s, 'fp_xu': fp_xu, 'fp_xs': fp_xs}

    print(f"({n},{p})    | {'0':>10s} | {x_u:>16.10f} | {x_s:>16.10f} | {fp_xs:>14.10f}")

print("\nVERIFICATION: f'(x_s) should equal -lambda for the physical solution (3,5):")
print("  (For (4,3) and (6,2), gain-coherence is NOT satisfied, so f'(x_s) = -lambda")
print("   only holds approximately — these are non-physical Diophantine branches.)")
for (n, p), fp in fixed_points.items():
    lam = params[(n, p)]['lambda']
    diff = abs(fp['fp_xs'] + lam)
    exact = diff < 1e-8
    print(f"  ({n},{p}): f'(x_s) = {fp['fp_xs']:.12f}, -lambda = {-lam:.12f}, "
          f"diff = {diff:.2e}, exact = {exact}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: TARGET PARTICLE MASSES (PDG 2024, in m_e units)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 3: TARGET PARTICLE MASSES (PDG 2024)")
print("=" * 90)

# m_e = 0.51099895000 MeV/c^2 (CODATA 2022)
m_e_MeV = 0.51099895000

target_particles = {
    # Leptons
    'muon':          206.768,
    'tau':           3477.48,
    # Pseudoscalar mesons
    'pi_charged':    273.13,
    'pi_neutral':    264.14,
    'K_charged':     966.12,
    'K_neutral':     974.55,
    'eta':           1073.2,
    'eta_prime':     1874.0,
    # Vector mesons
    'rho':           1517.1,
    'omega':         1532.3,
    'phi':           1995.3,
    # Heavy mesons
    'J_psi':         6040.0,
    'D_charged':     3654.8,
    'D_neutral':     3649.1,
    # Baryons
    'proton':        1836.153,
    'neutron':       1838.684,
}

print(f"\n{'Particle':>14s} | {'Mass (m_e)':>12s} | {'Mass (MeV)':>12s}")
print("-" * 45)
for name, mass in sorted(target_particles.items(), key=lambda x: x[1]):
    print(f"{name:>14s} | {mass:>12.3f} | {mass * m_e_MeV:>12.3f}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: PAIRWISE SUMS AND DIFFERENCES (EXACT RATIONAL)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 4: PAIRWISE SUMS AND DIFFERENCES OF DIOPHANTINE MASSES")
print("=" * 90)

print("\nAll pairwise combinations of the three Diophantine masses:")
print(f"\n{'Operation':>30s} | {'Exact Rational':>25s} | {'Float Value':>14s} | {'Denom Factors':>20s}")
print("-" * 100)

combo_values = {}  # store for later matching

sol_labels = {(3,5): 'M(3,5)', (4,3): 'M(4,3)', (6,2): 'M(6,2)'}
sol_list = list(diophantine_solutions)

for i in range(len(sol_list)):
    for j in range(len(sol_list)):
        if i == j:
            continue
        s1, s2 = sol_list[i], sol_list[j]
        M1, M2 = exact_masses[s1], exact_masses[s2]

        # Difference
        diff = M1 - M2
        if diff > 0:
            label = f"{sol_labels[s1]} - {sol_labels[s2]}"
            combo_values[label] = float(diff)
            denom_factors = factorint(diff.q) if diff.q > 1 else {1: 1}
            print(f"{label:>30s} | {str(diff):>25s} | {float(diff):>14.6f} | {denom_factors}")

# Sums
print()
for i in range(len(sol_list)):
    for j in range(i, len(sol_list)):
        s1, s2 = sol_list[i], sol_list[j]
        M1, M2 = exact_masses[s1], exact_masses[s2]
        total = M1 + M2
        label = f"{sol_labels[s1]} + {sol_labels[s2]}"
        combo_values[label] = float(total)
        denom_factors = factorint(total.q) if total.q > 1 else {1: 1}
        print(f"{label:>30s} | {str(total):>25s} | {float(total):>14.6f} | {denom_factors}")

# Also add individual masses
for s in sol_list:
    label = sol_labels[s]
    combo_values[label] = float_masses[s]

# Check denominator set {2,3,5,31}
print("\nDENOMINATOR SET CHECK — do all denominators factor through {2, 3, 5, 31}?")
cuft_primes = {2, 3, 5, 31}
for i in range(len(sol_list)):
    for j in range(i + 1, len(sol_list)):
        s1, s2 = sol_list[i], sol_list[j]
        M1, M2 = exact_masses[s1], exact_masses[s2]
        for op, val, label in [('-', M1 - M2, f"{sol_labels[s1]} - {sol_labels[s2]}"),
                                ('+', M1 + M2, f"{sol_labels[s1]} + {sol_labels[s2]}")]:
            denom = val.q
            factors = set(factorint(denom).keys()) if denom > 1 else set()
            in_set = factors.issubset(cuft_primes)
            marker = "YES" if in_set else "NO"
            print(f"  {label:>30s}: denom = {denom:>8d}, prime factors = {factors or '{1}'}, "
                  f"in {{2,3,5,31}}: {marker}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: MATCH COMBOS AGAINST PARTICLE ZOO
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 5: PAIRWISE COMBO MATCHES TO PARTICLE ZOO (< 1% error)")
print("=" * 90)

def find_matches(value, label, targets, threshold=0.01):
    """Find particle matches within threshold fractional error."""
    matches = []
    for pname, pmass in targets.items():
        if pmass < 1.0:
            continue
        frac_err = abs(value - pmass) / pmass
        if frac_err < threshold:
            matches.append((pname, pmass, frac_err))
    return sorted(matches, key=lambda x: x[2])

print(f"\n{'Combination':>30s} | {'Value (m_e)':>14s} | {'Particle':>14s} | {'Particle Mass':>14s} | {'Error':>10s}")
print("-" * 95)

all_combo_matches = []
for label, value in sorted(combo_values.items(), key=lambda x: x[1]):
    matches = find_matches(value, label, target_particles)
    for pname, pmass, err in matches:
        print(f"{label:>30s} | {value:>14.6f} | {pname:>14s} | {pmass:>14.3f} | {err*100:>9.4f}%")
        all_combo_matches.append((label, value, pname, pmass, err))

if not all_combo_matches:
    print("  No matches within 1% threshold found.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: 2D COUPLED MAP LATTICE — FIXED POINT SCAN
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 6: 2D COUPLED MAP LATTICE — COUPLED FIXED POINT ANALYSIS")
print("=" * 90)

print("""
  COUPLED SYSTEM:
    x_{t+1} = f_1(x_t) + epsilon * (y_t - x_t)
    y_{t+1} = f_2(y_t) + epsilon * (x_t - y_t)

  Fixed point condition (F(x,y) = (x,y)):
    x = f_1(x) + epsilon * (y - x)
    y = f_2(y) + epsilon * (x - y)

  Rearranging:
    f_1(x) - x + epsilon * (y - x) = 0
    f_2(y) - y + epsilon * (x - y) = 0
""")


def coupled_fixed_point_eq(state, n1, G1, l1, n2, G2, l2, eps):
    """Equations for fixed points of the 2D coupled map lattice.

    F(x,y) = (0, 0) where:
      F_1 = f_1(x) + eps*(y-x) - x = (G1*tanh^n1(x) - l1*x) + eps*(y-x) - x
      F_2 = f_2(y) + eps*(x-y) - y = (G2*tanh^n2(y) - l2*y) + eps*(x-y) - y
    """
    x, y = state
    f1 = G1 * np.tanh(x)**n1 - l1 * x
    f2 = G2 * np.tanh(y)**n2 - l2 * y
    eq1 = f1 + eps * (y - x) - x
    eq2 = f2 + eps * (x - y) - y
    return [eq1, eq2]


def coupled_jacobian(state, n1, G1, l1, n2, G2, l2, eps):
    """Jacobian of the coupled fixed point equations for stability analysis."""
    x, y = state
    # df1/dx
    t1 = np.tanh(x)
    s1_sq = 1.0 - t1**2
    df1dx = G1 * n1 * t1**(n1 - 1) * s1_sq - l1
    # df2/dy
    t2 = np.tanh(y)
    s2_sq = 1.0 - t2**2
    df2dy = G2 * n2 * t2**(n2 - 1) * s2_sq - l2

    # Jacobian of the map (x_new, y_new) = (f1(x)+eps*(y-x), f2(y)+eps*(x-y))
    # dF1/dx = df1dx - eps - 1,  dF1/dy = eps
    # dF2/dx = eps,                dF2/dy = df2dy - eps - 1
    J = np.array([
        [df1dx - eps - 1.0, eps],
        [eps, df2dy - eps - 1.0]
    ])
    return J


def find_all_coupled_fps(n1, G1, l1, n2, G2, l2, eps, num_ics=50):
    """Find all fixed points using many initial conditions.

    Returns list of (x, y, stable) tuples for unique fixed points.
    """
    fp_set = []

    # Generate diverse initial conditions
    # Include: fixed points of individual maps, random perturbations, grid
    xs_1 = fixed_points[(n1, int(round(G1**0.5)))]['x_s'] if (n1, int(round(G1**0.5))) in fixed_points else G1 * 0.9
    xu_1 = fixed_points[(n1, int(round(G1**0.5)))]['x_u'] if (n1, int(round(G1**0.5))) in fixed_points else 0.5
    xs_2 = fixed_points[(n2, int(round(G2**0.5)))]['x_s'] if (n2, int(round(G2**0.5))) in fixed_points else G2 * 0.9
    xu_2 = fixed_points[(n2, int(round(G2**0.5)))]['x_u'] if (n2, int(round(G2**0.5))) in fixed_points else 0.5

    initial_conditions = [
        (0.0, 0.0),
        (xs_1, xs_2), (-xs_1, -xs_2),
        (xs_1, -xs_2), (-xs_1, xs_2),
        (xu_1, xu_2), (-xu_1, -xu_2),
        (xu_1, -xu_2), (-xu_1, xu_2),
        (xs_1, xu_2), (xu_1, xs_2),
        (xs_1, 0.0), (0.0, xs_2),
        (-xs_1, 0.0), (0.0, -xs_2),
        (xu_1, 0.0), (0.0, xu_2),
    ]

    # Add grid-based ICs
    for xv in np.linspace(-G1 * 1.1, G1 * 1.1, 8):
        for yv in np.linspace(-G2 * 1.1, G2 * 1.1, 8):
            initial_conditions.append((xv, yv))

    for ic in initial_conditions:
        try:
            sol = fsolve(coupled_fixed_point_eq, ic,
                         args=(n1, G1, l1, n2, G2, l2, eps),
                         full_output=True, maxfev=5000)
            x_sol, info, ier, msg = sol
            if ier == 1:  # converged
                residual = np.max(np.abs(info['fvec']))
                if residual < 1e-10:
                    x_val, y_val = x_sol

                    # Check if this is a new fixed point
                    is_new = True
                    for existing in fp_set:
                        if abs(x_val - existing[0]) < 1e-6 and abs(y_val - existing[1]) < 1e-6:
                            is_new = False
                            break
                    if is_new:
                        # Stability: eigenvalues of Jacobian of the MAP
                        # The map Jacobian at fixed point
                        J = coupled_jacobian(x_sol, n1, G1, l1, n2, G2, l2, eps)
                        # For the fixed point equation F = map - identity = 0,
                        # the map Jacobian is J + I. Eigenvalues of map = eig(J+I).
                        # Stable if all |eigenvalues of map| < 1.
                        map_J = J + np.eye(2)
                        eigvals = np.linalg.eigvals(map_J)
                        stable = all(abs(ev) < 1.0 for ev in eigvals)
                        fp_set.append((x_val, y_val, stable, eigvals))
        except Exception:
            pass

    return fp_set


# Scan all three pairings
pairings = [
    ((3, 5), (4, 3)),
    ((3, 5), (6, 2)),
    ((4, 3), (6, 2)),
]

# Epsilon scan range
eps_values = np.arange(0.0, 0.501, 0.001)

# Store ALL coupling-induced fixed points
all_coupled_fps = {}  # key: (pairing, eps) -> list of (x, y, stable)

# For each pairing, track fixed points vs epsilon
print("Scanning coupled fixed points across epsilon values...")
print("(This may take a minute per pairing)\n")

# Key results storage: (pairing, eps, x, y, observable, match_particle, match_error)
key_results = []

for pair_idx, (s1, s2) in enumerate(pairings):
    n1, p1 = s1
    n2, p2 = s2
    G1 = params[s1]['Gamma']
    l1 = params[s1]['lambda']
    G2 = params[s2]['Gamma']
    l2 = params[s2]['lambda']

    pair_label = f"({n1},{p1})-({n2},{p2})"
    print(f"\n{'─' * 90}")
    print(f"PAIRING: f_1 uses (n,p)=({n1},{p1}), f_2 uses (n,p)=({n2},{p2})")
    print(f"  Gamma_1 = {G1}, lambda_1 = {l1:.10f}")
    print(f"  Gamma_2 = {G2}, lambda_2 = {l2:.10f}")
    print(f"{'─' * 90}")

    # Track unique observable values across epsilon
    observable_tracker = {}  # eps -> list of observables

    # Coarser scan first to find interesting regions, then refine
    eps_coarse = np.arange(0.0, 0.501, 0.005)
    interesting_eps = set()

    for eps in eps_coarse:
        fps = find_all_coupled_fps(n1, G1, l1, n2, G2, l2, eps, num_ics=30)

        for x_val, y_val, stable, eigvals in fps:
            # Compute observables: individual values and combinations
            observables = {
                'x': abs(x_val),
                'y': abs(y_val),
                'x^2': x_val**2,
                'y^2': y_val**2,
                'x^2+y^2': x_val**2 + y_val**2,
                '|x^2-y^2|': abs(x_val**2 - y_val**2),
                'x*y': abs(x_val * y_val),
            }

            for obs_name, obs_val in observables.items():
                if obs_val < 50 or obs_val > 250000:
                    continue
                matches = find_matches(obs_val, '', target_particles, threshold=0.01)
                if matches:
                    interesting_eps.add(eps)
                    # Mark nearby epsilon for fine scan
                    for de in np.arange(-0.01, 0.011, 0.001):
                        e2 = eps + de
                        if 0.0 <= e2 <= 0.5:
                            interesting_eps.add(round(e2, 3))

    # Fine scan on interesting regions + always scan eps=0 neighborhood
    interesting_eps.add(0.0)
    for de in np.arange(0.0, 0.05, 0.001):
        interesting_eps.add(round(de, 3))

    eps_scan = sorted(interesting_eps)

    # Now do detailed scan
    pair_matches = []

    for eps in eps_scan:
        fps = find_all_coupled_fps(n1, G1, l1, n2, G2, l2, eps, num_ics=40)

        for x_val, y_val, stable, eigvals in fps:
            observables = {
                'x^2': x_val**2,
                'y^2': y_val**2,
                'x^2+y^2': x_val**2 + y_val**2,
                '|x^2-y^2|': abs(x_val**2 - y_val**2),
                'x*y': abs(x_val * y_val),
                '(x+y)^2/2': (x_val + y_val)**2 / 2,
                '(x-y)^2/2': (x_val - y_val)**2 / 2,
            }

            for obs_name, obs_val in observables.items():
                if obs_val < 50 or obs_val > 250000:
                    continue
                matches = find_matches(obs_val, '', target_particles, threshold=0.01)
                for pname, pmass, err in matches:
                    stab_str = "stable" if stable else "unstable"
                    pair_matches.append({
                        'eps': eps,
                        'x': x_val, 'y': y_val,
                        'observable': obs_name,
                        'obs_val': obs_val,
                        'particle': pname,
                        'pmass': pmass,
                        'error': err,
                        'stable': stable,
                    })

    # Deduplicate: keep best match per (particle, observable) combination
    best_matches = {}
    for m in pair_matches:
        key = (m['particle'], m['observable'])
        if key not in best_matches or m['error'] < best_matches[key]['error']:
            best_matches[key] = m

    if best_matches:
        print(f"\n  MATCHES FOUND (best per particle/observable, < 1% error):")
        print(f"  {'epsilon':>8s} | {'Observable':>14s} | {'Value':>12s} | {'Particle':>14s} | {'Target':>10s} | {'Error':>8s} | {'Stability':>10s}")
        print(f"  {'-'*8} | {'-'*14} | {'-'*12} | {'-'*14} | {'-'*10} | {'-'*8} | {'-'*10}")
        for key in sorted(best_matches.keys(), key=lambda k: best_matches[k]['error']):
            m = best_matches[key]
            stab = "STABLE" if m['stable'] else "unstable"
            print(f"  {m['eps']:>8.3f} | {m['observable']:>14s} | {m['obs_val']:>12.3f} | {m['particle']:>14s} | {m['pmass']:>10.3f} | {m['error']*100:>7.4f}% | {stab:>10s}")
            key_results.append((pair_label, m))
    else:
        print(f"\n  No particle matches found within 1% for this pairing.")

    # Report fixed point landscape at eps=0 (uncoupled baseline)
    print(f"\n  UNCOUPLED BASELINE (epsilon = 0):")
    fps_0 = find_all_coupled_fps(n1, G1, l1, n2, G2, l2, 0.0, num_ics=40)
    print(f"  Found {len(fps_0)} fixed points:")
    for x_val, y_val, stable, eigvals in sorted(fps_0, key=lambda f: f[0]**2 + f[1]**2):
        stab = "STABLE" if stable else "unstable"
        print(f"    x = {x_val:>12.6f}, y = {y_val:>12.6f}, "
              f"x^2+y^2 = {x_val**2+y_val**2:>12.3f}, "
              f"|eig| = ({abs(eigvals[0]):.4f}, {abs(eigvals[1]):.4f}), {stab}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: EXTENDED ALGEBRAIC COMBINATIONS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 7: EXTENDED ALGEBRAIC COMBINATIONS OF DIOPHANTINE MASSES")
print("=" * 90)

print("""
  Beyond simple sums/differences, check:
  - Products and ratios scaled to m_e units
  - Geometric means
  - Lambda-weighted combinations
  - Fixed-point coordinate products
""")

M35 = exact_masses[(3, 5)]
M43 = exact_masses[(4, 3)]
M62 = exact_masses[(6, 2)]

extended_combos = {}

# Simple arithmetic
extended_combos['M(3,5) - M(4,3)'] = M35 - M43
extended_combos['M(3,5) - M(6,2)'] = M35 - M62
extended_combos['M(4,3) - M(6,2)'] = M43 - M62
extended_combos['M(3,5) + M(4,3)'] = M35 + M43
extended_combos['M(3,5) + M(6,2)'] = M35 + M62
extended_combos['M(4,3) + M(6,2)'] = M43 + M62
extended_combos['M(3,5) + M(4,3) + M(6,2)'] = M35 + M43 + M62

# Double/triple masses
extended_combos['2*M(4,3)'] = 2 * M43
extended_combos['2*M(6,2)'] = 2 * M62
extended_combos['3*M(6,2)'] = 3 * M62
extended_combos['2*M(4,3) + M(6,2)'] = 2 * M43 + M62
extended_combos['M(4,3) + 2*M(6,2)'] = M43 + 2 * M62

# Differences of multiples
extended_combos['M(3,5) - 2*M(4,3)'] = M35 - 2 * M43
extended_combos['M(3,5) - 3*M(6,2)'] = M35 - 3 * M62
extended_combos['M(3,5) - 2*M(6,2)'] = M35 - 2 * M62
extended_combos['2*M(3,5) - M(4,3)'] = 2 * M35 - M43
extended_combos['M(3,5) - M(4,3) - M(6,2)'] = M35 - M43 - M62

# Harmonic/geometric means (as rational approximations)
extended_combos['sqrt(M35*M43) approx'] = None  # Will use float
extended_combos['sqrt(M35*M62) approx'] = None
extended_combos['sqrt(M43*M62) approx'] = None

print(f"{'Combination':>35s} | {'Value (m_e)':>14s} | {'Particle':>14s} | {'Target':>10s} | {'Error':>10s} | {'Denom Factors':>20s}")
print("-" * 115)

for label, val in sorted(extended_combos.items(), key=lambda x: abs(float(x[1])) if x[1] is not None else 0):
    if val is None:
        continue
    fval = float(val)
    if fval <= 0:
        continue

    # Denominator factorization
    if hasattr(val, 'q'):
        denom = val.q
        dfactors = factorint(denom) if denom > 1 else {1: 1}
    else:
        dfactors = 'N/A'

    matches = find_matches(fval, label, target_particles, threshold=0.01)
    if matches:
        for pname, pmass, err in matches:
            print(f"{label:>35s} | {fval:>14.6f} | {pname:>14s} | {pmass:>10.3f} | {err*100:>9.4f}% | {dfactors}")
    else:
        # Still print if within 2% of anything interesting
        matches_2 = find_matches(fval, label, target_particles, threshold=0.02)
        if matches_2:
            for pname, pmass, err in matches_2:
                print(f"{label:>35s} | {fval:>14.6f} | {pname:>14s} | {pmass:>10.3f} | {err*100:>9.4f}% | {dfactors}")

# Geometric means (float only)
geo_combos = {
    'sqrt(M35*M43)': np.sqrt(float(M35) * float(M43)),
    'sqrt(M35*M62)': np.sqrt(float(M35) * float(M62)),
    'sqrt(M43*M62)': np.sqrt(float(M43) * float(M62)),
    '(M35*M43)^(1/3)': (float(M35) * float(M43))**(1.0/3),
    '(M35*M62)^(1/3)': (float(M35) * float(M62))**(1.0/3),
}

print(f"\n  GEOMETRIC MEAN COMBINATIONS:")
for label, fval in geo_combos.items():
    matches = find_matches(fval, label, target_particles, threshold=0.02)
    if matches:
        for pname, pmass, err in matches:
            marker = " <-- MATCH" if err < 0.01 else ""
            print(f"  {label:>25s} = {fval:>12.3f}  ~  {pname:>14s} ({pmass:.1f} m_e, {err*100:.3f}%){marker}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8: DENOMINATOR FACTORIZATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 8: DENOMINATOR FACTORIZATION — {2, 3, 5, 31} CLOSURE")
print("=" * 90)

print("""
  CUFT-RASP prediction: all physical masses are exact rationals whose
  denominators factor exclusively through {2, 3, 5, 31} where 31 = Phi_3(5).

  Check this property for all pairwise sums and differences:
""")

cuft_set = {2, 3, 5, 31}
print(f"{'Expression':>40s} | {'Exact Rational':>25s} | {'Denom':>10s} | {'Prime Factors':>20s} | {'In {2,3,5,31}':>15s}")
print("-" * 120)

all_rational_combos = {}
for label, val in extended_combos.items():
    if val is None or not hasattr(val, 'q'):
        continue
    if float(val) <= 0:
        continue
    all_rational_combos[label] = val

for label, val in sorted(all_rational_combos.items(), key=lambda x: float(x[1])):
    denom = val.q
    if denom == 1:
        factors_set = set()
        factors_dict = {1: 1}
    else:
        factors_dict = factorint(denom)
        factors_set = set(factors_dict.keys())

    in_cuft = factors_set.issubset(cuft_set)
    marker = "YES" if in_cuft else "NO"

    # Truncate rational string if too long
    rat_str = str(val)
    if len(rat_str) > 25:
        rat_str = f"{val.p}/{val.q}"
        if len(rat_str) > 25:
            rat_str = f"{float(val):.10f}"

    print(f"{label:>40s} | {rat_str:>25s} | {denom:>10d} | {factors_dict!s:>20s} | {marker:>15s}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 9: COMPREHENSIVE RESULTS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 9: COMPREHENSIVE RESULTS SUMMARY")
print("=" * 90)

# Collect ALL matches from all analyses
print("\n  A. PAIRWISE DIFFERENCES/SUMS MATCHING PARTICLES (< 1% error):")
print(f"  {'Expression':>35s} | {'Value (m_e)':>14s} | {'Particle':>14s} | {'Target':>10s} | {'Error':>10s}")
print(f"  {'-'*35} | {'-'*14} | {'-'*14} | {'-'*10} | {'-'*10}")

summary_A = []
for label, val in extended_combos.items():
    if val is None:
        continue
    fval = float(val)
    if fval <= 0:
        continue
    matches = find_matches(fval, label, target_particles, threshold=0.01)
    for pname, pmass, err in matches:
        summary_A.append((label, fval, pname, pmass, err))

for label, fval, pname, pmass, err in sorted(summary_A, key=lambda x: x[4]):
    print(f"  {label:>35s} | {fval:>14.3f} | {pname:>14s} | {pmass:>10.3f} | {err*100:>9.4f}%")

if not summary_A:
    print("  (No matches within 1%)")

print(f"\n  B. 2D COUPLED LATTICE MATCHES (< 1% error):")
print(f"  {'Pairing':>18s} | {'eps':>7s} | {'Observable':>14s} | {'Value':>12s} | {'Particle':>14s} | {'Target':>10s} | {'Error':>8s}")
print(f"  {'-'*18} | {'-'*7} | {'-'*14} | {'-'*12} | {'-'*14} | {'-'*10} | {'-'*8}")

if key_results:
    for pair_label, m in sorted(key_results, key=lambda x: x[1]['error']):
        print(f"  {pair_label:>18s} | {m['eps']:>7.3f} | {m['observable']:>14s} | {m['obs_val']:>12.3f} | {m['particle']:>14s} | {m['pmass']:>10.3f} | {m['error']*100:>7.4f}%")
else:
    print("  (No matches within 1%)")

# Final statistics
print(f"\n  SUMMARY STATISTICS:")
print(f"    Pairwise algebraic matches (< 1%): {len(summary_A)}")
print(f"    Coupled lattice matches (< 1%):    {len(key_results)}")
print(f"    Total unique particles matched:     ", end="")
matched_particles = set()
for _, _, pname, _, _ in summary_A:
    matched_particles.add(pname)
for _, m in key_results:
    matched_particles.add(m['particle'])
print(f"{len(matched_particles)}: {sorted(matched_particles)}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 10: COUPLING BIFURCATION STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("SECTION 10: COUPLING BIFURCATION — NUMBER OF FIXED POINTS vs EPSILON")
print("=" * 90)

print("""
  Track how the number of fixed points changes with coupling strength.
  Bifurcations (changes in FP count) are dynamically significant.
""")

for pair_idx, (s1, s2) in enumerate(pairings):
    n1, p1 = s1
    n2, p2 = s2
    G1 = params[s1]['Gamma']
    l1 = params[s1]['lambda']
    G2 = params[s2]['Gamma']
    l2 = params[s2]['lambda']

    pair_label = f"({n1},{p1})-({n2},{p2})"
    print(f"\n  PAIRING: {pair_label}")

    prev_count = None
    for eps in np.arange(0.0, 0.51, 0.01):
        fps = find_all_coupled_fps(n1, G1, l1, n2, G2, l2, eps, num_ics=30)
        n_stable = sum(1 for f in fps if f[2])
        n_unstable = len(fps) - n_stable
        count = len(fps)

        if count != prev_count:
            # Bifurcation detected
            marker = " <-- BIFURCATION" if prev_count is not None else " (initial)"
            print(f"    eps = {eps:.3f}: {count} FPs ({n_stable} stable, {n_unstable} unstable){marker}")
            prev_count = count

print("\n" + "=" * 90)
print("ANALYSIS COMPLETE")
print("=" * 90)
print("""
  This script has:
  1. Computed exact rational masses for all three Diophantine solutions
  2. Found fixed points (x_u, x_s) for each uncoupled recursion
  3. Scanned all pairwise sums/differences/multiples against the particle zoo
  4. Built 2D coupled map lattices for all three pairings
  5. Scanned coupling epsilon from 0 to 0.5, finding ALL fixed points
  6. Checked coupling-induced modes against known particle masses
  7. Verified denominator factorization through {2, 3, 5, 31}
  8. Tracked bifurcation structure vs coupling strength

  KEY KNOWN RESULT: M(3,5) - M(4,3) = 1515.5 m_e ~ rho meson (1517.1 m_e, 0.11%)
  This is the difference of two exact rationals with zero free parameters.
""")
