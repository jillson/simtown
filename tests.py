import unittest
#TODO: do we want to do magic so we import unittest.mock if python3 and mock if python 2?
from mock import patch
from people import Person, simple_next_gen, reaper
from StringIO import StringIO

class TestPeople(unittest.TestCase):

  #TODO: mock random
  #TODO: move getting out to setUp
  
  def test_check_first_gen(self):
      p = Person()
      self.assertGreater(p.age,15)
      self.assertLessEqual(p.age,32)

  def test_viable(self):
      p = Person()
      p.body = 0
      self.assertFalse(p.viable())
      p.body = 1
      p.strength = 1
      p.intelligence = 1
      p.charisma = 1
      p.will = 1
      p.dex = 1
      self.assertTrue(p.viable())
      for dstat in ["body","strength","intelligence","charisma","will","dex"]:
          p.__dict__[dstat] = 0
          self.assertFalse(p.viable())
          p.__dict__[dstat] = 1
          
  def test_check_second_gen(self):
      p1 = Person()
      p2 = Person()
      p3 = Person([p1,p2])

  def test_output(self):
      p = Person()
      p.body = 1
      p.strength = 2
      p.dex = 3
      p.intelligence = 4
      p.charisma = 5
      p.will = 6

      out = StringIO()
      p.print_stats(out=out)
      output = out.getvalue().strip()
      self.assertEqual(output,'1:2:3:4:5:6')

  def test_simple_gen(self):
    with patch('random.randint',return_value=2) as mock_randint:
      population = [Person() for _ in xrange(32)]
      out = StringIO()
      nextPop = simple_next_gen(population,out=out)
      expectedPeople = 32
      actualPeople = len(nextPop)
      output = out.getvalue().strip()
      self.assertEqual("We had %d folks die off at birth and %d new kids" % (expectedPeople-actualPeople,actualPeople),output)
      for p in nextPop:
        self.assertTrue(p.viable())
  def test_reaper(self):
    class Dummy:
      def __init__(self,x):
        self.x = x
      def viable(self):
        return self.x
    deadPool = [Dummy(False) for _ in xrange(5)]
    livePool = [Dummy(True) for _ in xrange(5)]
    mixedPool = deadPool + livePool
    dpo = reaper(deadPool)
    lpo = reaper(livePool)
    mpo = reaper(mixedPool)
    self.assertEqual(len(dpo),0)
    self.assertEqual(len(lpo),5)
    self.assertEqual(len(mpo),5)
  def test_json(self):
    p = Person()
    x = p.json()
    pass
  
  
if __name__ == '__main__':
    unittest.main()


