from Clases import *
import matplotlib.pyplot as plt
from MetaHeuristicas import BusquedaGenetica, BusquedaAleatoria
ruta_json = r'/Users/diego/Documents/GitHub/practicas_Inteligengtes/pr2_SSII/sample-problems-lab2/small/calle_agustina_aroca_albacete_250_0_candidates_75_ns_7.json'



problema = Problema(ruta_json)

genetica = BusquedaGenetica(problema, 50, 100)
    
# Ejecuta la búsqueda
valores = genetica.buscar()

plt.plot(valores)
#plt.show()


"""
problema = Problema(ruta_json)

aleatoria = BusquedaAleatoria(problema, 1000).buscar()
"""