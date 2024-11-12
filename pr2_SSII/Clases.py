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

    def __eq__(self, other):
        return self.interseccion == other.interseccion
    
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
        return self.generado < other.generado

class Problema:
    def __init__(self, ruta):
        #abrimos el archivo y lo guardamos
        with open(ruta, 'r') as archivo:
            self.datos_json = json.load(archivo)

        self.distancia = self.datos_json["distance"]
        self.veloMax = 0

        self.intersecciones = {}
        self.acciones = {} #Diccionario de acciones
       # Combinar ambos bucles en uno
        for dato in self.datos_json["intersections"] + self.datos_json["segments"]:
            if "identifier" in dato:  # Procesar intersección
                estado = Estado(dato["identifier"], dato["latitude"], dato["longitude"])
                self.intersecciones[dato["identifier"]] = estado
                self.acciones[dato["identifier"]] = PriorityQueue()
            elif "origin" in dato:  # Procesar segmento
                accion = Accion(dato["origin"], dato["destination"], (dato["distance"]/(dato["speed"]*(10/36))))
                self.acciones[dato["origin"]].put((accion.destino, accion))
                if dato["speed"] > self.veloMax:
                    self.veloMax = dato["speed"]

        self.veloMax = self.veloMax * (10/36)

        self.estado_inicial = self.intersecciones[self.datos_json["initial"]]
        self.estado_objetivo = self.intersecciones[self.datos_json["final"]]
    

    def getAcciones(self, estado):
        return self.acciones[estado.interseccion]

    def esObjetivo(self, estado):
        return estado.interseccion == self.estado_objetivo.interseccion

class ProblemaGeneral:
    def _init(self,ruta):
        with open(ruta, 'r') as archivo:
            self.datos_json = json.load(archivo)

        self.distancia = self.datos_json["distance"]
        self.veloMax = 0

        self.intersecciones = {}
        self.acciones = {}
        for dato in self.datos_json["intersections"]:
            estado = Estado(dato["identifier"], dato["latitude"], dato["longitude"])
            self.intersecciones[dato["identifier"]] = estado
            self.acciones[dato["identifier"]] = PriorityQueue()

        for segmento in self.datos_json["segments"]:
            accion = Accion(segmento["origin"], segmento["destination"], (segmento["distance"]/(segmento["speed"]*(10/36))))
            self.acciones[segmento["origin"]].put((accion.destino, accion))
            if segmento["speed"] > self.veloMax :
                self.veloMax = segmento["speed"]

        self.veloMax = self.veloMax * (10/36)

        self.estado_inicial = self.intersecciones[self.datos_json["initial"]]
        self.estado_objetivo = self.intersecciones[self.datos_json["final"]]
    
    