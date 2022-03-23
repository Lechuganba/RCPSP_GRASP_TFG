import InputData
from src import GRASP

if __name__ == '__main__':
    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    # filepath = "../resources/j120.sm/"
    print("¿Que tipo de problema quieres utilizar? Escriba el nombre de la carpeta:")
    okay = False
    folder = input()
    print("¿Que fichero quieres utilizar? Escriba el nombre del fichero (sin la extensión):")
    projectName = input()
    filepath = "../resources/" + folder + ".sm/" + projectName + ".sm"
    project = InputData.readFile(filepath, projectName)
    print("Proyecto creado correctamente")
    # project = InputData.readFile("../resources/j120.sm/j1201_10.sm", "j1201_10")
    print("Introduce el número de iteraciones para el algoritmo:")
    okay = False
    m = input()
    maxIterations = int(m)
    # maxIterations = 10
    print("Introduce el valor de alfa para el algoritmo, debe ser entre 0 y 1:")
    alpha = float(input())
    print("Comenzamos el algoritmo")
    bestSol = GRASP.startAlgorithm(maxIterations, project, alpha)
    print("Algoritmo terminado")
    print("La mejor solución ha sido el esquema con tiempo = ", bestSol[0].duration)
