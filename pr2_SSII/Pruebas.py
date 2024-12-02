from Clases import *
from Busqueda import *
import matplotlib.pyplot as plt
ruta_json = r'/Users/diego/Documents/GitHub/practicas_Inteligengtes/pr2_SSII/sample-problems-lab2/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'

problema = Problema(ruta_json)

#a estrella
valores = Busqueda_Genetica(problema,10,5,4).busqueda()


# Dibujar la gráfica
plt.plot(valores)

# Mostrar la gráfica
plt.show()
