# Paper 1 — Final Audit Checklist
*Generated: 2026-03-21 14:40 CDT*
*Version: v0.7*

---

## 1. SCRIPTS — Referenced in Paper (must exist + run + produce correct results)

### Bohr Series (cuft-bohr-1.py through cuft-bohr-24.py)
- [x] cuft-bohr-1.py — Coherent energy, Diophantine discovery
- [x] cuft-bohr-2.py
- [x] cuft-bohr-3.py
- [x] cuft-bohr-4.py — Exact Gamma_classical = 24.84
- [x] cuft-bohr-5.py
- [x] cuft-bohr-6.py
- [x] cuft-bohr-7.py — Bohr quantization p = round(sqrt(Gamma))
- [x] cuft-bohr-8.py
- [x] cuft-bohr-9.py — Lambda = 1/(p^3-1) derivation
- [x] cuft-bohr-10.py
- [x] cuft-bohr-11.py — k = n self-consistency, Gamma ~ n^n
- [x] cuft-bohr-12.py
- [x] cuft-bohr-13.py
- [x] cuft-bohr-14.py
- [x] cuft-bohr-15.py
- [x] cuft-bohr-16.py
- [x] cuft-bohr-17.py — Nine dynamical tools exhausted
- [x] cuft-bohr-18.py
- [x] cuft-bohr-19.py
- [x] cuft-bohr-20.py
- [x] cuft-bohr-21.py — Virial-Diophantine equivalence, Lyapunov elimination
- [x] cuft-bohr-22.py — Occam uniqueness scan, c_{-1} = c_1^2 * Gamma
- [x] cuft-bohr-23.py — Exact kappa identity, c_1 physical identification
- [x] cuft-bohr-24.py — N-body coupled recursion, four derivation approaches

### Additional Verification Scripts (February 2026)
- [x] cuft-crosspoint-virial.py — Cross-fixed-point virial analysis
- [x] cuft-nquark-factorization.py — n-quark decomposition + CODATA + Monte Carlo
- [x] cuft-coupling-proof.py — Scaling/coefficient/uniqueness theorems for kappa
- [x] cuft-angle1-factorization-theorem.py — Factorization structural argument
- [x] cuft-angle2-derive-mass-formula.py — Derivation gap analysis + Cornell
- [x] cuft-angle3-complex-residue.py — Contour integral / complex residue
- [x] cuft-exact-identity-hunt.py — Exhaustive identity scan
- [x] cuft-simplest-angles.py — 10 algebraic approaches (Eqs 13-14)
- [x] cuft-fine-structure.py — Fine structure constant from (n,p)
- [x] cuft-inter-ratios.py — Inter-solution mass ratios and differences
- [x] cuft-lambda-correction.py — Second-order lambda correction
- [x] cuft-alpha-derivation.py — Alpha formula structural analysis
- [x] cuft-dynamical-proof-hunt.py — Exhaustive dynamical proof search (1400+)
- [x] cuft-refined-hunt.py — 6-phase constant search
- [x] cuft-verify-hits.py — Exact rational arithmetic verification
- [x] cuft-structural-analysis.py — 14-analysis structural investigation
- [x] cuft-dynamical-c1-proof.py — 22-analysis lambda-perturbative c_1
- [x] cuft-c1-extended-precision.py — 100-digit perturbation theory

### c_1 Uniqueness Proof Scripts (March 2026 — 9 attack vectors)
- [x] cuft-attack-bootstrap.py — Bootstrap Theorem (p-independence)
- [x] cuft-attack-denominator-closure.py — 3094-value rational sweep
- [x] cuft-attack-extremal.py — 4-functional extremal convergence
- [x] cuft-attack-lyapunov.py — Lyapunov exponent, multiplier, stability
- [x] cuft-attack-spectral-gap.py — Transfer matrix, modular arithmetic
- [x] cuft-attack-dissipative-v2.py — 3 dissipation models, cascade
- [x] cuft-attack-cubic-reciprocity.py — CRT, Frobenius, cyclotomic
- [x] cuft-attack-rg-fixed-point.py — RG flow, IR attractor, UV insensitivity
- [x] cuft-attack-p-adic.py — p-adic valuations, Hensel, adelic structure
- [x] cuft-attack-hopf-vortex.py — Torus knot winding, curl eigenspectrum, mode-locking

