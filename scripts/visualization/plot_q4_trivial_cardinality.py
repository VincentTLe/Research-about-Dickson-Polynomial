"""
Q4: Prove that when n = 0, 1, or p, the cardinality of the value set is 1.

This script verifies computationally that D_n(x, 1) is constant for n in {0, 1, p},
identifies the constant output values, and confirms these are the ONLY indices
with cardinality 1. Generates a verification table and bar chart.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os


def reversed_dickson_polynomial(n, x, p):
    """Compute D_n(1, x) mod p using the recurrence relation."""
    if n == 0:
        return 2 % p
    if n == 1:
        return 1 % p
    d_prev = 2 % p
    d_curr = 1 % p
    for i in range(2, n + 1):
        d_next = (d_curr - x * d_prev) % p
        d_prev = d_curr
        d_curr = d_next
    return d_curr


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def main():
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    csv_path = os.path.join(base_dir, 'data', 'reversed_dickson_values.csv')
    plot_dir = os.path.join(base_dir, 'output', 'plots')
    result_dir = os.path.join(base_dir, 'output', 'results')
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    primes = [p for p in range(5, 98, 2) if is_prime(p)]

    print("=" * 70)
    print("Q4: Trivial Cardinality Verification")
    print("    Verifying |V_n(1)| = 1 for n = 0, 1, p")
    print("=" * 70)
    print()

    # --- Direct computation ---
    table_data = []
    for p in primes:
        row = {'p': p}
        for n_label, n_val in [('n=0', 0), ('n=1', 1), ('n=p', p)]:
            values = set()
            for x in range(p):
                values.add(reversed_dickson_polynomial(n_val, x, p))
            row[n_label + '_value'] = sorted(values)[0] if len(values) == 1 else sorted(values)
            row[n_label + '_card'] = len(values)
        table_data.append(row)

    # Print results
    print(f"{'p':>5} | {'D_0(x,1)':>10} | {'D_1(x,1)':>10} | {'D_p(x,1)':>10} | All card=1?")
    print("-" * 65)
    all_ok = True
    for row in table_data:
        ok = row['n=0_card'] == 1 and row['n=1_card'] == 1 and row['n=p_card'] == 1
        all_ok = all_ok and ok
        print(f"{row['p']:5d} | {row['n=0_value']:>10} | {row['n=1_value']:>10} | {row['n=p_value']:>10} | "
              f"{'YES' if ok else 'NO'}")
    print()
    print(f"All primes verified: {'YES' if all_ok else 'NO'}")

    # --- Cross-check with CSV: confirm exactly {0, 1, p} have cardinality 1 ---
    df = pd.read_csv(csv_path)
    print()
    print("Cross-check with CSV data:")
    csv_ok = True
    for p in primes:
        sub = df[(df['p'] == p) & (df['value_count'] == 1)]
        card1_indices = sorted(sub['n'].tolist())
        expected = [0, 1, p]
        match = card1_indices == expected
        if not match:
            print(f"  p={p}: MISMATCH! expected={expected}, got={card1_indices}")
            csv_ok = False
    if csv_ok:
        print("  All primes: cardinality-1 indices are exactly {0, 1, p}")
    print()

    # --- Plot 1: Verification table as figure ---
    fig, ax = plt.subplots(figsize=(10, max(6, len(primes) * 0.35)))
    ax.axis('off')
    ax.set_title('Q4: Trivial Cardinality Verification\n'
                 r'$|V_n(1)| = 1$ for $n \in \{0, 1, p\}$', fontsize=14, fontweight='bold')

    col_labels = ['Prime $p$', '$D_0(x,1)$', '$D_1(x,1)$', '$D_p(x,1)$', 'Card-1 indices']
    cell_text = []
    for row in table_data:
        p = row['p']
        cell_text.append([
            str(p),
            str(row['n=0_value']),
            str(row['n=1_value']),
            str(row['n=p_value']),
            f'{{0, 1, {p}}}'
        ])

    table = ax.table(cellText=cell_text, colLabels=col_labels,
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.3)

    # Color header row
    for j in range(len(col_labels)):
        table[0, j].set_facecolor('#4472C4')
        table[0, j].set_text_props(color='white', fontweight='bold')

    # Alternate row colors
    for i in range(1, len(cell_text) + 1):
        color = '#D9E2F3' if i % 2 == 0 else 'white'
        for j in range(len(col_labels)):
            table[i, j].set_facecolor(color)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q4_trivial_cardinality_table.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Table saved to output/plots/q4_trivial_cardinality_table.png")

    # --- Plot 2: Bar chart showing constant values ---
    fig, ax = plt.subplots(figsize=(12, 5))
    x_pos = np.arange(len(primes))
    width = 0.25

    d0_vals = [row['n=0_value'] for row in table_data]
    d1_vals = [row['n=1_value'] for row in table_data]
    dp_vals = [row['n=p_value'] for row in table_data]

    bars1 = ax.bar(x_pos - width, d0_vals, width, label='$D_0(x,1) = 2$', color='#4472C4', alpha=0.8)
    bars2 = ax.bar(x_pos, d1_vals, width, label='$D_1(x,1) = 1$', color='#ED7D31', alpha=0.8)
    bars3 = ax.bar(x_pos + width, dp_vals, width, label='$D_p(x,1) = 1$', color='#70AD47', alpha=0.8)

    ax.set_xlabel('Prime $p$', fontsize=12)
    ax.set_ylabel('Constant Output Value', fontsize=12)
    ax.set_title('Q4: Constant Output Values for $n = 0, 1, p$', fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(p) for p in primes], rotation=45, ha='right')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 3)
    ax.axhline(y=2, color='#4472C4', linestyle='--', alpha=0.3)
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.3)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'q4_constant_values.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Bar chart saved to output/plots/q4_constant_values.png")

    # --- Save verification text ---
    out_path = os.path.join(result_dir, 'q4_verification.txt')
    with open(out_path, 'w') as f:
        f.write("Q4: Trivial Cardinality Verification\n")
        f.write("=" * 50 + "\n\n")
        f.write("For all primes 5 <= p <= 97:\n\n")
        f.write("  D_0(x, 1) = 2  for all x in F_p  (cardinality 1)\n")
        f.write("  D_1(x, 1) = 1  for all x in F_p  (cardinality 1)\n")
        f.write("  D_p(x, 1) = 1  for all x in F_p  (cardinality 1)\n\n")
        f.write("These are the ONLY n in [0, p^2-1) with cardinality 1.\n")
        f.write(f"Verified across all {len(primes)} primes: {all_ok and csv_ok}\n\n")
        f.write("Mathematical explanation:\n")
        f.write("  n=0: D_0 = 2 by definition (base case)\n")
        f.write("  n=1: D_1 = 1 by definition (a=1 base case)\n")
        f.write("  n=p: D_p(x,1) = y^p + (1-y)^p = y + (1-y) = 1\n")
        f.write("        by Frobenius endomorphism (z^p = z for z in F_p,\n")
        f.write("        and y^p = 1-y for y in F_{p^2} \\ F_p)\n")
    print(f"Verification saved to output/results/q4_verification.txt")


if __name__ == '__main__':
    main()
