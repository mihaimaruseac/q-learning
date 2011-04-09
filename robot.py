# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

from globaldefs import *

class Robot(object):
    """
    A robot which should navigate in a world.
    """

    def __init__(self, config):
        """
        Construct a new robot, passing several configurations to him.

        config  The user configurations which affect the robot.
        """
        self._greedy = config['greedy?']
        self._eps_or_tau = config['___ε/τ']
        self._Q = config['Q?']
        self._alpha = config['___α']
        self._gamma = config['___γ']

    def step(self, state):
        """
        Does a single step (takes an action).
        """
        return FORWARD

