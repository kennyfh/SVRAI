import math
import random
import time
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
        self.state = None

        self.upper_bounds = [self.max_x,self.max_v]
        self.lower_bounds = [self.min_x,-self.max_v]

    def get_initial_state(self):
        """
        Devuelve el estado inicial del problema.

        Returns:
            Una tupla con la posición y velocidad inicial del coche. Se ha decidido asignar un valor
            extraído de una distribución uniforme para que la posición inicial no siempre valga 0
        """
        x = random.uniform(-0.6, -0.4)
        self.state = (x,0.)
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


    def execute(self,action:int):
        """
        Ejecuta la acción dada en el estado actual y devuelve el siguiente estado
        y la recompensa obtenida.

        Args:
            state (Tuple[float,float]): El estado actual.
            action (int): La acción a realizar.

        Returns:
            Una tupla con el siguiente estado,la recompensa obtenida y condición si ha terminado
        """
        # Posición actual del carro, velocidad
        x_act,v_act = self.state

        # Cálculo de pos y velocidad siguiente
        v_new = v_act + (0.001*action) - (0.0025*math.cos(3*x_act))
        # Recortamos la velocidad para que no se pase del intervalo
        v_new = max(-self.max_v, min(v_new, self.max_v))
        # X' <- x + v'
        x_new = x_act + v_new
        x_new = max(self.min_x, min(x_new,self.min_x))
        if x_new == self.min_x and v_new < 0:
            v_new = 0

        self.state = (x_new,v_new)
        cond = x_new >= .6 and v_new >=0
        reward = -1.

        return self.state, reward, cond

class QLearningMountainCar:

    
    def __init__(self, 
                 model, 
                 bandit, 
                 qfunction, 
                 alpha=0.1) -> None :
        """ 
        Parámetros iniciales
        """
        
        self.model = model # Nuestro problema modelado
        self.bandit = bandit # Estrategia para aprender una política
        self.alpha = alpha # Nuestro factor de aprendizaje
        self.qfunction = qfunction

        self.x_space = np.linspace(-1.2, 0.6, 12)
        self.v_space = np.linspace(-0.07, 0.07, 20)

    # https://link.springer.com/chapter/10.1007/978-3-031-21743-2_12
    def discretize_state(self,state):
        pos, vel =  state
        pos_bin = int(np.digitize(pos, self.x_space))
        vel_bin = int(np.digitize(vel, self.v_space))
        return (pos_bin, vel_bin)


    """ Función que ejecuta el algoritmo libre de modelo"""

    def execute(self, episodes=100) -> None :
        for episode in range(episodes):

            # Conseguimos el estado inicial
            state = self.discretize_state(self.model.get_initial_state())
            done = False

            while not done:
                # Elegimos la acción
                actions = self.model.get_actions(state)
                action = self.bandit.select(state, actions, self.qfunction)
    
                # Calculamos el siguiente estado, recompensa y si ha finalizado
                next_state, reward, done = self.model.execute(action)
                next_state = self.discretize_state(next_state)
                
                # Calculamos el Q-Value
                actions = self.model.get_actions(next_state)
                next_action = self.bandit.select(next_state, actions, self.qfunction)
                q_value = self.qfunction.get_q_value(state, action)
                
                # Actualizamos la tabla
                delta = self.get_delta(reward, q_value, state, next_state, next_action)
                self.qfunction.update(state, action, delta)

                # Parámetros importantes
                print(f"Episodio número: {episode+1}")
                print(f"Acción seleccionada: {str(action)}")
                print(f"Estado actual: {str(state)}")
                print(f"Recompensa ganada: {str(reward)}")            
                print("===========================================")

                time.sleep(0.03)

                if done:
                    print("Lo hemos LOGRADO")
                    break
                state = next_state
                action = next_action

            
    """ Calcular el delta para la actualización """

    def get_delta(self, reward, q_value, state, next_state, next_action):
        next_state_value = self.state_value(next_state, next_action)
        delta = reward + self.model.discount_factor * next_state_value - q_value
        return self.alpha * delta

    """ Obtener el valor de un estado (esto es lo que deberán implementar los diferentes métodos)"""
    def state_value(self, state, action):
        (_, max_q_value) = self.qfunction.get_max_q(state, self.model.get_actions(state))
        return max_q_value



    
