import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_color():
    red = random.uniform(0.0, 1.0)
    green = random.uniform(0.0, 1.0)
    blue = random.uniform(0.0, 1.0)
    return [red, green, blue]


def draw_monochromatic_triangle(points, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(points[0][0], points[0][1])
    glVertex2f(points[1][0], points[1][1])
    glVertex2f(points[2][0], points[2][1])
    glEnd()


def draw_achromatic_triangle(points, colors):
    glBegin(GL_TRIANGLES)
    glColor3f(colors[0][0], colors[0][1], colors[0][2])
    glVertex2f(points[0][0], points[0][1])
    glColor3f(colors[1][0], colors[1][1], colors[1][2])
    glVertex2f(points[1][0], points[1][1])
    glColor3f(colors[2][0], colors[2][1], colors[2][2])
    glVertex2f(points[2][0], points[2][1])
    glEnd()


def draw_rectangle(x, y, a, b, color, d=0.0):
    if d == 0.0 or d == 1.0:
        draw_monochromatic_triangle([[x, y], [x + a, y], [x + a, y - b]], color)
        draw_monochromatic_triangle([[x, y], [x, y - b], [x + a, y - b]], color)
    else:
        a *= d
        b *= d
        draw_monochromatic_triangle([[x, y], [x + a, y], [x + a, y - b]], color)
        draw_monochromatic_triangle([[x, y], [x, y - b], [x + a, y - b]], color)


def draw_sierpinski_carpet(depth, x=-100.0, y=-100.0, a=200.0, color=[0.0, 0.0, 0.0]):
    if depth > 0:
        a /= 3
        draw_sierpinski_carpet(depth - 1, x, y, a)
        draw_sierpinski_carpet(depth - 1, x + a, y, a)
        draw_sierpinski_carpet(depth - 1, x + 2 * a, y, a)
        draw_sierpinski_carpet(depth - 1, x, y - a, a)
        draw_sierpinski_carpet(depth - 1, x + 2 * a, y - a, a)
        draw_sierpinski_carpet(depth - 1, x, y - 2 * a, a)
        draw_sierpinski_carpet(depth - 1, x + a, y - 2 * a, a)
        draw_sierpinski_carpet(depth - 1, x + 2 * a, y - 2 * a, a)
    else:
        draw_rectangle(x, y, a, a, color)


def draw_sierpinski_carpet_iterative(depth, x=-100.0, y=-100.0, a=200.0, color=[0.0, 0.0, 0.0]):
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    points = [[0.0, 0.0], [0.0, 50.0], [50.0, 0.0]]
    colors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    color = draw_color()

    # draw_achromatic_triangle(points, colors)
    # draw_rectangle(-90.0, 90.0, 180.0, 180.0, color, -1.05)
    draw_sierpinski_carpet(4, -90.0, 90.0, 180.0)
    glFlush()


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

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

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
