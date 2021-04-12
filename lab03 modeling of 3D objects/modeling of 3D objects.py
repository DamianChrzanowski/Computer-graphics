#!/usr/bin/env python3
import sys
import math
import numpy

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 50

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(angle):
    # glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 0.1)

def designate_x(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v);

def designate_y(u, v):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2;

def designate_z(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

def designate_egg_vertices(N):
    vertices = [[[0 for k in range(3)] for j in range(N)] for i in range(N)]

    step = 1.0 / N
    u = 0.0
    v = 0.0

    for i in range(N):
        for j in range(N):
            vertices[i][j][0] = designate_x(u, v)
            vertices[i][j][1] = designate_y(u, v)
            vertices[i][j][2] = designate_z(u, v)
            v += step
        u += step

    return vertices

def render(time, egg_vertices):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()
    spin(time * 180 / math.pi)

    for i in range(N):
        for j in range(N):
            glBegin(GL_POINTS)
            glColor(255, 255, 255)
            glVertex3f(egg_vertices[i][j][0] / 2,
                       egg_vertices[i][j][1] / 2,
                       egg_vertices[i][j][2] / 2)
            glEnd()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    egg_vertices = designate_egg_vertices(N)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), egg_vertices)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
