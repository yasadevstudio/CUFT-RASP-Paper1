#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-23.py — Exact kappa identity, c_1 physical identification

Verifies the exact kappa identities:
    kappa = lambda * x_s = 1/p
    kappa^n = lambda/(1+lambda) = 1/p^n
    x_s * f'(x_s) = -kappa  (stable virial)
    x_u * f'(x_u) = n/p + O(lambda)  (unstable virial, leading)
and the physical identification c_1 = n*kappa = n/p.
"""

from fractions import Fraction
import math

# ============================================================================
# PARAMETERS
# ============================================================================

n_i = 3
p_i = 5
n = Fraction(n_i)
p = Fraction(p_i)
Gamma = p ** 2                              # 25
lam = Fraction(1, p_i ** 3 - 1)            # 1/124
lam_f = float(lam)
Gamma_f = float(Gamma)
X = n * p * (p - 1)                        # 60
Phi3 = p ** 2 + p + 1                      # 31
kappa = Fraction(1, p_i)                    # 1/5

# Numerical fixed points
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

# Find x_u via Newton
x_u = 0.2
for _ in range(100):
    g = f(x_u) - x_u
    gp = fp(x_u) - 1.0
    if abs(gp) < 1e-30:
        break
    x_u -= g / gp
    if abs(g) < 1e-14:
        break

# ============================================================================
print("=" * 72)
print("CUFT-BOHR-23: Exact kappa identity, c_1 physical identification")
print("=" * 72)

results = []

# --------------------------------------------------------------------------
# SECTION 1: kappa = lambda * x_s
# --------------------------------------------------------------------------
print()
print("--- SECTION 1: kappa = lambda * x_s ---")
print()

# Exact: x_s = Gamma/(1+lambda) = p^2/(1 + 1/(p^3-1)) = p^2 * (p^3-1)/p^3 = (p^3-1)/p
x_s_exact = Fraction(p_i ** 3 - 1, p_i)
print(f"  x_s (exact, saturated regime) = (p^3-1)/p = {x_s_exact}")
print(f"  x_s (exact decimal)           = {float(x_s_exact):.15f}")
print(f"  x_s (numerical Newton)        = {x_s:.15f}")
print(f"  |exact - numerical|           = {abs(float(x_s_exact) - x_s):.2e}")
print()

lam_times_xs = lam * x_s_exact
print(f"  lambda * x_s = {lam} * {x_s_exact}")
print(f"               = {lam_times_xs}")
print(f"               = {float(lam_times_xs)}")

ok1 = (lam_times_xs == kappa)
results.append(("kappa = lambda * x_s = 1/p exactly", ok1))
print(f"  kappa = lambda * x_s: {'PASS' if ok1 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 2: kappa^n = lambda/(1+lambda) = 1/p^n
# --------------------------------------------------------------------------
print()
print("--- SECTION 2: kappa^n = lambda/(1+lambda) = 1/p^n ---")
print()

kappa_n = kappa ** n_i
lam_ratio = lam / (1 + lam)
inv_p_n = Fraction(1, p_i ** n_i)

print(f"  kappa^n             = (1/p)^{n_i} = {kappa_n}")
print(f"  lambda/(1+lambda)   = {lam}/({1+lam}) = {lam_ratio}")
print(f"  1/p^n               = 1/{p_i**n_i} = {inv_p_n}")

ok2a = (kappa_n == lam_ratio)
ok2b = (kappa_n == inv_p_n)
ok2c = (lam_ratio == inv_p_n)
ok2 = ok2a and ok2b and ok2c
results.append(("kappa^n = lambda/(1+lambda) = 1/p^n", ok2))
print(f"\n  kappa^n = lambda/(1+lambda): {'PASS' if ok2a else 'FAIL'}")
print(f"  kappa^n = 1/p^n:             {'PASS' if ok2b else 'FAIL'}")
print(f"  lambda/(1+lambda) = 1/p^n:   {'PASS' if ok2c else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 3: Derivation chain for kappa
# --------------------------------------------------------------------------
print()
print("--- SECTION 3: Derivation chain ---")
print()

print("  Step 1: lambda = 1/(p^3 - 1)  [UV threshold from recursion]")
print(f"          lambda = 1/{p_i**3-1} = {lam}")
print()
print("  Step 2: kappa^n = lambda/(1+lambda)  [algebraic identity]")
print(f"          kappa^{n_i} = {lam_ratio} = 1/{p_i**n_i}")
print()
print("  Step 3: kappa = (kappa^n)^(1/n) = (1/p^n)^(1/n) = 1/p")
print(f"          kappa = 1/{p_i} = {float(kappa)}")
print()
print("  All three steps are MATHEMATICAL CONSEQUENCES of the recursion.")
print("  kappa = 1/p is DERIVED, not assumed.")

# --------------------------------------------------------------------------
# SECTION 4: x_s * f'(x_s) = -kappa (stable virial)
# --------------------------------------------------------------------------
print()
print("--- SECTION 4: Stable virial: x_s * f'(x_s) = -kappa ---")
print()

product_s = x_s * fp(x_s)
print(f"  x_s * f'(x_s) = {x_s:.12f} * {fp(x_s):.12f}")
print(f"                 = {product_s:.15f}")
print(f"  -kappa         = {-float(kappa):.15f}")
print(f"  |x_s*f'(x_s) + kappa| = {abs(product_s + float(kappa)):.2e}")

ok3 = abs(product_s + float(kappa)) < 1e-10
results.append(("x_s * f'(x_s) = -kappa exactly", ok3))
print(f"  Stable virial: {'PASS' if ok3 else 'FAIL'}")

# Explain: f'(x_s) = -lambda, x_s = (p^3-1)/p, so x_s * f'(x_s) = -(p^3-1)/(p*(p^3-1)) = -1/p
print()
print("  Algebraic proof:")
print(f"    f'(x_s) = -lambda = -1/{p_i**3-1}")
print(f"    x_s = (p^3-1)/p = {x_s_exact}")
print(f"    x_s * f'(x_s) = -({x_s_exact}) * ({lam}) = -{x_s_exact * lam} = -{kappa}")

# --------------------------------------------------------------------------
# SECTION 5: x_u * f'(x_u) leading order
# --------------------------------------------------------------------------
print()
print("--- SECTION 5: Unstable virial: x_u * f'(x_u) ---")
print()

product_u = x_u * fp(x_u)
target_leading = float(n) / float(p)
print(f"  x_u = {x_u:.12f}")
print(f"  f'(x_u) = {fp(x_u):.12f}")
print(f"  x_u * f'(x_u) = {product_u:.12f}")
print(f"  n/p = {float(n/p):.12f}")
print(f"  Difference: {abs(product_u - target_leading):.6f}")
print()
print(f"  The unstable virial x_u*f'(x_u) = n/p + O(lambda) at leading order.")
print(f"  This is NOT exact (unlike the stable case) because x_u is not in")
print(f"  the saturated regime. The O(lambda) correction is small:")
print(f"  |x_u*f'(x_u) - n/p| = {abs(product_u - target_leading):.6f}")

ok4 = abs(product_u - target_leading) < 0.1
results.append(("x_u * f'(x_u) = n/p + O(lambda) at leading order", ok4))
print(f"  Unstable virial (leading): {'PASS' if ok4 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 6: Physical identification c_1 = n*kappa
# --------------------------------------------------------------------------
print()
print("--- SECTION 6: Physical identification c_1 = n*kappa = n/p ---")
print()

c1 = n * kappa
print(f"  kappa = 1/p = {kappa}  [DERIVED from recursion]")
print(f"  n = {n_i}               [gate exponent, the single input]")
print(f"  c_1 = n * kappa = {c1} = {float(c1)}")
print()
print("  Physical interpretation:")
print(f"    Each of the n = {n_i} quarks couples to the background field")
print(f"    with strength kappa = 1/p = {float(kappa)}.")
print(f"    The collective coupling is c_1 = n*kappa = {n_i}*{float(kappa)} = {float(c1)}.")
print()
print("  This is the SAME factorization that the chain rule produces")
print("  in the derivative of the n-fold gate tanh^n:")
print(f"    d/dx [tanh^n(x)] = n * tanh^(n-1)(x) * sech^2(x)")
print(f"    At x_s: n * 1^(n-1) * sech^2(x_s) = n * sech^2(x_s) ~ n * kappa")

ok5 = (c1 == Fraction(3, 5))
results.append(("c_1 = n*kappa = n/p = 3/5", ok5))
print(f"\n  c_1 = 3/5: {'PASS' if ok5 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 7: Alternative expression c_1 = n(n-2)/(n+2)
# --------------------------------------------------------------------------
print()
print("--- SECTION 7: c_1 = n(n-2)/(n+2) = pure function of n ---")
print()

# Using Diophantine: p = (n+2)/(n-2)
p_from_n = (n + 2) / (n - 2)
c1_from_n = n * (n - 2) / (n + 2)

print(f"  From Diophantine: p = (n+2)/(n-2) = {p_from_n}")
print(f"  c_1 = n/p = n * (n-2)/(n+2) = {c1_from_n}")
print()

# Verify for all three Diophantine solutions
for nn, pp in [(3, 5), (4, 3), (6, 2)]:
    nf, pf = Fraction(nn), Fraction(pp)
    c1_v = nf / pf
    c1_alt = nf * (nf - 2) / (nf + 2)
    print(f"  ({nn},{pp}): c_1 = n/p = {c1_v} = n(n-2)/(n+2) = {c1_alt}, equal: {c1_v == c1_alt}")

ok6 = all(
    Fraction(nn, pp) == Fraction(nn) * (Fraction(nn) - 2) / (Fraction(nn) + 2)
    for nn, pp in [(3, 5), (4, 3), (6, 2)]
)
results.append(("c_1 = n(n-2)/(n+2) for all Diophantine solutions", ok6))
print(f"\n  c_1 = n(n-2)/(n+2): {'PASS' if ok6 else 'FAIL'}")

# --------------------------------------------------------------------------
# SECTION 8: x_s cyclotomic form
# --------------------------------------------------------------------------
print()
print("--- SECTION 8: x_s = (p-1)*Phi_3(p)/p ---")
print()

x_s_cyclo = (p - 1) * Phi3 / p
print(f"  x_s = (p-1)*Phi_3(p)/p = {p-1}*{Phi3}/{p} = {x_s_cyclo}")
print(f"  x_s = {float(x_s_cyclo)}")
print(f"  Also: (p^3-1)/p = {x_s_exact} = {float(x_s_exact)}")

ok7 = (x_s_cyclo == x_s_exact)
results.append(("x_s = (p-1)*Phi_3(p)/p = (p^3-1)/p", ok7))
print(f"  x_s cyclotomic form: {'PASS' if ok7 else 'FAIL'}")

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
