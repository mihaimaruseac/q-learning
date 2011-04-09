# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import robot
from globaldefs import *

class World(object):
    """
    Holds the definitions for the world simulated. Basically, it contains the
    actual state of the robot (the robot knows only what his sensors provide
    him with but the world is more complex than that) and an instance of the
    robot.

    Simple workflow:
        __init__ -> [a:] step -> [*] -> goto a

    [*]: here, the GUI may call several functions to display the world in a
    nice graphical way.
    """

    def __init__(self, config):
        """
        Constructs a new world, taking into account the user configuration.

        config  The user configuration dictionary.
        """
        global NPOINTS, MPOINTS
        NPOINTS, MPOINTS = build_sep_points(config['N'], config['M'])
        self._parse_internal_data(config)
        self._build_robot(config)

    def _parse_internal_data(self, config):
        """
        Parses the configuration and sets the internal data.
        """
        self._N = config['N']
        self._M = config['M']
        self._D = config['D']
        self._xs = config['xs']
        self._ys = config['ys']
        self._xr = self._xs
        self._yr = self._ys
        self._d1 = config['d1']
        self._d2 = config['d2']
        self._runs = config['runs']

    def _build_robot(self, config):
        """
        Builds the robot.
        """
        d = {}
        d['greedy?'] = config['greedy?']
        d['___ε/τ'] = config['ε/τ']
        d['Q?'] = config['Q?']
        d['___α'] = config['α']
        d['___γ'] = config['γ']
        self._robot = robot.Robot(d)
        self._ror = ROBOT_S

    def fill(self, iw):
        """
        Fills the iw matrix with a part of the world, the part which will be
        shown on the GUI.

        That part will surely contain the robot within.
        """
        xs = max(filter(lambda x: x <= self._xr, NPOINTS))
        ys = max(filter(lambda y: y <= self._yr, MPOINTS))
        for i in range(N):
            for j in range(M):
                iw[i][j] = self._at(i + xs, j + ys)

    def _at(self, x, y):
        """
        Returns what can be found at x, y
        """
        if x == self._xr and y == self._yr:
            return self._ror
        if x < 0 or x >= self._N:
            return VOID
        if y < 0 or y >= self._M:
            return VOID
        return EMPTY

    def step(self):
        """
        Does one step of evolution. Calls robot's next_step method, giving
        him the reward and the new state.
        """
        act = self._robot.step()
        if act == FORWARD:
            self._forward()
        elif act == TURN_LEFT:
            self._turn_left()
        elif act == TURN_RIGTH:
            self._turn_right()

    def _forward(self):
        """
        Robot chose to go forward.
        """
# TODO: check for validity
        if self._ror == ROBOT_N:
            self._yr -= 1
        elif self._ror == ROBOT_E:
            self._xr += 1
        elif self._ror == ROBOT_S:
            self._yr += 1
        elif self._ror == ROBOT_W:
            self._xr -= 1

    def _turn_left(self):
        """
        Robot chose to turn left.
        """
        pass

    def _turn_right(self):
        """
        Robot chose to turn right.
        """
        pass

