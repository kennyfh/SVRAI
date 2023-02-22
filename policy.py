"""
Clase Policy: Implementa una política, que es la estrategia
que un agente hace uso para tomar decisiones en un entorno dado.

El objetivo que tenemos de la política es que maximice la recompensa
esperada que el agente recibirá a lo largo del tiempo.

Las políticas pueden ser deterministas o estocásticas.
"""

class Policy:
    def select_action(self, state):
        ...


"""
Clase DeterministicPolicy: Clase hija de Policy que nos permite
implementar una política determinista, es decir, aquella que asigna
una única acción a cada estado.
"""
class DeterministicPolicy(Policy):
    def update(self, state, action):
        ...

"""
Clase StochasticPolicy: Clase hija de Policy que permite la creación
de una política estocástica, es decir, la asignación de una distribución
de probabilidad sobre las posibles acciones para cada estado.
"""
class StochasticPolicy(Policy):

    def update(self, states, actions, rewards):
        ...

    def get_probability(self, state, action):
        ...
