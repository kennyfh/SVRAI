# ==========================================================
# Inteligencia Artificial. Tercer curso.
# Grado en Ingeniería Informática - Tecnologías Informáticas
# Curso 2019-20
# Ejercicio de programación
# ===========================================================

# -----------------------------------------------------------
# NOMBRE:
# APELLIDOS:
# -----------------------------------------------------------



# Escribir el código Python de las funciones que se piden en el
# espacio que se indica en cada ejercicio.

# IMPORTANTE: NO CAMBIAR EL NOMBRE NI A ESTE ARCHIVO NI A LAS FUNCIONES QUE SE
# PIDEN (aquellas funciones con un nombre distinto al que se pide en el
# ejercicio NO se corregirán).

# ESTE ENTREGABLE SUPONE 1 PUNTO DE LA NOTA TOTAL

# *****************************************************************************
# HONESTIDAD ACADÉMICA Y COPIAS: la realización de los ejercicios es un
# trabajo personal, por lo que deben completarse por cada estudiante de manera
# individual.  La discusión con los compañeros y el intercambio de información
# DE CARÁCTER GENERAL con los compañeros se permite, pero NO AL NIVEL DE
# CÓDIGO. Igualmente el remitir código de terceros, obtenido a través
# de la red o cualquier otro medio, se considerará plagio.

# Cualquier plagio o compartición de código que se detecte significará
# automáticamente la calificación de CERO EN LA ASIGNATURA para TODOS los
# alumnos involucrados, independientemente de otras medidas de carácter
# DISCIPLINARIO que se pudieran tomar. Por tanto a estos alumnos NO se les
# conservará, para futuras convocatorias, ninguna nota que hubiesen obtenido
# hasta el momento.
# *****************************************************************************

# En este entregable se pide implementar el algoritmo de iteración de valores
# para encontrar políticas óptimas en Proceso de Decisón de Markov, y
# aplicarlos a problemas de movimientos de robots en cuadrículas. 



# Lo que sigue se ha visto como parte de la práctica 4

import random

# Supondremos que un Procesos de Decisión de Markov (MDP, por sus siglas en
# inglés) va a ser un objeto de la siguiente clase (o mejor dicho, de una
# subclase de la siguiente clase). 
    
class MDP(object):

    """La clase genérica MDP tiene como métodos la función de recompensa R,
    la función A que da la lista de acciones aplicables a un estado, y la
    función T que implementa el modelo de transición. Para cada estado y
    acción aplicable al estado, la función T devuelve una lista de pares
    (ei,pi) que describe los posibles estados ei que se pueden obtener al
    plical la acción al estado, junto con la probabilidad pi de que esto
    ocurra. El constructor de la clase recibe la lista de estados posibles y
    el factor de descuento.

    En esta clase genérica, las funciones R, A y T aparecen sin definir. Un
    MDP concreto va a ser un objeto de una subclase de esta clase MDP, en la
    que se definirán de manera concreta estas tres funciones"""  

    def __init__(self,estados,descuento):

        self.estados=estados
        self.descuento=descuento

    def R(self,estado):
        pass

    def A(self,estado):
        pass
        
    def T(self,estado,accion):
        pass

# Para probar el algoritmo que se pide, podemos hacerlo con el ejemplo que se
# ha visto en la práctica 4:

class Rica_y_Conocida(MDP):
    
    def __init__(self,descuento=0.9):
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
        super().__init__(["RC","RD","PC","PD"],descuento)
        
    def R(self,estado):
        return self.Rdict[estado]
        
    def A(self,estado):
        return ["No publicidad","Gastar en publicidad"]
        
    def T(self,estado,accion):
        return self.Tdict[(estado,accion)]
        

rc_mdp=Rica_y_Conocida()

# Y lo que sigue es la implementación de iteración de políticas, que se puede
# usar para comparar con la salida que se obtenga con el algoritmo que se
# pide, iteración de valores:


def valoración_respecto_política(pi,mdp, k):
    """Calcula una aproximación a la valoración de los estados respecto de la
    política pi, aplicando el método iterativo"""
    R, T, gamma = mdp.R, mdp.T, mdp.descuento
    V = {e:0 for e in mdp.estados}
    for _ in range(k):
        V1 = V.copy()
        for s in mdp.estados:
            V[s] = R(s) + gamma *(sum([p * V1[s1] for (s1,p) in T(s, pi[s])]))
    return V


def valoración_esperada(acc,estado,V,mdp):
    """ Encuentra la valoración esperada de una acción respecto de una función
    de valoración V"""

    return sum((p * V[e] for (e,p) in mdp.T(estado, acc)))


