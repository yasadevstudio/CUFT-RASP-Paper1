#!/usr/bin/env python3
"""
CUFT-RASP: VERIFY TOP HITS FROM REFINED HUNT
==============================================
YASA PRESENTS — 2026-02-24

Exact arithmetic verification of the best candidates.
"""

from fractions import Fraction

# ═══════════════════════════════════════════════════════════════════
# RASP CONSTANTS
# ═══════════════════════════════════════════════════════════════════

n, p = 3, 5
G = p**2                      # 25
L = Fraction(1, p**3 - 1)     # 1/124
X = n * p * (p - 1)           # 60
Phi3 = p**2 + p + 1           # 31

# Proton mass (exact)
M = Fraction(X**2, 2) + Fraction(n, p) * X + Fraction(n**2, X) + L / n
inv_alpha = Fraction(p**3) + n*(p-1) + Fraction(n**2, 2*p**3)

# Experimental values (CODATA 2022)
mp_exp = 1836.152673426     # m_p/m_e (32)
mn_exp = 1838.68366173      # m_n/m_e (89)
mu_exp = 206.7682827        # m_μ/m_e (46)

def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def show_rasp_factorization(num, label=""):
    """Show how a number factorizes in terms of n=3, p=5, Phi3=31."""
    factors = factorize(abs(num))
    factor_str = " × ".join(str(f) for f in factors)

    # Try to express in RASP terms
    rasp_parts = []
    temp = abs(num)
    n_count = 0
    p_count = 0
    phi3_count = 0
    two_count = 0

    while temp % 2 == 0:
        two_count += 1
        temp //= 2
    while temp % 3 == 0:
        n_count += 1
        temp //= 3
    while temp % 5 == 0:
        p_count += 1
        temp //= 5
    while temp % 31 == 0:
        phi3_count += 1
        temp //= 31

    rasp = []
    if two_count: rasp.append(f"2^{two_count}" if two_count > 1 else "2")
    if n_count: rasp.append(f"n^{n_count}" if n_count > 1 else "n")
    if p_count: rasp.append(f"p^{p_count}" if p_count > 1 else "p")
    if phi3_count: rasp.append(f"Φ₃^{phi3_count}" if phi3_count > 1 else "Φ₃")
    if temp > 1: rasp.append(str(temp))

    rasp_str = "·".join(rasp) if rasp else "1"
    return f"{num} = {factor_str} = {rasp_str}"


print("=" * 90)
print("CUFT-RASP: EXACT VERIFICATION OF TOP HITS")
print("=" * 90)

# ═══════════════════════════════════════════════════════════════════
# HIT 1: NEUTRON MASS — 1.1 ppb version
# m_n/m_e = M + p/2 + n²/(pX) + np/(p³-1)²
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("HIT 1: NEUTRON MASS — 4-term correction")
print("─" * 90)

delta_1a = Fraction(p, 2)                    # 5/2
delta_1b = Fraction(n**2, p * X)             # 9/300 = 3/100
delta_1c = Fraction(n * p, (p**3 - 1)**2)   # 15/15376

delta_total = delta_1a + delta_1b + delta_1c
M_n_v1 = M + delta_total

print(f"\n  m_n/m_e = M + p/2 + n²/(pX) + np/(p³-1)²")
print(f"\n  Term-by-term:")
print(f"    M          = {M} = {float(M):.12f}")
print(f"    p/2        = {delta_1a} = {float(delta_1a):.12f}")
print(f"    n²/(pX)    = {delta_1b} = {float(delta_1b):.12f}")
print(f"    np/(p³-1)² = {delta_1c} = {float(delta_1c):.12f}")
print(f"\n  Total delta  = {delta_total}")
print(f"               = {float(delta_total):.12f}")
print(f"\n  m_n/m_e      = {M_n_v1}")
print(f"               = {float(M_n_v1):.15f}")
print(f"\n  Experimental:  {mn_exp:.15f}")
print(f"  Error: {abs(float(M_n_v1) - mn_exp) / mn_exp * 1e9:.1f} ppb")
print(f"\n  Numerator:   {M_n_v1.numerator}")
print(f"  Denominator: {show_rasp_factorization(M_n_v1.denominator)}")
print(f"\n  np/(p³-1)² = {n}·{p}/({p**3-1})² = {n*p}/{(p**3-1)**2}")
print(f"  Note: (p³-1) = {p**3-1} = 4·Φ₃(p) = 4·{Phi3}")
print(f"  So (p³-1)² = 16·Φ₃² = 16·{Phi3**2} = {16*Phi3**2}")
print(f"  np/(p³-1)² = np/(16·Φ₃²) = {n*p}/(16·{Phi3**2}) = {Fraction(n*p, 16*Phi3**2)}")

