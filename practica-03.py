# practica-03.py
# Inteligencia Artificial, 
# Tercer curso del Grado de Ingeniería Informática - Tecnologías Informáticas. 
# Universidad de Sevilla.

# Práctica 3: Búsqueda en espacios de estados
# ===========================================

# En esta práctica aplicaremos los algoritmos de búsqueda vistos en clase,
# viendo cómo se comportan con el problema del 8 puzzle. 

# La práctica tiene tres partes bien diferenciadas:

# Parte I: Representación de problemas de espacios de estados. Veremos una
# técnica general para hacerlo, y en particular se implementará el problema del
# ocho puzzle.

# Parte II: Experimentación con los algoritmos implementados. Ejecución de los
# algoritmos implementados, para la búsuqeda de soluciones a instancias
# concretas de los problemas.

# Parte III: Calcularemos algunos estadísticas sobre la ejecución de los
# algoritmos para resolución de problemas de ocho puzzle. Así, se comprobarán
# experimentalmente algunas propiedades de los algoritmos.


# El código que se usa en esta práctica está basado principalmente en el
# código Python que se proporciona con el libro "Artificial Intelligence: A
# Modern Approach" de S. Russell y P. Norvig
# (http://code.google.com/p/aima-python, módulo search.py). Las modificaciones
# al código y la traducción han realizadas por José Luis Ruiz Reina (Depto. de
# Ciencias de la Computación e Inteligencia Artificial de la Universidad de
# Sevilla).







#===============================================
# PARTE I. REPRESENTACIÓN DE ESPACIOS DE ESTADOS
#===============================================



# Recuérdese que según lo que se ha visto en clase, la implementación de la
# representación de un problema de espacio de estados consiste en:

# * Representar estados y acciones mediante una estructura de datos.
# * Definir: estado_inicial, es_estado_final(_), acciones(_), aplica(_,_) y
#   coste_de_aplicar_accion, si el problema tiene coste.

# La siguiente clase Problema representa este esquema general de cualquier
# problema de espacio de estados. Un problema concreto será una subclase de
# Problema, y requerirá implementar acciones, aplica y eventualmente __init__,
# es_estado_final y  coste_de_aplicar_accion. 


class Problema(object):
    """Clase abstracta para un problema de espacio de estados. Los problemas
    concretos habría que definirlos como subclases de Problema, implementando
    acciones, aplica y eventualmente __init__, es_estado_final y
    coste_de_aplicar_accion. Una vez hecho esto, se han de crear instancias de
    dicha subclase, que serán la entrada a los distintos algoritmos de
    resolución mediante búsqueda."""  


    def __init__(self, estado_inicial, estado_final=None):
        """El constructor de la clase especifica el estado inicial y
        puede que un estado_final, si es que es único. Las subclases podrían
        añadir otros argumentos"""
        
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

    def acciones(self, estado):
        """Devuelve las acciones aplicables a un estado dado. Lo normal es
        que aquí se devuelva una lista, pero si hay muchas se podría devolver
        un iterador, ya que sería más eficiente."""
        abstract

    def aplica(self, estado, accion):
        """ Devuelve el estado resultante de aplicar accion a estado. Se
        supone que accion es aplicable a estado (es decir, debe ser una de las
        acciones de self.acciones(estado)."""
        abstract

    def es_estado_final(self, estado):
        """Devuelve True cuando estado es final. Por defecto, compara con el
        estado final, si éste se hubiera especificado al constructor. Si se da
        el caso de que no hubiera un único estado final, o se definiera
        mediante otro tipo de comprobación, habría que redefinir este método
        en la subclase.""" 
        return estado == self.estado_final

    def coste_de_aplicar_accion(self, estado, accion):
        """Devuelve el coste de aplicar accion a estado. Por defecto, este
        coste es 1. Reimplementar si el problema define otro coste """ 
        return 1

# Lo que sigue es un ejemplo de cómo definir un problema como subclase
# de problema. En concreto, el problema de las jarras, visto en clase:

