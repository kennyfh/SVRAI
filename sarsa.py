from model_free_RL import ModelFreeRL

"""
Clase que implementa el algoritmo SARSA
(paradigma libre de modelo)
"""

class SARSA(ModelFreeRL):
    def state_value(self, state, action):
        return self.qfunction.get_q_value(state, action)