# ═══════════════════════════════════════════════════════════════════
# HIT 2: NEUTRON MASS — 3.2 ppb version (alternative delta)
# m_n/m_e = M + p/2 + n/(p²(p-1)) + n²/(Φ₃·p·X)
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("HIT 2: NEUTRON MASS — 3-term correction (alternative)")
print("─" * 90)

delta_2a = Fraction(p, 2)                          # 5/2
delta_2b = Fraction(n, p**2 * (p - 1))             # 3/100
delta_2c = Fraction(n**2, Phi3 * p * X)            # 9/9300

delta_total2 = delta_2a + delta_2b + delta_2c
M_n_v2 = M + delta_total2

print(f"\n  m_n/m_e = M + p/2 + n/(p²(p-1)) + n²/(Φ₃·p·X)")
print(f"\n  Term-by-term:")
print(f"    M              = {M} = {float(M):.12f}")
print(f"    p/2            = {delta_2a} = {float(delta_2a):.12f}")
print(f"    n/(p²(p-1))    = {delta_2b} = {float(delta_2b):.12f}")
print(f"    n²/(Φ₃·p·X)   = {delta_2c} = {float(delta_2c):.12f}")
print(f"\n  Total delta  = {delta_total2}")
print(f"               = {float(delta_total2):.12f}")
print(f"\n  m_n/m_e      = {M_n_v2}")
print(f"               = {float(M_n_v2):.15f}")
print(f"\n  Experimental:  {mn_exp:.15f}")
print(f"  Error: {abs(float(M_n_v2) - mn_exp) / mn_exp * 1e9:.1f} ppb")
print(f"\n  Numerator:   {M_n_v2.numerator}")
print(f"  Denominator: {show_rasp_factorization(M_n_v2.denominator)}")

# Check: is n/(p²(p-1)) the same as n²/(pX)?
print(f"\n  CHECK: n/(p²(p-1)) = {Fraction(n, p**2*(p-1))} = {float(Fraction(n, p**2*(p-1))):.12f}")
print(f"         n²/(pX)     = {Fraction(n**2, p*X)} = {float(Fraction(n**2, p*X)):.12f}")
print(f"         Same? {Fraction(n, p**2*(p-1)) == Fraction(n**2, p*X)}")

# So the original 2-term delta was p/2 + n²/(pX) = p/2 + 3/100
# And this 3-term version splits the second term differently
# Let's see what the actual difference is
print(f"\n  Original 2-term delta:     p/2 + n²/(pX) = {Fraction(p,2) + Fraction(n**2, p*X)}")
print(f"  New 3-term delta:          p/2 + n/(p²(p-1)) + n²/(Φ₃pX) = {delta_total2}")
print(f"  Difference:                {delta_total2 - (Fraction(p,2) + Fraction(n**2, p*X))}")
print(f"                           = {float(delta_total2 - (Fraction(p,2) + Fraction(n**2, p*X))):.15f}")

