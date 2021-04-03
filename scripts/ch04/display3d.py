import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from vectors import *
from transformations import *
from collections import namedtuple
import PIL.Image
import functools
import math

import time

Rotation = namedtuple('Rotation', ['initial', 'rate', 'axis'], defaults=[0.0, 0.0, (0.0, 1.0, 0.0)])
Scene = namedtuple('Scene', ['translate', 'rotate'], defaults=[(0.0, 0.0, -5.0), Rotation()])
Perspective = namedtuple('Perspective', ['fov', 'aspect_ratio', 'min_z', 'max_z'], defaults=[45.0, 1.0, 0.1, 50.0])
DisplayProperties = namedtuple('DisplayProperties', ['window_size', 'perspective', 'scene'],
                               defaults=[(400, 400), Perspective(), Scene()])


def shade(triangle, light_source, colormap=matplotlib.cm.get_cmap('Blues')):
    return colormap(1 - dot(unit(normal(triangle)), unit(light_source)))


def set_perspective(properties):
    gluPerspective(properties.perspective.fov,
                   properties.perspective.aspect_ratio,
                   properties.perspective.min_z,
                   properties.perspective.max_z)
    glTranslate(*properties.scene.translate)
    glRotatef(properties.scene.rotate.initial,
              *properties.scene.rotate.axis)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glCullFace(GL_BACK)


def create_window(properties, hidden=False):
    window = pygame.display.set_mode(properties.window_size, DOUBLEBUF | OPENGL | (HIDDEN if hidden else 0))
    set_perspective(properties)

    return window


def should_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
    return False


def render_axes():
    axes = [
        [(-1000.0, 0.0, 0.0), (1000.0, 0.0, 0.0)],
        [(0.0, -1000.0, 0.0), (0.0, 1000.0, 0.0)],
        [(0.0, 0.0, -1000.0), (0.0, 0.0, 1000.0)]
    ]
    glBegin(GL_LINES)
    for axis in axes:
        for vertex in axis:
            glColor3fv((1.0, 1.0, 1.0))
            glVertex3fv(vertex)
    glEnd()


def render_polygons(model, light_source):
    glBegin(GL_TRIANGLES)
    for polygon in model:
        color = shade(polygon, light_source)
        for vertex in polygon:
            glColor3fv((color[0], color[1], color[2]))
            glVertex3fv(vertex)
    glEnd()


def rotate_scene(rate=0.0, axis=(0, 0, 1), delta_milliseconds=0):
    if rate > 0.0:
        delta_angle = rate / 1000 * delta_milliseconds
        glRotatef(delta_angle, *axis)


def display_in_window(model, light_source, properties=DisplayProperties()):
    pygame.init()
    window = create_window(properties)
    clock = pygame.time.Clock()

    while not should_quit():
        delta_milliseconds = clock.tick()
        rotate_scene(properties.scene.rotate.rate,
                     properties.scene.rotate.axis,
                     delta_milliseconds)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        render_axes()
        render_polygons(model, light_source)
        pygame.display.flip()


def pygame_display(func):
    @functools.wraps(func)
    def pygame_wrapper(*args, **kwargs):
        pygame.display.init()
        try:
            return func(*args, **kwargs)
        finally:
            pygame.display.quit()
    return pygame_wrapper


@pygame_display
def render_frame(model, light_source, properties=DisplayProperties()):
    window = create_window(properties, hidden=True)

    screen_surface = render_on_surface(model, light_source, window.get_size())
    # swap the x, y axes since arrays are indexed column-first
    screen_array = pygame.surfarray.array3d(screen_surface).swapaxes(0, 1)

    return PIL.Image.fromarray(screen_array)


def render_on_surface(model, light_source, surface_size):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    render_axes()
    render_polygons(model, light_source)

    # https://stackoverflow.com/questions/66209365/how-to-save-pygame-scene-as-jpeg
    pixel_buffer = glReadPixels(0, 0, *surface_size, GL_RGB, GL_UNSIGNED_BYTE)

    # create a flipped surface because glReadPixels will invert the order of rows in memory
    return pygame.image.fromstring(pixel_buffer, surface_size, "RGB", True)


@pygame_display
def render_sequence(starting_model, light_source, transform_sequence, num_horizontal_frames=5, properties=DisplayProperties()):
    window = create_window(properties, hidden=True)
    frame_size = window.get_size()

    num_vertical_frames = math.ceil(float(len(transform_sequence) + 1) / num_horizontal_frames)
    result_surface = pygame.Surface((frame_size[0] * num_horizontal_frames, frame_size[1] * num_vertical_frames))
    result_surface.fill((255, 255, 255))

    model = starting_model
    current_frame = render_on_surface(model, light_source, frame_size)
    result_surface.blit(current_frame, (0, 0))
    for i, next_transform in enumerate(transform_sequence):
        model = map_to_polygons(next_transform, model)
        current_frame = render_on_surface(model, light_source, frame_size)
        row, col = int((i + 1) / num_horizontal_frames), (i + 1) % num_horizontal_frames
        result_surface.blit(current_frame, (frame_size[0] * col, frame_size[1] * row))

    screen_array = pygame.surfarray.array3d(result_surface).swapaxes(0, 1)
    return PIL.Image.fromarray(screen_array)
