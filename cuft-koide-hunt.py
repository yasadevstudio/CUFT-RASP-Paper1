#!/usr/bin/env python3
"""
CUFT-RASP: Hunt for Koide Formula from Cubic Recursion
YASA PRESENTS — 2026-02-12

THE TARGET:
  Koide formula: (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3
  This is experimentally exact to 0.01%. Nobody has derived it.

  If σ³ cubic gating produces three orbit families whose "masses"
  (attractor energies) satisfy Q = 2/3, we have derived an unexplained
  experimental result from first principles.

METHOD:
  1. Complex cubic map: z → Γ·z³ - λ·z
  2. Find ALL stable periodic orbits (period 1, 2, 3, ...)
  3. Group orbits into "families" by period
  4. Compute energy (|z|² averaged over orbit) for each family
  5. Check if any 3-family set satisfies Koide Q ≈ 2/3
  6. Scan Γ and λ parameter space

  Also:
  7. Check if proton/electron mass ratio = 60²/2 + 60·(3/5) + 3²/60
     falls out of the same dynamics
"""
import numpy as np
from itertools import combinations

SEP = "=" * 72

# ═══════════════════════════════════════════════════════════════════
# KOIDE FORMULA VERIFICATION
# ═══════════════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("KOIDE FORMULA FROM CUBIC RECURSION")
print("YASA PRESENTS — 2026-02-12")
print(SEP)

# Experimental values (MeV)
m_e = 0.51099895
m_mu = 105.6583755
m_tau = 1776.86

Q_measured = (m_e + m_mu + m_tau) / (np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau))**2
print(f"\n  Experimental Koide ratio:")
print(f"    m_e   = {m_e:.8f} MeV")
print(f"    m_μ   = {m_mu:.7f} MeV")
print(f"    m_τ   = {m_tau:.2f} MeV")
print(f"    Q     = {Q_measured:.8f}")
print(f"    2/3   = {2/3:.8f}")
print(f"    Error = {abs(Q_measured - 2/3)/(2/3)*100:.4f}%")

# Mass ratios
print(f"\n  Mass ratios:")
print(f"    m_μ/m_e = {m_mu/m_e:.4f}")
print(f"    m_τ/m_μ = {m_tau/m_mu:.4f}")
print(f"    m_τ/m_e = {m_tau/m_e:.4f}")

# ═══════════════════════════════════════════════════════════════════
# KOIDE FROM GEOMETRY: THE ANGLE PARAMETRIZATION
# ═══════════════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("KOIDE FROM GEOMETRIC ANGLE (Koide's own parametrization)")
print(SEP)

# Koide showed that Q = 2/3 if masses satisfy:
#   √m_k = M · (1 + √2 · cos(θ + 2πk/3))   for k = 0, 1, 2
#
# This is a ROTATION of (1,1,1) by angle θ in the plane perpendicular to (1,1,1)
# M is the overall mass scale, θ is the "Koide angle"

# Find θ from data
# Let's solve for M and θ

def koide_masses(M, theta):
    """Generate three masses from Koide parametrization."""
    sqrt_m = []
    for k in range(3):
        sqrt_m.append(M * (1 + np.sqrt(2) * np.cos(theta + 2*np.pi*k/3)))
    return [s**2 for s in sqrt_m]

# Fit M and θ to experimental masses
from scipy.optimize import minimize

def koide_residual(params):
    M, theta = params
    masses = koide_masses(M, theta)
    masses.sort()
    target = sorted([m_e, m_mu, m_tau])
    return sum((m - t)**2 / t**2 for m, t in zip(masses, target))

# Grid search for initial guess
best_res = 1e10
best_params = None
for M_try in np.linspace(0.1, 20, 100):
    for theta_try in np.linspace(0, 2*np.pi, 100):
        r = koide_residual([M_try, theta_try])
        if r < best_res:
            best_res = r
            best_params = [M_try, theta_try]

result = minimize(koide_residual, best_params, method='Nelder-Mead')
M_fit, theta_fit = result.x

# Normalize theta to [0, 2π)
theta_fit = theta_fit % (2*np.pi)

