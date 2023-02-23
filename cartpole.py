
import math
import random
import numpy as np
from typing import List, Tuple

class CartPole:

    """
    Clase que establece los parámetros necesarios para simular el problema CartPole.
    """

    def __init__(self,
                 buckets=(1, 1, 3, 6)) -> None:
        self.discount_factor=0.9
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masspole + self.masscart
        self.length = 0.5
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02

        # Rangos donde puede fallar el problema
        self.theta_threshold = 12 * 2 * math.pi
        self.x_threshold = 2.4

        # https://eprints.ucm.es/id/eprint/56648/1/1138035127-327684_JUAN_RAM%C3%93N_DEL_CA%C3%91O_VEGA_Aprendizaje_por_refuerzo_profundo_aplicado_a_juegos_sencillos_3940146_998640412.pdf
        self.buckets = buckets

        # Limites: [Posición del carro, Velocidad del carro, Ángulo del poste, Velocidad angular del poste]
        self.upper_bounds = [4.8, 0.5, .418, math.radians(50)]
        self.lower_bounds = [-4.8, -0.5, -.418,-math.radians(50)]

        self.steps_beyond_terminated = None
    

    def get_initial_state(self):
        """Devuelve un estado inicial aleatorio para la simulación.

        Returns:
            Una tupla que contiene los valores del estado inicial aleatorio.
        """
        x = random.uniform(-0.05, 0.05) # Posición del carro
        x_dot = random.uniform(-0.05, 0.05) # Velocidad del carro
        theta = random.uniform(-0.05, 0.05) # Ángulo del poste
        theta_dot= random.uniform(-0.05, 0.05) # Velocidad angular del poste

        return self.discretize_state((x, x_dot, theta, theta_dot))
        

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

    def is_terminal(self,state) -> bool:
        """Indica si el estado es terminal o no.

        Args:
            state: Una tupla que contiene los valores del estado actual.

        Returns:
            bool: True si se pasa de cierto ángulo de inclinación y 
            no se encuentra dentro de los límites laterales y False en caso contrario
        """
        x, _, theta, _ = state
        return x < -self.x_threshold or x > self.x_threshold \
            or theta < -self.theta_threshold or theta > self.theta_threshold
    


    def discretize_state(self,state):
        """
        Discretización del estado según un tipo de bucket
        """
        ratios = [(state[i] + self.upper_bounds[i]) / (self.upper_bounds[i] - self.lower_bounds[i]) for i in range(len(state))]
        classified_state = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(state))]
        classified_state = [min(self.buckets[i] - 1, max(0, classified_state[i])) for i in range(len(state))]

        return tuple(classified_state)


    def execute(self,state,action:int):
        """Ejecuta la acción dada en el estado actual y devuelve la siguiente tupla de estado-recompensa.

        Args:
            state: Una tupla que contiene los valores del estado actual.
            action (int): Un valor entero que representa la acción que se va a ejecutar.

        Returns:
            Una tupla que contiene el siguiente estado y la recompensa.
        """
        x, x_dot, theta, theta_dot = state
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

        next_state = self.discretize_state((x,x_dot,theta,theta_dot))

        if not self.is_terminal(next_state):
            reward =1.
        elif self.steps_beyond_terminated is None:
            self.steps_beyond_terminated = 0
            reward = 1.
        else:
            if self.steps_beyond_terminated ==0:
                print("No deberías volver porqu8e ya has llegado a un estado terminal")
            self.steps_beyond_terminated += 1
            reward = 0.0

        return next_state, reward

