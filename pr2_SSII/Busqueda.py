from abc import ABC, abstractmethod
from Clases import *
from queue import PriorityQueue

class Busqueda(ABC):
    def __init__(self, problema):
        #Datos que necesitamos para el problems
        self.problema = problema
        self.nodos_cerrados = set()
        self.frontera = None

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

        for accion in range(len(acciones)):
            destino = nodo.estado.aplicarAccion(acciones[accion])
            if destino not in self.nodos_cerrados:
                nuevo_nodo = Nodo(
                    self.problema.intersecciones[destino],
                    padre=nodo,
                    coste=nodo.coste + acciones[accion].coste,
                    profundidad=nodo.profundidad + 1,
                    generado=nodo.generado + 1
                )
                self.insertarNodo(nuevo_nodo, self.frontera)
    
    def busqueda(self,cacheGlobalCandidatosCaminos):
        e_inicial = Nodo(self.inicio)
        self.insertarNodo(e_inicial, self.frontera)

        while not self.esVacio(self.frontera):
            nodo = self.extraerNodo(self.frontera)
            if nodo.estado.interseccion not in self.nodos_cerrados: #Sabemos que el nodo no ha sido explorado

                if ((nodo.estado.interseccion, self.final.interseccion) in cacheGlobalCandidatosCaminos): #Sabemos que el nodo ya ha sido calculado, return el resultado
                    return cacheGlobalCandidatosCaminos[nodo.estado.interseccion, self.final.interseccion]
                
                if (nodo.estado.interseccion in self.problema.candidatos) and nodo.estado.interseccion != self.inicio: #Sabemos que el nodo es un candidato, guardamos su coste
                    cacheGlobalCandidatosCaminos[self.inicio, nodo.estado.interseccion] = nodo.coste

                if nodo.estado.interseccion == self.final.interseccion:
                    return nodo.coste
                
                self.nodos_cerrados.add(nodo.estado.interseccion)
                self.expandir(nodo)


        return 9999     #Por si no hay solucion un numero grande para el coste (mas d 2 cm)

class Busqueda_a_estrella(Busqueda):
    
    def __init__(self, problema, inicial, final):
        super().__init__(problema)
        self.frontera = PriorityQueue()
        self.heuristica = Heuristica_Geodesica(problema, final)
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
    def __init__(self, problema, final):
        self.problema = problema
        #Obtenemos la lat y lon del estado objetivo
        self.lat_objetivo = self.problema.intersecciones[final.interseccion].latitud
        self.lon_objetivo = self.problema.intersecciones[final.interseccion].longitud
    @abstractmethod
    def getHeuristica(self, estado):
        pass

class Heuristica_Geodesica(Heuristica):
    def __init__(self, problema, final):
        super().__init__(problema, final)


    def getHeuristica(self, estado):
        # Obtener la intersección actual del estado
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = self.problema.intersecciones[estado.interseccion].latitud
        lon_actual = self.problema.intersecciones[estado.interseccion].longitud

        #Formula para el calculo de la distancia geodesica
        distancia = geodesic((lat_actual, lon_actual), (self.lat_objetivo, self.lon_objetivo)).meters

        return distancia
