def load_off_file(filename):
    with open(filename) as file:
        if file.readline() != 'OFF\n':
            raise Exception('Not a valid OFF file')

        length_strings = file.readline().split()
        num_vertices, num_faces = int(length_strings[0]), int(length_strings[1])

        vertices = [tuple([float(string_value)
                           for string_value in file.readline().split()])
                    for _ in range(num_vertices)]

        faces = [[int(string_value)
                  for string_value in file.readline().split()[1:]]
                 for _ in range(num_faces)]

        return vertices, faces


def make_triangles(polygon):
    if len(polygon) < 3:
        raise ValueError('len(polygon) < 3')

    return [[polygon[0], polygon[i+1], polygon[i]] for i in range(1, len(polygon) - 1)]


def create_3d_model(vertices, faces):
    model = []
    for f in faces:
        polygon = [vertices[vertex_index] for vertex_index in f]
        for triangle in make_triangles(polygon):
            model.append(triangle)
    return model
