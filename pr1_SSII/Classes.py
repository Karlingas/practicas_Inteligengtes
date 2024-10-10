import json

class Accion:
    def __init__(self, origen, destino, coste):
        self.origen = origen
        self.destino = destino
        self.coste = coste


class Estado:
    def __init__(self, interseccion):
        self.interseccion = interseccion
        


class Nodo:
    def __init__(self,  estado, padre=None, accion=None, coste=0, profundidad=0, id=1):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.coste = coste
        self.profundidad = profundidad
        self.id = id
    
    def hijo(self, accion):
        estado_resultante = accion  # Suponiendo que las acciones modifican el estado
        return Nodo(estado_resultante, self, accion, self.coste + 1, self.profundidad + 1)
    
    def solucion(self):
        # Reconstruir el camino de la solución desde el nodo inicial
        solucion = []
        nodo_actual = self
        while nodo_actual.padre is not None:
            solucion.append(nodo_actual.accion)
            nodo_actual = nodo_actual.padre
        solucion.reverse()  # Para tener la solución en orden desde el inicio hasta el final
        return solucion
    
    def getInterseccion(self):
        return self.estado.interseccion


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
        return estado == self.estado_objetivo
    
    def acciones(self, estado):
        # Aquí se deben devolver las acciones posibles desde el estado actual (las intersecciones conectadas)
        return [seg["destination"] for seg in self.segmentos if seg["origin"] == estado]
    
    def resultado(self, estado, accion):
        # El resultado de aplicar una acción es simplemente el destino (intersección) al que se va
        return accion
    
    def coste_individual(self, nodo, accion, s):
        # Calcular el coste de la acción
        for seg in self.segmentos:
            if seg["origin"] == nodo.estado and seg["destination"] == accion:
                return seg["distance"]
        return float('inf')  # Si no se encuentra el segmento

