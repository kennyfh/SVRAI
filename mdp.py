"""
MARKOV CHAIN CLASS
"""

import random


class MDP:
    """ Return all states of this MDP """
    def get_states(self):
        ...

    """ Return all actions with non-zero probability from this state """
    def get_actions(self, state):
        ...

    """ Return all non-zero probability transitions for this action
        from this state, as a list of (state, probability) pairs
    """
    def get_transitions(self, state, action):
        ...

    """ Return the reward for transitioning from state to
        nextState via action
    """
    def get_reward(self, state, action, next_state):
        ...

    """ Return true if and only if state is a terminal state of this MDP """
    def is_terminal(self, state):
        ...

    """ Return the discount factor for this MDP """
    def get_discount_factor(self):
        ...

    """ Return the initial state of this MDP """
    def get_initial_state(self):
        ...

    """ Return all goal states of this MDP """
    def get_goal_states(self):
        ...
