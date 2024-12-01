from functools import lru_cache
import json
import math
from geopy.distance import geodesic
from queue import PriorityQueue


class Accion:

    def __init__(self, origen, destino, coste):
        self.origen = origen
        self.destino = destino
        self.coste = coste #Este coste viene en tiempo   

    def __lt__(self, other):
        return self.destino < other.destino
    
class Estado:

    def __init__(self, interseccion, latitud, longitud):
        self.interseccion = interseccion
        self.latitud = latitud
        self.longitud = longitud

    
    def __lt__(self, other):
        return self.interseccion < other.interseccion
    
    def aplicarAccion(self, accion):
        if self.interseccion == accion.origen:
            return accion.destino
        raise Exception("No se puede aplicar la acción")

class Nodo:
    def __init__(self, estado, padre=None, coste = 0, profundidad = 0, generado = 1):
        self.estado = estado
        self.padre = padre
        self.coste = coste
        self.profundidad = profundidad
        self.generado = generado

    def getSolucion(self):
        solucion = []
        nodo = self
        while nodo.padre is not None:
            solucion.insert(0, nodo.estado.interseccion)
            nodo = nodo.padre
        solucion.insert(0, nodo.estado.interseccion)
        return solucion
    
    def __lt__(self, other):
        return self.estado < other.estado

class Problema:
    def __init__(self, ruta):
        #abrimos el archivo y lo guardamos
        with open(ruta, 'r') as archivo:
            self.datos_json = json.load(archivo)

        self.distancia = self.datos_json["distance"]
        self.estaciones = self.datos_json["number_stations"]
        self.veloMax = 0

        self.intersecciones = {}
        self.acciones = {}  # Diccionario de acciones
        self.candidatos = []

        for dato in self.datos_json["intersections"]:
            estado = Estado(dato["identifier"], dato["latitude"],
                            dato["longitude"])
            self.intersecciones[dato["identifier"]] = estado
            self.acciones[dato["identifier"]] = []  # Inicializar como lista vacía

        for dato in self.datos_json["segments"]:
            accion = Accion(dato["origin"], dato["destination"],
                            (dato["distance"] / (dato["speed"] * (10 / 36))))
            self.acciones[dato["origin"]].append(accion)  # Añadir acción a la lista
            if dato["speed"] > self.veloMax:
                self.veloMax = dato["speed"]

        for dato in self.datos_json["candidates"]:
            self.candidatos.append((dato[0], dato[1]))

        self.veloMax = self.veloMax * (10 / 36)
        self.ordenarAcciones()  # Ordenar las acciones al crear el objeto

    def ordenarAcciones(self):
        for key in self.acciones:
            self.acciones[key].sort(key=lambda accion: accion.destino)

    @lru_cache(maxsize=4096)
    def getAcciones(self, estado):
        return self.acciones[estado.interseccion]

