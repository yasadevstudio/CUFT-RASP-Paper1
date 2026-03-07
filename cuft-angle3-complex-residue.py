#!/usr/bin/env python3
"""
CUFT-RASP ANGLE 3: COMPLEX RESIDUE / CONTOUR INTEGRAL APPROACH
===============================================================
YASA PRESENTS — 2026-02-24

GOAL: Use contour integration around the fixed points to extract
      topological invariants that constrain c1 = n/p.

APPROACH:
  The recursion f(x) = Gamma*tanh^n(x) - lambda*x has fixed points
  where f(x*) = x* (i.e., g(x) = f(x) - x = 0).

  The contour integral:
    I = (1/2pi*i) oint x*g'(x)/g(x) dx
  around a fixed point x* gives the RESIDUE, which encodes:
    - The multiplicity of the root
    - The local behavior of the map near x*

  For a SIMPLE zero at x*: Res = x* (the fixed point value itself)
  For a zero of multiplicity m: more complex expression

  Strategy:
  1. Compute the residues at x_u and x_s analytically
  2. Check if the SUM or DIFFERENCE of residues relates to M or c1
  3. Look for topological invariants (winding numbers, indices)
  4. Explore the complex extension of tanh^n
  5. Check if Cauchy's argument principle gives integer constraints
"""

import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from fractions import Fraction

# ===================================================================
# PARAMETERS
# ===================================================================

n = 3
p = 5
GAMMA = p**2
LAMBDA = 1/(p**3 - 1)
kappa = 1/p
X = n * p * (p - 1)
M_target = float(Fraction(853811, 465))

def g(x, G=GAMMA, lam=LAMBDA, nq=n):
    """g(x) = f(x) - x = Gamma*tanh^n(x) - (1+lambda)*x"""
    return G * np.tanh(x)**nq - (1 + lam) * x

def g_prime(x, G=GAMMA, lam=LAMBDA, nq=n):
    """g'(x) = f'(x) - 1"""
    t = np.tanh(x)
    return nq * G * t**(nq-1) * (1 - t**2) - (1 + lam)

def f_map(x, G=GAMMA, lam=LAMBDA, nq=n):
    return G * np.tanh(x)**nq - lam * x

def f_prime(x, G=GAMMA, lam=LAMBDA, nq=n):
    t = np.tanh(x)
    return nq * G * t**(nq-1) * (1 - t**2) - lam

x_u = brentq(g, 0.01, 1.0)
x_s = brentq(g, 10.0, 30.0)

print("=" * 72)
print("ANGLE 3: COMPLEX RESIDUE / CONTOUR INTEGRAL APPROACH")
print("=" * 72)
print(f"\nFixed points: x_u = {x_u:.10f}, x_s = {x_s:.10f}")

# ===================================================================
# SECTION 1: FIXED-POINT INDEX (TOPOLOGICAL INVARIANT)
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 1: FIXED-POINT INDEX")
print("=" * 72)

# The fixed-point index of a 1D map f at x* is:
#   ind(x*) = sgn(1 - f'(x*))
# For an attracting point (|f'| < 1): ind = +1
# For a repelling point (f' > 1): ind = -1
# For a repelling point (f' < -1): ind = -1
# At x=0: f'(0) = -lambda < 0, |f'| < 1 -> ind = +1
# At x_u: f'(x_u) > 1 (unstable from above) -> ind = -1
# At x_s: f'(x_s) near 0 (strongly attracting) -> ind = +1

fp_0 = f_prime(0)
fp_u = f_prime(x_u)
fp_s = f_prime(x_s)

ind_0 = np.sign(1 - fp_0)
ind_u = np.sign(1 - fp_u)
ind_s = np.sign(1 - fp_s)

print(f"\nFixed-point indices (Lefschetz):")
print(f"  x=0:  f'(0)={fp_0:.6f},   1-f'={1-fp_0:.6f},   ind={int(ind_0)}")
print(f"  x_u:  f'(x_u)={fp_u:.6f}, 1-f'={1-fp_u:.6f},  ind={int(ind_u)}")
print(f"  x_s:  f'(x_s)={fp_s:.10f},  1-f'={1-fp_s:.10f}, ind={int(ind_s)}")
print(f"\n  Sum of indices: {int(ind_0 + ind_u + ind_s)}")
print(f"  (Lefschetz: sum = L(f) for compact manifold)")

