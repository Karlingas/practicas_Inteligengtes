from Clases import *
from Busqueda import *
ruta_json = r'pr1_SSII/examples_with_solutions/problems/large/calle_f_albacete_5000_4.json'

problema = Problema(ruta_json)

#a estrella
print("\na estrella")
a_estrella = Busqueda_a_estrella(problema).busqueda()