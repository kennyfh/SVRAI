
import math
import random
import time
import numpy as np
from typing import List, Tuple

class CartPole:

    """
    Clase que establece los parámetros necesarios para simular el problema CartPole.
    """

    def __init__(self,
                 buckets=(1, 1, 6, 3)) -> None:
        """
        Inicialización de la clase
        """
        self.discount_factor= .9  #0.9
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masspole + self.masscart
        self.length = 0.5
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02

        self.steps_beyond_terminated = None
        self.state = None
    

    def get_initial_state(self):
        """Devuelve un estado inicial aleatorio para la simulación.

        Returns:
            Una tupla que contiene los valores del estado inicial aleatorio.
        """
        x = random.uniform(-0.05, 0.05) # Posición del carro
        x_dot = random.uniform(-0.05, 0.05) # Velocidad del carro
        theta = random.uniform(-0.05, 0.05) # Ángulo del poste
        theta_dot= random.uniform(-0.05, 0.05) # Velocidad angular del poste
        self.state= (x, x_dot, theta, theta_dot)
        return (x, x_dot, theta, theta_dot)
        

    def get_actions(self,state) -> List[int]:
        """Devuelve una lista de posibles acciones que se pueden tomar en el estado actual.

        Args:
        state : Una tupla que contiene los valores del estado actual.

        Returns:
        List[int]: Posibles acciones que puede tomar
            0 -> Empujar el carro hacia la izquierda
            1 -> Empujar el carro hacia la derecha
        """
        return [0,1]
    

    def execute(self,action:int):
        """Ejecuta la acción dada en el estado actual y devuelve la siguiente tupla de estado-recompensa.

        Args:
            state: Una tupla que contiene los valores del estado actual.
            action (int): Un valor entero que representa la acción que se va a ejecutar.

        Returns:
            Una tupla que contiene el siguiente estado y la recompensa.
        """
        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag


        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        temp = (force + self.polemass_length * theta_dot**2 * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.masspole * costheta**2 / self.total_mass))
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc

        self.state = (x,x_dot,theta,theta_dot)

        terminated = x < -2.4 or x > 2.4 or theta < -12 * 2 * math.pi / 360 or theta > 12 * 2 * math.pi / 360

        if not terminated:
            reward = 1.0
            self.steps_beyond_terminated = None

        elif self.steps_beyond_terminated is None:
            # Pole just fell!
            self.steps_beyond_terminated = 0
            reward = 1.0
        else:
            if self.steps_beyond_terminated == 0:
                print("Pole just fell!")
            self.steps_beyond_terminated += 1
            reward = 0.0

        return self.state, reward, terminated
    

class QLearningCartPole:

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
        self.buckets = (1,1,6,3)

        # Limites: [Posición del carro, Velocidad del carro, Ángulo del poste, Velocidad angular del poste]
        self.upper_bounds = [4.8, 0.5, math.radians(24), math.radians(50)]
        self.lower_bounds = [-4.8, -0.5, math.radians(-24), -math.radians(50)]

        self.state_value_bounds = list(zip(self.lower_bounds,self.upper_bounds))


    # https://arxiv.org/abs/2006.04938
    def discretize_state(self,state_value) -> List[int]:
        bucket_indices = []
        for i in range(len(state_value)):
            if state_value[i] <= self.state_value_bounds[i][0]:
                bucket_index = 0
            elif state_value[i] >= self.state_value_bounds[i][1]:
                bucket_index = self.buckets[i] - 1
            else:
                bound_width = self.state_value_bounds[i][1] - self.state_value_bounds[i][0]
                offset = (self.buckets[i]-1) * self.state_value_bounds[i][0] / bound_width
                scaling = (self.buckets[i]-1) / bound_width
                bucket_index = int(round(scaling*state_value[i] -offset))
            bucket_indices.append(bucket_index)
        return(tuple(bucket_indices))


    def execute(self, episodes=100) -> None :
        max_time_steps = 250
        solved_time = 199
        no_streaks = 0

        for episode in range(episodes):

            # Conseguimos el estado inicial
            state = self.discretize_state(self.model.get_initial_state())

            for time_step in range(max_time_steps):
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
                    print("===================================")
                    print(f"Episodio {episode} finalizado tras {time_step} pasos de tiempo")
                    print("===================================")
                    if time_step >= solved_time:
                        no_streaks += 1
                    else:
                        no_streaks = 0
                    break

                
                state = next_state
                action = next_action
                

            
    """ Calcular el delta para la actualización """

    def get_delta(self, reward, q_value, state, next_state, next_action):
        next_state_value = self.state_value(next_state, next_action)
        delta = reward + self.model.discount_factor * next_state_value - q_value
        return self.alpha * delta

    """ Q-learning"""
    def state_value(self, state, action):
        (_, max_q_value) = self.qfunction.get_max_q(state, self.model.get_actions(state))
        return max_q_value

# if __name__ == "__main__":
#     from qtable import QTable
#     from multi_armed_bandit import EpsilonGreedy
#     cartpole = CartPole()
#     qfunction = QTable()
#     QLearningCartPole(cartpole, EpsilonGreedy(), qfunction).execute(episodes=1000)