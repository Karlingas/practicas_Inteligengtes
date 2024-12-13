from Clases import *
import matplotlib.pyplot as plt
from MetaHeuristicas import BusquedaGenetica, BusquedaAleatoria
ruta_json = r'pr2_SSII\sample-problems-lab2\large\calle_del_virrey_morcillo_albacete_1000_1_candidates_598_ns_99.json'


#valores = Busqueda_Aleatoria(problema,1000).busqueda()



problema = Problema(ruta_json)

genetica = BusquedaGenetica(problema, 50, 100)
    
# Ejecuta la búsqueda
valores = genetica.buscar()

plt.plot(valores)
plt.show()


"""
problema = Problema(ruta_json)

aleatoria = BusquedaAleatoria(problema, 1000).buscar()
"""