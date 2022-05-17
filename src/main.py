import argparse
import os
import shutil

import InputData
from src import GRASP

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Ejecutar directamente el problema en cuestión')
    parser.add_argument(
        '--problem', type=str, default="/j30.sm/j301_1.sm", help='Path al proyecto que se quiere ejecutar, desde ../resources')
    parser.add_argument(
        '--iterations', type=str, default="100", help='Número de iteraciones a ejecutar por el algoritmo, debe ser mayor que 0')
    parser.add_argument(
        '--alpha', type=str, default="0.5", help='Valor de la variable alpha, debe ser entre 0 y 1')
    args = parser.parse_args()

    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    # Tipo de problema
    folder = args.problem
    # Nombre del proyecto
    filepath = "../resources" + folder
    fp = open(filepath, "r")
    # Creación del proyecto
    projectName = folder.split("/")[2]
    problemType = folder.split("/")[1]
    project = InputData.readFile(filepath, projectName, fp)
    # Número de iteraciones
    maxIterations = int(args.iterations)
    # Valor de alpha
    alpha = float(args.alpha)
    bestSol = GRASP.startAlgorithm(maxIterations, project, alpha)
    # Finalizamos y mostramos el mejor tiempo
    projectNameAux = projectName.split(".")[0]
    problemTypeAux = problemType.split(".")[0]
    print("La mejor solución ha sido el esquema con tiempo = ", bestSol[0].makespan)
    #os.makedirs("../results/j120")
    path = "../results/" + problemTypeAux + "/" + projectNameAux + ".txt"
    file = open(path, "w")
    file.write("Problem: " + projectNameAux + ", Makespan: " + str(bestSol[0].makespan) + ", Duration: " + str(bestSol[0].duration))
    file.close()
