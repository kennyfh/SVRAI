import numpy as np


class CartPole():

    def __init__(self, ) -> None :
        self.gravity=  9.8
        self.masscart= 1.
        self.masspole= .1
        self.total_mass = self.masspole + self.masscart
        self.length = .5  # actually half the pole's length
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.
        self.tau = .02

        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        high = np.array(
            [
                self.x_threshold * 2,
                np.finfo(np.float32).max,
                self.theta_threshold_radians * 2,
                np.finfo(np.float32).max,
            ],
            dtype=np.float32,
        )


    def get_actions(self, state):
        ...
  

    def is_terminal(self, state):
        ...

    def get_initial_state(self):
        ...


