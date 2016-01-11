from collections import defaultdict
from operator import mul,add
#from functools import reduce #uncomment for python3
import random

from people import Person,reaper


def pickBest(alist,metric,n=1,picker=None):
    if len(alist) <= n:
        return alist
    mdict = defaultdict(list)
    rez = []
    for p in alist:
        mdict[metric(p,picker)].append(p)
    while(len(rez) < n):
        bestMetric = max(mdict.keys())
        foo = mdict[bestMetric]
        random.shuffle(foo)
        rez += foo
        mdict.pop(bestMetric)
    return rez[:n]

#TODO: make this be handle p
def makeRule(attribs):
    return lambda x,p=None: reduce(mul,[x.__dict__(a) for a in attribs])

def makeWeightedRule(weighted_attribs):
    return lambda x,p=None: reduce(mul,[x.__dict__[a[1]]*a[0] for a in weighted_attribs])

def makeWeightedAddRule(weighted_attribs):
    return lambda x,p=None: reduce(add,[x.__dict__[a[1]]*a[0] for a in weighted_attribs])

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
        #TODO: allow king to order priorites based on his traits
        
        
        

if __name__ == "__main__":
    t = Town("Sandwich")
    
