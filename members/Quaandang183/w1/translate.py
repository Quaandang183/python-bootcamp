"""W1-4: binary search translated from C++.

Difference from C++:
In Python, the division operator '/' always returns a float. To perform
integer division (like in C++), we must use the floor division operator '//'.
"""


def binary_search(a: list[int], key: int) -> int:
    """Return the index of ``key`` in the sorted list ``a``, or -1 if it is absent."""
    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if a[mid] == key:
            return mid
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1
