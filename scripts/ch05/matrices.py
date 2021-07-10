from vectors import *


def multiply_matrix_vector(m, v):
    return linear_combination(v, *zip(*m))


def matrix_multiply(m1, m2):
    m2_columns = tuple(zip(*m2))

    return tuple(
        tuple(
            dot(row_m1, column_m2) for column_m2 in m2_columns
        ) for row_m1 in m1
    )