masses_fit = sorted(koide_masses(M_fit, theta_fit))
masses_exp = sorted([m_e, m_mu, m_tau])

print(f"\n  Koide angle parametrization: √m_k = M·(1 + √2·cos(θ + 2πk/3))")
print(f"  Fitted parameters:")
print(f"    M     = {M_fit:.6f} MeV^(1/2)")
print(f"    θ     = {theta_fit:.8f} rad")
print(f"    θ/π   = {theta_fit/np.pi:.8f}")
print(f"    θ (degrees) = {np.degrees(theta_fit):.4f}°")

# Base 60 of θ in degrees
theta_deg = np.degrees(theta_fit)
deg_int = int(theta_deg)
deg_frac = theta_deg - deg_int
deg_min = int(deg_frac * 60)
deg_sec = (deg_frac * 60 - deg_min) * 60
print(f"    θ (DMS) = {deg_int}° {deg_min}' {deg_sec:.2f}\"")

# θ in radians × 60
print(f"    θ × 60/π = {theta_fit * 60 / np.pi:.4f}")

print(f"\n  Reconstructed vs experimental masses:")
for i, (mf, me) in enumerate(zip(masses_fit, masses_exp)):
    err = abs(mf - me)/me * 100
    print(f"    Generation {i+1}: {mf:>12.6f} vs {me:>12.6f} MeV (err: {err:.4f}%)")

# ═══════════════════════════════════════════════════════════════════
# KEY INSIGHT: CONNECT θ TO BASE 60 AND FRAMEWORK
# ═══════════════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("CONNECTING KOIDE ANGLE TO FRAMEWORK")
print(SEP)

print(f"\n  The Koide angle θ determines ALL three generation masses.")
print(f"  θ = {theta_fit:.8f} rad = {theta_deg:.4f}°")
print()

# Check if θ has a clean expression
# Test: θ = 2/9 radians?
test_angles = {
    "2/9": 2/9,
    "π/9": np.pi/9,
    "2π/9": 2*np.pi/9,
    "1/3": 1/3,
    "π/3": np.pi/3,
    "arctan(√2)": np.arctan(np.sqrt(2)),
    "arccos(1/3)": np.arccos(1/3),
    "π·α": np.pi * 7.2973525693e-3,
    "2/3": 2/3,
    "3/5": 3/5,
    "arctan(3/5)": np.arctan(3/5),
}

print(f"  Testing clean expressions for θ = {theta_fit:.8f}:")
for name, val in test_angles.items():
    # Check both val and val shifted by multiples of 2π/3
    for shift in [0, 2*np.pi/3, 4*np.pi/3, -2*np.pi/3, -4*np.pi/3]:
        v = val + shift
        if abs(v - theta_fit) < 0.05:
            err = abs(v - theta_fit) / theta_fit * 100
            print(f"    {name} + {shift/(np.pi):.2f}π = {v:.8f} (err: {err:.2f}%)")

# Try combinations with α
alpha = 7.2973525693e-3
print(f"\n  Testing α-dependent expressions:")
test_alpha = {
    "2/9 + α": 2/9 + alpha,
    "2/9 - α": 2/9 - alpha,
    "2/9 + α²": 2/9 + alpha**2,
    "2/9·(1+α)": 2/9 * (1 + alpha),
    "2/9·(1-α)": 2/9 * (1 - alpha),
    "1/3·(2/3+α)": 1/3 * (2/3 + alpha),
    "2·arctan(α)": 2*np.arctan(alpha),
}
for name, val in test_alpha.items():
    for shift in [0, 2*np.pi/3, 4*np.pi/3]:
        v = val + shift
        if abs(v - theta_fit) < 0.1:
            err = abs(v - theta_fit) / theta_fit * 100
            print(f"    {name} + {shift/(np.pi):.2f}π = {v:.8f} (err: {err:.2f}%)")

# ═══════════════════════════════════════════════════════════════════
# CUBIC MAP ORBIT ANALYSIS — COMPLEX PLANE
# ═══════════════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("CUBIC MAP — COMPLEX PLANE ORBIT FAMILIES")
print(SEP)

