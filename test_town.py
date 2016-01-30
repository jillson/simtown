
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

        self.assertEqual(0,su)
        self.assertEqual(bigger-smaller,bu)
    def testTownAttributes(self):
        t = Town("dummy")
        self.assertGreater(0,len(t.buildings))

  
if __name__ == '__main__': # pragma: no cover
    unittest.main()

