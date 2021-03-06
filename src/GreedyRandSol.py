import random

from src.Solution import Solution


# Método que contruye la solución
def constructGRS(project, alpha):
    # Reseteamos los tiempos de todos los jobs
    reset(project)
    # Array que representa el esquema de la solución
    scheme = []
    # Project Duration Time
    makespan = 0
    # Duration in ms
    duration = 0
    # Solution:
    sol = Solution(scheme, makespan, duration, {})
    # Array que almacena los finished jobs
    finishedJobs = []
    # Array que almacena los jobs que se estan ejecutando
    executingJobs = []
    # Obtención de la candidate list
    candidateList = getCandidateList(project, makespan, finishedJobs, scheme)
    # Evaluate incremental cost
    evaluateIncrementalCost(candidateList, makespan)
    # Bucle para la construcción de la solución
    while 1:
        if candidateList:
            minMax = getMinMax(candidateList)
            restrictedCL = getRestrictedCandidateList(candidateList, minMax, alpha)
            sig = selectNext(restrictedCL)
            if sig is not None:
                scheme.append(sig)
                executeActivity(makespan, project, sig, executingJobs)
        if makespan == 0:
            getFinishedActivities(executingJobs, project, makespan, finishedJobs)
        if len(finishedJobs) == len(project.jobs) - 1:
            addEntryRecDicc(makespan, project)
            getFinishedActivities(executingJobs, project, makespan, finishedJobs)
            break
        addEntryRecDicc(makespan, project)
        makespan = makespan + 1
        getFinishedActivities(executingJobs, project, makespan, finishedJobs)
        executingJobs = removeExecuted(executingJobs)
        candidateList = getCandidateList(project, makespan, finishedJobs, scheme)
        evaluateIncrementalCost(candidateList, makespan)
    sol.makespan = makespan
    return sol


# Método que obtiene la lista de candidatos
def getCandidateList(project, makespan, finishedJobs, scheme):
    cl = []
    if makespan == 0:
        cl.append(project.jobs[0])
    else:
        succFinished = getSucc(finishedJobs, project.succDicc, project.jobs, scheme)
        for job in succFinished:
            if isFactible(job, project.resources, finishedJobs, project.predDicc):
                cl.append(job)
    return cl


# Método que obtiene los sucesores de un job
def getSucc(finishedJobs, succDicc, jobs, scheme):
    succ = []
    for finishedJob in finishedJobs:
        succAux = succDicc[finishedJob.njob]
        for j in succAux:
            if jobs[j] not in scheme and jobs[j] not in succ:
                succ.append(jobs[j])
    return succ


# Método que comprueba si un job se puede ejecutar
def isFactible(job, resources, finishedJobs, predDicc):
    return alreadyPreds(job, finishedJobs, predDicc) and recNeeded(job, resources)


# Método que comprueba si los predecesores de un job han terminado de ejecutarse
def alreadyPreds(job, finishedJobs, predDicc):
    result = True
    predAux = predDicc[job.njob]
    for pred in predAux:
        if not finishedJobs.__contains__(pred):
            result = False
    return result


# Método que comprueba si los recursos que necesita para ejecutarse están disponibles
def recNeeded(job, resources):
    result = False
    neededQuant = job.resourceQuant
    if compareRecs(resources, neededQuant):
        result = True
    return result


def compareRecs(resources, neededQuant):
    result = True
    for i in range(0, len(resources)):
        if resources[i].quantity < neededQuant[i]:
            result = False
    return result


# Método que evalúa el coste incremental de ejecutar un job
def evaluateIncrementalCost(cl, makespan):
    for job in cl:
        job.incrementalCost = makespan + job.makespan


# Método que selecciona el siguiente de forma aleatoria
def selectNext(factibles):
    sig = None
    if factibles:
        sig = random.choice(factibles)
    return sig


# Método ejecuta las actividades en un timeStep
def executeActivity(makespan, project, job, executingJobs):
    job.executing = True
    job.initTime = makespan
    job.finishTime = makespan + job.makespan
    neededQuant = job.resourceQuant
    minusRecs(project, neededQuant)
    executingJobs.append(job)


def minusRecs(project, neededQuant):
    for i in range(0, len(project.resources)):
        project.resources[i].quantity = project.resources[i].quantity - neededQuant[i]


def plusRecs(project, neededQuant):
    for i in range(0, len(project.resources)):
        project.resources[i].quantity = project.resources[i].quantity + neededQuant[i]


# Método que obtiene las actividades que han termiando de ejecutarse
def getFinishedActivities(executingJobs, project, makespan, finishedActivities):
    for job in executingJobs:
        if makespan == job.finishTime and not job.finished:
            job.executing = False
            job.finished = True
            neededQuant = job.resourceQuant
            plusRecs(project, neededQuant)
            finishedActivities.append(job)


def removeExecuted(executingJobs):
    aux = []
    i = 0
    for job in executingJobs:
        aux.append(job)
    while i <= len(aux):
        job = aux.pop(0)
        if not job.finished:
            aux.append(job)
        i = i + 1
    return aux


# Método que obtiene el valor mínimo y máximo
def getMinMax(cl):
    costs = []
    for job in cl:
        costs.append(job.incrementalCost)
    return [min(costs), max(costs)]


# Método que obtiene la lista de restristed candidate list a través de la candidate list
def getRestrictedCandidateList(cl, minMax, alpha):
    rcl = []
    value = minMax[0] + alpha * (minMax[1] - minMax[0])
    for job in cl:
        if job.incrementalCost <= value:
            rcl.append(job)
    return rcl


def niceCost(job, minMax, alpha):
    result = False
    value = minMax[0] + alpha * (minMax[1] - minMax[0])
    if job.incrementalCost <= value:
        result = True
    return result


# Método que resetea el objeto Project para comenzar una nueva solución
def reset(project):
    for i in range(0, len(project.jobs)):
        job = project.jobs[i]
        job.executing = False
        job.finished = False
        job.initTime = 0
        job.finishTime = 0


# Método que inserta en el diccionario de recursos
def addEntryRecDicc(makespan, project):
    nres = []
    for rec in project.resources:
        nres.append(rec.quantity)
    project.resDicc[makespan] = nres
