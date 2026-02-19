"""Shared Dickson polynomial implementations.

Notation convention used in this repository:
- Reversed Dickson form is written as D_n(a, x).
- Canonical research focus is D_n(1, x), i.e. reversed form with a=1.

Supported variants
------------------
1) Reversed first-kind Dickson polynomial:
   D_0(a, x) = 2,
   D_1(a, x) = a,
   D_n(a, x) = a D_{n-1}(a, x) - x D_{n-2}(a, x)  (n >= 2).

2) Classical first-kind Dickson polynomial:
   E_0(x, a) = 2,
   E_1(x, a) = x,
   E_n(x, a) = x E_{n-1}(x, a) - a E_{n-2}(x, a)  (n >= 2).
"""


def reversed_dickson(n: int, a: int, x: int, modulus: int | None = None) -> int:
    """Evaluate reversed Dickson polynomial D_n(a, x).

    Formula:
        D_0(a, x) = 2,
        D_1(a, x) = a,
        D_n(a, x) = a D_{n-1}(a, x) - x D_{n-2}(a, x).

    If ``modulus`` is given, arithmetic is performed modulo ``modulus``.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    if modulus is not None:
        a %= modulus
        x %= modulus

    if n == 0:
        return 2 % modulus if modulus else 2
    if n == 1:
        return a % modulus if modulus else a

    prev2, prev1 = 2, a
    for _ in range(2, n + 1):
        cur = a * prev1 - x * prev2
        if modulus is not None:
            cur %= modulus
        prev2, prev1 = prev1, cur

    return prev1


def reversed_dickson_d1(n: int, x: int, modulus: int) -> int:
    """Evaluate canonical repository variant D_n(1, x) modulo ``modulus``.

    This is a thin wrapper around ``reversed_dickson`` with ``a=1``.
    """
    return reversed_dickson(n=n, a=1, x=x, modulus=modulus)


def classical_dickson(n: int, x: int, a: int, modulus: int | None = None) -> int:
    """Evaluate classical first-kind Dickson polynomial E_n(x, a).

    Formula:
        E_0(x, a) = 2,
        E_1(x, a) = x,
        E_n(x, a) = x E_{n-1}(x, a) - a E_{n-2}(x, a).

    If ``modulus`` is given, arithmetic is performed modulo ``modulus``.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    if modulus is not None:
        a %= modulus
        x %= modulus

    if n == 0:
        return 2 % modulus if modulus else 2
    if n == 1:
        return x % modulus if modulus else x

    prev2, prev1 = 2, x
    for _ in range(2, n + 1):
        cur = x * prev1 - a * prev2
        if modulus is not None:
            cur %= modulus
        prev2, prev1 = prev1, cur

    return prev1


def reversed_value_set(n: int, p: int, a: int = 1) -> set[int]:
    """Return value set {D_n(a, x) : x in F_p} for reversed variant."""
    return {reversed_dickson(n=n, a=a, x=x, modulus=p) for x in range(p)}
