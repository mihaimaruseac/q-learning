# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#
# This file contains only some global definitions to avoid their duplication.
#
# It is safe to do from globaldefs import *

TITLE = "Robot in a Grid"

N = 12
M = 8

VOID_FILE = "img/void.png"
EMPTY_FILE = "img/empty.png"
ROBOT_FILE = "img/robot.png"
ROBOT_N_FILE = "img/robot_n.png"
ROBOT_E_FILE = "img/robot_e.png"
ROBOT_S_FILE = "img/robot_s.png"
ROBOT_W_FILE = "img/robot_w.png"

VOID = 42
EMPTY = 43
ROBOT = 0
ROBOT_N = 1
ROBOT_E = 2
ROBOT_S = 3
ROBOT_W = 4

FORWARD = 42
TURN_LEFT = 43
TURN_RIGHT = 41

FRONT = 0
RIGHT = 1
BACK = 2
LEFT = 3

IMAGES = {}

def build_sep_points(maxN, maxM):
    """
    Builds the spliting points for a multi-screen world.
    """
    return (xrange(-1, maxN, N), xrange(-1, maxM, M))

