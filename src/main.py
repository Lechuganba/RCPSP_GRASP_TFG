import os
import time

import InputData
from src import GRASP, Const

if __name__ == '__main__':
    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    dirs = [Const.j30, Const.J60, Const.j90, Const.J120]
    for dir in dirs:
        folder = "/" + dir + ".sm/"
        listdir = os.listdir("../resources/" + dir + ".sm")
        path = "../results/" + dir + "Final-1.csv"
        file = open(path, "w")
        file.write("projectName, alpha, makespan, duration;\n")
        alphas = [0.25, 0.5, 0.75, 1]
        maxIterations = [100]
        for j in listdir:
            for it in maxIterations:
                filepath = "../resources" + folder + j
                fp = open(filepath, "r")
                # Creación del proyecto
                projectName = j
                projectNameAux = projectName.split(".")[0]
                project = InputData.readFile(projectName, dir, fp)
                # Número de iteraciones
                initMS = time.time()
                bestSol = GRASP.startAlgorithm(it, project, 1)
                # Finalizamos y mostramos el mejor tiempo
                finishMS = time.time()
                bestSol.duration = round(finishMS - initMS, 2)
                file.write(projectNameAux + "," + str(it) + "," + "RND" + "," + str(bestSol.makespan) + "," + str(
                    bestSol.duration) + "\n")
        file.close()
