import random
import InputData
from src import GRASP

if __name__ == '__main__':
    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    filepath = "../resources/j120.sm/"
    # print("¿Que proyecto quieres utilizar? Escriba el nombre del proyecto:")
    # projectName = input()
    # filepath = filepath + projectName + ".sm"
    # project = InputData.readFile(filepath, projectName)
    # meter try-catch para comprobar que el nombre del proyecto es correcto
    project = InputData.readFile("../resources/j120.sm/j1201_10.sm", "j1201_10")
    print("Proyecto creado correctamente")
    # print("Introduce el número de iteraciones para el algoritmo:")
    # maxIterations = int(input())
    maxIterations = 10
    seed = random.random()
    print("Comenzamos el algoritmo")
    bestSol = GRASP.startAlgorithm(maxIterations, project, seed)
    print("Algoritmo terminado")
    print("La mejor solución ha sido el esquema con tiempo = ", bestSol.duration)