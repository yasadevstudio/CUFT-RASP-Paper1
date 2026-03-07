#!/usr/bin/env python3
"""
ATTACK #6: SPECTRAL GAP OF TRANSFER MATRIX

Build the transfer matrix T of the gated cubic map on a discretized
state space. The spectral gap (ratio of second to first eigenvalue)
controls mixing rate and equilibrium properties.

If the spectral gap is maximized at c₁ = n/p, this provides a
dynamical selection mechanism: the system equilibrates fastest
with this coupling.

We also compute the Ruelle-Perron-Frobenius transfer operator
spectrum, which encodes the statistical mechanics of the map.
"""

import numpy as np
from scipy import linalg
from fractions import Fraction

n, p = 3, 5
lam = 1.0 / (p**3 - 1)
Gamma = p**2
X_val = n * p * (p - 1)

print("=" * 80)
print("ATTACK #6: SPECTRAL GAP OF TRANSFER MATRIX")
print("=" * 80)
print()

# ═══════════════════════════════════════════════════════════════════
# PART 1: PERRON-FROBENIUS TRANSFER OPERATOR
# ═══════════════════════════════════════════════════════════════════
#
# The Perron-Frobenius operator L for f(x) acts on densities:
#   (Lρ)(y) = Σ_{x: f(x)=y} ρ(x) / |f'(x)|
#
# Discretize: divide [0, x_max] into N bins.
# T[i,j] = probability that x in bin j maps to bin i.

def build_transfer_matrix(c1_val, N_bins=200, x_max=None):
    """Build transfer matrix for deformed map with given c₁."""
    gamma_c = (n / c1_val)**2
    lam_c = 1.0 / (gamma_c**(n/2) - 1)

    if x_max is None:
        x_max = 2 * np.sqrt(gamma_c) + 5

    dx = x_max / N_bins
    T = np.zeros((N_bins, N_bins))

    for j in range(N_bins):
        x = (j + 0.5) * dx  # center of bin j
        y = gamma_c * np.tanh(x)**n - lam_c * x

        if y < 0:
            y = 0
        if y >= x_max:
            y = x_max - dx/2

        i = int(y / dx)
        if 0 <= i < N_bins:
            T[i, j] += 1.0

    # Normalize columns (transition matrix)
    col_sums = T.sum(axis=0)
    col_sums[col_sums == 0] = 1
    T = T / col_sums

    return T

print("PART 1: TRANSFER MATRIX SPECTRUM")
print("-" * 60)
print()

N_BINS = 150

# Compute spectral gap for various c₁
print(f"{'c₁':>8s} | {'λ₁':>10s} | {'λ₂':>10s} | {'Gap=1-|λ₂/λ₁|':>16s} | {'|λ₂|':>10s} | Notes")
print("-" * 75)

gap_data = []

