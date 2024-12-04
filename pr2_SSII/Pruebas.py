from Clases import *
from Busqueda import *
import matplotlib.pyplot as plt
ruta_json = r'/Users/diego/Documents/GitHub/practicas_Inteligengtes/pr2_SSII/sample-problems-lab2/medium/calle_agustina_aroca_albacete_500_1_candidates_89_ns_22.json'


#valores = Busqueda_Aleatoria(problema,1000).busqueda()
#print(valores)
#a estrella
if __name__ == "__main__":
    from Busqueda import Busqueda_Genetica
    import matplotlib.pyplot as plt

    problema = Problema(ruta_json)
    genetica = Busqueda_Genetica(problema, 64, 100, 10, 2)
    
    # Ejecuta la búsqueda
    valores = genetica.busqueda()

    # Asegúrate de que 'valores' tiene datos antes de intentar graficarlo
    if valores is not None:
        plt.plot(valores)
        plt.show()
    else:
        print("No se generaron valores para graficar.")

