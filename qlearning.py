from model_free_RL import ModelFreeRL


class QLearning(ModelFreeRL):
    def state_value(self, state, action):
        (_, max_q_value) = self.qfunction.get_max_q(state, self.mdp.get_actions(state))
        return max_q_value