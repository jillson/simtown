import random
import sys
from collections import defaultdict
from utils import pickBest,makeWeightedRule
        
#TODO: replace this with a list of lastnames or a generator for same
class Family(object):
    ID=0
    def __init__(self):
        self.name="Family%d"%Family.ID
        self.id = Family.ID
        Family.ID+= 1

class Gene:
    def __init__(self,name):
        self.name = name

attribNames = ["body","strength","dex","intelligence","charisma","will"]
genes = [Gene(x) for x in attribNames]

        
#This may want to go in its own class with crazy patterns and stuff but for now
def court(men,women):
    #filter out marriaged people
    men = dict([[man,[]] for man in men if not man.spouse])
    women = [man for man in women if not man.spouse]
    wooed = defaultdict(list)
    for man in men:
        men[man] = pickBest(women,makeWeightedRule([[man.__dict__[a],a] for a in attribNames]),len(women))
        wooed[men[man][0]].append(man)
    rejected = []
    previousRejected = []
    toReject = max(0,len(men) - len(women))
    while True:
        
        #print "Debug: men's ranking:"
        #for m in men:
        #    print m.name,[f.name for f in men[m]]
        #print "Debug: wooed list:"
        #for w in wooed:
        #    print w.name,[m.name for m in wooed[w]]
        #print "We will expect %d men to get rejected" % (toReject)
    

        for woman in wooed:
            if len(wooed[woman]) <= 1:
                #print "This woman (%s) has %d suitor(s)" % (woman.name,len(wooed[woman]))
                continue
            best = pickBest(wooed[woman],makeWeightedRule([[woman.__dict__[a],a] for a in attribNames]))[0]
            for m in wooed[woman]:
                if m != best:
                    men[m].pop(0)
                    rejected.append(m)
            wooed[woman] = [best]
        rejected = set(rejected)
        #NOTE: bug ... should modify so it requires that the rejected list be the same as the previous iteration
        if len(rejected) <= toReject and rejected == previousRejected:
            break
        for r in rejected:
            if len(men[r]) > 0:
                wooed[men[r][0]].append(r)
                #print "Debug... rejected:",r.name
            #else:
                #print "%s ran out of folks to ask" % r.name
        previousRejected = rejected
        rejected = []
    for woman in wooed:
        if wooed[woman]:
            wooed[woman][0].marry(woman)
        

class Person(object):
    ID=0
    def __init__(self,parents=None):
        self.name=Person.ID
        Person.ID+=1
        if parents:
            self.mate(*parents)
            self.parents = parents
            self.family = parents[0].family
            self.age = 0
        else:
            self.generate()
            self.family = Family()
        self.gender = random.choice("MF")
        self.get_stats()
        self.job = None
        self.spouse = None

    def setJob(self,newJob):
        if self.job:
            self.job.removeWorker(self)
        if newJob:
            newJob.addWorker(self)
        self.job = newJob

    def marry(self,spouse):
        if not self.spouse and not spouse.spouse and spouse.gender != self.gender:
            self.spouse = spouse
            self.spouse.spouse = self

    def divorce(self):
        if self.spouse:
            self.spouse.spouse = None
            self.spouse = None

    def mate(self,p1,p2):
        p1_picked = random.sample(p1.genes,7)
        p2_picked = random.sample(p2.genes,7)
        self.genes = p1_picked + p2_picked

    def generate(self):
        self.age = random.randint(16,32)
        self.genes = genes + [random.choice(genes) for _ in xrange(8)]

    def get_stats(self):
        self.body = 0
        self.strength = 0
        self.dex = 0
        self.intelligence = 0
        self.charisma = 0
        self.will = 0
        for g in self.genes:
            self.__dict__[g.name]+=1
        self.__dict__[random.choice(genes).name]+=1
    def viable(self):
        return self.body > 0 and self.strength > 0 and self.dex > 0 and self.intelligence > 0 and self.charisma > 0 and self.will > 0
    def print_stats(self,out=sys.stdout):
        out.write("%d:%d:%d:%d:%d:%d"%(self.body,self.strength,self.dex,self.intelligence,self.charisma,self.will))
    def json(self):
        return dict([[v,self.__dict__[v]] for v in ["name","age","gender"] + attribNames])

def simple_next_gen(population,out=sys.stdout):
    nextPop = []
    stillborn = 0
    for i in xrange(len(population)//2):
        for _ in xrange(random.randint(2,5)):
            kid = Person([population[i*2],population[i*2+1]])
            if kid.viable():
                nextPop.append(kid)
            else:
                stillborn += 1
    out.write("We had %d folks die off at birth and %d new kids" % (stillborn,len(nextPop)))
    random.shuffle(nextPop)
    return nextPop

def reaper(alist):
    return [a for a in alist if a.viable()]

if __name__ == '__main__': # pragma: no cover
    population=[Person() for _ in xrange(32)]
    deadPool = [p for p in population if not p.viable()]
    print "We had %d folks die off at the beginning" % len(deadPool)
    for d in deadPool:
        population.remove(d)

    for p in population:
        p.print_stats()

    for gen in xrange(20):
        population = simple_next_gen(population)

    for p in population:
        p.print_stats()



