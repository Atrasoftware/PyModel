"""
PowerSwitch, based on C# example at nmodel.codeplex.com, model program page


"""

import random

### Model

# State

power = False
ciccio = True

# Actions

def PowerOn():
  global power
  power = True

def PowerOnEnabled():
  return not power

def PowerOff():
  global power
  global ciccio
  power = False
  ciccio = False

def PowerOffEnabled():
  return power

def Accepting():
  return not power

# needed for multiple test runs in one session

def Reset():
  global power
  if(random.random()<0.3):
    power = False
  else:
    power = True

### Metadata

state = ('power', 'ciccio')

actions = (PowerOn, PowerOff, Reset)
enablers = { PowerOn:(PowerOnEnabled,), PowerOff:(PowerOffEnabled,), Reset:(PowerOffEnabled,)}
cleanup = (PowerOff,)
