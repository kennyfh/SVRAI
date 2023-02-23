import math
import random
from typing import List, Tuple

import numpy as np

class MountainCar:

    """
    Clase que establece los parámetros necesarios para simular el problema del coche en la montaña.
    """

    def __init__(self) -> None:
        """
        Inicializa los parámetros del problema.
        """

        self.min_x = -1.2 # x ∈ [−1.2,0.6]
        self.max_x = 0.6
        self.max_v = 0.07 # v∈[−0.07,0.07]
        self.discount_factor=0.9 # Factor de descuento

    def get_initial_state(self) -> Tuple[float,float]:
        """
        Devuelve el estado inicial del problema.

        Returns:
            Una tupla con la posición y velocidad inicial del coche. Se ha decidido asignar un valor
            extraído de una distribución uniforme para que la posición inicial no siempre valga 0
        """
        x = random.uniform(-0.6, -0.4)
        return (x,0.)

    def get_actions(self,state) -> List[int]:
        """
        Devuelve una lista con las acciones posibles en el estado actual.

        Args:
            state: El estado actual.

        Returns:
            Una lista con las acciones posibles (-1, 0, 1).
                -1  -> Acelenar a la izquierda
                0  -> Dejarse llevar por la inercia
                1  -> Acelerar a la derecha
        """
        return [-1,0,1]

    def is_terminal(self,state:Tuple[float,float]) -> bool:
        """
        Comprueba si el estado actual es terminal.

        Args:
            state (Tuple[float,float]): El estado actual.

        Returns:
            True si el estado es terminal, False en otro caso.
        """
        x,_ = state
        return x >= 0.6

    def execute(self,state:Tuple[float,float],action:int) -> Tuple[Tuple[float,float],float]:
        """
        Ejecuta la acción dada en el estado actual y devuelve el siguiente estado
        y la recompensa obtenida.

        Args:
            state (Tuple[float,float]): El estado actual.
            action (int): La acción a realizar.

        Returns:
            Una tupla con el siguiente estado y la recompensa obtenida.
        """
        # Posición actual del carro, velocidad
        x_act,v_act = state

        # Cálculo de pos y velocidad siguiente
        # v′ <- v+0.001 a−0.0025cos(3x)
        v_new = v_act + (0.001*action) - (0.0025*math.cos(3*x_act))
        # Recortamos la velocidad para que no se pase del intervalo
        v_new = np.clip(v_act, -self.max_v, self.max_v)
        # X' <- x + v'
        x_new = x_act + v_new
        x_new = np.clip(x_act, self.min_x, self.max_x)

        next_state = (x_new,v_new)

        reward = 0 if self.is_terminal(next_state) else -1

        return next_state, reward

    
# if __name__ == "__main__":
#     mountaincar = MountainCar()
#     qfunction = QTable()
#     qlearning = QLearning(mountaincar, Softmax(), qfunction, alpha =0.2)
#     qlearning.execute(episodes=200)
#     print(qfunction.qtable)

