"""
POLICY GRADIENT 
"""
from tqdm import tqdm


class PolicyGradient:
    
    """Inicio de la clase"""
    def __init__(self, model, policy, alpha) -> None:
        super().__init__()
        self.alpha = alpha  # Tasa de aprendizaje
        self.model = model # Modelo de nuestro problema MDP
        self.policy = policy # Política

    """ Genera y almacena una trayectoria de episodios completa para utilizarla en la actualización de la política."""

    def execute(self, episodes=100):
        for _ in tqdm(range(episodes), desc="Episodios"):
            states, actions, rewards = [], [], []
            state = self.model.get_initial_state()

            # episode_reward = 0
            while not self.model.is_terminal(state):
                action = self.policy.select_action(state)
                next_state, reward = self.model.execute(state, action)

                # Almacena la información de este paso de la trayectoria
                states.append(state)
                actions.append(action)
                rewards.append(reward)

                state = next_state

            deltas = self.calculate_deltas(rewards)
            self.policy.update(states=states, actions=actions, deltas=deltas)

    """
        Generar una lista de las recompensas futuras descontadas en cada paso de un episodio.
    """
    def calculate_deltas(self, rewards):
        
        T = len(rewards)
        discounted_future_rewards = [0 for _ in range(T)]
        # The final discounted reward is the reward you get at that step
        discounted_future_rewards[T - 1] = rewards[T - 1]
        for t in reversed(range(0, T - 1)):
            discounted_future_rewards[t] = (
                rewards[t]
                + discounted_future_rewards[t + 1] * self.model.get_discount_factor()
            )
        deltas = []
        for t in range(len(discounted_future_rewards)):
            deltas += [
                self.alpha
                * (self.model.get_discount_factor() ** t)
                * discounted_future_rewards[t]
            ]
        return deltas