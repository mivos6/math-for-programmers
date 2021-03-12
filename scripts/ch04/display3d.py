import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from vectors import *
from collections import namedtuple

Rotation = namedtuple('Rotation', ['initial', 'rate', 'axis'], defaults=[0.0, 0.0, (0.0, 1.0, 0.0)])
Scene = namedtuple('Scene', ['translate', 'rotate'], defaults=[(0.0, 0.0, -5.0), Rotation()])
Perspective = namedtuple('Perspective', ['fov', 'aspect_ratio', 'min_z', 'max_z'], defaults=[45.0, 1.0, 0.1, 50.0])
DisplayProperties = namedtuple('DisplayProperties', ['window_size', 'perspective', 'scene'],
                               defaults=[(400, 400), Perspective(), Scene()])


def shade(triangle, light_source, colormap=matplotlib.cm.get_cmap('Blues')):
    return colormap(1 - dot(unit(normal(triangle)), unit(light_source)))


def create_window(properties):
    pygame.init()
    window = pygame.display.set_mode(properties.window_size, DOUBLEBUF | OPENGL)

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
    pygame.display.flip()


def rotate_scene(rate=0.0, axis=(0, 0, 1), delta_milliseconds=0):
    if rate > 0.0:
        delta_angle = rate / 1000 * delta_milliseconds
        glRotatef(delta_angle, *axis)


def display(model, light_source, properties=DisplayProperties()):
    create_window(properties)
    clock = pygame.time.Clock()

    while not should_quit():
        delta_milliseconds = clock.tick()
        rotate_scene(properties.scene.rotate.rate,
                     properties.scene.rotate.axis,
                     delta_milliseconds)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        render_axes()
        render_polygons(model, light_source)
