
import unittest
try: #python 3.3's unittest.mock backported in separate mock for Python 2
    from unittest.mock import patch
except ImportError:
    from mock import patch

from StringIO import StringIO
from collections import defaultdict


from job import Job
from people import Person, attribNames

class FakePerson:
    def __init__(self):
        self.job = None
        self.attrib = defaultdict(int)
    def setJob(self,job):
        if self.job:
            self.job.removeWorker(self)
        if job:
            job.addWorker(self)
        self.job = job


allOnes = [1]*len(attribNames)
allOnesZipped = zip(allOnes,attribNames)
allMixed = range(1,len(attribNames)+1)
allMixedZipped = zip(allMixed,attribNames)

class TestJob(unittest.TestCase):
    def setUp(self):
        self.job = Job(name="testjob",level=1,prefWeights=allOnes,attribWeights=allOnesZipped)
        self.job2 = Job(name="testjob",level=1,prefWeights=allMixed,attribWeights=allMixedZipped)
    def testPreferences(self):
        m = self.job.calcPreference([1,2,3,4,5,6])
        self.assertEqual(m,31)
        self.job.level = 2
        m = self.job.calcPreference([1,2,3,4,5,6])
        self.assertEqual(m,41)
        m = self.job2.calcPreference([1,2,3,4,5,6])
        self.assertEqual(m,10+1+4+9+16+25+36)
    def testHireFireWorkers(self):
        p1 = FakePerson()
        j = self.job
        j2 = self.job2
        self.assertEqual(0,len(j.workers))
        j.removeWorker(p1) #implicit assert that this doesn't throw an exception
        j.addWorker(p1)
        self.assertEqual(1,len(j.workers))
        self.assertEqual(0,len(j2.workers))
        self.assertEqual(p1.job,None)
        j.removeWorker(p1)
        self.assertEqual(p1.job,None)
        self.assertEqual(0,len(j.workers))
        p1.setJob(j)
        self.assertEqual(1,len(j.workers))
        self.assertEqual(0,len(j2.workers))
        self.assertEqual(p1.job,j)
        p1.setJob(j2)
        self.assertEqual(0,len(j.workers))
        self.assertEqual(1,len(j2.workers))
        self.assertEqual(p1.job,j2)
    def testRankings(self):
        j = self.job
        p1 = FakePerson()
        for a in attribNames:
            p1.attrib[a] = 1
        self.assertEqual(1,j.rank(p1))
        for a in attribNames:
            p1.attrib[a] = 2
        self.assertEqual(2**6,j.rank(p1))
    def testFillSlots(self):
        better = FakePerson()
        worse = FakePerson()
        for a in attribNames:
            worse.attrib[a] = 1
            better.attrib[a] = 2
        j = self.job
        better.setJob(j)
        worse.setJob(j)
        for k in [2,1,0]:
            j.rejectWorst(k)
            self.assertEqual(k,len(j.workers))
            if k == 1:
                self.assertEqual(worse.job,None)
                self.assertEqual(better.job,j)
                self.assertGreaterEqual(j.rank(better),j.rank(worse))


class TestJobTurns(unittest.TestCase):
    def testBasicTurn(self):
        job = Job(name="testjob",level=1,prefWeights=allOnes,attribWeights=allOnesZipped)
        p = FakePerson()
        p.setJob(job)
        events = job.turn(p)
        self.assertTrue("work" in events)
  
if __name__ == '__main__': # pragma: no cover
    unittest.main()

