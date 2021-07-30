import math


def add(*vectors):
    return tuple(map(sum, zip(*vectors)))


def translate(translation_vec, vectors):
    return [add(translation_vec, v) for v in vectors]


def components2d(vector):
    return [(vector[0], 0), (0, vector[1])]


def length(vector):
    return math.sqrt(sum([c**2 for c in vector]))


def scale(scalar, vector):
    return tuple([scalar*c for c in vector])


def scale_all(scalar, vectors):
    return [scale(scalar, v) for v in vectors]


def subtract(v1, v2):
    return add(v1, scale(-1, v2))


def distance(v1, v2):
    return length(subtract(v2, v1))


def direction(vector):
    return math.atan2(vector[1], vector[0])


def to_cartesian(polar_vector):
    r, theta = polar_vector[0], polar_vector[1]
    return (r * math.cos(theta), r * math.sin(theta))


def to_polar(cartesian_vector):
    return (length(cartesian_vector), direction(cartesian_vector))


def rad(deg):
    return deg * math.pi/180


def deg(rad):
    return rad * 180/math.pi


def normalize_radians(rad):
    return rad - 2*math.pi * math.floor(rad / (2*math.pi))


def rotate(angle, vectors):
    return [to_cartesian((length(v), direction(v) + angle)) for v in vectors]