# For maps on R+, the Lefschetz number isn't directly applicable,
# but the ALTERNATING sum of indices at fixed points relates to
# the topology of the phase space.

# ===================================================================
# SECTION 2: RESIDUE OF x*g'(x)/g(x) AT SIMPLE ZEROS
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 2: RESIDUE CALCULATIONS")
print("=" * 72)

# For g(x) with simple zero at x*:
# g(x) = g'(x*)*(x-x*) + O((x-x*)^2)
# x*g'(x)/g(x) near x*:
#   x*g'(x*) / [g'(x*)*(x-x*)] + regular = x* / (x-x*) + regular
# So Res_{x*}[x*g'(x)/g(x)] = x* (the fixed point value)

# More useful: Res_{x*}[g'(x)/g(x)] = 1 (always, for simple zero)
# This is just the argument principle.

gp_at_0 = g_prime(0)
gp_at_u = g_prime(x_u)
gp_at_s = g_prime(x_s)

print(f"\ng'(x) = f'(x) - 1 at fixed points:")
print(f"  g'(0)   = {gp_at_0:.10f}")
print(f"  g'(x_u) = {gp_at_u:.10f}")
print(f"  g'(x_s) = {gp_at_s:.10f}")

print(f"\nResidues of x*g'/g at fixed points (simple zeros):")
print(f"  Res(0)   = 0 (trivial)")
print(f"  Res(x_u) = x_u = {x_u:.10f}")
print(f"  Res(x_s) = x_s = {x_s:.10f}")
print(f"  Sum = x_u + x_s = {x_u + x_s:.10f}")

# ===================================================================
# SECTION 3: CAUCHY ARGUMENT PRINCIPLE
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 3: CAUCHY ARGUMENT PRINCIPLE — WINDING NUMBERS")
print("=" * 72)

# The number of zeros of g(x) = f(x)-x inside a contour C:
#   N = (1/2pi*i) oint g'(z)/g(z) dz
#
# For a contour enclosing x_u and x_s (but not 0):
#   N = 2 (two simple zeros)
#
# For a contour enclosing only x_u: N = 1
# For a contour enclosing only x_s: N = 1
#
# These are topological invariants — they give INTEGER values.
# But they don't constrain c1 because they count roots, not
# describe the map's structure.

# More interesting: the integral of specific functions along contours.
# What about:
#   I_k = (1/2pi*i) oint x^k * g'(x)/g(x) dx
# For k=0: I_0 = N (number of zeros)
# For k=1: I_1 = sum of zeros
# For k=2: I_2 = sum of squares of zeros

print(f"\nGeneralized contour integrals (argument principle):")
print(f"  I_0 = N (zeros) = 3 (including x=0)")
print(f"  I_1 = sum of zeros = 0 + x_u + x_s = {x_u + x_s:.10f}")
print(f"  I_2 = sum of squares = x_u^2 + x_s^2 = {x_u**2 + x_s**2:.10f}")
print(f"  I_3 = sum of cubes = {x_u**3 + x_s**3:.10f}")

# Check if any combination gives M
print(f"\n  M = {M_target:.10f}")
print(f"  x_s^2/2 = {x_s**2/2:.10f}")
print(f"  M - x_s^2/2 = {M_target - x_s**2/2:.10f}")
print(f"  X^2/2 = {X**2/2}")
print(f"  (x_u+x_s)^2/2 = {(x_u+x_s)**2/2:.10f}")

# ===================================================================
# SECTION 4: STABILITY MULTIPLIERS AND TOPOLOGICAL PRESSURE
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 4: STABILITY MULTIPLIERS AND TOPOLOGICAL PRESSURE")
print("=" * 72)

# The stability multiplier at x*: sigma = f'(x*)
# For the map f, the "topological pressure" at fixed points:
#   P = -sum_i ln|f'(x_i)| / (period)
# For period-1 fixed points (period = 1):

sigma_0 = abs(fp_0)
sigma_u = abs(fp_u)
sigma_s = abs(fp_s)

print(f"\nStability multipliers |f'(x*)|:")
print(f"  |f'(0)|   = {sigma_0:.10f}")
print(f"  |f'(x_u)| = {sigma_u:.10f}")
print(f"  |f'(x_s)| = {sigma_s:.15e}")

