from abc import ABC, abstractmethod
from collections import deque
import copy
from Clases import *
import time
from queue import PriorityQueue

class Busqueda(ABC):
    def __init__(self, problema):
        #Datos que necesitamos para el problems
        self.problema = problema
        self.nodos_cerrados = set()
        self.frontera = None

        #Datos para las estadisticas
        self.tiempo_ejecucion = 0
        self.nodos_generados = 0
        self.nodos_expandidos = 0
        self.profundidad_sol = 0
        self.coste_sol = 0
        self.hay_sol = False
        self.solucion = []
    
    #Metodos implementados en las clases especificas
    @abstractmethod
    def insertarNodo(self, nodo, frontera):
        pass
    @abstractmethod
    def extraerNodo(self, frontera):
        pass
    @abstractmethod
    def esVacio(self, frontera):
        pass
    
    #Metodos para las estadisticas
    def formatoTiempo(self, tiempo_total): #El tiempo total tiene que estar dado en segundos
        horas = int(tiempo_total // 3600)
        minutos = int((tiempo_total % 3600) // 60)
        segundos = int(tiempo_total % 60)
        milisegundos = int((tiempo_total - int(tiempo_total)) * 1000000)
        tiempo_formateado = f"{horas:01d}:{minutos:02d}:{segundos:02d}.{milisegundos:06d}"
        return tiempo_formateado

    def formatoSolucion(self, solucion):
        return [f"( {solucion[i]} -> {solucion[i + 1]} )" for i in range(len(solucion) - 1)]

    def imprimirEstadisticas(self):
        if self.hay_sol:
            print("\nEstadísticas:")
            print(f"Nodos generados: {self.nodos_generados}")
            print(f"Nodos expandidos: {self.nodos_expandidos}")
            print(f"Tiempo de ejecuccion: {self.formatoTiempo(self.tiempo_ejecucion)}")
            print(f"Profundidad de la solución: {self.profundidad_sol}")
            print(f"Coste: {self.formatoTiempo(self.coste_sol)}")
            print("Solución encontrada:", self.formatoSolucion(self.solucion))
        else:
            print("\n\nNo se encontró solución.")

    #Metodos para la busqueda

    def expandir(self, nodo):
        sucesores = []
        acciones = PriorityQueue()
        acciones.queue = copy.deepcopy(self.problema.getAcciones(nodo.estado)) 
        #Por alguna razon, si no hago copia, se elimina la queue de problema

        while not acciones.empty():
            accion = acciones.get()[1]
            accion_sucesor = nodo.estado.aplicarAccion(accion)
            nuevo_nodo = Nodo(
                self.problema.intersecciones[accion_sucesor],
                padre=nodo,
                coste=nodo.coste + accion.coste,
                profundidad=nodo.profundidad + 1,
                generado=nodo.generado + 1
            )
            sucesores.append(nuevo_nodo)
        
        return sucesores

    
    def busqueda(self):
        inicio = time.perf_counter()
        e_inicial = Nodo(self.problema.estado_inicial)
        self.insertarNodo(e_inicial, self.frontera)
        #self.nodos_generados += 1

        while not self.esVacio(self.frontera):
            nodo = self.extraerNodo(self.frontera)
            if nodo.estado.interseccion in self.nodos_cerrados:
                continue

            if self.problema.esObjetivo(nodo.estado):
                self.tiempo_ejecucion = time.perf_counter() - inicio
                self.hay_sol = True
                self.profundidad_sol = nodo.profundidad
                self.coste_sol = nodo.coste
                self.solucion = nodo.getSolucion()
                return self.imprimirEstadisticas()
            
            #Ha sido explorado y no es solucion
            self.nodos_expandidos += 1
            self.nodos_cerrados.add(nodo.estado.interseccion)
            #expandimos
            sucesores = self.expandir(nodo)

            for sucesor in sucesores:
                self.insertarNodo(sucesor, self.frontera)
                self.nodos_generados += 1
            
        
        return self.imprimirEstadisticas()

class Busqueda_a_estrella(Busqueda):
    def __init__(self, problema):
        super().__init__(problema)
        self.frontera = PriorityQueue()
        self.heuristica = Heuristica_Geodesica(problema)

    def insertarNodo(self, nodo, frontera):
        final = self.heuristica.getHeutistica(nodo.estado) / self.problema.veloMax
        nodo.heuristica =  nodo.coste + final 
        frontera.put(((nodo.heuristica), nodo))

    def extraerNodo(self, frontera):
        return frontera.get()[1]

    def esVacio(self, frontera):
        return frontera.empty()

class Heuristica(ABC):
    def __init__(self, problema):
        self.problema = problema
        #Obtenemos la lat y lon del estado objetivo
        self.lat_objetivo = self.problema.estado_objetivo.latitud
        self.lon_objetivo = self.problema.estado_objetivo.longitud
    def getHeutistica(self, estado):
        pass

class Heuristica_Geodesica(Heuristica):
    def __init__(self, problema):
        super().__init__(problema)

    def getHeutistica(self, estado):
        # Obtener la intersección actual del estado
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = self.problema.intersecciones[estado.interseccion].latitud
        lon_actual = self.problema.intersecciones[estado.interseccion].longitud

        #Formula para el calculo de la distancia geodesica
        distancia = geodesic((lat_actual, lon_actual), (self.lat_objetivo, self.lon_objetivo)).kilometers * 1000

        return distancia

class Heuristica_Euclides(Heuristica):
    def __init__(self, problema):
        super().__init__(problema)

    def getHeutistica(self, estado):
        # Obtener la intersección actual del estado
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = self.problema.intersecciones[estado.interseccion].latitud
        lon_actual = self.problema.intersecciones[estado.interseccion].longitud


        # Formula para el calculo de la distancia eucladiana
        distancia = math.dist([lat_actual, lon_actual],[self.lat_objetivo, self.lon_objetivo])
        return distancia
