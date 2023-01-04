
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: GRID WORLD (PROBLEM 2)
# Created By  : KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# GRID WORLD
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

# Imports
from typing import Dict, List, Tuple
from mdp import *


"""
    Definición de una clase llamada Grid (Cuadrícula), siendo esta herencia de MDP
    Los argumentos de entrada son los siguintes:

    - grid: representación de una cuadrícula
    - reward_default: recompensa de las casillas no terminales,
                      con un valor por defecto de -0.04
    - y: atributo descuento con un valor por defecto de 0.9
    - noise: es la probabilidad de que una acción no siga el efecto
             deseado, por lo que realizará uno de los dos movimientos
             perpendiculares al deseado. Si el ruido tiene un valor de 0.3,
            tiene una posibilidad de 0.7 de dar un paso en la dirección deseada,
            y una probabilidad de 0.1 en cualquiera de las otras 3 direcciones.

    """


class Grid(MDP):
    """
        A class representing a Markov Decision Process (MDP).
    """

    def __init__(self, grid: List[List[int]],
                 reward_default: float = -0.04,
                 y: float = 0.9,
                 noise: float = 0.3) -> None:
        """
        Initializes the Grid MDP.

        Args:
            grid (List[List[int]]): a list of lists representing the grid.
            reward_default (float, optional): the default reward for non-terminal states. Defaults to -0.04.
            y (float, optional): the discount factor for the MDP. Defaults to 0.9.
            noise (float, optional): the probability of the action not being executed as intended. Defaults to 0.3.
        """
        # Estados y recompensas
        states = {}
        terminals = []
        reward = {}
        rows, cols = len(grid), len(grid[0])
        # Por cada elemento de la cuadricula
        for i in range(rows):
            for j in range(cols):
                # Seleccionamos el contenido que se encuentra en la celda
                content = grid[i][j]

                # Si el contenido no es un obstáculo
                if content != "*":
                    # Guardamos el estado en el diccionario de estados
                    state = (i, j)
                    states[state] = True
                    # Si el contenido es un número entero o real
                    if isinstance(content, (int, float)):
                        # Guardamos el contenido como recompensa y terminal
                        reward[state] = content
                        terminals.append(state)
                    else:
                        # Si no, nosotros le ponemos una recompensa negativa
                        reward[state] = reward_default

        super().__init__(list(states.keys()), y)
        self.end_states = terminals
        self.rows = rows
        self.cols = cols
        self.reward = reward
        self.noise = noise
        self.displacements = {
            "up": [(-1, 0), (0, -1), (0, 1)],
            "down": [(1, 0), (0, -1), (0, 1)],
            "left": [(0, -1), (-1, 0), (1, 0)],
            "right": [(0, 1), (-1, 0), (1, 0)]
        }

    def R(self, state: Tuple[int, int]) -> float:
        """
        Returns the reward for the given state.
        
        Args:
            state (Tuple[int, int]): the state for which the reward should be returned.
            
        Returns:
            float: the reward for the given state.
        """
        return self.reward[state]

    def A(self, state: Tuple[int, int]) -> List[str]:
        """
        Returns the list of available actions for the given state.
        
        Args:
            state (Tuple[int, int]): the state for which the list of available actions should be returned.
            
        Returns:
            List[str]: the list of available actions for the given state.
        """
        return (["exit"] if state in self.end_states else ["up", "down", "left", "right"])





    def T(self, state: Tuple[int, int], action: str) -> List[Tuple[Tuple[int, int], float]]:
        """
        Returns the list of tuples representing the transition probabilities for the given state and action.
        
        Args:
            state (Tuple[int, int]): the state for which the transition probabilities should be returned.
            action (str): the action for which the transition probabilities should be returned.
            
        Returns:
            List[Tuple[Tuple[int, int], float]]: a list of tuples representing the transition probabilities for the given state and action.
        """
        def  move(state: Tuple[int, int], m: Tuple[int, int]) -> Tuple[int, int]:
            """
            Returns the next state after taking the given action from the given state.
            
            Args:
                state (Tuple[int, int]): the current state.
                m (Tuple[int, int]): the action to be taken.
                
            Returns:
                Tuple[int, int]: the next state after taking the given action from the current state.
            """
            x, y = state
            i, j = m
            nx, ny = x + i, y + j
            if (nx, ny) in self.states:
                return nx, ny
            else:
                return x, y

        if action == "exit":
            return ([(state, 0)])
        else:
            mov = self.displacements[action]
            pok = 1 - self.noise
            pnook = self.noise / 2
            return [(move(state, mov[0]), pok),
                    (move(state, mov[1]), pnook),
                    (move(state, mov[2]), pnook)]


def print_policy_grid(pi: Dict[Tuple[int, int], str], P: MDP):
    """
    Prints the policy grid for the given MDP and policy.
    
    Args:
        pi (Dict[Tuple[int, int], str]): the policy for the MDP.
        P (MDP): the MDP for which the policy grid should be printed.
    """
    flechas = {"up": "↑", "down": "↓",
               "left": "←", "right": "→", "exit": " "}
    lv = "-"*(P.cols*4+1)+"\n"
    str = lv
    print()
    for f in range(P.rows):
        for c in range(P.cols):
            if (f, c) in P.states:
                str += "| "+flechas[pi[(f, c)]]+" "
            else:
                str += "| * "
        str += "|\n"+lv
    print(str)


grid_1 = [[' ', ' ', ' ', +1],
          [' ', '*', ' ', -1],
          [' ', ' ', ' ', ' ']]


grid_2 = [[' ', ' ', ' ', ' ', ' '],
          [' ', '*', ' ', ' ', ' '],
          [' ', '*', 1, '*', 10],
          [' ', ' ', ' ', ' ', ' '],
          [-10, -10, -10, -10, -10]]

grid_exercise = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, ],
                 [1,  ' ',  ' ',  ' ',  ' ',  ' ',  10],
                 ['*', -100, -100, -100, -100, -100, '*']]

# Representa gráficamente el MDP.
# Resuelve el MDP por diversos métodos.
# Describe la política óptima.


def main() -> None:
    # >>> mdp_c1=Cuadrícula(cuadrícula_1)
    # >>> pi_c1,_=iteración_de_valores(mdp_c1)
    # >>> imprime_política_cuadricula(pi_c1,mdp_c1)

    # -----------------
    # | → | → | → |   |
    # -----------------
    # | ↑ | * | ↑ |   |
    # -----------------
    # | ↑ | → | ↑ | ← |

    P_c1 = Grid(grid_1, reward_default=-1)
    pi_c1, _ = value_iteration(P_c1)
    print_policy_grid(pi_c1, P_c1)

    # >>> mdp_c2=Cuadrícula(cuadrícula_2)
    # >>> pi_c2,_=iteración_de_valores(mdp_c2)
    # >>> imprime_política_cuadricula(pi_c2,mdp_c2)

    # ---------------------
    # | → | → | → | → | ↓ |
    # ---------------------
    # | ↑ | * | → | → | ↓ |
    # ---------------------
    # | ↑ | * |   | * |   |
    # ---------------------
    # | ↑ | ↑ | → | → | ↑ |
    # ---------------------
    # |   |   |   |   |   |
    P_c2 = Grid(grid_2)
    pi_c2, _ = value_iteration(P_c2)
    print_policy_grid(pi_c2, P_c2)


if __name__ == "__main__":
    main()
