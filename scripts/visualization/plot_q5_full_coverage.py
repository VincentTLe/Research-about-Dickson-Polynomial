"""
Q5: Let 5 <= p <= 97. Can you explain why the cardinalities of value sets
vary from 1 through p-1 for only p = 5, 7, 11?

This script investigates the structural reasons by analyzing the factorization
of p^2 - 1, divisor counts, and their relationship to coverage.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os


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


def tau(n):
    """Number of divisors of n."""
    facts = factorize(n)
    result = 1
    for e in facts.values():
        result *= (e + 1)
    return result


def omega(n):
    """Number of distinct prime factors of n."""
    return len(factorize(n))


def euler_phi(n):
    """Euler's totient function."""
    facts = factorize(n)
    result = n
    for p in facts:
        result = result * (p - 1) // p
    return result


def factorize_str(n):
    """Pretty-print factorization."""
    facts = factorize(n)
    parts = []
    for p in sorted(facts):
        e = facts[p]
        if e == 1:
            parts.append(str(p))
        else:
            parts.append(f'{p}^{e}')
    return ' * '.join(parts)


def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    csv_path = os.path.join(base_dir, 'data', 'reversed_dickson_values.csv')
    plot_dir = os.path.join(base_dir, 'output', 'plots')
    os.makedirs(plot_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df[df['p'] > 3].copy()
    primes = sorted(df['p'].unique())

    print("=" * 70)
    print("Q5: Full Coverage Analysis")
    print("    Why only p = 5, 7, 11 have all cardinalities 1..p-1?")
    print("=" * 70)
    print()

    # Build analysis data
    analysis = []
    for p in primes:
        sub = df[df['p'] == p]
        observed = set(sub['value_count'].unique())
        expected = set(range(1, p))
        coverage = len(expected & observed) / len(expected) * 100
        n = p * p - 1
        analysis.append({
            'p': p,
            'p2_minus_1': n,
            'factorization': factorize_str(n),
            'tau': tau(n),
            'omega': omega(n),
            'phi': euler_phi(n),
            'coverage': coverage,
            'num_missing': len(expected - observed),
            'full_coverage': coverage == 100,
        })

    # Print factorization table
    print(f"{'p':>4} | {'p^2-1':>8} | {'Factorization':>28} | {'tau':>5} | {'omega':>5} | "
          f"{'phi':>8} | {'Coverage':>8} | Full?")
    print("-" * 95)
    for row in analysis:
        print(f"{row['p']:4d} | {row['p2_minus_1']:8d} | {row['factorization']:>28} | "
              f"{row['tau']:5d} | {row['omega']:5d} | {row['phi']:8d} | "
              f"{row['coverage']:7.1f}% | {'YES' if row['full_coverage'] else ''}")
    print()

    # =====================================================================
    # Plot 1: Coverage vs p
    # =====================================================================
    fig, ax = plt.subplots(figsize=(12, 6))

    p_vals = [r['p'] for r in analysis]
    cov_vals = [r['coverage'] for r in analysis]
    full_mask = [r['full_coverage'] for r in analysis]

    # Plot non-full coverage primes
    non_full_p = [p for p, f in zip(p_vals, full_mask) if not f]
    non_full_c = [c for c, f in zip(cov_vals, full_mask) if not f]
    ax.scatter(non_full_p, non_full_c, c='#4472C4', s=60, edgecolors='navy',
               zorder=3, label='Partial coverage')

    # Plot full coverage primes
    full_p = [p for p, f in zip(p_vals, full_mask) if f]
    full_c = [c for c, f in zip(cov_vals, full_mask) if f]
    ax.scatter(full_p, full_c, c='#51CF66', s=100, edgecolors='darkgreen',
               zorder=4, marker='*', label='Full coverage (100%)')

    # Annotate the three special primes
    for p in [5, 7, 11]:
        ax.annotate(f'$p={p}$', (p, 100), textcoords="offset points",
                    xytext=(8, -5), fontsize=11, color='green', fontweight='bold')

    # Trend line
    p_arr = np.array(p_vals, dtype=float)
    c_arr = np.array(cov_vals, dtype=float)
    coeffs = np.polyfit(np.log(p_arr), c_arr, 1)
    p_smooth = np.linspace(4, 100, 200)
    ax.plot(p_smooth, np.polyval(coeffs, np.log(p_smooth)), 'r--', alpha=0.5,
            linewidth=1.5, label=f'Log trend')

    ax.axhline(y=100, color='green', linestyle=':', alpha=0.3)
    ax.set_xlabel('Prime $p$', fontsize=12)
    ax.set_ylabel('Coverage %', fontsize=12)
    ax.set_title('Q5: Cardinality Coverage vs Prime $p$\n'
                 'Only $p = 5, 7, 11$ achieve full coverage',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_ylim(60, 105)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q5_coverage_vs_p.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Coverage vs p saved to output/plots/q5_coverage_vs_p.png")

    # =====================================================================
    # Plot 2: Coverage vs number of divisors of p^2-1
    # =====================================================================
    fig, ax = plt.subplots(figsize=(10, 6))

    for row in analysis:
        color = '#51CF66' if row['full_coverage'] else '#4472C4'
        marker = '*' if row['full_coverage'] else 'o'
        size = 100 if row['full_coverage'] else 50
        ax.scatter(row['tau'], row['coverage'], c=color, s=size,
                   edgecolors='navy', zorder=3, marker=marker)
        ax.annotate(str(row['p']), (row['tau'], row['coverage']),
                    textcoords="offset points", xytext=(4, 4), fontsize=8)

    ax.axhline(y=100, color='green', linestyle=':', alpha=0.3)
    ax.set_xlabel(r'$\tau(p^2 - 1)$ (number of divisors)', fontsize=12)
    ax.set_ylabel('Coverage %', fontsize=12)
    ax.set_title(r'Q5: Coverage vs Divisor Count $\tau(p^2-1)$',
                 fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q5_coverage_vs_divisors.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Coverage vs divisors saved to output/plots/q5_coverage_vs_divisors.png")

    # =====================================================================
    # Plot 3: Factorization table as figure
    # =====================================================================
    fig, ax = plt.subplots(figsize=(16, max(6, len(primes) * 0.35)))
    ax.axis('off')
    ax.set_title(r'Q5: Factorization of $p^2 - 1$ and Coverage',
                 fontsize=14, fontweight='bold', pad=20)

    col_labels = ['$p$', '$p^2-1$', 'Factorization', r'$\tau$', r'$\omega$',
                  r'$\varphi$', 'Coverage %']
    cell_text = []
    cell_colors = []
    for row in analysis:
        cell_text.append([
            str(row['p']),
            str(row['p2_minus_1']),
            row['factorization'],
            str(row['tau']),
            str(row['omega']),
            str(row['phi']),
            f"{row['coverage']:.1f}%"
        ])
        if row['full_coverage']:
            cell_colors.append(['#C6EFCE'] * 7)
        else:
            cell_colors.append(['white' if i % 2 == 0 else '#F2F2F2'
                                for i in range(7)])

    table = ax.table(cellText=cell_text, colLabels=col_labels,
                     cellLoc='center', loc='center',
                     cellColours=cell_colors)
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.3)

    # Header styling
    for j in range(len(col_labels)):
        table[0, j].set_facecolor('#4472C4')
        table[0, j].set_text_props(color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q5_factorization_table.png'),
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Factorization table saved to output/plots/q5_factorization_table.png")

    # =====================================================================
    # Additional analysis: ratio (p-1) / tau(p^2-1)
    # =====================================================================
    print()
    print("Ratio analysis: (p-1) / tau(p^2-1)")
    print(f"{'p':>4} | {'p-1':>5} | {'tau':>5} | {'ratio':>8} | Full?")
    print("-" * 40)
    for row in analysis:
        ratio = (row['p'] - 1) / row['tau']
        print(f"{row['p']:4d} | {row['p']-1:5d} | {row['tau']:5d} | "
              f"{ratio:8.3f} | {'YES' if row['full_coverage'] else ''}")

    print()
    print("Key observation: p=5,7,11 have the smallest p^2-1 values")
    print("with relatively few prime factors, making it more likely")
    print("that the orbit structure of t -> t^n on the cyclic group")
    print("of order p^2-1 produces all possible cardinality values.")
    print("\nDone.")


if __name__ == '__main__':
    main()
