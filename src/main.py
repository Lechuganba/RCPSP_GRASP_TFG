import argparse
import os
import random
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
        '--iterations', type=str, default="50",
        help='Número de iteraciones a ejecutar por el algoritmo, debe ser mayor que 0')
    parser.add_argument(
        '--alpha', type=str, default="0.5", help='Valor de la variable alpha, debe ser entre 0 y 1')
    args = parser.parse_args()

    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    dirs = ["j30", "j60", "j90", "j120"]
    for dir in dirs:
        alphas = []
        for i in range(0, 4):
            alphaAux = round(random.random(), 2)
            alphas.append(alphaAux)
        folder = "/" + dir + ".sm/"
        listdir = os.listdir("../resources/" + dir + ".sm")
        instances = random.sample(listdir, 50)
        path = "../results/" + dir + ".csv"
        file = open(path, "w")
        file.write("projectName, alpha, makespan, duration;\n")
        for alpha in alphas:
            for j in instances:
                filepath = "../resources" + folder + j
                fp = open(filepath, "r")
                # Creación del proyecto
                projectName = j
                projectNameAux = projectName.split(".")[0]
                project = InputData.readFile(projectName, dir, fp)
                # Número de iteraciones
                maxIterations = int(args.iterations)
                initMS = time.time()
                bestSol = GRASP.startAlgorithm(maxIterations, project, alpha)
                # Finalizamos y mostramos el mejor tiempo
                finishMS = time.time()
                bestSol.duration = finishMS - initMS
                file.write(projectNameAux + "," + str(alpha) + "," + str(bestSol.makespan) + "," + str(bestSol.duration) + ";\n")
        file.close()
        Results.processResults(alphas, dir)