class Jarras(Problema):
    """Problema de las jarras:
    Representaremos los estados como tuplas (x,y) de dos números enteros,
    donde x es el número de litros de la jarra de 4 e y es el número de litros
    de la jarra de 3"""

    def __init__(self):
        super().__init__((0,0))

    def acciones(self,estado):
        jarra_de_4=estado[0]
        jarra_de_3=estado[1]
        accs=list()
        if jarra_de_4 > 0:
            accs.append("vaciar jarra de 4")
            if jarra_de_3 < 3:
                accs.append("trasvasar de jarra de 4 a jarra de 3")
        if jarra_de_4 < 4:
            accs.append("llenar jarra de 4")
            if jarra_de_3 > 0:
                accs.append("trasvasar de jarra de 3 a jarra de 4")
        if jarra_de_3 > 0:
            accs.append("vaciar jarra de 3")
        if jarra_de_3 < 3:
            accs.append("llenar jarra de 3")
        return accs

    def aplica(self,estado,accion):
        j4=estado[0]
        j3=estado[1]
        if accion=="llenar jarra de 4":
            return (4,j3)
        elif accion=="llenar jarra de 3":
            return (j4,3)
        elif accion=="vaciar jarra de 4":
            return (0,j3)
        elif accion=="vaciar jarra de 3":
            return (j4,0)
        elif accion=="trasvasar de jarra de 4 a jarra de 3":
            return (j4-3+j3,3) if j3+j4 >= 3 else (0,j3+j4)
        else: #  "trasvasar de jarra de 3 a jarra de 4"
            return (j3+j4,0) if j3+j4 <= 4 else (4,j3-4+j4)

    def es_estado_final(self,estado):
        return estado[0]==2


# Ejemplos:

# >>> pj = Jarras()
# >>> pj.estado_inicial
# (0, 0)
# >>> pj.acciones(pj.estado_inicial)
# ['llenar jarra de 4', 'llenar jarra de 3']
# >>> pj.aplica(pj.estado_inicial,"llenar jarra de 4")
# (4, 0)
# >>> pj.coste_de_aplicar_accion(pj.estado_inicial,"llenar jarra de 4")
# 1
# >>> pj.es_estado_final(pj.estado_inicial)
# False

    
    
# -----------
# Ejercicio 1
# -----------    

# ---------------------------------------------------------------------------
# Definir la clase Ocho_Puzzle, que implementa la representación del
# problema del 8-puzzle visto en clase. Para ello, completar el código que se
# presenta a continuación, en los lugares marcados con interrogantes.
# ----------------------------------------------------------------------------


# class Ocho_Puzzle(Problema):
#     """Problema a del 8-puzzle.  Los estados serán tuplas de nueve elementos,
#     permutaciones de los números del 0 al 8 (el 0 es el hueco). Representan la
#     disposición de las fichas en el tablero, leídas por filas de arriba a
#     abajo, y dentro de cada fila, de izquierda a derecha. Por ejemplo, el
#     estado final será la tupla (1, 2, 3, 8, 0, 4, 7, 6, 5). Las cuatro
#     acciones del problema las representaremos mediante las cadenas:
#     "Mover hueco arriba", "Mover hueco abajo", "Mover hueco izquierda" y
#     "Mover hueco dercha", respectivamente. 
#     """"

#     def __init__(self,tablero_inicial):
#         super().__init__(estado_inicial=?????, estado_final=?????)

#     def acciones(self,estado):
#         pos_hueco=estado.index(0)
#         accs=list()
#         if pos_hueco not in ?????: 
#             accs.append(?????)
#         if pos_hueco not in ?????: 
#             accs.append(?????)
#         if pos_hueco not in ?????: 
#             accs.append(?????)
#         if pos_hueco not in ?????: 
#             accs.append(?????)
#         return accs     

#     def aplica(self,estado,accion):
#         ???????

# Ejemplos que se pueden ejecutar una vez se ha definido la clase:

# >>> p8p_1 = Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# >>> p8p_1.estado_inicial
# (2, 8, 3, 1, 6, 4, 7, 0, 5)
# >>> p8p_1.estado_final
# (1, 2, 3, 8, 0, 4, 7, 6, 5)
# >>> p8p_1.acciones(p8p_1.estado_inicial)
# ['Mover hueco arriba', 'Mover hueco izquierda', 'Mover hueco derecha']
# >>> p8p_1.aplica(p8p_1.estado_inicial,"Mover hueco arriba")
# (2, 8, 3, 1, 0, 4, 7, 6, 5)
# >>> p8p_1.coste_de_aplicar_accion(p8p_1.estado_inicial,"Mover hueco arriba")
# 1

