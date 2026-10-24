def transpose(matrix):
    """Transpose a matrix using list comprehensions."""
    if not matrix:
        return []

    return [
        [matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]
