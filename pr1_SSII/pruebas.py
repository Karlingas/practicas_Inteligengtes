from Classes import *
from Busqueda import Busqueda_Anchura
#Windows
#ruta_json = r'problems\medium\calle_mariÌa_mariÌn_500_0.json'
#MacOs
ruta_json = r'pr1_SSII/problems/medium/calle_mariÌa_mariÌn_500_0.json'

# Crear el objeto problema
problema = Problema(ruta_json)

anchura = Busqueda_Anchura(problema=problema)

# Ejecutar el algoritmo de búsqueda
solucion, soluciones_generadas, nodos_explorados, nodos_expandidos, coste, profundidad = anchura.buscar()

# Mostrar la solución y estadísticas
if solucion:
    print("Solución encontrada:", solucion)
    print("Estadísticas:")
    print(f"Número de soluciones generadas: {soluciones_generadas}")
    print(f"Número de nodos explorados: {nodos_explorados}")
    print(f"Número de nodos expandidos: {nodos_expandidos}")
    print(f"Coste de la solución: {coste}")
    print(f"Profundidad de la solución: {profundidad}")
else:
    print("No se encontró solución.")