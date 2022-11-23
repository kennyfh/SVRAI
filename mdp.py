import numpy as np


class Search():
    """
    struct Search
    𝒮 # state space
    𝒜 # valid action function
    T # transition function
    R # reward function
    end
    """

    def __init__(self, state,action,transition, reward) -> None:
        # TODO: modify this
        self.state = state
        self.action = action
        self.transition = transition
        self.reward = reward
