-De la clase busqueda hemos cambiado:
    Hemos añadido un final y un inicial que se asignan en A*, (no sabemos si quitar el tiempo de ejecuccion) pero si hemos quitado las estadisticas. 
    En a* ahora se le pasa en el constructor un inicial y un final que son el identificador de la interseccion.
    En clase Nodo cambiar lo de los nodos generados (_lt_ cambiado a comparar el estado.interseccion)
    Cambiar en a* el nombre del método getHeuristica
    Segmentos pasa a ser un diccionario de listas, en vez de PriorityQueue
    En la clase Problema hacer 3 bucles for para crear los diccionarios

en la clase problema, los candidatos tenemos en cuenta su poblacion

Respecto al AG:
    - Hemos utilizado una representacion binaria, ya que es la que mejor funciona para este problema, nos permite en un array con una velocidad de cómputo rápida almacenar las estaciones elegidas con un 1 y las no elegidas con un 0.
    - En la primera implementación, respecto al método de selección hemos utilizado la selección por torneo, con el objetivo de probar el algoritmo con la menor presión selectiva posible.
        Como comprobamos que los resultados eran poco consistentes probamos con un método de selección con mayor presión selectiva, por lo que implementamos la selección proporcional al fitness. Pero también nos dimos cuenta que caímos en el peligro de que un valor cope toda la población.
        Como último método de seleccion y (creo de momento que el mejor) hemos implementado la selección basada en rango, ya que tiene una presión selectiva mayor que el método por torneo, pero no tan alta como la selección proporcional al fitness. Lo que nos permite elegir mejor un valor adecuado pero no caer rápidamente en un valor que converga rápidamente.