class MountainCar:
    def __init__(self) -> None:
        ...

    def get_initial_state(self):
        ...

    def get_actions(self,state):
        ...

    def is_terminal(self,state):
        ...

    def execute(self,state,action):
        ...