### Level 2 Extension + Sub-ppb Scripts (March 2026)
- [x] cuft-level1-hunt.py — 270-block greedy search
- [x] cuft-level1-verify.py — Exact Fraction arithmetic verification
- [x] cuft-ppb-hunt.py — PPB-precision correction term search
- [x] cuft-ppb-hunt2.py — Nuclear composite + g-factor analysis
- [x] cuft-subppb-corrections.py — Systematic sub-ppb correction search
- [x] cuft-2d-coupled-lattice.py — 2D coupled lattice time crystal
- [x] cuft-dissipative-selection.py — Dissipative selection proof
- [x] cuft-photonic-tc-design.py — Photonic time crystal experimental design

### Five-Pronged Selection Scripts (March 2026)
- [x] cuft-attack-stat-mech.py — Statistical mechanics selection
- [x] cuft-attack-number-theory.py — Number-theoretic derivations
- [x] cuft-attack-rep-theory.py — Representation theory (CG, E_8)
- [x] cuft-attack-variational.py — Variational ground state (Percival)
- [x] cuft-attack-info-theory.py — Information-theoretic elimination

### Derivation Route Scripts (March 2026)
- [x] cuft-derive-form-7routes.py — 7 derivation routes
- [x] cuft-derive-form-final-attack.py — 5 final attacks
- [x] cuft-denominator-quantization.py — DQT (508 rationals, integer p)

### Floquet/v0.7 Scripts (March 2026)
- [x] cuft-lambda-perturbation-derivation.py — Floquet eigenvalue derivation
- [x] cuft-tau-unification.py — Tau formula unification + Belle II/HFLAV
- [x] cuft-beltrami-t35-construction.py — T(3,5) Beltrami + Efimov spectral

### Other Scripts (March 2026, referenced elsewhere)
- [x] cuft-floquet-perturbation-derivation.py — Floquet propagator
- [x] cuft-tighten-q2-q7.py — Sub-ppb correction tightening
- [x] cuft-proof.py — Core proof script (passed in full audit, exit 0)

---

## 2. SCRIPTS — Exist but NOT referenced in paper (in directory but not cited)
*These are intermediate/exploratory scripts. Not required for repo.*
- To be catalogued after background audit completes

---

