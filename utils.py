from collections import defaultdict
from operator import mul,add
#from functools import reduce #uncomment for python3
import random
import itertools

class RNGTester:
    def __init__(self,ndie,sides):
        if ndie <= 0:
            raise ValueError("RNGTester","need positive number of dice")
        if sides <= 0:
            raise ValueError("RNGTester","need positive number of sides")
        self.ndie = ndie
        self.sides = sides
        r = range(1,sides+1)
        self.combo = [r]*ndie
        self.generator = self.gen()
    def randint(self,low,high):
        if low != 1 or high != self.sides:
            raise ValueError("randint","randint should be from 1 to %d, not %d to %d" % (self.sides,low,high))
        return next(self.generator)
    def gen(self):
        while True:
            for c in itertools.product(*self.combo):
                for v in c:
                    yield v


def pickBest(alist,metric,n=1,picker=None):
    if len(alist) < n:
        if len(alist) > 0:
            random.shuffle(alist)
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
    return lambda x,p=None: reduce(mul,[x.attrib[a] for a in attribs])

def makeWeightedRule(weighted_attribs):
    return lambda x,p=None: reduce(mul,[x.attrib[a[1]]*a[0] for a in weighted_attribs])

def makeWeightedAddRule(weighted_attribs):
    return lambda x,p=None: reduce(add,[x.attrib[a[1]]*a[0] for a in weighted_attribs])
