import random

from utils import pickBest, makeRule, makeWeightedRule, makeWeightedAddRule
from people import Person,reaper,court
from job import Job


class Town(object):
    def __init__(self,name):
        self.name = name
        self.pop = reaper([Person() for _ in xrange(64)])
        self.pickInitialJobs()

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
        court(men,women)
        

if __name__ == "__main__":
    t = Town("Sandwich")
    
