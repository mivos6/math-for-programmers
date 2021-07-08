from vectors import add, subtract, scale


def epsilon_equal(u, v, epsilon):
    return False not in [abs(delta) < epsilon for delta in subtract(u, v)]


def is_transformation_linear(t, u, v, s):
    epsilon = 1e-6

    preserves_addition = epsilon_equal(t(add(u, v)), add(t(u), t(v)), epsilon)
    preserves_scalar_multiplication = epsilon_equal(t(scale(s, v)), scale(s, t(v)), epsilon)

    assert preserves_addition
    assert preserves_scalar_multiplication
