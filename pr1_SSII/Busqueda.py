from Classes import *
from abc import ABC,abstractmethod
from queue import PriorityQueue

class Busqueda(ABC):
    def __init__(self, problema):
        self.problema = problema
        self.nodos_explorados = 0
        self.nodos_expandidos = 0
        self.soluciones_generadas = 0
        self.coste = 0
        self.profundidad = 0
        self.frontera = []
        self.cerrados = set()

    def expandir(self, nodo, problema):
        sucesores = []
        nodo.defineAcciones()
        for accion in nodo.acciones:
            resultado = accion.destino
            s = Nodo(id=resultado, padre=nodo, problema= problema)
            s.coste = nodo.coste + accion.coste
            s.profundidad = nodo.profundidad + 1
            sucesores.append(s)
        return sucesores      
    
    def buscar(self):
        nodo_inicial = Nodo(self.problema.estado_inicial,problema=self.problema)
        self.frontera = self.insertar_nodo(nodo_inicial, self.frontera)

        while not self.es_vacio(self.frontera): #movido aqui y que salga del bucle

            # Extraemos el primer nodo de la frontera
            nodo = self.extraer_nodo(self.frontera)
            self.nodos_explorados += 1

            # Comprobamos que el nodo a comprobar no es cerrado
            if not self.cerrados.__contains__(nodo.estado.interseccion_id):
                # Comprobamos si el nodo es la solución
                if self.problema.es_objetivo(nodo.estado):
                    coste = nodo.coste
                    profundidad = nodo.profundidad
                    return nodo.getSolucion(), self.soluciones_generadas, self.nodos_explorados, self.nodos_expandidos, coste, profundidad
                
                
                
                # Si no es la solución, expandimos los nodos sucesores
                sucesores = self.expandir(nodo, self.problema)
                self.nodos_expandidos += len(sucesores)
            
                # Concatenar los sucesores a la frontera
                self.frontera = self.concatenar_nodos(self.frontera, sucesores)
                self.soluciones_generadas += len(sucesores)

                #print("\n añadido a cerrados")
                self.cerrados.add(nodo.estado.interseccion_id)
                
            
            #print("\n sigo, profundidad "+ str(nodo.profundidad))

            
        
        return None, self.soluciones_generadas, self.nodos_explorados, self.nodos_expandidos, None, None
    
    @abstractmethod
    def insertar_nodo(self, nodo, frontera):
        pass
    @abstractmethod
    def concatenar_nodos(self, frontera, sucesores):
        pass
    @abstractmethod
    def extraer_nodo(self, frontera):
        pass
    @abstractmethod
    def es_vacio(self, frontera):
        pass



class Busqueda_Anchura(Busqueda):

    def __init__(self, problema):
        super().__init__(problema)
    
    # El metodo Busqueda en anchura la lista de nodos se hace en FIFO (First in Fist Out),
    # por lo tanto se insertan los nodos al final y se sacan al principio

    # Se inserta al final
    def insertar_nodo(self, nodo, frontera):
        frontera.append(nodo)  
        return frontera
    
    # Se agregan al final
    def concatenar_nodos(self, frontera, sucesores):
        frontera.extend(sucesores)
        return frontera
    
     # Se extrae el primero (FIFO)
    def extraer_nodo(self, frontera):
        return frontera.pop(0) 
    
    def es_vacio(self, frontera):
        return len(frontera) == 0
    
    def buscar(self):
        return super().buscar()
    
class Busqueda_Profundidad(Busqueda):
    def __init__(self, problema):
        super().__init__(problema)
    
    # El metodo Busqueda en anchura la lista de nodos se hace en FILO (First in Last Out),
    # por lo tanto se insertan los nodos al principio y se sacan al principio

    # Se inserta al principio
    def insertar_nodo(self, nodo, frontera):
        frontera.insert(0, nodo)
        return frontera
    
    # Se agregan al final
    def concatenar_nodos(self, frontera, sucesores):
        return sucesores + frontera
    
     # Se extrae el primero (FIlO)
    def extraer_nodo(self, frontera):
        return frontera.pop(0) 
    
    def es_vacio(self, frontera):
        return len(frontera) == 0
    
    def buscar(self):
        return super().buscar()


class Busqueda_Primero_Mejor(Busqueda):
    def __init__(self, problema):
        super().__init__(problema)
    
    #La estructura de la frontera es una cola de prioridad (PriorityQueue), 
    # donde el nodo con mayor valor de la función heurística es el primero en salir (el que tenga mejor heurística)
    # La función heurística es la distancia entre el nodo actual y el nodo objetivo (hasta el nodo objetivo) y la velocidad máxima
    # de la carretera
    # La función heurística se calcula en el método getHeuristica
    def getHeuristica(self, nodo):
        return nodo.getDistanciaFinal() / nodo.getVelocidad()
    
    # Se inserta en la cola de prioridad
    def insertar_nodo(self, nodo, frontera):
        frontera.put((self.getHeuristica(nodo), nodo))
        return frontera

    # Se agregan los sucesores a la cola de prioridad
    def concatenar_nodos(self, frontera, sucesores):
        for sucesor in sucesores:
            frontera.put((self.getHeuristica(sucesor), sucesor))
        return frontera

    # Se extrae el nodo con la mayor prioridad (menor valor heurístico)
    def extraer_nodo(self, frontera):
        return frontera.get()[1]

    # Comprueba si la cola de prioridad está vacía
    def es_vacio(self, frontera):
        return frontera.empty()
    
    def buscar(self):
        self.frontera = PriorityQueue()
        return super().buscar()
    

    



