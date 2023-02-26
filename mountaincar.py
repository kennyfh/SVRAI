import math
import random
import time
from typing import List, Tuple
from matplotlib import pyplot as plt

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

    def get_initial_state(self) -> Tuple[float,float]:
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
        x_old, v_old = self.state

        reward = -1.
        cond = True if x_old >= self.max_x else False

        # Cambiados a un estado nuevo
        v = v_old + 0.001 * action - 0.0025 * np.cos(3*x_old)
        v = np.clip(v, -self.max_v, self.max_v)
        x = x_old + v
        x = np.clip(x,self.min_x,self.max_x)

        self.state = (x,v)

        return self.state, reward, cond

class ModelFreeMountainCar:

    
    def __init__(self, 
                 model, 
                 bandit, 
                 qfunction, 
                 alpha=0.1,
                 print_info=False) -> None :
        """ 
        Parámetros iniciales
        """
        
        self.model = model # Nuestro problema modelado
        self.bandit = bandit # Estrategia para aprender una política
        self.alpha = alpha # Nuestro factor de aprendizaje
        self.qfunction = qfunction
        self.INFO= print_info

        self.x_space = np.linspace(-1.2, 0.6, 28)
        self.v_space = np.linspace(-0.07, 0.07, 18)

        self.epsilon = 1.

    # https://link.springer.com/chapter/10.1007/978-3-031-21743-2_12
    def discretize_state(self,state:Tuple[float,float]) -> Tuple[int,int]:
        pos, vel =  state
        pos_bin = int(np.digitize(pos, self.x_space))
        vel_bin = int(np.digitize(vel, self.v_space))
        return (pos_bin, vel_bin)



    def execute(self, episodes=100) -> None :
        """
        Función que ejecuta el algoritmo libre de modelo
        """
        score = 0
        total_score = np.zeros(episodes)
        explore_rate_per_episode=[]
        for episode in range(episodes):

            self.bandit.epsilon = self.epsilon
            explore_rate_per_episode.append(self.epsilon)

            # Conseguimos el estado inicial
            state = self.discretize_state(self.model.get_initial_state())
            done = False

            # Para ir viendo como evolucionan los episodios
            if episode % 100 == 0:
                print(f'episode: {episode}, score: {score}, epsilon: {self.epsilon:0.3f}')

            score = 0

            while not done:
                # Elegimos la acción
                action = self.bandit.select(state, [-1,0,1], self.qfunction)
    
                # Calculamos el siguiente estado, recompensa y si ha finalizado
                observation, reward, done = self.model.execute(action)
                next_state = self.discretize_state(observation)
                score += reward
                
                # Calculamos el Q-Value
                # Obtenemos nueva acción
                next_action = self.bandit.select(next_state, [-1,0,1], self.qfunction)
                q_value = self.qfunction.get_q_value(state, action)
                
                # Actualizamos la tabla
                delta = self.get_delta(reward, q_value, state, next_state, next_action) # α*(r + γmax Q(s',a') - Q(s,a))
                #  Q(s,a) ← Q(s,a) + α*(r + γmax Q(s',a') - Q(s,a))
                self.qfunction.update(state, action, delta)

                # # Parámetros importantes
                if self.INFO:
                    print(f"Episodio número: {episode+1}")
                    print(f"Acción seleccionada: {str(action)}")
                    print(f"Estado actual: {str(state)}")
                    print(f"Recompensa ganada: {str(reward)}")            
                    print("===========================================")

                time.sleep(0.03)

                # Nuevo estado
                state = next_state
                action = next_action
                
            # Save score for this episode
            total_score[episode] = score
            # Reduce epsilon 
            self.epsilon = self.epsilon - 2/episodes if self.epsilon > 0.01 else 0.01

        # Graficamos los datos
        fig, axs = plt.subplots(2, figsize=(10, 10))
        fig.suptitle("Resultados del entrenamiento")
        axs[0].plot(total_score)
        axs[0].set_ylabel('Recompensa por episodio')
        axs[1].plot(explore_rate_per_episode)
        axs[1].set(xlabel='Episodios', ylabel='Tasa de exploración (epsilon)')
        plt.show()
            
    """ Calcular el delta para la actualización """

    def get_delta(self, reward, q_value, state, next_state, next_action):
        next_state_value = self.state_value(next_state, next_action)
        delta = reward + self.model.discount_factor * next_state_value - q_value
        return self.alpha * delta

    """ Obtener el valor de un estado (esto es lo que deberán implementar los diferentes métodos)"""
    def state_value(self, state, action):
        ...

class QLearningMountainCar(ModelFreeMountainCar):
    def state_value(self, state, action):
        (_, max_q_value) = self.qfunction.get_max_q(
            state, self.model.get_actions(state))
        return max_q_value


class SARSAMountainCar(ModelFreeMountainCar):
    def state_value(self, state, action):
        return self.qfunction.get_q_value(state, action)
