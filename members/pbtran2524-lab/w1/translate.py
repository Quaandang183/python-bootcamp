"""Euclidean algorithm module for computing the Greatest Common Divisor (GCD).

This module provides a function to calculate the GCD of two integers using
the Euclidean algorithm, along with a command-line interface for user input.
"""


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor (GCD) using the Euclidean algorithm.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The greatest common divisor of `a` and `b`. Returns a positive integer.
            If `a` or `b` is negative, the returned value remains non-negative.
    """
    while b != 0:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    try:
        raw_input = input("Enter two integers a and b (separated by a space): ").strip()
        num_a, num_b = map(int, raw_input.split())

        result = gcd(num_a, num_b)
        print(f"The greatest common divisor GCD({num_a}, {num_b}) is: {result}")
    except ValueError:
        print("Error: Please enter two valid integers!")