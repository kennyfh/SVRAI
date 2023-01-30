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



class VehicleSlopeV1(MDP):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    def __init__(self,
                discount_factor=0.8,
                energy=50
                )


    def get_states(self):
        return ["low","medium","high"]

    def get_actions(self, state):
        return []

    def get_transitions(self, state, action):
        ...

    """ Return the reward for transitioning from state to
        nextState via action
    """
    def get_reward(self, state, action, next_state):
        ...

    """ Return true if and only if state is a terminal state of this MDP """
    def is_terminal(self, state):
        ...

    """ Return the discount factor for this MDP """
    def get_discount_factor(self):
        ...

    """ Return the initial state of this MDP """
    def get_initial_state(self):
        ...

    """ Return all goal states of this MDP """
    def get_goal_states(self):
        ...

if __name__ == "__main__":
    print("prueba")