# So the 3rd term n²/(Φ₃pX) is the new part
# And n/(p²(p-1)) might equal n²/(pX) or not
diff_terms = Fraction(n, p**2*(p-1)) - Fraction(n**2, p*X)
print(f"\n  n/(p²(p-1)) - n²/(pX) = {diff_terms} = {float(diff_terms):.15f}")
# They ARE the same! So the "3-term" is really: p/2 + n²/(pX) + n²/(Φ₃pX)
# Let me re-examine
if diff_terms == 0:
    print(f"  → SAME TERM! So the formula is really: M + p/2 + n²/(pX) + n²/(Φ₃·p·X)")
    print(f"     = M + p/2 + n²/(pX)·(1 + 1/Φ₃)")
    print(f"     = M + p/2 + n²/(pX)·(Φ₃+1)/Φ₃")
    print(f"     = M + p/2 + n²·(Φ₃+1)/(pX·Φ₃)")

    combined = Fraction(n**2, p*X) + Fraction(n**2, Phi3*p*X)
    print(f"\n     n²/(pX) + n²/(Φ₃pX) = {combined} = {float(combined):.12f}")
    print(f"     = n²(Φ₃+1)/(pXΦ₃) = {n**2}·{Phi3+1}/({p}·{X}·{Phi3})")
    print(f"     = {n**2*(Phi3+1)}/{p*X*Phi3}")
    print(f"     = {Fraction(n**2*(Phi3+1), p*X*Phi3)}")

    # What is Phi3+1 = p²+p+2?
    print(f"\n     Φ₃ + 1 = {Phi3+1} = p² + p + 2 = {p**2} + {p} + 2")
    # Factor 32 = 2^5
    print(f"     32 = 2⁵")
    print(f"     So combined = 9·32/(5·60·31) = 288/9300 = {Fraction(288,9300)}")

# ═══════════════════════════════════════════════════════════════════
# HIT 3: MUON MASS
# m_μ/m_e = p(p³-1)/n + 1/(p(p³-1)) + p/(2Γ)
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("HIT 3: MUON MASS CORRECTION")
print("─" * 90)

mu_base = Fraction(p * (p**3 - 1), n)              # 620/3
mu_corr1 = Fraction(1, p * (p**3 - 1))             # 1/620
mu_corr2 = Fraction(p, 2 * G)                      # 5/50 = 1/10

mu_total = mu_base + mu_corr1 + mu_corr2

print(f"\n  m_μ/m_e = p(p³-1)/n + 1/(p(p³-1)) + p/(2Γ)")
print(f"\n  Term-by-term:")
print(f"    p(p³-1)/n      = {mu_base} = {float(mu_base):.12f}")
print(f"    1/(p(p³-1))    = {mu_corr1} = {float(mu_corr1):.12f}")
print(f"    p/(2Γ)         = {mu_corr2} = {float(mu_corr2):.12f}")
print(f"\n  Total: {mu_total}")
print(f"       = {float(mu_total):.15f}")
print(f"\n  Experimental: {mu_exp:.15f}")
print(f"  Error: {abs(float(mu_total) - mu_exp) / mu_exp * 1e6:.2f} ppm")
print(f"  Error: {abs(float(mu_total) - mu_exp) / mu_exp * 1e9:.1f} ppb")
print(f"\n  Numerator:   {mu_total.numerator}")
print(f"  Denominator: {show_rasp_factorization(mu_total.denominator)}")

# Simplify
print(f"\n  Simplification:")
print(f"    p(p³-1)/n = {p}·{p**3-1}/{n} = {p*(p**3-1)}/{n}")
print(f"    1/(p(p³-1)) = 1/({p}·{p**3-1}) = 1/{p*(p**3-1)}")
print(f"    p/(2Γ) = {p}/(2·{G}) = {p}/{2*G} = {Fraction(p, 2*G)}")
print(f"\n    Note: p(p³-1) = {p*(p**3-1)} = 4p·Φ₃ = 4·{p}·{Phi3} = {4*p*Phi3}")
print(f"    So: 1/(p(p³-1)) = 1/(4pΦ₃)")
print(f"    And: p/(2Γ) = p/(2p²) = 1/(2p) = {Fraction(1, 2*p)}")
print(f"\n    REWRITTEN: m_μ/m_e = 4pΦ₃/n + 1/(4pΦ₃) + 1/(2p)")

# Common denominator
# LCD of 3, 620, 10
print(f"\n    Common denominator: {mu_total.denominator}")
print(f"    m_μ/m_e = {mu_total.numerator}/{mu_total.denominator}")

