#!/usr/bin/env python3
"""
YASA PRESENTS
cuft-cry-exciton-hamiltonian-v2.py - Corrected 13-state Frenkel exciton
Hamiltonian for cryptochrome tryptophan triad

v2 corrections over v1:
  1. mu(1La) = 5.0 D (Callis 1997 experimental consensus)
     NOT 6.0 D (CASPT2/Stark overestimate; Pierce & Boxer 1995)
  2. TDC correction factor applied: point-dipole overestimates
     coupling by 1.5-3x at 5-7 A separations
     (Krueger/Scholes/Fleming 1998, Kenny/Kassal 2016, Czader/Bittner 2008)
  3. Family-dependent analysis: CRY1, CRY4a, plant CRY, insect CRY

Data sources:
  - Callis, Methods Enzymol. 278, 113 (1997): mu(1La) = 4.5-5.5 D
  - Krueger et al., J. Phys. Chem. B 102, 5378 (1998): TDC benchmarks
  - Kenny & Kassal, J. Phys. Chem. B 120, 25 (2016): TDC vs point-dipole
  - Serrano-Andres & Roos, JACS 118, 185 (1996): Indole CASPT2
  - PDB 1U3C (AtCRY1), 6PU0 (ClCRY4)
"""

import numpy as np

print("=" * 70)
print("FRENKEL EXCITON HAMILTONIAN — CRY TRYPTOPHAN TRIAD (CORRECTED)")
print("mu(1La) = 5.0 D + TDC correction (v2)")
print("=" * 70)

# ============================================================
# MONOMER ENERGIES (eV) — All Trp (indole)
# ============================================================
E_Trp = np.array([0.0, 3.10, 4.30, 4.65, 5.84])  # S0, T1, 1Lb, 1La, 1Bb
labels = ['S0', 'T1', '1Lb', '1La', '1Bb']

# Site-dependent protein shifts (from spectroscopic data)
shift_A = np.array([0.0, -0.05, -0.10, -0.15, -0.10])  # W400 near FAD
shift_B = np.array([0.0, -0.08, -0.12, -0.12, -0.08])  # W377
shift_C = np.array([0.0, -0.03, -0.08, -0.10, -0.06])  # W324

E_A = E_Trp + shift_A
E_B = E_Trp + shift_B
E_C = E_Trp + shift_C

# ============================================================
# CORRECTED TRANSITION DIPOLE MOMENTS (Debye)
# ============================================================
# v1 ERROR: mu(1La) = 6.0 D (CASPT2/Stark overestimate)
# v2 FIX:   mu(1La) = 5.0 D (Callis 1997 experimental consensus)
#
# Callis, Methods Enzymol. 278, 113 (1997):
#   "The 1La transition dipole moment in indole is 4.5-5.5 D"
# The 6.0 D value from Pierce & Boxer (1995) is the PERMANENT
# dipole CHANGE (Stark effect), not the transition dipole moment.

mu_Trp_v1 = np.array([0.0, 0.0, 1.0, 6.0, 3.5])  # OLD (wrong)
mu_Trp_v2 = np.array([0.0, 0.0, 1.0, 5.0, 3.5])  # CORRECTED

print(f"\nTransition dipole moments (Debye):")
print(f"  {'State':<6} {'v1 (wrong)':<14} {'v2 (corrected)':<16} {'Source'}")
print(f"  {'-'*60}")
for i in range(5):
    src = ""
    if i == 3:
        src = "Callis 1997 (was Pierce/Boxer Stark)"
    print(f"  {labels[i]:<6} {mu_Trp_v1[i]:<14.1f} {mu_Trp_v2[i]:<16.1f} {src}")

# ============================================================
# TDC CORRECTION FACTOR
# ============================================================
# Point-dipole approximation overestimates coupling at short
# distances (R < 2*chromophore_extent) because the dipole is
# distributed over the aromatic ring (~4.5 A for indole).
#
# Literature benchmarks for aromatic chromophores at 5-7 A:
#   Krueger/Scholes/Fleming (1998): TDC/point-dipole = 0.4-0.7
#   Kenny & Kassal (2016): 0.3-0.6 for face-to-face
#   Czader & Bittner (2008): 0.5 typical for stacked aromatics
#
# Conservative range: point-dipole overestimates by 1.5-3x
# -> correction factor = 0.33-0.67

