
import unittest
try: #python 3.3's unittest.mock backported in separate mock for Python 2
    from unittest.mock import patch
except ImportError:
    from mock import patch

from StringIO import StringIO

from history import history

class TestHistory(unittest.TestCase):
    def setUp(self):
        history.reset()
    def testSingleton(self):
        from town import history as townHistory
        from people import history as peopleHistory
        self.assertEqual(townHistory,peopleHistory)
        self.assertEqual(history,townHistory)
        history.record("actor1","action1")
        townHistory.record("actor2","action2")
        records = peopleHistory.getRecords(actor="actor1")
        self.assertEqual(records,["action1"])
    def testGetRecords(self):
        for i in "actor1","actor2":
            for j in xrange(5):
                history.record(i,"action%d"%j)
        self.assertEqual(10,len(history.getRecords()))
        self.assertEqual(2,len(history.getRecords(action="action2")))
        self.assertEqual(5,len(history.getRecords(actor="actor1")))
        self.assertEqual(0,len(history.getRecords(actor="actor3")))
        self.assertEqual(1,len(history.getRecords(actor="actor1",action="action1")))
        self.assertEqual(0,len(history.getRecords(actor="actor1",action="action_none")))
                               
                               
                         

        
  
if __name__ == '__main__': # pragma: no cover
    unittest.main()

