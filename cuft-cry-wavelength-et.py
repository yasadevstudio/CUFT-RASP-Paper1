#!/usr/bin/env python3
"""
YASA PRESENTS
cuft-cry-wavelength-et.py - Wavelength-dependent ET rate prediction

Computes the predicted excitation-wavelength dependence of FAD
photoreduction in the CRY Trp triad. Tests whether 1La excitonic
mixing produces measurable rate differences at 260 nm vs 280 nm.

Physics:
  - 260 nm excitation populates 1La states (excitonically mixed)
  - 280 nm excitation populates 1Lb states (no excitonic mixing)
  - ET from Trp to FAD depends on excitation amplitude at TrpA
  - Collective 1La states redistribute amplitude across triad
"""

import numpy as np

# ============================================================
# PARAMETERS (from corrected Hamiltonian, Sec 8.1)
# ============================================================

# 1La energies (eV) with protein-induced site shifts
E_1La = np.array([4.45, 4.47, 4.50])  # TrpA, TrpB, TrpC (20-50 meV detuning)

# Corrected 1La-1La couplings (meV) - mu=5.0D, TDC=0.50
V_AB = 17.0e-3  # eV (best estimate from Sec 8.1)
V_BC = 12.0e-3  # eV (longer distance B-C pair)
V_AC = 2.0e-3   # eV (next-nearest, much weaker)

# 1Lb properties
E_1Lb = np.array([4.30, 4.31, 4.33])  # eV
mu_1Lb = 2.5  # Debye (well-established, weak transition)
# 1Lb coupling negligible: V/dE << 0.01 (factorized)

# 1La transition dipole
mu_1La = 5.0  # Debye

# FAD-TrpA ET coupling (from CDFT-CI, Luo et al. 2023)
V_DA_FAD = 6.35e-3  # eV

# Marcus parameters for FAD* -> TrpA
lambda_reorg = 0.400  # eV
DG = -0.170  # eV
kBT = 0.026  # eV at 300K

# ============================================================
# 1. DIAGONALIZE 1La HAMILTONIAN
# ============================================================

H_1La = np.array([
    [E_1La[0], V_AB,     V_AC],
    [V_AB,     E_1La[1], V_BC],
    [V_AC,     V_BC,     E_1La[2]]
])

eigenvalues, eigenvectors = np.linalg.eigh(H_1La)

print("=" * 65)
print("1La EXCITON HAMILTONIAN EIGENSTATES")
print("=" * 65)
print(f"\n{'State':>6} {'Energy (eV)':>12} {'|cA|^2':>8} {'|cB|^2':>8} {'|cC|^2':>8} {'f/f_mono':>8}")
print("-" * 60)

# Transition dipole of each eigenstate (assume all mu aligned for max effect)
# More realistic: orientational average
f_ratios = []
for i in range(3):
    c = eigenvectors[:, i]
    # Oscillator strength ratio: f_eig/f_mono = |sum c_i|^2 for aligned dipoles
    # With orientational average, use f ~ sum |c_i|^2 * mu_i^2 but all same mu
    # For superradiance: f_bright/f_mono = |c_A + c_B + c_C|^2
    f_ratio = abs(np.sum(c))**2
    f_ratios.append(f_ratio)
    print(f"  |{i+1}>  {eigenvalues[i]:12.6f}  {c[0]**2:8.4f}  {c[1]**2:8.4f}  {c[2]**2:8.4f}  {f_ratio:8.4f}")

# Identify bright state (highest f_ratio)
bright_idx = np.argmax(f_ratios)
c_bright = eigenvectors[:, bright_idx]

print(f"\nBright state: |{bright_idx+1}> with f/f_mono = {f_ratios[bright_idx]:.4f}")
print(f"  TrpA amplitude: |c_A| = {abs(c_bright[0]):.4f}")
print(f"  TrpA weight:    |c_A|^2 = {c_bright[0]**2:.4f}")

