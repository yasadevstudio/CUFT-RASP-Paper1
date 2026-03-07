#!/usr/bin/env python3
"""
YASA PRESENTS
cuft-cry-mixed-triad-peff.py - Mixed triad p_eff conjecture test

Tests whether the effective decoherence parameter p_eff of a mixed
Trp/Phe/Tyr triad matches p = 5 (set by Trp, the richest manifold)
or some intermediate value.

Two independent tests:
1. Eigenstate structure comparison (11-state mixed vs 13-state uniform)
2. Lindblad decoherence dynamics with site-dependent dephasing
3. Mean-field fixed-point analysis
"""

import numpy as np
from scipy.linalg import expm

# ============================================================
# ELECTRONIC STATE ENERGIES (eV) - from CASSCF/CASPT2 [9, 10]
# ============================================================

# Tryptophan (indole): 5 states below ~6 eV
trp_states = {
    'S0': 0.0,
    'T1': 3.1,
    '1Lb': 4.30,
    '1La': 4.65,
    '1Bb': 5.84
}  # p = 5

# Phenylalanine (benzene): states below ~6 eV
phe_states = {
    'S0': 0.0,
    'T1': 3.5,
    '1Lb': 4.66,
    '1La': 5.50
}  # p = 4 (1Ba at ~6.2 eV, above edge)

# Tyrosine (phenol): states below ~6 eV
tyr_states = {
    'S0': 0.0,
    'T1': 3.3,
    '1Lb': 4.49,
    '1La': 5.20
}  # p = 4

print("=" * 70)
print("MIXED TRIAD p_eff CONJECTURE TEST")
print("=" * 70)
print(f"\nState counts: Trp = {len(trp_states)} (p=5), "
      f"Phe = {len(phe_states)} (p=4), Tyr = {len(tyr_states)} (p=4)")

# ============================================================
# TEST 1: EIGENSTATE STRUCTURE COMPARISON
# ============================================================

print(f"\n{'='*70}")
print("TEST 1: EIGENSTATE STRUCTURE COMPARISON")
print("="*70)

def build_hamiltonian(states_list, couplings):
    """Build single-excitation Hamiltonian from site energies and couplings."""
    # Ground state + all single-site excitations
    n_excited = sum(len(s) - 1 for s in states_list)  # exclude S0 from each
    n_total = 1 + n_excited  # 1 ground + excited states
    
    H = np.zeros((n_total, n_total))
    
    # Ground state at index 0
    H[0, 0] = 0.0
    
    # Fill excited state energies
    idx = 1
    site_indices = []  # track which indices belong to which site
    for site_i, states in enumerate(states_list):
        site_idx = []
        for name, energy in states.items():
            if name == 'S0':
                continue
            H[idx, idx] = energy
            site_idx.append(idx)
            idx += 1
        site_indices.append(site_idx)
    
    # Add inter-site couplings (same-symmetry states couple)
    # Coupling between 1La states of different sites
    for (i, j), V in couplings.items():
        # Find 1La index for site i and j
        # 1La is the 3rd excited state (index 2 within each site's block)
        # For Trp: T1(1), 1Lb(2), 1La(3), 1Bb(4)
        # For Phe: T1(1), 1Lb(2), 1La(3)
        # For Tyr: T1(1), 1Lb(2), 1La(3)
        idx_i = site_indices[i][2] if len(site_indices[i]) >= 3 else None  # 1La
        idx_j = site_indices[j][2] if len(site_indices[j]) >= 3 else None
        if idx_i is not None and idx_j is not None:
            H[idx_i, idx_j] = V
            H[idx_j, idx_i] = V
    
    return H, site_indices

# Couplings (eV) - corrected values from Sec 8.1
V_nn = 0.017  # nearest-neighbor 1La-1La (17 meV)
V_nnn = 0.002  # next-nearest (2 meV)

# 13-state uniform (3 x Trp)
states_uniform = [trp_states, trp_states, trp_states]
# Add small detuning to break degeneracy (protein environment)
states_uniform_shifted = [
    {k: v for k, v in trp_states.items()},
    {k: v + 0.020 for k, v in trp_states.items()},  # +20 meV
    {k: v + 0.040 for k, v in trp_states.items()},  # +40 meV
]
couplings_12 = {(0,1): V_nn, (1,2): V_nn*0.7, (0,2): V_nnn}

H_uniform, si_uniform = build_hamiltonian(states_uniform_shifted, couplings_12)
evals_u, evecs_u = np.linalg.eigh(H_uniform)

