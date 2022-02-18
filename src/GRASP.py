from GreedyRandSol import GreedyRandSol


class GRASP:

    def startAlgorithm(self, maxIterations, project, seed):
        bestSol = None
        for i in range(0, maxIterations):
            sol = GreedyRandSol.generateGRS(project, seed)
            if not self.isFactible(sol):
                sol = self.repair(sol)
            timeSol = self.localSearch(sol)
            if timeSol < bestSol:
                bestSol = timeSol
        self.mostrarResultados()
        return bestSol

    def isFactible(self, sol):
        return 0

    def localSearch(self, sol):
        return 0

    def mostrarResultados(self):
        resultados = None
        # return resultados