ln_sigma_0 = np.log(sigma_0)
ln_sigma_u = np.log(sigma_u)
# f'(x_s) is very close to -lambda, use exact value
ln_sigma_s = np.log(abs(fp_s))

print(f"\nLog multipliers ln|f'(x*)|:")
print(f"  ln|f'(0)|   = {ln_sigma_0:.10f}")
print(f"  ln|f'(x_u)| = {ln_sigma_u:.10f}")
print(f"  ln|f'(x_s)| = {ln_sigma_s:.10f}")

# The Lyapunov exponent at the stable FP is essentially ln(lambda)
print(f"\n  ln(lambda) = ln(1/{p**3-1}) = {np.log(LAMBDA):.10f}")
print(f"  ln|f'(x_s)| = {ln_sigma_s:.10f}")
print(f"  Ratio: {ln_sigma_s / np.log(LAMBDA):.10f}")

# Topological entropy / pressure combinations
print(f"\n  x_u * ln|f'(x_u)| = {x_u * ln_sigma_u:.10f}")
print(f"  x_s * ln|f'(x_s)| = {x_s * ln_sigma_s:.10f}")
print(f"  Sum = {x_u * ln_sigma_u + x_s * ln_sigma_s:.10f}")

# ===================================================================
# SECTION 5: THE HOLOMORPHIC INDEX
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 5: HOLOMORPHIC INDEX AT FIXED POINTS")
print("=" * 72)

# For a holomorphic map f with fixed point x*:
# The holomorphic index is:
#   iota(x*) = 1/(1 - f'(x*))
# (related to the Lefschetz index for analytic maps)

iota_0 = 1 / (1 - fp_0)
iota_u = 1 / (1 - fp_u)
iota_s = 1 / (1 - fp_s)

print(f"\nHolomorphic indices iota = 1/(1-f'(x*)):")
print(f"  iota(0)   = 1/(1-({fp_0:.6f}))   = {iota_0:.10f}")
print(f"  iota(x_u) = 1/(1-({fp_u:.6f})) = {iota_u:.10f}")
print(f"  iota(x_s) = 1/(1-({fp_s:.10f}))  = {iota_s:.10f}")
print(f"\n  Sum = {iota_0 + iota_u + iota_s:.10f}")

# For maps on the Riemann sphere, sum of holomorphic indices = 1
# For maps on R, this doesn't hold, but let's check:
print(f"  Sum of indices (should = 1 on Riemann sphere): {iota_0 + iota_u + iota_s:.10f}")

# There's also a fixed point at infinity for the map f(x) = Gamma*tanh^n(x) - lambda*x
# At x -> inf: f(x) -> Gamma - lambda*x -> -infinity (if lambda > 0)
# So f'(inf) = -lambda, iota(inf) = 1/(1+lambda) = (p^3-1)/p^3
iota_inf = 1 / (1 + LAMBDA)
print(f"\n  iota(inf) = 1/(1+lambda) = {iota_inf:.10f}")
print(f"  Sum with inf: {iota_0 + iota_u + iota_s + iota_inf:.10f}")

# Interesting: iota_0 + iota_inf should = iota_u + ...
# Actually for a polynomial-like map of degree d on Riemann sphere,
# sum of all indices = 1.

# ===================================================================
# SECTION 6: NUMERICAL CONTOUR INTEGRATION
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 6: NUMERICAL CONTOUR INTEGRATION")
print("=" * 72)

# Compute contour integrals numerically along small circles
# in the COMPLEX plane around each fixed point.

# g(z) = Gamma*tanh^n(z) - (1+lambda)*z extended to complex z
def g_complex(z):
    return GAMMA * np.tanh(z)**n - (1 + LAMBDA) * z

def g_prime_complex(z):
    t = np.tanh(z)
    return n * GAMMA * t**(n-1) * (1 - t**2) - (1 + LAMBDA)

# Contour around x_u: z = x_u + r*exp(i*theta)
r_u = 0.05  # small radius
def integrand_u(theta, k=0):
    z = x_u + r_u * np.exp(1j * theta)
    gp = g_prime_complex(z)
    gv = g_complex(z)
    dz = 1j * r_u * np.exp(1j * theta)
    return (z**k * gp / gv * dz).real, (z**k * gp / gv * dz).imag

