from src import GreedyRandSol
from src.Solution import Solution


def startAlgorithm(maxIterations, project, alpha):
    bestSol = [Solution([], 1000000), {}]
    solutions = []
    for i in range(0, maxIterations):
        sol = GreedyRandSol.constructGRS(project, alpha)
        print("Solución creada con una duración de: ", sol.duration)
        solutions.append(sol)
        finishSol = localSearch(sol, project)
        if finishSol[0].duration < bestSol[0].duration:
            bestSol = finishSol
            print("Nuevo mejor tiempo", bestSol[0].duration)
    mostrarResultados()
    return bestSol


def localSearch(sol, project):
    for job in sol.scheme:
        can = canExecuteBeforeNew(job, project)
        if can[0]:
            actualizaTiemposyRec(job, can[1], project.resDicc)
    finishSol = actualizarSolucionEntera(sol, project)
    print("LocalSearch con nuevo mejor tiempo = ", sol.duration)
    return [sol, finishSol]


def actualizarSolucionEntera(sol, project):
    finishSol = initializeFinishSol(project.jobs[len(project.jobs) - 1].finishTime)
    for job in project.jobs:
        arrayFinished = finishSol[job.finishTime]
        arrayFinished.append(job)
    sol.duration = project.jobs[len(project.jobs) - 1].finishTime
    return finishSol


def initializeFinishSol(finishTime):
    finishSol = {}
    for i in range(0, finishTime + 1 ):
        finishSol[i] = []
    return finishSol


def canExecuteBeforeNew(job, project):
    can = [False, None]
    if job.njob > 0:
        initTime = job.initTime
        lateFinishTime = getLateFinishTime(job, project)
        for timeStep in range(lateFinishTime, initTime + 1):
            if canExecuteOnTimestep(timeStep, job, project):
                return [True, timeStep]
    return can


def getLateFinishTime(job, project):
    lateFinishTime = 0
    preds = project.predDicc[job.njob]
    for job in preds:
        pred = project.jobs[job.njob]
        finishTime = pred.finishTime
        if finishTime >= lateFinishTime:
            lateFinishTime = finishTime
    return lateFinishTime


def canExecuteOnTimestep(timeStep, job, project):
    result = False
    if timeStep > 0 and timeStep != job.initTime:
        if alreadyPredsNew(job, project.predDicc, timeStep) \
                and recNeededNew(timeStep, job, project.resDicc):
            result = True
    return result


def alreadyPredsNew(job, predDicc, timeStep):
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


def mostrarResultados():
    resultados = None
    # return resultados
