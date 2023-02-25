#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import sys
import numpy as np
import pygame
from mdp import *   
from typing import List, Union, Tuple

# COLORES PARA PYGAME
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
CELL_SIZE = 50

class GridWorld(MDP):

    """
    GridWorld es una clase que representa el entorno del problema del Mundo Malla. En este problema es un entorno discreto
    que representa la cuadrícula donde un agente debe moverse entre las celdas.
    
    """
    
    TERMINAL = ('end', 'end')
    TERMINATE = 'end'
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(
        self,
        noise=0.3,
        width=10,
        height=10,
        discount_factor=0.9,
        # blocked_states=[],
        action_cost=0.0,
        initial_state=(0, 0),
        goals=None,
    ) -> None:
        
        """
        Crea una instancia del problema Mundo Malla.
        
        Args:
            noise (float): el ruido que introduce el entorno en la acción del agente. Por defecto es 0.3.
            width (int): la anchura de la cuadrícula. Por defecto es 10.
            height (int): la altura de la cuadrícula. Por defecto es 10.
            discount_factor (float): el factor de descuento que determina la importancia que tiene la recompensa en el futuro. Por defecto es 0.9.
            blocked_states (List[Tuple[int, int]]): una lista de tuplas que representan las celdas bloqueadas. 
            action_cost (float): el coste que tiene realizar una acción. Por defecto es 0.0.
            initial_state (Tuple[int, int]): una tupla que representa la posición inicial del agente. Por defecto es (0, 0).
            goals (Union[None, List[Tuple[Tuple[int, int], int]]]): una lista de tuplas que representan las posiciones de las celdas objetivo y su recompensa. Por defecto es None.
        """

        self.noise = noise # Ruido
        self.width = width # Dimensionalidad
        self.height = height
        self.discount_factor = discount_factor # Factor de descuento
        self.initial_state = initial_state # Estado inicial

        # Recompensas
        if goals is None:
            # Se pondrán 2 recompensas de prueba si no hay metas
            self.goal_states = dict(
                [((width - 1, height - 1), 1), ((width - 1, height - 2), -1)]
            )
        else:
            self.goal_states = dict(goals)
        
        self.state_set = [(x, y) for x in range(self.width) for y in range(self.height)]
        outside_coords = [(x, y) for x in range(-1, self.width+1) for y in range(-1, self.height+1) if (x,y) not in self.state_set]
        self.blocked_states = sorted(list(set(outside_coords)))

        # Coste de accion
        self.action_cost = action_cost


    def get_states(self) -> List[Union[str, Tuple[int, int]]]:
        """
        Devuelve la lista de estados del GridWorld.

        Returns:
            List[Union[str, Tuple[int, int]]]: Lista de estados.
        """

        states = [self.TERMINAL]
        # states += [(x, y) for x in range(self.width)
        #            for y in range(self.height) if (x,y) not in self.blocked_states]
        states += self.state_set

        return states

    def get_actions(self, state=None) -> List[str]:
        """
        Devuelve la lista de acciones posibles para un estado o para cualquier estado.

        Args:
            state (Tuple[int, int], optional): Estado para el que se quieren conocer las acciones. Si es None, se devuelven las acciones para cualquier estado. Por defecto None.

        Returns:
            List[str]: Lista de acciones posibles.
        """

        actions = [self.UP, self.DOWN,self.LEFT, self.RIGHT, self.TERMINATE]
        if state is None:
            return actions
        valid_actions = []
        for a in actions:
            for (_, prob) in self.get_transitions(state,a):
                if prob > 0:
                    valid_actions.append(a)
                    break
        return valid_actions

    def valid_add(self, state:Tuple[int, int], new_state:Tuple[int, int], prob:float) -> Tuple[Tuple[int, int], float]:
        """
        Añade una transición válida a la lista de transiciones.

        Args:
            state (Tuple[int, int]): Estado actual.
            new_state (Tuple[int, int]): Nuevo estado.
            prob (float): Probabilidad de la transición.

        Returns:
            Tuple[Tuple[int, int], float]: Nueva transición válida.
        """
        if prob == 0.0:
            return ()

        if new_state in self.blocked_states:
            return (state, prob)

        (x, y) = new_state
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return ((x, y), prob)

        return (state, prob)

    def get_transitions(self, state:Tuple[int, int], action:str) -> List[Tuple[Union[Tuple[str, int], Tuple[int, int]], float]]:
        """
        Devuelve la lista de transiciones posibles para un estado y una acción.

        Args:
            state (Tuple[int, int]): Estado actual.
            action (str): Acción a realizar.

        Returns:
            List[Tuple[Union[Tuple[str, int], Tuple[int, int]], float]]: Lista de transiciones posibles.
        """
        transitions = []

        if state == self.TERMINAL:
            if action == self.TERMINATE:
                return [(self.TERMINAL, 1.0)]
            else:
                return []

        straight = 1 - (2 * self.noise)

        (x, y) = state
        movements = {
            "UP": [(x, y+1), (x-1, y), (x+1, y)],
            "DOWN": [(x, y-1), (x-1,y), (x+1, y)],
            "LEFT": [(x-1,y), (x, y-1), (x, y+1)],
            "RIGHT": [(x+1, y), (x, y-1), (x, y+1)]
            }
        if state in self.get_goal_states().keys():
            if action == self.TERMINATE:
                transitions += [(self.TERMINAL, 1.0)]

        elif action==self.UP or action == self.DOWN or action==self.LEFT or action==self.RIGHT:
            mov =  movements[action]
            transitions += [self.valid_add(state, mov[0], straight),
                            self.valid_add(state, mov[1], self.noise),
                            self.valid_add(state, mov[2], self.noise)]
        return transitions


    def get_reward(self, 
                  state: Union[Tuple[int, int], Tuple[str, str]],
                  action: str,
                  next_state:Union[Tuple[int, int], Tuple[str, str]]) -> float:
        """
        Calcula la recompensa para una transición de estado a estado.
        
        Args:
            state (Union[Tuple[int, int], Tuple[str, str]]): El estado actual.
            action (str): La acción tomada en el estado actual.
            next_state (Union[Tuple[int, int], Tuple[str, str]])): El siguiente estado.

        Returns:
            reward (int): La recompensa obtenida por la transición de estado a estado
        """

        reward = 0.
        if state in self.get_goal_states().keys() and next_state == self.TERMINAL:
            reward = self.get_goal_states().get(state)
        elif next_state in self.blocked_states:
            reward=-1.    
        else:
            reward = self.action_cost
        return reward

    def is_terminal(self, state:Union[Tuple[int, int], Tuple[str, str]]) -> bool:
        """
        Determina si un estado es un estado terminal.

        Args:
            state (Union[Tuple[int, int], Tuple[str, str]]): El estado a evaluar.

        Returns:
            True si el estado es un estado terminal, False en caso contrario.
        """
        return True if state==self.TERMINAL else False

    def get_discount_factor(self) -> float:
        """
        Define el factor de descuento
        """
        return self.discount_factor

    def get_initial_state(self) -> Tuple[int,int]:
        """
        Define el estado inicial del entorno 
        """
        return self.initial_state

    def get_goal_states(self) -> List[Tuple[int,int]]:
        """
        Define el estado terminal del entorno 
        """
        return self.goal_states
    
    @staticmethod
    def pygame_installed():
        try:
            import pygame
            return True
        except ModuleNotFoundError:
            return False
    
    
    def visualise_initial_state(self) -> None:
        """
        Función para visualizar el estado inicial, si no se tiene pygame instalado, se printea por
        consola 
        """
        if self.pygame_installed:
            pygame.init()
            screen = pygame.display.set_mode((500, 500))
            pygame.display.set_caption(f"GridWorld {self.width}x{self.height} (estado inicial)")

            mat = np.zeros((10,10))
            for x,y in self.goal_states.items():
                 mat[x[0],x[1]]=y
            mat = np.fliplr(mat)

            for x in range(mat.shape[0]):
                for y in range(mat.shape[1]):
                    if mat[x,y] > 0:
                        self.draw_cell(screen,x,y,GREEN, str(mat[x,y]))
                    elif mat[x,y] < 0:
                        self.draw_cell(screen,x,y,RED, str(mat[x,y]))
                    else:
                        self.draw_cell(screen,x,y,WHITE," ")

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
        else:
            raise ModuleNotFoundError("Tienes que tener instalado Pygame")


    def draw_cell(self,screen, x, y, color, arrow) -> None:
                # Fondo
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)

                # Borde
                border_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, border_rect, 1)

                # Texto
                font = pygame.font.SysFont("arial", 20)
                text = font.render(arrow, True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

     
    def visualise_policy(self,policy) -> None:
        """
        Función que pinta en Pygame la política ya sea con Pygame o por terminal
        """ 
        mov = {self.UP: "↑", self.DOWN: "↓",
                    self.LEFT: "←", self.RIGHT: "→", self.TERMINATE: " "}
        if self.pygame_installed:
            pygame.init()
            screen = pygame.display.set_mode((500, 500))
            def draw_grid():
                for x in range(self.width):
                    for y in range(self.height):
                        if (x,y) in self.goal_states and self.goal_states[(x,y)] >0:
                            self.draw_cell(screen, x,abs(9-y), GREEN, str(self.goal_states[(x, y)]))
                        elif (x,y) in self.goal_states and self.goal_states[(x,y)] <0:
                            self.draw_cell(screen,x,abs(9-y), RED, str(self.goal_states[(x, y)]))
                        else:
                            self.draw_cell(screen,x,abs(9-y),WHITE,str(mov[policy.select_action((x, y))]))

            draw_grid()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()

            
        else:
            print(self.policy_to_string(policy))


    def policy_to_string(self, policy) -> str:
        """
        Dibuja la política del entorno en la terminal
        """       
        result= "\n "
        mov = {self.UP: "↑", self.DOWN: "↓",
                    self.LEFT: "←", self.RIGHT: "→", self.TERMINATE: " "}
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                # # Si el elemento es un obstáculo
                # if (x,y) in self.blocked_states:
                #     result += " | ##"
                # Si el elemento es una recompensa
                if policy.select_action((x, y)) == self.TERMINATE:
                    result += f" | {self.goal_states[(x, y)]} "
                # Si es otro
                else:
                    result += " |  " + mov[policy.select_action((x, y))] + " "
            result += "\n"
        return result


    def execute(self, state, action):
        """
        Ejecuta como si el problema fuera libre de modelo
        """
        if state in self.goal_states:
            return MDP.execute(self, state=state, action=self.TERMINATE)

        return super().execute(state, action)
