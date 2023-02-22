import random
from collections import defaultdict
from policy import DeterministicPolicy

"""
TabularPolicy: Representación de una política en forma de tabla
que mapea desde cada estado a la acción para ese determinado estado.
"""

class TabularPolicy(DeterministicPolicy):

    def __init__(self, default_action=None) -> None:
        """
        El hacer uso de defaultdict en vez de un diccionario nos evita
        el tener que comprobar si una clave existe antes de acceder a ella.
        """
        self.policy_table = defaultdict(lambda: default_action)

    def select_action(self, state):
        return self.policy_table[state]

    def update(self, state, action) -> dict:
        self.policy_table[state] = action
