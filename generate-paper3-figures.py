#!/usr/bin/env python3
"""
YASA PRESENTS
generate-paper3-figures.py - Generate all three figures for Paper 3
(RASP-CRYPTOCHROME-TRIAD)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.gridspec import GridSpec
import matplotlib.patheffects as pe

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'text.usetex': False,
})

# ================================================================
# FIGURE 1: The (3,5) structural motif across quantum biology
# ================================================================
def make_figure1():
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(1, 2, width_ratios=[1.6, 1], wspace=0.3)

    # --- Panel (a): Seven systems schematic ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_xlim(-0.5, 3.5)
    ax1.set_ylim(-0.5, 7.8)
    ax1.axis('off')
    ax1.set_title('(a) Seven (n=3) biological systems', fontsize=11, fontweight='bold', loc='left')

    systems = [
        ('CRY/PHL',     'Trp-Trp-Trp',     '3.8/3.9/7.6',   '1',   '3/3', '#2166ac'),
        ('CcP',         'W191/Y71/W51',     '5.1/8.2/10.3',  '1',   '2/3', '#4393c3'),
        ('RNR',         'Y122/W48/Y356',    '3.4/7.6/10.1',  '1',   '1/3', '#92c5de'),
        ('CcO',         'Y244/W236/Y129',   '4.8/8.1/11.2',  '1',   '1/3', '#92c5de'),
        ('Rhodopsin',   'F261/W265/Y268',   '3.8/3.9/6.5',   '1**', '1/3', '#f4a582'),
        ('GPCRs',       'W6.48/F6.44/F5.47','4.1/5.2/7.3',   '1**', '1/3', '#f4a582'),
        ('Tubulin',     'W407/F404/Y408',   '3.8/7.6/5.2',   '1*',  '1/3', '#d6604d'),
    ]

    for i, (name, triad, dists, tier, rasp, color) in enumerate(systems):
        y = 7.0 - i * 1.05
        # System box
        box = FancyBboxPatch((0.0, y-0.35), 0.95, 0.65, boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor='black', alpha=0.7, linewidth=0.8)
        ax1.add_patch(box)
        ax1.text(0.47, y, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white',
                 path_effects=[pe.withStroke(linewidth=1.5, foreground='black')])

        # Triad residues as three circles
        cx = 1.4
        for j, res in enumerate(triad.split('/')):
            xp = cx + j * 0.55
            is_trp = res.startswith('W') or res.startswith('Trp') or res.startswith('3x')
            fc = '#1a9850' if is_trp else '#d9d9d9'
            ec = '#005a32' if is_trp else '#636363'
            circ = Circle((xp, y), 0.18, facecolor=fc, edgecolor=ec, linewidth=1.0, zorder=3)
            ax1.add_patch(circ)
            label = res if len(res) <= 4 else res[:4]
            ax1.text(xp, y, label, ha='center', va='center', fontsize=5.5, fontweight='bold', zorder=4)

        # Tier and RASP fraction
        ax1.text(3.05, y+0.05, f'Tier {tier}', ha='center', va='center', fontsize=7.5)
        ax1.text(3.05, y-0.18, f'RASP: {rasp}', ha='center', va='center', fontsize=6.5, color='#555555')

    # Legend
    legend_y = -0.15
    circ_trp = Circle((0.3, legend_y), 0.12, facecolor='#1a9850', edgecolor='#005a32', linewidth=1.0)
    circ_oth = Circle((1.5, legend_y), 0.12, facecolor='#d9d9d9', edgecolor='#636363', linewidth=1.0)
    ax1.add_patch(circ_trp)
    ax1.add_patch(circ_oth)
    ax1.text(0.5, legend_y, '= Trp (p=5, RASP site)', ha='left', va='center', fontsize=7.5)
    ax1.text(1.7, legend_y, '= Phe/Tyr (p=4)', ha='left', va='center', fontsize=7.5)

    # Category labels on left
    ax1.text(-0.4, 5.35, 'Direct\nquantum', ha='center', va='center', fontsize=7, fontstyle='italic',
             rotation=90, color='#2166ac')
    ax1.text(-0.4, 1.88, 'Structural\nquantum\ncontrol', ha='center', va='center', fontsize=7,
             fontstyle='italic', rotation=90, color='#d6604d')

    # --- Panel (b): Energy level diagram ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(-0.5, 3.5)
    ax2.set_ylim(-0.5, 7.0)
    ax2.set_ylabel('Energy (eV)', fontsize=11)
    ax2.set_title('(b) Electronic states below absorption edge', fontsize=11, fontweight='bold', loc='left')

    # Absorption edge
    ax2.axhline(y=6.0, color='red', linestyle='--', linewidth=1.0, alpha=0.7)
    ax2.text(3.3, 6.1, 'Protein\nabsorption\nedge ~6.0 eV', fontsize=7, ha='right', va='bottom', color='red')

    residues = {
        'Trp (p=5)': {
            'x': 0.5, 'color': '#1a9850',
            'states': [('S0', 0.0), ('T1', 3.0), ('1Lb', 4.3), ('1La', 4.5), ('1Bb', 5.8)],
        },
        'Tyr (p=4)': {
            'x': 1.7, 'color': '#636363',
            'states': [('S0', 0.0), ('T1', 3.5), ('1Lb', 4.5), ('1La', 4.8)],
        },
        'Phe (p=4)': {
            'x': 2.9, 'color': '#969696',
            'states': [('S0', 0.0), ('T1', 3.8), ('1B2u', 4.9), ('1B1u', 5.5)],
        },
    }

    for name, info in residues.items():
        x = info['x']
        c = info['color']
        for sname, E in info['states']:
            ax2.plot([x-0.3, x+0.3], [E, E], color=c, linewidth=2.0, solid_capstyle='round')
            ax2.text(x+0.35, E, sname, fontsize=7, va='center', ha='left', color=c)
        ax2.text(x, -0.35, name, ha='center', va='top', fontsize=9, fontweight='bold', color=c)
        # Count label
        n_states = len(info['states'])
        ax2.text(x, 6.4, f'{n_states} states', ha='center', va='bottom', fontsize=8,
                 fontweight='bold', color=c,
                 bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor=c, alpha=0.8))

    ax2.set_xticks([])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)

    fig.savefig('/home/yasa/RESEARCH/CUFT-RASP/figure1-structural-motif.png')
    plt.close(fig)
    print("Figure 1 saved: figure1-structural-motif.png")


# ================================================================
# FIGURE 2: Collective-factorized transition in CRY Trp triads
# ================================================================
def make_figure2():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # --- Panel (a): V/Delta_E vs detuning ---
    ax1.set_title('(a) Collective-factorized transition', fontsize=11, fontweight='bold', loc='left')

    mu = 5.0  # Debye, corrected TDM
    TDC_corr = 0.50
    # V ~ mu^2 / R^3 * TDC_corr, for nearest-neighbor ~3.8 A
    R_nn = 3.8e-10  # meters
    # V in meV: mu^2 * TDC / R^3 in proper units
    # Using tabulated: V_nn ~ 28 meV at mu=5.0D, TDC=0.50
    V_nn = 28.0  # meV

    detuning = np.linspace(1, 600, 500)  # meV
    V_over_dE = V_nn / detuning

    ax1.plot(detuning, V_over_dE, 'k-', linewidth=2.0, label='V/\u0394E (nearest-neighbor)')

    # Regime shading
    ax1.axhspan(0.4, 1.0, alpha=0.15, color='gold', label='Transition regime')
    ax1.axhspan(1.0, 5.0, alpha=0.10, color='blue', label='Collective regime')
    ax1.axhspan(0.0, 0.4, alpha=0.10, color='red', label='Factorized regime')

    # CRY band
    ax1.axvspan(20, 50, alpha=0.25, color='green', label='CRY (20-50 meV)')
    # Tubulin band
    ax1.axvspan(400, 550, alpha=0.25, color='orange', label='Tubulin (~500 meV)')

    ax1.set_xlabel('Protein-induced detuning \u0394E (meV)', fontsize=11)
    ax1.set_ylabel('V / \u0394E', fontsize=11)
    ax1.set_ylim(0, 3.0)
    ax1.set_xlim(0, 600)
    ax1.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax1.axhline(y=1.0, color='blue', linestyle=':', alpha=0.4)
    ax1.axhline(y=0.4, color='red', linestyle=':', alpha=0.4)

    # Annotations
    ax1.annotate('CRY: V/\u0394E = 0.4-1.0\n(transition)', xy=(35, 0.7), fontsize=8,
                 ha='center', va='center', fontweight='bold', color='#006d2c',
                 bbox=dict(boxstyle='round', fc='white', ec='green', alpha=0.8))
    ax1.annotate('Tubulin: V/\u0394E < 0.06\n(deep factorized)', xy=(475, 0.25), fontsize=8,
                 ha='center', va='center', fontweight='bold', color='#8c2d04',
                 bbox=dict(boxstyle='round', fc='white', ec='orange', alpha=0.8))

    # --- Panel (b): CRY family V/Delta_E values ---
    ax2.set_title('(b) CRY family variation at corrected parameters', fontsize=11, fontweight='bold', loc='left')

    families = ['CRY1', 'CRY-DASH', 'CPD PHL', '(6-4) PHL']
    # Detuning ranges from different CRY family structures
    detuning_vals = [35, 25, 40, 45]  # meV, representative
    V_dE_vals = [V_nn / d for d in detuning_vals]
    colors = ['#2166ac', '#4393c3', '#92c5de', '#d1e5f0']

    bars = ax2.bar(families, V_dE_vals, color=colors, edgecolor='black', linewidth=0.8, width=0.6)

    # Transition regime band
    ax2.axhspan(0.4, 1.0, alpha=0.2, color='gold', zorder=0)
    ax2.axhline(y=1.0, color='blue', linestyle=':', alpha=0.5, label='Collective boundary')
    ax2.axhline(y=0.4, color='red', linestyle=':', alpha=0.5, label='Factorized boundary')

    for bar, val in zip(bars, V_dE_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax2.set_ylabel('V / \u0394E', fontsize=11)
    ax2.set_ylim(0, 1.4)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.text(2.0, 0.7, 'Transition\nregime', ha='center', va='center', fontsize=10,
             fontstyle='italic', color='#8c6d31', alpha=0.7)
    ax2.text(0.5, 0.15, '\u03bc = 5.0 D, TDC = 0.50', ha='left', va='center', fontsize=8,
             fontstyle='italic', color='gray')

    fig.tight_layout()
    fig.savefig('/home/yasa/RESEARCH/CUFT-RASP/figure2-collective-factorized.png')
    plt.close(fig)
    print("Figure 2 saved: figure2-collective-factorized.png")


# ================================================================
# FIGURE 3: Decoherence and spectroscopic predictions
# ================================================================
def make_figure3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # --- Panel (a): Dephasing function g(t) and coherence C(t) ---
    ax1.set_title('(a) Dephasing function and coherence decay', fontsize=11, fontweight='bold', loc='left')

    # Drude-Lorentz parameters for CRY
    lambda_reorg = 35.0  # meV (reorganization energy)
    tau_c = 50.0  # fs (bath correlation time)
    gamma_c = 1.0 / tau_c  # fs^-1
    kBT = 25.7  # meV at 300 K

    t = np.linspace(0.1, 500, 2000)  # fs

    # Dephasing function g(t) for Drude-Lorentz (high-T approximation)
    # g(t) = (lambda * kBT / hbar^2 * gamma_c) * [gamma_c * t - 1 + exp(-gamma_c * t)]
    #       + i * (lambda / hbar * gamma_c) * [gamma_c * t - 1 + exp(-gamma_c * t)]
    # Real part dominates at 300 K
    gt = (lambda_reorg * kBT) * (gamma_c * t - 1 + np.exp(-gamma_c * t))
    # Scale to make units work (dimensionless g(t))
    # At T=300K, lambda=35meV, tau_c=50fs: T2* ~ 12 fs
    # Calibrate: g(12) should be ~1 for single chromophore
    scale = 1.0 / (12.0**2 * 0.5 * gamma_c)  # Gaussian regime: g ~ t^2/(2*T2*^2)
    gt_scaled = (t / 12.0)**2 * 0.5 * np.where(t < tau_c, 1.0, tau_c / t)
    # More physical: smooth crossover
    gt_phys = np.zeros_like(t)
    for i_t, ti in enumerate(t):
        x = gamma_c * ti
        gt_phys[i_t] = lambda_reorg * kBT / 1000.0 * (x - 1 + np.exp(-x))

    # Normalize so T2* = 12 fs (g(12) = 1)
    g12 = lambda_reorg * kBT / 1000.0 * (gamma_c * 12 - 1 + np.exp(-gamma_c * 12))
    gt_norm = gt_phys / g12

    Ct = np.exp(-gt_norm)

    # Plot g(t) on left y-axis
    color_g = '#2166ac'
    ax1.semilogy(t, gt_norm, color=color_g, linewidth=2.0, label='g(t) / g(T$_2$*)')
    ax1.set_xlabel('Time (fs)', fontsize=11)
    ax1.set_ylabel('g(t) [normalized]', fontsize=11, color=color_g)
    ax1.tick_params(axis='y', labelcolor=color_g)

    # Coherence on twin axis
    ax1b = ax1.twinx()
    color_c = '#d6604d'
    ax1b.plot(t, Ct, color=color_c, linewidth=2.0, linestyle='--', label='C(t) = exp(-g(t))')
    ax1b.set_ylabel('Coherence C(t)', fontsize=11, color=color_c)
    ax1b.tick_params(axis='y', labelcolor=color_c)
    ax1b.set_ylim(-0.05, 1.05)

    # Mark T2* = 12 fs
    ax1.axvline(x=12, color='gray', linestyle=':', alpha=0.7)
    ax1.text(14, 0.5, 'T$_2$* = 12 fs\n(single)', fontsize=8, va='center', color='gray')

    # Mark T2* = 19 fs (collective)
    ax1.axvline(x=19, color='#1a9850', linestyle=':', alpha=0.7)
    ax1.text(21, 2.0, 'T$_2$* = 19 fs\n(collective)', fontsize=8, va='center', color='#1a9850')

    # Mark 390 fs ET step
    ax1.axvline(x=390, color='black', linestyle='-', alpha=0.5, linewidth=1.5)
    ax1.text(370, 100, 'First ET\nstep\n390 fs', fontsize=8, ha='right', va='center',
             fontweight='bold', bbox=dict(boxstyle='round', fc='lightyellow', ec='black', alpha=0.8))

    # C(390 fs) annotation
    C390 = Ct[np.argmin(np.abs(t - 390))]
    ax1b.annotate(f'C(390 fs) < 10$^{{-49}}$', xy=(390, 0.0), xytext=(300, 0.3),
                  fontsize=8, fontweight='bold', color=color_c,
                  arrowprops=dict(arrowstyle='->', color=color_c, lw=1.5),
                  bbox=dict(boxstyle='round', fc='white', ec=color_c, alpha=0.8))

    # Mark Gaussian vs Markovian crossover
    ax1.axvline(x=50, color='purple', linestyle='-.', alpha=0.4)
    ax1.text(55, 20, '\u03c4$_c$ = 50 fs\n(crossover)', fontsize=7, color='purple', alpha=0.7)

    ax1.set_xlim(0, 500)
    ax1.set_ylim(0.01, 1e4)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=8)

    # --- Panel (b): Temperature dependence of T2* ---
    ax2.set_title('(b) Temperature dependence of T$_2$*', fontsize=11, fontweight='bold', loc='left')

    T_range = np.linspace(5, 350, 200)  # K
    kB = 0.08617  # meV/K

    # T2* ~ hbar / sqrt(2 * lambda * kBT) for high-T Gaussian regime
    # Single chromophore
    T2_single = 12.0 * np.sqrt(300.0 / T_range)  # Scale from 12 fs at 300K
    # Collective (exchange-narrowed by sqrt(3))
    T2_collective = T2_single * np.sqrt(3) / np.sqrt(3) * (19.0 / 12.0)
    # More precisely, collective T2* = 19 fs at 300K
    T2_collective = 19.0 * np.sqrt(300.0 / T_range)

    ax2.plot(T_range, T2_single, color='#2166ac', linewidth=2.0, label='Single chromophore T$_2$*')
    ax2.plot(T_range, T2_collective, color='#1a9850', linewidth=2.0, label='Collective T$_2$* (exchange-narrowed)')

    # 390 fs ET step line
    ax2.axhline(y=390, color='black', linestyle='--', alpha=0.5, linewidth=1.5, label='First ET step (390 fs)')

    # Find crossing temperatures
    T_cross_single = 300.0 * (12.0 / 390.0)**2
    T_cross_coll = 300.0 * (19.0 / 390.0)**2

    ax2.axvline(x=T_cross_single, color='#2166ac', linestyle=':', alpha=0.5)
    ax2.axvline(x=T_cross_coll, color='#1a9850', linestyle=':', alpha=0.5)

    ax2.annotate(f'T = {T_cross_single:.1f} K', xy=(T_cross_single, 390),
                 xytext=(T_cross_single + 15, 450), fontsize=8, color='#2166ac',
                 arrowprops=dict(arrowstyle='->', color='#2166ac'))
    ax2.annotate(f'T = {T_cross_coll:.1f} K', xy=(T_cross_coll, 390),
                 xytext=(T_cross_coll + 15, 500), fontsize=8, color='#1a9850',
                 arrowprops=dict(arrowstyle='->', color='#1a9850'))

    # Shade biological temperature range
    ax2.axvspan(290, 310, alpha=0.15, color='red', label='Biological range')

    # Shade where coherence survives to ET step
    ax2.fill_between(T_range, T2_collective, 390,
                     where=T2_collective > 390, alpha=0.1, color='green')
    ax2.text(5, 420, 'Coherence survives\nto ET step', fontsize=8, color='#1a9850', fontstyle='italic')

    ax2.set_xlabel('Temperature (K)', fontsize=11)
    ax2.set_ylabel('T$_2$* (fs)', fontsize=11)
    ax2.set_xlim(0, 350)
    ax2.set_ylim(0, 600)
    ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig('/home/yasa/RESEARCH/CUFT-RASP/figure3-decoherence-predictions.png')
    plt.close(fig)
    print("Figure 3 saved: figure3-decoherence-predictions.png")


if __name__ == '__main__':
    make_figure1()
    make_figure2()
    make_figure3()
    print("\nAll three figures generated successfully.")
