import unittest
#TODO: do we want to do magic so we import unittest.mock if python3 and mock if python 2?
from mock import patch
from people import Person, simple_next_gen, reaper, attribNames, court
from StringIO import StringIO

class FakeJob:
  def __init__(self):
    pass
  def removeWorker(self,w):
    pass
  def addWorker(self,w):
    pass
  

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
  def test_job(self):
    j = FakeJob()
    j2 = FakeJob()
    p = Person()
    self.assertEqual(p.job,None)
    #TODO: replace FakeJob with a real mock and check calls
    p.setJob(j)
    self.assertEqual(p.job,j)
    p.setJob(j2)
    self.assertEqual(p.job,j2)
  def test_marriage(self):
    m = Person()
    f = Person()
    m2 = Person()
    m.gender = "M"
    m2.gender = "M"
    f.gender = "F"
    m.marry(f)
    self.assertEqual(m.spouse,f)
    self.assertEqual(f.spouse,m)
    m.divorce()
    self.assertEqual(m.spouse,None)
    self.assertEqual(f.spouse,None)
    m.marry(m2) #not dealing with it
    self.assertEqual(m.spouse,None)
    self.assertEqual(m2.spouse,None)
    f.marry(m2)
    m.marry(f)
    self.assertEqual(m.spouse,None)
    self.assertEqual(m2.spouse,f)
    self.assertEqual(f.spouse,m2)

  def test_courting(self):
    self.common_courting(4,4)
    self.common_courting(6,4)
    self.common_courting(4,6)
    

  def common_courting(self,nm,nw):
    men = [Person() for _ in xrange(nm)]
    women = [Person() for _ in xrange(nw)]
    biggest = max(nm,nw)+10
    for i in xrange(nm):
      men[i].gender = "M"
      for a in attribNames:
        men[i].__dict__[a] = biggest-i
    for i in xrange(nw):
      women[i].gender = "F"
      for a in attribNames:
        women[i].__dict__[a] = biggest-i

    court(men,women)
    for i in xrange(min(nm,nw)):
      self.assertEqual(men[i].spouse,women[i])
      self.assertEqual(women[i].spouse,men[i])
    if nm > nw:
      extra = men
    else:
      extra = women
    for i in xrange(min(nm,nw),max(nm,nw)):
      self.assertEqual(extra[i].spouse,None)

      
    
if __name__ == '__main__': # pragma: no cover
    unittest.main()


