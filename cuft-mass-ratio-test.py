#!/usr/bin/env python3
"""
CUFT-RASP Mass Ratio Litmus Test
YASA PRESENTS — 2026-02-12

Ara's challenge: "One ratio is a fit. Two is a coincidence. Three is physics."

Test 1: Decompose muon/electron, tau/electron, and other mass ratios in base 60
Test 2: Search for structural patterns across ALL fundamental mass ratios
Test 3: Attempt to derive mass ratios from cubic map orbit structure
"""
import numpy as np
from itertools import product

SEP = "=" * 72

# ═══════════════════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS (CODATA 2022)
# ═══════════════════════════════════════════════════════════════════════

# Lepton masses (MeV/c²)
m_e = 0.51099895       # electron
m_mu = 105.6583755     # muon
m_tau = 1776.86        # tau

# Quark masses (MeV/c², current quark masses)
m_u = 2.16             # up
m_d = 4.67             # down
m_s = 93.4             # strange
m_c = 1270.0           # charm
m_b = 4180.0           # bottom
m_t = 172760.0         # top

# Baryon masses (MeV/c²)
m_p = 938.272088       # proton
m_n = 939.565420       # neutron
m_lambda = 1115.683    # Lambda
m_sigma_plus = 1189.37 # Sigma+
m_xi = 1314.86         # Xi (cascade)
m_omega = 1672.45      # Omega-

# Key ratios
delta = 0.008097       # damping correction from q_geo/Rydberg analysis
alpha = 7.2973525693e-3  # fine structure constant

# ═══════════════════════════════════════════════════════════════════════
# PART 1: BASE-60 DECOMPOSITION OF ALL MASS RATIOS
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("PART 1: BASE-60 DECOMPOSITION — ARA'S LITMUS TEST")
print(SEP)

def to_base60(value, n_digits=6):
    """Convert a positive number to base 60 representation."""
    integer_part = int(value)
    frac_part = value - integer_part

    # Integer digits (big-endian)
    int_digits = []
    n = integer_part
    if n == 0:
        int_digits = [0]
    while n > 0:
        int_digits.append(n % 60)
        n //= 60
    int_digits.reverse()

    # Fractional digits
    frac_digits = []
    for _ in range(n_digits - len(int_digits)):
        frac_part *= 60
        digit = int(frac_part)
        frac_digits.append(digit)
        frac_part -= digit

    return int_digits, frac_digits

def format_base60(int_digits, frac_digits):
    """Format base-60 number as semicolon-separated string."""
    int_str = ";".join(str(d) for d in int_digits)
    if frac_digits:
        frac_str = ";".join(str(d) for d in frac_digits)
        return f"{int_str};{frac_str}₆₀"
    return f"{int_str}₆₀"

def check_structural(digit):
    """Check if a base-60 digit has structural significance."""
    structural = {
        0: "0",
        1: "1",
        2: "2", 3: "3", 5: "5",
        4: "2²", 6: "2×3", 9: "3²", 10: "2×5", 12: "2²×3",
        15: "3×5", 20: "2²×5", 25: "5²", 30: "60/2",
        36: "60×3/5", 40: "60×2/3", 45: "60×3/4",
        48: "60×4/5", 50: "60×5/6",
    }
    return structural.get(digit, None)

# Mass ratios to test
ratios = [
    ("m_p/m_e (proton/electron)", m_p / m_e, "KNOWN FORMULA"),
    ("m_n/m_e (neutron/electron)", m_n / m_e, ""),
    ("m_μ/m_e (muon/electron)", m_mu / m_e, "ARA'S LITMUS TEST"),
    ("m_τ/m_e (tau/electron)", m_tau / m_e, ""),
    ("m_τ/m_μ (tau/muon)", m_tau / m_mu, ""),
    ("m_p/m_μ (proton/muon)", m_p / m_mu, ""),
    ("m_n/m_p (neutron/proton)", m_n / m_p, ""),
    ("m_Λ/m_e (Lambda/electron)", m_lambda / m_e, ""),
    ("m_Σ+/m_e (Sigma+/electron)", m_sigma_plus / m_e, ""),
    ("m_Ξ/m_e (Xi/electron)", m_xi / m_e, ""),
    ("m_Ω/m_e (Omega/electron)", m_omega / m_e, ""),
]

