import random

from src.Solution import Solution


# Método que contruye la solución
def constructGRS(project, alpha):
    reset(project)
    # Array que representa el esquema
    scheme = []
    # Project Duration Time
    duration = 0
    # Solution:
    sol = Solution(scheme, duration)
    # Variable que si se ha terminado el esquema
    finished = False
    # Finished jobs
    finishedJobs = []
    # Candidate List
    candidateList = getCandidateList(project, duration, finishedJobs, scheme)
    # Evaluate incremental cost
    evaluateIncrementalCost(candidateList, duration)
    while not finished:
        if candidateList:
            minMax = getMinMax(candidateList)
            restrictedCL = getRestrictedCandidateList(candidateList, minMax, alpha)
            sig = selectNext(restrictedCL)
            if sig is not None:
                scheme.append(sig)
        executeActivities(scheme, project, duration)
        if duration == 0 or len(finishedJobs) == 121:
            addEntryRecDicc(duration, project)
            getFinishActivities(scheme, project, duration, finishedJobs)
        duration = duration + 1
        addEntryRecDicc(duration, project)
        getFinishActivities(scheme, project, duration, finishedJobs)
        finished = len(finishedJobs) == len(project.jobs)
        candidateList = getCandidateList(project, duration, finishedJobs, scheme)
        evaluateIncrementalCost(candidateList, duration)
    sol.duration = duration
    return sol


# Método que obtiene la lista de candidatos
def getCandidateList(project, duration, finishedJobs, scheme):
    cl = []
    if duration == 0:
        cl.append(project.jobs[0])
    else:
        succFinished = getSucc(finishedJobs, project.succDicc, project.jobs, scheme)
        for job in succFinished:
            if isFactible(job, project.resources, scheme, project.predDicc):
                cl.append(job)
    return cl


# Método que obtiene los sucesores de un job
def getSucc(finishedJobs, succDicc, jobs, scheme):
    succ = []
    for finishedJob in finishedJobs:
        succAux = succDicc[finishedJob.njob]
        for j in succAux:
            if jobs[j] not in scheme:
                succ.append(jobs[j])
    return succ


# Método que comprueba si un job se puede ejecutar
def isFactible(job, resources, scheme, predDicc):
    return alreadyPreds(job, scheme, predDicc) and recNeeded(job, resources)


# Método que comprueba si los predecesores de un job han terminado de ejecutarse
def alreadyPreds(job, scheme, predDicc):
    result = True
    predAux = predDicc[job.njob]
    for pred in predAux:
        if not scheme.__contains__(pred):
            result = False
    return result


# Método que comprueba si los recursos que necesita para ejecutarse están disponibles
def recNeeded(job, resources):
    result = False
    neededRec = job.resourceType
    neededQuant = job.resourceQuant
    if resources[neededRec - 1].quantity >= neededQuant:
        result = True
    return result


# Método que evalúa el coste incremental de ejecutar un job
def evaluateIncrementalCost(cl, duration):
    for job in cl:
        job.incrementalCost = duration + job.duration


# Método que selecciona el siguiente de forma aleatoria
def selectNext(factibles):
    sig = None
    if factibles:
        sig = random.choice(factibles)
    return sig


# Método ejecuta las actividades en un timeStep
def executeActivities(scheme, project, duration):
    for job in scheme:
        if not job.finished and not job.executing:
            job.executing = True
            job.initTime = duration
            job.finishTime = duration + job.duration
            neededRec = job.resourceType
            neededQuant = job.resourceQuant
            project.resources[neededRec - 1].quantity = project.resources[neededRec - 1].quantity - neededQuant


# Método que obtiene las actividades que han termiando de ejecutarse
def getFinishActivities(scheme, project, duration, finishedActivities):
    for job in scheme:
        if duration == job.finishTime:
            job.executing = False
            job.finished = True
            neededRec = job.resourceType
            neededQuant = job.resourceQuant
            project.resources[neededRec - 1].quantity = project.resources[neededRec - 1].quantity + neededQuant
            finishedActivities.append(job)


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


# Método que obtiene que la lista de candidatos de forma más optimizada que la anterior
def getRestrictedCandidateListNew(cl):
    rcl = filter(niceCost, cl)
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
    print("Reset complete")


# Método que inserta en el diccionario de recursos
def addEntryRecDicc(duration, project):
    nres = []
    for rec in project.resources:
        nres.append(rec.quantity)
    project.resDicc[duration] = nres