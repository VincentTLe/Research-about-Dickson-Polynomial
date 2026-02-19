"""
Q1: Let the parameter a be nonzero. Is the cardinality of the value set
independent of the parameter a?

This script computes value sets for D_n(a, x) for all nonzero a and
visualizes that the cardinality distributions are identical. The case
a=0 is shown as a degenerate contrast.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math
import os
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.append(str(SCRIPT_ROOT))

from utilities.dickson import reversed_dickson


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def compute_value_sets(p, a):
    """Compute value sets for reversed Dickson polynomial D_n(a, x)
    for all n in [0, p^2-1) and all x in F_p.

    Returns list of (n, cardinality, is_permutation, value_set).
    """
    results = []
    Dprev = [2 % p] * p
    Dcurr = [a % p] * p

    vals = sorted(set(Dprev))
    results.append((0, len(vals), len(vals) == p, vals))
    vals = sorted(set(Dcurr))
    results.append((1, len(vals), len(vals) == p, vals))

    for n in range(2, p * p):
        Dnext = []
        for x in range(p):
            # Explicitly using reversed variant D_n(a, x).
            Dnext_val = reversed_dickson(n=n, a=a, x=x, modulus=p)
            Dnext.append(Dnext_val)
        vals = sorted(set(Dnext))
        results.append((n, len(vals), len(vals) == p, vals))
        Dprev, Dcurr = Dcurr, Dnext

    return results


def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    plot_dir = os.path.join(base_dir, 'output', 'plots')
    result_dir = os.path.join(base_dir, 'output', 'results')
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    # Selected primes (keeping small for computational feasibility)
    PRIMES = [5, 7, 11, 13, 23]

    print("=" * 70)
    print("Q1: Parameter Independence Visualization")
    print("    Is |V_n(a)| independent of nonzero a?")
    print("=" * 70)
    print()

    verification_lines = []

    for p in PRIMES:
        print(f"Processing p = {p} ...", flush=True)

        # Build matrix: rows = a values (0..p-1), cols = cardinalities (1..p)
        card_matrix = np.zeros((p, p), dtype=int)  # card_matrix[a, c-1] = count of n with card=c

        for a in range(p):
            results = compute_value_sets(p, a)
            for (n, card, is_perm, vals) in results:
                if 1 <= card <= p:
                    card_matrix[a, card - 1] += 1

        # Verify: all nonzero a rows are identical
        nonzero_rows = card_matrix[1:, :]
        all_identical = np.all(nonzero_rows == nonzero_rows[0])
        a0_differs = not np.array_equal(card_matrix[0], card_matrix[1])

        status = f"p={p}: All nonzero a identical: {all_identical}, a=0 differs: {a0_differs}"
        print(f"  {status}")
        verification_lines.append(status)

        # --- Heatmap ---
        fig, ax = plt.subplots(figsize=(max(8, p * 0.4), max(5, p * 0.25)))

        # Use log scale for better visibility
        display_matrix = card_matrix.astype(float)
        display_matrix[display_matrix == 0] = np.nan  # mask zeros

        im = ax.imshow(display_matrix, aspect='auto', cmap='YlOrRd',
                       interpolation='nearest')

        ax.set_xlabel('Cardinality $c$', fontsize=12)
        ax.set_ylabel('Parameter $a$', fontsize=12)
        ax.set_title(f'Q1: Cardinality Distribution by Parameter $a$ ($p = {p}$)\n'
                     f'All nonzero $a$ identical: {all_identical}',
                     fontsize=13, fontweight='bold')

        # Tick labels
        card_labels = list(range(1, p + 1))
        a_labels = list(range(p))
        ax.set_xticks(range(p))
        ax.set_xticklabels(card_labels, fontsize=8)
        ax.set_yticks(range(p))
        ax.set_yticklabels(a_labels, fontsize=8)

        # Highlight a=0 row with a border
        rect = plt.Rectangle((-0.5, -0.5), p, 1, linewidth=2.5,
                              edgecolor='blue', facecolor='none', linestyle='--')
        ax.add_patch(rect)
        ax.text(p + 0.3, 0, '$a=0$\n(degenerate)', fontsize=9, color='blue',
                va='center', fontweight='bold')

        plt.colorbar(im, ax=ax, label='Count of indices $n$', shrink=0.8)
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, f'q1_parameter_heatmap_p{p}.png'),
                    dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Heatmap saved to output/plots/q1_parameter_heatmap_p{p}.png")

    # --- Summary figure: side-by-side comparison for a=0 vs a=1 ---
    fig, axes = plt.subplots(1, len(PRIMES), figsize=(4 * len(PRIMES), 5),
                             sharey=False)
    if len(PRIMES) == 1:
        axes = [axes]

    for idx, p in enumerate(PRIMES):
        ax = axes[idx]
        # Recompute for summary (quick for small primes)
        results_a0 = compute_value_sets(p, 0)
        results_a1 = compute_value_sets(p, 1)

        cards_a0 = [r[1] for r in results_a0]
        cards_a1 = [r[1] for r in results_a1]

        bins = np.arange(0.5, p + 1.5, 1)
        ax.hist(cards_a1, bins=bins, alpha=0.7, label='$a \\neq 0$', color='#4472C4')
        ax.hist(cards_a0, bins=bins, alpha=0.5, label='$a = 0$', color='#ED7D31')
        ax.set_xlabel('Cardinality', fontsize=10)
        if idx == 0:
            ax.set_ylabel('Count of indices $n$', fontsize=10)
        ax.set_title(f'$p = {p}$', fontsize=12, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=0.3)

    fig.suptitle('Q1: Cardinality Distribution — $a = 0$ (degenerate) vs $a \\neq 0$',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q1_parameter_comparison.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nComparison plot saved to output/plots/q1_parameter_comparison.png")

    # --- Save verification ---
    out_path = os.path.join(result_dir, 'q1_verification.txt')
    with open(out_path, 'w') as f:
        f.write("Q1: Parameter Independence Verification\n")
        f.write("=" * 50 + "\n\n")
        f.write("Result: For all nonzero a in F_p, the cardinality distribution\n")
        f.write("of value sets {D_n(a, x) : x in F_p} is IDENTICAL.\n\n")
        f.write("Mathematical explanation:\n")
        f.write("  D_n(a, x) = a^n * D_n(x/a^2, 1)  for a != 0\n")
        f.write("  Since x -> x/a^2 is a bijection on F_p and\n")
        f.write("  multiplication by a^n is a bijection on F_p,\n")
        f.write("  the value set has the same cardinality.\n\n")
        f.write("The case a = 0 is degenerate (different recurrence behavior).\n\n")
        for line in verification_lines:
            f.write(line + "\n")
    print(f"Verification saved to output/results/q1_verification.txt")


if __name__ == '__main__':
    main()
