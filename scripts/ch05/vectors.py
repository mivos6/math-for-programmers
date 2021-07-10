import math


def add(*vectors):
    return tuple(map(sum, zip(*vectors)))


def components2d(vector):
    return [(vector[0], 0), (0, vector[1])]


def length(vector):
    return math.sqrt(sum([c ** 2 for c in vector]))


def scale(scalar, vector):
    return tuple([scalar * c for c in vector])


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


def deg(angle_rad):
    return angle_rad * 180 / math.pi


def rad(angle_deg):
    return angle_deg * math.pi / 180


def normalize_angle(angle_rad):
    return angle_rad - 2 * math.pi * math.floor(angle_rad / (2 * math.pi))


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


def rotate2d(radians, vector):
    return to_cartesian((length(vector), direction2d(vector) + radians))


def rotate_z(radians, vector):
    x, y, z = vector
    if x == y == 0:
        return vector

    xr, yr = rotate2d(radians, (x, y))
    return xr, yr, z


def rotate_x(radians, vector):
    x, y, z = vector
    if y == z == 0:
        return vector

    yr, zr = rotate2d(radians, (y, z))
    return x, yr, zr


def linear_combination(scalars, *vectors):
    assert len(scalars) == len(vectors), "{} != {}".format(len(scalars), len(vectors))

    scaled = [scale(s, v) for s, v in zip(scalars, vectors)]
    return add(*scaled)
