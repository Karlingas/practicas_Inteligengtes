from Clases import *
import matplotlib.pyplot as plt
from MetaHeuristicas import BusquedaGenetica, BusquedaAleatoria
ruta_json = r'/Users/diego/Documents/GitHub/practicas_Inteligengtes/pr2_SSII/sample-problems-lab2/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'


#valores = Busqueda_Aleatoria(problema,1000).busqueda()



problema = Problema(ruta_json)

genetica = BusquedaGenetica(problema, 80, 100)
    
# Ejecuta la búsqueda
valores = genetica.buscar()

plt.plot(valores)
plt.show()


"""
problema = Problema(ruta_json)

aleatoria = BusquedaAleatoria(problema, 1000).buscar()
"""