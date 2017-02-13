from mock import patch,Mock

mockTrueFunc = Mock()
mockTrueFunc.return_value = True
mockFalseFunc = Mock()
mockFalseFunc.return_value = False

def f_all_1(*args):
  return 1

def f_all_6(*args):
  return 6

def f_all_max(low,high):
  return high

def f_all_min(low,high):
  return low

staticRepeatValue = 6
def f_repeat_1_to_6(*args):
  global staticRepeatValue
  staticRepeatValue = (staticRepeatValue % 6) + 1
  return staticRepeatValue


def makeGenerator(alist):
  while True:
    for item in alist:
      yield item

def makeGetNext(generator):
  return next(generator)

  
