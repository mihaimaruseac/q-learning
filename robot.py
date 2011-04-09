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
        self._Q_or_SARSA = config['Q?']
        self._alpha = config['___α']
        self._gamma = config['___γ']

        # state, action utility dictionary
        self._Q = {}

    def step(self, state):
        """
        Does a single step (takes an action).
        """
        # Chose action from state
        if self._Q.has_key(state):
            act = self._Q[state]
            return act[0]
        return FORWARD

    def receive_reward_and_state(self, olds, news, r):
        """
        Receive a reward after taking an action from olds state, reaching news
        state. Basically, learn (state,action) utilities.
        """
        pass

