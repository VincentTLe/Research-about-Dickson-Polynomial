"""
Q5: You are working on the case where the parameter of the Dickson
polynomial is a=1. If you let the parameter a be any value from 0
through p, how does it change the results?

The reversed Dickson polynomial D_n(a, x) uses the recurrence:
  D_0 = 2
  D_1 = a
  D_n = a * D_{n-1} - x * D_{n-2}  (all mod p)

where x varies over F_p and a is the parameter (previously fixed at 1).

This script computes value sets for all primes 3..97, all a in {0,..,p-1},
and all n in {0,..,p^2-2}.
"""

import math
import os
import sys
from pathlib import Path

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
    period = p * p - 1  # p^2 - 1

    # D_0(a, x) = 2 for all x
    Dprev = [2 % p] * p
    # D_1(a, x) = a for all x
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
    primes = [p for p in range(3, 98, 2) if is_prime(p)]

    print("=" * 70)
    print("Q5: Parameter 'a' Variation Analysis")
    print("    Reversed Dickson polynomial D_n(a, x) for a = 0, 1, ..., p-1")
    print("=" * 70)
    print()

    out_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'q5_parameter_a_variation.txt')

    # Collect summary data
    summary_data = []  # (p, a, num_card2, num_perm, card2_indices, all_cardinalities)

    with open(out_path, 'w') as f:
        f.write("Q5: Parameter 'a' Variation Analysis\n")
        f.write("=" * 50 + "\n\n")

        for p in primes:
            print(f"Processing p = {p} ...", end=" ", flush=True)
            f.write(f"\n{'='*60}\n")
            f.write(f"Prime p = {p}\n")
            f.write(f"{'='*60}\n")

            for a in range(p):
                results = compute_value_sets(p, a)

                # Analyze results
                card2_indices = [r[0] for r in results if r[1] == 2]
                perm_indices = [r[0] for r in results if r[2]]
                all_cards = sorted(set(r[1] for r in results))
                num_card2 = len(card2_indices)
                num_perm = len(perm_indices)

                summary_data.append({
                    'p': p, 'a': a,
                    'num_card2': num_card2,
                    'num_perm': num_perm,
                    'card2_indices': card2_indices,
                    'all_cardinalities': all_cards,
                })

                f.write(f"\n  a = {a}:\n")
                f.write(f"    Cardinality 2 count: {num_card2}\n")
                if card2_indices:
                    f.write(f"    Cardinality 2 indices: {card2_indices}\n")
                f.write(f"    Permutation count: {num_perm}\n")
                f.write(f"    All observed cardinalities: {all_cards}\n")

            print("done")

    # === Print summary analysis ===
    print()
    print("=" * 70)
    print("SUMMARY ANALYSIS")
    print("=" * 70)
    print()

    # 1. How does the number of cardinality-2 indices change with a?
    print("1. Number of cardinality-2 indices by (p, a):")
    print(f"   {'p':>5} | {'a=0':>5}", end="")
    # Just show a=0,1,2 and last few for readability
    print(f" | {'a=1':>5} | {'a=2':>5} | ... | consistent?")
    print("   " + "-" * 50)

    for p in primes:
        if p <= 3:
            continue
        p_data = [d for d in summary_data if d['p'] == p]
        counts = [d['num_card2'] for d in p_data]
        c0 = counts[0] if len(counts) > 0 else '?'
        c1 = counts[1] if len(counts) > 1 else '?'
        c2 = counts[2] if len(counts) > 2 else '?'
        all_same = len(set(counts)) == 1
        unique_counts = sorted(set(counts))
        print(f"   {p:5d} | {c0:>5} | {c1:>5} | {c2:>5} | ... | "
              f"{'YES (all=' + str(counts[0]) + ')' if all_same else 'NO: ' + str(unique_counts)}")

    print()

    # 2. Does a=0 produce degenerate results?
    print("2. Special case a = 0:")
    for p in primes[:5]:
        p_a0 = [d for d in summary_data if d['p'] == p and d['a'] == 0]
        if p_a0:
            d = p_a0[0]
            print(f"   p={p}: cardinalities = {d['all_cardinalities']}, "
                  f"card2={d['num_card2']}, perms={d['num_perm']}")
    print()

    # 3. Check if the 3 cardinality-2 formulas hold for a=1
    print("3. Verification: cardinality-2 indices for a=1 match known formulas?")
    for p in primes:
        if p <= 3:
            continue
        p_a1 = [d for d in summary_data if d['p'] == p and d['a'] == 1]
        if p_a1:
            d = p_a1[0]
            expected = sorted([(p*p+1)//2, p*p-1, (p*p+2*p-1)//2])
            actual = sorted(d['card2_indices'])
            match = actual == expected
            if not match:
                print(f"   p={p}: MISMATCH! expected={expected}, got={actual}")
    print("   All a=1 cases match known formulas (or no mismatch printed).")
    print()

    # 4. Do quadratic residues / non-residues matter?
    print("4. Effect of a being a quadratic residue vs non-residue:")
    for p in primes[2:7]:  # A few sample primes
        if p <= 3:
            continue
        qr = set()
        for x in range(1, p):
            qr.add(pow(x, 2, p))
        nqr = set(range(1, p)) - qr

        qr_card2 = []
        nqr_card2 = []
        for d in summary_data:
            if d['p'] == p and d['a'] in qr:
                qr_card2.append(d['num_card2'])
            elif d['p'] == p and d['a'] in nqr:
                nqr_card2.append(d['num_card2'])

        print(f"   p={p}:")
        print(f"     QR  a values: card2 counts = {sorted(set(qr_card2))} "
              f"(from {len(qr_card2)} values)")
        print(f"     NQR a values: card2 counts = {sorted(set(nqr_card2))} "
              f"(from {len(nqr_card2)} values)")
    print()

    # 5. Number of permutation indices by a
    print("5. Number of permutation indices by a (sample primes):")
    for p in primes[2:7]:
        if p <= 3:
            continue
        p_data = [d for d in summary_data if d['p'] == p]
        perm_counts = [d['num_perm'] for d in p_data]
        unique_perm = sorted(set(perm_counts))
        print(f"   p={p}: permutation counts across all a: {unique_perm}")
        if len(unique_perm) == 1:
            print(f"     -> SAME for all a: {unique_perm[0]}")
        else:
            # Show which a values give different counts
            for cnt in unique_perm:
                a_vals = [d['a'] for d in p_data if d['num_perm'] == cnt]
                print(f"     -> {cnt} permutations for a = {a_vals[:10]}"
                      + ("..." if len(a_vals) > 10 else ""))
    print()

    # 6. Overall: does changing a change things at all?
    print("6. Overall: Does changing a affect cardinality-2 count?")
    changes_found = False
    for p in primes:
        if p <= 3:
            continue
        p_data = [d for d in summary_data if d['p'] == p]
        counts = set(d['num_card2'] for d in p_data)
        if len(counts) > 1:
            print(f"   p={p}: YES, card-2 count varies: {sorted(counts)}")
            changes_found = True
    if not changes_found:
        print("   No variation found — card-2 count is the same for all a for every prime!")
    print()

    print(f"Detailed results saved to {out_path}")


if __name__ == '__main__':
    main()
