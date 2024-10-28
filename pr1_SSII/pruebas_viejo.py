from pr1_SSII.Classes_viejo import *
from pr1_SSII.Busqueda_viejo import Busqueda_Anchura, Busqueda_Primero_Mejor,Busqueda_Profundidad, Busqueda_a_estrella
#Windows
#ruta_json = r'problems\medium\calle_mariÌa_mariÌn_500_0.json'
#MacOs
ruta_json = r'pr1_SSII/examples_with_solutions/problems/large/calle_agustina_aroca_albacete_1000_2.json'

#horas
def horas(numero):
 tiempo =numero 
 horas=int(tiempo)
 minutos=(tiempo*60) % 60
 return "%02d:%02d"%(horas,minutos)

# Mostrar la solución y estadísticas
def imprimir_esta():
    if solucion:
        print("\n\nEstadísticas:")
        print("Tiempo de ejecuccion: ", tiempo)
        print(f"Nodos generados: {soluciones_generadas}")
        print(f"Nodos expandidos: {nodos_expandidos}")
        print(f"Coste: {horas(coste/60)}")
        print(f"Profundidad de la solución: {profundidad}")
        print("Solución encontrada:", solucion)
    else:
        print("No se encontró solución.")

# Crear el objeto problema
problema = Problema(ruta_json)

# Anchura
anchura = Busqueda_Anchura(problema=problema)
solucion, soluciones_generadas, nodos_expandidos, coste, profundidad, tiempo = anchura.buscar()
imprimir_esta()

# Profundidad
profun = Busqueda_Profundidad(problema=problema)
solucion, soluciones_generadas, nodos_expandidos, coste, profundidad, tiempo = profun.buscar()
imprimir_esta()

