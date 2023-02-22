"""
CLASE QUE PERMITE LA CREACIÓN DE MODELOS DE MARKOV PARA EL PARADIGMA BASADO EN MODELOS
(aunque se permite el uso de algoritmos libres de modelo)
"""

import random


class MDP:

    """
    CLASE MDP

    * Si algún MDP se quiere hacer uso de algoritmos libres de modelo, los algoritmos descartarán las
    funciones get_states, get_transitions y get_rewards
    
    """

    """ Devuelve todos los estados del MDP"""
    def get_states(self):
        ...

    """ Devolvemos True si llegamos a un estado que finalice"""
    def is_terminal(self, state):
        ...

    """ Devolvemos el factor de descuento """
    def get_discount_factor(self):
        ...

    """ Se devuelve el estados """
    def get_initial_state(self):
        ...

    """ Se devuelve todos los estado objetivo """
    def get_goal_states(self):
        ...
    
    """ Devuelve todas las acciones de un estado con una probabilidad distinta de nula"""
    def get_actions(self, state):
        ...

    """ Return all non-zero probability transitions for this action
        from this state, as a list of (state, probability) pairs
    """
    def get_transitions(self, state, action):
        ...

    """ Return the reward for transitioning from state to
        nextState via action
    """
    def get_reward(self, state, action, next_state):
        ...

    """ Devuelve un nuevo estado y la recompensa. Esto se puede usar para el paradigma
    de aprendizaje sin modelo."""
    def execute(self, state, action):
        rand = random.random()
        cumulative_probability = 0.0
        for (new_state, probability) in self.get_transitions(state, action):
            if cumulative_probability <= rand <= probability + cumulative_probability:
                return (new_state, self.get_reward(state, action, new_state))
            cumulative_probability += probability
            if cumulative_probability >= 1.0:
                raise (
                    "Probabilidad acumulada >= 1,0 para la acción "
                    + str(action)
                    + " del estado "
                    + str(state)
                )

        raise (
            "No hay estado de resultado en la simulación para la acción"
            + str(action)
            + " del estado "
            + str(state)
        )