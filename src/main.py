import InputData
from GreedyRandSol import GreedyRandSol
from GRASP import GRASP
if __name__ == '__main__':
    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    filepath = "./resources/j120.sm/"
    # print("¿Que proyecto quieres utilizar? Escriba el nombre del proyecto:")
    # projectName = input()
    # filepath = filepath + projectName + ".sm"
    # project = InputData.readFile(filepath, projectName)
    project = InputData.readFile("../resources/j120.sm/j1201_10.sm", "j1201_10")
    print("Proyecto creado correctamente")
    # print("Introduce el número de iteraciones para el algoritmo:")
    # maxIterations = int(input())
    maxIterations = 100
    swarm = GreedyRandSol(5)
    seed = 0.5
    print("Comenzamos el algoritmo")
    GRASP.startAlgorithm(GRASP, maxIterations, project, seed)
