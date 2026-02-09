"""
Q2: If the cardinality of the value set does not take on a particular
value for a given p, is there a pattern for such values?

Analyzes missing cardinalities across all primes and looks for patterns:
- Relationship to divisors of p-1 and p+1
- Dependence on p mod 4, p mod 6
- Even/odd patterns
"""

import pandas as pd
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


def main():
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reversed_dickson_values.csv')
    df = pd.read_csv(csv_path)

    print("=" * 70)
    print("Q2: Missing Cardinality Pattern Analysis")
    print("=" * 70)
    print()

    missing_data = {}  # p -> list of missing cardinalities

    for p in sorted(df['p'].unique()):
        if p <= 3:
            continue
        sub = df[df['p'] == p]
        observed = set(sub['value_count'].unique())
        expected = set(range(1, p))
        missing = sorted(expected - observed)
        if missing:
            missing_data[p] = missing

    if not missing_data:
        print("No missing cardinalities found for any prime p > 3!")
        print("Every cardinality from 1 to p-1 appears for all primes tested.")
        return

    # === Analysis 1: Which cardinalities are most commonly missing? ===
    print("=" * 50)
    print("1. Missing cardinalities by prime")
    print("=" * 50)
    for p, missing in sorted(missing_data.items()):
        print(f"  p = {p:3d}: missing = {missing}")
    print()

    # === Analysis 2: Frequency of each missing cardinality ===
    from collections import Counter
    all_missing = []
    for p, missing in missing_data.items():
        all_missing.extend(missing)
    freq = Counter(all_missing)

    print("=" * 50)
    print("2. Most frequently missing cardinalities")
    print("=" * 50)
    for card, count in freq.most_common():
        primes_missing_it = [p for p, m in missing_data.items() if card in m]
        print(f"  Cardinality {card}: missing for {count} prime(s) -> {primes_missing_it}")
    print()

    # === Analysis 3: Divisor relationships ===
    print("=" * 50)
    print("3. Divisor relationship analysis")
    print("=" * 50)
    for p, missing in sorted(missing_data.items()):
        divs_pm1 = divisors(p - 1)
        divs_pp1 = divisors(p + 1)
        divs_p2m1 = divisors(p * p - 1)
        for m in missing:
            in_pm1 = m in divs_pm1
            in_pp1 = m in divs_pp1
            in_p2m1 = m in divs_p2m1
            print(f"  p={p:3d}, missing card={m:3d}: "
                  f"divides(p-1)={in_pm1}, divides(p+1)={in_pp1}, "
                  f"divides(p^2-1)={in_p2m1}")
    print()

    # === Analysis 4: Even/odd pattern ===
    print("=" * 50)
    print("4. Even/odd pattern of missing cardinalities")
    print("=" * 50)
    even_count = sum(1 for m in all_missing if m % 2 == 0)
    odd_count = sum(1 for m in all_missing if m % 2 == 1)
    print(f"  Even missing cardinalities: {even_count}")
    print(f"  Odd missing cardinalities:  {odd_count}")
    print()

    # === Analysis 5: p mod 4 and p mod 6 ===
    print("=" * 50)
    print("5. Missing cardinalities by p mod 4 and p mod 6")
    print("=" * 50)
    for mod_val, mod_name in [(4, "p mod 4"), (6, "p mod 6")]:
        groups = {}
        for p, missing in missing_data.items():
            r = p % mod_val
            if r not in groups:
                groups[r] = []
            groups[r].append((p, missing))
        print(f"\n  {mod_name}:")
        for r in sorted(groups):
            print(f"    {mod_name} = {r}:")
            for p, missing in groups[r]:
                print(f"      p={p}: missing={missing}")
    print()

    # === Analysis 6: Missing as fraction of p ===
    print("=" * 50)
    print("6. Missing cardinalities as fractions of p")
    print("=" * 50)
    for p, missing in sorted(missing_data.items()):
        ratios = [f"{m}/{p}={m/p:.3f}" for m in missing]
        print(f"  p={p:3d}: {', '.join(ratios)}")
    print()

    # === Analysis 7: Relationship to (p+1)/2 and (p-1)/2 ===
    print("=" * 50)
    print("7. Relationship to (p+1)/2 and (p-1)/2")
    print("=" * 50)
    for p, missing in sorted(missing_data.items()):
        half_p_plus = (p + 1) // 2
        half_p_minus = (p - 1) // 2
        for m in missing:
            print(f"  p={p:3d}, missing={m:3d}: "
                  f"(p-1)/2={half_p_minus}, (p+1)/2={half_p_plus}, "
                  f"m=(p-1)/2? {m == half_p_minus}, m=(p+1)/2? {m == half_p_plus}")

    # Save results
    out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'q2_missing_patterns.txt')

    with open(out_path, 'w') as f:
        f.write("Missing Cardinality Patterns\n")
        f.write("=" * 40 + "\n\n")
        for p, missing in sorted(missing_data.items()):
            divs_pm1 = divisors(p - 1)
            f.write(f"p={p}: missing={missing}, divisors(p-1)={sorted(divs_pm1)}\n")
        f.write(f"\nTotal primes with gaps: {len(missing_data)}\n")
        f.write(f"Frequency of missing cardinalities: {dict(freq.most_common())}\n")
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    main()