# ----------------------------------------------------------------------------





#=========================
# PARTE II. Experimentando
#=========================


# -----------
# Ejercicio 2
# -----------

# Usar búsqueda en anchura y en profundidad para encontrar soluciones tanto al
# problema de las jarras como al problema del ocho puzzle con distintos
# estados iniciales.

# Ejemplos de uso:

# >>> búsqueda_en_anchura(Jarras()).solucion()
# ['llenar jarra de 4', 'trasvasar de jarra de 4 a jarra de 3', 
#  'vaciar jarra de 3', 'trasvasar de jarra de 4 a jarra de 3', 
#  'llenar jarra de 4', 'trasvasar de jarra de 4 a jarra de 3']
# >>> búsqueda_en_profundidad(Jarras()).solucion()
# ['llenar jarra de 3', 'trasvasar de jarra de 3 a jarra de 4', 
#  'llenar jarra de 3', 'trasvasar de jarra de 3 a jarra de 4', 
#  'vaciar jarra de 4', 'trasvasar de jarra de 3 a jarra de 4']
# >>> búsqueda_en_anchura(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solucion()
# ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda', 
#  'Mover hueco abajo', 'Mover hueco derecha']
# >>> búsqueda_en_profundidad(Ocho_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))).solucion()
# ['Mover hueco derecha', 'Mover hueco arriba', ... ] # ¡más de 3000 acciones!

# No olvidar cargar el módulo con los algoritmos de búsqueda:

from algoritmos_de_búsqueda import *

# ------------------------------------------

# -----------
# Ejercicio 3
# -----------


# Definir las dos funciones heurísticas para el 8 puzzle que se han visto en
# clase. Es decir:
# - h1_ocho_puzzle(estado): cuenta el número de casillas mal colocadas respecto
#   del estado final.
# - h2_ocho_puzzle_estado(estado): suma la distancia Manhattan desde cada casilla
#   a la posición en la que debería estar en el estado final. 

# Ejemplos:

# >>> h1_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# 4
# >>> h2_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# 5
# >>> h1_ocho_puzzle((5,2,3,0,4,8,7,6,1))
# 4
# >>> h2_ocho_puzzle((5,2,3,0,4,8,7,6,1))
# 11




# ------------------------------------------------------------------------------









#============
# Ejercicio 4
#============

# Resolver usando búsqueda_óptima, búsqueda_primero_el_mejor y
# búsqueda_a_estrella (con las dos heurísticas), el problema del 8 puzzle para
# el siguiente estado inicial:

#              +---+---+---+
#              | 2 | 8 | 3 |
#              +---+---+---+
#              | 1 | 6 | 4 |
#              +---+---+---+
#              | 7 | H | 5 |
#              +---+---+---+

# ---------------------------------------------------------------------------------


#========================
# PARTE III. Estadísticas
#========================


# La siguientes definiciones nos van a permitir experimentar con distintos
# estados iniciales, algoritmos y heurísticas, para resolver el
# 8-puzzle. Además se van a contar el número de nodos analizados durante la
# búsqueda:


class Problema_con_Analizados(Problema):

    """Es un problema que se comporta exactamente igual que el que recibe al
       inicializarse, y además incorpora un atributos nuevos para almacenar el
       número de nodos analizados durante la búsqueda. De esta manera, no
       tenemos que modificar el código del algorimo de búsqueda.""" 
         
    def __init__(self, problema):
        self.estado_inicial = problema.estado_inicial
        self.problema = problema
        self.analizados  = 0

    def acciones(self, estado):
        return self.problema.acciones(estado)

    def aplica(self, estado, accion):
        return self.problema.aplica(estado, accion)

    def es_estado_final(self, estado):
        self.analizados += 1
        return self.problema.es_estado_final(estado)

    def coste_de_aplicar_accion(self, estado, accion):
        return self.problema.coste_de_aplicar_accion(estado,accion)



