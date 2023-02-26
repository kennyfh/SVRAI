from tabular_policy import TabularPolicy

class ValueFunction():

    def update(self, state, value):
        ...

    def merge(self, value_table):
        ...

    def get_value(self, state):
        ...

    """Devolver el valor de q por la acción del estado"""
    def get_q_value(self, model, state, action):
        q_value = 0.0
        for (new_state, probability) in model.get_transitions(state, action):
            reward = model.get_reward(state, action, new_state)
            q_value += probability * (
                reward
                + (model.get_discount_factor() * self.get_value(new_state))
            )

        return q_value
    
    """Devolver una política de esta función de valor"""
    def extract_policy(self, model):
        policy = TabularPolicy()
        for state in model.get_states():
            max_q = float("-inf")
            for action in model.get_actions(state):
                q_value = self.get_q_value(model, state, action)
                
                if q_value > max_q:
                    policy.update(state, action)
                    max_q = q_value

        return policy
