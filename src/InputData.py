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


# Creación del diccionario de predecesores
def getPred(jobs):
    predDicc = {}
    for j in jobs:
        preds = []
        for k in jobs:
            succ = k.succ
            if succ.__contains__(j.njob):
                preds.append(k)
        predDicc[j.njob] = preds
    return predDicc


def projectType(projectType):
    valores = []
    if projectType == "j30":
        valores = [18, 50, 36, 89]
    elif projectType == "j60":
        valores = [18, 80, 66, 149]
    elif projectType == "j90":
        valores = [18, 110, 96, 209]
    elif projectType == "j120":
        valores = [18, 140, 126, 269]
    return valores


# Lectura de los datos del fichero
def readFile(projectName, problemTypeAux,  fp):
    # Variables que vamos a utilizar
    # Diccionario de sucesores
    succDicc = {}
    projectype = projectType(problemTypeAux)

    lines = fp.readlines()

    # Obtenemos las actividades
    jobs = []
    for i in range(projectype[0], projectype[1]):
        line = lines[i]
        lineAux = lines[i + projectype[2]]
        words = line.split(" ")
        wordsAux = lineAux.split(" ")
        numbers = getNumbers(words)
        numbersAux = getNumbers(wordsAux)
        dyr = getDyr(numbersAux)
        if numbers and numbersAux:
            job = Job(numbers, dyr)
            jobs.append(job)
            succDicc[job.njob] = job.succ

    # Obtenemos los recursos
    resources = []
    lineResources = lines[projectype[3]]
    wordsRes = lineResources.split(" ")
    resourcesAux = getNumbers(wordsRes)
    for j in range(0, len(resourcesAux)):
        r = Resource(j + 1, resourcesAux[j])
        resources.append(r)

    # Diccionario de predecesores
    predDicc = getPred(jobs)
    # Diccionario de recursos en un timeStep
    resDicc = {}
    # Creación del objeto Project
    project = Project(projectName, jobs, resources, succDicc, predDicc, resDicc)
    return project