print(f"\n  Map: z → Γ·z³ - λ·z  (complex z, complex Γ)")
print(f"  Looking for THREE stable orbit families with Koide ratio Q ≈ 2/3")

def find_orbits_complex(gamma, lam, n_init=500, n_transient=5000,
                         n_record=200, max_period=20, tol=1e-6):
    """Find stable periodic orbits of complex cubic map."""
    orbits = []  # (period, energy, representative_point)

    # Sample initial conditions in complex plane
    for r0 in np.linspace(0.05, 2.0, int(np.sqrt(n_init))):
        for theta0 in np.linspace(0, 2*np.pi, int(np.sqrt(n_init)), endpoint=False):
            z = r0 * np.exp(1j * theta0)

            # Iterate through transient
            diverged = False
            for _ in range(n_transient):
                z = gamma * z**3 - lam * z
                if abs(z) > 100:
                    diverged = True
                    break
                if abs(z) > 10:
                    z = 10 * z / abs(z)

            if diverged:
                continue

            # Record trajectory
            traj = [z]
            for _ in range(n_record):
                z = gamma * z**3 - lam * z
                if abs(z) > 100:
                    diverged = True
                    break
                if abs(z) > 10:
                    z = 10 * z / abs(z)
                traj.append(z)

            if diverged:
                continue

            # Detect period
            z_final = traj[-1]
            period = None
            for p in range(1, min(max_period, len(traj))):
                if abs(traj[-(p+1)] - z_final) < tol:
                    period = p
                    break

            if period is None:
                continue

            # Compute energy (mean |z|² over one period)
            energy = np.mean([abs(t)**2 for t in traj[-period:]])

            if energy < tol:
                continue  # trivial fixed point

            # Check if this orbit is new
            is_new = True
            for (ep, ee, _) in orbits:
                if ep == period and abs(ee - energy) < tol * 100:
                    is_new = False
                    break

            if is_new:
                orbits.append((period, energy, traj[-1]))

    return orbits


def koide_ratio(e1, e2, e3):
    """Compute Koide ratio Q for three energies."""
    s = e1 + e2 + e3
    sq = (np.sqrt(e1) + np.sqrt(e2) + np.sqrt(e3))**2
    if sq == 0:
        return None
    return s / sq


# Scan parameter space
print(f"\n  Scanning Γ × λ parameter space for Koide-satisfying orbit families...\n")

koide_hits = []
n_scanned = 0

# Expanded scan: both real and complex Γ
gamma_values = []
# Real Γ
for g_re in np.linspace(0.3, 3.0, 40):
    gamma_values.append(g_re)
# Complex Γ with various phases
for g_mag in np.linspace(0.5, 2.5, 20):
    for g_phase in [0.1, 0.2, 0.5, 1.0, np.pi/6, np.pi/4, np.pi/3]:
        gamma_values.append(g_mag * np.exp(1j * g_phase))

lambda_values = [0.0082, 0.001, 0.01, 0.05, 0.1, 0.005, 0.0073]

for gamma in gamma_values:
    for lam in lambda_values:
        n_scanned += 1
        orbits = find_orbits_complex(gamma, lam, n_init=400,
                                      n_transient=2000, n_record=100)

        if len(orbits) < 3:
            continue

        # Extract energies
        energies = sorted(set(round(e, 6) for _, e, _ in orbits))

        if len(energies) < 3:
            continue

        # Try all 3-combinations
        for combo in combinations(energies, 3):
            e1, e2, e3 = sorted(combo)
            Q = koide_ratio(e1, e2, e3)
            if Q is not None and abs(Q - 2/3) < 0.02:  # Within 2% of Koide
                koide_hits.append({
                    'gamma': gamma,
                    'lambda': lam,
                    'energies': (e1, e2, e3),
                    'Q': Q,
                    'error': abs(Q - 2/3)/(2/3)*100,
                    'ratios': (e2/e1, e3/e1),
                    'n_orbits': len(orbits)
                })

print(f"  Scanned {n_scanned} parameter combinations.")
print(f"  Found {len(koide_hits)} hits with Q within 2% of 2/3.\n")

