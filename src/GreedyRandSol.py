import random

from src.Solution import Solution


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


def getSucc(finishedJobs, succDicc, jobs, scheme):
    succ = []
    for finishedJob in finishedJobs:
        succAux = succDicc[finishedJob.njob]
        for j in succAux:
            if jobs[j] not in scheme:
                succ.append(jobs[j])
    return succ


def isFactible(job, resources, scheme, predDicc):
    return alreadyPreds(job, scheme, predDicc) and recNeeded(job, resources)


def alreadyPreds(job, scheme, predDicc):
    result = True
    predAux = predDicc[job.njob]
    for pred in predAux:
        if not scheme.__contains__(pred):
            result = False
    return result


def recNeeded(job, resources):
    result = False
    neededRec = job.resourceType
    neededQuant = job.resourceQuant
    # print("Comprobando recursos de: ", job.njob)
    if resources[neededRec - 1].quantity >= neededQuant:
        result = True
    return result


def evaluateIncrementalCost(cl, duration):
    for job in cl:
        job.incrementalCost = duration + job.duration


def selectNext(factibles):
    sig = None
    if factibles:
        sig = random.choice(factibles)
    return sig


def executeActivities(scheme, project, duration):
    for job in scheme:
        if not job.finished and not job.executing:
            job.executing = True
            job.initTime = duration
            job.finishTime = duration + job.duration
            neededRec = job.resourceType
            neededQuant = job.resourceQuant
            project.resources[neededRec - 1].quantity = project.resources[neededRec - 1].quantity - neededQuant


def getFinishActivities(scheme, project, duration, finishedActivities):
    for job in scheme:
        if duration == job.finishTime:
            job.executing = False
            job.finished = True
            neededRec = job.resourceType
            neededQuant = job.resourceQuant
            project.resources[neededRec - 1].quantity = project.resources[neededRec - 1].quantity + neededQuant
            finishedActivities.append(job)


def getMinMax(cl):
    costs = []
    for job in cl:
        costs.append(job.incrementalCost)
    return [min(costs), max(costs)]


def getRestrictedCandidateList(cl, minMax, alpha):
    rcl = []
    value = minMax[0] + alpha * (minMax[1] - minMax[0])
    for job in cl:
        if job.incrementalCost <= value:
            rcl.append(job)
    return rcl


def getRestrictedCandidateListNew(cl):
    rcl = filter(niceCost, cl)
    return rcl


def niceCost(job, minMax, alpha):
    result = False
    value = minMax[0] + alpha * (minMax[1] - minMax[0])
    if job.incrementalCost <= value:
        result = True
    return result


def reset(project):
    for i in range(0, len(project.jobs)):
        job = project.jobs[i]
        job.executing = False
        job.finished = False
        job.initTime = 0
        job.finishTime = 0
    print("Reset complete")


def addEntryRecDicc(duration, project):
    nres = []
    for rec in project.resources:
        nres.append(rec.quantity)
    project.resDicc[duration] = nres