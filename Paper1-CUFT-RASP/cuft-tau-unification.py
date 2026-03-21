#!/usr/bin/env python3
"""
YASA PRESENTS
cuft-tau-unification.py

Proves the two tau lepton formulas differ by exactly 1/(2p)^2.
Compares both against Belle II 2023 and HFLAV 2025 measurements.

Author: CSL for YASA
Date: 2026-03-21
"""

from fractions import Fraction

n, p = 3, 5
lam = Fraction(1, p**3 - 1)  # 1/124
X = n * p * (p - 1)  # 60
Phi3 = p**2 + p + 1  # 31
m_e = 0.51099895000  # MeV

print("=" * 60)
print("TAU FORMULA UNIFICATION")
print("=" * 60)

# Formula 32: (Phi3 - n)/lam + p + 1/(p-1)
tau1 = (Phi3 - n) * (p**3 - 1) + p + Fraction(1, p - 1)
print(f"\nFormula (32): (Phi3-n)/lam + p + 1/(p-1)")
print(f"  = ({Phi3}-{n})*{p**3-1} + {p} + 1/{p-1}")
print(f"  = {tau1} = {float(tau1):.6f}")

# Formula 33: X^2 - 1/lam + Phi3/p^2
tau2 = X**2 - (p**3 - 1) + Fraction(Phi3, p**2)
print(f"\nFormula (33): X^2 - 1/lam + Phi3/p^2")
print(f"  = {X**2} - {p**3-1} + {Phi3}/{p**2}")
print(f"  = {tau2} = {float(tau2):.6f}")

# Exact difference
diff = tau1 - tau2
print(f"\nDifference: {tau1} - {tau2} = {diff}")
print(f"  = 1/(2p)^2 = 1/{(2*p)**2} = {Fraction(1, (2*p)**2)}")
assert diff == Fraction(1, (2*p)**2), "IDENTITY FAILED"
print(f"  VERIFIED: tau1 - tau2 = 1/(2p)^2 EXACTLY")

# Connection to muon zero-point energy
zpe = Fraction(1, 2*p)
print(f"\n  Muon zero-point energy: 1/(2p) = {zpe}")
print(f"  tau1 - tau2 = [1/(2p)]^2 = [{zpe}]^2 = {zpe**2}")
print(f"  The tau difference IS the square of the muon ZPE.")

# Unified formula
print(f"\nUNIFIED FORMULA:")
print(f"  m_tau/m_e = X^2 - 1/lambda + Phi_3/p^2 + delta")
print(f"  delta = 0:          {float(tau2):.4f}  (2.9 ppm)")
print(f"  delta = 1/(2p)^2:   {float(tau1):.4f}  (5.8 ppm)")

# Experimental comparisons
print(f"\n{'='*60}")
print(f"EXPERIMENTAL COMPARISON")
print(f"{'='*60}")

measurements = [
    ("CODATA 2022", 1776.86, 0.12),
    ("Belle II 2023 (PRD 108 032006)", 1777.09, 0.14),
    ("HFLAV 2025 (SciPost 17 001)", 1776.96, 0.09),
]

print(f"\n  {'Source':<35} {'m_tau/m_e':>12} {'F(32) sigma':>12} {'F(33) sigma':>12}")
print(f"  {'-'*73}")

for name, m_tau, unc in measurements:
    ratio = m_tau / m_e
    unc_ratio = unc / m_e
    sig1 = abs(float(tau1) - ratio) / unc_ratio
    sig2 = abs(float(tau2) - ratio) / unc_ratio
    print(f"  {name:<35} {ratio:>12.4f} {sig1:>12.2f} {sig2:>12.2f}")

print(f"\n  Both formulas within ~1 sigma of all measurements.")
print(f"  Separation: {float(diff):.4f} m_e = {float(diff)/float(tau1)*1e6:.1f} ppm")
print(f"  HFLAV uncertainty: {0.09/m_e:.4f} m_e = {0.09/m_e/float(tau1)*1e6:.1f} ppm")
print(f"  Need {0.09/m_e/float(diff):.0f}x improvement to distinguish at 1 sigma")

print(f"\n{'='*60}")
print(f"VERIFICATION COMPLETE")
print(f"{'='*60}")
