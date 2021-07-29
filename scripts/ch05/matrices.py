from vectors import *


def multiply_matrix_vector(m, v):
    return linear_combination(v, *zip(*m))


def multiply_matrix_vector2(m, v):
    return tuple(
            sum(row_elem*vector_elem for row_elem, vector_elem in zip(row, v)) 
            for row in m
        )


def multiply_matrix_vector3(m, v):
    return tuple(dot(row, v) for row in m)


def matrix_multiply(m1, m2):
    m2_columns = tuple(zip(*m2))

    return tuple(
        tuple(
            dot(row_m1, column_m2) for column_m2 in m2_columns
        ) for row_m1 in m1
    )

def matrix_power(power, matrix):
    if power < 1:
        raise ValueError("Argument 'power' must be >=1, is {}".format(power))

    result = matrix
    for _ in range(power-1):
        result = matrix_multiply(result, matrix)
    
    return result

