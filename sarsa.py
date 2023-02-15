from model_free_RL import ModelFreeRL

class SARSA(ModelFreeRL):
    def state_value(self, state, action):
        return self.qfunction.get_q_value(state, action)
