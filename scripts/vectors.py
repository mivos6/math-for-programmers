import math


def add(*vectors):
    return tuple(map(sum, zip(*vectors)))


def translate(translation_vec, vectors):
    return [add(translation_vec, v) for v in vectors]


def components2d(vector):
    return [(vector[0], 0), (0, vector[1])]


def length(vector):
    return math.sqrt(sum([c ** 2 for c in vector]))


def scale(scalar, vector):
    return tuple([scalar * c for c in vector])


def scale_all(scalar, vectors):
    return [scale(scalar, v) for v in vectors]


def subtract(v1, v2):
    return add(v1, scale(-1, v2))


def distance(v1, v2):
    return length(subtract(v2, v1))


def direction2d(vector):
    return math.atan2(vector[1], vector[0])


def to_cartesian(polar_vector):
    r, theta = polar_vector[0], polar_vector[1]
    return r * math.cos(theta), r * math.sin(theta)


def to_polar(cartesian_vector):
    return length(cartesian_vector), direction2d(cartesian_vector)


def rad(deg):
    return deg * math.pi / 180


def deg(rad):
    return rad * 180 / math.pi


def normalize_radians(rad):
    return rad - 2 * math.pi * math.floor(rad / (2 * math.pi))


def rotate2d(degrees, vectors):
    return [to_cartesian((length(v), direction2d(v) + degrees)) for v in vectors]


def unit(v):
    return scale(1 / length(v), v)


def dot(u, v):
    return sum([cu * cv for cu, cv in zip(u, v)])


def angle(u, v):
    return math.acos(dot(u, v) / (length(u) * length(v)))


def cross(u, v):
    ux, uy, uz = u[0], u[1], u[2]
    vx, vy, vz = v[0], v[1], v[2]
    return (uy * vz - uz * vy), (uz * vx - ux * vz), (ux * vy - uy * vx)


def vertices(*triangles):
    return list(set([vertex for triangle in triangles for vertex in triangle]))


def normal(triangle):
    return cross(subtract(triangle[1], triangle[0]), subtract(triangle[2], triangle[0]))


def projection_length(vector, projection_vector):
    return dot(vector, projection_vector) / length(projection_vector)


def project_vectors_to_xy_plane(*vectors):
    return [(projection_length(v, (1, 0, 0)), projection_length(v, (0, 1, 0)))
            for v in vectors]
