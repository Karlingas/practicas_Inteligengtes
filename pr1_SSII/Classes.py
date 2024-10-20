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
        


class Nodo:
    def __init__(self, id=None, padre=None, coste=0, profundidad=0, problema=None):
        self.problema = problema
        self.estado = Estado(id)
        self.acciones = []
        self.padre = padre
        self.coste = coste
        self.profundidad = profundidad 
    
    #def hijo(self, accion):
        #estado_resultante = accion  # Suponiendo que las obten_acciones modifican el estado
        #return Nodo(estado_resultante, self, accion, self.coste + 1, self.profundidad + 1)
    

    def getSolucion(self):
        # Reconstruir el camino de la solución desde el nodo inicial
        solucion = []
        nodo_actual = self
        while nodo_actual.padre is not None:
            solucion.append(nodo_actual.estado.interseccion_id)
            nodo_actual = nodo_actual.padre
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

    # Obtener la velocidad entre el estado actual y el estado siguiente en el problema
    def getVelocidad(self):
        # Buscar el segmento correspondiente al estado actual y el destino siguiente
        for segmento in self.problema.segmentos:
            if segmento["origin"] == self.estado.interseccion_id:
                # Devolver la velocidad del segmento actual
                return segmento["speed"]
        
        # Si no se encuentra el segmento, devolvemos una velocidad de 0
        return 0
        
class Problema:
    def __init__(self, ruta_json):
        with open(ruta_json, 'r') as archivo:
            self.datos_json = json.load(archivo)

        self.distancia = self.datos_json["distance"]
        self.interseccion = self.datos_json["intersections"]
        self.estado_inicial = self.datos_json["initial"]
        self.estado_objetivo = self.datos_json["final"]
        self.segmentos = self.datos_json["segments"]
    

    def es_objetivo(self, estado):
        return estado.interseccion_id == self.estado_objetivo
    
    def obten_acciones(self, estado):
    # Aquí se devuelven objetos de la clase Accion, que contienen origen, destino y coste (distancia)
        return [Accion(origen=seg["origin"], destino=seg["destination"], coste=seg["distance"]) 
            for seg in self.segmentos if seg["origin"] == estado.interseccion_id]

    
    #def resultado(self, estado, accion):
        # El resultado de aplicar una acción es simplemente el destino (intersección) al que se va
        return accion
    

    #no hace falta coste individual si tenemos accion como una clase que contiene el coste de la accion
    #def coste_individual(self, nodo, accion, s):
        # Calcular el coste de la acción
        for seg in self.segmentos:
            if seg["origin"] == nodo.estado and seg["destination"] == accion:
                return seg["distance"]
        return float('inf')  # Si no se encuentra el segmento