# I_k = (1/2pi*i) oint z^k * g'/g dz
# = (1/2pi) int_0^{2pi} z^k * g'(z)/g(z) * r*exp(i*theta) dtheta (the i cancels)

for k in range(4):
    real_part, _ = quad(lambda t: integrand_u(t, k)[1], 0, 2*np.pi)
    imag_part, _ = quad(lambda t: integrand_u(t, k)[0], 0, 2*np.pi)
    # The contour integral (1/2pi*i) gives real_part/2pi for the residue
    residue = real_part / (2 * np.pi)
    print(f"  I_{k}(x_u) = {residue:.10f} (expected: x_u^{k} = {x_u**k:.10f})")

# Contour around x_s: z = x_s + r*exp(i*theta)
r_s = 0.05
def integrand_s(theta, k=0):
    z = x_s + r_s * np.exp(1j * theta)
    gp = g_prime_complex(z)
    gv = g_complex(z)
    dz = 1j * r_s * np.exp(1j * theta)
    return (z**k * gp / gv * dz).real, (z**k * gp / gv * dz).imag

print()
for k in range(4):
    real_part, _ = quad(lambda t: integrand_s(t, k)[1], 0, 2*np.pi)
    residue = real_part / (2 * np.pi)
    print(f"  I_{k}(x_s) = {residue:.10f} (expected: x_s^{k} = {x_s**k:.10f})")

# ===================================================================
# SECTION 7: CROSS-POINT CONTOUR — ENCLOSING BOTH x_u AND x_s
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 7: LARGE CONTOUR ENCLOSING BOTH FIXED POINTS")
print("=" * 72)

# Large contour: z = (x_u+x_s)/2 + R*exp(i*theta)
# with R large enough to enclose both x_u and x_s
center = (x_u + x_s) / 2
R = (x_s - x_u) / 2 + 1.0  # encloses both with margin

def integrand_large(theta, k=0):
    z = center + R * np.exp(1j * theta)
    gp = g_prime_complex(z)
    gv = g_complex(z)
    dz = 1j * R * np.exp(1j * theta)
    return (z**k * gp / gv * dz).real, (z**k * gp / gv * dz).imag

print(f"\nLarge contour center={center:.4f}, R={R:.4f}")
print(f"Enclosing x_u={x_u:.4f} and x_s={x_s:.4f}")

for k in range(5):
    real_part, _ = quad(lambda t: integrand_large(t, k)[1], 0, 2*np.pi,
                        limit=200)
    residue = real_part / (2 * np.pi)
    expected = x_u**k + x_s**k
    print(f"  I_{k}(both) = {residue:.10f} (expected x_u^{k}+x_s^{k} = {expected:.10f})")

# ===================================================================
# SECTION 8: CAN CONTOUR INTEGRALS GIVE c1?
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 8: ATTEMPTING TO EXTRACT c1 FROM CONTOUR INTEGRALS")
print("=" * 72)

# The residues at x_u and x_s are just x_u^k and x_s^k.
# These are the NEWTON POWER SUMS of the roots of g(x) = 0.
#
# By Newton's identities, these relate to the COEFFICIENTS
# of the polynomial whose roots are x_u and x_s.
#
# But g(x) = Gamma*tanh^n(x) - (1+lambda)*x is NOT a polynomial!
# It has infinitely many complex zeros (tanh has poles at i*pi/2 + n*i*pi).
#
# So the "polynomial whose roots are x_u and x_s" is a FACTOR of g,
# not g itself. And extracting this factor is equivalent to
# already knowing x_u and x_s.

# However, we can ask: what polynomial P(x) has roots at x_u and x_s?
# P(x) = (x - x_u)(x - x_s) = x^2 - (x_u+x_s)x + x_u*x_s

e1 = x_u + x_s   # elementary symmetric polynomial
e2 = x_u * x_s   # product of roots

print(f"\nElementary symmetric polynomials of fixed points:")
print(f"  e1 = x_u + x_s = {e1:.10f}")
print(f"  e2 = x_u * x_s = {e2:.10f}")

# Express in terms of (n, p):
# x_u is transcendental (defined by the fixed-point equation)
# x_s approx p^2 - 1/p
# So e1 approx x_u + p^2 - 1/p
# And e2 approx x_u * (p^2 - 1/p)

