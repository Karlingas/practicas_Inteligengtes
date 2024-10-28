#Hay 4 clases, Accion Estado Nodo y Problema
import json
import math
from geopy.distance import geodesic


class Accion:
    __slots__ = ['origen', 'destino', 'coste']

    def __init__(self, origen, destino, coste):
        self.origen = origen
        self.destino = destino
        self.coste = coste #Este coste viene en tiempo   

class Estado:
    __slots__ = ['interseccion']

    def __init__(self, interseccion):
        self.interseccion = interseccion

    def __eq__(self, other):
        return self.interseccion == other.interseccion
    
    def aplicarAccion(self, accion):
        if self.interseccion == accion.origen:
            return Estado(accion.destino)
        raise Exception("No se puede aplicar la acción")

class Nodo:
    __slots__ = ['estado', 'padre', 'coste', 'profundidad', 'accion', 'heuristica']

    def __init__(self, estado, padre=None, coste=0, profundidad=0):
        if isinstance(estado, Estado):
            self.estado = estado
        else:
            self.estado = Estado(estado)
        self.padre = padre
        self.coste = coste
        self.profundidad = profundidad
        self.accion = []
        self.heuristica = 0

    def getSolucion(self):
        solucion = []
        nodo = self
        while nodo.padre is not None:
            solucion.insert(0, nodo.estado.interseccion)
            nodo = nodo.padre
        solucion.insert(0, nodo.estado.interseccion)
        return solucion
    
    def __lt__(self, other):
        return self.heuristica < other.heuristica

class Problema:
    def __init__(self, ruta):
        #abrimos el archivo y lo guardamos
        with open(ruta, 'r') as archivo:
            self.datos_json = json.load(archivo)

        self.distancia = self.datos_json["distance"]
        self.interseccion = self.datos_json["intersections"]
        self.estado_inicial = self.datos_json["initial"]
        self.estado_objetivo = self.datos_json["final"]
        self.segmentos = self.datos_json["segments"]
        self.veloMax = 0
        for seg in self.segmentos:
            if seg["speed"] > self.veloMax :
                self.veloMax = seg["speed"]
        
        self.veloMax = self.veloMax * (10/36)
    
    def getAcciones(self, estado):
        acciones = []
        for segmento in self.segmentos:
            if segmento["origin"] == estado.interseccion:
                acciones.append(Accion(segmento["origin"], segmento["destination"], (segmento["distance"]/(segmento["speed"]*(10/36)))))
        return acciones
    
    def esObjetivo(self, estado):
        return estado.interseccion == self.estado_objetivo
    
    # Obtener la distancia entre el estado actual y el estado final en el problema
    def getDistanciaFinal(self, estado):
        # Obtener la intersección actual del estado
        interseccion_actual = None
        for interseccion in self.interseccion:
            if interseccion["identifier"] == estado.interseccion:
                interseccion_actual = interseccion
                break
        # Obtener el estado objetivo
        for interseccion in self.interseccion:
            if interseccion["identifier"] == self.estado_objetivo:
                interseccion_objetivo = interseccion
                break
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = interseccion_actual["latitude"]
        lon_actual = interseccion_actual["longitude"]
        lat_objetivo = interseccion_objetivo["latitude"]
        lon_objetivo = interseccion_objetivo["longitude"]

        # Fórmula de distancia euclidiana entre los puntos (lat, lon) del estado actual y el final
        
        #distancia = math.dist([lat_actual, lon_actual],[lat_objetivo, lon_objetivo])
        distancia = geodesic((lat_actual, lon_actual), (lat_objetivo, lon_objetivo)).kilometers * 1000

        return distancia

    # Obtener la distancia entre el estado actual y el estado inicial en el problema
    def getDistanciaInicial(self, estado):
        # Obtener la intersección actual del estado
        interseccion_actual = None
        for interseccion in self.interseccion:
            if interseccion["identifier"] == estado.interseccion:
                interseccion_actual = interseccion
                break

        # Obtener el estado objetivo
        for interseccion in self.interseccion:
            if interseccion["identifier"] == self.estado_inicial:
                interseccion_inicial = interseccion
                break
        
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = interseccion_actual["latitude"]
        lon_actual = interseccion_actual["longitude"]
        lat_objetivo = interseccion_inicial["latitude"]
        lon_objetivo = interseccion_inicial["longitude"]

        # Formula para el calculo de la distancia geodesica
        distancia = math.dist([lat_actual, lon_actual],[lat_objetivo, lon_objetivo])
        return distancia
