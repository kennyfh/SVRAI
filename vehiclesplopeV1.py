#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    #States
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    # Actions
    SPIN = "SPIN"
    NOT_SPIN = "NOT_SPIN"

    def __init__(self,
                discount_factor=0.8
                )-> None:
        self.discount_factor = discount_factor
        self.transitions_dict = {
            (self.LOW,self.SPIN):[(self.MEDIUM, 1)],
            (self.LOW,self.NOT_SPIN):[(self.LOW, 1)],
            (self.MEDIUM,self.SPIN):[(self.HIGH, 1)],
            (self.MEDIUM,self.NOT_SPIN):[(self.LOW, 1)],
            (self.HIGH,self.SPIN):[(self.HIGH, 1)],
            (self.HIGH,self.NOT_SPIN):[(self.MEDIUM, 1)]
        }
            

    def get_states(self):
        return [self.LOW, self.MEDIUM, self.HIGH]

    def get_actions(self, state=None):
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

    def get_transitions(self, state, action):
        return self.transitions_dict[(state,action)]

    def get_reward(self, state, action, next_state):
        if state == self.LOW and action == self.NOT_SPIN:
            return 0
        else:
            return 3 - int(action == self.SPIN)

    def is_terminal(self, state):
        return False

    def get_discount_factor(self):
        return self.discount_factor

    def get_initial_state(self):
        return self.LOW

    def get_goal_states(self):
        return []

if __name__ == "__main__":
    print("prueba")