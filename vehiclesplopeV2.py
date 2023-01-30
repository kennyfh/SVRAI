#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Vehicleslope
# Created By  : KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# EL PROBLEMA DEL VEHICULO EN PENDIENTE (V1)
#
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

# Estados: bajo, medio, alto y superior
# Estado final: cuando llegue al superior que será la cima 

class VehicleSlopeV2(MDP):
    # States
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    TOP = "TOP"
    # Actions
    SPIN_FAST = "SPIN_FAST"
    SPIN_LOW = "SPIN_LOW"

    def __init__(self,
                discount_factor=0.8,
                energy=50,
                initial_state="LOW"
                ) -> None:
        self.discount_factor=discount_factor
        self.energy=energy
        self.initial_state=initial_state
        
        self.transitions_dict{
            (self.LOW,self.SPIN_LOW):[(self.MEDIUM,0.3),(self.LOW,0.7)],
            (self.LOW,self.SPIN_FAST):[(self.MEDIUM,0.7),(self.LOW,0.3)],
            (self.MEDIUM,self.SPIN_LOW):[(self.HIGH,0.3),(self.LOW,0.7)],
            (self.MEDIUM,self.SPIN_FAST):[(self.HIGH,0.7),(self.LOW,0.3)],
            (self.HIGH,self.SPIN_LOW):[(self.TOP,0.3),(self.LOW,0.7)],
            (self.HIGH,self.SPIN_FAST):[(self.TOP,0.7),(self.LOW,0.3)], 

        }

    def get_states(self):
        return [self.LOW,self.MEDIUM, self.HIGH, self.TOP]

    def get_actions(self, state):
        return [self.SPIN_LOW,self.SPIN_FAST]

    def get_transitions(self, state, action):
        return transitions_dict[(state,action)]

    """ Return the reward for transitioning from state to
        nextState via action
    """
    def get_reward(self, state, action, next_state):
        ...

    def is_terminal(self, state) -> bool:
        return True if self.state == self.TOP else False

    def get_discount_factor(self):
        return self.discount_factor

    def get_initial_state(self):
        return self.initial_state

    def get_goal_states(self):
        return self.goal_states

if __name__ == "__main__":
    print("prueba")