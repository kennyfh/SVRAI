#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# EL PROBLEMA DEL VEHICULO EN PENDIENTE (V1)

# Consideremos un vehículo que opera en una pendiente y utiliza paneles solares para recargarse. 
# Puede encontrarse en uno de los tres estados de la pendiente: alto, medio y bajo. Si hace girar sus ruedas,
# sube la pendiente en cada paso de tiempo (de bajo a medio o de medio a alto) o se mantiene alto. Si no gira
# las ruedas, desciende por la pendiente en cada paso de tiempo (de alto a medio o de medio a bajo) o se mantiene
# bajo. Hacer girar las ruedas consume una unidad de energía por paso de tiempo. Estando en la parte alta 
# o media de la pendiente gana tres unidades de energía por paso de tiempo a través de los paneles solares, 
# mientras que estando en la parte baja de la pendiente no gana nada de energía por paso de tiempo.
#  El robot quiere ganar tanta energía como sea posible.
# ---------------------------------------------------------------------------
from mdp import *
from typing import List, Tuple

class VehicleSlopeV1(MDP):

    """
    Clase para el problema del Vehículo en la pendiente (V1).
    """
    #Estados
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    # Acciones
    SPIN = "SPIN"
    NOT_SPIN = "NOT_SPIN"

    def __init__(self,
                discount_factor=0.8
                )-> None:
        
        """
        Inicializa el problema del Vehículo en la pendiente.

        Args:
            discount_factor (float): factor de descuento. Por defecto 0.8.
        """

        self.discount_factor = discount_factor
        self.transitions_dict = {
            (self.LOW,self.SPIN):[(self.MEDIUM, 1)],
            (self.LOW,self.NOT_SPIN):[(self.LOW, 1)],
            (self.MEDIUM,self.SPIN):[(self.HIGH, 1)],
            (self.MEDIUM,self.NOT_SPIN):[(self.LOW, 1)],
            (self.HIGH,self.SPIN):[(self.HIGH, 1)],
            (self.HIGH,self.NOT_SPIN):[(self.MEDIUM, 1)]
        }
            

    def get_states(self) -> List[str]:
        """
        Devuelve todos los estados posibles.

        Returns:
            List[str]: lista de estados posibles.
        """
        return [self.LOW, self.MEDIUM, self.HIGH]

    def get_actions(self, state=None) -> List[str]:
        """
        Devuelve las acciones posibles en un estado determinado o en todos los estados.

        Args:
            state (str): el estado del que se quieren obtener las acciones. Por defecto None.

        Returns:
            List[str]: lista de acciones posibles.
        """
        actions = [self.SPIN,self.NOT_SPIN]
        if state is None:
            return actions
        valid_actions =[]
        for a in actions:
            for (_,prob) in self.get_transitions(state,a):
                if prob > 0:
                    valid_actions.append(a)
                    break
        return valid_actions

    def get_transitions(self, state:str, action:str) -> List[Tuple[str,float]]:
        """
        Devuelve la probabilidad de transición a los siguientes estados posibles y sus respectivas probabilidades.

        Args:
            state (str): el estado actual.
            action (str): la acción tomada.

        Returns:
            List[Tuple[str,float]]: lista de tuplas con los estados siguientes y sus probabilidades de transición.
        """
        return self.transitions_dict[(state,action)]


    def get_reward(self, state:str, action:str, next_state:str) -> float:
        """
        Calcula la recompensa de realizar una acción en un estado y alcanzar el siguiente estado.

        Args:
            state (str): Estado actual.
            action (str): Acción realizada en el estado actual.
            next_state (str): Siguiente estado alcanzado después de tomar la acción.

        Returns:
            float: Recompensa recibida por tomar la acción en el estado actual y llegar al siguiente estado.

            - 
        """
        reward = 0.
        if state == self.MEDIUM or state == self.HIGH:
            reward = 3.
        return reward

    def is_terminal(self, state) -> bool:
        """
        Verifica si nos encontramos un estado inicial

        Args:
            state (str): El estado a comprobar.

        Returns:
            False: debido a que no tenemos ningún estado inicial en este problema
        """
        return False

    def get_discount_factor(self) -> float:
        """
        Obtiene el factor de descuento para las recompensas futuras.

        Returns:
            float: El factor de descuento.
        """
        return self.discount_factor

    def get_initial_state(self) -> str:
        """
        Obtiene el estado inicial.

        Returns:
            str: El estado inicial.
        """
        return random.choice(self.LOW,self.MEDIUM,self.HIGH)

    def get_goal_states(self) -> None:
        """
        Obtiene los estados objetivo (en este caso ninguno)
        """
        return
    

    def print_value_function(self,valuef) -> None :
        """
        Función que imprime por pantalla la función de valor de 
        cada estado haciendo uso del algoritmo de iteración de valores        
        """
        states = self.get_states()
        print("+----------+---------------+")
        print("|  Estado  |     Valor     |")
        print("+----------+---------------+")
        for state in states:
            print(f"| {state:<8} | {round(valuef.get_value(state),3):<13} |")
            print("+----------+---------------+")



