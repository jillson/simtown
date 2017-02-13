
import unittest
try: #python 3.3's unittest.mock backported in separate mock for Python 2
    from unittest.mock import patch
except ImportError:
    from mock import patch

from StringIO import StringIO
from collections import defaultdict


from market import Market
from utils_for_testing import *


class FakePerson:
    def __init__(self,roll=1,gold=1):
        self.job = None
        self.attrib = defaultdict(int)
        self.rollValue = roll
        self.attrib["gold"] = gold
    def roll(self,attrib):
        return self.rollValue
    

people = [FakePerson(gold=2) for _ in xrange(90)] + [FakePerson(gold=10) for _ in xrange(10)] + 
    
class TestMarket(unittest.TestCase):
    def setUp(self):
        self.market = Market()
    def testBasicDemand(self):
        m = self.market
        m.addInventory({"food":100})
        p = m.calcPrice(people,"food")
        self.assertEqual(p,2)
    #TODO: test when price < 1, price > 2, and various combinations between etc.
  
if __name__ == '__main__': # pragma: no cover
    unittest.main()

