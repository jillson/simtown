
import unittest
try: #python 3.3's unittest.mock backported in separate mock for Python 2
    from unittest.mock import patch
except ImportError:
    from mock import patch

from StringIO import StringIO

from utils import pickBest, makeRule, makeWeightedRule, makeWeightedAddRule


class Dummy:
    pass


class TestMakeRules(unittest.TestCase):
    def testMakeSingleAttribRule(self):
        m = makeRule(['foo'])
        d = Dummy()
        d.foo = 0
        self.assertEqual(0,m(d))
        d.foo = 3
        self.assertEqual(3,m(d))
    def testMakeMultiAttribRule(self):
        m = makeRule(['foo','bar'])
        d = Dummy()
        d.foo = 0
        self.assertEqual(0,m(d))
        d.foo = 3
        self.assertEqual(0,m(d))
        d.bar = 4
        self.assertEqual(12,m(d))


class TestMakeWeightedRules(unittest.TestCase):
    def testMakeSingleAttribRule(self):
        m = makeWeightedRule([[2,'foo']])
        d = Dummy()
        d.foo = 0
        self.assertEqual(0,m(d))
        d.foo = 3
        self.assertEqual(6,m(d))
    def testMakeMultiAttribRule(self):
        m = makeWeightedRule([[1,'foo'],[2,'bar']])
        d = Dummy()
        d.foo = 0
        self.assertEqual(0,m(d))
        d.foo = 3
        self.assertEqual(0,m(d))
        d.bar = 4
        self.assertEqual(24,m(d))

class TestMakeWeightedAddedRules(unittest.TestCase):
    def testMakeSingleAttribRule(self):
        m = makeWeightedAddRule([[1,'foo']])
        d = Dummy()
        d.foo = 0
        self.assertEqual(0,m(d))
        d.foo = 3
        self.assertEqual(3,m(d))
    def testMakeMultiAttribRule(self):
        m = makeWeightedAddRule([[1,'foo'],[2,'bar']])
        d = Dummy()
        d.foo = 0
        self.assertEqual(0,m(d))
        d.foo = 3
        self.assertEqual(3,m(d))
        d.bar = 4
        self.assertEqual(11,m(d))


        
class TestPickBest(unittest.TestCase):
    def simpleMetric(self,x,dummy):
        return x
    def testHandleEmpty(self):
        x = pickBest([],None)
        self.assertTrue(len(x) == 0)
    def testHandleTrivial(self):
        with patch('random.shuffle') as mock_shuffle:
            x = pickBest([1,2,3],None,n=4)
            self.assertTrue(len(x) == 3)
            self.assertEqual([1,2,3],x)
            self.assertTrue(mock_shuffle.called)
    def testHandleAllDifferent(self):
        with patch('random.shuffle') as mock_shuffle:
            x = pickBest([1,2,3],self.simpleMetric,n=2)
            self.assertTrue(len(x) == 2)
            self.assertEqual([3,2],x)
            self.assertNotEqual([2,3],x)
            self.assertTrue(mock_shuffle.called)
            for i,v in enumerate(x):
                self.assertEqual([v],mock_shuffle.call_args_list[i][0][0])
                
    def testHandleLastDifferent(self):
        with patch('random.shuffle') as mock_shuffle:
            x = pickBest([1,1,2,3],self.simpleMetric,n=2)
            self.assertTrue(len(x) == 2)
            self.assertEqual([3,2],x)
            self.assertNotEqual([2,3],x)
            self.assertTrue(mock_shuffle.called)
            for i,v in enumerate(x):
                self.assertEqual([v],mock_shuffle.call_args_list[i][0][0])
    def testHandleFirstDifferent(self):
        with patch('random.shuffle') as mock_shuffle:
            x = pickBest([1,2,3,3],self.simpleMetric,n=2)
            self.assertTrue(len(x) == 2)
            self.assertEqual([3,3],x)
            self.assertTrue(mock_shuffle.called)
            self.assertEqual(len(mock_shuffle.call_args_list),1)



  
if __name__ == '__main__': # pragma: no cover
    unittest.main()

