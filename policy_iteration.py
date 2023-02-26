from tqdm import tqdm
from tabular_policy import TabularPolicy
from tabular_value_function import TabularValueFunction
from qtable import QTable

"""
CLASE PARA DESARROLLAR EL ALGORITMO DE ITERACIÓN DE POLÍTICAS
"""

class PolicyIteration:
    def __init__(self, model, policy) -> None:
        self.model = model
        self.policy = policy

    def policy_evaluation(self, policy, values, theta:float=0.001):

        while True:
            delta = 0.0
            for state in self.model.get_states():
                # Calcula el valor de V(s)
                old_value = values.get_value(state)
                new_value = values.get_q_value(self.model, state, policy.select_action(state))
                values.update(state, new_value)
                delta = max(delta, abs(old_value - new_value))

            # Termina si la función converge
            if delta < theta:
                break

        return values

    """ Implementación del algoritmo de iteración de valores """

    def policy_iteration(self, max_iterations:int=100, theta:float=0.001) -> int:

        # Crea una función tabular para mantener los detalles
        values = TabularValueFunction()

        for i in range(1, max_iterations + 1):
        # for i in tqdm(range(1, max_iterations + 1), desc="Interaciones"):
            policy_changed = False
            values = self.policy_evaluation(self.policy, values, theta)

            for state in self.model.get_states():

                old_action = self.policy.select_action(state)
                q_values = QTable()

                for action in self.model.get_actions(state):
                    # Calcula el valor de Q(s,a)
                    new_value = values.get_q_value(self.model, state, action)
                    q_values.update(state, action, new_value)

                # V(s) = argmax_a Q(s,a)
                (new_action, _) = q_values.get_max_q(state, self.model.get_actions(state))
                self.policy.update(state, new_action)

                policy_changed = True if new_action is not old_action else policy_changed
        
            if not policy_changed:
                return i

        return max_iterations
