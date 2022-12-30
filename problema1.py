from mdp import *

##### 
# EJEMPLO 1: RICA Y CONOCIDA
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
        

def main():
    rc_mdp=Rica_y_Conocida()
    x = policy_iteration(rc_mdp,1000)
    #print(x)
    #print("\n")
    y = value_iteration(rc_mdp)
    #({'RC': 'No publicidad',
    #  'RD': 'No publicidad',
    #  'PC': 'No publicidad',
    #  'PD': 'Gastar en publicidad'},
    # {'RC': 54.200642541833474,
    #  'RD': 44.023220042320894,
    #  'PC': 38.603060167101546,
    #  'PD': 31.584148098472188})
    print(y)


if __name__ == "__main__":
    main()