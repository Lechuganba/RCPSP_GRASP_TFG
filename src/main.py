import argparse
import os
import time

import InputData
from src import GRASP
import Results

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Ejecutar directamente el problema en cuestión')
    parser.add_argument(
        '--problem', type=str, default="/j120.sm/", help='Path al proyecto que se quiere ejecutar, desde ../resources')
    parser.add_argument(
        '--iterations', type=str, default="25",
        help='Número de iteraciones a ejecutar por el algoritmo, debe ser mayor que 0')
    parser.add_argument(
        '--alpha', type=str, default="0.5", help='Valor de la variable alpha, debe ser entre 0 y 1')
    args = parser.parse_args()

    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    # Valor de alpha

    #Results.panditas()

    alphas = [0.25, 0.5, 0.75, 1]
    for k in alphas:
        dirs = ["j30", "j60", "j90", "j120"]
        for i in dirs:
            folder = "/" + i + ".sm/"
            listdir = os.listdir("../resources/" + i + ".sm")
            problemType = folder.split("/")[1]
            problemTypeAux = problemType.split(".")[0]
            path = "../results/totals/" + str(k) + "/" + problemTypeAux + ".csv"
            file = open(path, "w")
            file.write("projectName, makespan, duration;\n")
            for j in listdir:
                initMS = time.time()
                filepath = "../resources" + folder + j
                fp = open(filepath, "r")
                # Creación del proyecto
                projectName = j
                projectNameAux = projectName.split(".")[0]
                project = InputData.readFile(projectName, problemTypeAux, fp)
                # Número de iteraciones
                maxIterations = int(args.iterations)
                initMS = time.time()
                bestSol = GRASP.startAlgorithm(maxIterations, project, k)
                # Finalizamos y mostramos el mejor tiempo
                finishMS = time.time()
                bestSol[0].duration = finishMS - initMS
                file.write(projectNameAux + "," + str(bestSol[0].makespan) + "," + str(bestSol[0].duration) + ";\n")
            file.close()
