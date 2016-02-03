from collections import defaultdict
import random


from people import attribNames 
from utils import makeWeightedRule, pickBest

class WorkerWrapper:
    def __init__(self,worker,rank):
        self.worker = worker
        self.attrib = {"rank":rank}


class WorkResult:
    def __init__(self,amt,source):
        self.amt = amt
        self.source = source

class Job:
    def __init__(self,name,level,prefWeights,attribWeights):
        self.name = name
        self.level = level
        self.attribWeights = attribWeights
        self.prefWeights = prefWeights
        self.workers = []
        self.rule = makeWeightedRule(attribWeights)
    def addWorker(self,worker):
        self.workers.append(WorkerWrapper(worker,self.rank(worker)))
    def removeWorker(self,worker):
        ww = None
        for x in self.workers:
            if x.worker == worker:
                ww = x
        if ww:
            self.workers.remove(ww)

    def rejectWorst(self,maxToKeep):
        worstList = pickBest(self.workers,makeWeightedRule([(-1,"rank")]),n=len(self.workers)-maxToKeep)
        for fired in worstList:
            fired.worker.setJob(None)

    def rank(self,worker):
        return self.rule(worker)
                                     
    def calcPreference(self,attribs):
        aRank = sum([a[0]*a[1] for a in zip(attribs,self.prefWeights)])
        return aRank + self.level * 10

    def turn(self,person):
        attribToCheck = random.choice(self.attribWeights)[1]
        rez = person.roll(attribToCheck)
        return {"work":[WorkResult(rez,self.name)]}
    
    
