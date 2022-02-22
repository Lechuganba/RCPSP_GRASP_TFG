from Job import Job
from Resource import Resource
from Project import Project


# Método para obtener solo los números de la línea que leemos
def getNumbers(a):
    numbers = []
    for i in range(0, len(a)):
        if a[i] != "":
            if a[i].__contains__("\n"):
                n = a[i].split("\n")
                if n[0] != '':
                    numbers.append(int(n[0]))
            else:
                numbers.append(int(a[i]))
    return numbers


# Método para obtener la duración, el tipo de recurso
# y la cantidad de recusoss de la línea que leemos
def getDyr(numbersAux):
    tupla = [0, 0, 0]
    tupla[0] = numbersAux[2]
    for i in range(3, len(numbersAux)):
        if numbersAux[i] != 0:
            tupla[1] = numbersAux[i]
            tupla[2] = i - 2
    return tupla


# Lectura de los datos del fichero j1201_10.sm
def readFile(filepath, projectName):
    # Variables que vamos a utilizar
    succDicc = {}

    # Abrimos el fichero en modo lectura
    fp = open(filepath, "r")
    lines = fp.readlines()

    # Obtenemos las actividades
    jobs = []
    for i in range(18, 140):
        line = lines[i]
        lineAux = lines[i + 126]
        words = line.split(" ")
        wordsAux = lineAux.split(" ")
        numbers = getNumbers(words)
        numbersAux = getNumbers(wordsAux)
        dyr = getDyr(numbersAux)
        if numbers and numbersAux:
            job = Job(numbers, dyr)
            jobs.append(job)
            succDicc[job.njob] = job.succ

    # Obtención de los recursos
    resources = []
    lineResources = lines[269]
    wordsRes = lineResources.split(" ")
    resourcesAux = getNumbers(wordsRes)
    for j in range(0, len(resourcesAux)):
        r = Resource(j + 1, resourcesAux[j])
        resources.append(r)

    # Creación del objeto Project
    project = Project(projectName, jobs, resources, succDicc)
    return project
