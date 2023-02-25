from tqdm import tqdm

"""
Marco genérico para algoritmos de aprendizaje por refuerzo libres de modelo
"""

class GenericModelFreeRL:

    """ Parámetros iniciales"""
    def __init__(self, 
                 model, 
                 bandit, 
                 qfunction, 
                 alpha=0.1,
                 print_params=False) -> None :
        
        self.model = model # Nuestro problema modelado
        self.bandit = bandit # Estrategia para aprender una política
        self.alpha = alpha # Nuestro factor de aprendizaje
        self.qfunction = qfunction

        self.print_params = print_params

    """ Función que ejecuta el algoritmo libre de modelo"""

    def execute(self, episodes=100) -> None :

        for _ in tqdm(range(episodes), desc="Episodes"):
            # Conseguimos el estado inicial
            state = self.model.get_initial_state()
            actions = self.model.get_actions(state)
            # Elegimos la acción
            action = self.bandit.select(state, actions, self.qfunction)

            while (not self.model.is_terminal(state)):
                next_state, reward = self.model.execute(state, action)
                actions = self.model.get_actions(next_state)
                next_action = self.bandit.select(next_state, actions, self.qfunction)
                q_value = self.qfunction.get_q_value(state, action)
                delta = self.get_delta(reward, q_value, state, next_state, next_action)
                self.qfunction.update(state, action, delta)
                state = next_state
                action = next_action

            if self.print_params:
                # Imprimimos parámetros importantes
                print(f"Episodio número: {episodes}")
                print(f"Acción seleccionada: {str(action)}")
                print(f"Estado actual: {str(state)}")
                print(f"Recompensa ganada: {str(reward)}")            
                print("===========================================")

            
    """ Calcular el delta para la actualización """

    def get_delta(self, reward, q_value, state, next_state, next_action):
        next_state_value = self.state_value(next_state, next_action)
        delta = reward + self.model.discount_factor * next_state_value - q_value
        return self.alpha * delta

    """ Obtener el valor de un estado (esto es lo que deberán implementar los diferentes métodos)"""
    def state_value(self, state, action):
        ...


class QLearning(GenericModelFreeRL):
    def state_value(self, state, action):
        (_, max_q_value) = self.qfunction.get_max_q(state, self.model.get_actions(state))
        return max_q_value

class SARSA(GenericModelFreeRL):
    def state_value(self, state, action):
        return self.qfunction.get_q_value(state, action)
