"""
Q3: The polynomial is a permutation polynomial if and only if the
cardinality of the value set equals p. Anything interesting in this case?

Analyzes which indices n make D_n(x,1) a permutation polynomial over F_p.
Tests the known criterion: D_n(x,a) is a permutation poly iff gcd(n, p^2-1) = 1.
"""

import pandas as pd
import math
import os


def main():
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reversed_dickson_values.csv')
    df = pd.read_csv(csv_path)

    print("=" * 70)
    print("Q3: Permutation Polynomial Index Analysis")
    print("    D_n(x,1) is a permutation poly iff value set has cardinality p")
    print("=" * 70)
    print()

    all_results = []

    for p in sorted(df['p'].unique()):
        if p <= 3:
            continue

        sub = df[df['p'] == p]
        perm_indices = sorted(sub[sub['is_permutation'] == True]['n'].tolist())
        total_indices = p * p  # n ranges from 0 to p^2-1
        period = p * p - 1

        # Test gcd criterion: D_n is permutation iff gcd(n, p^2-1) = 1
        gcd_predicted = sorted([n for n in range(total_indices) if math.gcd(n, period) == 1])

        gcd_match = (set(perm_indices) == set(gcd_predicted))

        # Euler's totient of p^2 - 1 gives expected count
        # phi(p^2-1) = number of integers in [1, p^2-2] coprime to p^2-1
        # But we also include n=0 check: gcd(0, p^2-1) = p^2-1 != 1, so n=0 is not a permutation
        expected_count = sum(1 for n in range(total_indices) if math.gcd(n, period) == 1)

        density = len(perm_indices) / total_indices * 100 if total_indices > 0 else 0

        result = {
            'p': p,
            'count': len(perm_indices),
            'total': total_indices,
            'density': density,
            'gcd_criterion_holds': gcd_match,
            'expected_by_gcd': expected_count,
            'first_few': perm_indices[:10],
        }
        all_results.append(result)

        print(f"Prime p = {p} (p^2 = {p*p}, period = {period})")
        print(f"  Permutation indices count: {len(perm_indices)}")
        print(f"  Expected by gcd(n, p^2-1)=1: {expected_count}")
        print(f"  gcd criterion matches: {gcd_match}")
        print(f"  Density: {density:.2f}%")
        print(f"  First few indices: {perm_indices[:10]}")

        if not gcd_match:
            data_not_gcd = set(perm_indices) - set(gcd_predicted)
            gcd_not_data = set(gcd_predicted) - set(perm_indices)
            if data_not_gcd:
                print(f"  In data but NOT predicted by gcd: {sorted(data_not_gcd)[:10]}")
            if gcd_not_data:
                print(f"  Predicted by gcd but NOT in data: {sorted(gcd_not_data)[:10]}")
        print()

    # === Summary ===
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()

    all_match = all(r['gcd_criterion_holds'] for r in all_results)
    print(f"gcd(n, p^2-1) = 1 criterion holds for ALL primes: {all_match}")
    print()

    print("Permutation count and density by prime:")
    print(f"{'p':>5}  {'count':>8}  {'total':>8}  {'density':>8}  {'phi/total':>10}")
    print("-" * 45)
    for r in all_results:
        euler_ratio = r['expected_by_gcd'] / r['total'] * 100
        print(f"{r['p']:5d}  {r['count']:8d}  {r['total']:8d}  {r['density']:7.2f}%  {euler_ratio:9.2f}%")
    print()

    # Euler product formula: phi(n)/n = prod_{p|n} (1 - 1/p)
    # For p^2 - 1 = (p-1)(p+1), the density should relate to this
    print("Note: The density of permutation indices equals phi(p^2-1)/(p^2-1),")
    print("which is the Euler product over prime factors of p^2-1 = (p-1)(p+1).")
    print()

    # Factor p^2-1 for each prime
    print("Factorization of p^2 - 1:")
    for r in all_results:
        p = r['p']
        n = p * p - 1
        factors = []
        temp = n
        for f in range(2, int(math.sqrt(temp)) + 1):
            while temp % f == 0:
                factors.append(f)
                temp //= f
            if temp == 1:
                break
        if temp > 1:
            factors.append(temp)
        print(f"  p={p:3d}: p^2-1 = {n} = {' * '.join(map(str, factors))}")

    # Save results
    out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'q3_permutation_indices.txt')

    with open(out_path, 'w') as f:
        f.write("Permutation Polynomial Index Analysis\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"gcd(n, p^2-1) = 1 criterion holds for all primes: {all_match}\n\n")
        for r in all_results:
            f.write(f"p={r['p']}: count={r['count']}, density={r['density']:.2f}%, "
                    f"gcd_match={r['gcd_criterion_holds']}\n")
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    main()
