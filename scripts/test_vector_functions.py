from hypothesis import given, strategies as st
import pytest
from .vectors import add, subtract, distance, dot, angle, cross, projection_length, project_vectors_to_xy_plane, linear_combination


scalars = st.floats(min_value=-1000, max_value=1000, allow_nan=False)

# generate variable-length vectors
vectors = st.integers(min_value=2, max_value=10, ).flatmap(
    lambda n: st.tuples(*[scalars for _ in range(n)]))

lists_of_vectors_of_unique_length = st.lists(
    vectors, min_size=2, max_size=100, unique_by=lambda v: len(v))


@given(vl=lists_of_vectors_of_unique_length)
def test_add_vectors_of_different_size_raises_exception(vl):
    with pytest.raises(ValueError):
        add(*vl)


pairs_of_vectors = st.tuples(vectors, vectors)
pairs_of_vectors_with_different_length = pairs_of_vectors.filter(
    lambda pair: len(pair[0]) != len(pair[1])
)


@given(vs=pairs_of_vectors_with_different_length)
def test_subtract_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        subtract(vs[0], vs[1])


@given(vs=pairs_of_vectors_with_different_length)
def test_distance_betwwen_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        distance(vs[0], vs[1])


@given(vs=pairs_of_vectors_with_different_length)
def test_dot_product_betwwen_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        dot(vs[0], vs[1])


@given(vs=pairs_of_vectors_with_different_length)
def test_angle_betwwen_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        angle(vs[0], vs[1])


@given(vs=pairs_of_vectors.filter(lambda pair: len(pair[0]) != 3 or len(pair[1]) != 3))
def test_cross_product_betwwen_non_3d_vectors_raises_exception(vs):
    with pytest.raises(ValueError):
        cross(vs[0], vs[1])


@given(vs=pairs_of_vectors_with_different_length)
def test_projection_length_between_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        projection_length(vs[0], vs[1])


@given(v=vectors.filter(lambda v: len(v) == 3))
def test_projection_length_raises_exsception_when_projecting_to_nul_vector(v):
    with pytest.raises(ValueError):
        projection_length(v, (0, 0, 0))


@given(vl=lists_of_vectors_of_unique_length.filter(lambda vl: 3 not in map(len, vl)))
def test_project_vectors_to_xy_plane_raises_exception_for_non_3d_vectors(vl):
    with pytest.raises(ValueError):
        project_vectors_to_xy_plane(*vl)


lists_of_vectors_of_equal_length = st.integers(
    min_value=1, max_value=10, ).flatmap(
        lambda n: st.lists(
            st.tuples(*[scalars for _ in range(n)]), min_size=1, max_size=100)
    )
scalars_and_vectors_of_different_size = st.tuples(
    st.lists(scalars), lists_of_vectors_of_equal_length).filter(
        lambda pair: len(pair[0]) != len(pair[1])
    )


@ given(sv_pair=scalars_and_vectors_of_different_size)
def test_linear_combination_raises_exception_when_number_of_scalars_is_not_equal_to_number_of_vectors(sv_pair):
    with pytest.raises(ValueError):
        linear_combination(sv_pair[0], *sv_pair[1])


scalars_and_vectors_of_unique_length = st.tuples(
    st.lists(scalars), lists_of_vectors_of_unique_length).filter(
        lambda pair: (len(pair[0]) == len(pair[1]))
    )


@ given(sv_pair=scalars_and_vectors_of_unique_length)
def test_linear_combination_for_vectors_of_different_length_raises_exception(sv_pair):
    with pytest.raises(ValueError):
        linear_combination(sv_pair[0], *sv_pair[1])
