# CUFT-RASP

**Recursive Algebraic Structure of Physical Constants (RASP) within the Compactified Universal Field Theory (CUFT) framework.**

By Eliseu Spiller de Barros Lima (YASA Development Studio)

## Repository Purpose

This repository contains the **publishing versions** of the CUFT-RASP papers and **all scripts and data required for independent replication** of every numerical result claimed in the papers. Nothing else.

## Papers

| Paper | File | Description |
|-------|------|-------------|
| **Paper 1** | `CUFT-RASP-PUBLICATION-DRAFT-2026-02-12.txt` | RASP framework: derives muon mass, fine-structure constant, proton and neutron mass ratios from a single recursion with zero free parameters |
| **Paper 2** | `CUFT-RASP-ORCH-OR-BRIDGE-2026-03-02.txt` | Orch-OR Bridge: connects RASP's (n,p) = (3,5) to the tubulin aromatic triad (Trp-407, Phe-404, Tyr-408) and Penrose-Hameroff orchestrated objective reduction |

## Replication

Every numerical claim in both papers can be verified by running the corresponding Python script. Scripts require only standard Python 3 with numpy/scipy.

### Paper 1 Scripts

| Script | Verifies |
|--------|----------|
| `cuft-final.py` | Core RASP recursion, all 4 physical constants, ppb-level precision |
| `cuft-denominator-quantization.py` | Denominator Quantization Theorem (integer p required) |
| `cuft-dissipative-selection.py` | Dissipative selection: only (3,5) survives among Diophantine solutions |
| `cuft-floquet-analysis.py` | Floquet/time-crystal analysis of the recursion |
| `cuft-2d-coupled-lattice.py` | 2D coupled map lattice (pion mass extension) |
| `cuft-photonic-tc-design.py` | Photonic time crystal experimental design |
| `cuft-bohr-*.py` (1-24) | Bohr step verification suite (166/166 checks) |
| `cuft-alpha-derivation.py` | Fine-structure constant derivation path |
| `cuft-neutron-mass.py` | Neutron mass ratio derivation |
| `cuft-c1-extended-precision.py` | Extended precision verification of c_1 |
| `cuft-subppb-corrections.py` | Sub-ppb correction terms |

### Paper 2 Scripts

| Script | Verifies |
|--------|----------|
| `cuft-penrose-or-bridge.py` | Orch-OR bridge calculations, E_G correction, frequency predictions |
| `cuft-triad-exciton-hamiltonian.py` | 13-state Frenkel exciton Hamiltonian diagonalization (V/Delta_E bounds) |
| `cuft-n3-meanfield-exact.py` | Exact N=3 Ising partition function vs mean-field comparison |
| `cuft-aromatic-decoherence.py` | Aromatic triad decoherence estimates |
| `cuft-spin-boson-decoherence.py` | Spin-boson model decoherence calculation |
| `cuft-triad-decoherence-complete.py` | Complete triad decoherence analysis |
| `pdb-aromatic-triad-search.py` | PDB structure search for aromatic triads (requires 1JFF.pdb) |

### Data Files

| File | Purpose |
|------|---------|
| `1JFF.pdb` | Tubulin crystal structure (PDB ID: 1JFF) for aromatic triad verification |

## What Is NOT In This Repo

Research notes, external/simplified paper versions, primary source extractions, review correspondence, and PDF references are kept locally but not published here. This repo contains only what is needed to read the papers and replicate every result.

## License

All rights reserved. Papers and scripts are provided for review and replication purposes only.
