from vectors import add, scale, rotate_z, rotate_x


def map_to_polygons(transformation, polygons):
    return [[transformation(vertex) for vertex in polygon] for polygon in polygons]


def compose(*transformations):
    def composed_transform(vector):
        result = vector
        for t in transformations:
            result = t(result)
        return result

    return composed_transform


def scale_by(scalar):
    return lambda vector: scale(scalar, vector)


def translate_by(translation_vector):
    return lambda vector: add(translation_vector, vector)


def rotate_z_by(radians):
    return lambda vector: rotate_z(radians, vector)


def rotate_x_by(radians):
    return lambda vector: rotate_x(radians, vector)
