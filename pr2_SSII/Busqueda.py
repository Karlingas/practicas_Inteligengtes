from abc import ABC, abstractmethod
import os
import random
from Clases import *
import time
from queue import PriorityQueue
from multiprocessing import Manager, Process
import multiprocessing

cacheGlobalCandidatosCaminos = {}
cacheGlobalCandidatos = {}

cacheGlobalCandidatosCaminos[0] = 0
cacheGlobalCandidatos[0] = 0
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

def evaluacionIndividuo(cacheGlobalCandidatos, cacheGlobalCandidatosCaminos, problema, individuo, id, resultados):
        solucionMin = math.inf
        for candidato in range(len(individuo[0])):
            costeCand = 0

            if individuo[0][candidato][0] in cacheGlobalCandidatos:
                costeCand = cacheGlobalCandidatos[individuo[0][candidato][0]]
            else :    
                for i in range(len(problema.candidatos)):
                    inicial = problema.intersecciones[problema.candidatos[i][0]]
                    final = problema.intersecciones[individuo[0][candidato][0]]
                    costeCand += Busqueda_a_estrella( problema, inicial, final).busqueda(cacheGlobalCandidatosCaminos) * individuo[0][candidato][1]

                cacheGlobalCandidatos[individuo[0][candidato][0]] = costeCand

            if costeCand < solucionMin:
                solucionMin = costeCand 
        
        resultados[id] = solucionMin

