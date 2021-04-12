#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 10.0
phi = 10.0
pix2angle = 1.0
pix2radian = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

scale = 1.0
scaling_multiplier = 0.1

# variables for handling mouse scroll (i know, i didn't have to do it, but i did must)
scroll_step = 0.05
scroll_scaling = 1.0

R = 10.125
R_scalling = 0.05
R_min_value = 3.75
R_max_value = 16.5
eye_x = 0.0
eye_y = 0.0
eye_z = 10.0

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False

x_pos = 0.0
move_x_step = 0.1
z_pos = 0.0
move_z_step = 0.05

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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global phi

    global scale

    global R
    global eye_x
    global eye_y
    global eye_z

    global x_pos
    global z_pos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # gluLookAt(viewer[0], viewer[1], viewer[2],
    #           x_pos, 0.0, z_pos, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        # theta += delta_x * pix2angle
        # phi += delta_y * pix2angle
        theta += delta_x * pix2radian
        phi += delta_y * pix2radian

    if right_mouse_button_pressed:
        # scale += delta_x * scaling_multiplier
        new_R_value = R + delta_y * R_scalling
        if new_R_value < R_min_value:
            R = R_min_value
        elif new_R_value > R_max_value:
            R = R_max_value
        else:
            R = new_R_value

    # print("R = " + str(R))
    # print("theta = " + str(theta))
    # print("phi = " + str(phi))

    eye_x = R * math.cos(theta) * math.cos(phi)
    eye_y = R * math.sin(phi)
    eye_z = R * math.sin(theta) * math.sin(phi)

    # print("eye_x = " + str(eye_x))
    # print("eye_y = " + str(eye_y))
    # print("eye_z = " + str(eye_z))

    # glRotatef(theta, 0.0, 1.0, 0.0)
    # glRotatef(phi, 1.0, 0.0, 0.0)
    # glScale(scale, scale, scale)
    # glScale(scroll_scaling, scroll_scaling, scroll_scaling)

    if w_pressed:
        x_pos += move_x_step
    if a_pressed:
        z_pos += move_z_step
    if s_pressed:
        x_pos -= move_x_step
    if d_pressed:
        z_pos -= move_z_step

    gluLookAt(eye_x, eye_y, eye_z,
              x_pos, 0.0, z_pos, 0.0, 1.0, 0.0)

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    global pix2radian

    pix2angle = 360.0 / width
    pix2radian = 2 * math.pi / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global w_pressed
    global a_pressed
    global s_pressed
    global d_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    # W key

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        w_pressed = True

    if key == GLFW_KEY_W and action == GLFW_RELEASE:
        w_pressed = False

    # A key

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        a_pressed = True

    if key == GLFW_KEY_A and action == GLFW_RELEASE:
        a_pressed = False

    # S key

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        s_pressed = True

    if key == GLFW_KEY_S and action == GLFW_RELEASE:
        s_pressed = False

    # D key

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        d_pressed = True

    if key == GLFW_KEY_D and action == GLFW_RELEASE:
        d_pressed = False

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

def mouse_scroll_callback(window, xoffset, yoffset):
    global scroll_scaling

    # for scrolling forward yoffset returns 1.0
    # for backward returns -1.0
    scroll_scaling += yoffset * scroll_step

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetScrollCallback(window, mouse_scroll_callback)
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