TDC_CORRECTION_RANGE = (0.33, 0.67)  # V_real / V_point-dipole
TDC_CORRECTION_BEST = 0.50  # geometric mean

print(f"\nTDC correction factor (V_TDC / V_point-dipole):")
print(f"  Range: {TDC_CORRECTION_RANGE[0]:.2f} - {TDC_CORRECTION_RANGE[1]:.2f}")
print(f"  Best estimate: {TDC_CORRECTION_BEST:.2f}")
print(f"  Sources: Krueger 1998, Kenny/Kassal 2016, Czader/Bittner 2008")

# ============================================================
# COUPLING CALCULATION
# ============================================================
D_to_Cm = 3.33564e-30
eps0 = 8.854187817e-12
Ang_to_m = 1e-10
eV_to_J = 1.602176634e-19
eV_per_cm1 = 1.0 / 8065.54
kappa2 = 2.0 / 3.0

def coupling_eV(mu_i_D, mu_j_D, R_Ang, tdc_factor=1.0):
    """Dipole-dipole coupling in eV, with optional TDC correction."""
    mu_i = mu_i_D * D_to_Cm
    mu_j = mu_j_D * D_to_Cm
    R = R_Ang * Ang_to_m
    V_J = kappa2 * mu_i * mu_j / (4 * np.pi * eps0 * R**3)
    return V_J / eV_to_J * tdc_factor

# Inter-chromophore distances (ring centroid to ring centroid)
R_AB = 6.75   # W400-W377 effective center-to-center
R_BC = 7.14   # W377-W324
R_AC = 12.50  # W400-W324

# ============================================================
# COMPARISON: v1 vs v2 COUPLINGS
# ============================================================
print("\n" + "=" * 70)
print("COUPLING COMPARISON: v1 (mu=6D, no TDC) vs v2 (mu=5D + TDC)")
print("=" * 70)

print(f"\n  {'Pair':<10} {'R (A)':<8} {'V_v1 (meV)':<14} {'V_v2_low':<12} {'V_v2_best':<12} {'V_v2_high':<12}")
print(f"  {'-'*68}")

for name, R in [("A-B", R_AB), ("B-C", R_BC), ("A-C", R_AC)]:
    V_v1 = coupling_eV(6.0, 6.0, R) * 1000
    V_v2_low = coupling_eV(5.0, 5.0, R, TDC_CORRECTION_RANGE[0]) * 1000
    V_v2_best = coupling_eV(5.0, 5.0, R, TDC_CORRECTION_BEST) * 1000
    V_v2_high = coupling_eV(5.0, 5.0, R, TDC_CORRECTION_RANGE[1]) * 1000
    print(f"  {name:<10} {R:<8.2f} {V_v1:<14.2f} {V_v2_low:<12.2f} {V_v2_best:<12.2f} {V_v2_high:<12.2f}")

# ============================================================
# BUILD 13x13 HAMILTONIAN — THREE VERSIONS
# ============================================================
def build_hamiltonian(mu_arr, E_sites, R_pairs, tdc=1.0):
    """Build and diagonalize 13-state Frenkel exciton Hamiltonian."""
    N = 13
    H = np.zeros((N, N))

    # Diagonal: site energies
    for i in range(4):
        H[1+i, 1+i] = E_sites[0][1+i]
        H[5+i, 5+i] = E_sites[1][1+i]
        H[9+i, 9+i] = E_sites[2][1+i]

    # Off-diagonal: couplings
    for i in range(4):
        for j in range(4):
            V_AB = coupling_eV(mu_arr[1+i], mu_arr[1+j], R_pairs[0], tdc)
            H[1+i, 5+j] = V_AB; H[5+j, 1+i] = V_AB
            V_AC = coupling_eV(mu_arr[1+i], mu_arr[1+j], R_pairs[1], tdc)
            H[1+i, 9+j] = V_AC; H[9+j, 1+i] = V_AC
            V_BC = coupling_eV(mu_arr[1+i], mu_arr[1+j], R_pairs[2], tdc)
            H[5+i, 9+j] = V_BC; H[9+j, 5+i] = V_BC

    eigenvalues, eigenvectors = np.linalg.eigh(H)
    return H, eigenvalues, eigenvectors

R_pairs = [R_AB, R_AC, R_BC]
E_sites = [E_A, E_B, E_C]

