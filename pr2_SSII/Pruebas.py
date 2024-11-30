from Clases import *
from Busqueda import *
ruta_json = r'/Users/diego/Documents/GitHub/practicas_Inteligengtes/pr2_SSII/sample-problems-lab2/small/calle_agustina_aroca_albacete_250_0_candidates_75_ns_7.json'

problema = Problema(ruta_json)

#a estrella
alea = Busqueda_Aleatoria(problema, 10)

soluciones = alea.busqueda()

for sol in soluciones:
    print(sol)

