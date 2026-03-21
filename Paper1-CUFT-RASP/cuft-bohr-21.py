#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-21.py — Virial-Diophantine equivalence, Lyapunov elimination

Proves algebraically that the virial relation c_2 = 1/2 is equivalent
to the Diophantine equation (n-2)(p-1) = 4. Shows f'(x_s) = -lambda
exactly, eliminating Lyapunov as an independent constraint.
"""

from fractions import Fraction
import math

# ============================================================================
# PARAMETERS
# ============================================================================

n = Fraction(3)
p = Fraction(5)
Gamma = p ** 2                              # 25
lam = Fraction(1, int(p ** 3 - 1))         # 1/124
X = n * p * (p - 1)                        # 60
Phi3 = p ** 2 + p + 1                      # 31
M = Fraction(int(X) ** 2, 2) + Fraction(int(n), int(p)) * int(X) + Fraction(int(n) ** 2, int(X)) + lam / n

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-21: Virial-Diophantine equivalence, Lyapunov elimination")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: Algebraic equivalence n*(p-1) = 2*(p+1) iff (n-2)(p-1) = 4
# --------------------------------------------------------------------------
print()
print("--- SECTION 1: Algebraic equivalence proof ---")
print()
print("  CLAIM: n*(p-1) = 2*(p+1)  iff  (n-2)(p-1) = 4")
print()
print("  Forward direction: n*(p-1) = 2*(p+1) => (n-2)(p-1) = 4")
print("    n*(p-1) - 2*(p-1) = 2*(p+1) - 2*(p-1)")
print("    (n-2)*(p-1) = 2p + 2 - 2p + 2 = 4")
print()
print("  Reverse direction: (n-2)(p-1) = 4 => n*(p-1) = 2*(p+1)")
print("    (n-2)(p-1) = 4")
print("    n*(p-1) - 2*(p-1) = 4")
print("    n*(p-1) = 2*(p-1) + 4 = 2*p - 2 + 4 = 2*p + 2 = 2*(p+1)")
print()

# Verify for all three Diophantine solutions
dioph = [(3, 5), (4, 3), (6, 2)]
all_ok = True
for nn, pp in dioph:
    nf, pf = Fraction(nn), Fraction(pp)
    virial = nf * (pf - 1)
    rhs = 2 * (pf + 1)
    dioph_val = (nf - 2) * (pf - 1)
    check_v = (virial == rhs)
    check_d = (dioph_val == 4)
    all_ok = all_ok and check_v and check_d
    print(f"  ({nn},{pp}): n(p-1)={virial}, 2(p+1)={rhs}, equal={check_v}; "
          f"(n-2)(p-1)={dioph_val}, =4: {check_d}")

ok1 = all_ok
results.append(("Virial-Diophantine equivalence for all 3 solutions", ok1))
print(f"\n  All solutions satisfy equivalence: {'PASS' if ok1 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 2: c_2 = 1/2 verification
# --------------------------------------------------------------------------
print()
print("--- SECTION 2: c_2 = (p+1)/(n*(p-1)) = 1/2 ---")
print()

print(f"  c_2 = n*Gamma*(Gamma-1)/X^2")
print(f"      = (p+1)/(n*(p-1))")
print()

for nn, pp in dioph:
    nf, pf = Fraction(nn), Fraction(pp)
    c2 = (pf + 1) / (nf * (pf - 1))
    print(f"  ({nn},{pp}): c_2 = ({pp}+1)/({nn}*({pp}-1)) = {pf+1}/{nf*(pf-1)} = {c2}")

ok2 = True
for nn, pp in dioph:
    nf, pf = Fraction(nn), Fraction(pp)
    c2 = (pf + 1) / (nf * (pf - 1))
    ok2 = ok2 and (c2 == Fraction(1, 2))

results.append(("c_2 = 1/2 for all Diophantine solutions", ok2))
print(f"\n  All c_2 = 1/2: {'PASS' if ok2 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 3: Derive c_2 from scratch for (3,5)
# --------------------------------------------------------------------------
print()
print("--- SECTION 3: c_2 derivation from recursion parameters ---")
print()

# c_2 = n * Gamma * (Gamma - 1) / X^2
c2_full = n * Gamma * (Gamma - 1) / X ** 2
print(f"  c_2 = n * Gamma * (Gamma - 1) / X^2")
print(f"      = {n} * {Gamma} * {Gamma - 1} / {X}^2")
print(f"      = {n * Gamma * (Gamma - 1)} / {X ** 2}")
print(f"      = {c2_full}")

ok3 = (c2_full == Fraction(1, 2))
results.append(("c_2 from n*Gamma*(Gamma-1)/X^2 = 1/2", ok3))
print(f"  c_2 = 1/2: {'PASS' if ok3 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 4: f'(x_s) = -lambda (Lyapunov elimination)
# --------------------------------------------------------------------------
print()
print("--- SECTION 4: f'(x_s) = -lambda exactly ---")
print()

# Compute numerically
lam_f = float(lam)
Gamma_f = float(Gamma)
n_i = int(n)

def f(x):
    return Gamma_f * math.tanh(x) ** n_i - lam_f * x

def fp(x):
    t = math.tanh(x)
    return n_i * Gamma_f * t ** (n_i - 1) * (1 - t ** 2) - lam_f

# Find x_s via Newton
x_s = 24.0
for _ in range(100):
    g = f(x_s) - x_s
    gp = fp(x_s) - 1.0
    if abs(gp) < 1e-30:
        break
    x_s -= g / gp
    if abs(g) < 1e-14:
        break

fprime_xs = fp(x_s)
print(f"  x_s = {x_s:.15f}")
print(f"  f'(x_s) = {fprime_xs:.15f}")
print(f"  -lambda  = {-lam_f:.15f}")
print(f"  |f'(x_s) - (-lambda)| = {abs(fprime_xs + lam_f):.2e}")

ok4 = abs(fprime_xs + lam_f) < 1e-12
results.append(("f'(x_s) = -lambda to machine precision", ok4))
print(f"  f'(x_s) = -lambda: {'PASS' if ok4 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 5: Lyapunov is NOT independent
# --------------------------------------------------------------------------
print()
print("--- SECTION 5: Lyapunov elimination argument ---")
print()

print("  The multiplier f'(x_s) = -lambda is determined by:")
print("    1. The saturated regime: tanh(x_s) -> 1")
print("    2. The fixed-point equation: Gamma - lambda*x_s = x_s")
print("    3. Taking f'(x_s) = -lambda (from the derivative)")
print()
print("  This means lambda is BOTH:")
print("    (a) The damping constant (from Step 3: UV threshold)")
print("    (b) The stable multiplier |f'(x_s)|")
print()
print("  Therefore: the Lyapunov exponent ln(lambda) is NOT an")
print("  independent constraint. It is algebraically equivalent to")
print("  the UV threshold that already determined lambda = 1/(p^3-1).")
print()
print("  CONSEQUENCE: The virial relation c_2 = 1/2 (proved equivalent")
print("  to the Diophantine) plus f'(x_s) = -lambda (proved equivalent")
print("  to the UV threshold) means there are NO additional dynamical")
print("  constraints beyond those already in the 6-step derivation chain.")

# Verify: lambda * x_s = 1/p (kappa identity)
kappa_check = lam_f * x_s
print()
print(f"  Verification: lambda * x_s = {kappa_check:.15f}")
print(f"  1/p = {1/int(p):.15f}")
print(f"  |lambda*x_s - 1/p| = {abs(kappa_check - 1/int(p)):.2e}")

ok5 = abs(kappa_check - 1.0 / int(p)) < 1e-12
results.append(("lambda * x_s = 1/p (kappa identity)", ok5))
print(f"  kappa identity: {'PASS' if ok5 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 6: Exact mass formula verification
# --------------------------------------------------------------------------
print()
print("--- SECTION 6: M = 853811/465 exact ---")
print()

print(f"  M = X^2/2 + (n/p)*X + n^2/X + lambda/n")
print(f"    = {int(X)**2//2} + {Fraction(int(n),int(p))*int(X)} + {Fraction(int(n)**2,int(X))} + {lam/n}")
print(f"    = {M}")
print(f"    = {M.numerator}/{M.denominator}")
print(f"    = {float(M):.12f}")

ok6 = (M == Fraction(853811, 465))
results.append(("M = 853811/465 exactly", ok6))
print(f"  M = 853811/465: {'PASS' if ok6 else 'FAIL'}")

# 8 ppb check
CODATA_mu = 1836.152673426
frac_acc = abs(float(M) - CODATA_mu) / CODATA_mu
ppb_val = frac_acc * 1e9

print(f"  Fractional accuracy: {ppb_val:.1f} ppb")
ok7 = abs(ppb_val - 8.0) < 1.5
results.append(("Accuracy approximately 8 ppb", ok7))
print(f"  Accuracy ~ 8 ppb: {'PASS' if ok7 else 'FAIL'}")

# ============================================================================
# SUMMARY
# ============================================================================
print()
print("=" * 72)
print("SUMMARY")
print("=" * 72)
passed = sum(1 for _, ok in results if ok)
total = len(results)
for desc, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")
print(f"\n  {passed}/{total} checks passed.")
if passed == total:
    print("  ALL CHECKS PASSED.")
else:
    print(f"  WARNING: {total - passed} check(s) FAILED.")