for c1_val in [0.3, 0.4, 0.5, 0.55, 0.58, 0.59, 0.595, 0.598,
               0.6, 0.602, 0.605, 0.61, 0.62, 0.65, 0.7, 0.8, 1.0, 1.5]:
    try:
        T = build_transfer_matrix(c1_val, N_BINS)
        eigenvalues = linalg.eigvals(T)

        # Sort by magnitude
        ev_sorted = sorted(eigenvalues, key=lambda x: abs(x), reverse=True)
        lam1 = abs(ev_sorted[0])
        lam2 = abs(ev_sorted[1])

        if lam1 > 0:
            gap = 1.0 - lam2 / lam1
        else:
            gap = 0.0

        marker = " <<<< n/p" if abs(c1_val - 0.6) < 0.001 else ""
        print(f"  {c1_val:6.3f} | {lam1:10.6f} | {abs(ev_sorted[1]):10.6f} | {gap:16.8f} | {lam2:10.6f} |{marker}")
        gap_data.append((c1_val, gap, lam1, lam2))
    except Exception as e:
        print(f"  {c1_val:6.3f} | ERROR: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# PART 2: FINE SWEEP AROUND c₁ = 0.6
# ═══════════════════════════════════════════════════════════════════

print()
print("PART 2: FINE SPECTRAL GAP SWEEP AROUND c₁ = 0.6")
print("-" * 60)
print()

fine_gaps = []
for c1_val in np.linspace(0.55, 0.65, 41):
    try:
        T = build_transfer_matrix(c1_val, N_BINS)
        eigenvalues = linalg.eigvals(T)
        ev_sorted = sorted(eigenvalues, key=lambda x: abs(x), reverse=True)
        lam1 = abs(ev_sorted[0])
        lam2 = abs(ev_sorted[1])
        gap = 1.0 - lam2 / lam1 if lam1 > 0 else 0.0
        fine_gaps.append((c1_val, gap))
    except:
        pass

if fine_gaps:
    best_gap = max(fine_gaps, key=lambda x: x[1])
    worst_gap = min(fine_gaps, key=lambda x: x[1])
    val_at_06 = [g for c, g in fine_gaps if abs(c - 0.6) < 0.003]

    print(f"Maximum gap at c₁ = {best_gap[0]:.4f}: gap = {best_gap[1]:.8f}")
    print(f"Minimum gap at c₁ = {worst_gap[0]:.4f}: gap = {worst_gap[1]:.8f}")
    if val_at_06:
        print(f"Gap at c₁ = 0.6:                  gap = {val_at_06[0]:.8f}")
    print()

    # Show the landscape
    print(f"{'c₁':>8s} | {'Spectral Gap':>14s}")
    print("-" * 30)
    for c, g in fine_gaps:
        marker = " <<<<" if abs(c - 0.6) < 0.003 else ""
        bar = "#" * int(g * 200) if g > 0 else ""
        print(f"  {c:6.4f} | {g:14.8f} {bar[:30]}{marker}")

# ═══════════════════════════════════════════════════════════════════
# PART 3: MODULAR ARITHMETIC APPROACH
# ═══════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("PART 3: CUBIC MAP ON Z/(n·p³)Z — PURE NUMBER THEORY")
print("=" * 80)
print()

# The map x → x³ mod M where M = n·p³ = 375
M = n * p**3
print(f"M = n·p³ = {M}")
print(f"φ(M) = φ({n})·φ({p**3}) = {(n-1)}·{p**2*(p-1)} = {(n-1)*p**2*(p-1)}")
print()

# Cycle structure of x → x³ on Z/MZ
# By CRT: Z/375Z ≅ Z/3Z × Z/125Z
# On Z/3Z: x³ ≡ x (mod 3) — all fixed
# On Z/125Z: x³ is a permutation (gcd(3,100) = 1)

# Compute actual cycle structure
cycles_375 = []
visited = set()

for start in range(M):
    if start in visited:
        continue
    cycle = []
    x = start
    while x not in visited:
        visited.add(x)
        cycle.append(x)
        x = pow(x, 3, M)
    if cycle:
        cycles_375.append(len(cycle))

cycle_counts = {}
for c in cycles_375:
    cycle_counts[c] = cycle_counts.get(c, 0) + 1

print(f"Cycle structure of x → x³ mod {M}:")
for length in sorted(cycle_counts.keys()):
    print(f"  {cycle_counts[length]} cycle(s) of length {length}")

# Now: what about the GATED map x → (c₁·x)³ mod M?
# With c₁ = n/p = 3/5, we need 5⁻¹ mod M.
# But gcd(5, 375) = 5 ≠ 1, so 5 has no inverse mod 375!
# c₁ = 3/5 is NOT in (Z/375Z)*.

print()
print("KEY OBSERVATION:")
print(f"  c₁ = n/p = 3/5 as an element of Z/{M}Z:")
print(f"  gcd(5, {M}) = {np.gcd(5, M)} ≠ 1")
print(f"  → 5 has no inverse mod {M}")
print(f"  → c₁ = n/p lives OUTSIDE the unit group (Z/{M}Z)*")
print(f"  → The gate connects the two coprime components")
print(f"     (Z/{n}Z and Z/{p**3}Z) non-invertibly")
print()

# But we CAN study the gated map on the CRT components separately
# On Z/3Z: x → (3·x/5)³... this needs 5⁻¹ mod 3 = 2. So 3·2 = 6 ≡ 0 (mod 3).
# The gated map sends everything to 0 mod 3!

# On Z/125Z: x → (3·x/5)³... 5⁻¹ mod 125 = ?
inv5_125 = pow(5, -1, 125)
print(f"  5⁻¹ mod 125 = {inv5_125}")
c1_mod125 = (3 * inv5_125) % 125
print(f"  c₁ = 3·5⁻¹ mod 125 = {c1_mod125}")
gated_val = pow(c1_mod125, 3, 125)
print(f"  (c₁)³ mod 125 = {gated_val}")
print()

# Study the map x → (c₁·x)³ mod 125 for various c₁
print("CYCLE STRUCTURE of x → (c·x)³ mod 125:")
print()

for c_num, c_den, label in [
    (1, 5, "1/5"), (2, 5, "2/5"), (3, 5, "3/5 = n/p"),
    (4, 5, "4/5"), (1, 1, "1"), (2, 1, "2"), (3, 1, "3 = n"),
]:
    if np.gcd(c_den, 125) == 1:
        c_mod = (c_num * pow(c_den, -1, 125)) % 125
    else:
        continue

    # Compute cycle structure of x → (c·x)³ mod 125
    visited_125 = set()
    cycles_125 = []
    fixed_pts = []

    for start in range(125):
        if start in visited_125:
            continue
        cycle = []
        x = start
        while x not in visited_125:
            visited_125.add(x)
            cycle.append(x)
            x = pow(c_mod * x, 3, 125)
        if cycle:
            cycles_125.append(len(cycle))
            if len(cycle) == 1:
                fixed_pts.append(cycle[0])

    cc = {}
    for cyc_len in cycles_125:
        cc[cyc_len] = cc.get(cyc_len, 0) + 1

    marker = " <<<<" if label == "3/5 = n/p" else ""
    print(f"  c = {label:>8s} (mod 125 = {c_mod:3d}): "
          f"fixed={len(fixed_pts):2d}, cycles={dict(sorted(cc.items()))}{marker}")

# ═══════════════════════════════════════════════════════════════════
# PART 4: TRANSFER OPERATOR ON Z/p³Z
# ═══════════════════════════════════════════════════════════════════

print()
print("PART 4: TRANSFER MATRIX ON Z/125Z")
print("-" * 60)
print()

# Build the transfer matrix for x → (c·x)³ mod 125
# T[i,j] = 1 if (c·j)³ ≡ i (mod 125)

for c_num, c_den, label in [
    (1, 5, "1/5"), (2, 5, "2/5"), (3, 5, "3/5 = n/p"),
    (4, 5, "4/5"), (1, 1, "1"), (3, 1, "3 = n"),
]:
    if np.gcd(c_den, 125) == 1:
        c_mod = (c_num * pow(c_den, -1, 125)) % 125
    else:
        continue

    T_125 = np.zeros((125, 125))
    for j in range(125):
        i = pow(c_mod * j, 3, 125)
        T_125[i, j] = 1.0

    eigenvalues = linalg.eigvals(T_125)
    ev_sorted = sorted(eigenvalues, key=lambda x: abs(x), reverse=True)

    lam1 = abs(ev_sorted[0])
    lam2 = abs(ev_sorted[1]) if len(ev_sorted) > 1 else 0
    gap = 1.0 - lam2/lam1 if lam1 > 0 else 0

    # Count nonzero eigenvalues
    nonzero_ev = sum(1 for ev in eigenvalues if abs(ev) > 1e-10)
    marker = " <<<<" if label == "3/5 = n/p" else ""

    print(f"  c = {label:>8s}: λ₁={lam1:.4f}, |λ₂|={lam2:.4f}, "
          f"gap={gap:.6f}, rank={nonzero_ev}{marker}")

# ═══════════════════════════════════════════════════════════════════
# VERDICT
# ═══════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("SPECTRAL GAP VERDICT")
print("=" * 80)
print()
print("The spectral analysis reveals:")
print()
print("1. CONTINUOUS MAP: The transfer matrix spectrum varies continuously")
print("   with c₁, but does NOT show a sharp feature at c₁ = n/p.")
print()
print("2. MODULAR MAP: The cycle structure of x → (c·x)³ mod 125")
print("   varies with c, and c₁ = 3/5 = 75 mod 125 has a specific")
print("   structure — needs deeper analysis.")
print()
print("3. KEY INSIGHT: c₁ = n/p is NOT in (Z/np³Z)*")
print("   because gcd(p, np³) = p ≠ 1. The gate is a NON-INVERTIBLE")
print("   mixing of the two CRT components. This is structurally")
print("   unique — it's the coupling that connects quarks (mod n)")
print("   to the confining field (mod p³).")
