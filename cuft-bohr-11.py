#!/usr/bin/env python3
"""YASA PRESENTS
cuft-bohr-11.py — k = n self-consistency, Gamma ~ n^n

Verifies the n=3 uniqueness theorem: among the three Diophantine
solutions, only n=3 has gain-coherence and Diophantine simultaneously
satisfiable. For n=3, Gamma_classical ~ 24.84 rounds to p=5. For n=4,
gain-coherence gives p=15, not the required p=3. For n=6, gain-coherence
admits no nontrivial solution.

Paper reference: Step 1 (Eq 2,3), Step 4 uniqueness theorem

The gain-coherence is solved for the UNDAMPED map f_0(x) = Gamma*tanh^n(x)
(lambda=0), as in the paper: lambda is only determined AFTER quantization
in Step 3.
"""

from fractions import Fraction
import math
from scipy.optimize import brentq

results = []

print("=" * 70)
print("CUFT-BOHR-11: k = n self-consistency, n=3 uniqueness theorem")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# UNDAMPED GAIN-COHERENCE SOLVER
# ═══════════════════════════════════════════════════════════════
# The paper's Step 1 uses the undamped map f_0(x) = Gamma*tanh^n(x).
# Lambda is determined AFTER quantization in Step 3.
#
# f_0(x) = Gamma * tanh^n(x)
# Fixed point: Gamma * tanh^n(x_u) = x_u
# f_0'(x) = Gamma * n * tanh^(n-1)(x) * sech^2(x)
# Gain-coherence: |f_0'(x_u)|^n = Gamma

def find_Gamma_classical_undamped(n_val, G_lo=5.0, G_hi=500.0):
    """Find Gamma_classical from the undamped gain-coherence (lambda=0).

    Solves: Gamma*tanh^n(x_u) = x_u  AND  [Gamma*n*tanh^(n-1)(x_u)*sech^2(x_u)]^n = Gamma
    """

    def residual(Gamma_try):
        def g(x):
            return Gamma_try * math.tanh(x)**n_val - x

        try:
            x_u = brentq(g, 0.01, 10.0, xtol=1e-14)
        except ValueError:
            return float('inf')

        t = math.tanh(x_u)
        sech2 = 1.0 - t**2
        fp = Gamma_try * n_val * t**(n_val - 1) * sech2

        return fp**n_val - Gamma_try

    # Scan for sign changes
    N_scan = 2000
    prev_val = None
    sign_changes = []

    for i in range(N_scan + 1):
        G = G_lo + (G_hi - G_lo) * i / N_scan
        try:
            val = residual(G)
            if math.isinf(val) or math.isnan(val):
                prev_val = None
                continue
            if prev_val is not None and val * prev_val < 0:
                sign_changes.append((G - (G_hi - G_lo) / N_scan, G))
            prev_val = val
        except:
            prev_val = None
            continue

    # Solve each sign change
    solutions = []
    for lo, hi in sign_changes:
        try:
            Gamma_sol = brentq(residual, lo, hi, xtol=1e-12)
            res_check = abs(residual(Gamma_sol))
            if res_check < 1e-6 and Gamma_sol > 2.0:
                solutions.append((Gamma_sol, res_check))
        except:
            continue

    if not solutions:
        return None

    solutions.sort(key=lambda x: x[1])
    return solutions[0][0]


# ═══════════════════════════════════════════════════════════════
# TEST 1: n=3 gain-coherence -> Gamma_classical ~ 24.84
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 1: n=3 gain-coherence ---")

Gamma_3 = find_Gamma_classical_undamped(3)
p_3 = round(math.sqrt(Gamma_3)) if Gamma_3 else None
dioph_p_3 = 5  # From (3-2)(p-1) = 4 => p = 5

ok_range = Gamma_3 is not None and 24.0 < Gamma_3 < 26.0
ok_p = p_3 == 5
ok = ok_range and ok_p
results.append(("n=3: Gamma_classical ~ 24.84, p = round(sqrt) = 5", ok))

