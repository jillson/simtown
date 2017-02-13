
import unittest
try: #python 3.3's unittest.mock backported in separate mock for Python 2
    from unittest.mock import patch
except ImportError:
    from mock import patch

from StringIO import StringIO

from town import *

class TestTown(unittest.TestCase):
    def testTownCreation(self):
        t = Town("sometown")
        self.assertEqual(t.name,"sometown")
        self.assertLessEqual(len(t.pop),64)
        for name,gender in [["king","M"],["queen","F"],["priest","M"],["commander","M"],["foreman","M"]]:
            self.assertEqual(t.__dict__[name].gender,gender,"%s should be %s" % (name,gender))
            self.assertEqual(t.jobs[name],t.__dict__[name].job)
        males = 0
        females = 0
        um = 0
        uf = 0
        #TODO: coverage complains because for a given (non-determinstic) run, either um or ut will be zero (hence the assertion)...
        dummyMan = Person()
        dummyMan.gender = "M"
        dummyWoman = Person()
        dummyWoman.gender = "F"
        t.pop.append(dummyMan)
        t.pop.append(dummyWoman)
        for x in t.pop:
            if x.gender == "M":
                males += 1
                if x.spouse == None:
                    um += 1
            else:
                females += 1
                if x.spouse == None:
                    uf += 1
        self.assertEqual(len(t.pop),males+females)
        print "Check... we had %d males (%d unmarried) and %d females (%d unmarried)" % (males,um,females,uf)
        bigger = max(males,females)
        smaller = min(males,females)
        bu = max(um,uf)
        su = min(um,uf)

        self.assertEqual(1,su)
        self.assertEqual(bigger-smaller,bu-1)

    def testJobManagement(self):
        t = Town("dummy")
        employed = 0
        for p in t.pop:
            if p.job:
                employed += 1
        self.assertGreaterEqual(employed * 3,len(t.pop))
    def testTownBuildings(self):
        t = Town("dummy")
        self.assertGreater(len(t.buildings),0,"Hmm, why you no have buildings")
        for b in defaultBuildings:
            building = t.buildings.get(b,None)
            self.assertTrue(building != None,"Missing " + building.name)


class TestTownTurn(unittest.TestCase):
    def setUp(self):
        self.t = Town("test")
    def testOutputOfTurn(self):
        t = self.t
        self.assertGreater(t.resources["food"],0)
        startFood = t.resources["food"]
        startPopIds = [p.name for p in t.pop]
        t.turn()
        endPopIds = [p.name for p in t.pop]
        self.assertNotEqual(startPopIds,endPopIds)
    def testEvents(self):
        t = self.t
        testEvents = {"death":[t.pop[0]],"bogus":[]}
        dead = t.pop[0]
        t.handleEvents(testEvents)
        self.assertTrue(dead not in t.pop)
    def testStarving(self):
        """ checks that if food supply dries up, food gets reset to zero but we kill off the weaker or poorer or whatever folks """
        t = self.t
        t.resources["food"] = -1000
        nonBabiesPre = len([p for p in t.pop if p.attrib["age"] > 1])
        t.turn()
        nonBabies = len([p for p in t.pop if p.attrib["age"] > 1])
        self.assertEqual(0,t.resources["food"])
        self.assertGreater(nonBabiesPre,nonBabies)
    def testEconomy(self):
        """ checks if a person gets gold based on some demand for their services / skill levels """
        t = self.t
        t.resources["food"] = 1000
        levelOneFolks = [x for x in t.pop if x.attrib["joblevel"] > 0]
        self.assertGreater(len(levelOneFolks),0)
        dummy = levelOneFolks[0]
        self.assertEqual(0,dummy.attrib["gold"])
        t.turn()
        self.assertEqual(dummy.attrib["joblevel"],dummy.attrib["gold"])
        dummy.attrib["gold"] = 1000
        t.resources["food"] = 10
        t.turn()
        self.assertTrue(dummy in t.pop)
        self.assertLess(dummy.attrib["gold"],1000)
    def testSupplyDemand(self):
        pass
if __name__ == '__main__': # pragma: no cover
    unittest.main()

