import json
import math

class Accion:
    def __init__(self, origen, destino, coste):
        self.origen = origen
        self.destino = destino
        self.coste = coste 


class Estado:
    def __init__(self, interseccion):
        self.interseccion_id = interseccion

    def aplicar_accion(self, accion):
        if self.interseccion_id == accion.origen:
            return Estado(accion.destino)
        return False #no se puede hacer la accion 
        


class Nodo:
    def __init__(self, estado=None, padre=None, coste=0, profundidad=0, problema=None):
        self.problema = problema
        if isinstance(estado, Estado):
            self.estado = estado
        else :
            self.estado = Estado(estado)
        self.acciones = []
        self.padre = padre
        self.coste = coste
        self.profundidad = profundidad 
        self.heuristica = 0 

    def __lt__(self, other):
        return self.heuristica < other.heuristica   

    def getSolucion(self):
        # Reconstruir el camino de la solución desde el nodo inicial
        solucion = []
        nodo_actual = self
        while nodo_actual.padre is not None:
            solucion.append(nodo_actual.estado.interseccion_id)
            nodo_actual = nodo_actual.padre
        solucion.append(nodo_actual.estado.interseccion_id)
        solucion.reverse()  # Para tener la solución en orden desde el inicio hasta el final
        return solucion
    
    def defineAcciones(self):
        self.acciones = self.problema.obten_acciones(self.estado)
        
    # Obtener la distancia entre el estado actual y el estado final en el problema
    def getDistanciaFinal(self):
        # Obtener la intersección actual del estado
        interseccion_actual = None
        for interseccion in self.problema.interseccion:
            if interseccion["identifier"] == self.estado.interseccion_id:
                interseccion_actual = interseccion
                break
        # Obtener el estado objetivo
        for interseccion in self.problema.interseccion:
            if interseccion["identifier"] == self.problema.estado_objetivo:
                interseccion_objetivo = interseccion
                break
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = interseccion_actual["latitude"]
        lon_actual = interseccion_actual["longitude"]
        lat_objetivo = interseccion_objetivo["latitude"]
        lon_objetivo = interseccion_objetivo["longitude"]

        # Fórmula de distancia euclidiana entre los puntos (lat, lon) del estado actual y el final
        distancia = math.sqrt((lat_actual - lat_objetivo) ** 2 + (lon_actual - lon_objetivo) ** 2)
        
        return distancia

    # Obtener la distancia entre el estado actual y el estado inicial en el problema
    def getDistanciaInicial(self):
        # Obtener la intersección actual del estado
        interseccion_actual = None
        for interseccion in self.problema.interseccion:
            if interseccion["identifier"] == self.estado.interseccion_id:
                interseccion_actual = interseccion
                break

        # Obtener el estado objetivo
        for interseccion in self.problema.interseccion:
            if interseccion["identifier"] == self.problema.estado_inicial:
                interseccion_inicial = interseccion
                break
        
        # Calcular la distancia entre el estado actual y el estado objetivo
        lat_actual = interseccion_actual["latitude"]
        lon_actual = interseccion_actual["longitude"]
        lat_objetivo = interseccion_inicial["latitude"]
        lon_objetivo = interseccion_inicial["longitude"]

        # Fórmula de distancia euclidiana entre los puntos (lat, lon) del estado actual y el inicial
        distancia = math.sqrt((lat_actual - lat_objetivo) ** 2 + (lon_actual - lon_objetivo) ** 2)
        return distancia
    
class Problema:
    def __init__(self, ruta_json):
        with open(ruta_json, 'r') as archivo:
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
        
    

    def es_objetivo(self, estado):
        return estado.interseccion_id == self.estado_objetivo
    
    def obten_acciones(self, estado):
    # Aquí se devuelven objetos de la clase Accion, que contienen origen, destino y coste (distancia)
        return [Accion(seg["origin"], seg["destination"], (seg["distance"]/(seg["speed"]*(10/36)))) 
            for seg in self.segmentos if seg["origin"] == estado.interseccion_id]