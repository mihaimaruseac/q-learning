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
        self._crun = 0

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
        self._ror = self._oror = ROBOT_S

    def fill(self, iw):
        """
        Fills the iw matrix with a part of the world, the part which will be
        shown on the GUI.

        That part will surely contain the robot within.
        """
        xs = max(filter(lambda x: x <= self._xr, NPOINTS))
        ys = max(filter(lambda y: y <= self._yr, MPOINTS))
        for i in xrange(N):
            for j in xrange(M):
                iw[i][j] = self._at(i + xs, j + ys)

    def _at(self, x, y):
        """
        Returns what can be found at x, y
        """
        if x < 0 or x >= self._N or y < 0 or y >= self._M:
            return VOID
        if x == self._xr and y == self._yr:
            return self._ror
        return EMPTY

    def step(self):
        """
        Does one step of evolution. Calls robot's next_step method giving him
        the start state. After receiving robot's action, update state and send
        the newstate and reward to the robot.
        """
        # update count of steps in this epoch
        self._crun += 1
        if self._crun == self._runs:
            # reset state
            self._crun = 0
            self._xr, self._yr, self._ror = self._xs, self._ys, self._oror

        state = self._get_state()
        act = self._robot.step(state)
        if act == FORWARD:
            if self._ror % 2 == 1:
                self._yr += self._ror - 2
                if self._yr < 0:
                    self._yr = 0
                if self._yr >= self._M:
                    self._yr = self._M - 1
            else:
                self._xr += self._ror - 3
                if self._xr < 0:
                    self._xr = 0
                if self._xr >= self._N:
                    self._xr = self._N - 1
        elif act == TURN_LEFT:
            self._ror = 1 + self._ror % ROBOT_E
        elif act == TURN_RIGTH:
            self._ror = 1 + (self._ror - 2)% ROBOT_E

        newstate = self._get_state()
        reward = self._get_reward(newstate)
        self._robot.receive_reward_and_state(state, act, newstate, reward)

    def _get_state(self):
        """
        Returns the state for a specific position and orientation.
        """
        x, y, o = self._xr, self._yr, self._ror
        # assume that o = ROBOT_N (that is we are facing north)
        # compute the real distances
        state = [x, y, self._N - x - 1, self._M - y - 1]
        # trim to range
        for i in xrange(len(state)):
            if state[i] > self._D:
                state[i] = self._D
        # rotate state
        state = state[(o-1):] + state[:(o-1)]
#        state.append(o)
        return tuple(state)

    def _get_reward(self, state):
        """
        Returns the reward for a given state.
        """
        a = -10 # small negative value to discourage turnings

        # Penalty for being able to leave the grid
        p = -1000
        if state[FRONT] == 0:
            print 'able to leave'
            a += p

        # Penalty for being between the min value and the borders
        p = -5000
        if state[RIGHT] < self._d1:
            print 'too close'
            a += p

        # Penalty for being above the max value (toward the center of grid)
        p = -5000
        if state[RIGHT] > self._d2:
            print 'too far'
            a += p

        # Bonus for being in the correct corridor
        p = 100
        if self._d1 <= state[RIGHT] <= self._d2:
            print 'ok'
            a += p

        # Penalty for having a wrong orientation
        p = -100
        if state[RIGHT] > state[FRONT]:
            print 'turn'
            a += p
        if state[RIGHT] > state[FRONT]:
            print 'turn'
            a += p
        if state[RIGHT] > state[FRONT]:
            print 'turn'
            a += p

        return a

