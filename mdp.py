import random

"""
Creación de una clase genérica MDP
"""

class MDP:
    def __init__(self, states,y=0.9):
        """
        States: atributo para almacenar una lista con los estados del MDP
        """
        self.states = states
        """
        y: atributo que almacena el descuento para la valoración
        de las secuencias de estados
        """
        self.y=y
    
    def R(self,state):
        """"
        Método que recibe un estado como entrada y devuelve
        la recompensa en ese estado
        """
        pass

    def A(self,state):
        """
        Método que recibe un estado y devuelve una lista de acciones
        aplicables al estado
        """
        pass

    def T(self,state,action):
        """
        Método que implementa el modelo de transición
        """
        pass

# =======
# ALGORITMOS
# =======

# 1. Algoritmo Iteración de políticas

def policy_assessment(P:MDP,pi,n):
    """
    Valoración respecto a una política

    Calcula una aproximación a la valoración de los estados
    respecto a una política pi, aplicando el método iterativo
    """
    R,T, gamma = P.R, P.T, P.y
    V = {s:0 for s in P.states}
    for _ in range(n):
        last_V = V.copy()
        for e in P.states:
            V[e] = R(e) + gamma*sum(p*last_V[s] for (s,p) in T(e,pi[e]))
    return V

def argmax(seq,f):
    """
    Función auxiliar para poder obtener el argumento máximo
    sobre unas secuencia de elementos.

    TODO: Podría mejorarse realizando esto
    https://stackoverflow.com/questions/5098580/implementing-argmax-in-python"""
    maxi = float("-inf")
    amax = None
    for x in seq:
        fx = f(x)
        if fx > maxi:
            maxi = fx
            amax = x
    return amax

def expected_value(a,state,V,P):
    """
        Valoración esperada 

        Encuentra la valoración esperada de una acción respecto
        de una función de valoración V

        \sum_s P(s|e,a)*V(s)
    
    """
    return sum(p*V[s] for (s,p) in P.T(state,a))

def policy_iteration(P:MDP,k):
    """
    Algoritmo de iteración de políticas

    """
    V = {e:0 for e in P.states}
    pi = {e:random.choice(P.A(e)) for e in P.states}
    while True:
        V = policy_assessment(P,pi,k)
        update=False
        for s in P.states:
            acc=argmax(P.A(s), lambda a : expected_value(a,s,V,P))
            if(acc!=pi[s] and expected_value(acc,s,V,P)>expected_value(pi[s],s,V,P)):
                pi[s] =acc
                update=True
        if not update:
            return pi,V

# 2º Algoritmo de iteración de valores

def value_iteration(P:MDP,epsilon:float=0.0001):
    """
    Algoritmo de iteración de valores

    P: Problema MDP
    epsilon: cota de error máximo que se permite

    """
    # Sea V una función sobre los estados, con valor 0
    # para cada estado que tengamos
    V = {s:0 for s in P.states} # Vo
    delta = float("inf")
    R, gamma = P.R, P.y  # γ
    # Repetir
    while True:
        V_last = V.copy() # Vi-1
        delta = 0
        # Para cada estado s
        for s in P.states:
            V[s] = R(s) + gamma * max(expected_value(a,s,V_last,P) for a in P.A(s))

            # Si  |Vi (s) − Vi−1(s)| > δ
            error = abs(V[s] - V_last[s])
            if error > delta:
                delta = error
        # Hasta que se supere la cota de error máximo que se permite
        #  δ < epsilon · (1 − γ)/γ
        if delta < epsilon * (1-gamma) / gamma:
            break

    # Calculamos π*
    policy = {s:argmax(P.A(s),lambda a : expected_value(a,s,V,P) ) for s in P.states}

    return policy,V

