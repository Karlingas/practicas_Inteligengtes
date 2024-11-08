from Clases import *
from Busqueda import *
ruta_json = r'pr2_SSII/sample-problems-lab2\toy\calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'

problema = Problema(ruta_json)

#a estrella
print("\na estrella")
a_estrella = Busqueda_a_estrella(problema).busqueda()