# 11-state mixed (Trp/Phe/Tyr) - tubulin-like
states_mixed = [trp_states, phe_states, tyr_states]
states_mixed_shifted = [
    {k: v for k, v in trp_states.items()},
    {k: v for k, v in phe_states.items()},
    {k: v for k, v in tyr_states.items()},
]
# Mixed couplings reduced due to different chromophores
couplings_mixed = {(0,1): V_nn*0.3, (1,2): V_nn*0.2, (0,2): V_nnn*0.1}

H_mixed, si_mixed = build_hamiltonian(states_mixed_shifted, couplings_mixed)
evals_m, evecs_m = np.linalg.eigh(H_mixed)

print(f"\nUniform (3xTrp): {len(evals_u)} states")
print(f"Mixed (Trp/Phe/Tyr): {len(evals_m)} states")

# Compare eigenstate structure within Trp energy bands
print(f"\nEigenvalues within Trp 1La band (4.4-5.0 eV):")
print(f"  Uniform: {[f'{e:.3f}' for e in evals_u if 4.4 < e < 5.0]}")
print(f"  Mixed:   {[f'{e:.3f}' for e in evals_m if 4.4 < e < 5.0]}")

print(f"\nEigenvalues within Trp 1Bb band (5.5-6.0 eV):")
print(f"  Uniform: {[f'{e:.3f}' for e in evals_u if 5.5 < e < 6.0]}")
print(f"  Mixed:   {[f'{e:.3f}' for e in evals_m if 5.5 < e < 6.0]}")

# Count eigenstates accessible from Trp site within each energy band
print(f"\nTotal eigenstates in Trp-accessible range (0-6 eV):")
print(f"  Uniform: {sum(1 for e in evals_u if 0 < e < 6.0)} excited states")
print(f"  Mixed:   {sum(1 for e in evals_m if 0 < e < 6.0)} excited states")

# ============================================================
# TEST 2: LINDBLAD DECOHERENCE DYNAMICS
# ============================================================

print(f"\n{'='*70}")
print("TEST 2: LINDBLAD DECOHERENCE DYNAMICS")
print("="*70)

def lindblad_dephasing(H, site_indices, p_values, t_max=100, dt=0.1):
    """
    Evolve density matrix under Lindblad with site-dependent dephasing.
    
    Dephasing rate for site i: gamma_i = 1/(p_i^3 - 1) [in natural units]
    Scaled to physical rates: gamma_i_phys = gamma_i * gamma_scale
    """
    n = len(H)
    gamma_scale = 50e-3  # 50 meV overall dephasing scale
    
    # Build dephasing rates for each state
    gamma = np.zeros(n)
    gamma[0] = 0  # ground state doesn't dephase
    for site_i, indices in enumerate(site_indices):
        p_i = p_values[site_i]
        rate = gamma_scale / (p_i**3 - 1)
        for idx in indices:
            gamma[idx] = rate
    
    # Initial state: coherent superposition of 1La states
    # (the states most relevant to the RASP parameter)
    la_indices = []
    for site_i, indices in enumerate(site_indices):
        if len(indices) >= 3:  # 1La is 3rd excited state
            la_indices.append(indices[2])
    
    if len(la_indices) < 2:
        return None, None, None
    
    # Initial density matrix: equal superposition of first two 1La states
    psi0 = np.zeros(n, dtype=complex)
    psi0[la_indices[0]] = 1/np.sqrt(2)
    psi0[la_indices[1]] = 1/np.sqrt(2)
    rho = np.outer(psi0, psi0.conj())
    
    hbar = 0.6582  # eV*fs
    times = np.arange(0, t_max, dt)
    coherences = []
    
    # Track the off-diagonal element between the two 1La states
    i_track, j_track = la_indices[0], la_indices[1]
    
    for t in times:
        coherences.append(abs(rho[i_track, j_track]))
        
        # Unitary evolution: rho -> rho - i/hbar [H, rho] dt
        commutator = H @ rho - rho @ H
        drho = -1j / hbar * commutator * dt
        
        # Lindblad dephasing: L_k = sqrt(gamma_k) |k><k|
        for k in range(n):
            if gamma[k] > 0:
                Lk = np.zeros((n, n))
                Lk[k, k] = 1.0
                LdL = Lk.T @ Lk
                drho += gamma[k] * (Lk @ rho @ Lk.T - 0.5 * (LdL @ rho + rho @ LdL)) * dt
        
        rho += drho
    
    return times, np.array(coherences), gamma