print(f"\n  x_u ≈ {x_u:.10f} (no closed form)")
print(f"  x_s ≈ p^2 - 1/p = {p**2 - 1/p:.10f}")
print(f"  e1 ≈ x_u + p^2 - 1/p = {x_u + p**2 - 1/p:.10f}")

# The problem: x_u has no closed-form expression in terms of (n, p).
# It's defined implicitly by Gamma*tanh^n(x_u) = (1+lambda)*x_u.
# For small x_u: tanh(x) approx x - x^3/3
# So Gamma*(x_u - x_u^3/3)^n approx (1+lambda)*x_u
# Gamma*x_u^n*(1 - x_u^2/3)^n approx (1+lambda)*x_u
# For n=3: Gamma*x_u^3*(1-x_u^2)^3 approx (1+lambda)*x_u (rough)
# Better: Gamma*x_u^2*(1-x_u^2/3)^3 approx (1+lambda) (divide by x_u)

print(f"\nApproximation for x_u (small x_u limit):")
print(f"  Gamma*tanh^n(x_u) = (1+lambda)*x_u")
print(f"  For small x: tanh(x) ~ x - x^3/3")
print(f"  tanh^3(x) ~ x^3(1 - x^2)^3 ~ x^3 - 3x^5 + ...")
print(f"  So: Gamma*x_u^2*(1-x_u^2)^3 ~ (1+lambda)")

# Better: tanh(x) ~ x - x^3/3, so tanh^3(x) ~ x^3 - x^5 + ...
# Gamma*x_u^3*(1 - x_u^2)^3 ~ (1+lambda)*x_u (nope, tanh^3 != (x-x^3/3)^3)
# Actually tanh^3(x) = [tanh(x)]^3, and tanh(x) = x - x^3/3 + 2x^5/15 - ...
# [x - x^3/3 + ...]^3 = x^3 - x^5 + ... (keeping leading terms)

# Let's use the exact small-x expansion:
# Gamma*(x^3 - x^5 + ...) = (1+lambda)*x
# Gamma*x^2*(1 - x^2 + ...) = (1+lambda)
# x^2 ~ (1+lambda)/Gamma
# x_u ~ sqrt((1+lambda)/Gamma) = sqrt(p^3/(p^3-1)/p^2) = sqrt(p/(p^3-1))
x_u_approx = np.sqrt(p / (p**3 - 1))
print(f"\n  x_u ~ sqrt(p/(p^3-1)) = {x_u_approx:.10f}")
print(f"  Actual x_u = {x_u:.10f}")
print(f"  Relative error: {abs(x_u - x_u_approx)/x_u * 100:.2f}%")

# Better approximation including next term:
# Gamma*x^2*(1 - x^2 + ...) = (1+lambda)
# Let alpha = (1+lambda)/Gamma = p^3/((p^3-1)*p^2) = p/(p^3-1)
alpha_param = (1 + LAMBDA) / GAMMA
print(f"\n  alpha = (1+lambda)/Gamma = {alpha_param:.10f}")
print(f"  sqrt(alpha) = {np.sqrt(alpha_param):.10f}")

# x^2(1 - x^2) = alpha  =>  x^4 - x^2 + alpha = 0
# x^2 = (1 - sqrt(1 - 4*alpha)) / 2  (smaller root)
disc = 1 - 4*alpha_param
x_u_better = np.sqrt((1 - np.sqrt(disc)) / 2)
print(f"  Better: x_u ~ sqrt((1-sqrt(1-4alpha))/2) = {x_u_better:.10f}")
print(f"  Actual: {x_u:.10f}")
print(f"  Error: {abs(x_u - x_u_better)/x_u * 100:.4f}%")

# ===================================================================
# SECTION 9: THE VIRIAL CROSS-RATIO
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 9: VIRIAL CROSS-RATIO")
print("=" * 72)

# Define the virial V(x*) = x* * f'(x*) at each fixed point
V_0 = 0 * fp_0  # = 0
V_u = x_u * fp_u
V_s = x_s * fp_s

print(f"\nVirial products x*f'(x*):")
print(f"  V(0)   = {V_0:.10f}")
print(f"  V(x_u) = {V_u:.10f}")
print(f"  V(x_s) = {V_s:.10f}")

# We know V(x_s) = -1/p = -kappa (exact)
# We know V(x_u) ~ n/p + O(lambda) (approximate)
print(f"\n  V(x_s) = -1/p? {abs(V_s + 1/p):.2e}")
print(f"  V(x_u) = n/p? {abs(V_u - n/p):.6f} (off by {abs(V_u - n/p)/V_u*100:.4f}%)")