class Busqueda_Genetica():
    def __init__(self, problema, individuos, generaciones, tamanoTorneo = 2, elitismo = 1):
        self.problema = problema #Problema a resolver

        if individuos%2 == 0:
            self.individuos = individuos #Numero de individuos en la poblacion, un individuo estara formado por n intersecciones candidatas (n siendo numero de estaciones)
        else :
            self.individuos = individuos + 1
        self.generaciones = generaciones #Numero de generaciones que vamos a hacer (condicion de parada)
        self.poblacion = [None] * individuos #Una poblacion formada por n individuos (soluciones que vamos a evaluar)
        
        self.poblacionTotal = 0
        self.fitness = {}
        for i in range(len(self.problema.candidatos)):
            self.fitness[self.problema.candidatos[i][0]] = 0
            self.poblacionTotal += self.problema.candidatos[i][1]

      
            

        self.tamTorneo = tamanoTorneo #Tamaño del torneo
        self.elitismo = elitismo  # Número de individuos a preservar mediante elitismo

        self.mejorIndividuo = None
        self.futuraGen = []
        self.anteriorGen = []
  
    def inicializacion(self):
        # Para la inicializacion cogeremos n individuos de tamIndi
        for i in range(self.individuos):  # Cambiado i por _ ya que no se usa el índice
            # Creamos un individuo
            individuo = random.sample(list(self.problema.candidatos), self.problema.estaciones) # Cogemos tantos candidatos como estaciones haya
            self.poblacion[i] = [individuo, 0]
        
        self.evaluacionMultiProcess(self.poblacion)
            
    @lru_cache(maxsize=999999)
    def aEstrella(self, inicial, final):
        return Busqueda_a_estrella(self.problema, inicial, final).busqueda(cacheGlobalCandidatos)
    
    
    def evaluacionMultiProcess(self, poblacion):
        #Evaluamos cada individuo de la poblacion
        solucionMin = math.inf
        countProcesses = os.cpu_count() #Tiene que ser el numero de cores para que sea lo mas optimo
        procesos = [None] * countProcesses 
        resultados = multiprocessing.Array('d', len(poblacion))
        global cacheGlobalCandidatos, cacheGlobalCandidatosCaminos
        with Manager() as manager:
            cacheGlobalCandidatoss = manager.dict(cacheGlobalCandidatos)
            cacheGlobalCandidatosCaminoss = manager.dict(cacheGlobalCandidatosCaminos)
            
            for individuo in range(0, len(poblacion), countProcesses):
                for i in range(countProcesses):
                    if individuo + i < len(poblacion):
                        procesos[i] = Process(
                            target=evaluacionIndividuo,
                            args=(cacheGlobalCandidatoss, cacheGlobalCandidatosCaminoss, self.problema, poblacion[individuo + i], individuo + i, resultados)
                        )
                        procesos[i].start()

                for i in range(countProcesses):
                    if procesos[i]:
                        procesos[i].join()
        
            cacheGlobalCandidatos = dict(cacheGlobalCandidatoss)
            cacheGlobalCandidatosCaminos = dict(cacheGlobalCandidatosCaminoss)


        for individuo in range(len(poblacion)):
            poblacion[individuo][1] = resultados[individuo] / self.poblacionTotal

    
        self.mejorIndividuo = min(self.poblacion, key=lambda x: x[1]) #Problema de minimizacion

    def evaluacion(self, poblacion):
        #Evaluamos cada individuo de la poblacion
        solucionMin = math.inf
        for individuo in range(len(poblacion)):
            poblacion[individuo][1] = 0
            for candidato in range(len(poblacion[individuo][0])):
                costeCand = 0

                if poblacion[individuo][0][candidato][0] in cacheGlobalCandidatos:
                    costeCand = cacheGlobalCandidatos[poblacion[individuo][0][candidato][0]]
                else :    
                    for i in range(len(self.problema.candidatos)):
                        inicial = self.problema.intersecciones[self.problema.candidatos[i][0]]
                        final = self.problema.intersecciones[poblacion[individuo][0][candidato][0]]
                        costeCand += self.aEstrella(inicial, final) * poblacion[individuo][0][candidato][1]

                    cacheGlobalCandidatos[poblacion[individuo][0][candidato][0]] = costeCand

                if costeCand < solucionMin:
                    solucionMin = costeCand  
            
            poblacion[individuo][1] = 1 / solucionMin
    

        self.mejorIndividuo = min(self.poblacion, key=lambda x: x[1]) #Problema de minimizacion

    def seleccionTorneo(self):
        #Para la seleccion de individuos que resultaran en la proxima generacion
        nueva_poblacion = []
        for i in range(self.individuos):
            luchadores = random.sample(self.poblacion, self.tamTorneo) #jaja, luchadores, es un torneo
            nueva_poblacion.append(min(luchadores, key=lambda x: x[1])) 
        self.futuraGen = nueva_poblacion

    def seleccionProporcionalFitness(self):
        # Usamos selección proporcional al fitness (ruleta)
        nueva_poblacion = []
        
        # Sumar los fitness de todos los individuos
        total_fitness = sum(individuo[1] for individuo in self.poblacion)
        
        # Normalizar los fitness para evitar valores extremos
        if total_fitness == 0:
            raise ValueError("El fitness total es 0, lo que sugiere que todos los individuos tienen un fitness muy bajo.")
        
        for _ in range(self.individuos):
            # Generar un número aleatorio en el rango del fitness acumulado
            punto_ruleta = random.uniform(0, total_fitness)
            suma_acumulada = 0
            
            # Selección del individuo basado en el fitness acumulado
            for individuo in self.poblacion:
                suma_acumulada += individuo[1]
                if suma_acumulada >= punto_ruleta:
                    nueva_poblacion.append(individuo)
                    break
        
        self.futuraGen = nueva_poblacion

    def seleccionRango(self):
        # Ordenar la población por fitness en orden descendente
        # (mejor individuo primero)
        self.poblacion.sort(key=lambda x: x[1])
        
        # Asignar pesos en función del rango
        num_individuos = len(self.poblacion)
        pesos = [num_individuos - i for i in range(num_individuos)]  # Peso más alto para el mejor individuo
        
        # Calcular el total de los pesos para normalización
        total_pesos = sum(pesos)
        
        nueva_poblacion = []
        for _ in range(self.individuos):
            # Generar un número aleatorio en el rango de los pesos totales
            punto_ruleta = random.uniform(0, total_pesos)
            suma_acumulada = 0
            
            # Seleccionar individuo basado en la acumulación de pesos
            for i, individuo in enumerate(self.poblacion):
                suma_acumulada += pesos[i]
                if suma_acumulada >= punto_ruleta:
                    nueva_poblacion.append(individuo)
                    break
        
        self.futuraGen = nueva_poblacion

    def seleccionElitistaTorneo(self):
        # Primero, seleccionamos los mejores individuos mediante torneo
        elite = sorted(self.poblacion, key=lambda x: x[1], reverse=True)[:self.elitismo]

        # Luego, aplicamos el método de torneo para seleccionar el resto de la población
        restante = []
        for _ in range(self.individuos - self.elitismo):
            luchadores = random.sample(self.poblacion, self.tamTorneo)
            restante.append(min(luchadores, key=lambda x: x[1]))

        # Combinamos la elite con el resto de la población
        self.futuraGen = elite + restante

    def cruce(self):
        # Para el cruce, vamos a usar el cruce de un punto
        # con una probabilidad de cruce del 80%
        nueva_poblacion = []
        for i in range(0, self.individuos, 2):  # Iterar sobre parejas gays de padres
            padre1 = self.futuraGen[i][0]
            padre2 = self.futuraGen[i+1][0]
            if random.random() < 0.7:  # Aplicar cruce con probabilidad del 80%
                punto_cruce = random.randint(1, self.problema.estaciones - 1)  # Elegir punto de cruce aka punto donde empieza uno y acaba otro
                hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
                hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
                nueva_poblacion.append([hijo1, 0])
                nueva_poblacion.append([hijo2, 0])
            else:  # No aplicar cruce, copiar los padres
                nueva_poblacion.append([padre1, 0])
                nueva_poblacion.append([padre2, 0])
        
        self.futuraGen = nueva_poblacion  # Actualizar la población

    def mutacion(self):
        # Para la mutación, vamos a cambiar una intersección aleatoria de cada individuo
        # con una probabilidad de mutación del 1%
        for individuo in self.futuraGen:
            for i in range(self.problema.estaciones):
                if random.random() < 0.01:  # Aplicar mutación con probabilidad del 1%
                    # Obtener una nueva intersección aleatoria que no esté ya en el individuo
                    nueva_interseccion = random.choice(list(set(self.problema.candidatos) - set(individuo[0])))  #gracias a mi compa (asiq ni idea si esta bien)
                    individuo[0][i] = nueva_interseccion  # Reemplazar la intersección

    def reemplazo(self):
        # Seleccionamos los mejores individuos (según el atributo de aptitud)
        #elite = sorted(self.poblacion, key=lambda x: x[1])[:self.elitismo]
        
        # Actualizamos la población actual manteniendo los mejores
        #self.poblacion = elite + self.futuraGen[:self.individuos - self.elitismo]
        self.poblacion = self.futuraGen

    def busqueda(self):
        tiempoej = time.perf_counter()
        tiempoEvaluacion = 0
        tiempoSeleccion = 0
        tiempoCruce = 0
        tiempoMutacion = 0
        tiempoReemplazo = 0
        # Primero inicializamos la población
        mejores = []
        self.inicializacion()
        
        tiemposs = time.perf_counter()- tiempoej
        for i in range(self.generaciones):  # Iterar sobre las generaciones            
            #print(f"Generacion {i+1}")
            mejor_solucion = min(self.poblacion, key=lambda x: x[1])
            mejores.append(mejor_solucion[1])

            tiempo = time.perf_counter()
            self.seleccionRango()
            tiempoSeleccion += time.perf_counter() - tiempo

            tiempo = time.perf_counter()
            self.cruce()
            tiempoCruce += time.perf_counter() - tiempo

            tiempo = time.perf_counter()
            self.mutacion()
            tiempoMutacion += time.perf_counter() - tiempo

            tiempo = time.perf_counter()
            self.evaluacion(self.futuraGen)
            tiempoEvaluacion += time.perf_counter() - tiempo

            tiempo = time.perf_counter()
            self.reemplazo()  # Reemplazo con elitismo
            tiempoReemplazo += time.perf_counter() - tiempo

        # Obtener la mejor solución de la población final
        tiempo_ej = time.perf_counter() - tiempoej
        print("TOTAL: ")
        print(Busqueda.formatoTiempo(self, tiempo_ej))
        mejores.sort(key=lambda x: x)
        mejor_solucion = mejores[0]
        print(f"Mejor solucion: {mejor_solucion}")
        #Regla de 3 para conocer los %, si tiempo_ej es 100% calcular cuanto es cada cosa
        print("Porcentajes: ")
        inicializacion = tiemposs * 100 / tiempo_ej
        print(f"Inicializacion: {inicializacion}%")
        seleccion = tiempoSeleccion * 100 / tiempo_ej
        print(f"Seleccion: {seleccion}%")
        cruce = tiempoCruce * 100 / tiempo_ej
        print(f"Cruce: {cruce}%")
        mutacion = tiempoMutacion * 100 / tiempo_ej
        print(f"Mutacion: {mutacion}%")
        evaluacion = tiempoEvaluacion * 100 / tiempo_ej
        print(f"Evaluacion: {evaluacion}%")
        reemplazo = tiempoReemplazo * 100 / tiempo_ej
        print(f"Reemplazo: {reemplazo}%")

        return mejores 