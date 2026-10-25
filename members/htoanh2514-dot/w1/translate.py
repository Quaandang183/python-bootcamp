"""Module for prime number generation using algorithms such as the Sieve of Eratosthenes."""


def sieve_of_eratosthenes(n: int) -> list[int]:
    """Generate all prime numbers up to a given integer n using the Sieve of Eratosthenes.

    Args:
        n (int): The upper limit integer up to which prime numbers are calculated.

    Returns:
        list[int]: A list of prime numbers less than or equal to n.
    """
    if n < 2:
        return []

    # Initialize a boolean array marking all numbers up to n as potentially prime
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    # Mark composite numbers starting from p^2 up to n
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False

    # Collect all indices that remain marked as prime
    return [p for p in range(2, n + 1) if is_prime[p]]