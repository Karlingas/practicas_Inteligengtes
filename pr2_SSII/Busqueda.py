from abc import ABC, abstractmethod
from collections import deque
import copy
import random
from Clases import *
import time
from queue import PriorityQueue

class Busqueda(ABC):
    def __init__(self, problema):
        #Datos que necesitamos para el problems
        self.problema = problema
        self.nodos_cerrados = set()
        self.frontera = None
        self.inicio = None #esto es un identificador
        self.final = None #y esto mas de lo mismo

        #Datos para las estadisticas
        self.tiempo_ejecucion = 0
        #self.nodos_generados = 0
        #self.nodos_expandidos = 0
        #self.profundidad_sol = 0
        self.coste_sol = 0
        self.hay_sol = False
        #self.solucion = []
    
    
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

    #def formatoSolucion(self, solucion):
        return [f"( {solucion[i]} -> {solucion[i + 1]} )" for i in range(len(solucion) - 1)]

    #def imprimirEstadisticas(self):
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
        acciones = self.problema.getAcciones(nodo.estado) 

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
            self.insertarNodo(nuevo_nodo, self.frontera)
    
    
    def busqueda(self):
        inicio = time.perf_counter()
        e_inicial = Nodo(self.inicio)
        self.insertarNodo(e_inicial, self.frontera)

        while not self.esVacio(self.frontera):
            nodo = self.extraerNodo(self.frontera)
            if nodo.estado.interseccion not in self.nodos_cerrados:
                if nodo.estado.interseccion == self.final:
                    self.tiempo_ejecucion = time.perf_counter() - inicio
                    self.hay_sol = True
                    return nodo.coste
                
                self.nodos_cerrados.add(nodo.estado.interseccion)
                self.expandir(nodo)


        return 696969696969     #Por si no hay solucion un numero grande para el coste (mas d 2 cm)

class Busqueda_a_estrella(Busqueda):
    def __init__(self, problema, inicial, final):
        super().__init__(problema)
        self.frontera = PriorityQueue()
        self.heuristica = Heuristica_Geodesica(problema)
        self.inicio = inicial
        self.final = final

    def insertarNodo(self, nodo, frontera):
        final = self.heuristica.getHeuristica(nodo.estado) / self.problema.veloMax
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
    @abstractmethod
    def getHeuristica(self, estado):
        pass

class Heuristica_Geodesica(Heuristica):
    def __init__(self, problema):
        super().__init__(problema)

    def getHeuristica(self, estado):
        # Obtener la intersección actual del estado
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = self.problema.intersecciones[estado.interseccion].latitud
        lon_actual = self.problema.intersecciones[estado.interseccion].longitud

        #Formula para el calculo de la distancia geodesica
        distancia = geodesic((lat_actual, lon_actual), (self.lat_objetivo, self.lon_objetivo)).meters

        return distancia

    def __init__(self, problema):
        super().__init__(problema)

    def getHeuristica(self, estado):
        # Obtener la intersección actual del estado
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = self.problema.intersecciones[estado.interseccion].latitud
        lon_actual = self.problema.intersecciones[estado.interseccion].longitud


        # Formula para el calculo de la distancia eucladiana
        distancia = math.dist([lat_actual, lon_actual],[self.lat_objetivo, self.lon_objetivo])
        return distancia



class Busqueda_Aleatoria():
    def __init__(self,problema, generaciones = 1):
        self.problema = problema
        self.listaCandidatos = self.problema.candidatos
        self.soluciones = []

        self.candidatos = []

        for candi in self.listaCandidatos:
            self.soluciones.append(0)

        for i in range(generaciones):
            tempo = random.sample(list(self.listaCandidatos), self.problema.estaciones)
            print(tempo)
            for j in range(len(tempo)):
                self.soluciones[self.listaCandidatos.index(tempo[j])] = 1
            self.candidatos.append(tempo)


        self.tiempo_ej = 0

    def evaluaSolucion(self, solucion):
        """
        Evalúa la solución S usando la fórmula especificada:
        value(S) = (1 / sum(C[i].pop)) * min_j(sum(C[i].pop * time(C[i].id, S[j])))
        """
        total_poblacion = sum([self.problema.datos_json["intersections"][i]["population"] 
                               for i in range(len(self.problema.datos_json["intersections"]))])
        
        min_costo = float("inf")
        for s in solucion:
            costo_total = 0
            for c in self.problema.datos_json["intersections"]:
                poblacion = c["population"]
                id_ciudad = c["identifier"]
                
                # Ejecutar A* para calcular el tiempo entre C[i].id y S[j]
                busqueda_astar = Busqueda_a_estrella(self.problema, id_ciudad, s)
                tiempo = busqueda_astar.busqueda()
                
                costo_total += poblacion * tiempo
            
            min_costo = min(min_costo, costo_total)

        value_s = (1 / total_poblacion) * min_costo
        return value_s

    def busqueda(self):
        for i in range(len(self.candidatos)):
            print("Candidato", self.candidatos[i])
        print("Coste :", self.evaluaSolucion(self.candidatos[i]))