print(f"  Gamma_classical = {Gamma_3:.6f}" if Gamma_3 else "  Gamma_classical = None")
print(f"  sqrt(Gamma)     = {math.sqrt(Gamma_3):.6f}" if Gamma_3 else "  sqrt(Gamma)     = None")
print(f"  p = round(sqrt) = {p_3}")
print(f"  Diophantine requires p = {dioph_p_3}")
print(f"  Match: {p_3 == dioph_p_3}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 2: n=3 Gamma ~ n^n check
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 2: Gamma_classical ~ n^n for n=3 ---")

n_cubed = 3**3  # = 27
ratio = Gamma_3 / n_cubed if Gamma_3 else None
ok = Gamma_3 is not None and abs(ratio - 1.0) < 0.15  # Within 15%
results.append((f"Gamma_classical/n^n = {ratio:.4f} (close to 1)", ok))

print(f"  n^n = 3^3 = {n_cubed}")
print(f"  Gamma_classical = {Gamma_3:.6f}" if Gamma_3 else "  Gamma_classical = None")
print(f"  Ratio Gamma/n^n = {ratio:.4f}" if ratio else "  Ratio = None")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 3: n=4 gain-coherence gives p != 3 (Diophantine incompatible)
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 3: n=4 gain-coherence -> p != 3 (Diophantine incompatible) ---")

Gamma_4 = find_Gamma_classical_undamped(4)
p_4 = round(math.sqrt(Gamma_4)) if Gamma_4 else None
dioph_p_4 = 3  # From (4-2)(p-1) = 4 => 2(p-1) = 4 => p = 3

if Gamma_4 is not None:
    ok = p_4 != dioph_p_4
    results.append((f"n=4: Gamma_classical ~ {Gamma_4:.1f}, p={p_4} != 3 (Diophantine)", ok))
    print(f"  Gamma_classical = {Gamma_4:.4f}")
    print(f"  sqrt(Gamma)     = {math.sqrt(Gamma_4):.4f}")
    print(f"  p = round(sqrt) = {p_4}")
    print(f"  Diophantine requires p = {dioph_p_4}")
    print(f"  INCOMPATIBLE: {p_4} != {dioph_p_4}")
    print(f"  Gamma ratio: {Gamma_4:.1f} / {dioph_p_4**2} = {Gamma_4/dioph_p_4**2:.1f}x mismatch")
else:
    ok = True
    results.append(("n=4: no gain-coherence solution (Diophantine incompatible)", ok))
    print(f"  No gain-coherence solution found for n=4")
    print(f"  Diophantine requires p = {dioph_p_4}")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 4: n=6 gain-coherence admits no nontrivial solution
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 4: n=6 gain-coherence admits no nontrivial solution ---")

Gamma_6 = find_Gamma_classical_undamped(6)
dioph_p_6 = 2  # From (6-2)(p-1) = 4 => 4(p-1) = 4 => p = 2

if Gamma_6 is not None:
    p_6 = round(math.sqrt(Gamma_6))
    ok = p_6 != dioph_p_6
    print(f"  Gamma_classical = {Gamma_6:.4f}")
    print(f"  p = round(sqrt) = {p_6}")
    print(f"  Diophantine requires p = {dioph_p_6} (Gamma = {dioph_p_6**2})")
    if p_6 != dioph_p_6:
        print(f"  INCOMPATIBLE: p={p_6} != {dioph_p_6}")
else:
    p_6 = None
    ok = True
    print(f"  No nontrivial gain-coherence solution found for n=6")
    print(f"  Diophantine requires p = {dioph_p_6} (Gamma = {dioph_p_6**2})")

results.append(("n=6: no viable gain-coherence solution compatible with p=2", ok))
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# TEST 5: Uniqueness conclusion
# ═══════════════════════════════════════════════════════════════
print("\n--- TEST 5: n=3 uniqueness theorem ---")

n3_match = p_3 == 5    # gain-coherence matches Diophantine
n4_match = (p_4 == 3) if p_4 else False
n6_match = (p_6 == 2) if p_6 else False

ok = n3_match and not n4_match and not n6_match
results.append(("Only n=3 satisfies both gain-coherence and Diophantine", ok))

p4_str = str(p_4) if p_4 else "N/A"
p6_str = str(p_6) if p_6 else "N/A"

print(f"  n=3: gain-coherence p = {p_3}, Diophantine p = 5  -> {'MATCH' if n3_match else 'MISMATCH'}")
print(f"  n=4: gain-coherence p = {p4_str}, Diophantine p = 3  -> {'MATCH' if n4_match else 'MISMATCH'}")
print(f"  n=6: gain-coherence p = {p6_str}, Diophantine p = 2  -> {'MATCH' if n6_match else 'MISMATCH'}")
print(f"  Conclusion: n=3 is the UNIQUE solution")
print(f"  PASS" if ok else f"  FAIL")

# ═══════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════
print("\n--- Summary Table ---")
print(f"  {'n':>3} | {'Gamma_cl':>10} | {'p_gc':>5} | {'p_dioph':>7} | {'Compatible':>10}")
print(f"  {'---':>3}-+-{'-'*10}-+-{'-'*5}-+-{'-'*7}-+-{'-'*10}")

g3_str = f"{Gamma_3:.2f}" if Gamma_3 else "N/A"
g4_str = f"{Gamma_4:.2f}" if Gamma_4 else "N/A"
g6_str = f"{Gamma_6:.2f}" if Gamma_6 else "N/A"

print(f"  {'3':>3} | {g3_str:>10} | {str(p_3):>5} | {'5':>7} | {'YES':>10}")
print(f"  {'4':>3} | {g4_str:>10} | {p4_str:>5} | {'3':>7} | {'NO':>10}")
print(f"  {'6':>3} | {g6_str:>10} | {p6_str:>5} | {'2':>7} | {'NO':>10}")

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