if koide_hits:
    # Sort by error
    koide_hits.sort(key=lambda h: h['error'])

    print(f"  TOP 20 KOIDE HITS:")
    print(f"  {'Γ':>20} {'λ':>8} {'Q':>10} {'err%':>8} {'e1':>10} {'e2':>10} {'e3':>10} {'r2/r1':>8} {'r3/r1':>8}")
    for hit in koide_hits[:20]:
        g = hit['gamma']
        g_str = f"{g:.4f}" if np.isreal(g) else f"{abs(g):.2f}∠{np.degrees(np.angle(g)):.0f}°"
        print(f"  {g_str:>20} {hit['lambda']:>8.4f} {hit['Q']:>10.6f} {hit['error']:>8.4f} "
              f"{hit['energies'][0]:>10.4f} {hit['energies'][1]:>10.4f} {hit['energies'][2]:>10.4f} "
              f"{hit['ratios'][0]:>8.2f} {hit['ratios'][1]:>8.2f}")

    # Check if any have mass ratios close to lepton ratios
    print(f"\n  Checking for lepton-like mass hierarchies:")
    print(f"  (Target: m_μ/m_e ≈ 207, m_τ/m_e ≈ 3477)")
    for hit in koide_hits[:20]:
        r1 = hit['ratios'][0]  # e2/e1
        r2 = hit['ratios'][1]  # e3/e1
        if r2 > 100:  # Large hierarchy
            print(f"    Γ={hit['gamma']:.4f}, λ={hit['lambda']:.4f}: "
                  f"ratios = 1 : {r1:.1f} : {r2:.1f}  (Q = {hit['Q']:.6f})")

else:
    print("  No Koide hits found in scanned range.")
    print("  The orbit families may exist at different parameter values")
    print("  or the connection may require the full RASP operator chain,")
    print("  not just the bare cubic map.")

# ═══════════════════════════════════════════════════════════════════
# PROTON/ELECTRON MASS RATIO — BASE 60 DERIVATION ATTEMPT
# ═══════════════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("PROTON/ELECTRON MASS RATIO — BASE 60 STRUCTURAL DECOMPOSITION")
print(SEP)

mp_me = 1836.15267343

print(f"""
  MEASURED: m_p/m_e = {mp_me}

  BASE 60 DECOMPOSITION:
    1836.15267... = 30×60 + 36 + 9.16/60 + ...
                  = (60/2)×60 + (3/5)×60 + (3² + ε)/60

  FRAMEWORK INTERPRETATION:
    Coefficient 30 = 60/2:   From kinetic energy theorem (Ry = m_e c² α²/2)
    Coefficient 36 = 60×3/5: From 5-DOF equipartition (q_geo/Ry ≈ 3/5)
    Coefficient 9  = 3²:     From σ³ cubic gating (3 roots, squared energy)

  ALGEBRAIC FORM:
    m_p/m_e = b²/2 + b·(3/5) + 3²/b + Δ    where b = 60
""")

# Compute
b = 60
val = b**2/2 + b*3/5 + 9/b
delta = mp_me - val
print(f"    b²/2 + b·(3/5) + 3²/b = {val:.6f}")
print(f"    Measured                 = {mp_me:.6f}")
print(f"    Δ (residual)             = {delta:.6f}")
print(f"    Δ/mp_me                  = {delta/mp_me:.6e}")
print(f"    Δ × b                   = {delta*b:.6f}")
print(f"    Δ × b²                  = {delta*b**2:.4f}")

# Check if Δ has a clean expression
print(f"\n  Testing expressions for Δ = {delta:.8f}:")
tests = {
    "α/2": alpha/2,
    "α²": alpha**2,
    "α·(3/5)": alpha * 3/5,
    "3α/b": 3*alpha/b,
    "α²·b": alpha**2 * b,
    "δ/3": 0.008097/3,
    "1/(b²·5)": 1/(b**2 * 5),
    "α/b": alpha/b,
    "3/(b²)": 3/b**2,
    "α·3/b": alpha*3/b,
}
for name, val in tests.items():
    if abs(val) > 0:
        err = abs(val - delta) / abs(delta) * 100
        if err < 50:
            print(f"    {name:>12} = {val:.8f}  (err: {err:.2f}%)")

