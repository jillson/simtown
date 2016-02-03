import random
from collections import defaultdict

from utils import pickBest, makeRule, makeWeightedRule, makeWeightedAddRule
from people import Person,reaper,court
from job import Job

class Building(object):
    def __init__(self,name):
        self.name = name

defaultBuildings = ["TownHall","StoreHouse","Garrison","Chapel"]
        
buildingDict = dict([[name,Building(name)] for name in defaultBuildings])



#class Event(object):
#    pass

#class OrcAttackEvent(Event):
#    def __init__(self):
#        pass
#    def calculateNumber(self):
#        return min(10,int(random.lognormvariate(0,0.5)))
#    def findResults(self,aTown):
#        pass

class Town(object):
    def __init__(self,name):
        self.name = name
        self.pop = reaper([Person() for _ in xrange(64)])
        self.pickInitialJobs()
        self.buildings = dict([[name,buildingDict[name]] for name in defaultBuildings])
        self.eventHandlerMap = {"birth":self.handleBirths,
                                "death":self.handleDeaths,
                                "work":self.handleWork}

    def handleBirths(self,birthObjs):
        self.pop += reaper(birthObjs)

    def handleDeaths(self,deathObjs):
        for deadPerson in set(deathObjs):
            self.pop.remove(deadPerson)

    def handleWork(self,workObjs):
        workTypes = defaultdict(int)
        for work in workObjs:
            workTypes[work.source] += work.amt
        print "Shoudl do something with ", workTypes

    def pickInitialJobs(self):
        self.jobs = {}
        self.jobs["king"] = Job(name="king",level=1000,prefWeights=[1],attribWeights=[["age",1]])
        self.jobs["queen"] = Job(name="queen",level=1000,prefWeights=[1],attribWeights=[["age",1]])  
        
        men = [p for p in self.pop if p.gender == "M"]
        women = [p for p in self.pop if p.gender == "F"]
        print "Check, out of %d people we had %d men and %d women" % (len(self.pop),len(men),len(women))
        #TODO: do we want to have women "kings" or how to handle?
        self.king = pickBest(men,makeWeightedRule([[1,"charisma"],[2,"intelligence"],[3,"strength"]]))[0]
        self.king.setJob(self.jobs["king"])
        men.remove(self.king)
        self.queen = pickBest(women,makeWeightedAddRule([[2,"charisma"],[2,"intelligence"],[-0.1,"age"],[1,"body"]]))[0]
        self.queen.setJob(self.jobs["queen"])
        women.remove(self.queen)
        self.king.marry(self.queen)
        #TODO: allow king to order priorites based on his traits
        leaders = []
        for name,attribsZipped  in [
                ["commander",[[1,"charisma"],[2,"strength"],[2,"body"],[1,"intelligence"]]],
                ["priest",[[2,"charisma"],[2,"intelligence"],[1,"age"]]],
                ["foreman",[[1,"charisma"],[2,"strength"],[2,"body"],[1,"intelligence"]]]]:
            guy = pickBest(men,makeWeightedRule(attribsZipped))[0]
            self.__dict__[name] = guy
            men.remove(guy)
            newJob = Job(name=name,level=500,prefWeights=[],attribWeights=attribsZipped)
            self.jobs[name] = newJob
            guy.setJob(newJob)
            leaders.append(guy)

        court(men+leaders,women)
        self.men = men+leaders+[self.king]
        self.women = women+[self.queen]

    def getEvents(self):
        events = defaultdict(list)
        for p in self.pop:
            pevents = p.turn()
            for k in pevents:
                events[k] += pevents[k]
        return events

    def handleEvents(self,events):
        for eventType in events:
            eh = self.eventHandlerMap.get(eventType)
            if eh:
                eh(events[eventType])
            else:
                print "Warning, we haven't implemented ",eventType
    
    def turn(self):
        self.handleEvents(self.getEvents())

        
        

if __name__ == "__main__": # pragma: no cover
    t = Town("Sandwich")
    
