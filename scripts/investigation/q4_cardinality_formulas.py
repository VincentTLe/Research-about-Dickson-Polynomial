"""
Q4: Given a prime p, what about the indices for which the cardinality
of the value set is 1, 3, 4, etc.? Are there similar patterns?

For each cardinality c, we look at:
- How many indices per prime have that cardinality
- Whether the count is consistent across primes
- Whether polynomial formulas can predict those indices (like cardinality 2)
"""

import pandas as pd
import numpy as np
import math
import os


def pretty_poly_str(coeffs):
    """Creates a human-readable string for a polynomial from its coefficients."""
    parts = []
    for i, c in enumerate(coeffs):
        if abs(c) < 1e-9:
            continue
        power = len(coeffs) - 1 - i
        term = f"{c:.4f}"
        if power > 0:
            term += "*p"
        if power > 1:
            term += f"^{power}"
        parts.append(term)
    return " + ".join(parts).replace(" + -", " - ")


def try_rational_formula(ps, ns):
    """Try to express n as a simple rational function of p.
    Tests: n = (a*p^2 + b*p + c) / d for small d."""
    ps = np.array(ps, dtype=float)
    ns = np.array(ns, dtype=float)

    best = None
    for d in [1, 2, 3, 4, 6]:
        # Fit: d*n = a*p^2 + b*p + c
        target = d * ns
        coeffs = np.polyfit(ps, target, 2)
        pred = np.polyval(coeffs, ps)
        rmse = np.sqrt(np.mean((target - pred) ** 2))
        if rmse < 0.01:
            # Round coefficients to check if they're integers
            rounded = [round(c) for c in coeffs]
            check = np.polyval(rounded, ps)
            rmse2 = np.sqrt(np.mean((target - check) ** 2))
            if rmse2 < 0.01:
                a, b, c = rounded
                if d == 1:
                    formula = f"n = {a}p^2 + {b}p + {c}".replace("+ -", "- ")
                else:
                    formula = f"n = ({a}p^2 + {b}p + {c})/{d}".replace("+ -", "- ")
                if best is None or d == 1:
                    best = (formula, rmse2, d, rounded)
    return best


def main():
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reversed_dickson_values.csv')
    df = pd.read_csv(csv_path)

    # Only consider p > 3
    df = df[df['p'] > 3].copy()

    primes = sorted(df['p'].unique())

    print("=" * 70)
    print("Q4: Cardinality-Specific Index Formula Analysis")
    print("    For each cardinality c, find patterns in the indices")
    print("=" * 70)
    print()

    # Get all cardinalities that appear
    all_cards = sorted(df['value_count'].unique())
    print(f"Cardinalities observed across all primes: {all_cards}")
    print()

    results_text = []

    for c in all_cards:
        card_df = df[df['value_count'] == c]
        primes_with_c = sorted(card_df['p'].unique())

        # Count per prime
        counts_per_prime = {}
        indices_per_prime = {}
        for p in primes_with_c:
            indices = sorted(card_df[card_df['p'] == p]['n'].tolist())
            counts_per_prime[p] = len(indices)
            indices_per_prime[p] = indices

        count_values = sorted(set(counts_per_prime.values()))
        consistent = len(count_values) == 1

        print("=" * 60)
        print(f"CARDINALITY = {c}")
        print("=" * 60)
        print(f"  Appears for {len(primes_with_c)}/{len(primes)} primes (p > 3)")
        print(f"  Count per prime: {dict(counts_per_prime)}")

        if consistent:
            print(f"  ** CONSISTENT: always {count_values[0]} indices per prime **")
        else:
            print(f"  Variable count per prime: {count_values}")
        print()

        # Show indices for small primes
        for p in primes_with_c[:5]:
            print(f"  p={p}: indices = {indices_per_prime[p][:20]}"
                  + ("..." if len(indices_per_prime[p]) > 20 else ""))

        # Try polynomial regression if count is consistent and small
        if consistent and count_values[0] <= 10 and len(primes_with_c) >= 4:
            num_indices = count_values[0]
            print(f"\n  Attempting formula derivation ({num_indices} indices per prime):")

            # Sort indices for each prime and try formula for each position
            for pos in range(num_indices):
                pairs = []
                for p in primes_with_c:
                    idx_list = indices_per_prime[p]
                    if pos < len(idx_list):
                        pairs.append((p, idx_list[pos]))

                if len(pairs) >= 3:
                    ps_arr = np.array([x[0] for x in pairs], dtype=float)
                    ns_arr = np.array([x[1] for x in pairs], dtype=float)

                    # Try degree 2 polynomial
                    coeffs = np.polyfit(ps_arr, ns_arr, 2)
                    pred = np.polyval(coeffs, ps_arr)
                    rmse = np.sqrt(np.mean((ns_arr - pred) ** 2))

                    poly_str = pretty_poly_str(coeffs)
                    print(f"    Index #{pos+1}: n(p) = {poly_str}")
                    print(f"      RMSE = {rmse:.6f}{'  ** EXACT **' if rmse < 0.01 else ''}")

                    # Try rational formula
                    rational = try_rational_formula(
                        [x[0] for x in pairs], [x[1] for x in pairs])
                    if rational:
                        formula, r_rmse, d, rounded_coeffs = rational
                        print(f"      Rational formula: {formula} (RMSE={r_rmse:.6f})")

        # For cardinality 1: check what value set it is
        if c == 1:
            print(f"\n  Value sets for cardinality 1:")
            for p in primes_with_c[:5]:
                sub = card_df[card_df['p'] == p][['n', 'values']].head(10)
                for _, row in sub.iterrows():
                    print(f"    p={p}, n={row['n']}: values={row['values']}")

        # Check relationship to gcd(n, p^2-1)
        if c <= 5 and len(primes_with_c) >= 3:
            print(f"\n  gcd(n, p^2-1) analysis:")
            for p in primes_with_c[:5]:
                period = p * p - 1
                for n in indices_per_prime[p][:5]:
                    g = math.gcd(n, period)
                    print(f"    p={p}, n={n}: gcd(n, p^2-1) = gcd({n}, {period}) = {g}, "
                          f"(p^2-1)/gcd = {period // g}")

        print()

    # Save results
    out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'q4_cardinality_formulas.txt')

    # Re-run summary to file
    with open(out_path, 'w') as f:
        f.write("Cardinality-Specific Index Formula Analysis\n")
        f.write("=" * 50 + "\n\n")
        for c in all_cards:
            card_df = df[df['value_count'] == c]
            primes_with_c = sorted(card_df['p'].unique())
            counts = {}
            for p in primes_with_c:
                counts[p] = len(card_df[card_df['p'] == p])
            count_vals = sorted(set(counts.values()))
            f.write(f"Cardinality {c}: appears for {len(primes_with_c)} primes, "
                    f"count per prime = {count_vals}\n")
    print(f"Results saved to {out_path}")


if __name__ == '__main__':
    main()
