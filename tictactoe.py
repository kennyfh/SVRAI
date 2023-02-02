import numpy as np

from mdp import * 

EMPTY = '-'
PLAYER_X = 'X'
PLAYER_O = 'O'

class TicTacToe(object):

    def __init__(self):
        self.board = np.full((3,3),self.EMPTY)
        self.player_x = player_x
        self.player_o = player_o

        
        self.first_player = None

    def select_first_player(self):
        return np.random.choice([PLAYER_X,PLAYER_O])

    def move(self,action):
        ...

    def reset_board(self):
        ...
    
    def move(self,action):
        ...
    
    def print_board(self) -> None:
        ...


class Agent(MDP):
    def __init__(self):
        ...

    