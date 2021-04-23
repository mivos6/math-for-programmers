from hypothesis import given, strategies as st
from vectors import add, subtract, scale
from transformations import rotate_z_by


def epsilon_equal(u, v, epsilon):
    return False not in [abs(delta) < epsilon for delta in subtract(u, v)]


scalars = st.floats(min_value=-1000, max_value=1000, allow_nan=False)
vectors = st.tuples(scalars, scalars, scalars)


@given(u=vectors, v=vectors, s=scalars)
def test_is_rotate_z_linear_transformation(u, v, s):
    t = rotate_z_by(0.5)
    epsilon = 1e-6

    assert epsilon_equal(t(add(u, v)), add(t(u), t(v)), epsilon)
    assert epsilon_equal(t(scale(s, v)), scale(s, t(v)), epsilon)

