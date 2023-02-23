import random
from collections import defaultdict
from policy import DeterministicPolicy

"""
TabularPolicy: Representación de una política en forma de tabla
que mapea desde cada estado a la acción para ese determinado estado.
"""

class TabularPolicy(DeterministicPolicy):

    """Inicialización de la clase"""
    def __init__(self, 
                default_action=None) -> None:
        """
        El hacer uso de defaultdict en vez de un diccionario nos evita
        el tener que comprobar si una clave existe antes de acceder a ella.
        """
        self.policy_table = defaultdict(lambda: default_action)

    """Método para seleccionar una acción según un estado"""
    def select_action(self, state):
        return self.policy_table[state]

    """Método para actualizar la tabla"""
    def update(self, state, action) -> dict:
        self.policy_table[state] = action

    """Método para imprimir la tabla de políticas"""
    def print_policy_table(self, state_width=8, action_width=20) -> None:
        header = f"| {'Estado':<{state_width}} | {'Accion':<{action_width}} |"
        print(f"+{'-' * (len(header) - 2)}+")
        print(header)
        print(f"+{'-' * (len(header) - 2)}+")
        for state, action in self.policy_table.items():
            print(f"| {str(state):<{state_width}} | {action:<{action_width}} |")
            print(f"+{'-' * (len(header) - 2)}+")