from abc import ABC, abstractmethod
from collections import deque
import copy
import random
from Clases import *
import time
from queue import PriorityQueue
from copy import copy
from functools import lru_cache

class Busqueda(ABC):
    def __init__(self, problema):
        #Datos que necesitamos para el problems
        self.problema = problema
        self.nodos_cerrados = set()
        self.frontera = None

        #Datos para las estadisticas
        self.tiempo_ejecucion = 0
        self.coste_sol = 0
        self.hay_sol = False
    
    
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

        for accion in acciones:
            accion_sucesor = nodo.estado.aplicarAccion(accion)
            nuevo_nodo = Nodo(
                self.problema.intersecciones[accion_sucesor],
                padre=nodo,
                coste=nodo.coste + accion.coste,
                profundidad=nodo.profundidad + 1,
                generado=nodo.generado + 1
            )
            self.insertarNodo(nuevo_nodo, self.frontera)
    
    @lru_cache(maxsize=4096)
    def busqueda(self):
        inicio = time.perf_counter()
        e_inicial = Nodo(self.inicio)
        self.insertarNodo(e_inicial, self.frontera)

        while not self.esVacio(self.frontera):
            nodo = self.extraerNodo(self.frontera)
            if nodo.estado.interseccion not in self.nodos_cerrados:
                if nodo.estado.interseccion == self.final.interseccion:
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

class Busqueda_Aleatoria():
    def __init__(self,problema, generaciones = 1):
        self.problema = problema
        self.listaCandidatos = self.problema.candidatos
        self.soluciones = []
        self.candidatos = []

        for candi in self.listaCandidatos:
            self.soluciones.append(0) #Hacemos el bitmap para saber cual sera la lista

        for i in range(generaciones):
            tempo = random.sample(list(self.listaCandidatos), self.problema.estaciones)
            for j in range(len(tempo)):
                self.soluciones[self.listaCandidatos.index(tempo[j])] = 1
            self.candidatos.append(tempo)
        self.tiempo_ej = 0

    def evaluaSolucion(self, solucion):
        tiempo = time.perf_counter()
        costeSol = 0
        for candidato in solucion:
            costeInd = 0
            poblacionCandidato = candidato[1]
            for inter in self.problema.intersecciones:
                inicial = self.problema.intersecciones[inter]
                final = self.problema.intersecciones[candidato[0]]
                coste = self.aEstrellita(self.problema, inicial, final)
                costeInd += coste *poblacionCandidato #el coste de cada individuo tiene que estar relacionado con la poblacion del mismo
            costeSol += 1 / costeInd #nos interesa saber cual sera el mas bajo
            

        tiempoej = time.perf_counter() - tiempo

        return costeSol

    def busqueda(self):
        tiempo = time.perf_counter()
        soluciones = PriorityQueue()

        for solucion in self.candidatos:
            coste_sol = self.evaluaSolucion(solucion)
            #tenemos el coste de la solucion, ahora la metemos en una lista ordenada 
            soluciones.put((coste_sol, solucion))

        self.tiempo_ej = time.perf_counter() - tiempo
        print(Busqueda.formatoTiempo(self, self.tiempo_ej))

        #return del primero y del ultimo
        return soluciones.get()[1]
    
    @lru_cache(maxsize=4096)
    def aEstrellita(self, problema, inicial, final):
        return Busqueda_a_estrella(problema, inicial, final).busqueda()

