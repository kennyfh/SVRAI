
import math
import random
from multi_armed_bandit import EpsilonGreedy
from qlearning import QLearning

from qtable import QTable

class CartPole:
    def __init__(self) -> None:
        self.discount_factor=0.9
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masspole + self.masscart
        self.length = 0.5  # actually half the pole's length
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02  # seconds between state updates

        # Rangos donde puede fallar el problema
        self.theta_threshold = -12 * 2 * math.pi
        self.x_threshold = 2.4
    

    def get_initial_state(self):
        x = random.uniform(-0.05, 0.05)
        x_dot = random.uniform(-0.05, 0.05)
        theta = random.uniform(-0.05, 0.05)
        theta_dot= random.uniform(-0.05, 0.05)

        return (x, x_dot, theta, theta_dot)
        

    def get_actions(self,state):
        return [0,1]

    def is_terminal(self,state):
        x, _, theta, _ = state
        return x < -self.x_threshold or x > self.x_threshold \
            or theta < -self.theta_threshold or theta > self.theta_threshold



    def execute(self,state,action):
        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (
            force + self.polemass_length * theta_dot**2 * sintheta
        ) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.masspole * costheta**2 / self.total_mass)
        )
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        
        x = x + self.tau * x_dot,
        x_dot = x_dot + self.tau * xacc,
        theta = theta + self.tau * theta_dot,
        theta_dot = theta_dot + self.tau * thetaacc
        next_state = (x,x_dot,theta,theta_dot)

        reward = 0

        if not self.is_terminal(next_state):
            reward = 1 if abs(x) < self.x_threshold \
                      and abs(theta) < self.theta_threshold else 0


        return next_state, reward

if __name__ == "__main__":
    cartpole = CartPole()
    qfunction = QTable()
    QLearning(cartpole, EpsilonGreedy(), qfunction).execute(episodes=100)
    print(qfunction.qtable)
