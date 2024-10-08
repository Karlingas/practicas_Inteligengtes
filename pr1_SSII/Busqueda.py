from Classes import *
from abc import ABC,abstractmethod

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
        for accion in problema.acciones(nodo.estado):
            resultado = problema.resultado(nodo.estado, accion)
            s = Nodo(resultado, nodo, accion)
            s.coste = nodo.coste + problema.coste_individual(nodo, accion, s)
            s.profundidad = nodo.profundidad + 1
            sucesores.append(s)
        return sucesores      
    
    def buscar(self):
        nodo_inicial = Nodo(self.problema.estado_inicial)
        self.insertar_nodo(nodo_inicial, self.frontera)

        while True:
            # Comprobamos que la frontera no está vacía
            if self.es_vacio(self.frontera):
                # No hay solución
                return None, self.soluciones_generadas, self.nodos_explorados, self.nodos_expandidos, None, None
            
            # Extraemos el primer nodo de la frontera
            nodo = self.extraer_nodo(self.frontera)
            self.nodos_explorados += 1

            # Comprobamos si el nodo es la solución
            if self.problema.es_objetivo(nodo.estado):
                coste = nodo.coste
                profundidad = nodo.profundidad
                return nodo.solucion(), self.soluciones_generadas, self.nodos_explorados, self.nodos_expandidos, coste, profundidad
            
            # Si no es la solución, expandimos los nodos sucesores
            sucesores = self.expandir(nodo, self.problema)
            self.nodos_expandidos += len(sucesores)
            
            # Concatenar los sucesores a la frontera
            self.concatenar_nodos(self.frontera, sucesores)
            self.soluciones_generadas += len(sucesores)
    
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
        
    # Se inserta al final
    def insertar_nodo(self, nodo, frontera):
        frontera.append(nodo)  
    
    # Se agregan al final
    def concatenar_nodos(self, frontera, sucesores):
        frontera.extend(sucesores)  
    
     # Se extrae el primero (FIFO)
    def extraer_nodo(self, frontera):
        return frontera.pop(0) 
    
    def es_vacio(self, frontera):
        return len(frontera) == 0
    
    def buscar(self):
        return super().buscar()
    
    

            
                

#class Busqueda_Profundidad(Busqueda):


#class Busqueda_Primero_Mejor(Busqueda):