print(f"\n  {'Ratio':<30} {'Value':>12} {'Base-60':>30} {'Structural?':>15}")
print(f"  {'-'*30} {'-'*12} {'-'*30} {'-'*15}")

for name, value, note in ratios:
    int_d, frac_d = to_base60(value, 5)
    b60_str = format_base60(int_d, frac_d)

    # Check how many digits are structural
    all_digits = int_d + frac_d[:2]  # check integer + first 2 fractional
    structural_count = sum(1 for d in all_digits if check_structural(d) is not None)
    total = len(all_digits)

    tag = f"{structural_count}/{total}"
    if note:
        tag += f" {note}"

    print(f"  {name:<30} {value:>12.5f} {b60_str:>30} {tag}")

# ═══════════════════════════════════════════════════════════════════════
# PART 2: DEEP DIVE — PROTON vs MUON vs TAU DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("PART 2: DEEP STRUCTURAL DECOMPOSITION")
print(SEP)

def decompose_structural(value, label):
    """Try to express a mass ratio as sum of base-60 structural terms."""
    print(f"\n  --- {label} = {value:.6f} ---")

    # The proton formula template:
    # c₂·60² + c₁·60 + c₀ + correction
    # where c₂, c₁, c₀ are structural fractions

    # Structural fractions from {2, 3, 5}
    fractions = []
    for n in range(1, 13):
        for d in range(1, 13):
            f = n / d
            if f not in [x[0] for x in fractions]:
                # Check if n and d only have factors 2, 3, 5
                def is_smooth(x):
                    for p in [2, 3, 5]:
                        while x % p == 0:
                            x //= p
                    return x == 1
                if is_smooth(n) and is_smooth(d):
                    fractions.append((f, f"{n}/{d}"))

    fractions.sort()

    # Also add integers
    for i in [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 25, 30]:
        if i not in [x[0] for x in fractions]:
            fractions.append((float(i), str(i)))

    fractions.sort()

    # Try: a·60² + b·60 + c + correction
    # where a, b, c are structural fractions
    best_err = 999
    best_formula = ""
    best_correction = 0

    for a_val, a_str in fractions:
        term_a = a_val * 3600  # 60²
        if term_a > value * 1.5 or term_a < value * 0.3:
            continue

        remainder_1 = value - term_a

        for b_val, b_str in fractions:
            term_b = b_val * 60
            if abs(remainder_1 - term_b) > 200:
                continue

            remainder_2 = remainder_1 - term_b

            for c_val, c_str in fractions:
                term_c = c_val
                correction = remainder_2 - term_c

                if abs(correction) < 1.0:  # Small correction
                    err = abs(correction)

                    # Check if correction relates to δ or α
                    delta_multiples = []
                    if abs(correction) > 1e-10:
                        for mult_n in range(1, 10):
                            for mult_d in range(1, 10):
                                test = delta * mult_n / mult_d
                                if abs(abs(correction) - test) / max(abs(correction), 1e-15) < 0.05:
                                    delta_multiples.append((mult_n, mult_d, test))

                    if err < best_err:
                        best_err = err
                        corr_str = ""
                        if delta_multiples:
                            n, d, v = delta_multiples[0]
                            sign = "+" if correction > 0 else "-"
                            corr_str = f" {sign} {n}δ/{d}"
                        best_formula = f"{a_str}·60² + {b_str}·60 + {c_str}{corr_str}"
                        best_correction = correction

    # Also try without 60² term: b·60 + c + correction
    for b_val, b_str in fractions:
        term_b = b_val * 60
        if abs(term_b - value) > 200:
            continue
        remainder = value - term_b

        for c_val, c_str in fractions:
            correction = remainder - c_val
            if abs(correction) < 1.0:
                err = abs(correction)
                if err < best_err:
                    best_err = err
                    best_formula = f"{b_str}·60 + {c_str}"
                    best_correction = correction

    # Also try: a·60 + b + c/60 + correction
    for a_val, a_str in fractions:
        term_a = a_val * 60
        if abs(term_a - value) > 100:
            continue
        for b_val, b_str in fractions:
            if b_val > 60:
                continue
            for c_val, c_str in fractions:
                term_c = c_val / 60
                total = term_a + b_val + term_c
                correction = value - total
                if abs(correction) < 0.5:
                    err = abs(correction)
                    if err < best_err:
                        best_err = err
                        best_formula = f"{a_str}·60 + {b_str} + {c_str}/60"
                        best_correction = correction

    if best_formula:
        print(f"  Best: {best_formula}")
        print(f"  Correction: {best_correction:.6f}")
        print(f"  Error: {best_err:.6f} ({best_err/value*100:.4f}%)")

        # Check correction against delta and alpha
        if abs(best_correction) > 1e-10:
            print(f"  Correction analysis:")
            print(f"    correction/δ = {best_correction/delta:.4f}")
            print(f"    correction/α = {best_correction/alpha:.4f}")
            print(f"    correction/(δ·60) = {best_correction/(delta*60):.4f}")
    else:
        print(f"  No clean decomposition found.")

