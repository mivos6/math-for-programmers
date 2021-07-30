from hypothesis import given, strategies as st
import pytest
from .vectors import add, subtract, distance, dot, angle, cross, projection_length, project_vectors_to_xy_plane, linear_combination


scalars = st.floats(min_value=-1000, max_value=1000, allow_nan=False)

# generate variable-length vectors
vectors = st.integers(min_value=2, max_value=10, ).flatmap(
    lambda n: st.tuples(*[scalars for _ in range(n)]))

lists_of_vectors_of_unique_length = st.lists(
    vectors, min_size=1, max_size=100, unique_by=lambda v: len(v))

lists_of_vectors_of_equal_length = st.integers(min_value=2, max_value=10, ).flatmap(
    lambda n: st.lists(st.tuples(*[scalars for _ in range(n)]), min_size=1, max_size=100))


@given(vl=lists_of_vectors_of_unique_length)
def test_add_vectors_of_different_size_raises_exception(vl):
    with pytest.raises(ValueError):
        add(*vl)


@given(u=vectors, v=vectors)
def test_subtract_vectors_of_different_size_raises_exception(u, v):
    if len(u) != len(v):
        with pytest.raises(ValueError):
            subtract(u, v)


@given(u=vectors, v=vectors)
def test_distance_betwwen_vectors_of_different_size_raises_exception(u, v):
    if len(u) != len(v):
        with pytest.raises(ValueError):
            distance(u, v)


@given(u=vectors, v=vectors)
def test_dot_product_betwwen_vectors_of_different_size_raises_exception(u, v):
    if len(u) != len(v):
        with pytest.raises(ValueError):
            dot(u, v)


@given(u=vectors, v=vectors)
def test_angle_betwwen_vectors_of_different_size_raises_exception(u, v):
    if len(u) != len(v):
        with pytest.raises(ValueError):
            angle(u, v)


@given(u=vectors, v=vectors)
def test_cross_product_betwwen_non_3d_vectors_raises_exception(u, v):
    if len(u) != 3 or len(v) != 3:
        with pytest.raises(ValueError):
            cross(u, v)


@given(u=vectors, v=vectors)
def test_projection_length_betwwen_vectors_of_different_size_raises_exception(u, v):
    if len(u) != len(v):
        with pytest.raises(ValueError):
            projection_length(u, v)


@given(vl=lists_of_vectors_of_unique_length)
def test_project_vectors_to_xy_plane_raises_exception_for_non_3d_vectors(vl):
    with pytest.raises(ValueError):
        project_vectors_to_xy_plane(*vl)


@given(s=st.lists(scalars), vl=lists_of_vectors_of_equal_length)
def test_linear_combination_raises_exception_when_number_of_scalars_is_not_equal_to_number_of_vectors(s, vl):
    if len(s) != len(vl):
        with pytest.raises(ValueError):
            linear_combination(s, *vl)
