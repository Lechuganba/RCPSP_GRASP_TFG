import InputData
from src import GRASP

if __name__ == '__main__':
    # Inicializamos la lectura del fichero con el método de la clase InputData
    # y creamos el proyecto
    # Tipo de problema
    print("¿Que tipo de problema quieres utilizar? Escriba el nombre de la carpeta:")
    while 1:
        folder = input()
        if folder == "j30" or folder == "j60" or folder == "j90" or folder == "j120":
            break
        else:
            print("No se encuentra la carpeta, por favor, introduzca de nuevo:")
    # Nombre del proyecto
    print("¿Que fichero quieres utilizar? Escriba el nombre del fichero (sin la extensión):")
    while 1:
        try:
            projectName = input()
            filepath = "../resources/" + folder + ".sm/" + projectName + ".sm"
            fp = open(filepath, "r")
            print("Hola")
        except FileNotFoundError:
            print("El fichero", projectName, ".sm no existe o no se encuentra, introduce de nuevo el nombre del proyecto")
            continue
        if fp:
            break
    # Creación del proyecto
    project = InputData.readFile(filepath, projectName, fp)
    print("Proyecto creado correctamente")

    # Número de iteraciones
    print("Introduce el número de iteraciones para el algoritmo:")
    while 1:
        try:
            m = input()
            maxIterations = int(m)
        except ValueError:
            print(m, "no es un número entero, introduzca de nuevo:")
            continue
        if maxIterations > 0:
            break
        else:
            print("El número debe ser mayor que 0, introduzca de nuevo")
    # Valor de alpha
    print("Introduce el valor de alfa para el algoritmo, debe ser un número entre 0 y 1:")
    while 1:
        try:
            a = input()
            alpha = float(a)
        except ValueError:
            print(alpha, "no es un número, introduzca de nuevo")
            continue
        if 0 < alpha < 1:
            okay = True
            break
        else:
            print("alpha no es un número valido, introduce el valor de alfa entre los valores permitdos:")

    print("Comenzamos el algoritmo")
    bestSol = GRASP.startAlgorithm(maxIterations, project, alpha)
    # Finalizamos y mostramos el mejor tiempo
    print("Algoritmo terminado")
    print("La mejor solución ha sido el esquema con tiempo = ", bestSol[0].duration)