# ============================================================
# 2. ET RATE: BRIGHT 1La vs SINGLE-SITE 1La vs 1Lb
# ============================================================

print("\n" + "=" * 65)
print("ELECTRON TRANSFER COUPLING TO FAD")
print("=" * 65)

# For ET from Trp to FAD, only the TrpA component matters
# (TrpA is the proximal donor, ~7.4 A from FAD)
# Effective coupling = c_A * V_DA for eigenstate excitation

# Case 1: Direct excitation of TrpA only (no mixing)
V_eff_single = V_DA_FAD
print(f"\n1. Single-site TrpA excitation:")
print(f"   V_eff = V_DA = {V_eff_single*1000:.2f} meV")

# Case 2: Bright 1La eigenstate
V_eff_bright = abs(c_bright[0]) * V_DA_FAD
print(f"\n2. Bright 1La eigenstate (260 nm):")
print(f"   V_eff = |c_A| * V_DA = {abs(c_bright[0]):.4f} * {V_DA_FAD*1000:.2f} = {V_eff_bright*1000:.2f} meV")

# Case 3: 1Lb excitation (no mixing, stays on excited site)
V_eff_1Lb = V_DA_FAD  # Same coupling, but different spectral overlap
print(f"\n3. 1Lb excitation (280 nm):")
print(f"   V_eff = V_DA = {V_eff_1Lb*1000:.2f} meV (no excitonic mixing)")

# ============================================================
# 3. MARCUS RATE CALCULATION
# ============================================================

print("\n" + "=" * 65)
print("MARCUS ET RATES")
print("=" * 65)

def marcus_rate(V, lam, dG, kBT):
    """Nonadiabatic Marcus rate in s^-1"""
    hbar = 6.582e-16  # eV*s
    prefactor = (2 * np.pi / hbar) * V**2
    fc = np.exp(-(lam + dG)**2 / (4 * lam * kBT))
    fc /= np.sqrt(4 * np.pi * lam * kBT)
    return prefactor * fc

# Rate for single-site excitation
k_single = marcus_rate(V_DA_FAD, lambda_reorg, DG, kBT)
tau_single = 1.0 / k_single

# Rate for bright 1La eigenstate
# Key: the Marcus DG changes because the eigenstate energy differs from monomer
dE_bright = eigenvalues[bright_idx] - E_1La[0]  # Energy shift of bright state
DG_bright = DG - dE_bright  # Modified driving force (eigenstate is higher energy)
k_bright = marcus_rate(V_eff_bright, lambda_reorg, DG_bright, kBT)
tau_bright = 1.0 / k_bright

# Rate for 1Lb excitation (different DG due to lower excitation energy)
DG_1Lb = DG + (E_1La[0] - E_1Lb[0])  # 1Lb is ~0.15 eV lower than 1La
k_1Lb = marcus_rate(V_DA_FAD, lambda_reorg, DG_1Lb, kBT)
tau_1Lb = 1.0 / k_1Lb

print(f"\nSingle-site TrpA (reference):")
print(f"  k = {k_single:.3e} s^-1, tau = {tau_single*1e12:.2f} ps")

print(f"\nBright 1La eigenstate (260 nm excitation):")
print(f"  V_eff = {V_eff_bright*1000:.2f} meV")
print(f"  DG_eff = {DG_bright*1000:.1f} meV (shifted by {dE_bright*1000:.1f} meV)")
print(f"  k = {k_bright:.3e} s^-1, tau = {tau_bright*1e12:.2f} ps")

print(f"\n1Lb excitation (280 nm excitation):")
print(f"  V_eff = {V_DA_FAD*1000:.2f} meV")
print(f"  DG_eff = {DG_1Lb*1000:.1f} meV")
print(f"  k = {k_1Lb:.3e} s^-1, tau = {tau_1Lb*1e12:.2f} ps")

