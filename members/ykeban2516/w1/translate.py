"""Matrix manipulation tools translated to Python."""


def transpose(matrix):
    """Transpose a 2D matrix using list comprehensions.

    Args:
        matrix: A 2D list of elements representing rows and columns.

    Returns:
        The transposed 2D list where rows and columns are swapped.
    """
    if not matrix:
        return []

    return [
        [matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]