# Cross-ratio of virials:
cross = V_u / V_s
print(f"\n  V(x_u)/V(x_s) = {cross:.10f}")
print(f"  Expected -n = {-n}")
print(f"  Error: {abs(cross + n):.6f}")

# The cross-ratio is NOT exactly -n.
# But if it WERE, we'd have:
# V(x_u) = -n * V(x_s) = -n * (-1/p) = n/p = c1
# This would be a topological constraint!

# Let's check for other (n,p):
print(f"\nCross-ratio V(x_u)/V(x_s) for all Diophantine solutions:")
solutions = [(3, 5), (4, 3), (6, 2)]
for nn, pp in solutions:
    GG = pp**2
    LL = 1/(pp**3 - 1)

    def g_sol(x, G=GG, lam=LL, nq=nn):
        return G * np.tanh(x)**nq - (1 + lam) * x
    def fp_sol(x, G=GG, lam=LL, nq=nn):
        t = np.tanh(x)
        return nq * G * t**(nq-1) * (1 - t**2) - lam

    xu = brentq(g_sol, 0.01, 2.0)
    try:
        xs = brentq(g_sol, GG*0.5, GG*1.2)
    except:
        xs = brentq(g_sol, 1.0, GG*1.2)

    Vu = xu * fp_sol(xu)
    Vs = xs * fp_sol(xs)
    cr = Vu / Vs if abs(Vs) > 1e-15 else float('nan')

    print(f"  ({nn},{pp}): V_u={Vu:.6f}, V_s={Vs:.6f}, ratio={cr:.6f}, -n={-nn}, error={abs(cr+nn):.4f}")

# ===================================================================
# SECTION 10: WEIGHTED RESIDUE — VIRIAL AS WEIGHT
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 10: VIRIAL-WEIGHTED CONTOUR INTEGRALS")
print("=" * 72)

# What if we use f'(x) as a weight?
# I = oint f'(z) * z^k * g'(z)/g(z) dz / (2pi*i)
# Res at x* = x*^k * f'(x*)  (since g has simple zero)

# For k=1: Res = x* * f'(x*) = the virial product
# Sum = V(x_u) + V(x_s) = V_u + V_s

print(f"\nVirial-weighted residues:")
print(f"  Sum V(x_u) + V(x_s) = {V_u + V_s:.10f}")
print(f"  Difference V(x_u) - V(x_s) = {V_u - V_s:.10f}")
print(f"  n/p - (-1/p) = (n+1)/p = {(n+1)/p:.10f}")
print(f"  Actual diff: {V_u - V_s:.10f}")
print(f"  Match V_u-V_s = (n+1)/p? error: {abs(V_u - V_s - (n+1)/p):.6f}")

# The difference V_u - V_s is approximately (n+1)/p but not exactly.
# This is because V_u = n/p + O(lambda), while V_s = -1/p exactly.

# Exact: V_u - V_s = V_u + 1/p
# If V_u were exactly n/p, then V_u - V_s = (n+1)/p.
# The error is the same O(lambda) correction in V_u.

correction = V_u - n/p
print(f"\n  O(lambda) correction to V_u: {correction:.10f}")
print(f"  lambda = {LAMBDA:.10f}")
print(f"  Correction/lambda = {correction/LAMBDA:.10f}")

# ===================================================================
# SECTION 11: COMPLEX POLES OF tanh^n
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 11: COMPLEX STRUCTURE OF tanh^n(z)")
print("=" * 72)

# tanh(z) has poles at z = i*pi/2 + k*i*pi for integer k
# tanh^n(z) has poles of order n at the same locations
#
# g(z) = Gamma*tanh^n(z) - (1+lambda)*z
# g has: poles at z = i*pi*(k+1/2) for all integers k
#        zeros at z = 0, x_u, x_s (real) plus complex zeros
#
# The TOTAL number of zeros minus poles in any region is given
# by the argument principle.