# Compare structures
print(f"\n  STRUCTURAL COMPARISON:")
print(f"    m_p/m_e: X²/2 + (n/p)X + n²/X + λ/n")
print(f"           = {float(Fraction(X**2,2)):.4f} + {float(Fraction(n,p)*X):.4f} + {float(Fraction(n**2,X)):.6f} + {float(L/n):.8f}")
print(f"    1/α:     p³ + n(p-1) + n²/(2p³)")
print(f"           = {p**3:.4f} + {n*(p-1):.4f} + {float(Fraction(n**2, 2*p**3)):.6f}")
print(f"    m_n/m_e: M + p/2 + n²/(pX) + n²/(Φ₃pX)   [3.2 ppb version]")
print(f"           = {float(M):.4f} + {float(Fraction(p,2)):.4f} + {float(Fraction(n**2,p*X)):.6f} + {float(Fraction(n**2,Phi3*p*X)):.8f}")
print(f"    m_μ/m_e: 4pΦ₃/n + 1/(4pΦ₃) + 1/(2p)")
print(f"           = {float(mu_base):.4f} + {float(mu_corr1):.6f} + {float(mu_corr2):.6f}")


# ═══════════════════════════════════════════════════════════════════
# HIT 4: ANOTHER MUON CORRECTION (from Phase 2)
# m_e/m_μ ≈ (p-1)/(Φ₃·p²) - λ²·p  at 46 ppm
# ═══════════════════════════════════════════════════════════════════

print("\n" + "─" * 90)
print("HIT 4: m_e/m_μ CANDIDATE")
print("─" * 90)

me_mu_1 = Fraction(p-1, Phi3 * p**2) - L**2 * p

print(f"\n  m_e/m_μ = (p-1)/(Φ₃·p²) - λ²·p")
print(f"    (p-1)/(Φ₃·p²)  = {Fraction(p-1, Phi3*p**2)} = {float(Fraction(p-1, Phi3*p**2)):.12f}")
print(f"    λ²·p            = {L**2*p} = {float(L**2*p):.12f}")
print(f"    Difference       = {me_mu_1} = {float(me_mu_1):.12f}")
print(f"    Experimental:    0.00483633169")
print(f"    Error: {abs(float(me_mu_1) - 0.00483633169)/0.00483633169*1e6:.1f} ppm")
print(f"    Inverted: m_μ/m_e = {float(1/float(me_mu_1)):.6f}")
print(f"    Inverted error: {abs(1/float(me_mu_1) - 206.7682827)/206.7682827*1e6:.1f} ppm")


# ═══════════════════════════════════════════════════════════════════
# GRAND COMPARISON TABLE
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("GRAND COMPARISON — ALL CANDIDATES")
print("=" * 90)

results = [
    ("m_p/m_e", "X²/2 + (n/p)X + n²/X + λ/n", M, mp_exp, "Tier 1"),
    ("1/α", "p³ + n(p-1) + n²/(2p³)", inv_alpha, 137.035999177, "Tier 2"),
    ("m_n/m_e (v1)", "M + p/2 + n²/(pX) + np/(p³-1)²", M + delta_total, mn_exp, "Tier 3"),
    ("m_n/m_e (v2)", "M + p/2 + n²/(pX) + n²/(Φ₃pX)", M + delta_total2, mn_exp, "Tier 3"),
    ("m_μ/m_e", "4pΦ₃/n + 1/(4pΦ₃) + 1/(2p)", mu_total, mu_exp, "Tier 3"),
]

print(f"\n  {'Constant':>18s}  {'Predicted':>16s}  {'Experimental':>16s}  {'Error':>10s}  {'Tier':>8s}")
print("  " + "─" * 75)
for name, formula, pred, exp_val, tier in results:
    fval = float(pred)
    if abs(exp_val) > 100:
        err_str = f"{abs(fval-exp_val)/exp_val*1e9:.1f} ppb"
    else:
        err_str = f"{abs(fval-exp_val)/exp_val*1e6:.1f} ppm"
    print(f"  {name:>18s}  {fval:16.10f}  {exp_val:16.10f}  {err_str:>10s}  {tier:>8s}")

print(f"\n  Formulas:")
for name, formula, pred, exp_val, tier in results:
    print(f"    {name}: {formula} = {pred}")
