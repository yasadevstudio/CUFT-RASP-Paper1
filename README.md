# Four Fundamental Constants of Nature from a Gated Cubic Recursion with Zero Free Parameters

By Eliseu Spiller de Barros Lima

## Overview

A single integer input — the quark count n = 3 — determines four fundamental constants at sub-ppb precision through a six-step derivation chain with zero free parameters. Three additional mass ratios extend the framework to seven constants at ppm precision, all sharing {2, 3, 5, 31} denominator closure.

## Repository Contents

- `Paper1-CUFT-RASP/main.tex` — arXiv LaTeX source
- `Paper1-CUFT-RASP/main.pdf` — Compiled PDF
- `Paper1-CUFT-RASP/PAPER1-AUDIT-CHECKLIST.md` — Verification checklist

## Requirements

Python 3.8+ with:
```
numpy
scipy
sympy
mpmath
```

## Verification Scripts

### Core Derivation Chain

| Script | Verifies |
|--------|----------|
| `cuft-proof.py` | Gain-coherence equation, all 4 constants, ppb precision |
| `cuft-denominator-quantization.py` | Denominator Quantization Theorem (integer p required) |
| `cuft-dissipative-selection.py` | Only (3,5) survives among Diophantine solutions |
| `cuft-final.py` | Complete RASP recursion, mass formula output |
| `cuft-alpha-derivation.py` | Fine-structure constant derivation |
| `cuft-neutron-mass.py` | Neutron mass ratio |
| `cuft-c1-extended-precision.py` | Extended precision verification of c₁ = 3/5 |
| `cuft-verify-hits.py` | All predicted mass ratios vs CODATA 2022 |
| `cuft-fine-structure.py` | Fine-structure constant verification |
| `gamma-first-principles-derivation.py` | First-principles derivation of Γ = p^(n-1) from partition function |

### Bohr Step Verification Suite

| Script | Verifies |
|--------|----------|
| `cuft-bohr-1.py` through `cuft-bohr-24.py` | 24-part Bohr quantization verification suite |

### Lambda Perturbation Theory

| Script | Verifies |
|--------|----------|
| `cuft-lambda-perturbation-derivation.py` | Lambda hierarchy derivation, all 4 constants as λ-series |
| `cuft-lambda-correction.py` | Lambda correction terms |
| `cuft-subppb-corrections.py` | Sub-ppb correction search (exhaustive scan) |
| `cuft-tighten-q2-q7.py` | Higher-order correction tightening |
| `cuft-close-q6-q7.py` | Residual closure analysis |
| `cuft-close-abc.py` | ABC correction analysis |
| `cuft-floquet-spectrum.py` | Floquet observable spectrum (diagonal operator) |
| `cuft-floquet-analysis.py` | Floquet/time-crystal analysis |
| `cuft-floquet-perturbation-derivation.py` | Floquet perturbation derivation |
| `cuft-tau-unification.py` | Tau lepton formula and perturbative structure |

### Structural Uniqueness

| Script | Verifies |
|--------|----------|
| `cuft-attack-bootstrap.py` | Bootstrap Theorem (c₁ uniqueness) |
| `cuft-attack-denominator-closure.py` | Denominator closure attack |
| `cuft-attack-dissipative-v2.py` | Dissipative selection proof |
| `cuft-attack-hopf-vortex.py` | T(3,5) Hopf vortex geometry |
| `cuft-attack-number-theory.py` | Number-theoretic selection (Mersenne-triangular) |
| `cuft-attack-rep-theory.py` | Representation theory (Clebsch-Gordan) |
| `cuft-attack-info-theory.py` | Information-theoretic selection (DPI + Jaynes) |
| `cuft-attack-stat-mech.py` | Statistical mechanics (max entropy production) |
| `cuft-attack-variational.py` | Variational selection (Percival action) |
| `cuft-attack-cubic-reciprocity.py` | Cubic reciprocity analysis |
| `cuft-attack-extremal.py` | Extremal analysis |
| `cuft-attack-lyapunov.py` | Lyapunov stability analysis |
| `cuft-attack-p-adic.py` | p-adic analysis |
| `cuft-attack-rg-fixed-point.py` | Renormalization group fixed point |
| `cuft-attack-spectral-gap.py` | Spectral gap analysis |
| `cuft-beltrami-t35-construction.py` | Rigorous T(3,5) Beltrami field on S³ |

