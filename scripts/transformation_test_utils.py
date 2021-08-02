from .vectors import add, scale
from .compare import vector_epsilon_equal 

def assert_transformation_is_linear(t, u, v, s):
    epsilon = 1e-6

    preserves_addition = vector_epsilon_equal(t(add(u, v)), add(t(u), t(v)), epsilon)
    preserves_scalar_multiplication = vector_epsilon_equal(t(scale(s, v)), scale(s, t(v)), epsilon)

    assert preserves_addition
    assert preserves_scalar_multiplication