state_labels = ['Ground'] + \
    [f'A-{labels[i+1]}' for i in range(4)] + \
    [f'B-{labels[i+1]}' for i in range(4)] + \
    [f'C-{labels[i+1]}' for i in range(4)]

# v1: old parameters
H_v1, evals_v1, evecs_v1 = build_hamiltonian(mu_Trp_v1, E_sites, R_pairs, 1.0)

# v2: corrected mu, best-estimate TDC
H_v2, evals_v2, evecs_v2 = build_hamiltonian(mu_Trp_v2, E_sites, R_pairs, TDC_CORRECTION_BEST)

# v2 low: corrected mu, strongest TDC correction
H_v2lo, evals_v2lo, evecs_v2lo = build_hamiltonian(mu_Trp_v2, E_sites, R_pairs, TDC_CORRECTION_RANGE[0])

# v2 high: corrected mu, weakest TDC correction
H_v2hi, evals_v2hi, evecs_v2hi = build_hamiltonian(mu_Trp_v2, E_sites, R_pairs, TDC_CORRECTION_RANGE[1])

# ============================================================
# V/dE ANALYSIS — CORRECTED
# ============================================================
print("\n" + "=" * 70)
print("V/dE ANALYSIS — CORRECTED (mu=5.0D + TDC)")
print("=" * 70)

def compute_vde(mu_arr, tdc=1.0):
    """Compute V/dE for all near-degenerate pairs."""
    results = []
    for state_idx in range(4):
        for pair, R, i_site, j_site in [
            ("A-B", R_AB, 0, 1), ("A-C", R_AC, 0, 2), ("B-C", R_BC, 1, 2)
        ]:
            Es = [E_A, E_B, E_C]
            E_i = Es[i_site][1 + state_idx]
            E_j = Es[j_site][1 + state_idx]
            V = coupling_eV(mu_arr[1 + state_idx], mu_arr[1 + state_idx], R, tdc)
            dE = abs(E_i - E_j)
            VdE = abs(V) / dE if dE > 1e-6 else float('inf')
            results.append((pair, labels[1 + state_idx], V * 1000, dE * 1000, VdE))
    return results

vde_v1 = compute_vde(mu_Trp_v1, 1.0)
vde_v2_best = compute_vde(mu_Trp_v2, TDC_CORRECTION_BEST)
vde_v2_lo = compute_vde(mu_Trp_v2, TDC_CORRECTION_RANGE[0])
vde_v2_hi = compute_vde(mu_Trp_v2, TDC_CORRECTION_RANGE[1])

print(f"\n  {'Pair':<6} {'State':<6} {'V/dE (v1)':<12} {'V/dE (v2 lo)':<14} {'V/dE (v2 best)':<16} {'V/dE (v2 hi)':<14} {'Regime (v2)'}")
print(f"  {'-'*90}")

max_vde_v1 = 0
max_vde_v2_best = 0
max_vde_v2_range = [float('inf'), 0]

for idx in range(len(vde_v1)):
    pair, state, V1, dE1, vde1 = vde_v1[idx]
    _, _, V2lo, _, vde2lo = vde_v2_lo[idx]
    _, _, V2best, _, vde2best = vde_v2_best[idx]
    _, _, V2hi, _, vde2hi = vde_v2_hi[idx]

    if abs(V1) < 1e-6:
        continue  # skip spin-forbidden

    if dE1 > 1e-3:
        max_vde_v1 = max(max_vde_v1, vde1)
        max_vde_v2_best = max(max_vde_v2_best, vde2best)
        max_vde_v2_range[0] = min(max_vde_v2_range[0], vde2lo) if vde2lo < max_vde_v2_range[0] else max_vde_v2_range[0]
        max_vde_v2_range[1] = max(max_vde_v2_range[1], vde2hi)

    if vde2best > 1.0:
        regime = "DELOCALIZED"
    elif vde2best > 0.3:
        regime = "TRANSITION"
    elif vde2best > 0.1:
        regime = "MIXED"
    else:
        regime = "factorized"

    print(f"  {pair:<6} {state:<6} {vde1:<12.4f} {vde2lo:<14.4f} {vde2best:<16.4f} {vde2hi:<14.4f} {regime}")

# ============================================================
# 1La BLOCK FOCUS — THE CRITICAL SUBSPACE
# ============================================================
print("\n" + "=" * 70)
print("1La BLOCK: 3x3 SUBSPACE (corrected)")
print("(This is the only subspace with significant delocalization)")
print("=" * 70)

