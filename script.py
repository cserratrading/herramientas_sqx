import matplotlib.pyplot as plt
import numpy as np
from settings import runs, oos_percentage, failed_optimization


def function_matrix():
    # Tamaño de la matriz
    oos_percentage_labels = list(range(oos_percentage[0], oos_percentage[1] + 1, 2))
    runs_labels = list(range(runs[1], runs[0] - 1, -1))
    wf_matrix = np.ones((len(runs_labels), len(oos_percentage_labels)))  # 1 representará aciertos

    # Fallos que se pasan como lista de tuplas
    failed_combinations = [(run, oos) for run, oos_list in failed_optimization.items() for oos in oos_list]

    # Convertimos los fallos en posiciones de la matriz
    for fail in failed_combinations:
        run_failed, oos_failed = fail
        if oos_failed in oos_percentage_labels and run_failed in runs_labels:
            oos_idx = oos_percentage_labels.index(oos_failed)
            run_idx = runs_labels.index(run_failed)
            wf_matrix[run_idx, oos_idx] = 0

    # Invertir la matriz para que la representación gráfica muestre el eje Y invertido
    wf_matrix = np.flipud(wf_matrix)

    # Función para determinar si una celda es un super acierto
    def es_super_acierto(matrix, i, j):
        if matrix[i, j] != 1:
            return False
        # Verificar las 8 celdas adyacentes
        adyacentes = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                      (i, j - 1), (i, j + 1),
                      (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        for x, y in adyacentes:
            if x < 0 or y < 0 or x >= matrix.shape[0] or y >= matrix.shape[1]:
                return False
            if matrix[x, y] != 1:
                return False
        return True

    # Determinar super aciertos
    super_aciertos = []
    for i in range(wf_matrix.shape[0]):
        for j in range(wf_matrix.shape[1]):
            if es_super_acierto(wf_matrix, i, j):
                super_aciertos.append((i, j))

    # Marcar super aciertos en la matriz con 2
    for i, j in super_aciertos:
        wf_matrix[i, j] = 2

    # Función para determinar si una celda es un mega acierto
    def es_mega_acierto(matrix, i, j):
        if matrix[i, j] != 2:
            return False
        # Verificar las 8 celdas adyacentes que deben ser super aciertos
        adyacentes = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                      (i, j - 1), (i, j + 1),
                      (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        for x, y in adyacentes:
            if x < 0 or y < 0 or x >= matrix.shape[0] or y >= matrix.shape[1]:
                return False
            if matrix[x, y] != 2:
                return False
        return True

    # Determinar mega aciertos
    mega_aciertos = []
    for i in range(wf_matrix.shape[0]):
        for j in range(wf_matrix.shape[1]):
            if es_mega_acierto(wf_matrix, i, j):
                mega_aciertos.append((i, j))

    # Marcar mega aciertos en la matriz con 3
    for i, j in mega_aciertos:
        wf_matrix[i, j] = 3

    # Colores para la matriz
    colors = ['red', 'green', 'blue', 'purple']

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Mostrar la matriz
    cmap = plt.cm.colors.ListedColormap(['red', 'green', 'blue', 'purple'])
    cax = ax.matshow(wf_matrix, cmap=cmap)

    # Configurar los ejes con los labels
    ax.set_xticks(np.arange(len(oos_percentage_labels)))
    ax.set_xticklabels([f"{x}%" for x in oos_percentage_labels])

    ax.set_yticks(np.arange(len(runs_labels)))
    ax.set_yticklabels(runs_labels[::-1])

    # Añadir colorbar para la leyenda
    cbar = fig.colorbar(cax, ticks=[0, 1, 2, 3], orientation='vertical')
    cbar.ax.set_yticklabels(['Fallos', 'Aciertos', 'Super Aciertos', 'Mega Aciertos'])

    plt.show()
    pass


if __name__ == '__main__':
    function_matrix()
