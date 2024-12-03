from Clases import *
from Busqueda import *
import matplotlib.pyplot as plt
ruta_json = r'pr2_SSII\sample-problems-lab2\toy\calle_del_virrey_morcillo_albacete_250_3_candidates_15_ns_4.json'

problema = Problema(ruta_json)
valores = Busqueda_Aleatoria(problema,1000).busqueda()
print(valores)
#a estrella
valores = Busqueda_Genetica(problema,6,1000,2,10).busqueda()

print(valores)
# Dibujar la gráfica
plt.plot(valores)

# Mostrar la gráfica
plt.show()
