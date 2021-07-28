from vectors import add, subtract, scale


def vector_epsilon_equal(u, v, epsilon=1e-6):
    if not len(u) == len(v):
        return False

    return False not in [abs(delta) < epsilon for delta in subtract(u, v)]


def matrix_epsilon_equal(m1, m2, epsilon=1e-6):
    if not len(m1) == len(m2):
        return False

    return False not in [
            vector_epsilon_equal(row1, row2, epsilon)
            for row1, row2 in zip(m1, m2)
        ]


def assert_transformation_is_linear(t, u, v, s):
    epsilon = 1e-6

    preserves_addition = vector_epsilon_equal(t(add(u, v)), add(t(u), t(v)), epsilon)
    preserves_scalar_multiplication = vector_epsilon_equal(t(scale(s, v)), scale(s, t(v)), epsilon)

    assert preserves_addition
    assert preserves_scalar_multiplication
