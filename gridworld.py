#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: GRIDWORLD
# Created By  : KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# EL PROBLEMA DEL MUNDO MALLA
#
# El ejemplo de mundo malla es una idealización del movimiento de un robot en un entorno.
# En cada momento, el robot se encuentra en una ubicación y puede desplazarse a las ubicaciones vecinas,
#  recogiendo recompensas y castigos. Supongamos que las acciones son estocásticas, de modo que existe una
#  distribución de probabilidad sobre los estados resultantes dada la acción y el estado.

# En la figura adjunta se muestra un mundo cuadriculado de 10×10, en el que el robot puede elegir
#  una de cuatro acciones: arriba, abajo, izquierda o derecha. Si el agente lleva a cabo una de estas acciones,
#  tiene una probabilidad de 0.7 de dar un paso en la dirección deseada y una probabilidad de 0.1 de dar un paso
#  en cualquiera de las otras tres direcciones. Si choca contra la pared exterior (es decir, la ubicación calculada
# está fuera de la malla), tiene una penalización de 1 (es decir, una recompensa de −1) y el agente no se mueve.
# Hay cuatro estados con recompensa (aparte de las paredes): +10 (en la posición (9,8)), +3 (en (8,3)), −5 (en (4,5))
#  y −10 (en (4,8)). En cada uno de estos estados, el agente obtiene la recompensa después de realizar una acción
# en ese estado, no cuando entra en él. Cuando el agente alcanza uno de los estados con recompensa positiva
# (ya sea +3 o +10), independientemente de la acción que realice, en el siguiente paso es lanzado, al azar, a
#  una de las cuatro esquinas del mundo cuadriculado.
# ---------------------------------------------------------------------------


from mdp import *
from policy_iteration import PolicyIteration
from tabular_policy import TabularPolicy

# {"up": "↑", "down": "↓",
#    "left": "←", "right": "→", "exit": " "}


class GridWorld(MDP):
    TERMINATE = 'end'
    TERMINAL = ('end', 'end')
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    """ Initialization"""

    def __init__(
        self,
        noise=0.3,
        width=10,
        height=10,
        discount_factor=0.9,
        blocked_states=[],
        action_cost=0.0,
        initial_state=(0, 0),
        goals=None,
    ) -> None:
        # Ruido:
        self.noise = noise
        # Dimensiones del grid
        self.width = width
        self.height = height
        # Factor de descuento y
        self.discount_factor = discount_factor
        # Estado inicial
        self.initial_state = initial_state
        # Recompensas
        if goals is None:
            # Si no existen recompensas dentro de la malla, pondremos 2 recompensas para testear la prueba
            self.goal_states = dict(
                [((width - 1, height - 1), 1), ((width - 1, height - 2), -1)]
            )
        else:
            self.goal_states = dict(goals)
        
        # Movimientos
        self.movements = {
            "UP": [(-1, 0), (0, -1), (0, 1)],
            "DOWN": [(1, 0), (0, -1), (0, 1)],
            "LEFT": [(0, -1), (-1, 0), (1, 0)],
            "RIGHT": [(0, 1), (-1, 0), (1, 0)]
            }

        # Obstáculos: en nuestro problema no tenemos ningún obstáculo, pero podemos añadir algunos por experimentación
        self.blocked_states = blocked_states
        # Coste de accion
        self.action_cost = action_cost
        super().__init__()

    
    def get_states(self):
        """ Los estados son todas las casillas donde no se encuentran
        obstáculos"""
        states = [self.TERMINAL]
        states += [(x, y) for x in range(self.width)
                   for y in range(self.height) if (x,y) not in self.blocked_states]
        return states

    def get_actions(self, state=None):
        actions = [self.UP, self.DOWN,self.LEFT, self.RIGHT, self.TERMINATE]
        if state is None:
            return actions

        valid_actions = []

        for a in actions:
            for (new_state, prob) in self.get_transitions(state,a):
                if prob > 0:
                    valid_actions.append(action)
                    break
        return valid_actions


    """ Return all non-zero probability transitions for this action
        from this state, as a list of (state, probability) pairs
    """

    def get_transitions(self, state, action):
        def  move(state,m):
            x, y = state
            i, j = m
            nx, ny = x + i, y + j
            if (nx, ny) in self.states:
                return nx, ny
            else:
                return x, y

        if state == self.TERMINATE:
            return [(self.TERMINAL, 1.0)] if action == self.TERMINATE else []

        transitions = []

        if state in self.get_goal_states().keys():
            if action == self.TERMINATE:
                transitions += [(self.TERMINAL, 1.0)]
        
        else:
            mov = self.movements[action]
            pok = 1 - self.noise
            pnook = self.noise / 2
            transitions += [(move(state, mov[0]), pok),
                            (move(state, mov[1]), pnook),
                            (move(state, mov[2]), pnook)]

        # Merge any duplicate outcomes
        merged = defaultdict(lambda: 0.0)
        for (state, probability) in transitions:
            merged[state] = merged[state] + probability

        transitions = []
        for outcome in merged.keys():
            transitions += [(outcome, merged[outcome])]

        return transitions


    def get_reward(self, state, action, next_state):
        """
        Devuelve una recompensa si el siguiente estado es un terminal y
        y este estado es una que tiene recompensa
        """
        cond = self.get_goal_states().keys() and next_state == self.TERMINAL
        return self.get_goal_states().get(state) if cond else self.action_cost

    def is_terminal(self, state):
        if state == self.TERMINAL:
            # self.rewards += [self.episode_rewards]
            return True
        return False

    def get_discount_factor(self):
        return self.discount_factor

    def get_initial_state(self):
        return self.initial_state

    def get_goal_states(self):
        return self.goal_states


if __name__ == "__main__":
    gridworld = GridWorld(goals=[((9, 8), +10), ((8, 3), +3),
                   ((4, 5), -5), ((4, 8), -10)])
    policy = TabularPolicy(default_action=gridworld.LEFT)
    vi = PolicyIteration(gridworld, policy).policy_iteration(max_iterations=100)
    print(vi)