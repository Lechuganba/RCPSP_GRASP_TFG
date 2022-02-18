

class GreedyRandSol:

    def __init__(self, nparticles):
        # Número de partículas del enjambre
        self.nparticles = nparticles
        # Inizializamos la mejor solución global
        self.globalBest = None
        # Array de partículas
        self.particles = []

    def initializeSwarm(self, project):
        # Algoritmo que inicializa las partículas
        n = 0
        # Tenemos que generar partículas que sean soluciones válidas
        while n != self.nparticles:
            # Generamos la partícula
            particle = Particle()
            ps = self.pararellScheme(particle, project)
            print("Particula creada correctamente")
            self.particles.append([particle, ps])
            n = n + 1
        # return self.particlesS

    def pararellScheme(self, particle, project):
        self.reset(project)
        # Array que representa el esquema
        scheme = []
        # Earliest Finish Time
        duration = 0
        # Variable que si se ha terminado el esquema
        finished = False
        # Número de actividades terminadas
        nJobsFinished = 0
        finishedActivities = []
        while not finished:
            factibles = self.getFactibles(scheme, particle, project)
            posSig = self.selectNext(particle, factibles)
            if posSig is not None:
                sig = project.jobs[posSig]
                scheme.append(sig)
                factibles.remove(sig)
            self.executeActivities(scheme, project, duration)
            self.getFinishActivities(scheme, project, duration, finishedActivities)
            finished = len(finishedActivities) == len(particle.position)
            duration = duration + 1
        return scheme

    def reset(self, project):
        for i in range(0, len(project.jobs)):
            job = project.jobs[i]
            job.executing = False
            job.finished = False
            job.initTime = 0
            job.finishTime = 0
        # print("Reset complete")

    def executeActivities(self, scheme, project, duration):
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

    def getFinishActivities(self, scheme, project, duration, finishedActivities):
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

    def selectNext(self, particle, factibles):
        sig = None
        if factibles:
            prios = self.orderPrios(factibles, particle)
            biggerPrio = prios[0]
            sig = particle.position.index(biggerPrio)
        return sig

    def getFactibles(self, scheme, particle, project):
        factibles = []
        printFactibles = []
        for i in range(0, len(particle.position)):
            job = project.jobs[i]
            preds = self.findPred(i, project.jobs)
            if self.isFactible(job, preds, scheme, project.resources):
                factibles.append(job)
                # printFactibles.append(job.njob)
        return factibles

    def isFactible(self, job, preds, scheme, resources):
        factible = False
        if job not in scheme:
            factible = self.alreadyPreds(preds, scheme) and self.hayRecursos(job, resources)
        return factible

    def alreadyPreds(self, preds, scheme):
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

    def hayRecursos(self, job, resources):
        result = False
        neededRec = job.resourceType
        neededQuant = job.resourceQuant
        # print("Comprobando recursos de: ", job.njob)
        if resources[neededRec - 1].quantity >= neededQuant:
            result = True
        return result

    def orderPrios(self, factibles, particle):
        prios = []
        for i in range(0, len(factibles)):
            prio = particle.position[factibles[i].njob]
            prios.append(prio)
        prios.sort(reverse=True)
        return prios

    def findPred(self, activity, jobs):
        result = []
        for i in range(0, len(jobs)):
            j = jobs[i]
            succs = []
            for k in range(0, len(j.succ)):
                succs.append(j.succ[k])
            if succs.__contains__(activity):
                result.append(j)
        return result

    ######################## NO ES ASÍ ##############################
    def achieveRestrictions(self, particle, jobs):
        result = 0
        aP = self.achievePriority(particle, jobs)
        aRR = self.achieveResourcesRestrictions(particle)
        if aP == 1 or aRR == 1:
            result = 1
        return result

    def achievePriority(self, particle, jobs):
        result = 0
        oragnizedActivities = self.organizeActivities(particle.position)
        # Comprobamos las restricciones de prioridad
        organized = self.comprobatePriority(oragnizedActivities, jobs)
        if organized == 1:
            result = 1
        return result

    def organizeActivities(self, positions):
        particlePosAux = []
        for i in range(0, len(positions)):
            particlePosAux.append(positions[i])
        particlePosAux.sort(reverse=True)
        result = []
        for i in range(0, len(particlePosAux)):
            elem = particlePosAux[i]
            p = positions.index(elem)
            result.append(p)
        return result

    def comprobatePriority(self, organizedActivities, jobs):
        result = 0
        i = 0
        while result == 0 and i < len(organizedActivities):
            activity = organizedActivities[i]
            job = jobs[activity]
            aP = self.afterPred(activity, jobs, organizedActivities)
            bS = self.beforeSucc(activity, job, organizedActivities)
            if bS == 0 and aP == 0:
                i = i + 1
            else:
                result = 1
        return result

    def afterPred(self, activity, jobs, organizedActivities):
        result = 0
        preds = self.findPred(activity, jobs)
        i = 0
        while result == 0 and i < len(preds):
            p = preds[i]
            # indexPred = organizedActivities.index(p)
            indexAct = organizedActivities.index(activity)
            indexPred = organizedActivities.index(p)
            if indexPred > indexAct:
                result = 1
            else:
                i = i + 1
        return result

    def beforeSucc(self, activity, job, organizedActivities):
        result = 0
        i = 0
        while result == 0 and i < job.nsuccesors:
            s = job.succ[i]
            indexAct = organizedActivities.index(activity)
            indexSuc = organizedActivities.index(s)
            if indexAct > indexSuc:
                result = 1
            else:
                i = i + 1
        return result

    def achieveResourcesRestrictions(self, particle):
        result = 0
        return result
