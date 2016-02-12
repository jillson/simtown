import unittest
#TODO: do we want to do magic so we import unittest.mock if python3 and mock if python 2?
from mock import patch,Mock
from StringIO import StringIO
from utils_for_testing import *

from matching import Matchmaker,GenericTarget,GenericApplicant

attribNames = ["dummy%d" % (i+1) for i in xrange(6)]

class testMatchmaker(unittest.TestCase):
    def setUp(self):
        self.mm = Matchmaker()
    def test_wrappers(self):
        gt = GenericTarget(attribs={"foo":"bar"})
        ga = GenericApplicant()
    def test_matchmaking_even(self):
        self.common_matchmaking_single(4,4)
        self.common_matchmaking_multi(3,2)
    def test_matchmaking_too_many_applicants(self):
        self.common_matchmaking_single(6,4)
        self.common_matchmaking_multi(4,2)
    def test_matchmaking_too_few_applicants(self):
        self.common_matchmaking_single(4,6)
        self.common_matchmaking_multi(3,3)
    
    def common_matchmaking_single(self,numApplicants,numTargets):
        applicants = [GenericApplicant(attribNames=attribNames) for _ in xrange(numApplicants)]
        targets = [GenericTarget(attribNames=attribNames) for i in xrange(numTargets)]
        biggest = max(numApplicants,numTargets)+10
        for i in xrange(numApplicants):
            for a in attribNames:
                applicants[i].attrib[a] = biggest-i
            applicants[i].id = i
        for i in xrange(numTargets):
            targets[i].id = i
            for a in attribNames:
                targets[i].attrib[a] = biggest-i
        
        self.mm.match(applicants,targets)
        for i in xrange(min(numApplicants,numTargets)):
            #print "Hmm... for i == %d, we expected to see %s in %s" % (i,str(targets[i].id),str([x.id for x in applicants[i].selected]))
            self.assertTrue(targets[i] in applicants[i].selected)
            self.assertTrue(applicants[i] in targets[i].selected)
        if numApplicants > numTargets:
            extra = applicants
        else:
            extra = targets
        for i in xrange(min(numApplicants,numTargets),max(numApplicants,numTargets)):
            self.assertEqual(len(extra[i].selected),0)

    def common_matchmaking_multi(self,numApplicants,numTargets):
        applicants = [GenericApplicant(attribNames=attribNames) for _ in xrange(numApplicants)]
        targets = [GenericTarget(maxSelected=(i+1),attribNames=attribNames) for i in xrange(numTargets)]
        numPositions = (numTargets * (numTargets + 1))/2
        biggest = max(numApplicants,numTargets)+10
        for i in xrange(numApplicants):
            for a in attribNames:
                applicants[i].attrib[a] = biggest-i
            applicants[i].id = "App%d" % i
        for i in xrange(numTargets):
            for a in attribNames:
                targets[i].attrib[a] = biggest-i
            targets[i].id = "Tar%d" % i

        self.mm.match(applicants,targets)
        
        jobID = 0
        jobCount = 0
        for targetID in xrange(min(numApplicants,numPositions)):
                self.assertTrue(applicants[targetID] in targets[jobID].selected)
                self.assertTrue(targets[jobID] in applicants[targetID].selected)
                if jobCount >= jobID:
                    jobCount = 0
                    jobID += 1
                else:
                    jobCount += 1

        if numApplicants == numPositions: 
            return
        
        if numApplicants > numPositions:
            for i in xrange(numPositions,numApplicants):
                self.assertEqual(len(applicants[i].selected),0)
        else:
            jobID += 1
            self.assertEqual(jobID * (jobID + 1) / 2 - jobID + jobCount,numApplicants)
            jobID -= 1
            while jobID < numTargets:
                self.assertEqual(len(targets[jobID].selected),0)
                jobID += 1


if __name__ == '__main__': # pragma: no cover
    unittest.main()

