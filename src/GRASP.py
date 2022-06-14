from src import GreedyRandSol
from src.Solution import Solution


# Método de la ejecución principal del algoritmo
def startAlgorithm(maxIterations, project, alpha):
    # Solución inicial que vamos a eliminar una vez creada la primera solución
    bestSol = [Solution([], 1000000, 0), {}]
    # Array de soluciones para los resultados
    solutions = []
    # Bucle que crea las soluciones según el número de iteraciones
    for i in range(0, maxIterations):
        # Creamos la solución
        sol = GreedyRandSol.constructGRS(project, alpha)
        solutions.append(sol)
        # Ejecutamos el LocalSearch
        finishSol = localSearch(sol, project)
        # Comprobación de la solución creada
        if finishSol[0].makespan < bestSol[0].makespan:
            bestSol = finishSol
    return bestSol


# Método Local Search para la búsqueda de una mejor solución sobre la solución creada
def localSearch(sol, project):
    for job in sol.scheme:
        can = canExecuteBeforeNew(job, project)
        if can[0]:
            actualizeTimesAndRec(job, can[1], project.resDicc)
    finishSol = actualizeFullSolution(sol, project)
    return [sol, finishSol]


# Método para crear la solución final
def actualizeFullSolution(sol, project):
    finishSol = initialiceFinishSol(project.jobs[len(project.jobs) - 1].finishTime)
    for job in project.jobs:
        arrayFinished = finishSol[job.finishTime]
        arrayFinished.append(job)
    sol.makespan = project.jobs[len(project.jobs) - 1].finishTime
    return finishSol


# Método que inicializa el diccionario de la solución
def initialiceFinishSol(finishTime):
    finishSol = {}
    for i in range(0, finishTime + 1):
        finishSol[i] = []
    return finishSol


# Método para comprobar que un job puede ejecutarse antes
def canExecuteBeforeNew(job, project):
    can = [False, None]
    if job.njob > 0:
        initTime = job.initTime
        lateFinishTime = getLateFinishTime(job, project)
        for timeStep in range(lateFinishTime, initTime + 1):
            if canExecuteOnTimestep(timeStep, job, project):
                return [True, timeStep]
    return can


# Método para obtener el late finish time
def getLateFinishTime(job, project):
    lateFinishTime = 0
    preds = project.predDicc[job.njob]
    for job in preds:
        pred = project.jobs[job.njob]
        finishTime = pred.finishTime
        if finishTime >= lateFinishTime:
            lateFinishTime = finishTime
    return lateFinishTime


# Método que comprueba si un job puede ejecutarse en un timeStep
def canExecuteOnTimestep(timeStep, job, project):
    result = False
    if timeStep > 0 and timeStep != job.initTime:
        if alreadyPredsNew(job, project.predDicc, timeStep) \
                and recNeededNew(timeStep, job, project.resDicc):
            result = True
    return result


# Método que comprueba si los predecesores de un job han terminado de ejecutarse
def alreadyPredsNew(job, predDicc, timeStep):
    result = True
    predAux = predDicc[job.njob]
    for pred in predAux:
        if pred.finishTime > timeStep:
            result = False
    return result


# Método que comprueba si los recursos que necesita para ejecutarse están disponibles
def recNeededNew(timeStep, job, resDicc):
    result = False
    neededQuant = job.resourceQuant
    resTimestep = resDicc[timeStep]
    if compareRecsNew(resTimestep, neededQuant):
        result = True
    return result


def compareRecsNew(resTimestep, neededQuant):
    result = True
    for i in range(0, len(resTimestep)):
        if resTimestep[i] < neededQuant[i]:
            result = False
    return result


# Método que actualiza los tiempos del job y el diccionario de recursos
def actualizeTimesAndRec(job, newTime, resDicc):
    oldInitTime = job.initTime
    job.initTime = newTime
    oldFinishTime = job.finishTime
    newFinishTime = newTime + job.makespan
    job.finishTime = newFinishTime

    neededQuant = job.resourceQuant
    plusRecsNew(oldInitTime, oldFinishTime, resDicc, neededQuant)
    minusRecsNew(newTime, newFinishTime, resDicc, neededQuant)


def plusRecsNew(oldInitTime, oldFinishTime, resDicc, neededQuant):
    for timeStep in range(oldInitTime + 1, oldFinishTime + 1):
        resTimestep = resDicc[timeStep]
        for i in range(0, len(resTimestep)):
            resTimestep[i] = resTimestep[i] + neededQuant[i]


def minusRecsNew(newTime, newFinishTime, resDicc, neededQuant):
    for timeStep in range(newTime + 1, newFinishTime + 1):
        resTimestep = resDicc[timeStep]
        for i in range(0, len(resTimestep)):
            resTimestep[i] = resTimestep[i] - neededQuant[i]




