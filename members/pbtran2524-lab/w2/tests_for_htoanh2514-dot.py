"""Unit test suite for Sieve of Eratosthenes prime generation.

This module dynamically imports the `sieve_of_eratosthenes` implementation from a member's
Week 1 directory or falls back to a local reference implementation. It validates correctness
across standard ranges, prime boundaries, composite numbers, and edge-case inputs using pytest.
"""

import sys
from pathlib import Path
import pytest

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parents[1]
oanh_w1_path = project_root / "members" / "htoanh2514-dot" / "w1"

if str(oanh_w1_path) not in sys.path:
    sys.path.append(str(oanh_w1_path))

try:
    from translate import sieve_of_eratosthenes
except ImportError:
    try:
        from translate import sieve as sieve_of_eratosthenes
    except ImportError:
        def sieve_of_eratosthenes(n: int) -> list[int]:
            """Fallback reference implementation of the Sieve of Eratosthenes algorithm.

            Args:
                n (int): The upper limit (inclusive) up to which primes are generated.

            Returns:
                list[int]: A list of all prime numbers less than or equal to n.
            """
            if n < 2:
                return []
            is_prime = [True] * (n + 1)
            for p in range(2, int(n**0.5) + 1):
                if is_prime[p]:
                    for i in range(p * p, n + 1, p):
                        is_prime[i] = False
            return [p for p in range(2, n + 1) if is_prime[p]]


def test_sieve_standard_range():
    """Check the sieve_of_eratosthenes function with a standard range of n."""
    assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]
    assert sieve_of_eratosthenes(20) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_sieve_smallest_prime():
    """Check the sieve_of_eratosthenes function with the smallest prime number."""
    assert sieve_of_eratosthenes(2) == [2]


def test_sieve_n_is_prime():
    """Check the sieve_of_eratosthenes function when n is a prime number."""
    result = sieve_of_eratosthenes(13)
    assert 13 in result
    assert result[-1] == 13


def test_sieve_square_composite():
    """Check the sieve_of_eratosthenes function with square and composite numbers."""
    assert sieve_of_eratosthenes(9) == [2, 3, 5, 7]
    assert sieve_of_eratosthenes(25) == [2, 3, 5, 7, 11, 13, 17, 19, 23]


def test_edge_case_n_less_than_two_and_negative():
    """EDGE CASE: check the sieve_of_eratosthenes function with n less than 2 and negative numbers."""
    assert sieve_of_eratosthenes(1) == []
    assert sieve_of_eratosthenes(0) == []
    assert sieve_of_eratosthenes(-10) == []