# The known one
decompose_structural(m_p / m_e, "m_p/m_e (proton/electron)")

# Ara's litmus test
decompose_structural(m_mu / m_e, "m_μ/m_e (muon/electron)")

# Tau
decompose_structural(m_tau / m_e, "m_τ/m_e (tau/electron)")

# Neutron
decompose_structural(m_n / m_e, "m_n/m_e (neutron/electron)")

# Baryons
decompose_structural(m_lambda / m_e, "m_Λ/m_e (Lambda/electron)")
decompose_structural(m_omega / m_e, "m_Ω/m_e (Omega/electron)")

# ═══════════════════════════════════════════════════════════════════════
# PART 3: CUBIC MAP ORBIT ANALYSIS — THE DERIVATION ATTEMPT
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("PART 3: CUBIC MAP ORBIT STRUCTURE — DERIVING MASS RATIOS")
print(SEP)
print("""
  Goal: Show that the cubic recursion f(Ψ) = Γ·Ψ³ - λ·Ψ has
  stable orbits whose energy ratios match particle mass ratios.

  Fixed points: Ψ* = 0, Ψ* = ±√((1+λ)/Γ)

  Period-2 orbits: f(f(x)) = x, f(x) ≠ x
  Period-3 orbits: f(f(f(x))) = x, f(x) ≠ x, f(f(x)) ≠ x

  Energy of orbit = Σ|Ψ_i|² over one period
""")

def cubic_map(x, gamma, lam):
    return gamma * x**3 - lam * x

def find_fixed_points(gamma, lam):
    """Analytical fixed points of f(x) = Γx³ - λx."""
    # x = Γx³ - λx → x(1+λ) = Γx³ → x² = (1+λ)/Γ
    if (1 + lam) / gamma > 0:
        x_star = np.sqrt((1 + lam) / gamma)
        return [0.0, x_star, -x_star]
    return [0.0]