def iteración_de_políticas(mdp,k):
    "Algoritmo de iteración de políticas"
    V = {e:0 for e in mdp.estados}
    pi = {e:random.choice(mdp.A(e)) for e in mdp.estados}
    while True:
        V = valoración_respecto_política(pi,mdp, k)
        actualizado = False
        for e in mdp.estados:
            acc = max(mdp.A(e), key=lambda a:valoración_esperada(a, e,V, mdp))
            if (acc != pi[e] and 
                valoración_esperada(acc, e,V, mdp) > valoración_esperada(pi[e], e,V, mdp)): # Por si hay empate
                pi[e] = acc
                actualizado = True
        if not actualizado:
            return pi,V


    

# =======
# PARTE 1
# =======

# Definir  una función:

#   iteración_de_valores(mdp,epsilon=0.0001)

# que implemente el algoritmo de iteración de valores que se ha explicado en
# clase, donde mdp es un objeto de la clase MDP definida anteriormente, y
# epsilon es la cota de error máximo que se permite. Devolver tanto la
# valoración como la política óptima encontrada. 

# Ejemplos:

# In [ ]: iteración_de_valores(rc_mdp)
# Out[ ]: 

#({'RC': 'No publicidad',
#  'RD': 'No publicidad',
#  'PC': 'No publicidad',
#  'PD': 'Gastar en publicidad'},
# {'RC': 54.200642541833474,
#  'RD': 44.023220042320894,
#  'PC': 38.603060167101546,
#  'PD': 31.584148098472188})

# In [ ]: iteración_de_valores(rc_mdp,epsilon=0.0000000001)
# Out[9]: 

#({'RC': 'No publicidad',
#  'RD': 'No publicidad',
#  'PC': 'No publicidad',
#  'PD': 'Gastar en publicidad'},
# {'RC': 54.20159875209799,
#  'RD': 44.02417625258542,
#  'PC': 38.60401637736608,
#  'PD': 31.585104308736717})

# =========== Solución:
            












# ========
# PARTE II
# =========


# Vamos ahora a tratar otros MDP's, en concreto los correspondientes al
# movimiento de un robot en una cuadrícula, tal y como se describe en el tema
# 4. En este caso las acciones posibles en cualquier casilla no terminal son
# "arriba", "abajo", "izquierda" y "derecha", pero existe una probabilidad p
# de que la acción no tenga su efecto deseado, y se dirija a una de las dos
# casillas que están en direcciones perpendiculares a la que se quería
# ir. Además, si se dirige hacia una pared o hacia una casilla bloqueda, el
# robot quedará en la misma posición. Por último, en una casilla terminal, la
# única acción posible es "exit" (es una acción ficticia que no cambia de
# casilla). Ver los detalles en el tema 4.


# En concreto, queremos saber las políticas óptimas que ha de seguir el robot
# en las siguientes cuadrículas (la primera es la que se ha visto en clase): 

# CUADRÍCULA 1
# ------------

# -----------------
# |   |   |   | +1|
# -----------------
# |   | * |   | -1|
# -----------------
# |   |   |   |   |
# -----------------

# CUADRÍCULA 2
# ------------


# ---------------------
# |   |   |   |   |   |
# ---------------------
# |   | * |   |   |   |
# ---------------------
# |   | * | +1| * |+10|
# ---------------------
# |   |   |   |   |   |
# ---------------------
# |-10|-10|-10|-10|-10|
# ---------------------

# CUADRÍCULA 3
# ------------


# ------------------------------------
# |  * |-100|-100|-100|-100|-100| *  |
# ------------------------------------
# | +1 |    |    |    |    |    | +10|
# ------------------------------------
# |  * |-100|-100|-100|-100|-100| *  |
# ------------------------------------







# En python, las cuadrículas las vamos a representar mediante una lista cuyos
# elementos son a su vez listas que representan las sucesivas filas de la
# cuadrícula, y los elementos de esas listas representan las sucesivas
# casillas de la fila. Un asterisco significa una casilla bloqueada (por la
# que no se puede pasar), el resto de casillas son transitables. Si la casilla
# contiene un número, se considera que es una casilla terminal, y el número
# indica la recompensa en esa casilla. Si contiene un espacio en blanco, 
# se supone que tiene la recompensa por defecto.

# Ésta es la representación python de las tres cuadrículas anteriores:

cuadrícula_1 = [[' ',' ',' ',+1],
                [' ','*',' ',-1],
                [' ',' ',' ',' ']]