print(f"""
Complex structure of g(z) = Gamma*tanh^n(z) - (1+lambda)*z:

POLES of tanh(z): z_k = i*pi*(k + 1/2) for k in Z
  → tanh^n has poles of order n at each z_k
  → g(z) has poles of order n (Gamma*tanh^n dominates near poles)

REAL ZEROS: z = 0, x_u = {x_u:.6f}, x_s = {x_s:.6f}

For a contour enclosing the real interval [0, x_s] and staying
below the first pole at z = i*pi/2 (y < pi/2 ≈ {np.pi/2:.4f}):
  # zeros - # poles = winding number of g along contour
  # real zeros inside = 3 (counting 0)
  # poles inside = 0 (first pole at i*pi/2 is outside if contour < pi/2)
  → winding number = 3 = n+1? No, this is n (quarks) + 1 (trivial).
""")

# Actually the number of real zeros is related to n:
# For the recursion f(x) = Gamma*tanh^n(x) - lambda*x:
# - Always has x=0 as fixed point
# - For Gamma > threshold: has 2 additional fixed points (x_u, x_s)
# - Total real fixed points: 3
# - This is n = 3 quarks... but for (4,3) or (6,2) it's still 3 real FPs

# ===================================================================
# SECTION 12: THE INDEX THEOREM ANGLE
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 12: INDEX THEOREM — TOPOLOGICAL CONSTRAINTS ON c1")
print("=" * 72)

# The Atiyah-Singer index theorem relates:
# analytical index (solution count) = topological index (curvature integral)
#
# For our 1D map, the relevant theorem is much simpler.
# The Lefschetz fixed-point theorem says:
#   L(f) = sum_{f(x)=x} ind(x, f)
#
# For f: R -> R (not compact), this doesn't directly apply.
# But for the compactified map f: S^1 -> S^1 (identifying +inf and -inf):
#   L(f) = 1 - deg(f)
# where deg(f) is the degree of the map.
#
# Our f(x) = Gamma*tanh^n(x) - lambda*x:
# As x -> +inf: f(x) -> Gamma - lambda*x -> -inf (degree = -1 for the linear term)
# As x -> -inf: f(x) -> -Gamma - lambda*x -> +inf
# So f maps R monotonically (for large |x|) with slope -lambda.
# The degree on the circle would be -1 (reverses orientation at infinity).
# L(f) = 1 - (-1) = 2
# Sum of indices: ind(0) + ind(x_u) + ind(x_s) = 1 + (-1) + 1 = 1
# Plus ind(inf) = ... hmm.

print(f"""
Lefschetz analysis:
  ind(0)   = +1 (attracting, |f'| < 1)
  ind(x_u) = -1 (repelling, f' > 1)
  ind(x_s) = +1 (attracting, |f'| < 1)
  Sum of finite indices = {int(ind_0 + ind_u + ind_s)}

  This sum is +1, which equals the Euler characteristic of [0, inf)
  with the appropriate boundary conditions. This is a TOPOLOGICAL
  CONSTRAINT but it only tells us about the NUMBER and TYPE of
  fixed points, not about the mass formula.
""")

# ===================================================================
# SECTION 13: SPECTRAL ZETA FUNCTION
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 13: SPECTRAL ZETA FUNCTION APPROACH")
print("=" * 72)

# The spectral zeta function of the map:
# zeta_f(s) = sum_{f^k(x)=x} 1/|det(I - Df^k)|^s
# For period-1 fixed points:
# zeta_f(s) ~ 1/|1-f'(0)|^s + 1/|1-f'(x_u)|^s + 1/|1-f'(x_s)|^s

# The Ruelle zeta function:
# zeta_R(z) = exp(sum_{k=1}^inf z^k/k * sum_{f^k(x)=x} 1/|det(I-Df^k)|)

# For our purposes, the useful object is:
# Z(s) = sum_i x_i^s / |1 - f'(x_i)| where sum is over fixed points

for s_val in [0, 0.5, 1, 2, 3]:
    Z_s = (x_u**s_val / abs(1 - fp_u) + x_s**s_val / abs(1 - fp_s))
    print(f"  Z(s={s_val:.1f}) = {Z_s:.10f}, M/Z = {M_target/Z_s:.10f}")

# ===================================================================
# SECTION 14: THE SCHWINGER FUNCTION APPROACH
# ===================================================================

print("\n" + "=" * 72)
print("SECTION 14: PROPAGATOR / GREEN'S FUNCTION")
print("=" * 72)