# Extract 1La-1La couplings and build 3x3 sub-Hamiltonian
E_La = [E_A[3], E_B[3], E_C[3]]  # 1La site energies

for label, tdc, mu_arr in [
    ("v1 (mu=6D, no TDC)", 1.0, mu_Trp_v1),
    ("v2 low (mu=5D, TDC=0.33)", TDC_CORRECTION_RANGE[0], mu_Trp_v2),
    ("v2 best (mu=5D, TDC=0.50)", TDC_CORRECTION_BEST, mu_Trp_v2),
    ("v2 high (mu=5D, TDC=0.67)", TDC_CORRECTION_RANGE[1], mu_Trp_v2),
]:
    H3 = np.diag(E_La)
    V_AB = coupling_eV(mu_arr[3], mu_arr[3], R_AB, tdc)
    V_AC = coupling_eV(mu_arr[3], mu_arr[3], R_AC, tdc)
    V_BC = coupling_eV(mu_arr[3], mu_arr[3], R_BC, tdc)
    H3[0,1] = V_AB; H3[1,0] = V_AB
    H3[0,2] = V_AC; H3[2,0] = V_AC
    H3[1,2] = V_BC; H3[2,1] = V_BC

    evals3, evecs3 = np.linalg.eigh(H3)

    print(f"\n  --- {label} ---")
    print(f"  Site energies: {E_La[0]:.3f}, {E_La[1]:.3f}, {E_La[2]:.3f} eV")
    print(f"  Couplings: V_AB={V_AB*1000:.2f}, V_BC={V_BC*1000:.2f}, V_AC={V_AC*1000:.2f} meV")
    print(f"  V/dE(AB)={abs(V_AB)/(abs(E_La[0]-E_La[1]) if abs(E_La[0]-E_La[1])>1e-6 else 1e-6):.3f}, "
          f"V/dE(BC)={abs(V_BC)/(abs(E_La[1]-E_La[2]) if abs(E_La[1]-E_La[2])>1e-6 else 1e-6):.3f}")

    print(f"  Eigenstates:")
    for k in range(3):
        vec = evecs3[:, k]
        S_ent = 0
        for p in vec**2:
            if p > 1e-15:
                S_ent -= p * np.log(p)
        dom = ['A', 'B', 'C'][np.argmax(np.abs(vec))]
        print(f"    E_{k+1} = {evals3[k]:.6f} eV | "
              f"({vec[0]:+.4f}, {vec[1]:+.4f}, {vec[2]:+.4f}) | "
              f"S_ent = {S_ent:.3f} | dom = {dom}")

# ============================================================
# FAMILY-DEPENDENT V/dE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("FAMILY-DEPENDENT V/dE (CRY families have different Trp geometry)")
print("=" * 70)

# Different CRY families have different inter-Trp distances
# Distances from PDB crystal structures
families = {
    "CRY1 (AtCRY1, 1U3C)": {
        "R_12": 6.75, "R_23": 7.14, "R_13": 12.50,
        "dE_12": 30, "dE_23": 20,  # meV (protein shift differences)
    },
    "CRY4a (ClCRY4, 6PU0)": {
        "R_12": 6.50, "R_23": 7.00, "R_13": 12.00,
        "dE_12": 25, "dE_23": 25,
    },
    "Plant CRY2 (est.)": {
        "R_12": 7.00, "R_23": 7.50, "R_13": 13.00,
        "dE_12": 35, "dE_23": 30,
    },
    "Insect CRY (DmCRY, est.)": {
        "R_12": 6.80, "R_23": 7.20, "R_13": 12.80,
        "dE_12": 40, "dE_23": 20,
    },
}

mu_La = 5.0  # Corrected
tdc = TDC_CORRECTION_BEST

print(f"\n  mu(1La) = {mu_La} D, TDC correction = {tdc}")
print(f"\n  {'Family':<30} {'V_12 (meV)':<12} {'V_23 (meV)':<12} {'V/dE_12':<10} {'V/dE_23':<10} {'Max V/dE':<10} {'Regime'}")
print(f"  {'-'*96}")