## 3. REFERENCES — All [N] citations verified
- [x] [1] CODATA 2022 — Tiesinga et al., JPCRD 54, 033105 (2025) ✓ CORRECTED (was 53/031101/2024)
- [x] [2] BMW Collaboration — Durr et al., Science 322, 1224 (2008) ✓
- [x] [3] Koide — Lett. Nuovo Cim. 34, 201 (1982) ✓
- [x] [4] Cornell potential — Eichten et al., PRD 17, 3090 (1978) ✓
- [x] [5] Dicke — Phys. Rev. 93, 99 (1954) ✓
- [x] [6] Bohr — Phil. Mag. 26, 1 (1913) ✓
- [x] [7] Efimov — Kraemer et al., Nature 440, 315 (2006) + Efimov PLB 33, 563 (1970) ✓
- [x] [8] 331 model — Pisano & Pleitez, PRD 46, 410 (1992) ✓
- [x] [9] 331 model — Frampton, PRL 69, 2889 (1992) ✓
- [x] [10] Carroll — Coherence Research, coherenceresearch.com (2026) ✓
- [x] [11] PDG 2024 — Workman et al., PTEP 2022, 083C01 ✓
- [x] [12] HFLAV 2024 — Amhis et al., Eur. Phys. J. C 84 (2024) ✓
- [x] [13] CODATA 2022 full — Tiesinga et al., Rev. Mod. Phys. 97, 025002 (2025) ✓
- [x] [14] Time crystals — Sacha & Zakrzewski, RPP 81, 016401 (2018) ✓
- [x] [15] DTC — Yao et al., PRL 118, 030401 (2017) ✓
- [x] [16] Beltrami — Etnyre & Ghrist, Nonlinearity 13, 441 (2000) ✓
- [x] [17] Curl eigenvalues — Bär & Strohmaier, Amer. J. Math. 141, 1421 (2019) ✓
- [x] [18] Icosahedral — Alkauskas, arXiv:1706.09295 (2020) ✓
- [x] [19] Hydro topology — Arnol'd & Khesin, Springer (1998) ✓
- [x] [20] McKay — Proc. Symp. Pure Math. 37, 183 (1980) ✓
- [x] [21] Jaynes — Phys. Rev. 106, 620 (1957) ✓
- [x] [22] Klein — Teubner (1884) ✓
- [x] [BI1] Belle II — PRD 108, 032006 (2023), arXiv:2305.19116 ✓ VERIFIED
- [x] [HF2] HFLAV 2025 — SciPost Phys. Proc. 17, 001 (2025) ✓ VERIFIED

---

## 4. KEY NUMERICAL CLAIMS — Verified against script output
- [x] M = 853811/465 = 1836.152688... (cuft-verify-hits.py) ✓ EXACT MATCH
- [x] 1/alpha = 34259/250 = 137.036000 (cuft-fine-structure.py) ✓ EXACT MATCH
- [x] m_n/m_e = 2120370001/1153200 (cuft-verify-hits.py) ✓ EXACT MATCH
- [x] m_mu/m_e = 384589/1860 (cuft-verify-hits.py) ✓ EXACT MATCH
- [x] ppb residuals: 8.0, 6.0, 1.1, 15.1 (cuft-verify-hits.py) ✓ MATCH
- [x] Corrected m_p/m_e = 13128197831/7149840 at 0.033 ppb (cuft-subppb-corrections.py) ✓
- [x] Corrected 1/alpha = 4082439451/29791000 at 0.118 ppb (cuft-subppb-corrections.py) ✓
- [x] Corrected m_n/m_e = 2120369999/1153200 at 0.009 ppb (cuft-subppb-corrections.py) ✓
- [x] Tau: 13909/4 - 86931/25 = 1/100 (cuft-tau-unification.py) ✓ EXACT
- [x] Beltrami eigenmode residual = 0 (cuft-beltrami-t35-construction.py) ✓ VERIFIED
- [x] DQT: 508 rationals, zero clean (cuft-denominator-quantization.py) ✓ EXACT
- [x] 18,605 Occam solutions scanned (cuft-bohr-22.py) ✓ EXACT
- [x] Bootstrap: c_1 = 3/5 unique (cuft-attack-bootstrap.py) ✓ PROVED
- [x] Muon formula: unique rational 384589/1860 (cuft-lambda-perturbation-derivation.py) ✓
- [x] Gamma_classical = 24.837669 ≈ 24.84 (cuft-bohr-4.py) ✓ EXACT MATCH
- [x] Sigmoid universality: all give p=5 (cuft-proof.py exit 0, cuft-bohr-11.py confirms Diophantine match)

---

## 5. arXiv VERSION
- [x] External/arXiv version synced with draft (name → YASA only) ✓
- [x] Grep for real name = zero instances ✓ CLEAN
- [x] All v0.7 additions present ✓ (copied from draft)

## 6. GIT REPO
- [x] All 103 scripts staged and committed ✓
- [x] arXiv version in repo (draft REMOVED from tracking) ✓
- [x] Commit b25ed18 created ✓
- [ ] Push to yasadevstudio/CUFT-RASP-Paper1 — AWAITING YASA AUTHORIZATION
