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


    def execute(self, state, action):
        rand = random.random()
        cumulative_probability = 0.0
        for (new_state, probability) in self.get_transitions(state, action):
            if cumulative_probability <= rand <= probability + cumulative_probability:
                return (new_state, self.get_reward(state, action, new_state))
            cumulative_probability += probability
            if cumulative_probability >= 1.0:
                raise (
                    "Cumulative probability >= 1.0 for action "
                    + str(action)
                    + " from "
                    + str(state)
                )

        raise (
            "No outcome state in simulation for action"
            + str(action)
            + " from "
            + str(state)
        )