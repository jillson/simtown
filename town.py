import random

from utils import pickBest, makeRule, makeWeightedRule, makeWeightedAddRule
from people import Person,reaper



class Town(object):
    def __init__(self,name):
        self.name = name
        self.pop = reaper([Person() for _ in xrange(64)])
        self.pickInitialJobs()

    def pickInitialJobs(self):
        men = [p for p in self.pop if p.gender == "M"]
        women = [p for p in self.pop if p.gender == "F"]
        print "Check, out of %d people we had %d men and %d women" % (len(self.pop),len(men),len(women))
        #TODO: do we want to have women "kings" or how to handle?
        self.king = pickBest(men,makeWeightedRule([[1,"charisma"],[2,"intelligence"],[3,"strength"]]))[0]
        self.king.job = "king"
        men.remove(self.king)
        self.queen = pickBest(women,makeWeightedAddRule([[2,"charisma"],[2,"intelligence"],[-0.1,"age"],[1,"body"]]))[0]
        self.queen.job = "queen"
        women.remote(self.queen)
        #TODO: allow king to order priorites based on his traits
        commander = pickBest(men,makeWeightedRule([[1,"charisma"],[2,"strength"],[2,"body"],[1,"intelligence"]]))[0]
        men.remove(commander)
        priest = pickBest(men,makeWeightedRule([[2,"charisma"],[2,"intelligence"],[1,"age"]]))[0]
        men.remove(priest)
        headfarmers = pickBest(men,makeWeightedRule([[1,"charisma"],[2,"strength"],[2,"body"],[1,"intelligence"]]),4)
        
        

if __name__ == "__main__":
    t = Town("Sandwich")
    