for name, params in families.items():
    V_12 = coupling_eV(mu_La, mu_La, params["R_12"], tdc) * 1000
    V_23 = coupling_eV(mu_La, mu_La, params["R_23"], tdc) * 1000
    vde_12 = abs(V_12) / params["dE_12"]
    vde_23 = abs(V_23) / params["dE_23"]
    max_vde = max(vde_12, vde_23)

    if max_vde > 1.0:
        regime = "DELOCALIZED"
    elif max_vde > 0.3:
        regime = "TRANSITION"
    elif max_vde > 0.1:
        regime = "MIXED"
    else:
        regime = "factorized"

    print(f"  {name:<30} {V_12:<12.2f} {V_23:<12.2f} {vde_12:<10.3f} {vde_23:<10.3f} {max_vde:<10.3f} {regime}")

# ============================================================
# ENTANGLEMENT ENTROPY — CORRECTED
# ============================================================
print("\n" + "=" * 70)
print("ENTANGLEMENT ENTROPY: v1 vs v2 (1La eigenstates only)")
print("=" * 70)

# Extract 1La eigenstate entropies from full Hamiltonian
def get_la_entropies(evecs, evals, H_diag):
    """Extract 1La-dominated eigenstates and their entropies."""
    results = []
    for k in range(13):
        vec = evecs[:, k]
        # Check if this eigenstate has significant 1La character
        la_weight = vec[3]**2 + vec[7]**2 + vec[11]**2  # A-1La + B-1La + C-1La
        if la_weight > 0.5:
            w_A = vec[3]**2
            w_B = vec[7]**2
            w_C = vec[11]**2
            tot = w_A + w_B + w_C
            pn = np.array([w_A, w_B, w_C]) / tot
            S = -sum(p * np.log(p) if p > 1e-15 else 0 for p in pn)
            results.append((evals[k], w_A, w_B, w_C, S, la_weight))
    return results

la_v1 = get_la_entropies(evecs_v1, evals_v1, H_v1)
la_v2 = get_la_entropies(evecs_v2, evals_v2, H_v2)

print(f"\n  v1 (mu=6D, no TDC):")
print(f"  {'E (eV)':<10} {'w_A':<8} {'w_B':<8} {'w_C':<8} {'S_ent':<8} {'1La wt':<8}")
for E, wA, wB, wC, S, wt in la_v1:
    print(f"  {E:<10.4f} {wA:<8.4f} {wB:<8.4f} {wC:<8.4f} {S:<8.3f} {wt:<8.4f}")

print(f"\n  v2 best (mu=5D, TDC=0.50):")
print(f"  {'E (eV)':<10} {'w_A':<8} {'w_B':<8} {'w_C':<8} {'S_ent':<8} {'1La wt':<8}")
for E, wA, wB, wC, S, wt in la_v2:
    print(f"  {E:<10.4f} {wA:<8.4f} {wB:<8.4f} {wC:<8.4f} {S:<8.3f} {wt:<8.4f}")

# ============================================================
# OSCILLATOR STRENGTH REDISTRIBUTION
# ============================================================
print("\n" + "=" * 70)
print("OSCILLATOR STRENGTH REDISTRIBUTION (1La manifold)")
print("=" * 70)

print(f"\n  Point-dipole (v1): Each monomer contributes f ~ mu^2 * E")
print(f"  Three independent Trp: f_total = 3 * f_mono")
print(f"  Collective state: oscillator strength CONCENTRATED in bright state")

for label, evecs, evals, mu_la in [
    ("v1 (mu=6D)", evecs_v1, evals_v1, 6.0),
    ("v2 (mu=5D, TDC=0.50)", evecs_v2, evals_v2, 5.0),
]:
    print(f"\n  --- {label} ---")
    f_mono = mu_la**2  # proportional to
    for k in range(13):
        vec = evecs[:, k]
        la_weight = vec[3]**2 + vec[7]**2 + vec[11]**2
        if la_weight > 0.5:
            # Oscillator strength ~ |sum of transition dipoles|^2
            # For aligned dipoles: f_k ~ (vec[3] + vec[7] + vec[11])^2 * mu^2
            f_k = (vec[3] + vec[7] + vec[11])**2 * mu_la**2
            f_ratio = f_k / (3 * f_mono)
            print(f"    E = {evals[k]:.4f} eV | f/f_mono = {f_k/f_mono:.3f} | f/(3*f_mono) = {f_ratio:.3f}")

