"""Insertion sort algorithm implementation translated from C++."""


def insertion_sort(arr: list[int]) -> list[int]:
    """Sort a list of integers in ascending order using insertion sort.

    Args:
        arr: The list of integers to sort.

    Returns:
        The sorted list (modified in-place and returned).
    """
    result = list(arr)
    n = len(result)
    for i in range(1, n):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


if __name__ == "__main__":
    sample = [3, 1, 2]
    print("Mảng sau khi sắp xếp:", insertion_sort(sample))