print(f"\n{'='*65}")
print(f"WAVELENGTH DEPENDENCE RATIO")
print(f"{'='*65}")
ratio = k_bright / k_1Lb
print(f"\n  k(260 nm) / k(280 nm) = {ratio:.3f}")
print(f"\n  At 260 nm: ET {'faster' if ratio > 1 else 'slower'} by factor {ratio:.2f}x")

# ============================================================
# 4. SENSITIVITY ANALYSIS
# ============================================================

print(f"\n{'='*65}")
print(f"SENSITIVITY TO DETUNING")
print(f"{'='*65}")

print(f"\n{'delta (meV)':>12} {'|c_A|^2':>8} {'V_eff (meV)':>12} {'k_ratio':>10}")
print("-" * 46)

for delta in [0, 10, 20, 30, 50, 100]:
    E_test = np.array([4.45, 4.45 + delta*1e-3, 4.45 + 2*delta*1e-3])
    H_test = np.array([
        [E_test[0], V_AB,     V_AC],
        [V_AB,      E_test[1], V_BC],
        [V_AC,      V_BC,     E_test[2]]
    ])
    evals, evecs = np.linalg.eigh(H_test)
    f_test = [abs(np.sum(evecs[:, i]))**2 for i in range(3)]
    bi = np.argmax(f_test)
    cA = abs(evecs[bi, 0])
    V_eff = cA * V_DA_FAD
    dE = evals[bi] - E_test[0]
    DG_test = DG - dE
    k_test = marcus_rate(V_eff, lambda_reorg, DG_test, kBT)
    DG_lb = DG + (E_test[0] - E_1Lb[0])
    k_lb = marcus_rate(V_DA_FAD, lambda_reorg, DG_lb, kBT)
    print(f"  {delta:>8}     {cA**2:8.4f}  {V_eff*1000:12.2f}  {k_test/k_lb:10.3f}")

# ============================================================
# 5. FORSTER ENERGY TRANSFER (supplementary)
# ============================================================

print(f"\n{'='*65}")
print(f"FORSTER ENERGY TRANSFER: OSCILLATOR STRENGTH EFFECT")
print(f"{'='*65}")

# The bright 1La state concentrates oscillator strength
# Forster rate ~ f_donor * f_acceptor / R^6
# For emission from bright state: f_bright/f_mono gives enhancement
print(f"\n  f(bright 1La) / f(single Trp 1La) = {f_ratios[bright_idx]:.3f}")
print(f"  f(1Lb single) / f(single Trp 1La) = {(mu_1Lb/mu_1La)**2:.3f}")
print(f"\n  If energy transfer to FAD is Forster-type:")
print(f"    k_FRET(bright 1La) / k_FRET(1Lb) = {f_ratios[bright_idx] / (mu_1Lb/mu_1La)**2:.2f}x")
print(f"\n  Note: ET in CRY is Dexter (through-bond), not Forster.")
print(f"  The Forster ratio above is an UPPER BOUND on the")
print(f"  wavelength dependence via energy transfer pathway.")

print(f"\n{'='*65}")
print(f"CONCLUSION")
print(f"{'='*65}")
print(f"""
Two competing effects determine wavelength dependence:

1. EXCITONIC DILUTION: The bright 1La state distributes excitation
   across all 3 Trps, REDUCING the amplitude on TrpA (the FAD-
   proximal donor). This SLOWS Dexter ET by |c_A|^2 = {c_bright[0]**2:.3f}.

2. DRIVING FORCE SHIFT: The bright state is shifted +{dE_bright*1000:.1f} meV
   above the monomer 1La, modifying the Marcus driving force.

3. OSCILLATOR STRENGTH: The bright state concentrates f by
   {f_ratios[bright_idx]:.2f}x, enhancing any Forster-type pathway.

Net effect for Marcus ET: k(260)/k(280) = {ratio:.3f}
  -> {'The 1La excitonic mixing produces a measurable ' + str(round(abs(1-ratio)*100)) + '% wavelength dependence.' if abs(1-ratio) > 0.05 else 'The wavelength dependence is small (<5%), making prediction (f) difficult to test experimentally.'}
""")
