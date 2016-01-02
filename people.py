import random

#TODO: replace this with a list of lastnames or a generator for same
class Family:
    ID=0
    def __init__(self):
        self.name="Family%d"%Family.ID
        self.id = Family.ID
        Family.ID+= 1

class Gene:
    def __init__(self,name):
        self.name = name

genes = [Gene(x) for x in ["body","strength","dex","intelligence","charisma","will"]]

class Person:
    def __init__(self,parents=None):
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
    def print_stats(self):
        print("%d:%d:%d:%d:%d:%d"%(self.body,self.strength,self.dex,self.intelligence,self.charisma,self.will))

def simple_next_gen(population):
    nextPop = []
    stillborn = 0
    for i in xrange(len(population)//2):
        for _ in xrange(random.randint(2,5)):
            kid = Person([population[i*2],population[i*2+1]])
            if kid.viable():
                nextPop.append(kid)
            else:
                stillborn += 1
    print "We had %d folks die off at birth and %d new kids" % (stillborn,len(nextPop))
    random.shuffle(nextPop)
    return nextPop

        

if __name__ == '__main__':
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