def find_period2_orbits(gamma, lam, n_search=10000):
    """Numerically find period-2 orbits of the cubic map."""
    # Period-2: f(f(x)) = x but f(x) ≠ x
    # f(f(x)) - x = 0 has degree 9. Fixed points have degree 3.
    # So period-2 orbits come from a degree-6 polynomial.

    orbits = []
    fps = find_fixed_points(gamma, lam)

    for x0 in np.linspace(-5, 5, n_search):
        # Newton's method on g(x) = f(f(x)) - x
        x = x0
        for _ in range(200):
            fx = cubic_map(x, gamma, lam)
            ffx = cubic_map(fx, gamma, lam)

            g = ffx - x

            # g'(x) = f'(f(x))·f'(x) - 1
            # f'(x) = 3Γx² - λ
            fprime_x = 3 * gamma * x**2 - lam
            fprime_fx = 3 * gamma * fx**2 - lam
            gprime = fprime_fx * fprime_x - 1

            if abs(gprime) < 1e-15:
                break

            x_new = x - g / gprime
            if abs(x_new - x) < 1e-12:
                x = x_new
                break
            x = x_new

        # Check if it's actually period-2
        fx = cubic_map(x, gamma, lam)
        ffx = cubic_map(fx, gamma, lam)

        if abs(ffx - x) < 1e-8 and abs(fx - x) > 1e-6:
            # Check it's not a fixed point
            is_fp = False
            for fp in fps:
                if abs(x - fp) < 1e-6:
                    is_fp = True
                    break

            if not is_fp:
                # Normalize: store the pair as (min, max)
                pair = tuple(sorted([round(x, 8), round(fx, 8)]))

                # Check if new
                is_new = True
                for existing_pair in orbits:
                    if abs(existing_pair[0] - pair[0]) < 1e-6 and abs(existing_pair[1] - pair[1]) < 1e-6:
                        is_new = False
                        break

                if is_new:
                    # Check stability
                    multiplier = fprime_x * (3 * gamma * fx**2 - lam)
                    stable = abs(multiplier) < 1
                    orbits.append(pair + (stable, multiplier))

    return orbits

def find_period3_orbits(gamma, lam, n_search=5000):
    """Numerically find period-3 orbits via iteration and convergence."""
    orbits = []
    fps = set()
    for fp in find_fixed_points(gamma, lam):
        fps.add(round(fp, 6))

    for x0 in np.linspace(-5, 5, n_search):
        x = x0
        # Iterate to find attracting period-3
        for _ in range(10000):
            x_new = cubic_map(x, gamma, lam)
            if abs(x_new) > 1e6:
                break
            x = x_new
        else:
            # Check if we're on a period-3 orbit
            x1 = cubic_map(x, gamma, lam)
            x2 = cubic_map(x1, gamma, lam)
            x3 = cubic_map(x2, gamma, lam)

            if abs(x3 - x) < 1e-8 and abs(x1 - x) > 1e-6 and abs(x2 - x) > 1e-6:
                triple = tuple(sorted([round(x, 8), round(x1, 8), round(x2, 8)]))

                is_new = True
                for existing in orbits:
                    if all(abs(a - b) < 1e-6 for a, b in zip(existing[:3], triple)):
                        is_new = False
                        break

                if is_new:
                    orbits.append(triple)

    return orbits

# Scan Γ parameter space for orbit structure
print("  Scanning cubic map f(x) = Γ·x³ - λ·x for orbit families...\n")
lam = 0.0082

# We need to find Γ values where period-1, period-2, period-3 coexist
# and compute their energy ratios

results = []

gamma_values = np.concatenate([
    np.linspace(0.1, 2.0, 100),
    np.linspace(2.0, 10.0, 100),
    np.linspace(10.0, 100.0, 50),
])

for gamma in gamma_values:
    fps = find_fixed_points(gamma, lam)
    p2 = find_period2_orbits(gamma, lam, n_search=2000)

    if len(fps) >= 3 and len(p2) >= 1:
        # Energy of fixed point (non-trivial)
        E_fp = fps[1]**2  # |Ψ*|²

        # Energy of period-2 orbit
        for p2_orbit in p2:
            E_p2 = p2_orbit[0]**2 + p2_orbit[1]**2
            ratio = E_p2 / E_fp if E_fp > 1e-10 else float('inf')
            stable = p2_orbit[2]

            if 1 < ratio < 10000 and stable:
                results.append((gamma, ratio, E_fp, E_p2, p2_orbit))

