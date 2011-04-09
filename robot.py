# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import random

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

        # decided upon action (when using SARSA)
        self.__a__ = None

    def step(self, state):
        """
        Does a single step (takes an action).

        state   Current state
        return  Action
        """
        # Chose action from state
        if self._Q.has_key(state):
            a = self._choose_action(self._Q[state])
        else:
            self._Q[state] = {FORWARD:0, TURN_LEFT:0, TURN_RIGHT:0}
            a = random.choice(self._Q[state].keys())
#        print 'From state {0}, chose {1}'.format(state, a)
        return a

    def receive_reward_and_state(self, olds, a, news, r):
        """
        Receive a reward after taking an action from olds state, reaching news
        state. Basically, learn (state,action) utilities.

        olds    Old state
        a       Action taken in that state
        news    New state
        r       Reward given
        """
#        print 'From state {0}, chose {1}, got to {2} with reward {3}'.\
#            format(olds, a, news, r)
        if not self._Q.has_key(news):
            q = 0
        elif self._Q_or_SARSA:
            # Q learning
            d = self._Q[news]
            q = max(zip(d.values(), d.keys()))[0]
        else:
            # SARSA
            q = self._Q[news][self._choose_action(self._Q[news], True)]
        qa = self._Q[olds][a]
        self._Q[olds][a] += self._alpha * (r + self._gamma * q - qa)
#        print 'Now Q is {0}'.format(self._Q)

    def _choose_action(self, actions, future=False):
        """
        Choose an action from the list of actions and their rewards (a
        dictionary to be more exact).

        actions Dictionary containing each possible action and its value.
        future  True if using SARSA and this call is only prospective (in
                which case, the same action should be returned on the next
                call, which will have future=False).
        """
        a = actions.keys()[0]
        if self._greedy:
            # ε-greedy selection
            tmp = random.uniform(0, 1)
            if tmp > self._eps_or_tau:
                a = max(zip(actions.values(), actions.keys()))[1]
            else:
                a = random.choice(actions.keys())
        if future:
            self.__a__ = a
        elif self.__a__:
            a = self.__a__ #take the generated action
            self.__a__ = None
        return a

