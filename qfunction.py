from tabular_policy import TabularPolicy


class QFunction:

    """ Actualiza el valor Q de (estado, acción) por delta"""

    def update(self, state, action, delta):
        ...

    """ Obtiene un valor Q para un par estado-acción dado """

    def get_q_value(self, state, action):
        ...

    """ Devuelve un par que contiene la acción y el valor Q, donde la acción 
        tiene el máximo valor Q en el estado
    """

    def get_max_q(self, state, actions):
        arg_max_q = None
        max_q = float("-inf")
        for action in actions:
            value = self.get_q_value(state, action)
            if max_q < value:
                arg_max_q = action
                max_q = value
        return (arg_max_q, max_q)

    """ Extrae la política de la Q-function  """

    def extract_policy(self, mdp):
        policy = TabularPolicy()
        for state in mdp.get_states():
            # Find the action with maximum Q-value and make this the
            (action, _) = self.get_max_q(state, mdp.get_actions(state))
            policy.update(state, action)

        return policy
