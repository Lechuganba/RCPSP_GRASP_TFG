from src import GreedyRandSol

from src.GreedyRandSol import alreadyPreds, recNeeded
from src.Solution import Solution


def startAlgorithm(maxIterations, project, alpha):
    bestSol = Solution([], 1000000)
    solutions = []
    for i in range(0, maxIterations):
        sol = GreedyRandSol.constructGRS(project, alpha)
        print("Solución creada con una duración de: ", sol.duration)
        solutions.append(sol)
        sol = localSearchNew(sol, project)
        if sol.duration < bestSol.duration:
            bestSol = sol
            print("Nuevo mejor tiempo", bestSol.duration)
    mostrarResultados()
    return bestSol


def localSearchNew(sol, project):
    newScheme = []
    finishedDicc = initialiceFinishedDicc(sol.duration)
    for job in sol.scheme:
        can = canExecuteBeforeNew(job, sol, project, newScheme, finishedDicc)
        if can[0]:
            actualizaTiempos(job, can[1])
        entryProjectDicc(job, finishedDicc)
    return sol


def initialiceFinishedDicc(duration):
    dicc = {}
    for i in range(0, duration):
        dicc[i] = []
    return dicc


def entryProjectDicc(job, finishedDicc):
    array = finishedDicc[job.finishTime]
    array.append(job)


def canExecuteBeforeNew(job, sol, project, newScheme, finishedDicc):
    can = [False, None]
    if job.njob > 0:
        initTime = job.initTime
        for timeStep in range(0, initTime + 1):
            if canExecuteOnTimestep(timeStep, job, project, sol, newScheme, finishedDicc):
                return [True, timeStep]
    return can


def canExecuteOnTimestep(timeStep, job, project, sol, newScheme, finishedDicc):
    result = False
    if timeStep > 0 and timeStep != job.initTime:
        if alreadyPredsNew(job, newScheme, project.predDicc, finishedDicc) and recNeededNew(timeStep, job, project.resDicc):
            result = True
    return result


def alreadyPredsNew(job, newScheme, predDicc, finishedDicc):
    result = True
    predAux = predDicc[job.njob]
    for pred in predAux:
        finishedOnTime = finishedDicc[pred.finishTime]
        if not finishedOnTime.__contains__(pred):
            result = False
    return result


def recNeededNew(timeStep, job, resDicc):
    result = False
    neededRec = job.resourceType
    neededQuant = job.resourceQuant
    resTimestep = resDicc[timeStep]
    if resTimestep[neededRec - 1] >= neededQuant:
        result = True
    return result


def actualizaTiempos(job, newTime):
    job.initTime = newTime
    job.finishTime = newTime + job.duration


def desencadenamiento(sol, project):
    return 0


###### OLD ######
def localSearch(sol, project):
    finished = False
    newDuration = 0
    while not finished:
        for job in sol.scheme:
            if canExecuteBefore(job, sol, newDuration, project):
                refreshTimesAndResources(job, newDuration, sol, project)
            # actualizar los tiempos
        # newDuration = newDuration + 1
    return sol


def getJobsOnTimestep(sol, newDuration):
    result = []
    for job in sol.scheme:
        if job.initTime == newDuration:
            result.append(job)
    return result


def canExecuteBefore(job, sol, newDuration, project):
    result = False
    if job.njob > 0:
        if alreadyPredsNew(job, sol.scheme, project.predDicc) \
                and recNeededAux(job, project.resDicc):
            result = True
    return result


def recNeededAux(job, newDuration, resDicc):
    result = False
    neededRec = job.resourceType
    neededQuant = job.resourceQuant
    resTimestep = resDicc[newDuration]
    if resTimestep[neededRec - 1] >= neededQuant:
        result = True
    return result


def refreshTimesAndResources(job, newDuration, sol, project):
    refreshJobTimes(job, newDuration)
    refreshResourceDicc(project)
    return 0


def refreshJobTimes(job, newDuration):
    job.initTime = newDuration
    job.finishTime = newDuration + job.duration


def refreshResourceDicc(project):
    return 0


def mostrarResultados():
    resultados = None
    # return resultados
