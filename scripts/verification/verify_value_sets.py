"""Verification for the canonical reversed Dickson variant D_n(1, x)."""

from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.append(str(SCRIPT_ROOT))

from utilities.dickson import reversed_dickson_d1


def reversed_dickson_polynomial(n, x, p):
    """Compute D_n(1, x) mod p via shared reversed recurrence."""
    return reversed_dickson_d1(n=n, x=x, modulus=p)


def compute_value_set(n, p):
    """
    Compute the value set of D_n(1, x) for all x in F_p.
    Returns sorted list of unique values.
    """
    values = set()
    for x in range(p):
        value = reversed_dickson_polynomial(n, x, p)
        values.add(value)
    return sorted(values)


def verify_for_prime(p):
    """Verify the three cardinality-2 indices for a specific prime p."""
    n1 = p**2 - 1
    n2 = (p**2 + 1) // 2
    n3 = (p**2 + 2*p - 1) // 2

    results = {
        'n1': {'n': n1, 'expected': [1, 2], 'actual': compute_value_set(n1, p)},
        'n2': {'n': n2, 'expected': [1, p-1], 'actual': compute_value_set(n2, p)},
        'n3': {'n': n3, 'expected': [1, p-1], 'actual': compute_value_set(n3, p)}
    }

    return results


def main():
    print("=" * 70)
    print("Verification of Dickson Polynomial Value Sets with Cardinality 2")
    print("=" * 70)

    test_primes = [5, 7, 11, 13, 17, 19, 23, 29]

    all_passed = True

    for p in test_primes:
        print(f"\nPrime p = {p}:")
        print("-" * 50)

        results = verify_for_prime(p)

        for case_name, data in results.items():
            n = data['n']
            expected = sorted(data['expected'])
            actual = sorted(data['actual'])
            passed = (expected == actual)

            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {case_name}: n = {n}")
            print(f"    Expected: {expected}")
            print(f"    Actual:   {actual}")
            print(f"    Status: {status}")

            if not passed:
                all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("The theoretical formulas correctly predict the value sets!")
    else:
        print("✗ SOME TESTS FAILED")
        print("There may be an issue with the formulas or implementation.")
    print("=" * 70)


if __name__ == "__main__":
    main()