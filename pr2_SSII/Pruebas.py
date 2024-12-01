from Clases import *
from Busqueda import *
ruta_json = r'/Users/diego/Documents/GitHub/practicas_Inteligengtes/pr2_SSII/sample-problems-lab2/toy/calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'

problema = Problema(ruta_json)

#a estrella
print(Busqueda_Genetica(problema,2,100,2).busqueda())