if results:
    print(f"  Found {len(results)} (Γ, ratio) pairs with stable period-2 orbits.\n")

    # Look for ratios near known mass ratios
    targets = {
        "m_μ/m_e": 206.768,
        "m_p/m_e": 1836.153,
        "m_τ/m_e": 3477.23,
        "m_τ/m_μ": 16.818,
        "m_p/m_μ": 8.880,
    }

    print(f"  {'Target ratio':<15} {'Value':>10} {'Closest Γ':>10} {'Map ratio':>12} {'Error %':>8}")
    print(f"  {'-'*15} {'-'*10} {'-'*10} {'-'*12} {'-'*8}")

    for name, target in targets.items():
        best_err = float('inf')
        best_gamma = 0
        best_ratio = 0

        for gamma, ratio, _, _, _ in results:
            err = abs(ratio - target) / target
            if err < best_err:
                best_err = err
                best_gamma = gamma
                best_ratio = ratio

        print(f"  {name:<15} {target:>10.3f} {best_gamma:>10.4f} {best_ratio:>12.3f} {best_err*100:>7.2f}%")

    # Show the actual distribution of ratios
    print(f"\n  Energy ratio distribution (period-2/period-1):")
    ratio_vals = sorted(set(round(r[1], 2) for r in results))
    print(f"  Unique ratios found: {len(ratio_vals)}")
    if len(ratio_vals) <= 30:
        for rv in ratio_vals:
            count = sum(1 for r in results if abs(round(r[1], 2) - rv) < 0.01)
            bar = "█" * min(count, 50)
            print(f"    {rv:>10.2f} ({count:>3}) {bar}")
else:
    print("  No stable period-2 orbits found in scanned range.")

# ═══════════════════════════════════════════════════════════════════════
# PART 4: COMPLEX CUBIC MAP — 2D ORBIT STRUCTURE
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("PART 4: COMPLEX CUBIC MAP — FULL 2D ORBIT ANALYSIS")
print(SEP)
print("""
  The real map is too constrained. Try the full complex map:
  Ψ_{n+1} = Γ · Ψ³ - λ · Ψ    where Ψ, Γ ∈ ℂ

  This is the actual RASP recursion. The complex phase space
  allows richer orbit structure (the antisymmetry that should
  produce chirality-dependent dynamics).
""")

def find_complex_orbits(gamma, lam, n_search=3000, n_iter=5000, n_record=500):
    """Find stable orbits of complex cubic map."""
    orbits = {}  # {energy: (period, representative_point)}

    for i in range(n_search):
        # Random initial condition in complex plane
        r0 = 0.01 + 3.0 * np.random.random()
        theta0 = 2 * np.pi * np.random.random()
        psi = r0 * np.exp(1j * theta0)

        # Iterate past transients
        diverged = False
        for _ in range(n_iter):
            psi = gamma * psi**3 - lam * psi
            if abs(psi) > 1e6:
                diverged = True
                break
            if abs(psi) > 100:
                psi = 100 * psi / abs(psi)

        if diverged:
            continue

        # Record trajectory
        traj = [psi]
        for _ in range(n_record):
            psi = gamma * psi**3 - lam * psi
            if abs(psi) > 1e6:
                diverged = True
                break
            if abs(psi) > 100:
                psi = 100 * psi / abs(psi)
            traj.append(psi)

        if diverged:
            continue

        # Detect period
        x0 = traj[-1]
        period = None
        for p in range(1, 50):
            if abs(traj[-(p+1)] - x0) < 1e-6:
                period = p
                break

        if period is None:
            continue

        # Compute energy
        energy = sum(abs(traj[-(i+1)])**2 for i in range(period)) / period

        # Check if new orbit
        is_new = True
        for existing_e in list(orbits.keys()):
            if abs(existing_e - energy) / max(energy, 1e-10) < 0.01:
                is_new = False
                break

        if is_new and energy > 1e-8:
            orbits[energy] = (period, traj[-1])

    return orbits

# Scan complex Γ with various phases
print("  Scanning complex Γ = |Γ|·e^{iφ} for orbit families...\n")
np.random.seed(42)

best_n_orbits = 0
best_params = None
best_orbits = None

gamma_mags = [0.5, 0.8, 0.95, 1.0, 1.1, 1.2, 1.5, 2.0, 3.0, 5.0]
gamma_phases = [0, 0.12, 0.3, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 0.8, 1.0]