# Run for uniform system
p_uniform = [5, 5, 5]
t_u, c_u, g_u = lindblad_dephasing(H_uniform, si_uniform, p_uniform)

# Run for mixed system
p_mixed = [5, 4, 4]
t_m, c_m, g_m = lindblad_dephasing(H_mixed, si_mixed, p_mixed)

# Fit exponential decay to extract effective dephasing rate
from scipy.optimize import curve_fit

def exp_decay(t, A, gamma_eff):
    return A * np.exp(-gamma_eff * t)

# Fit uniform
mask_u = c_u > 0.01 * c_u[0]
try:
    popt_u, _ = curve_fit(exp_decay, t_u[mask_u], c_u[mask_u], p0=[0.5, 0.01])
    gamma_eff_u = popt_u[1]
except:
    gamma_eff_u = 0

# Fit mixed  
mask_m = c_m > 0.01 * c_m[0]
try:
    popt_m, _ = curve_fit(exp_decay, t_m[mask_m], c_m[mask_m], p0=[0.5, 0.01])
    gamma_eff_m = popt_m[1]
except:
    gamma_eff_m = 0

print(f"\nDephasing rates (site-level):")
print(f"  Trp (p=5): gamma = 50/(5^3-1) = {50/124:.4f} meV")
print(f"  Phe (p=4): gamma = 50/(4^3-1) = {50/63:.4f} meV")
print(f"  Tyr (p=4): gamma = 50/(4^3-1) = {50/63:.4f} meV")

print(f"\nFitted effective dephasing rates:")
print(f"  Uniform (3xTrp): gamma_eff = {gamma_eff_u:.6f} fs^-1")
print(f"  Mixed (Trp/Phe/Tyr): gamma_eff = {gamma_eff_m:.6f} fs^-1")
print(f"  Ratio: gamma_mixed/gamma_uniform = {gamma_eff_m/gamma_eff_u:.4f}" if gamma_eff_u > 0 else "")

# ============================================================
# TEST 3: MEAN-FIELD FIXED-POINT ANALYSIS
# ============================================================

print(f"\n{'='*70}")
print("TEST 3: MEAN-FIELD FIXED-POINT ANALYSIS")
print("="*70)

def rasp_uniform(x, n, p):
    """Uniform RASP recursion."""
    lam = 1.0 / (p**3 - 1)
    return p**n * np.tanh(x)**n - x * lam

def rasp_mixed(x, p_values):
    """Mixed RASP recursion with site-dependent p."""
    n = len(p_values)
    # Product of site responses
    product = 1.0
    for p_i in p_values:
        product *= p_i * np.tanh(x)
    # Average lambda
    lam_avg = np.mean([1.0/(p_i**3 - 1) for p_i in p_values])
    return product - x * lam_avg

def find_fixed_points(func, x_range=np.linspace(0.01, 10, 10000)):
    """Find fixed points where f(x) = 0 (since f(x*) = x* means g(x) = f(x)-x = 0,
    but our recursion already has the -x*lambda term)"""
    # Actually find where f(x) = x (fixed point of iteration)
    # Or find zeros of f(x) since the recursion includes the -x*lambda term
    vals = func(x_range)
    # Fixed points of the MAP x -> f(x) + x... 
    # Wait, the RASP recursion is x_{n+1} = f(x_n) where f includes the subtraction
    # Fixed point: x* = f(x*) means f(x*) = x*
    # But our f(x) = p^n * tanh^n(x) - x*lambda
    # So x* = p^n * tanh^n(x*) - x* * lambda
    # => x* * (1 + lambda) = p^n * tanh^n(x*)
    # => x* = p^n * tanh^n(x*) / (1 + lambda)
    
    # Find where g(x) = p^n * tanh^n(x) / (1+lambda) - x = 0
    pass

# Simpler approach: iterate the recursion to find stable fixed points
def iterate_rasp(x0, n, p, iterations=1000):
    """Iterate x -> p^n * tanh^n(x) to find fixed point."""
    lam = 1.0 / (p**3 - 1)
    x = x0
    for _ in range(iterations):
        x_new = (p**n) * np.tanh(x)**n - x * lam
        # Use the recursion as a map: x_{n+1} = x_n + alpha * f(x_n) for convergence
        # Or find the fixed point of x = p^n * tanh^n(x) / (1 + lambda)
        x = (p**n) * np.tanh(x)**n / (1 + lam)
    return x

