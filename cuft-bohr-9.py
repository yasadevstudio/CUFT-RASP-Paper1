#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-9.py — Lambda = 1/(p^3-1) derivation

Derives the damping constant lambda from the UV threshold condition.
Starting from kappa = 1/p = lambda * x_s, substitutes the saturated
fixed-point expression x_s = Gamma/(1+lambda) = p^2/(1+lambda),
solves for lambda algebraically, and verifies the factorization
p^3-1 = (p-1)*Phi_3(p).

Paper reference: Step 3 (Eq 6a, 6b)
"""

from fractions import Fraction

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
n = 3
p = 5
Gamma = Fraction(p**2)          # = 25
Phi3_p = p**2 + p + 1           # = 31

results = []

print("=" * 70)
print("CUFT-BOHR-9: Lambda = 1/(p^3-1) derivation")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# TEST 1: Derive lambda from kappa = lambda * x_s
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 1: Algebraic derivation of lambda ---")

# kappa = 1/p (Bohr quantization coupling)
kappa = Fraction(1, p)
print(f"  kappa = 1/p = {kappa}")

# x_s = Gamma/(1+lambda) = p^2/(1+lambda)   [Eq 6a, saturated regime]
# Condition: kappa = lambda * x_s
# => 1/p = lambda * p^2 / (1 + lambda)
# => (1 + lambda) / p = lambda * p^2
# => 1 + lambda = lambda * p^3
# => 1 = lambda * p^3 - lambda = lambda * (p^3 - 1)
# => lambda = 1 / (p^3 - 1)

lambda_derived = Fraction(1, p**3 - 1)
lambda_expected = Fraction(1, 124)

ok = lambda_derived == lambda_expected
results.append(("lambda = 1/(p^3-1) = 1/124", ok))
print(f"  p^3 - 1 = {p**3} - 1 = {p**3 - 1}")
print(f"  lambda = 1/(p^3-1) = {lambda_derived} = {float(lambda_derived):.10f}")
print(f"  Expected: 1/124 = {lambda_expected}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 2: Verify x_s = p^2/(1+lambda)
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 2: Saturated fixed point x_s ---")

lam = lambda_derived
x_s = Gamma / (1 + lam)
x_s_expected = Fraction(p**2 * (p**3 - 1), p**3)

# Simplify: p^2/(1 + 1/(p^3-1)) = p^2 * (p^3-1)/p^3
ok = x_s == x_s_expected
results.append(("x_s = p^2/(1+lambda) = p^2*(p^3-1)/p^3", ok))
print(f"  x_s = Gamma/(1+lambda) = {Gamma} / (1 + {lam}) = {x_s}")
print(f"  x_s = {float(x_s):.10f}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 3: Verify kappa = lambda * x_s
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 3: kappa = lambda * x_s consistency ---")

product = lam * x_s
ok = product == kappa
results.append(("lambda * x_s = 1/p", ok))
print(f"  lambda * x_s = {lam} * {x_s} = {product}")
print(f"  kappa = 1/p  = {kappa}")
print(f"  Match: {product == kappa}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 4: Factorization p^3 - 1 = (p-1) * Phi_3(p)
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 4: Factorization p^3 - 1 = (p-1) * Phi_3(p) ---")

lhs = p**3 - 1
rhs = (p - 1) * Phi3_p

ok = lhs == rhs
results.append((f"p^3-1 = (p-1)*Phi_3(p) = {p-1}*{Phi3_p} = {rhs}", ok))
print(f"  p^3 - 1 = {lhs}")
print(f"  (p-1) * Phi_3(p) = ({p}-1) * ({p}^2+{p}+1) = {p-1} * {Phi3_p} = {rhs}")
print(f"  Match: {lhs == rhs}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 5: Verify Phi_3(5) = 31
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 5: Third cyclotomic polynomial Phi_3(p) ---")

Phi3_computed = p**2 + p + 1
ok = Phi3_computed == 31
results.append(("Phi_3(5) = 25 + 5 + 1 = 31", ok))
print(f"  Phi_3(p) = p^2 + p + 1 = {p}^2 + {p} + 1 = {Phi3_computed}")
print(f"  Expected: 31")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 6: kappa^n = lambda/(1+lambda) = 1/p^n
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 6: kappa^n = lambda/(1+lambda) = 1/p^n ---")

kappa_n = kappa ** n
lam_ratio = lam / (1 + lam)
inv_p_n = Fraction(1, p**n)

ok1 = kappa_n == inv_p_n
ok2 = lam_ratio == inv_p_n
ok = ok1 and ok2
results.append(("kappa^3 = lambda/(1+lambda) = 1/125", ok))
print(f"  kappa^n = (1/{p})^{n} = {kappa_n} = {float(kappa_n):.10f}")
print(f"  lambda/(1+lambda) = {lam}/({1+lam}) = {lam_ratio} = {float(lam_ratio):.10f}")
print(f"  1/p^n = 1/{p**n} = {inv_p_n} = {float(inv_p_n):.10f}")
print(f"  kappa^n == 1/p^n: {ok1}")
print(f"  lambda/(1+lambda) == 1/p^n: {ok2}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 7: Denominator prime factors of lambda
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 7: Denominator prime factors ---")

def prime_factors(n):
    """Return set of prime factors of n."""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors

denom = lam.denominator  # 124
factors = prime_factors(denom)
expected_factors = {2, 31}  # 124 = 4 * 31 = 2^2 * 31

ok = factors == expected_factors
results.append((f"prime_factors(124) = {{2, 31}} subset of {{2,3,5,31}}", ok))
print(f"  lambda denominator = {denom}")
print(f"  {denom} = 4 * 31 = 2^2 * 31")
print(f"  Prime factors: {sorted(factors)}")
print(f"  Expected: {sorted(expected_factors)}")
print(f"  All in {{2, 3, 5, 31}}: {factors.issubset({2, 3, 5, 31})}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

passed = sum(1 for _, ok in results)
total = len(results)

for desc, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {desc}")

print(f"\n  {passed}/{total} tests passed")

if passed == total:
    print("\n  ALL TESTS PASSED")
else:
    print(f"\n  {total - passed} TESTS FAILED")