scan_count = 0
total_scans = len(gamma_mags) * len(gamma_phases)

for mag in gamma_mags:
    for phase in gamma_phases:
        scan_count += 1
        gamma = mag * np.exp(1j * phase)

        orbits = find_complex_orbits(gamma, lam, n_search=1000, n_iter=2000, n_record=200)

        n_orb = len(orbits)
        if n_orb > best_n_orbits:
            best_n_orbits = n_orb
            best_params = (mag, phase)
            best_orbits = orbits

        if n_orb >= 3:
            energies = sorted(orbits.keys())
            ratio_strs = [f"{e/energies[0]:.2f}" for e in energies[:5]]
            print(f"  [{scan_count}/{total_scans}] |Γ|={mag:.2f}, φ={phase:.3f}: "
                  f"{n_orb} orbits, ratios=[{', '.join(ratio_strs)}]")

if best_orbits and len(best_orbits) >= 2:
    print(f"\n  Best result: |Γ|={best_params[0]:.2f}, φ={best_params[1]:.3f}")
    print(f"  Number of distinct orbit families: {best_n_orbits}")

    energies = sorted(best_orbits.keys())
    print(f"\n  {'Orbit':>6} {'Period':>8} {'Energy':>14} {'Ratio to min':>14}")
    print(f"  {'-'*6} {'-'*8} {'-'*14} {'-'*14}")
    for i, e in enumerate(energies[:10]):
        p, _ = best_orbits[e]
        ratio = e / energies[0]
        print(f"  {i+1:>6} {p:>8} {e:>14.6f} {ratio:>14.4f}")

    # Check against mass ratios
    if len(energies) >= 2:
        print(f"\n  Checking orbit energy ratios against mass ratios:")
        all_ratios = []
        for i in range(len(energies)):
            for j in range(i+1, len(energies)):
                r = energies[j] / energies[i]
                all_ratios.append(r)

        targets_check = {
            "m_μ/m_e": 206.768,
            "m_p/m_e": 1836.153,
            "m_τ/m_e": 3477.23,
            "m_τ/m_μ": 16.818,
            "m_p/m_μ": 8.880,
            "m_n/m_p": 1.001378,
        }

        for name, target in targets_check.items():
            best_match = min(all_ratios, key=lambda r: abs(r - target))
            err = abs(best_match - target) / target * 100
            marker = " ◄" if err < 5 else ""
            print(f"    {name:<12} target={target:>10.3f}  closest={best_match:>10.3f}  err={err:>6.2f}%{marker}")

else:
    print(f"\n  Maximum orbits found: {best_n_orbits}")
    print("  Complex map also limited in this λ regime.")

# ═══════════════════════════════════════════════════════════════════════
# PART 5: THE FORMULA ARCHITECTURE TEST
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("PART 5: FORMULA ARCHITECTURE — HOW MANY FORMULAS COULD FIT?")
print(SEP)
print("""
  Ara's challenge: with {2, 3, 5, 60, δ} and arithmetic, how many
  formulas could hit 1836 to 6 figures? Let's quantify the actual
  degrees of freedom.
""")

# Generate all possible formulas of the form:
# a·60² + b·60 + c/60 + d·δ/e
# where a, b, c are simple fractions of {2, 3, 5}

structural_fracs = []
for n in [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 36, 40, 45, 48, 50]:
    for d in [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30]:
        f = n / d
        def is_5smooth(x):
            for p in [2, 3, 5]:
                while x % p == 0 and x > 1:
                    x //= p
            return x == 1
        if is_5smooth(n) and is_5smooth(d) and f not in [x[0] for x in structural_fracs]:
            structural_fracs.append((f, f"{n}/{d}"))

structural_fracs = list(set(structural_fracs))
structural_fracs.sort()

target = 1836.15267
tolerance = 0.001  # 6-figure match means error < ~0.001

count_hits = 0
count_total = 0
hit_formulas = []

