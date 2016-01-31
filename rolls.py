import random
from collections import defaultdict
import sys

sigma = float(sys.argv[1])
vals = defaultdict(int)

for _ in xrange(10000):
    x = min(10,int(random.lognormvariate(0,sigma)))
    vals[x] += 1

for k in vals:
    print k,vals[k]

