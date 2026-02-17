"""
Q3: Can you find patterns for n values for which the cardinality of the
value set is 3, 4, 5, ..., p-1?

This script visualizes:
1. How many indices achieve each cardinality, as a function of p
2. Cardinality distribution histograms for selected primes
3. Relationship between divisors of p^2-1 and number of distinct cardinalities
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os


def divisors(n):
    """Return the set of divisors of n."""
    divs = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return divs


def factorize(n):
    """Return prime factorization as dict {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    csv_path = os.path.join(base_dir, 'data', 'reversed_dickson_values.csv')
    plot_dir = os.path.join(base_dir, 'output', 'plots')
    os.makedirs(plot_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df[df['p'] > 3].copy()
    primes = sorted(df['p'].unique())

    print("=" * 70)
    print("Q3: Cardinality c Index Patterns Visualization")
    print("=" * 70)
    print()

    # Count indices per (prime, cardinality)
    counts = df.groupby(['p', 'value_count']).size().reset_index(name='index_count')

    # =====================================================================
    # Plot 1: Index count by cardinality (for cardinalities 1-10)
    # =====================================================================
    fig, axes = plt.subplots(2, 5, figsize=(20, 8), sharey=False)
    colors = plt.cm.tab10(np.linspace(0, 1, 10))

    for idx, c in enumerate(range(1, 11)):
        ax = axes[idx // 5, idx % 5]
        sub = counts[counts['value_count'] == c]

        # Get data for all primes (fill 0 where cardinality doesn't appear)
        p_vals = []
        count_vals = []
        for p in primes:
            p_sub = sub[sub['p'] == p]
            p_vals.append(p)
            count_vals.append(p_sub['index_count'].values[0] if len(p_sub) > 0 else 0)

        ax.scatter(p_vals, count_vals, c=[colors[idx]], s=30, edgecolors='black',
                   linewidths=0.5, zorder=3)
        ax.plot(p_vals, count_vals, color=colors[idx], alpha=0.4, linewidth=1)

        # Highlight constant patterns
        if c <= 2:
            ax.axhline(y=3, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax.text(primes[-1], 3.5, 'always 3', fontsize=7, color='red', ha='right')

        ax.set_title(f'Card = {c}', fontsize=11, fontweight='bold')
        ax.set_xlabel('$p$', fontsize=9)
        if idx % 5 == 0:
            ax.set_ylabel('# of indices', fontsize=9)
        ax.grid(alpha=0.3)
        ax.tick_params(labelsize=7)

    fig.suptitle('Q3: Number of Indices Achieving Each Cardinality vs Prime $p$',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q3_index_counts.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Index counts plot saved to output/plots/q3_index_counts.png")

    # =====================================================================
    # Plot 2: Cardinality histograms for selected primes
    # =====================================================================
    selected_primes = [11, 37, 67, 97]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for idx, p in enumerate(selected_primes):
        ax = axes[idx // 2, idx % 2]
        sub = df[df['p'] == p]
        card_counts = sub['value_count'].value_counts().sort_index()

        ax.bar(card_counts.index, card_counts.values, color='#4472C4',
               edgecolor='navy', linewidth=0.3, alpha=0.8)

        # Mark (p+1)/2
        half = (p + 1) / 2
        ax.axvline(x=half, color='red', linestyle='--', alpha=0.6, linewidth=1.5)
        ax.text(half, ax.get_ylim()[1] * 0.9, f'$(p+1)/2={half:.0f}$',
                fontsize=9, color='red', ha='left', va='top')

        ax.set_xlabel('Cardinality $c$', fontsize=10)
        ax.set_ylabel('Number of indices $n$', fontsize=10)
        ax.set_title(f'$p = {p}$  ($p^2-1 = {p*p-1}$)', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

    fig.suptitle('Q3: Distribution of Value Set Cardinalities',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q3_cardinality_histograms.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Histograms saved to output/plots/q3_cardinality_histograms.png")

    # =====================================================================
    # Plot 3: Divisor relationship
    # =====================================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: num divisors of p^2-1 vs number of distinct cardinalities
    ax = axes[0]
    for p in primes:
        n_divs = len(divisors(p * p - 1))
        sub = df[df['p'] == p]
        n_distinct_cards = sub['value_count'].nunique()
        ax.scatter(n_divs, n_distinct_cards, c='#4472C4', s=50,
                   edgecolors='navy', zorder=3)
        ax.annotate(str(p), (n_divs, n_distinct_cards),
                    textcoords="offset points", xytext=(3, 3), fontsize=7)

    ax.set_xlabel('Number of divisors of $p^2 - 1$', fontsize=11)
    ax.set_ylabel('Number of distinct cardinalities achieved', fontsize=11)
    ax.set_title('Divisor Count vs Distinct Cardinalities', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3)

    # Right: num distinct prime factors of p^2-1 vs coverage %
    ax = axes[1]
    for p in primes:
        facts = factorize(p * p - 1)
        n_prime_factors = len(facts)
        sub = df[df['p'] == p]
        observed = set(sub['value_count'].unique())
        expected = set(range(1, p))
        coverage = len(expected & observed) / len(expected) * 100

        color = '#51CF66' if coverage == 100 else '#4472C4'
        ax.scatter(n_prime_factors, coverage, c=color, s=60,
                   edgecolors='navy', zorder=3)
        ax.annotate(str(p), (n_prime_factors, coverage),
                    textcoords="offset points", xytext=(3, 3), fontsize=7)

    ax.set_xlabel('Number of distinct prime factors of $p^2 - 1$', fontsize=11)
    ax.set_ylabel('Coverage %', fontsize=11)
    ax.set_title('Prime Factor Count vs Coverage', fontsize=12, fontweight='bold')
    ax.axhline(y=100, color='green', linestyle=':', alpha=0.4)
    ax.grid(alpha=0.3)

    fig.suptitle('Q3: Relationship Between $p^2-1$ Structure and Cardinality Patterns',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q3_divisor_relationship.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Divisor relationship saved to output/plots/q3_divisor_relationship.png")

    # Print summary
    print()
    print("Summary of index counts for small cardinalities:")
    for c in range(1, 6):
        sub = counts[counts['value_count'] == c]
        vals = sub['index_count'].tolist()
        if vals:
            print(f"  Card={c}: min={min(vals)}, max={max(vals)}, "
                  f"constant={'YES' if min(vals) == max(vals) else 'NO'}")

    print("\nDone.")


if __name__ == '__main__':
    main()
