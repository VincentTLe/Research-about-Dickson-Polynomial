"""
Q1: Given a prime p > 3, is the set of cardinalities of value sets
equal to all numbers from 1 through p-1?

For each prime, we check which cardinalities actually appear among
all indices n in [0, p^2-2] and report any gaps.
"""

import pandas as pd
import os

def main():
    # Load existing data
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reversed_dickson_values.csv')
    df = pd.read_csv(csv_path)

    results = []
    print("=" * 70)
    print("Q1: Cardinality Coverage Analysis")
    print("    For each prime p > 3, does every cardinality 1..p-1 appear?")
    print("=" * 70)
    print()

    for p in sorted(df['p'].unique()):
        if p <= 3:
            continue

        sub = df[df['p'] == p]
        observed = set(sub['value_count'].unique())
        expected = set(range(1, p))  # {1, 2, ..., p-1}
        full_range = set(range(1, p + 1))  # {1, 2, ..., p} including permutation case

        missing_from_expected = sorted(expected - observed)
        extra = sorted(observed - expected)  # cardinality p if it appears
        has_permutations = p in observed
        coverage = len(expected & observed) / len(expected) * 100

        results.append({
            'p': p,
            'observed': sorted(observed),
            'missing': missing_from_expected,
            'has_permutations': has_permutations,
            'coverage_pct': coverage,
            'num_missing': len(missing_from_expected),
        })

        print(f"Prime p = {p}")
        print(f"  Expected cardinalities: 1 through {p-1}")
        print(f"  Observed cardinalities: {sorted(observed)}")
        if missing_from_expected:
            print(f"  MISSING from {{1..{p-1}}}: {missing_from_expected}")
        else:
            print(f"  All cardinalities 1..{p-1} are present!")
        print(f"  Has permutation indices (card = {p}): {has_permutations}")
        print(f"  Coverage of {{1..{p-1}}}: {coverage:.1f}%")
        print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = len(results)
    full_coverage = sum(1 for r in results if r['num_missing'] == 0)
    print(f"Total primes analyzed (p > 3): {total}")
    print(f"Primes with full coverage (all of 1..p-1): {full_coverage}/{total}")
    print(f"Primes with gaps: {total - full_coverage}/{total}")
    print()

    if total - full_coverage > 0:
        print("Primes with missing cardinalities:")
        for r in results:
            if r['num_missing'] > 0:
                print(f"  p = {r['p']}: missing {r['missing']}")
    print()

    # Check if cardinality p always appears (permutation case)
    all_have_perms = all(r['has_permutations'] for r in results)
    print(f"Every prime has at least one permutation index: {all_have_perms}")

    # Save results
    out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'q1_cardinality_coverage.txt')

    with open(out_path, 'w') as f:
        for r in results:
            f.write(f"p={r['p']}: observed={r['observed']}, missing={r['missing']}, "
                    f"coverage={r['coverage_pct']:.1f}%, permutations={r['has_permutations']}\n")
        f.write(f"\nFull coverage: {full_coverage}/{total} primes\n")
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    main()
