from Clases import *
from Busqueda import *
#ruta_json = r'problems\medium\calle_mariÌa_mariÌn_500_0.json'

ruta_json = r'pr1_SSII/examples_with_solutions/problems/large/calle_f_albacete_5000_4.json'

problema = Problema(ruta_json)

#a estrella
print("\na estrella")
a_estrella = Busqueda_a_estrella(problema).busqueda()

#anchura
print("\nanchura")
anchura = Busqueda_Anchura(problema).busqueda()

#profundidad
print("\nprofundidad")
profundidad = Busqueda_Profundidad(problema).busqueda()

#primero mejor
print("\nprimero mejor")
primero_mejor = Busqueda_Primero_Mejor(problema).busqueda()