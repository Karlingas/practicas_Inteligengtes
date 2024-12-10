import math
from queue import PriorityQueue
import random
import time

from Busqueda import Busqueda_a_estrella, Busqueda

class BusquedaGenetica():
    def __init__(self, problema, tamanoPoblacion, generaciones, tamanoTorneo = 5, elitismo = 5):
        self.problema = problema

        self.tamanoPoblacion = tamanoPoblacion
        self.generaciones = generaciones
        self.tamanoTorneo = tamanoTorneo

        self.poblacion = [None] * tamanoPoblacion
        self.mejorIndividuo = math.inf
        self.cacheCoste = {}

    def buscar(self):
        tiempoej = time.perf_counter()
        tiempoEvaluacion = 0
        tiempoSeleccion = 0
        tiempoCruce = 0
        tiempoMutacion = 0

        # Primero inicializamos la población
        mejores = []
        self.inicializacion()

        tiemposs = time.perf_counter()- tiempoej
        for i in range(self.generaciones):  # Iterar sobre las generaciones            
            #print(f"Generacion {i+1}")
            #Guardamos la mejor solucion de cada generacion, es decir de todos los individuos el fitness
            #print(self.mejorIndividuo)
            mejores.append(self.mejorIndividuo)
            #seleccion de los individuos que pasaran a formar parte de la siguiente generacion
            tiempo = time.perf_counter()
            padres = self.seleccionTorneo()
            tiempoSeleccion += time.perf_counter() - tiempo


            for individuo in range(len(padres)-1):
                padre1 = padres[individuo]
                padre2 = padres[individuo+1]
                
                tiempo = time.perf_counter()
                hijo = self.cruce(padre1, padre2)        
                tiempoCruce += time.perf_counter() - tiempo

                tiempo = time.perf_counter()
                hijo = self.mutacion(hijo)
                tiempoMutacion += time.perf_counter() - tiempo

                tiempo = time.perf_counter()
                hijo[1] = self.evaluaIndividuo(hijo[0])
                tiempoEvaluacion += time.perf_counter() - tiempo

                if self.poblacion[individuo][1] == self.mejorIndividuo and hijo[1] < self.mejorIndividuo:
                    self.mejorIndividuo = hijo[1]
                    self.poblacion[individuo] = hijo
                else :
                    self.poblacion[individuo] = hijo


        def imprimir():# Obtener la mejor solución de la población final
            tiempo_ej = time.perf_counter() - tiempoej
            print("TOTAL: ")
            print(Busqueda.formatoTiempo(self, tiempo_ej))
            mejor_solucion = min(mejores, key=lambda x: x)
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

        imprimir()

        return mejores 
         
    def inicializacion(self):
        for i in range(self.tamanoPoblacion):
            individuo = random.sample(list(self.problema.candidatos), self.problema.estaciones)
            self.poblacion[i] = [individuo, self.evaluaIndividuo(individuo)]
            if self.poblacion[i][1] < self.mejorIndividuo:
                self.mejorIndividuo = self.poblacion[i][1]
    
    def evaluaIndividuo(self, individuo):
        pobTotal = 0
        valor = 0
        for candidata in range(len(self.problema.candidatos)):
            minimo = math.inf
            pobCandi = self.problema.candidatos[candidata][1]
            pobTotal += pobCandi

            inicio = self.problema.intersecciones[self.problema.candidatos[candidata][0]]
            for seleccionada in range(len(individuo)):
                if (self.problema.candidatos[candidata][0], individuo[seleccionada][0]) in self.cacheCoste:
                    coste = self.cacheCoste[self.problema.candidatos[candidata][0], individuo[seleccionada][0]]
                    if coste < minimo and coste != 0: #si no pones la comprobacion, encontes no tiene sentido ya que simpre sera el minimo aquel que sea de uno a el mismo
                        minimo = coste
                else:
                    final = self.problema.intersecciones[individuo[seleccionada][0]]
                    coste =  Busqueda_a_estrella(self.problema, inicio, final).busqueda(self.cacheCoste)
                    self.cacheCoste[self.problema.candidatos[candidata][0], individuo[seleccionada][0]] = coste 
                    if coste < minimo and coste != 0:
                        minimo = coste
                    
                
            valor += minimo * pobCandi
        

        return valor / pobTotal
    
    def seleccionTorneo(self):
        resultado = [None] * self.tamanoPoblacion
        for i in range(self.tamanoPoblacion):
            gladiadores = random.sample(self.poblacion, self.tamanoTorneo)
            resultado[i] = min(gladiadores, key=lambda x: x[1])
        
        return resultado

    def cruce(self, padre1, padre2):
        if padre1[1] < padre2[1]:
            primero = True
        else: 
            primero = False

        if random.random() < 0.8:
            puntoCruce = random.randint(1, self.problema.estaciones-1)
            if primero:
                hijo = [padre1[0][:puntoCruce]+ padre2[0][puntoCruce:], 0]
            else:
                hijo = [padre2[0][:puntoCruce]+ padre1[0][puntoCruce:], 0]
        else : #Si no ocurre la probabilidad de cruce, devolvemos el padre con mejor fitness
            if primero:
                hijo = padre1
            else:
                hijo = padre2
        
        return hijo

    def mutacion(self, hijo):
        if random.random() < 0.1:
            puntoMutacion = random.randint(0, self.problema.estaciones-1)
            hijo[0][puntoMutacion] = random.choice(list(set(self.problema.candidatos) - set(hijo[0])))

        return hijo

class BusquedaAleatoria():
    def __init__(self,problema, tamanoPoblacion):
        self.problema = problema

        self.tamanoPoblacion = tamanoPoblacion

        self.poblacion = [None] * tamanoPoblacion
        self.mejorIndividuo = math.inf
        self.cacheCoste = {}

    
    def buscar(self):
        # Primero inicializamos la población
        self.inicializacion()

        mejor_solucion = min(self.poblacion, key=lambda x: x[1])
        print(f"Mejor solucion: {mejor_solucion}")

    def inicializacion(self):
        for i in range(self.tamanoPoblacion):
            individuo = random.sample(list(self.problema.candidatos), self.problema.estaciones)
            self.poblacion[i] = [individuo, self.evaluaIndividuo(individuo)]
            if self.poblacion[i][1] < self.mejorIndividuo:
                self.mejorIndividuo = self.poblacion[i][1]
    
    def evaluaIndividuo(self, individuo):
        pobTotal = 0
        valor = 0
        for candidata in range(len(self.problema.candidatos)):
            minimo = math.inf
            pobCandi = self.problema.candidatos[candidata][1]
            pobTotal += pobCandi

            inicio = self.problema.intersecciones[self.problema.candidatos[candidata][0]]
            for seleccionada in range(len(individuo)):
                if (self.problema.candidatos[candidata][0], individuo[seleccionada][0]) in self.cacheCoste:
                    coste = self.cacheCoste[self.problema.candidatos[candidata][0], individuo[seleccionada][0]]
                    if coste < minimo and coste != 0: #si no pones la comprobacion, encontes no tiene sentido ya que simpre sera el minimo aquel que sea de uno a el mismo
                        minimo = coste
                else:
                    final = self.problema.intersecciones[individuo[seleccionada][0]]
                    coste =  Busqueda_a_estrella(self.problema, inicio, final).busqueda(self.cacheCoste)
                    self.cacheCoste[self.problema.candidatos[candidata][0], individuo[seleccionada][0]] = coste 
                    if coste < minimo and coste != 0:
                        minimo = coste
                    
                
            valor += minimo * pobCandi
        

        return valor / pobTotal