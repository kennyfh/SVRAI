import random

"""
Creación de una clase genérica MDP
"""

class MDP(object):

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


# Valoración respecto a política
# P:MDP, pi, n
def policy_assessment(P,pi,n):
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

"""Valoración esperada"""
def expected_value(a,state,V,P):
    '''\sum_s P(s|e,a)*V(s)'''
    return sum(p*V[s] for (s,p) in P.T(state,a))

# Evolución iteratica de la política
# DUDA: PONER pi como parametro, o eliminarlo 
# y poner la 40 fija
def iterative_policy_evaluation(P,pi,k):
    V = {e:0 for e in P.states}
    # pi = {e:random.choice(mdp.A(e)) for e in mdp.estados}
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
            

# Evaluación exacta de una política en MDP
def policy_evaluation(P,pi,n):
    R,T,gamma = P.R,P.T,P.y
    V = {s:0 for s in P.states}
    for _ in range(n):
        last_V = V.copy()
        for e in P.states:
            V[e] = R(e) + gamma*sum(p*last_V[s] for (s,p) in T(e,pi[e]))
        return V