#from hypothesis import given, strategies as st
import pytest
from .vectors import add


#scalars = st.floats(min_value=-1000, max_value=1000, allow_nan=False)

def test_adding_vectors_of_different_size_raises_excception():
    u = (1, 1)
    v = (1, 1, 1)

    with pytest.raises(ValueError):
        add(u, v)