# The Green's function of the linearized map at x_s:
# G_s(omega) = 1 / (1 - f'(x_s) * e^{i*omega})
# For |f'(x_s)| << 1, this is approximately 1 for all omega.
# The "propagator" is trivial at the stable fixed point.

# At x_u:
# G_u(omega) = 1 / (1 - f'(x_u) * e^{i*omega})
# f'(x_u) > 1, so this has a singularity at omega = 0.

# The "mass" in field theory is related to the POLE of the propagator:
# G(p) ~ 1/(p^2 + m^2)
# A pole at p=0 means m=0 (massless). No pole means massive.

# The analogy breaks down because our "propagator" is 1D and discrete.

# Let's try a different approach: the transfer matrix.
# For the recursion x_{t+1} = f(x_t), the transfer matrix near x_s is:
# T = f'(x_s) = -lambda (approximately)
# The "partition function" over N steps:
# Z_N = Tr(T^N) = f'(x_s)^N -> 0 as N -> inf (contracting)
# The free energy: F_N = -ln(Z_N)/N = -ln|f'(x_s)| ≈ ln(1/lambda)

F_transfer = -np.log(abs(fp_s))
print(f"\nTransfer matrix free energy per step:")
print(f"  F = -ln|f'(x_s)| = {F_transfer:.10f}")
print(f"  = ln(1/lambda) = ln({p**3-1}) = {np.log(p**3-1):.10f}")
print(f"  M / F = {M_target / F_transfer:.10f}")

# ===================================================================
# FINAL ASSESSMENT
# ===================================================================

print("\n" + "=" * 72)
print("ANGLE 3: FINAL ASSESSMENT")
print("=" * 72)

print(f"""
RESULT: CONTOUR INTEGRALS GIVE TOPOLOGICAL INVARIANTS BUT NOT c1.

What we found:
  1. Residues at fixed points = the fixed-point values themselves (trivial)
  2. Fixed-point indices: +1, -1, +1 (topological, counts types not values)
  3. Holomorphic indices: 1/(1-f'(x*)) — partition function weights
  4. Virial cross-ratio V(x_u)/V(x_s) ~ -n (APPROXIMATE, not exact)
  5. The correction is O(lambda), same as the cross-virial from earlier
  6. Complex structure reveals poles at i*pi*(k+1/2) from tanh
  7. Spectral zeta functions don't simplify to M

WHY CONTOUR INTEGRALS DON'T HELP:
  The argument principle gives INTEGER invariants (winding numbers,
  zero counts). These are TOPOLOGICAL — they constrain the EXISTENCE
  of fixed points but not the specific VALUE of the mass formula.

  The mass formula involves METRIC quantities (x_s, x_u, their
  derivatives) which are NOT topological. Contour integrals capture
  topology, not geometry.

  In short: contour integrals tell you HOW MANY fixed points exist
  (3, including 0), and WHAT TYPE they are (2 stable, 1 unstable),
  but not WHAT VALUE the mass formula takes.

THE O(lambda) BARRIER:
  The virial cross-ratio V(x_u)/V(x_s) ≈ -n is the SAME approximate
  result as the cross-fixed-point virial from the earlier analysis.
  It fails to be exact for the same reason: x_u has no closed form,
  and the O(lambda) correction to V(x_u) is non-universal.

  For (3,5): error is 0.2%, looks close but not a theorem.
  For (6,2): error is 14%, clearly not exact.
  For (4,3): error is ~40%, clearly not a general identity.

CONTRIBUTION TO PAPER: None beyond what's already included.
The contour integral approach confirms the cross-virial result
from a different angle but doesn't improve it.

OVERALL CONCLUSION FROM ALL THREE ANGLES:
===========================================
  Angle 1 (Factorization):  STRUCTURAL argument for c1 = n*kappa. ★★★★☆
  Angle 2 (Derive M):       CANNOT derive M from recursion alone.  ★★☆☆☆
  Angle 3 (Complex residue): Topology doesn't constrain c1.        ★★☆☆☆

  c1 = n/p remains PHYSICALLY motivated and Occam-selected.
  It is NOT a theorem. The paper's position is correct and honest.
  The multiple supporting arguments (virial, factorization, cross-virial,
  mean-field, Cornell analogy) make it the UNIQUE natural choice,
  but uniqueness is not derivation.
""")

print("=" * 72)
print("END ANGLE 3 — ALL THREE ANGLES COMPLETE")
print("=" * 72)