class Busqueda_Genetica():
    def __init__(self, problema, individuos, generaciones, tamanoTorneo = 2, elitismo = 1):
        self.problema = problema #Problema a resolver

        self.individuos = individuos #Numero de individuos en la poblacion, un individuo estara formado por n intersecciones candidatas (n siendo numero de estaciones)
        self.poblacion = [] #Una poblacion formada por n individuos (soluciones que vamos a evaluar)
        self.generaciones = generaciones #Numero de generaciones que vamos a hacer (condicion de parada)

        #self.tamIndi = self.problema.estaciones #Tamaño de cada individuo (numero de estaciones)
        self.tamTorneo = tamanoTorneo #Tamaño del torneo
        self.elitismo = elitismo  # Número de individuos a preservar mediante elitismo
        self.mejorIndividuo = None

    @lru_cache(maxsize=139487)
    def aestrellita(self, problema, inicial, final):
        return Busqueda_a_estrella(problema, inicial, final).busqueda()
    

    def inicializacion(self):
        # Para la inicializacion cogeremos n individuos de tamIndi
        for _ in range(self.individuos):  # Cambiado i por _ ya que no se usa el índice
            # Creamos un individuo
            individuo = random.sample(list(self.problema.candidatos), self.problema.estaciones) # Cogemos tantos candidatos como estaciones haya
            self.poblacion.append([individuo, 0])  # Usar una lista en lugar de una tupla
        
        self.evaluacion()
            

    def evaluacion(self):
        #Evaluamos cada individuo de la poblacion
        for individuo in self.poblacion:
            #evaluamos cada interseccion candidata del individuo
            for candidato in individuo[0]:
                #cada candidato se evalua con a* de todos los puntos a el
                costeIndv = 0
                poblacionCandidato = candidato[1]
                for inter in self.problema.intersecciones:
                    inicial = self.problema.intersecciones[inter]
                    final = self.problema.intersecciones[candidato[0]]
                    coste = self.aestrellita(self.problema, inicial, final)
                    costeIndv += coste * poblacionCandidato
            
            individuo[1] += 1/costeIndv # Esto es el fitness creo (1/costeIndv) 

            self.mejorIndividuo = max(self.poblacion, key=lambda x: x[1])

    def seleccion(self):
        #Para la seleccion de individuos que resultaran en la proxima generacion
        #Vamos a usar el metodo de torneo
        nueva_poblacion = []
        for i in range(self.individuos):
            luchadores = random.sample(self.poblacion, self.tamTorneo) #jaja, luchadores, es un torneo
            luchadores.sort(key=lambda x: x[1])
            nueva_poblacion.append(luchadores[0])
        self.poblacion = nueva_poblacion
    
    def cruce(self):
        # Para el cruce, vamos a usar el cruce de un punto
        # con una probabilidad de cruce del 80%
        nueva_poblacion = []
        for i in range(0, self.individuos, 2):  # Iterar sobre parejas gays de padres
            padre1 = self.poblacion[i][0]
            padre2 = self.poblacion[i+1][0]
            if random.random() < 0.8:  # Aplicar cruce con probabilidad del 80%
                punto_cruce = random.randint(1, self.problema.estaciones - 1)  # Elegir punto de cruce aka punto donde empieza uno y acaba otro
                hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
                hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
                nueva_poblacion.append([hijo1, 0])
                nueva_poblacion.append([hijo2, 0])
            else:  # No aplicar cruce, copiar los padres
                nueva_poblacion.append([padre1, 0])
                nueva_poblacion.append([padre2, 0])
        self.poblacion = nueva_poblacion  # Actualizar la población

    def mutacion(self):
        # Para la mutación, vamos a cambiar una intersección aleatoria de cada individuo
        # con una probabilidad de mutación del 1%
        for individuo in self.poblacion:
            for i in range(self.problema.estaciones):
                if random.random() < 0.01:  # Aplicar mutación con probabilidad del 1%
                    # Obtener una nueva intersección aleatoria que no esté ya en el individuo
                    nueva_interseccion = random.choice(list(set(self.problema.candidatos) - set(individuo[0])))  #gracias a mi compa (asiq ni idea si esta bien)
                    individuo[0][i] = nueva_interseccion  # Reemplazar la intersección

    def reemplazo(self):
        """
        Reemplazo con elitismo: Los mejores individuos se preservan automáticamente,
        el resto de la población se sustituye con nuevos individuos generados.
        """
        # Seleccionamos los mejores individuos (según el atributo de aptitud)
        elite = sorted(self.poblacion, key=lambda x: x[1], reverse=True)[:self.elitismo]
        
        # Actualizamos la población actual manteniendo los mejores
        self.poblacion = elite + self.poblacion[:self.individuos - self.elitismo]

    def busqueda(self):
        tiempo = time.perf_counter()
        # Primero inicializamos la población
        mejores = []
        self.inicializacion()
        for i in range(self.generaciones):  # Iterar sobre las generaciones

            #print(f"Generacion {i+1}")
            tiempogen = time.perf_counter() - tiempo
            #print(Busqueda.formatoTiempo(self, tiempogen))
            #imprimimos el mejor de la generacion con su coste
            mejor_solucion = max(self.poblacion, key=lambda x: x[1])
            mejores.append(mejor_solucion[1])
            #print(f"Mejor solucion: {mejor_solucion[1]}")

            self.seleccion()
            self.cruce()
            self.mutacion()
            self.evaluacion()
            self.reemplazo()  # Reemplazo con elitismo
            # No es necesario llamar a reemplazo() ya que se hace en la selección

        # Obtener la mejor solución de la población final
        tiempo_ej = time.perf_counter() - tiempo
        print(Busqueda.formatoTiempo(self, tiempo_ej))
        mejor_solucion = max(self.poblacion, key=lambda x: x[1])
        print(f"Mejor solucion: {mejor_solucion[1]}")
        return mejores # Devolver solo la lista de intersecci