# ============================================================
# PARAMETER SENSITIVITY
# ============================================================
print("\n" + "=" * 70)
print("PARAMETER SENSITIVITY: V/dE(max) vs mu and TDC")
print("=" * 70)

print(f"\n  {'mu (D)':<8} {'TDC':<8} {'V_AB (meV)':<14} {'V/dE(AB)':<12} {'V/dE(BC)':<12} {'Max V/dE'}")
print(f"  {'-'*64}")

for mu in [4.5, 5.0, 5.5, 6.0]:
    for tdc_f in [0.33, 0.50, 0.67, 1.0]:
        V_AB_meV = coupling_eV(mu, mu, R_AB, tdc_f) * 1000
        V_BC_meV = coupling_eV(mu, mu, R_BC, tdc_f) * 1000
        vde_AB = V_AB_meV / 30.0  # dE_AB = 30 meV
        vde_BC = V_BC_meV / 20.0  # dE_BC = 20 meV
        mx = max(vde_AB, vde_BC)
        marker = " <-- v2 best" if (mu == 5.0 and tdc_f == 0.50) else (
                 " <-- v1" if (mu == 6.0 and tdc_f == 1.0) else "")
        print(f"  {mu:<8.1f} {tdc_f:<8.2f} {V_AB_meV:<14.2f} {vde_AB:<12.3f} {vde_BC:<12.3f} {mx:<8.3f}{marker}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("CORRECTION SUMMARY")
print("=" * 70)

# Get v2 best 1La V/dE values
V_AB_v2 = coupling_eV(5.0, 5.0, R_AB, TDC_CORRECTION_BEST) * 1000
V_BC_v2 = coupling_eV(5.0, 5.0, R_BC, TDC_CORRECTION_BEST) * 1000
vde_AB_v2 = V_AB_v2 / 30.0
vde_BC_v2 = V_BC_v2 / 20.0

V_AB_v1 = coupling_eV(6.0, 6.0, R_AB, 1.0) * 1000
V_BC_v1 = coupling_eV(6.0, 6.0, R_BC, 1.0) * 1000
vde_AB_v1 = V_AB_v1 / 30.0
vde_BC_v1 = V_BC_v1 / 20.0

print(f"""
  | Quantity              | v1 (old)       | v2 (corrected)       |
  |-----------------------|----------------|----------------------|
  | mu(1La)               | 6.0 D          | 5.0 D (Callis 1997)  |
  | TDC correction        | none (1.0)     | 0.50 (0.33-0.67)     |
  | V_AB(1La) (meV)       | {V_AB_v1:.1f}          | {V_AB_v2:.1f} ({coupling_eV(5.0,5.0,R_AB,0.33)*1000:.1f}-{coupling_eV(5.0,5.0,R_AB,0.67)*1000:.1f})       |
  | V_BC(1La) (meV)       | {V_BC_v1:.1f}          | {V_BC_v2:.1f} ({coupling_eV(5.0,5.0,R_BC,0.33)*1000:.1f}-{coupling_eV(5.0,5.0,R_BC,0.67)*1000:.1f})       |
  | V/dE(AB)              | {vde_AB_v1:.3f}          | {vde_AB_v2:.3f} ({coupling_eV(5.0,5.0,R_AB,0.33)*1000/30:.3f}-{coupling_eV(5.0,5.0,R_AB,0.67)*1000/30:.3f})    |
  | V/dE(BC)              | {vde_BC_v1:.3f}          | {vde_BC_v2:.3f} ({coupling_eV(5.0,5.0,R_BC,0.33)*1000/20:.3f}-{coupling_eV(5.0,5.0,R_BC,0.67)*1000/20:.3f})    |
  | Regime                | DELOCALIZED    | TRANSITION (tunable) |

  KEY RESULT: V/dE drops from 1.5-2.1 to 0.3-1.0 after corrections.
  The system is in the TRANSITION regime — not firmly collective,
  but tunable across CRY families by protein environment.
  This is ACTUALLY MORE INTERESTING than firm delocalization:
  it means the coupling regime is a selectable property.

  All 4 CRY families fall in V/dE = 0.3-1.0 (transition regime).
  Family-dependent geometry tunes the exact position within this range.

  Verification: cuft-cry-exciton-hamiltonian-v2.py
""")
print("=" * 70)
print("END — YASA PRESENTS")
print("=" * 70)