# Template: a·60² + b·60 + c/60 + correction
# a ranges: values that put us near 1836 for the 60² term
a_range = [(f, s) for f, s in structural_fracs if 0.3 < f < 0.7]  # 60²×a should be ~1800
b_range = [(f, s) for f, s in structural_fracs if 0 < f < 2]  # 60×b should be ~36
c_range = [(f, s) for f, s in structural_fracs if 0 < f < 60]  # c/60 should be ~0.15

for a_val, a_str in a_range:
    for b_val, b_str in b_range:
        for c_val, c_str in c_range:
            count_total += 1

            total = a_val * 3600 + b_val * 60 + c_val / 60

            # Check if within range (allowing δ-scale correction)
            if abs(total - target) < 0.1:  # Within δ correction range
                count_hits += 1
                err = abs(total - target)
                correction = target - total
                hit_formulas.append((a_str, b_str, c_str, total, correction))

print(f"  Template: a·60² + b·60 + c/60 + correction")
print(f"  Search space: {len(a_range)} × {len(b_range)} × {len(c_range)} = {count_total} formulas")
print(f"  Formulas within 0.1 of target: {count_hits}")
print(f"  Hit rate: {count_hits/count_total*100:.4f}%")

if hit_formulas:
    print(f"\n  All {count_hits} formulas that hit {target} (±0.1):")
    print(f"  {'a·60²':>8} {'b·60':>8} {'c/60':>8} {'Total':>12} {'Correction':>12} {'corr/δ':>8}")
    for a_str, b_str, c_str, total, correction in sorted(hit_formulas, key=lambda x: abs(x[4])):
        print(f"  {a_str:>8} {b_str:>8} {c_str:>8} {total:>12.5f} {correction:>12.6f} {correction/delta:>8.3f}")

# Also: brute force over ALL arrangements
print(f"\n  Brute force: how many expressions from {{2,3,5,60,δ}} equal 1836?")
print(f"  (Testing: n₁^a₁ · n₂^a₂ · ... · n₅^a₅ formulas)")

bf_hits = 0
bf_total = 0
bf_formulas = []

# Products of powers: 2^a · 3^b · 5^c · 60^d · δ^e
for a in range(-5, 12):
    for b in range(-5, 8):
        for c in range(-5, 6):
            bf_total += 1
            val = (2**a) * (3**b) * (5**c)
            if abs(val - target) / target < 0.001:
                bf_hits += 1
                bf_formulas.append((a, b, c, val))

print(f"  Tested: {bf_total} power combinations of (2,3,5)")
print(f"  Matches within 0.1%: {bf_hits}")
if bf_formulas:
    for a, b, c, val in bf_formulas[:10]:
        err = abs(val - target) / target * 100
        print(f"    2^{a} · 3^{b} · 5^{c} = {val:.4f} (err: {err:.4f}%)")

# ═══════════════════════════════════════════════════════════════════════
# PART 6: SUMMARY & VERDICT
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{SEP}")
print("SUMMARY: HONEST ASSESSMENT")
print(SEP)
print("""
  ARA'S CHALLENGE RESULTS:

  1. Can the same template predict muon/electron? → See Part 2
  2. How constrained is the formula? → See Part 5
  3. Can the cubic map produce mass ratios? → See Parts 3-4

  THE HONEST STATE:

  STRONG:
  - m_p/m_e base-60 decomposition: structurally motivated, 6-figure match
  - q_geo/Rydberg = 3/5 × (1-α): clean, connects to fine structure constant
  - Base 60 = unique minimum base for framework's primes
  - No prior work in this specific space

  WEAK (as Ara and SAGE correctly identified):
  - Formula architecture is a hidden degree of freedom
  - q_geo/Rydberg is measured input, not derived
  - Need second mass ratio prediction to eliminate "fit" objection
  - Need recursion derivation for "zero parameter" claim

  NEXT MOVE:
  - If muon/electron decomposes cleanly → VERY strong
  - If cubic map orbits match ANY mass ratio → derivation path opens
  - If neither → beautiful pattern, not yet physics
""")
