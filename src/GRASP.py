from src import GreedyRandSol
import random

from src.GreedyRandSol import alreadyPreds, recNeeded
from src.Solution import Solution


def startAlgorithm(maxIterations, project, alpha):
    bestSol = Solution([], 1000000)
    solutions = []
    for i in range(0, maxIterations):
        sol = GreedyRandSol.constructGRS(project, alpha)
        print("Solución creada con una duración de: ", sol.duration)
        solutions.append(sol)
        sol = localSearch(sol, project)
        if sol.duration < bestSol.duration:
            bestSol = sol
            print("Nuevo mejor tiempo", bestSol.duration)
    mostrarResultados()
    return bestSol


def localSearch(sol, project):
    finished = False
    newDuration = 0
    while not finished:
        jobsOnTimestep = getJobsOnTimestep(sol, newDuration)
        for job in jobsOnTimestep:
            if canExecuteBefore(job, sol, newDuration, project) and job.initTime > newDuration:
                actualizarTiempos(sol)
                # actualizar los tiempos
        newDuration = newDuration + 1
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
        if alreadyPreds(job, sol.scheme, project.predDicc) and recNeededAux(job, newDuration,
                                                                            project.resDicc):
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


def actualizarTiempos(jobs):
    return 0


def mostrarResultados():
    resultados = None
    # return resultados
