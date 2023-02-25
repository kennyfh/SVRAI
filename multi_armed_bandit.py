import math
import random

"""
Clase que proporciona las estrategias del MultiArmedBandit
que pretenden aprender una política que minimice el arrepentimiento total

"""
class MultiArmedBandit():

    """ Select an action for this state given from a list given a Q-function """

    def select(self, state, actions, qfunction):
        ...

    """ Reset a multi-armed bandit to its initial configuration """

    def reset(self):
        self.__init__()


"""
Exploración ϵ-voraz (Epsilon-Greedy) es una estrategia que selecciona la acción conocida
con una probabilidad (1-epsilon) y una opción aleatoria epsion. Esto
nos permite explorar nuevas opciones con cierta frecuencia.

Esto se debe usar en problemas donde el número de opciones es
relativamente pequeño.

"""
class EpsilonGreedy(MultiArmedBandit):

    def __init__(self, epsilon=0.1) -> None:
        self.epsilon = epsilon

    def reset(self):
        pass

    def select(self, state, actions, qfunction):
        # Select a random action with epsilon probability
        if random.random() < self.epsilon:
            return random.choice(actions)
        (arg_max_q, _) = qfunction.get_max_q(state, actions)
        return arg_max_q
    
"""
Softmax es una estrategia que  hace uso de una distribución de probabilidad 
softmax para seleccionar una de las acciones. 
"""
class Softmax(MultiArmedBandit):
    def __init__(self, tau=1.0) -> None:
        self.tau = tau

    def reset(self):
        pass

    def select(self, state, actions, qfunction):

        # calculate the denominator for the softmax strategy
        total = 0.0
        for action in actions:
            total += math.exp(qfunction.get_q_value(state, action) / self.tau)

        rand = random.random()
        cumulative_probability = 0.0
        result = None
        for action in actions:
            probability = (
                math.exp(qfunction.get_q_value(state, action) / self.tau) / total
            )
            if cumulative_probability <= rand <= cumulative_probability + probability:
                result = action
            cumulative_probability += probability

        return result
    

"""
Upper Confidence Bound (UCB) es una estrategia enfocado en la
incertidumbre para poder equilibrar la exploración y la explotación
"""
class UpperConfidenceBounds(MultiArmedBandit):
    def __init__(self) -> None:
        self.total = 0
        # Número de veces que una acción ha sido seleccionada
        self.times_selected = {}

    def select(self, state, actions, qfunction):
        for action in actions:
            if action not in self.times_selected.keys():
                self.times_selected[action] = 1
                self.total += 1
                return action

        max_actions = []
        max_value = float("-inf")
        for action in actions:
            value = qfunction.get_q_value(state, action) + math.sqrt(
                (2 * math.log(self.total)) / self.times_selected[action]
            )
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        # Si hay varias acciones con el valor más alto,
        # se selecciona una al azar
        result = random.choice(max_actions)
        self.times_selected[result] = self.times_selected[result] + 1
        self.total += 1
        return result