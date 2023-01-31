#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Vehicleslopev2
# Created By  : KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
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
from mdp import *
from policy_iteration import PolicyIteration
from tabular_policy import TabularPolicy

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
                 initial_state="LOW"
                 ) -> None:
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

    def get_states(self):
        return [self.LOW, self.MEDIUM, self.HIGH, self.TOP]

    def get_actions(self, state=None):
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

    def get_transitions(self, state, action):
        return self.transitions_dict[(state, action)]

    def get_reward(self, state, action, next_state):
        reward = 0.
        if state == self.TOP and next_state == self.TOP:
            reward = 100
        else:
            reward = -1 if action == self.SPIN_LOW else -2
        return reward

    def is_terminal(self, state) -> bool:
        return True if state == self.TOP else False

    def get_discount_factor(self):
        return self.discount_factor

    def get_initial_state(self):
        return self.initial_state

    def get_goal_states(self):
        return self.goal_states


if __name__ == "__main__":
    print("prueba")
    vehicle = VehicleSlopeV2()
    policy = TabularPolicy(default_action=vehicle.SPIN_LOW)
    print(policy.policy_table)
    PolicyIteration(vehicle, policy).policy_iteration(max_iterations=100)
    print(policy.policy_table)
