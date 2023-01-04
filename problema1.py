from typing import List
from mdp import *

"""
Consideremos un vehículo que opera en una pendiente y utiliza paneles solares para recargarse. Puede encontrarse en uno de los tres
 estados de la pendiente: alto, medio y bajo. Si hace girar sus ruedas, sube la pendiente en cada paso de tiempo (de bajo a medio o de 
 medio a alto) o se mantiene alto. Si no gira las ruedas, desciende por la pendiente en cada paso de tiempo (de alto a medio o de medio 
 a bajo) o se mantiene bajo. Hacer girar las ruedas consume una unidad de energía por paso de tiempo. Estando en la parte alta o media 
 e la pendiente gana tres unidades de energía por paso de tiempo a través de los paneles solares, mientras que estando en la parte baja
  de la pendiente no gana nada de energía por paso de tiempo. El robot quiere ganar tanta energía como sea posible.

1. Representa gráficamente el MDP.
2. Resuelve el MDP utilizando la iteración de valores con un factor de descuento de 0,8.
3. Describe la política óptima
"""


class SlopeV1(MDP):
    """
    R(self, state): método que recibe un estado como entrada y devuelve la recompensa en ese estado. 
    Por ejemplo, si el vehículo se encuentra en la parte alta o media de la pendiente, se podría devolver una recompensa de
    3 unidades de energía, mientras que si se encuentra en la parte baja no se obtendría recompensa alguna.
    A(self, state): método que recibe un estado y devuelve una lista de acciones aplicables al estado. En este caso, podríamos
    considerar dos acciones: "girar las ruedas" y "no girar las ruedas".
    T(self, state, action): método que implementa el modelo de transición. Recibe un estado y una acción, 
    y devuelve una lista de tuplas (s', p), donde s' es un estado alcanzable desde el estado actual y p es la probabilidad de 
    transición desde el estado actual a s' al realizar la acción especificada.
    
    """

    def __init__(self, states: List[Tuple], y: float) -> None:
        super().__init__(states=states,y=y)
    
    def R(self, state:str)-> int:
        if state in ('high', 'medium'):
            return 3
        else:
            return 0
    
    def A(self, state):
        return ['turn', 'dont_turn']
    
    def T(self, state, action):
        if action == 'turn':
            if state == 'low':
                return [('medium', 1.0)]
            elif state == 'medium':
                return [('high', 1.0)]
            else:
                return [('high', 1.0)]
        else:
            if state == 'high':
                return [('medium', 1.0)]
            elif state == 'medium':
                return [('low', 1.0)]
            else:
                return [('low', 1.0)]
##############################################################################

"""
Supongamos ahora que el vehículo puede encontrarse en uno de los cuatro estados de la pendiente: superior, alto, medio y bajo.
Si gira sus ruedas lentamente, sube la pendiente en cada paso de tiempo (de bajo a medio, o de medio a alto, o de alto a superior) 
con una probabilidad de 0,3, y desciende por la pendiente hasta la parte baja con una probabilidad de 0,7. Si hace girar sus ruedas 
rápidamente, sube la pendiente en cada paso de tiempo (de bajo a medio, o de medio a alto, o de alto a superior) con una probabilidad 
de 0,7, y se desliza por la pendiente hasta llegar abajo con una probabilidad de 0,3. El giro lento de las ruedas consume una unidad 
de energía por paso de tiempo. Girar las ruedas rápidamente consume dos unidades de energía por unidad de tiempo. El vehículo se encuentra
 en la parte baja de la pendiente y su objetivo es llegar a la cima con el mínimo consumo de energía previsto.

1. Representa gráficamente el MDP.
2. Resuelve el MDP utilizando iteración de valor sin descuento (es decir, iteración de valor con un factor de descuento de 1).
3. Describe la política óptima.

"""


class SlopeV2(MDP):
    """
    R(self, state): Este método recibe un estado y devuelve la recompensa obtenida en ese estado. En este caso, he implementado 
    que si el estado es 'superior' la recompensa es 0, y en cualquier otro estado es -1 (para penalizar los pasos de tiempo consumidos).
    A(self, state): Este método recibe un estado y devuelve una lista de acciones aplicables en ese estado. En este caso, he 
    implementado que siempre se pueden aplicar las acciones 'slow' y 'fast'.
    T(self, state, action): Este método implementa el modelo de transición del MDP. Recibe un estado y una acción 
    y devuelve una lista de tuplas (s', p), donde s' es el estado al que se transiciona con probabilidad p desde el estado 
    s y la acción a. He implementado que si la acción es 'slow', la probabilidad de subir una posición en la pendiente es 0.3 
    y la probabilidad de no subir es 0.7. Si la acción es 'fast', la probabilidad de subir una posición en la pendiente es 0.7
    y la probabilidad de no subir es 0.3.
    """
    def __init__(self, states: List[Tuple], y: float) -> None:
        super().__init__(states=states,y=y)
    
    def R(self, state):
        if state == 'superior':
            return 0
        else:
            return -1
    
    def A(self, state):
        return ['slow', 'fast']
    
    def T(self, state, action):
        if action == 'slow':
            if state == 'low':
                return [('medium', 0.3), ('low', 0.7)]
            elif state == 'medium':
                return [('high', 0.3), ('medium', 0.7)]
            elif state == 'high':
                return [('superior', 0.3), ('high', 0.7)]
            else:
                return [('superior', 1.0)]
        else:
            if state == 'low':
                return [('medium', 0.7), ('low', 0.3)]
            elif state == 'medium':
                return [('high', 0.7), ('medium', 0.3)]
            elif state == 'high':
                return [('superior', 0.7), ('high', 0.3)]
            else:
                return [('superior', 1.0)]



def main() -> None:
    # # Creamos el MDP
    # mdp1 = SlopeV1(['high', 'medium', 'low'], y=0.8)

    # # Resolvemos el MDP utilizando el algoritmo de iteración de políticas
    # pi1 = policy_iteration(mdp1)

    # # Mostramos la política obtenida
    # print(pi1)

    mdp2 = SlopeV2(['superior', 'high', 'medium', 'low'], y=1)

    # Resolvemos el MDP utilizando el algoritmo de iteración de políticas
    pi2 = policy_iteration(mdp2)

    # Mostramos la política obtenida
    print(pi2)


    


if __name__ == "__main__":
    main()
