import datetime
from Classes import *
from Busqueda import Busqueda_Anchura, Busqueda_Primero_Mejor,Busqueda_Profundidad, Busqueda_a_estrella
#Windows
#ruta_json = r'problems\medium\calle_mariÌa_mariÌn_500_0.json'
#MacOs
ruta_json = r'pr1_SSII/examples_with_solutions/problems/huge/calle_agustina_aroca_albacete_5000_0.json'

# Mostrar la solución y estadísticas
def imprimir_esta():
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

# Crear el objeto problema
problema = Problema(ruta_json)

# Anchura
anchura = Busqueda_Anchura(problema=problema)
solucion, soluciones_generadas, nodos_explorados, nodos_expandidos, coste, profundidad = anchura.buscar()
imprimir_esta()

# Profundidad
profun = Busqueda_Profundidad(problema=problema)
solucion, soluciones_generadas, nodos_explorados, nodos_expandidos, coste, profundidad = profun.buscar()
imprimir_esta()

primero_mejor = Busqueda_Primero_Mejor(problema)
# Ejecutar el algoritmo de búsqueda
solucion, soluciones_generadas, nodos_explorados, nodos_expandidos, coste, profundidad = primero_mejor.buscar()
tiempesito = datetime(coste)
imprimir_esta()

a_estre = Busqueda_a_estrella(problema)
solucion, soluciones_generadas, nodos_explorados, nodos_expandidos, coste, profundidad = a_estre.buscar()
imprimir_esta()