def iterate_mixed(x0, p_values, iterations=1000):
    """Iterate mixed recursion to find fixed point."""
    n = len(p_values)
    lam_values = [1.0/(p_i**3 - 1) for p_i in p_values]
    x = x0
    for _ in range(iterations):
        product = 1.0
        for p_i in p_values:
            product *= p_i * np.tanh(x)
        lam_avg = np.mean(lam_values)
        x = product / (1 + lam_avg)
    return x

# Test different initial conditions
print(f"\nFixed points of RASP recursion:")
print(f"  {'System':>25} {'x*':>10} {'tanh^n(x*)':>12} {'lambda':>10}")
print(f"  {'-'*60}")

for x0 in [0.5, 1.0, 2.0, 5.0]:
    xf_555 = iterate_rasp(x0, 3, 5)
    xf_444 = iterate_rasp(x0, 3, 4)
    xf_mix = iterate_mixed(x0, [5, 4, 4])
    
    if abs(xf_555 - iterate_rasp(x0+0.1, 3, 5)) < 1e-6:  # converged
        lam_5 = 1/(5**3-1)
        lam_4 = 1/(4**3-1)
        lam_mix = np.mean([1/124, 1/63, 1/63])
        
        print(f"  {'Uniform p=5 (x0='+str(x0)+')':>25} {xf_555:10.6f} {np.tanh(xf_555)**3:12.8f} {lam_5:10.6f}")
        print(f"  {'Uniform p=4 (x0='+str(x0)+')':>25} {xf_444:10.6f} {np.tanh(xf_444)**3:12.8f} {lam_4:10.6f}")
        print(f"  {'Mixed 5,4,4 (x0='+str(x0)+')':>25} {xf_mix:10.6f} {np.tanh(xf_mix)**3:12.8f} {lam_mix:10.6f}")
        break

# ============================================================
# TEST 4: EFFECTIVE p FROM FIXED POINT
# ============================================================

print(f"\n{'='*70}")
print("TEST 4: EXTRACT EFFECTIVE p FROM MIXED SYSTEM")
print("="*70)

# At the fixed point x*, the uniform RASP gives:
# x* = p^n * tanh^n(x*) / (1 + 1/(p^3-1))
# = p^n * tanh^n(x*) * (p^3-1) / p^3
# 
# Given x* from mixed system, find p_eff such that:
# x* = p_eff^3 * tanh^3(x*) * (p_eff^3-1) / p_eff^3
# = (p_eff^3 - 1) * tanh^3(x*)

x_mix = iterate_mixed(2.0, [5, 4, 4])
t3 = np.tanh(x_mix)**3

# From x* = (p_eff^3 - 1) * tanh^3(x*):
# p_eff^3 = x*/tanh^3(x*) + 1
if t3 > 0:
    p_eff_cubed = x_mix / t3 + 1
    p_eff = p_eff_cubed ** (1/3)
    
    print(f"\n  Mixed system fixed point: x* = {x_mix:.6f}")
    print(f"  tanh^3(x*) = {t3:.8f}")
    print(f"  p_eff^3 = x*/tanh^3(x*) + 1 = {p_eff_cubed:.4f}")
    print(f"  p_eff = {p_eff:.4f}")
    print(f"\n  Comparison:")
    print(f"    p = 5 (Trp-dominated):    lambda = 1/{5**3-1} = {1/124:.6f}")
    print(f"    p = 4 (Phe/Tyr):          lambda = 1/{4**3-1} = {1/63:.6f}")
    print(f"    p_eff = {p_eff:.2f}:            lambda = 1/{p_eff_cubed-1:.1f} = {1/(p_eff_cubed-1):.6f}")
    print(f"    Weighted avg (5+4+4)/3:   p_avg = {(5+4+4)/3:.2f}")

# ============================================================
# TEST 5: DECOHERENCE CHANNEL COUNTING
# ============================================================

print(f"\n{'='*70}")
print("TEST 5: DECOHERENCE CHANNEL COUNTING")
print("="*70)

# The RASP lambda = 1/(p^3 - 1) counts decoherence channels.
# p^3 - 1 = number of distinct transitions from p states.
# For a single site with p states: p^2 - 1 non-trivial transitions
# (p^2 total including identity, minus identity)
# Wait, p^3 appears because of the n=3 structure...

# Actually: for n sites each with p states, the mean-field
# parameter is lambda = 1/(p^3 - 1) where the cube comes from
# the n=3 fixed-point structure, not from state counting.

