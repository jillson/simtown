import unittest
#TODO: do we want to do magic so we import unittest.mock if python3 and mock if python 2?
from mock import patch,Mock
from people import Person, AttributeMap, Skill, skillDict, simple_next_gen, reaper, attribNames, court
from StringIO import StringIO
from utils_for_testing import *

class FakeJob:
  def __init__(self):
    pass
  def removeWorker(self,w):
    pass
  def addWorker(self,w):
    pass
  def turn(self,person):
    return {"work":"foo"}

class FakePerson:
  pass

class TestAttributes(unittest.TestCase):
  def testBasic(self):
    a = AttributeMap(attribNames)
    p = FakePerson()
    p.attrib = a
    p.attrib[attribNames[0]] = 4
    self.assertEqual(4,p.attrib[attribNames[0]])
    self.assertEqual(0,p.attrib["nonExistent"])
  def testSkills(self):
    sampleAttrib = attribNames[0]
    a = AttributeMap(attribNames)
    p = FakePerson()
    p.attrib = a
    p.attrib[attribNames[0]] = 4
    skillDict["dummy"] = Skill("dummy",sampleAttrib)
    skillDict["untrained"] = Skill("untrained","nonExistent")
    skillDict["trained"] = Skill("trained",attribNames[1])
    p.attrib["trained"] = 5
    self.assertEqual(4,p.attrib["dummy"])
    self.assertEqual(0,p.attrib["dummy2"])
    self.assertEqual(5,p.attrib["trained"])
    p.attrib[attribNames[1]] = 2
    self.assertEqual(7,p.attrib["trained"])
  def testRepr(self):
    a = AttributeMap(attribNames)
    x = str(a)
    self.assertTrue(x)
  def testRoll(self):
    p = Person()
    p.attrib["dummyAttrib"]=3
    with patch("random.randint",side_effect=f_all_1):
      self.assertEqual(-1,p.roll("dummyAttrib"))
    with patch("random.randint",side_effect=f_all_6):
      self.assertEqual(p.roll("dummyAttrib"),7)
    with patch("random.randint",side_effect=f_repeat_1_to_6):
      self.assertEqual(p.roll("dummyAttrib"),1)
    with patch("random.randint",side_effect=f_repeat_1_to_6):
      self.assertEqual(p.roll("dummyAttrib"),3)

    
    


class TestBirth(unittest.TestCase):
  def setUp(self):
    h = Person()
    w = Person()
    h.gender = "M"
    w.gender = "W"
    h.marry(w)
    w.attrib["body"] = 5
    h.attrib["body"] = 5
    self.h = h
    self.w = w
    
  def testVirginBirth(self):
    p = Person()
    p.deathCheck = mockFalseFunc
    events = p.turn()
    self.assertFalse("birth" in events,"Has to be married to have a child here")
    self.assertFalse("death" in events,"Shouldn't have died")

  def testMaleBirth(self):
    self.assertFalse(self.h.birthCheck())

  def testBiologicalClock(self):
    #TODO: mock something so can check fertility rates
    w = self.w
    w.attrib["body"] = 1000
    w.attrib["age"] = 14
    events = w.turn()
    self.assertFalse("birth" in events)
    events = w.turn()
    self.assertTrue("birth" in events)
    w.attrib["age"] = 39
    events = w.turn()
    self.assertTrue("birth" in events)
    events = w.turn()
    self.assertFalse("birth" in events)

  def testTwins(self):
    print "Need to support this, eventually"
    
  def testDiedGivingBirth(self):
    #TODO: should we use mockTrueFunc or override the attribCheck
    w = self.w
    w.birthCheck = mockTrueFunc
    w.deathCheck = mockTrueFunc
    events = w.turn()
    #TODO: allow for child to also die :(
    self.assertTrue("birth" in events)
    self.assertTrue("death" in events)

  def testGaveBirth(self):
    w = self.w
    w.birthCheck = mockTrueFunc
    w.deathCheck = mockFalseFunc
    events = w.turn()
    self.assertTrue("birth" in events)
    self.assertFalse("death" in events)

  def testNoPregnancy(self):
    w = self.w
    w.birthCheck = mockFalseFunc
    w.deathCheck = mockFalseFunc
    events = w.turn()
    self.assertFalse("birth" in events)
    self.assertFalse("death" in events)

  def testCheckBaby(self):
    w = self.w
    w.birthCheck = mockTrueFunc
    w.deathCheck = mockFalseFunc
    events = w.turn()
    baby = events.get("birth",[False])[0]
    self.assertTrue(baby)
    self.assertTrue(self.h in baby.parents)
    self.assertTrue(w in baby.parents)
    self.assertEqual(baby.attrib["age"],0)

class TestPeopleTurns(unittest.TestCase):
  def setUp(self):
    p = Person()
    p.attrib["age"] = 18
    self.p = p
    
  def testDeath(self):
    #TODO: have death call body check we stub out
    p = self.p
    self.assertFalse(p.deathCheck())
    p.attrib["age"] = 120
    self.assertFalse(p.deathCheck())
    p.attrib["age"] = 121
    self.assertTrue(p.deathCheck())
    
  def testAging(self):
    p = self.p
    startAge = p.attrib["age"]
    events = p.turn()
    self.assertEqual(p.attrib["age"],startAge+1)
    p.attrib["age"] = 120
    events = p.turn()
    self.assertTrue("death" in events)

  def testWorking(self):
    p = self.p
    events = p.turn()
    self.assertFalse("work" in events)
    fakeJob = FakeJob()
    p.setJob(fakeJob)
    p.deathCheck = mockFalseFunc
    events = p.turn()
    self.assertTrue("work" in events)

class TestPeople(unittest.TestCase):

  #TODO: mock random
  #TODO: move getting out to setUp
  
  def test_check_first_gen(self):
      p = Person()
      self.assertGreater(p.attrib["age"],15)
      self.assertLessEqual(p.attrib["age"],32)

  def test_viable(self):
      p = Person()
      p.attrib["body"] = 0
      self.assertFalse(p.viable())
      for a in attribNames:
        p.attrib[a] = 1
      self.assertTrue(p.viable())
      for dstat in attribNames:
          p.attrib[dstat] = 0
          self.assertFalse(p.viable())
          p.attrib[dstat] = 1
          
  def test_check_second_gen(self):
      p1 = Person()
      p2 = Person()
      p3 = Person([p1,p2])
      print "This should really do a bit more, don't you think"

      
  def test_output(self):
      p = Person()
      for i,v in enumerate(attribNames):
        p.attrib[v] = i+1

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

  def test_courting_unaged(self):
    men = [Person() for _ in xrange(3)]
    women = [Person() for _ in xrange(3)]
    for i in xrange(3):
      men[i].gender = "M"
      women[i].gender = "F"
      

  

      
    
if __name__ == '__main__': # pragma: no cover
    unittest.main()


