class Job:

    def __init__(self, numbers, dyr):
        self.njob = numbers[0] - 1
        self.nsuccesors = numbers[2]
        self.succ = numbers[3:len(numbers)]
        for i in range(0, len(self.succ)):
            self.succ[i] = self.succ[i] - 1
        self.duration = dyr[0]
        self.resourceQuant = dyr[1]
        self.resourceType = dyr[2]
        self.initTime = 0
        self.finishTime = 0
        self.finished = False
        self.executing = False
        self.incrementalCost = 0
