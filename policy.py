"""
POLICY CLASS
"""
class Policy:
    def select_action(self, state):
        ...


class DeterministicPolicy(Policy):
    def update(self, state, action):
        ...


class StochasticPolicy(Policy):
    def update(self, states, actions, rewards):
        ...

    def get_probability(self, state, action):
        ...
