"""
PowerSwitch, based on C# example at nmodel.codeplex.com, model program page


"""


# coding: utf-8
from __future__ import print_function
import random
import time
import grpc
import temp_reg_pb2

channel = grpc.insecure_channel('localhost:6666')
stub = temp_reg_pb2.TRegStub(channel)
tid = temp_reg_pb2.TId()
empty = temp_reg_pb2.Empty()
get_confs = temp_reg_pb2.TConfigs()
set_confs = temp_reg_pb2.TConfigs()
tid.id = 0
set_confs.id = 0

### Model

# State
power = list()
for i in range(4):
  tid.id = i
  power.append(stub.GetConfigs(tid).run)
  time.sleep(0.5)

def PowerOn(x):
  global power
  global index
  global get_confs
  global tid
  tid.id = x
  stub.StartRegulators(tid)
  time.sleep(0.5)
  get_confs = stub.GetConfigs(tid)
  power[get_confs.id] = get_confs.run

def PowerOnEnabled(x):
  return not power[x]

def PowerOff(x):
  global power
  global index
  global get_confs
  global tid
  tid.id = x
  stub.StopRegulators(tid)
  time.sleep(0.5)
  get_confs = stub.GetConfigs(tid)
  power[get_confs.id] = get_confs.run

def PowerOffEnabled(x):
  return power[x]

def Accepting():
  return not power[tid.id]

# needed for multiple test runs in one session

def Reset():
  global power
  del power[:]

### Metadata

state = ('power',)

actions = (PowerOn, PowerOff)
enablers = {PowerOn:(PowerOnEnabled,),
    PowerOff:(PowerOffEnabled,),
    }

domains = {PowerOff: {'x':[0,1,2,3]},
           PowerOn: {'x':[0,1,2,3]},
          }

cleanup = (PowerOff,)
