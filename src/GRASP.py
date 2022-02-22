from src import GreedyRandSol
import random

from src.Solution import Solution


def startAlgorithm(maxIterations, project, alpha):
    bestSol = Solution([], 1000000)
    solutions = []
    for i in range(0, maxIterations):
        sol = GreedyRandSol.constructGRS(project, alpha)
        print("Solución creada con una duración de: ", sol.duration)
        solutions.append(sol)
        # if not self.isFactible(sol):
        #    sol = self.repair(sol)
        timeSol = localSearch(sol)
        if timeSol.duration < bestSol.duration:
            bestSol = timeSol
            print("Nuevo mejor tiempo", bestSol.duration)
    mostrarResultados()
    return bestSol


def isFactible(sol):
    return 0


def localSearch(sol):
    return sol


def repair(sol):
    return 0


def mostrarResultados():
    resultados = None
    # return resultados
