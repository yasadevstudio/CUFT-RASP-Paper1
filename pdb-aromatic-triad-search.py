#!/usr/bin/env python3
"""
YASA PRESENTS
pdb-aromatic-triad-search.py - Aromatic Triad Analysis in Beta-Tubulin (PDB 1JFF)

Purpose: Systematically find the tightest aromatic triad in beta-tubulin chain B
         by exhaustive combinatorial search over all aromatic residues (Trp, Phe, Tyr, His).

Method:  For each 3-residue combination, compute the maximum CA-CA distance.
         The "tightest" triad minimizes this maximum pairwise distance.

Context: CUFT-RASP Orch-OR bridge paper — verifying whether Trp407/Phe404/Tyr408
         is genuinely the tightest aromatic triad in beta-tubulin.
"""

import urllib.request
import math
import itertools
import os

# ──────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────

PDB_URL = "https://files.rcsb.org/download/1JFF.pdb"
PDB_PATH = "/home/yasa/RESEARCH/CUFT-RASP/1JFF.pdb"
TARGET_CHAIN = "B"  # Beta-tubulin
AROMATIC_RESIDUES = {"TRP", "PHE", "TYR", "HIS"}
TOP_N = 20
DETAILED_TOP = 5

# The claimed tightest triad from the paper
CLAIMED_TRIAD = frozenset([(407, "TRP"), (404, "PHE"), (408, "TYR")])


def download_pdb(url, path):
    """Download PDB file if not already present."""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"PDB file already exists: {path} ({size:,} bytes)")
        return
    print(f"Downloading PDB 1JFF from {url} ...")
    urllib.request.urlretrieve(url, path)
    size = os.path.getsize(path)
    print(f"Downloaded: {path} ({size:,} bytes)")


def parse_pdb_aromatic_ca(path, chain, aromatic_set):
    """
    Parse PDB file for CA atoms of aromatic residues in specified chain.

    PDB ATOM record format (fixed-width columns):
      Columns  1- 6: Record type ("ATOM  ")
      Columns  7-11: Atom serial number
      Columns 13-16: Atom name (e.g., " CA ")
      Column     17: Alternate location indicator
      Columns 18-20: Residue name (e.g., "TRP")
      Column     22: Chain ID
      Columns 23-26: Residue sequence number
      Column     27: Code for insertion of residues
      Columns 31-38: X coordinate (8.3 format)
      Columns 39-46: Y coordinate (8.3 format)
      Columns 47-54: Z coordinate (8.3 format)

    Returns: dict mapping (resnum, resname) -> (x, y, z)
    """
    residues = {}
    atom_count = 0
    total_atoms = 0

    with open(path, "r") as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            total_atoms += 1

            # Extract fields using fixed-width column positions (0-indexed)
            atom_name = line[12:16].strip()
            res_name = line[17:20].strip()
            chain_id = line[21]
            try:
                res_seq = int(line[22:26].strip())
            except ValueError:
                continue

            # Filter: chain B, CA atom, aromatic residue
            if chain_id != chain:
                continue
            if atom_name != "CA":
                continue
            if res_name not in aromatic_set:
                continue

            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())

            key = (res_seq, res_name)
            residues[key] = (x, y, z)
            atom_count += 1

    print(f"\nPDB parsing complete:")
    print(f"  Total ATOM records: {total_atoms:,}")
    print(f"  Chain {chain} aromatic CA atoms found: {atom_count}")
    return residues


def ca_distance(coord1, coord2):
    """Euclidean distance between two 3D coordinates."""
    dx = coord1[0] - coord2[0]
    dy = coord1[1] - coord2[1]
    dz = coord1[2] - coord2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def triad_max_distance(r1, r2, r3, coords):
    """Compute the maximum pairwise CA-CA distance for a triad."""
    d12 = ca_distance(coords[r1], coords[r2])
    d13 = ca_distance(coords[r1], coords[r3])
    d23 = ca_distance(coords[r2], coords[r3])
    return max(d12, d13, d23), (d12, d13, d23)


def format_residue(res):
    """Format a (resnum, resname) tuple as e.g. 'Trp-407'."""
    resnum, resname = res
    name_map = {"TRP": "Trp", "PHE": "Phe", "TYR": "Tyr", "HIS": "His"}
    return f"{name_map.get(resname, resname)}-{resnum}"