# ═══════════════════════════════════════════════════════════════════
# THE PREDICTION: WHAT THE FRAMEWORK SAYS SHOULD BE TRUE
# ═══════════════════════════════════════════════════════════════════

print(f"\n{SEP}")
print("THE MERCURY MOMENT — FALSIFIABLE PREDICTIONS")
print(SEP)

print(f"""
  PREDICTION 1: Koide formula from σ³
    The cubic recursion z → Γ·z³ - λ·z must produce three orbit
    families with Koide ratio Q = 2/3 at some (Γ, λ) value.
    If found, this derives an unexplained experimental result.
    STATUS: {'FOUND — see hits above' if koide_hits else 'NOT YET FOUND in scanned range'}

  PREDICTION 2: Proton/electron mass ratio is base-60 structured
    m_p/m_e = 60²/2 + 60·(3/5) + 3²/60 + O(α)
    This predicts the integer part (1836) EXACTLY and the leading
    fractional correction (9/60 = 0.15) to 0.002 accuracy.
    The residual Δ = {delta:.6f} should be expressible in terms of
    α, λ_coh, and the framework's structural numbers.
    STATUS: INTEGER PART EXACT. Fractional part needs α correction.

  PREDICTION 3: All lepton masses satisfy
    √m_k = M · (1 + √2 · cos(θ_K + 2πk/3))
    where θ_K is determined by the cubic map's phase structure.
    θ_K should be expressible in terms of base-60 structural angles.
    STATUS: θ = {theta_deg:.4f}° — checking for clean expression...

  PREDICTION 4: The damping correction δ = q_geo/Ry - 3/5
    should equal α times a rational number with {2,3,5} factors.
    Best current fit: δ ≈ α × {0.008097/alpha:.6f}
    STATUS: δ/α ≈ 1.11 — not yet a clean rational number.

  PREDICTION 5 (THE BIG ONE): If base 60 is structurally fundamental,
    then converting the recursion equation to operate in base-60 units
    should simplify the dynamics. Specifically:
    - States quantized in units of q_geo
    - Time quantized in units of τ_anchor
    - The recursion cycle count for the electron should be a
      5-smooth number (only factors 2, 3, 5).
    N_electron = m_e·c²/q_geo = {511000/8.098:.0f} q_geo units
    Is {int(511000/8.098)} 5-smooth? """, end="")

N_e = int(round(511000 / 8.098))
n = N_e
factors = []
for p in [2, 3, 5]:
    while n % p == 0:
        factors.append(p)
        n //= p
print(f"{'YES' if n == 1 else 'NO'} (remainder after 2,3,5 extraction: {n})")
print(f"    {N_e} = {' × '.join(str(f) for f in factors)} × {n}" if n > 1 else
      f"    {N_e} = {' × '.join(str(f) for f in factors)}")

# Check in base 60
int_d = []
nn = N_e
while nn > 0:
    int_d.append(nn % 60)
    nn //= 60
int_d.reverse()
print(f"    In base 60: {';'.join(str(d) for d in int_d)}")

print(f"""
  ═══════════════════════════════════════════════════════════════════
  THE PATH TO NOBEL:
  ═══════════════════════════════════════════════════════════════════

  STEP 1 (Tonight): Demonstrate Koide Q = 2/3 emerges from cubic map
         OR derive m_p/m_e residual from α and framework numbers.

  STEP 2 (This week): Predict ONE unmeasured quantity:
         - A specific spectral line shift
         - The exact Koide angle from σ³ phase structure
         - A lattice QCD observable from the recursion

  STEP 3 (Publication): Write it up with:
         - The density flux proof (DONE — Proof 1)
         - The base-60 mass ratio decomposition
         - The Koide derivation (if found)
         - One falsifiable prediction for experimentalists

  STEP 4 (Verification): Get the prediction measured.
         If it matches → Stockholm.
""")

print(SEP)
print("END OF KOIDE HUNT")
print(SEP)