# EL PROBLEMA DEL VEHICULO EN PENDIENTE (V2)
#
# Supongamos ahora que el vehículo puede encontrarse en uno de los cuatro estados de la pendiente: superior,
#  alto, medio y bajo. Si gira sus ruedas lentamente, sube la pendiente en cada paso de tiempo (de bajo a medio,
#   o de medio a alto, o de alto a superior) con una probabilidad de 0,3
# , y desciende por la pendiente hasta la parte baja con una probabilidad de 0,7
# . Si hace girar sus ruedas rápidamente, sube la pendiente en cada paso de tiempo (de bajo a medio, o de medio
# a alto, o de alto a superior) con una probabilidad de 0,7
# , y se desliza por la pendiente hasta llegar abajo con una probabilidad de 0,3
# . El giro lento de las ruedas consume una unidad de energía por paso de tiempo. Girar las ruedas rápidamente
#  consume dos unidades de energía por unidad de tiempo. El vehículo se encuentra en la parte baja de la pendiente
#   y su objetivo es llegar a la cima con el mínimo consumo de energía previsto.
# ---------------------------------------------------------------------------

class VehicleSlopeV2(MDP):
    """
    Clase para el problema del Vehículo en la pendiente (V2).
    """

    # Estados
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    TOP = "TOP"
    # Acciones
    SPIN_FAST = "SPIN_FAST"
    SPIN_LOW = "SPIN_LOW"

    
    def __init__(self,
                 discount_factor:float=0.8, # Factor de descuento
                 initial_state:str="LOW" # Estado inicial
                 ) -> None:
        """
        Inicializa el problema del Vehículo en la pendiente.

        Args:
            discount_factor (float): factor de descuento. Por defecto 0.8.
            initial_state (str): estado inicial. Por defecto "LOW".
        """
        
        self.discount_factor = discount_factor
        self.initial_state = initial_state

        self.transitions_dict = {
            (self.LOW, self.SPIN_LOW): [(self.MEDIUM, 0.3), (self.LOW, 0.7)],
            (self.LOW, self.SPIN_FAST): [(self.MEDIUM, 0.7), (self.LOW, 0.3)],
            (self.MEDIUM, self.SPIN_LOW): [(self.HIGH, 0.3), (self.LOW, 0.7)],
            (self.MEDIUM, self.SPIN_FAST): [(self.HIGH, 0.7), (self.LOW, 0.3)],
            (self.HIGH, self.SPIN_LOW): [(self.TOP, 0.3), (self.LOW, 0.7)],
            (self.HIGH, self.SPIN_FAST): [(self.TOP, 0.7), (self.LOW, 0.3)],
            (self.TOP, self.SPIN_LOW): [(self.TOP, 1)],
            (self.TOP, self.SPIN_FAST): [(self.TOP, 1)]
        }


    def get_states(self) -> List[str]:
        """
        Devuelve todos los estados posibles.

        Returns:
            List[str]: lista de estados posibles.
        """
        return [self.LOW, self.MEDIUM, self.HIGH, self.TOP]


    def get_actions(self, state=None) -> List[str]:
        """
        Devuelve las acciones posibles en un estado determinado o en todos los estados.

        Args:
            state (str): el estado del que se quieren obtener las acciones. Por defecto None.

        Returns:
            List[str]: lista de acciones posibles.
        """
        actions = [self.SPIN_LOW, self.SPIN_FAST]
        if state is None:
            return actions
        valid_actions =[]
        for a in actions:
            for (_,prob) in self.get_transitions(state,a):
                if prob > 0:
                    valid_actions.append(a)
                    break
        return valid_actions

    def get_transitions(self, state:str, action:str) -> List[Tuple[str,float]]:
        """
        Devuelve la probabilidad de transición a los siguientes estados posibles y sus respectivas probabilidades.

        Args:
            state (str): el estado actual.
            action (str): la acción tomada.

        Returns:
            List[Tuple[str,float]]: lista de tuplas con los estados siguientes y sus probabilidades de transición.
        """
        return self.transitions_dict[(state, action)]


    def get_reward(self, state:str, action:str, next_state:str) -> float:
        """
        Calcula la recompensa de realizar una acción en un estado y alcanzar el siguiente estado.

        Args:
            state (str): Estado actual.
            action (str): Acción realizada en el estado actual.
            next_state (str): Siguiente estado alcanzado después de tomar la acción.

        Returns:
            float: Recompensa recibida por tomar la acción en el estado actual y llegar al siguiente estado.
                - Si el siguiente estado es la cima (TOP) y la acción lleva a permanecer en la cima, la recompensa es de 100. 
                - Si la acción es girar las ruedas lentamente (SPIN_LOW), la recompensa es de -1. 
                - Si la acción es girar las ruedas rápidamente (SPIN_FAST), la recompensa es de -2.
        """
        reward = 0.
        if state == self.TOP and next_state == self.TOP:
            reward = 100.
        else:
            reward = -1. if action == self.SPIN_LOW else -2.
        return reward


    def is_terminal(self, state:str) -> bool:
        """
        Verifica si nos encontramos un estado inicial

        Args:
            state (str): El estado a comprobar.

        Returns:
            bool: Verdadero si el estado es la cima (TOP), Falso de lo contrario.
        """
        return True if state == self.TOP else False


    def get_discount_factor(self) -> float:
        """
        Obtiene el factor de descuento para las recompensas futuras.

        Returns:
            float: El factor de descuento.
        """
        return self.discount_factor


    
    def get_goal_states(self) -> None:
        """
        Obtiene los estados objetivo (en este caso, solo hay uno, la cima).

        Returns:
            None
        """
        return
    
    def print_value_function(self,valuef) -> None :
        """
        Función que imprime por pantalla la función de valor de 
        cada estado haciendo uso del algoritmo de iteración de valores        
        """
        states = self.get_states()
        print("+----------+---------------+")
        print("|  Estado  |     Valor     |")
        print("+----------+---------------+")
        for state in states:
            print(f"| {state:<8} | {round(valuef.get_value(state),3):<13} |")
            print("+----------+---------------+")
