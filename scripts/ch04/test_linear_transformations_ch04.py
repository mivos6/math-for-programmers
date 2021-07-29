from hypothesis import given, strategies as st
from transformation_test_utils import assert_transformation_is_linear
from transformations import rotate_z_by, translate_by

scalars = st.floats(min_value=-1000, max_value=1000, allow_nan=False)
vectors = st.tuples(scalars, scalars, scalars)


@given(u=vectors, v=vectors, s=scalars)
def test_is_rotate_z_linear(u, v, s):
    assert_transformation_is_linear(rotate_z_by(0.5), u, v, s)


@given(u=vectors, v=vectors, s=scalars)
def test_is_translate_linear(u, v, s):
    i, j, k = (1, 0, 0), (0, 1, 0), (0, 0, 1)

    assert_transformation_is_linear(translate_by(i), u, v, s)
    assert_transformation_is_linear(translate_by(j), u, v, s)
    assert_transformation_is_linear(translate_by(k), u, v, s)

