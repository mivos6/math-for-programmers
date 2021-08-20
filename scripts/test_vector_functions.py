from hypothesis import given
import hypothesis.strategies as strats
from hypothesis.strategies import composite
import pytest
from .vectors import add, subtract, distance, dot, angle, cross, projection_length, project_vectors_to_xy_plane, linear_combination

scalar = strats.floats(min_value=-1000, max_value=1000, allow_nan=False)


def length(min_val=0, max_val=None):
    return strats.integers(min_value=min_val, max_value=max_val)


@composite
def vector(draw, min_size=0, max_size=None):
    vector_size = draw(length(min_size, max_size))
    vectors = strats.tuples(*[scalar for _ in range(vector_size)])
    return draw(vectors)


def list_of_vectors(vector_strat=vector(max_size=20), min_length=0, max_length=None, unique_by=None):
    return strats.lists(vector_strat, min_size=min_length, max_size=max_length, unique_by=unique_by)


@given(vl=list_of_vectors(min_length=2, unique_by=lambda v: len(v)))
def test_add_vectors_of_different_size_raises_exception(vl):
    with pytest.raises(ValueError):
        add(*vl)


two_vectors_of_different_size = list_of_vectors(
    min_length=2, max_length=2, unique_by=lambda v: len(v))


@given(vs=two_vectors_of_different_size)
def test_subtract_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        subtract(vs[0], vs[1])


@given(vs=two_vectors_of_different_size)
def test_distance_between_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        distance(vs[0], vs[1])


@given(vs=two_vectors_of_different_size)
def test_dot_product_between_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        dot(vs[0], vs[1])


@given(vs=two_vectors_of_different_size)
def test_angle_between_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        angle(vs[0], vs[1])


@given(vs=list_of_vectors(vector_strat=vector(min_size=1, max_size=2), min_length=2, max_length=2))
def test_cross_product_between_1d_and_2d_vectors_raises_exception(vs):
    with pytest.raises(ValueError):
        cross(vs[0], vs[1])


@given(vs=list_of_vectors(vector_strat=vector(min_size=4, max_size=20), min_length=2, max_length=2))
def test_cross_product_between_vectors_higher_than_3d_raises_exception(vs):
    with pytest.raises(ValueError):
        cross(vs[0], vs[1])


@given(vs=two_vectors_of_different_size)
def test_projection_length_between_vectors_of_different_size_raises_exception(vs):
    with pytest.raises(ValueError):
        projection_length(vs[0], vs[1])


@given(v=vector(min_size=3, max_size=3))
def test_projection_length_raises_exception_when_projecting_to_nul_vector(v):
    with pytest.raises(ValueError):
        projection_length(v, (0, 0, 0))


@given(vl=list_of_vectors(vector_strat=vector(min_size=1, max_size=2), min_length=1))
def test_project_vectors_to_xy_plane_raises_exception_for_1d_and_2d_vectors(vl):
    with pytest.raises(ValueError):
        project_vectors_to_xy_plane(*vl)


@given(vl=list_of_vectors(vector_strat=vector(min_size=4, max_size=20), min_length=1))
def test_project_vectors_to_xy_plane_raises_exception_for_vectors_higher_than_3d(vl):
    with pytest.raises(ValueError):
        project_vectors_to_xy_plane(*vl)


@composite
def list_of_vectors_of_equal_length(draw, max_vector_size=20, min_length=0, max_length=None, unique_by=None):
    vector_size = draw(strats.integers(min_value=0, max_value=max_vector_size))
    vector_list = list_of_vectors(vector_strat=vector(
        min_size=vector_size, max_size=vector_size), min_length=min_length, max_length=max_length, unique_by=unique_by)
    return draw(vector_list)


@ given(strats.data())
def test_linear_combination_raises_exception_when_number_of_scalars_is_not_equal_to_number_of_vectors(data):
    sl = data.draw(strats.lists(scalar))
    vl = data.draw(list_of_vectors_of_equal_length(min_length=len(sl)+1))
    with pytest.raises(ValueError):
        linear_combination(sl, *vl)


@given(strats.data())
def test_linear_combination_for_vectors_of_different_length_raises_exception(data):
    sl = data.draw(strats.lists(scalar, min_size=2))
    vl = data.draw(list_of_vectors(min_length=len(
        sl), max_length=len(sl), unique_by=lambda v: len(v)))
    with pytest.raises(ValueError):
        linear_combination(sl, *vl)
