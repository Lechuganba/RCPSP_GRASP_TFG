import argparse
import os
import time

import InputData
from src import GRASP

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Ejecutar directamente el problema en cuestión')
    parser.add_argument(
        '--problem', type=str, default="/j120.sm/", help='Path al proyecto que se quiere ejecutar, desde ../resources')
    parser.add_argument(
        '--iterations', type=str, default="100", help='Número de iteraciones a ejecutar por el algoritmo, debe ser mayor que 0')
    parser.add_argument(
        '--alpha', type=str, default="0.5", help='Valor de la variable alpha, debe ser entre 0 y 1')
    args = parser.parse_args()

    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    listdir = os.listdir("../resources/j120.sm")
    for i in listdir:
        initMS = time.time()
        # Tipo de problema
        folder = args.problem
        # Nombre del proyecto
        filepath = "../resources" + folder + i
        fp = open(filepath, "r")
        # Creación del proyecto
        projectName = i
        #projectName = folder.split("/")[2]
        problemType = folder.split("/")[1]
        projectNameAux = projectName.split(".")[0]
        problemTypeAux = problemType.split(".")[0]
        path = "../results/" + problemTypeAux + "/" + projectNameAux + ".csv"
        file = open(path, "w")
        print(projectNameAux) #j12060_10, j9030_4
        project = InputData.readFile(projectName, problemTypeAux, fp)
        # Número de iteraciones
        maxIterations = int(args.iterations)
        # Valor de alpha
        alpha = float(args.alpha)
        i = 0
        alphas = [0.25, 0.5, 0.75, 1]
        for j in range(0, 4):
            alpha = alphas[i]
            initMS = time.time()
            bestSol = GRASP.startAlgorithm(maxIterations, project, alpha)
            # Finalizamos y mostramos el mejor tiempo
            finishMS = time.time()
            bestSol[0].duration = finishMS - initMS
            file.write(str(alpha) + "," + str(bestSol[0].makespan) + "," + str(bestSol[0].duration) + ";\n")
        file.close()
