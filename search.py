"""
Busqueda clásica como MDP
"""


# Clase Search

class search(object):

    def __init__(self,states):
        self.states = states


    def A(self,state):
        pass


    def R(self,state,action):
        pass

    def T(self, state, action):
        pass


def forward_search(P,s,d,U):
    
    actions = P.A(s)
    
    if not actions or d<= 0:
        return (None, U(s))

    best = (None, float("-inf"))

    for a in actions:
        ss = P.T(s,a)
        u = P.R(s,a) + forward_search(P,ss,d-1,U)[1]
        if u > best[1]:
            best = (a,u)

    return best
        

def branch_and_bound(P,s,d,Ulo,Qhi):
    actions = P.A(s)

    if not actions or d<=0:
        return (None,Ulo(s))

    best = (None,float("-inf"))

    for a in actions.sort(reverse=True, key= lambda a: Qhi(s,a)):
        if Qhi(s,a) <= best[1]:
            return best

        u = P.R(s,a) + branch_and_bound(P, P.T(s,a), d-1, Ulo,Qhi)[1]

        if u > best[1]:
            best = (a,u)


    return best


def dynamic_programming(P,s,d,U,M=dict()):
    if (d,s) in M:
        return M[(d,s)]

    actions = P.A(s)

    if not actions or d <= 0:
        best = (None,U(s))

    else:
        best = (actions[0],float("-inf"))
        for a in actions:
            ss = P.T(s,a)
            u = P.R(s,a) + dynamic_programming(P,ss,d-1,U,M)[1]
            if u > best[1]:
                best = (a,u)

    M[(d,s)]= best

    return best

