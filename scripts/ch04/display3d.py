import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from vectors import *
from math import *

default_display_properties = {
    'window_size': (400, 400),
    'perspective': {
        'fov': 45,
        'aspect_ratio': 1.0,
        'min_z': 0.1,
        'max_z': 50.0
    },
    'camera': {
        'translate': (0.0, 0.0, -5.0),
        'rotate': {
            'rate': 0.0,
            'axis': (0.0, 1.0, 0.0)
        }
    }
}


def shade(triangle, light_source, colormap=matplotlib.cm.get_cmap('Blues')):
    return colormap(1 - dot(unit(normal(triangle)), unit(light_source)))


def create_window(properties):
    pygame.init()
    window = pygame.display.set_mode(properties['window_size'], DOUBLEBUF | OPENGL)

    gluPerspective(properties['perspective']['fov'],
                   properties['perspective']['aspect_ratio'],
                   properties['perspective']['min_z'],
                   properties['perspective']['max_z'])
    glTranslate(*properties['camera']['translate'])

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glCullFace(GL_BACK)

    return window


def quit_if_prompted():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def render(model, light_source):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for polygon in model:
        color = shade(polygon, light_source)
        for vertex in polygon:
            glColor3fv((color[0], color[1], color[2]))
            glVertex3fv(vertex)
    glEnd()
    pygame.display.flip()


def rotate_camera(rate=0.0, axis=(0, 0, 1), delta_milliseconds=0):
    if rate > 0.0:
        delta_angle = rate / 1000 * delta_milliseconds
        glRotatef(delta_angle, *axis)


def display(model, light_source, properties=None):
    if properties is None:
        properties = default_display_properties

    create_window(properties)
    clock = pygame.time.Clock()

    while True:
        quit_if_prompted()

        delta_milliseconds = clock.tick()
        rotate_camera(properties['camera']['rotate']['rate'],
                      properties['camera']['rotate']['axis'],
                      delta_milliseconds)

        render(model, light_source)
