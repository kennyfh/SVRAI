import math
import random
from typing import List, Tuple
from multi_armed_bandit import Softmax
from qlearning import QLearning

from qtable import QTable
from sarsa import SARSA
import numpy as np


class MountainCar:
    def __init__(self) -> None:
        # Rango de la posición horizontal del vehículo
        # x∈[−1.2,0.6]
        self.min_x = -1.2
        self.max_x = 0.6
        # Máxima velocidad
        # v∈[−0.07,0.07]
        self.max_v = 0.07
        self.discount_factor=0.9

    def get_initial_state(self) -> Tuple[float,float]:
        """
        Para que no siempre la posición inicial valga 0, 
        se ha decidido asignarle un valor extraído de una
        distribución uniforme U(-0.1,0.1).

        La velocidad inicial siempre va a ser 0
        """
        x = random.uniform(-0.6, -0.4)
        return (x,0.)

    def get_actions(self,state) -> List[int]:
        """
        -1  -> Acelenar a la izquierda
         0  -> Dejarse llevar por la inercia
         1  -> Acelerar a la derecha
        """
        return [-1,0,1]

    def is_terminal(self,state) -> bool:
        x,_ = state
        return x >= 0.6

    def execute(self,state,action) -> Tuple[Tuple[float,float],float]:
        # Posición actual del carro, velocidad
        x_act,v_act = state

        # Cálculo de pos y velocidad siguiente
        # v′ <- v+0.001 a−0.0025cos(3x)
        v_new = v_act + (0.001*action) - (0.0025*math.cos(3*x_act))
        # Recortamos la velocidad para que no se pase del intervalo
        v_new = max(-self.max_v, min(v_new, self.max_v))
        # X' <- x + v'
        x_new = x_act + v_new
        x_new = max(self.min_x, min(x_new,self.min_x))

        next_state = (x_new,v_new)

        reward = 0 if self.is_terminal(next_state) else -1

        return next_state, reward

    
if __name__ == "__main__":
    mountaincar = MountainCar()
    qfunction = QTable()
    qlearning = QLearning(mountaincar, Softmax(), qfunction, alpha =0.2)
    qlearning.execute(episodes=200)
    print(qfunction.qtable)

