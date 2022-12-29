import random
# import numpy as np

"""
Creación de una clase genérica MDP
"""

class MDP:
    def __init__(self, states,y=0.9):
        # Estados
        self.states = states
        # Factor de descuento
        self.y=y
    
    def R(self,state):
        pass

    def A(self,state):
        pass

    def T(self,state,action):
        pass



            

# # Evaluación exacta de una política en MDP
# def policy_evaluation(P,pi,n):
#     R,T,gamma = P.R,P.T,P.y
#     V = {s:0 for s in P.states}
#     for _ in range(n):
#         last_V = V.copy()
#         for e in P.states:
#             V[e] = R(e) + gamma*sum(p*last_V[s] for (s,p) in T(e,pi[e]))
#         return V
    
    
##### 
# EJEMPLO 1
#####

class Rica_y_Conocida(MDP):
    
    def __init__(self,y=0.9):
        # RC: rica y conocida, RD: rica y desconocida, 
        # PC: pobre y conocida, PD: pobre y desconocida 
        self.Rdict={"RC":10,"RD":10,"PC":0,"PD":0}
        self.Tdict={("RC","No publicidad"):[("RC",0.5),("RD",0.5)],
                    ("RC","Gastar en publicidad"):[("PC",1)],
                    ("RD","No publicidad"):[("RD",0.5),("PD",0.5)],
                    ("RD","Gastar en publicidad"):[("PD",0.5),("PC",0.5)],
                    ("PC","No publicidad"):[("PD",0.5),("RC",0.5)],        
                    ("PC","Gastar en publicidad"):[("PC",1)],
                    ("PD","No publicidad"):[("PD",1)],
                    ("PD","Gastar en publicidad"):[("PD",0.5),("PC",0.5)]}
        super().__init__(["RC","RD","PC","PD"],y)
        
    def R(self,state):
        return self.Rdict[state]
        
    def A(self,state):
        return ["No publicidad","Gastar en publicidad"]
        
    def T(self,estado,accion):
        return self.Tdict[(estado,accion)]
        

### Algoritmos


# Iteración de políticas
# Valoración respecto a una política
# P:MDP, pi, n
def policy_assessment(P,pi,n):
    """
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
    """TODO: Upgrade argmax:
    https://stackoverflow.com/questions/5098580/implementing-argmax-in-python"""
    maxi = float("-inf")
    amax = None
    for x in seq:
        fx = f(x)
        if fx > maxi:
            maxi = fx
            amax = x
    return amax

#Valoración esperada
def expected_value(a,state,V,P):
    """
        Encuentra la valoración esperada de una acción respecto
        de una función de valoración V

        \sum_s P(s|e,a)*V(s)
    
    """
    return sum(p*V[s] for (s,p) in P.T(state,a))

# Algoritmo de iteración de políticas
def iterative_policy_evaluation(P:MDP,k):
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

def main():
    rc_mdp=Rica_y_Conocida()
    x = iterative_policy_evaluation(rc_mdp,1000)
    print(x)
    print("hehe")

if __name__ == "__main__":
    main()