### Extensions and Analysis

| Script | Verifies |
|--------|----------|
| `cuft-2d-coupled-lattice.py` | 2D coupled map lattice (pion, muon from inter-solution coupling) |
| `cuft-coupled-quarks.py` | Coupled quark analysis |
| `cuft-photonic-tc-design.py` | Photonic time crystal experimental design |
| `cuft-n3-meanfield-exact.py` | Exact N=3 Ising vs mean-field comparison |
| `cuft-base60-analysis.py` | Base-60 analysis of collective action X=60 |
| `cuft-koide-hunt.py` | Koide formula connection analysis |
| `lambda-order-uniqueness-scan.py` | Lambda-order uniqueness scan |

### Derivation Attempts and Exploration

| Script | Verifies |
|--------|----------|
| `cuft-R-derive.py` | R-derivation path |
| `cuft-angle1-factorization-theorem.py` | Factorization theorem |
| `cuft-angle2-derive-mass-formula.py` | Mass formula derivation |
| `cuft-angle3-complex-residue.py` | Complex residue analysis |
| `cuft-coupling-bridge.py` | Coupling bridge derivation |
| `cuft-coupling-derivation.py` | Coupling constant derivation |
| `cuft-coupling-proof.py` | Coupling proof |
| `cuft-crosspoint-virial.py` | Crosspoint virial analysis |
| `cuft-derivation-attempt.py` | Derivation attempt |
| `cuft-derivation-v2.py` | Derivation v2 |
| `cuft-derive-form-7routes.py` | 7-route mass formula derivation |
| `cuft-derive-form-final-attack.py` | Final derivation attack |
| `cuft-derive-form-post-tc.py` | Post-time-crystal derivation |
| `cuft-dynamical-c1-proof.py` | Dynamical c₁ proof |
| `cuft-dynamical-proof-hunt.py` | Dynamical proof search |
| `cuft-exact-identity-hunt.py` | Exact identity search |
| `cuft-final-structural.py` | Final structural analysis |
| `cuft-finish.py` | Completion verification |
| `cuft-fixed-point-landscape.py` | Fixed point landscape |
| `cuft-formula-derivation.py` | Formula derivation |
| `cuft-forward-derivation.py` | Forward derivation path |
| `cuft-inter-ratios.py` | Inter-solution ratios |
| `cuft-level1-hunt.py` | Level 1 constant search |
| `cuft-level1-verify.py` | Level 1 verification |
| `cuft-mass-ratio-test.py` | Mass ratio testing |
| `cuft-mechanism-derive.py` | Mechanism derivation |
| `cuft-mechanism.py` | Mechanism analysis |
| `cuft-nobel.py` | Nobel-grade verification |
| `cuft-nquark-factorization.py` | N-quark factorization |
| `cuft-ppb-hunt.py` | ppb-level search |
| `cuft-ppb-hunt2.py` | ppb-level search v2 |
| `cuft-prize.py` | Prize-grade verification |
| `cuft-quark-rule.py` | Quark rule analysis |
| `cuft-refined-hunt.py` | Refined constant search |
| `cuft-simplest-angles.py` | Simplest angle analysis |
| `cuft-solve.py` | Solver |
| `cuft-structural-analysis.py` | Structural analysis |
| `cuft-structural-test.py` | Structural testing |
| `cuft-third-constant-hunt.py` | Third constant search |

## License

All rights reserved. Paper and scripts are provided for review and independent replication purposes only.