def resuelve_ocho_puzzle(estado_inicial, algoritmo, h=None):
    """Función para aplicar un algoritmo de búsqueda dado al problema del ocho
       puzzle, con un estado inicial dado y (cuando el algoritmo lo necesite)
       una heurística dada.
       Ejemplo de uso:

       >>> resuelve_ocho_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5),búsqueda_a_estrella,h2_ocho_puzzle)
       Solución: ['Mover hueco arriba', 'Mover hueco arriba', 'Mover hueco izquierda', 
                  'Mover hueco abajo', 'Mover hueco derecha']
       Algoritmo: búsqueda_a_estrella
       Heurística: h2_ocho_puzzle
       Longitud de la solución: 5. Nodos analizados: 7
       """

    p8p=Problema_con_Analizados(Ocho_Puzzle(estado_inicial))
    sol= (algoritmo(p8p,h).solucion() if h else algoritmo(p8p).solucion()) 
    print("Solución: {0}".format(sol))
    print("Algoritmo: {0}".format(algoritmo.__name__))
    if h: 
        print("Heurística: {0}".format(h.__name__))
    else:
        pass
    print("Longitud de la solución: {0}. Nodos analizados: {1}".format(len(sol),p8p.analizados))


#============
# Ejercicio 5
#============

# Intentar resolver usando las distintas búsquedas y en su caso, las distintas
# heurísticas, el problema del 8 puzzle para los siguientes estados iniciales:

#           E1              E2              E3              E4
#           
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+    
#     | 2 | 8 | 3 |   | 4 | 8 | 1 |   | 2 | 1 | 6 |   | 5 | 2 | 3 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 1 | 6 | 4 |   | 3 | H | 2 |   | 4 | H | 8 |   | H | 4 | 8 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 7 | H | 5 |   | 7 | 6 | 5 |   | 7 | 5 | 3 |   | 7 | 6 | 1 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
    
# Se pide, en cada caso, hacerlo con la función resuelve_ocho_puzzle, para
# obtener, además de la solución, la longitud (el coste) de la solución
# obtenida y el número de nodos analizados. Anotar los resultados en la
# siguiente tabla (L, longitud de la solución, NA, nodos analizados), y
# justificarlos con las distintas propiedades teóricas estudiadas.

# -----------------------------------------------------------------------------------------
#                                       E1           E2           E3          E4
                                
# Anchura                             L=            L=           L=          L=  
#                                     NA=           NA=          NA=         NA= 
                                                                              
# Profundidad                         L=            L=           L=          L=  
#                                     NA=           NA=          NA=         NA= 
                                                                              
# Óptima                              L=            L=           L=          L=  
#                                     NA=           NA=          NA=         NA= 
                                                                              
# Primero el mejor (h1)               L=            L=           L=          L=
#                                     NA=           NA=          NA=         NA=
                                                                              
# Primero el mejor (h2)               L=            L=           L=          L= 
#                                     NA=           NA=          NA=         NA=
                                                                              
# A* (h1)                             L=            L=           L=          L= 
#                                     NA=           NA=          NA=         NA=
                                                                              
# A* (h2)                             L=            L=           L=          L= 
#                                     NA=           NA=          NA=         NA=

# -----------------------------------------------------------------------------------------







#============
# Ejercicio 6
#============

# La siguiente heurística h3_ocho_puzzle se obtiene sumando a la heurística
# h2_ocho_puzzle una componente que cuantifica la "secuencialidad" en las
# casillas de un tablero, al recorrerlo en el sentido de las aguas del reloj
# ¿Es h3 admisble? Comprobar cómo se comporta esta heurística cuando se usa en
# A*, con cada uno de los estados anteriores. Comentar los resultados.


def h3_ocho_puzzle(estado):

    suc_ocho_puzzle ={0: 1, 1: 2, 2: 5, 3: 0, 4: 4, 5: 8, 6: 3, 7: 6, 8: 7}  

    def secuencialidad_aux(estado,i):
        
        val=estado[i]
        if val == 0:
            return 0
        elif i == 4:
            return 1
        else:
            i_sig=suc_ocho_puzzle[i]
            val_sig = (val+1 if val<8 else 1)
            return 0 if val_sig == estado[i_sig] else 2 

    def secuencialidad(estado):
        res= 0 
        for i in range(8): 
            res+=secuencialidad_aux(estado,i)
        return res    

    return h2_ocho_puzzle(estado) + 3*secuencialidad(estado)
                   

