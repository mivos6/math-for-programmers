def delta(u, v):
    return tuple(map(lambda pair : pair[0] - pair[1], zip(u, v)))


def vector_epsilon_equal(u, v, epsilon=1e-6):
    if not len(u) == len(v):
        return False

    return False not in [abs(d) < epsilon for d in delta(u, v)]


def matrix_epsilon_equal(m1, m2, epsilon=1e-6):
    if not len(m1) == len(m2):
        return False

    return False not in [
            vector_epsilon_equal(row1, row2, epsilon)
            for row1, row2 in zip(m1, m2)
        ]
