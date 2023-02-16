from extensive_form_game import ExtensiveFormGame
from typing import List 
import numpy as np

HUMAN = "RED"
COMPUTER = "BLUE"


class Connect4(ExtensiveFormGame):

    """Initialise a Connect 4 Game """
    def __init__(self) -> None :
        self.players=[HUMAN,COMPUTER]

    def get_players(self) -> List[str]:
        return self.players


    def get_winner(self,state):

        