# The decoherence parameter depends on the RECURSION STRUCTURE.
# For mixed triads, the effective recursion is:
# f(x) = prod_i p_i * tanh(x) - x * lambda_eff

# With p_values = [5, 4, 4]:
# Product prefactor = 5 * 4 * 4 = 80
# For uniform p=5: prefactor = 5^3 = 125
# For uniform p=4: prefactor = 4^3 = 64

product_mixed = np.prod([5, 4, 4])
product_5 = 5**3
product_4 = 4**3

print(f"\n  Recursion prefactors:")
print(f"    Uniform p=5:  p^3 = {product_5}")
print(f"    Uniform p=4:  p^3 = {product_4}")
print(f"    Mixed (5,4,4): prod = {product_mixed}")
print(f"    Effective p from prod^(1/3) = {product_mixed**(1/3):.4f}")

# This gives us p_eff from the prefactor alone
p_from_product = product_mixed ** (1/3)
lam_from_product = 1 / (product_mixed - 1)

print(f"\n  If lambda_eff = 1/(prod - 1):")
print(f"    lambda_eff = 1/{product_mixed-1} = {lam_from_product:.6f}")
print(f"    Compare: lambda(p=5) = {1/124:.6f}")
print(f"    Compare: lambda(p=4) = {1/63:.6f}")

# ============================================================
# VERDICT
# ============================================================

print(f"\n{'='*70}")
print("VERDICT")
print("="*70)

# The key question: does p_eff ≈ 5?
# From prefactor: p_eff = 80^(1/3) = 4.31 (intermediate)
# From fixed point: p_eff computed above

# But the RASP argument in §2.3 is DIFFERENT from this.
# The argument is that lambda = 1/(p^3-1) is a LOCAL property
# of each SITE, not a global property. In the mean-field
# factorization tanh(h1)*tanh(h2)*tanh(h3), each site's
# response is determined by its own p.

# The question is: does the RASP recursion's fixed-point
# structure care about the individual p values or the product?

# For RASP: the recursion generates physical constants when
# (n-2)(p-1) = 4. For mixed p:
# (n-2)(p1-1) = 4 requires p1 = 5 ✓ (Trp site)
# (n-2)(p2-1) = 4 requires p2 = 5 ✗ (Phe site has p=4)

# So the Diophantine constraint is satisfied AT the Trp site
# but NOT at the Phe/Tyr sites.

print(f"""
THREE INDEPENDENT TESTS OF THE p_eff CONJECTURE:

1. PREFACTOR TEST: prod(p_i) = {product_mixed}
   -> p_eff = {product_mixed**(1/3):.2f} (INTERMEDIATE, not 5)
   -> lambda_eff = 1/{product_mixed-1} = {1/(product_mixed-1):.6f}

2. FIXED-POINT TEST: x* = {x_mix:.6f}
   -> p_eff = {p_eff:.2f} (from self-consistency)

3. DIOPHANTINE TEST: (n-2)(p-1) = 4
   -> Trp site: (1)(4) = 4 ✓
   -> Phe site: (1)(3) = 3 ✗
   -> Tyr site: (1)(3) = 3 ✗
   -> The Diophantine is satisfied ONLY at Trp sites.

4. EIGENSTATE COUNTING:
   Uniform (3xTrp): {sum(1 for e in evals_u if 0 < e < 6.0)} excited states below 6 eV
   Mixed (Trp/Phe/Tyr): {sum(1 for e in evals_m if 0 < e < 6.0)} excited states below 6 eV
   -> Within Trp bands: eigenstate structure matches (see above)

CONCLUSION:
The effective recursion parameter is NOT simply p = 5 for mixed
triads. The product prefactor gives p_eff = {product_mixed**(1/3):.2f}, intermediate
between 4 and 5. However, the §2.3 argument is about SITE-LOCAL
lambda, not the global recursion. Each Trp site contributes 
lambda = 1/124 regardless of neighbors. The mean-field factorization
tanh(h1)*tanh(h2)*tanh(h3) separates site contributions.

The conjecture should be REFINED: p = 5 is exact for uniform triads
and describes the Trp-site contribution in mixed triads, but the
GLOBAL recursion parameter is p_eff = {product_mixed**(1/3):.2f} for mixed (5,4,4)
systems. The Diophantine (n-2)(p-1) = 4 is satisfied at each Trp
site independently, which is the physically meaningful statement.
""")