cuadrícula_2 = [[' ',' ',' ',' ',' '],
                [' ','*',' ',' ',' '],
                [' ','*', 1,'*', 10],
                [' ',' ',' ',' ',' '],
                [-10,-10, -10, -10, -10]]

cuadrícula_3 = [[ '*',-100, -100, -100, -100, -100, '*'],
               [   1,  ' ',  ' ',  ' ',  ' ',  ' ',  10],
               [ '*',-100, -100, -100, -100, -100, '*']]



# Se pide definir una clase Cuadrícula, subclase de MDP, que define el
# problema de movimiento del robot por una cuadrícula. El constructor de esta
# subclase recibe como argumentos de entrada los siguientes:
# - cuadrícula: una cuadrícula, representada como se ha indicado.
# - recompensa_por_defecto: recompensa de las casillas no terminales, con
#   valor por defecto -0.04.
# - descuento: con valor por defecto 0.9
# - ruido: la probabilidad de que una acción no siga el efecto deseado, y haga
#   uno de los dos movimientos perpendiculares al deseado. Por defecto, valor
#   0.2. (Por ejemplo, si el ruido es 0.2 y se aplica la acción "arriba", con
#   probabilidad 0.8 el robot intentará ir arriba, con proabilidad 0.1 a la
#   izquierda, y con probabilidad 0.1 a la derecha.     
# En esta subclase tenemos que definir los métodos R, A y T, y además se
# pueden incluir como atributos adicionales lo que se considere necesario. Hay
# dos observaciones que debemos tener en cuenta: 

# * Los estados terminales se tratan de manera especial en este caso. La única
#   acción aplicable a un estado terminal es "exit", y la aplicación de "exit" a
#   un estado terminal no debe producir ningún estado; por eso consideramos que
#   en ese caso T(estado,"exit") es [(estado,0)], es decir se produce el mismo
#   estado, pero con probabilidad 0.

# * En un MDP de cuadrícula, los estados son las casillas y por tanto se
#   representan por un par de coordenadas. Por simplificar, supondremos que la
#   esquina superior izquierda es el (0,0) (Atención: este origen de coordenadas
#   es distinto del que se usa en las diapositivas). 

# Una vez definida la clase Cuadrícula, aplicar el algoritmo de iteración de
# valores del ejercicio anterior, para obtener distintas políticas óptimas
# en las cuadrículas anteriores, con distintos valores de ruido y/o recompensa por
# defecto. Tratar de justificar, mediante una explicación intuitiva, los
# resultados obtenidos.

# Puede ser útil, a la hora de visualizar gráficamente las distintas políticas
# obtenidas, la siguiente función que dibuja la cuadrícula y la dentro de cada
# casilla una flecha representando la acción que según la política hay que
# realizar en esa casilla (Nota: para que funcione, tendremos que haber
# definido la clase Cuadrícula con al menos dos atributos nfilas y ncolumnas
# con el número de filas y de columnas de la cuadrícula).

def imprime_política_cuadricula(pi,mdp):
    flechas={"arriba":"↑", "abajo":"↓",
    "izquierda":"←","derecha":"→","exit":" "}
    lv="-"*(mdp.ncolumnas*4+1)+"\n"
    str=lv
    print()
    for f in range(mdp.nfilas):
        for c in range(mdp.ncolumnas):
            if (f,c) in mdp.estados:
                str+="| "+flechas[pi[(f,c)]]+" "
            else:
                str+="| * "
        str+="|\n"+lv
    print(str)


# Por ejemplo:

# >>> mdp_c1=Cuadrícula(cuadrícula_1)
# >>> pi_c1,_=iteración_de_valores(mdp_c1)
# >>> imprime_política_cuadricula(pi_c1,mdp_c1)

# -----------------
# | → | → | → |   |
# -----------------
# | ↑ | * | ↑ |   |
# -----------------
# | ↑ | → | ↑ | ← |
# -----------------



# >>> mdp_c2=Cuadrícula(cuadrícula_2)
# >>> pi_c2,_=iteración_de_valores(mdp_c2)
# >>> imprime_política_cuadricula(pi_c2,mdp_c2)

# ---------------------
# | → | → | → | → | ↓ |
# ---------------------
# | ↑ | * | → | → | ↓ |
# ---------------------
# | ↑ | * |   | * |   |
# ---------------------
# | ↑ | ↑ | → | → | ↑ |
# ---------------------
# |   |   |   |   |   |
# ---------------------



# ---------------------------------------------------------------------    

# ========= Solución: 



        

        

        
