from collections import defaultdict
import random


from people import attribNames 
from utils import makeWeightedRule, pickBest

from matching import Matchmaker,GenericApplicant,GenericTarget


class WorkerWrapper:
    def __init__(self,worker,rank):
        self.worker = worker
        self.attrib = {"rank":rank}


class WorkResult:
    def __init__(self,amt,source):
        self.amt = amt
        self.source = source

class JobAttribWrapper:
    def __init__(self,job):
        self.job = job
        self.attrib = job.prefWeights

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
    

def assignJobs(people,jobs):
    applicants = [GenericApplicant(p,p.attrib,attribNames) for p in people]
    targets = [GenericTarget(30,j,defaultdict(int,[[x,y] for y,x in j.prefWeights])) for j in jobs]
    m = Matchmaker()
    m.match(applicants,targets)
    for a in applicants:
        if a.selected:
            a.obj.setJob(a.selected[0].obj)
            
farmJob = Job("farmer",level=1,prefWeights=[[1,"body"],[1,"strength"]],attribWeights=[[1,"body"],[1,"strength"]])
hunterJob = Job("hunter",level=1,prefWeights=[[1,"dex"],[1,"strength"]],attribWeights=[[1,"dex"],[1,"strength"]])
craftJob = Job("crafter",level=1,prefWeights=[[1,"intelligence"],[1,"strength"]],attribWeights=[[1,"intelligence"],[1,"strength"]])
servantJob = Job("serveant",level=1,prefWeights=[[1,"charisma"],[1,"will"]],attribWeights=[[1,"charisma"],[1,"will"]])
soldierJob = Job("soldier",level=1,prefWeights=[[1,"will"],[1,"strength"]],attribWeights=[[1,"will"],[1,"body"]])
entertainerJob = Job("entertainer",level=1,prefWeights=[[1,"charisma"],[1,"dex"]],attribWeights=[[1,"charisma"],[1,"dex"]])

jobList = [farmJob,hunterJob,craftJob,servantJob,soldierJob,entertainerJob]
jobPickList = dict([[job.name,JobAttribWrapper(job)] for job in jobList])
