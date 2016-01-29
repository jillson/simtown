import random
import sys
from collections import defaultdict
from utils import pickBest,makeWeightedRule

DEBUG=False

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

class Skill:
    def __init__(self,name,attrib):
        self.name = name
        self.attrib = attrib

skillDict = dict([[s.name,s] for s in [Skill("farming","body"),
             Skill("melee","strength"),
             Skill("archery","dex"),
             Skill("reading","intelligence"),
             Skill("diplomacy","charisma"),
             Skill("leadership","charisma"),
             Skill("skulduggery","dex"),
             Skill("athletics","strength")]])

        
class AttributeMap:
    def __init__(self,initialAttribs=None):
        if initialAttribs:
            self.attribs=dict([[a,0] for a in initialAttribs])
        else:
            self.attribs = {}
        self.skills = {}
    def __getitem__(self,key):
        if key in self.attribs:
            return self.attribs[key]
        if key in skillDict:
            sk = skillDict[key]
            skillRanks = self.skills.get(key,0)
            attribBonus = self.attribs.get(sk.attrib,0)
            return skillRanks + attribBonus
        return 0
    def __setitem__(self,key,value):
        if key in skillDict:
            self.skills[key] = value
        else:
            self.attribs[key] = value
    def __delitem__(self,key):
        print "Who called delitem for ",key
        pass
    def __repr__(self):
        return "Stats: " + str(self.attribs) + ", Skills: " + str(self.skills)
        


        
#This may want to go in its own class with crazy patterns and stuff but for now
def court(men,women):
    #filter out marriaged people
    men = dict([[man,[]] for man in men if not man.spouse])
    women = [man for man in women if not man.spouse]
    wooed = defaultdict(list)
    for man in men:
        men[man] = pickBest(women,makeWeightedRule([[man.attrib[a],a] for a in attribNames]),len(women))
        wooed[men[man][0]].append(man)
    rejected = []
    previousRejected = []
    toReject = max(0,len(men) - len(women))
    while True:

        if DEBUG:
            print "Debug: men's ranking:"
            for m in men:
                print m.name,[f.name for f in men[m]]
            print "Debug: wooed list:"
            for w in wooed:
                print w.name,[m.name for m in wooed[w]]
            print "We will expect %d men to get rejected" % (toReject)
    

        for woman in wooed:
            if len(wooed[woman]) <= 1:
                #print "This woman (%s) has %d suitor(s)" % (woman.name,len(wooed[woman]))
                continue
            best = pickBest(wooed[woman],makeWeightedRule([[woman.attrib[a],a] for a in attribNames]))[0]
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
        self.attrib = AttributeMap()
        Person.ID+=1
        if parents:
            self.mate(*parents)
            self.parents = parents
            self.family = parents[0].family
            self.attrib["age"] = 0
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
        self.attrib["age"] = random.randint(16,32)
        self.genes = genes + [random.choice(genes) for _ in xrange(8)]

    def get_stats(self):
        for g in self.genes:
            self.attrib[g.name]+=1
        self.attrib[random.choice(genes).name]+=1
    def viable(self):
        return all([self.attrib[x] > 0 for x in attribNames])
    def print_stats(self,out=sys.stdout):
        out.write(":".join([str(self.attrib[a]) for a in attribNames]))
    def json(self):
        return {"name":self.name,
                "gender":self.gender,
                "attributes":self.attrib}

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



