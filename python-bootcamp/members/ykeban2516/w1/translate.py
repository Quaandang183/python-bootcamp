def transpose(matrix):
    if not matrix:
        return []

    return [
        [matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]
