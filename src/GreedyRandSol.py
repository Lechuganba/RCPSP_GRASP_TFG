import random

from src.Solution import Solution


def constructGRS(project, alphaAux):
    global minMax
    global alpha
    alpha = alphaAux
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
    candidateList = getCandidateListNew(project, duration, finishedJobs, scheme)
    # Evaluate incremental cost
    evaluateIncrementalCost(candidateList, duration)
    while not finished:
        if candidateList:
            minMax = getMinMax(candidateList)
            restrictedCL = getRestrictedCandidateList(candidateList)
            sig = selectNext(restrictedCL)
            if sig is not None:
                scheme.append(sig)
        executeActivities(scheme, project, duration)
        getFinishActivities(scheme, project, duration, finishedJobs)
        finished = len(finishedJobs) == len(project.jobs)
        duration = duration + 1
        candidateList = getCandidateListNew(project, duration, finishedJobs, scheme)
        evaluateIncrementalCost(candidateList, duration)
    sol.duration = duration
    return sol


def getCandidateListNew(project, duration, finishedJobs, scheme):
    cl = []
    if duration == 0:
        cl.append(project.jobs[0])
    else:
        succFinished = getSucc(finishedJobs, project.succDicc, project.jobs)
        for job in succFinished:
            if isFactibleNew(job, project.resources) and job not in scheme:
                cl.append(job)
    return cl


def getSucc(finishedJobs, succDicc, jobs):
    succ = []
    for finishedJob in finishedJobs:
        succAux = succDicc[finishedJob.njob]
        for j in succAux:
            succ.append(jobs[j])
    return succ


def isFactibleNew(job, resources):
    return recNeeded(job, resources)


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
    minC = min(costs)
    maxC = max(costs)
    return [minC, maxC]


def getRestrictedCandidateList(cl):
    rcl = []
    for job in cl:
        if niceCost(job):
            rcl.append(job)
    return rcl


def getRestrictedCandidateListNew(cl):
    rcl = filter(niceCost, cl)
    return rcl


def niceCost(job):
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


####### OLD ######

def getCandidateList(scheme, project):
    factibles = []
    for i in range(0, len(project.jobs)):
        job = project.jobs[i]
        preds = findPred(i, project.jobs)
        if isFactible(job, preds, scheme, project.resources):
            factibles.append(job)
            # printFactibles.append(job.njob)
    return factibles


def findPred(activity, jobs):
    result = []
    for i in range(0, len(jobs)):
        j = jobs[i]
        succs = []
        for k in range(0, len(j.succ)):
            succs.append(j.succ[k])
        if succs.__contains__(activity):
            result.append(j)
    return result


def isFactible(job, preds, scheme, resources):
    factible = False
    if job not in scheme:
        factible = alreadyPreds(preds, scheme) and recNeeded(job, resources)
    return factible


def alreadyPreds(preds, scheme):
    result = True
    i = 0
    while result and i < len(preds):
        if preds[i] not in scheme:
            result = False
        i = i + 1
    for j in range(0, len(preds)):
        if not preds[j].finished:
            result = False
    return result
