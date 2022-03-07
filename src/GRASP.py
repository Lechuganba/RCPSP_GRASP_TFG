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
            actualizaTiemposyRec(job, can[1], project.resDicc)
        entryProjectDicc(job, finishedDicc)
    sol.duration = project.jobs[len(project.jobs) - 1].finishTime
    print("LocalSearch con nuevo mejor tiempo = ", sol.duration)
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
        if alreadyPredsNew(job, newScheme, project.predDicc, finishedDicc, timeStep) \
                and recNeededNew(timeStep, job, project.resDicc):
            result = True
    return result


def alreadyPredsNew(job, newScheme, predDicc, finishedDicc, timeStep):
    result = True
    predAux = predDicc[job.njob]
    for pred in predAux:
        if pred.finishTime > timeStep:
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


def actualizaTiemposyRec(job, newTime, resDicc):
    oldInitTime = job.initTime
    job.initTime = newTime
    oldFinishTime = job.finishTime
    newFinishTime = newTime + job.duration
    job.finishTime = newFinishTime

    neededRec = job.resourceType
    neededQuant = job.resourceQuant

    for timeStep in range(oldInitTime + 1, oldFinishTime + 1):
        resTimestep = resDicc[timeStep]
        resTimestep[neededRec - 1] = resTimestep[neededRec - 1] + neededQuant

    for timeStep in range(newTime + 1, newFinishTime + 1):
        resTimestep = resDicc[timeStep]
        resTimestep[neededRec - 1] = resTimestep[neededRec - 1] - neededQuant


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
