"""
Q2: Can you find patterns for missing indices (cardinalities that don't appear)
as p gets large?

This script visualizes:
1. A presence/absence heatmap of cardinalities across primes
2. A scatter plot of missing cardinalities
3. A coverage trend line
4. A frequency bar chart of most-commonly-missing cardinalities
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
import math
import os
from collections import Counter


def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    csv_path = os.path.join(base_dir, 'data', 'reversed_dickson_values.csv')
    plot_dir = os.path.join(base_dir, 'output', 'plots')
    os.makedirs(plot_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df[df['p'] > 3].copy()
    primes = sorted(df['p'].unique())

    print("=" * 70)
    print("Q2: Missing Cardinality Patterns Visualization")
    print("=" * 70)
    print()

    # Compute observed/missing cardinalities per prime
    data = {}
    for p in primes:
        sub = df[df['p'] == p]
        observed = set(sub['value_count'].unique())
        expected = set(range(1, p))
        missing = sorted(expected - observed)
        coverage = len(expected & observed) / len(expected) * 100
        data[p] = {
            'observed': observed,
            'missing': missing,
            'coverage': coverage,
        }

    # =====================================================================
    # Plot 1: Presence/absence heatmap
    # =====================================================================
    max_card = max(primes) - 1  # max cardinality is p-1 for largest prime
    heatmap = np.full((len(primes), max_card), np.nan)  # NaN = out of range

    for i, p in enumerate(primes):
        for c in range(1, p):
            if c in data[p]['observed']:
                heatmap[i, c - 1] = 1  # present
            else:
                heatmap[i, c - 1] = 0  # missing

    fig, ax = plt.subplots(figsize=(16, 8))
    cmap = mcolors.ListedColormap(['#FF6B6B', '#51CF66', '#E0E0E0'])
    bounds = [-0.5, 0.5, 1.5, 2.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Replace NaN with 2 for display
    display = np.where(np.isnan(heatmap), 2, heatmap)
    im = ax.imshow(display, aspect='auto', cmap=cmap, norm=norm, interpolation='nearest')

    ax.set_xlabel('Cardinality $c$', fontsize=12)
    ax.set_ylabel('Prime $p$', fontsize=12)
    ax.set_title('Q2: Cardinality Presence/Absence Across Primes\n'
                 '(Green = present, Red = missing, Gray = out of range)',
                 fontsize=14, fontweight='bold')

    # Tick labels
    ax.set_yticks(range(len(primes)))
    ax.set_yticklabels([str(p) for p in primes], fontsize=8)

    # Only show every 5th x tick for readability
    xtick_step = max(1, max_card // 20)
    ax.set_xticks(range(0, max_card, xtick_step))
    ax.set_xticklabels(range(1, max_card + 1, xtick_step), fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q2_cardinality_presence_heatmap.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Heatmap saved to output/plots/q2_cardinality_presence_heatmap.png")

    # =====================================================================
    # Plot 2: Missing cardinalities scatter
    # =====================================================================
    fig, ax = plt.subplots(figsize=(12, 7))

    for p in primes:
        missing = data[p]['missing']
        if missing:
            ax.scatter([p] * len(missing), missing, c='#FF6B6B', s=15,
                       alpha=0.7, edgecolors='darkred', linewidths=0.3)

    # Reference lines
    ax.plot(primes, [p - 1 for p in primes], 'k--', alpha=0.3, label='$c = p - 1$')
    ax.plot(primes, [p / 2 for p in primes], 'b--', alpha=0.3, label='$c = p/2$')

    ax.set_xlabel('Prime $p$', fontsize=12)
    ax.set_ylabel('Missing Cardinality $c$', fontsize=12)
    ax.set_title('Q2: Missing Cardinalities by Prime\n'
                 '(Each dot = a cardinality not achieved for that prime)',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q2_missing_scatter.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Scatter saved to output/plots/q2_missing_scatter.png")

    # =====================================================================
    # Plot 3: Coverage trend
    # =====================================================================
    fig, ax = plt.subplots(figsize=(10, 6))

    coverages = [data[p]['coverage'] for p in primes]
    ax.scatter(primes, coverages, c='#4472C4', s=60, zorder=3, edgecolors='navy')

    # Highlight 100% primes
    for p in primes:
        if data[p]['coverage'] == 100:
            ax.annotate(f'$p={p}$', (p, 100), textcoords="offset points",
                        xytext=(5, 5), fontsize=10, color='green', fontweight='bold')

    # Trend line
    p_arr = np.array(primes, dtype=float)
    c_arr = np.array(coverages, dtype=float)
    # Use log fit: coverage ~ a * log(p) + b
    log_p = np.log(p_arr)
    coeffs = np.polyfit(log_p, c_arr, 1)
    p_smooth = np.linspace(min(primes), max(primes), 200)
    trend = np.polyval(coeffs, np.log(p_smooth))
    ax.plot(p_smooth, trend, 'r--', alpha=0.6, linewidth=2,
            label=f'Trend: {coeffs[0]:.1f} ln($p$) + {coeffs[1]:.1f}')

    ax.axhline(y=100, color='green', linestyle=':', alpha=0.4)
    ax.set_xlabel('Prime $p$', fontsize=12)
    ax.set_ylabel('Coverage %', fontsize=12)
    ax.set_title('Q2: Cardinality Coverage Percentage vs Prime $p$',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_ylim(60, 105)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q2_coverage_trend.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Coverage trend saved to output/plots/q2_coverage_trend.png")

    # =====================================================================
    # Plot 4: Frequency of missing cardinalities
    # =====================================================================
    all_missing = []
    for p in primes:
        all_missing.extend(data[p]['missing'])

    if all_missing:
        freq = Counter(all_missing)
        cards_sorted = sorted(freq.keys())
        counts = [freq[c] for c in cards_sorted]

        fig, ax = plt.subplots(figsize=(14, 5))
        colors = ['#FF6B6B' if freq[c] >= 10 else '#FFB3B3' if freq[c] >= 5
                  else '#FFD9D9' for c in cards_sorted]
        ax.bar(cards_sorted, counts, color=colors, edgecolor='darkred', linewidth=0.5)

        # Highlight the most frequently missing
        most_common = freq.most_common(3)
        for card, count in most_common:
            ax.annotate(f'$c={card}$\n({count} primes)',
                        (card, count), textcoords="offset points",
                        xytext=(0, 8), ha='center', fontsize=8, fontweight='bold')

        ax.set_xlabel('Cardinality $c$', fontsize=12)
        ax.set_ylabel('Number of Primes Missing This Cardinality', fontsize=12)
        ax.set_title('Q2: How Often Each Cardinality is Missing Across Primes',
                     fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, 'q2_missing_frequency.png'),
                    dpi=150, bbox_inches='tight')
        plt.close()
        print("Frequency chart saved to output/plots/q2_missing_frequency.png")
    else:
        print("No missing cardinalities found!")

    print("\nDone.")


if __name__ == '__main__':
    main()
