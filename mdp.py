import random


class MDP:
    """
    Clase que permite la creación de Modelos de Markov para el paradigma basado en modelos
    (aunque también permite el uso de algoritmos libres de modelo).
    """

    def get_states(self):
        """
        Devuelve una lista con todos los estados posibles del modelo de Markov.

        Returns:
        states: Una lista de los estados posibles del modelo de Markov.
        """
        ...

    def is_terminal(self, state):
        ...

    def get_discount_factor(self):
        ...

    def get_initial_state(self):
        ...

    def get_goal_states(self):
        ...
    
    def get_actions(self, state):
        ...


    def get_transitions(self, state, action):
        ...


    def get_reward(self, state, action, next_state):
        """
        Devuelve la recompensa asociada a pasar del estado actual al siguiente estado
        con la acción actual.

        Args:
            state: El estado actual.
            action: La acción actual.
            next_state: El siguiente estado.

        Returns:
            La recompensa asociada a pasar del estado actual al siguiente estado con la acción actual.
        """
        ...


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