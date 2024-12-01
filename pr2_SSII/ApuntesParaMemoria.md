-De la clase busqueda hemos cambiado:
    Hemos añadido un final y un inicial que se asignan en A*, (no sabemos si quitar el tiempo de ejecuccion) pero si hemos quitado las estadisticas. 
    En a* ahora se le pasa en el constructor un inicial y un final que son el identificador de la interseccion.
    En clase Nodo cambiar lo de los nodos generados (_lt_ cambiado a comparar el estado.interseccion)
    Cambiar en a* el nombre del método getHeuristica
    Segmentos pasa a ser un diccionario de listas, en vez de PriorityQueue
    En la clase Problema hacer 3 for para crear los diccionarios

en la clase problema, los candidatos tenemos en cuenta su poblacion