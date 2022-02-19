import random

from src.Solution import Solution


def generateGRS(project, seed):
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
    finishedActivities = []
    # Candidate List
    candidateList = getCandidateList(scheme, project)
    # Evaluate incremental cost
    evaluateIncrementalCost(candidateList)
    while not finished:
        restrictedCL = getRestrictedCandidateList(candidateList)
        sig = selectNext(restrictedCL, seed)
        if sig is not None:
            scheme.append(sig)
            candidateList.remove(sig)
        executeActivities(scheme, project, duration)
        getFinishActivities(scheme, project, duration, finishedActivities)
        finished = len(finishedActivities) == len(project.jobs)
        duration = duration + 1
        candidateList = getCandidateList(scheme, project)
        evaluateIncrementalCost(candidateList)
    sol.duration = duration
    return sol


def getCandidateList(solution, project):
    factibles = []
    # printFactibles = []
    for i in range(0, len(project.jobs)):
        job = project.jobs[i]
        preds = findPred(i, project.jobs)
        if isFactible(job, preds, solution, project.resources):
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
        factible = alreadyPreds(preds, scheme) and hayRecursos(job, resources)
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


def hayRecursos(job, resources):
    result = False
    neededRec = job.resourceType
    neededQuant = job.resourceQuant
    # print("Comprobando recursos de: ", job.njob)
    if resources[neededRec - 1].quantity >= neededQuant:
        result = True
    return result


def selectNext(factibles, seed):
    sig = None
    if factibles:
        # Aleatorio entre la lista de factibles
        sig = random.choice(factibles)
    return sig


def executeActivities(scheme, project, duration):
    for i in range(0, len(scheme)):
        job = scheme[i]
        if not job.finished and not job.executing:
            job.executing = True
            # print("Executing job: ", job.njob)
            job.initTime = duration
            job.finishTime = duration + job.duration
            neededRec = job.resourceType
            neededQuant = job.resourceQuant
            project.resources[neededRec - 1].quantity = project.resources[neededRec - 1].quantity - neededQuant


def getFinishActivities(scheme, project, duration, finishedActivities):
    for i in range(0, len(scheme)):
        job = scheme[i]
        if duration == job.finishTime:
            job.executing = False
            job.finished = True
            # print("Finished job: ", job.njob)
            neededRec = job.resourceType
            neededQuant = job.resourceQuant
            project.resources[neededRec - 1].quantity = project.resources[neededRec - 1].quantity + neededQuant
            finishedActivities.append(job)


def getRestrictedCandidateList(candidateList):
    return candidateList


def reset(project):
    for i in range(0, len(project.jobs)):
        job = project.jobs[i]
        job.executing = False
        job.finished = False
        job.initTime = 0
        job.finishTime = 0
    print("Reset complete")


def evaluateIncrementalCost(candidateList):
    return 0