def main():
    print("=" * 72)
    print("AROMATIC TRIAD ANALYSIS — BETA-TUBULIN (PDB 1JFF, CHAIN B)")
    print("CUFT-RASP Orch-OR Bridge Paper Verification")
    print("=" * 72)

    # Step 1: Download PDB
    download_pdb(PDB_URL, PDB_PATH)

    # Step 2: Parse aromatic CA atoms
    coords = parse_pdb_aromatic_ca(PDB_PATH, TARGET_CHAIN, AROMATIC_RESIDUES)

    if not coords:
        print("ERROR: No aromatic CA atoms found in chain B. Check PDB file.")
        return

    # Step 3: List all aromatic residues found
    residues = sorted(coords.keys(), key=lambda r: r[0])
    print(f"\n{'─' * 72}")
    print(f"Aromatic residues in chain B ({len(residues)} total):")
    print(f"{'─' * 72}")

    by_type = {}
    for res in residues:
        rtype = res[1]
        by_type.setdefault(rtype, []).append(res)

    for rtype in ["TRP", "PHE", "TYR", "HIS"]:
        if rtype in by_type:
            rlist = by_type[rtype]
            nums = ", ".join(str(r[0]) for r in rlist)
            print(f"  {rtype} ({len(rlist)}): {nums}")

    # Step 4: Compute all triads
    n_triads = len(residues) * (len(residues) - 1) * (len(residues) - 2) // 6
    print(f"\n{'─' * 72}")
    print(f"Computing all {n_triads:,} possible triads...")
    print(f"{'─' * 72}")

    triad_results = []
    for combo in itertools.combinations(residues, 3):
        r1, r2, r3 = combo
        max_d, pairwise = triad_max_distance(r1, r2, r3, coords)
        triad_results.append((max_d, combo, pairwise))

    # Step 5: Sort by max distance (ascending = tightest first)
    triad_results.sort(key=lambda t: t[0])

    # Step 6: Display top 20
    print(f"\n{'=' * 72}")
    print(f"TOP {TOP_N} TIGHTEST AROMATIC TRIADS (by minimum max CA-CA distance)")
    print(f"{'=' * 72}")
    print(f"{'Rank':<6} {'Residue 1':<10} {'Residue 2':<10} {'Residue 3':<10} {'Max CA-CA (A)':>14}")
    print(f"{'─' * 56}")

    for i, (max_d, combo, pairwise) in enumerate(triad_results[:TOP_N]):
        r1, r2, r3 = combo
        label1 = format_residue(r1)
        label2 = format_residue(r2)
        label3 = format_residue(r3)
        marker = ""

        # Check if this is the claimed triad
        this_triad = frozenset([(r[0], r[1]) for r in combo])
        if this_triad == CLAIMED_TRIAD:
            marker = "  <-- CLAIMED"

        print(f"  {i+1:<4} {label1:<10} {label2:<10} {label3:<10} {max_d:>12.3f}{marker}")

    # Step 7: Find where the claimed triad ranks
    print(f"\n{'=' * 72}")
    print("CLAIMED TRIAD VERIFICATION: Trp-407 / Phe-404 / Tyr-408")
    print(f"{'=' * 72}")

    claimed_rank = None
    for i, (max_d, combo, pairwise) in enumerate(triad_results):
        this_triad = frozenset([(r[0], r[1]) for r in combo])
        if this_triad == CLAIMED_TRIAD:
            claimed_rank = i + 1
            claimed_max_d = max_d
            claimed_pairwise = pairwise
            claimed_combo = combo
            break

    if claimed_rank is not None:
        print(f"  Rank: #{claimed_rank} out of {n_triads:,} triads")
        print(f"  Max CA-CA distance: {claimed_max_d:.3f} A")
        r1, r2, r3 = claimed_combo
        d12, d13, d23 = claimed_pairwise
        print(f"  Pairwise distances:")
        print(f"    {format_residue(r1)} — {format_residue(r2)}: {d12:.3f} A")
        print(f"    {format_residue(r1)} — {format_residue(r3)}: {d13:.3f} A")
        print(f"    {format_residue(r2)} — {format_residue(r3)}: {d23:.3f} A")

        if claimed_rank == 1:
            print(f"\n  CONFIRMED: Trp-407/Phe-404/Tyr-408 IS the tightest aromatic triad.")
        else:
            # Show what actually IS #1
            best_max_d, best_combo, best_pairwise = triad_results[0]
            print(f"\n  NOT #1. The actual tightest triad is:")
            print(f"    {format_residue(best_combo[0])} / {format_residue(best_combo[1])} / {format_residue(best_combo[2])}")
            print(f"    Max CA-CA: {best_max_d:.3f} A vs claimed {claimed_max_d:.3f} A")
    else:
        print("  WARNING: Claimed triad NOT FOUND in chain B aromatic residues!")
        print("  Checking if residues 404, 407, 408 exist in any form...")
        for target_num in [404, 407, 408]:
            found = [r for r in residues if r[0] == target_num]
            if found:
                print(f"    Residue {target_num}: {found[0][1]} — FOUND")
            else:
                print(f"    Residue {target_num}: NOT FOUND in aromatic set")

    # Step 8: Detailed pairwise distances for top 5
    print(f"\n{'=' * 72}")
    print(f"DETAILED PAIRWISE DISTANCES — TOP {DETAILED_TOP} TRIADS")
    print(f"{'=' * 72}")

    for i, (max_d, combo, pairwise) in enumerate(triad_results[:DETAILED_TOP]):
        r1, r2, r3 = combo
        d12, d13, d23 = pairwise
        print(f"\n  #{i+1}: {format_residue(r1)} / {format_residue(r2)} / {format_residue(r3)}")
        print(f"       Max CA-CA: {max_d:.3f} A")
        print(f"       {format_residue(r1)} — {format_residue(r2)}: {d12:.3f} A")
        print(f"       {format_residue(r1)} — {format_residue(r3)}: {d13:.3f} A")
        print(f"       {format_residue(r2)} — {format_residue(r3)}: {d23:.3f} A")

        # Characterize the triad shape
        dists = sorted([d12, d13, d23])
        ratio = dists[2] / dists[0] if dists[0] > 0 else float('inf')
        print(f"       Shape: min={dists[0]:.3f}, mid={dists[1]:.3f}, max={dists[2]:.3f}")
        print(f"       Compactness (max/min): {ratio:.3f} (1.0 = equilateral)")

    # Step 9: Summary statistics
    print(f"\n{'=' * 72}")
    print("SUMMARY STATISTICS")
    print(f"{'=' * 72}")

    # Count by residue type in top 20
    type_counts = {"TRP": 0, "PHE": 0, "TYR": 0, "HIS": 0}
    for _, combo, _ in triad_results[:TOP_N]:
        for r in combo:
            type_counts[r[1]] += 1

    print(f"  Residue type frequency in top {TOP_N} triads:")
    for rtype in ["TRP", "PHE", "TYR", "HIS"]:
        print(f"    {rtype}: {type_counts[rtype]} appearances")

    # Identify most common residues in top 20
    res_counts = {}
    for _, combo, _ in triad_results[:TOP_N]:
        for r in combo:
            res_counts[r] = res_counts.get(r, 0) + 1

    print(f"\n  Most frequent residues in top {TOP_N} triads:")
    for res, count in sorted(res_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"    {format_residue(res)}: {count} appearances")

    # Check for all-WFY (no His) triads
    print(f"\n  Top 5 triads excluding HIS (Trp/Phe/Tyr only):")
    wfy_count = 0
    for i, (max_d, combo, pairwise) in enumerate(triad_results):
        if all(r[1] in {"TRP", "PHE", "TYR"} for r in combo):
            wfy_count += 1
            r1, r2, r3 = combo
            # Find overall rank
            rank = i + 1
            this_triad = frozenset([(r[0], r[1]) for r in combo])
            marker = " <-- CLAIMED" if this_triad == CLAIMED_TRIAD else ""
            print(f"    WFY-#{wfy_count} (overall #{rank}): "
                  f"{format_residue(r1)} / {format_residue(r2)} / {format_residue(r3)}  "
                  f"max={max_d:.3f} A{marker}")
            if wfy_count >= 5:
                break

    print(f"\n{'=' * 72}")
    print("Analysis complete.")
    print(f"{'=' * 72}")


if __name__ == "__main__":
    main()
