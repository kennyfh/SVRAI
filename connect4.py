from backward_induction import BackwardInduction
from extensive_form_game import ExtensiveFormGame
from typing import List 
import numpy as np

HUMAN = "X"
COMPUTER = "O"
EMPTY = " "


class Connect4(ExtensiveFormGame):

    def __init__(self) -> None:
        self.players = [HUMAN,COMPUTER]

    def get_players(self):
        return self.players

    def get_actions(self, state) -> np.array:

        board = state
        actions = []
        for col in range(board.shape[1]):
            # Si existen fichas vacías en la columna
            if np.any(board[:, col] == EMPTY):
                #Encontramos la fila más baja con una ficha vacía
                row = np.argmax(board[::-1, col] == EMPTY)
                if row < board.shape[0]:
                    actions.append((board.shape[0] - 1 - row, col))

        return np.array(actions)

    def get_transition(self, state, action):
        next_state = np.copy(state)
        next_state[action[0],action[1]] = self.get_player_turn(state)
        return next_state

    def get_reward(self, state):
        winner = self.get_winner(state)
        if winner == None:
            return {HUMAN:0, COMPUTER:0}
        elif winner == HUMAN:
            return {HUMAN:1,COMPUTER:-1}
        elif winner == COMPUTER:
            return {HUMAN:-1,COMPUTER:1}
        return winner
    
    def count_empty(self,board) -> np.array:
        """
        Contamos el número de casillas que tiene vacío el tablero
        """
        return np.count_nonzero(board == EMPTY)

    def is_terminal(self, state):
        """
        El juego se termina de dos maneras:
        
        1. Un jugador conecta 4 fichas horizontalmente, verticalmente o en diagonal, por lo cual gana el jugador que haya realizado esto
        2. Se llenan todas las casillas sin que ningún jugador conecte 4 fichas en las posiciones anteriormente mencionadas.
        """
        return self.count_empty(state) == 0 or self.get_winner(state) is not None

    def get_player_turn(self, state):
        """Selección del turno"""
        board = state
        empty = self.count_empty(board)        
        # HUMAN comienza el juego, por lo que si hay un número impar de celdas vacías, es el turno del ordenador
        return HUMAN if empty % 2 == 0 else COMPUTER
    

    def get_initial_state(self) -> np.array:
        """
        Creamos un tablero de las dimensiones originales del juego 
        """
        return np.full((6,7), EMPTY, dtype=str)

    def get_winner(self,state):
        board = state

        # TODO: La disposición horizontal y vertical son iguales, podemos crear una función para simplificar el método
        # Verificar si en una fila se encuentran 4 fichas del mismo jugador, si es así, ha ganado
        for row in range(board.shape[0]):
            # print(board[row])
            subarrays = np.lib.stride_tricks.sliding_window_view(board[row], 4)
            for s in subarrays:
                if np.all(s == HUMAN):
                    return HUMAN
                elif np.all(s == COMPUTER):
                    return COMPUTER
                
        # Verificar si en una columna hay 4 fichas del mismo jugador, si es así, ha ganado
        for col in range(board.shape[1]):
            subarrays = np.lib.stride_tricks.sliding_window_view(board[:,col], 4)
            for s in subarrays:
                if np.all(s == HUMAN):
                    return HUMAN
                elif np.all(s == COMPUTER):
                    return COMPUTER
        
        # Verificar si en una de las posibles diagonales de nuestro tablero existe
        diags = [board.diagonal(i) for i in range(-2, 4)]
        diags.extend(board[::-1, :].diagonal(i) for i in range(-board.shape[0]+3, board.shape[1]-2))
        for d in diags:
            if len(d) < 4:
                continue
            for i in range(len(d)-3):
                if np.all(d[i:i+4] == HUMAN):
                    return HUMAN
                elif np.all(d[i:i+4] == COMPUTER):
                    return COMPUTER
        return

if __name__ == "__main__":
    connect4 = Connect4()
    backward_induction = BackwardInduction(connect4)
    solution = backward_induction.backward_induction(connect4.get_initial_state())



    
