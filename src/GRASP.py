from src import GreedyRandSol
import random

from src.Solution import Solution


def startAlgorithm(maxIterations, project, seed):
    bestSol = Solution([], 1000000)
    solutions = []
    for i in range(0, maxIterations):
        sol = GreedyRandSol.generateGRS(project, seed)
        print("Solución creada con una duración de: ", sol.duration)
        solutions.append(sol)
        # if not self.isFactible(sol):
        #    sol = self.repair(sol)
        timeSol = localSearch(sol, solutions)
        if timeSol.duration < bestSol.duration:
            bestSol = timeSol
            print("Nuevo mejor tiempo", bestSol.duration)
    mostrarResultados()
    return bestSol


def isFactible(sol):
    return 0


def localSearch(sol, solutions):
    localSol = sol
    better = findBetter(sol, solutions)
    while better:
        localSol = random.choice(better)
        better = findBetter(localSol, solutions)
    return localSol


def findBetter(sol, solutions):
    better = []
    for i in range(0, len(solutions)):
        if solutions[i].duration < sol.duration:
            better.append(solutions[i])
    return better


def repair(sol):
    return 0


def mostrarResultados():
    resultados = None
    # return resultados
