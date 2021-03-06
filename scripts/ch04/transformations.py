from vectors import add, scale


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