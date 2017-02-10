"""
ProductModelProgram

Uniform interface to every kind of model: ModelProgram, FSM, TestSuite.

This module is used by both the analyzer and the tester.

This module uses *composition* to construct and use the *product* of
all the models in the session.

This module performs composition, so it must identify actions by name
strings (which are the same in all the composed models) not function
objects (which are specific to each model's module).

Users of this module identify actions by aname strings.
Modules used by this module invoke action function objects.
This module translates action function a to string aname: aname = a.__name__
and translates aname string to action function a: a = getattr(module, aname)
"""

from operator import concat
from collections import defaultdict

from FSM import FSM
from TestSuite import TestSuite
from ModelProgram import ModelProgram
from functools import reduce
import collections


class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


if __name__ == '__main__':
    s = OrderedSet('abracadaba')
    t = OrderedSet('simsalabim')
    print(s | t)
    print(s & t)
    print(s - t)


class ProductModelProgram(object):

  def __init__(self, options, args):
    self.TestSuite = False # used by pmt nruns logic
    self.module = dict()  # dict of modules keyed by name
    self.mp = dict()      # dict of model programs keyed by same module name

    # Populate self.module and self.mp from modules named in command line args
    # Models that users write are just modules, not classes (types)
    #  so we find out what type to wrap each one in
    #  by checking for one of each type's required attributes using hasattr
    for mname in args: # args is list of module name
      self.module[mname] = __import__(mname)
      if hasattr(self.module[mname], 'graph'):
        print("^^^^^^^^^^^^^^^^^^1111111111")
        self.mp[mname] = FSM(self.module[mname],options.exclude,options.action)
      # for backwards compatibility we accept all of these test_suite variants
      elif (hasattr(self.module[mname], 'testSuite') or
            hasattr(self.module[mname], 'testsuite') or
            hasattr(self.module[mname], 'test_suite')):
        print("^^^^^^^^^^^^^^^^^^22222222222")
        self.mp[mname] = TestSuite(self.module[mname],
                                   options.exclude, options.action)
        self.TestSuite = True # used by pmt nruns logic
      elif self.module[mname].__doc__.strip().upper().startswith('PYMODEL CONFIG'):
        print("^^^^^^^^^^^^^^^^^^33333333333333")
        pass # configuration module, merely importing it did all the work
      else:
        # got this far, should be a ModelProgram -- if not, crash
        print("^^^^^^^^^^^^^^^^^^4444444444444444")
        self.mp[mname] = ModelProgram(self.module[mname],
                                      options.exclude, options.action)

    # Now that all modules have been imported and executed their __init__
    #  do a postprocessing pass over all model objects
    #  to process metadata that might be affected by configuration modules
    for mp in list(self.mp.values()):
      mp.post_init()

    # set of all anames in all model programs - the vocabulary of the product
    self.anames = set().union(*[set([a.__name__ for a in mp.actions ])
                                for mp in list(self.mp.values())])
    # print 'anames %s' % self.anames # DEBUG

    # set of anames of all observable actions in all model programs
    # observables obtain arg values from the environment, not parameter gen.
    self.observables = set().union(*[set([a.__name__
                                          for a in mp.module.observables])
                                     for mp in list(self.mp.values())])
                                     # FSM and TestSuite must have .observables
    # print 'observables %s' % self.observables # DEBUG

    # dict from aname to set of all m where aname is in vocabulary
    self.vocabularies = \
        dict([(aname, set([m for m in self.mp if aname in
                           [a.__name__ for a in self.mp[m].actions]]))
              for aname in self.anames])
    # print 'vocabularies %s' % self.vocabularies # DEBUG

  # ProductModelProgram only provides methods etc. called by test runner etc.:
  # EnabledActions(cleanup), Properties(), DoAction(a,args), Reset(), TestSuite
  # BUT not methods used internally in mp classes: Churrent, Restore, GetNext

  def ActionEnabled(self, aname, args):
    """
    True if action aname with args is enabled in the current state
    """
    return all([m.ActionEnabled(getattr(m.module, aname), args)
                # NOT! empty argument list in model matches any arguments
                # NOT! or m.ActionEnabled(getattr(m.module, aname), ())
                # handle zero-args/match-all inside m.ActionEnabled
               for m in list(self.mp.values())
               # aname might be an unshared action, not present in all mp
               if aname in [ a.__name__ for a in m.actions ]])

  def EnabledTransitions(self, cleanup):
    """
    This is where composition happens!
    (aname,args,result) is enabled in the product if it is enabled,
    OR (aname, (), None) with empty args and None result is enabled
    in every machine where aname is in the vocabulary.
    Returns list: [(aname, args, result, next, properties), ... ]
     third item result is the same value from all mp, or None
     fourth item next is dict of mp name to that mp's next state:
       (m1:next1,m2:current2,m3:next3,...),...]
      or to its current state if aname is not in that mp vocabulary
     fifth item properties is dict of property name to value in next state:
       { 'accepting': True, 'statefilter': True, ... }
     where there is just one value for each property for the whole product
    """
    # Call ParamGen here to allow for state-dependent parameter generation
    for mp in list(self.mp.values()):
      if isinstance(mp, ModelProgram):
        mp.ParamGen()

    # Built up dicts from mp name to list of all its enabled
    #  (action, args, result, next state, properties)
    print("00000000000000000000")
    # dict for FSM and TestSuite only, they might provide args for observables
    enabledScenarioActions = \
        dict([(m, self.mp[m].EnabledTransitions(cleanup))
              for m in self.mp if (not isinstance(self.mp[m], ModelProgram))])
    print('enabledScenarioActions', enabledScenarioActions) # DEBUG
    print("11111111111111111111")
    # dict from action to sequence of argslists
    argslists = defaultdict(list)
    for transitions in list(enabledScenarioActions.values()):
      for (action, args, result, next_state, properties) in transitions:
        argslists[action].append(args) # append not extend
    print("22222222222222222")
    # If more than one scenario in product, there may be duplicates - use sets
    scenarioArgslists = dict([(action, set(args))
                              for (action,args) in list(argslists.items())])
    print('scenarioArgslists', scenarioArgslists)
    print("33333333333333333")

    # Pass scenarioArgslists to ModelProgram EnabledTransitions
    # so any observable actions can use these argslists

    # TODO: MUST DO THIS FOR EACH PERMUTATION
    #
    # for m in self.mp if isinstance(self.mp[m], ModelProgram):
    #     self.mp[m].EnabledTransitions(scenarioArgslists, cleanup)
    enabledModelActions = \
         dict([(m, self.mp[m].EnabledTransitions(scenarioArgslists, cleanup))
               for m in self.mp if isinstance(self.mp[m], ModelProgram)])
    print('enabledModelActions', enabledModelActions) # DEBUG
    print("44444444444444444")
    # Combine enabled actions dictionaries (they have distinct keys)
    enabledActions = dict()
    enabledActions.update(enabledScenarioActions) # FSM and TestSuite
    enabledActions.update(enabledModelActions)    # ModelProgam
    print ('enabledActions', enabledActions) # DEBUG

    # set (with no duplicates) of all (aname, args, result) in enabledActions
    transitions = OrderedSet([(a.__name__, args, result)
                        for (a,args,result,next,properties) in
                           reduce(concat,list(enabledActions.values()))])
    print ('transitions inside mp', transitions)

    # dict from (aname, args, result)
    # to set of all m where (aname, args, result) is enabled
    # this dict can be compared to self.vocabularies
    invocations = \
        dict([((aname, args, result),
               OrderedSet([ m for m in self.mp
                     if (aname,args,result) in
                     [(a.__name__, argsx, resultx) # argsx,resultx is inner loop
                      for (a,argsx,resultx,next,properties) in enabledActions[m]]]))
              for (aname, args, result) in transitions ])
    # print 'invocations %s' % invocations # DEBUG

    # list of all (aname, args, result) that are enabled in the product
    # (aname,args,result) enabled in product if (aname,args,result) is enabled
    # or (aname,()) and None result is enabled in all m where aname is in vocab
    # (would be nice to generalize to all prefixes of args, not just ())
    enabledAnameArgs = \
        [(aname, args, result)
         for (aname, args, result) in transitions
         # set union, maybe use ... .union(* ... ) for all prefixes
         if invocations[aname,args,result] | invocations.get((aname,(),None),
                                                             set())
         == self.vocabularies[aname]]

    # Now we have all enabled (action,args,result), now rearrange the data

    # for each enabled (aname,args), associate next states and properties by mp
    # all enabled [(aname,args,result,{m1:(next1,properties1),m2:...}), ...]
    enabledTs = \
        [(aname, args, result,
          dict([(m, [(next,properties)
                     for (a,argsx,resultx,next,properties) in enabledActions[m]
                     # ...[0] to extract item from singleton list
                     if a.__name__ == aname
                     and (argsx == args or argsx == ())][0]
                 if m in # aname,args or aname,() is enabled in m
                 invocations[aname,args,result] | invocations.get((aname,(),
                                                                   None),set())
                 # a,args not enabled in m, m remains in same state
                 # (the following pair is the value for key m)
                 else (self.mp[m].Current(), self.mp[m].Properties()))
                for m in self.mp ]))
         for (aname, args, result) in enabledAnameArgs ]

    # print 'enabledTs %s' % enabledTs # DEBUG

    # combine result and properties from all the mp
    # list, all enabled [(aname,args,result,{m1:next1,m2:next2},properties),...]
    mpEnabledTransitions = [(aname, args, result,
                             # dict of next states: {m:next1,m2:next2, ... }
                             dict([ (m,mdict[m][0]) for m in mdict ]),
                             # combined properties
                             self.NextProperties(dict([ (m,mdict[m][1])
                                                   for m in mdict ])))
                           for (aname,args,result,mdict) in enabledTs ]
    return mpEnabledTransitions

  def Accepting(self):
    return self.Properties()['accepting']

  def StateInvariant(self):
    return self.Properties()['stateinvariant']

  # lots of nearly-repeated code in next two methods, can we streamline ... ?

  def Properties(self):
    """
    Combine properties of mps in the current state
    """
    return { 'accepting':
             # all mp in the current state are in their accepting states
             all([ m.Properties()['accepting'] for m in list(self.mp.values()) ]),
             'statefilter':
             all([ m.Properties()['statefilter'] for m in list(self.mp.values()) ]),
             'stateinvariant':
             all([ m.Properties()['stateinvariant'] for m in list(self.mp.values()) ])
             }

  def NextProperties(self, next_properties):
    """
    Combine properties of mps in the next state
    """
    return { 'accepting':
             # all mp in the next state are in their accepting states
             all([ next_properties[m]['accepting'] for m in next_properties]),
             'statefilter':
             all([ next_properties[m]['statefilter'] for m in next_properties]),
             'stateinvariant':
             all([ next_properties[m]['stateinvariant'] for m in next_properties])
             }

  def DoAction(self, aname, args):
    """
    Execute action with aname in all the mp where it is enabled,
    return result from last mp arg
    """
    result = None
    for m in list(self.mp.values()):
      # aname might be an unshared action, not present in all mp
      if aname in [ a.__name__ for a in m.actions ]:
        result = m.DoAction(getattr(m.module, aname), args)
    return result  # results from all mp should be the same, return any one

  def Reset(self):
    """
    Reset all the mp
    """
    for m in list(self.mp.values()):
      m.Reset()

  def Current(self):
    """
    Return dictionary of current states
    """
    return dict([(m, self.mp[m].Current()) for m in self.mp ])

  def Restore(self, state):
    """
    Restore states from dictionary
    """
    for m in self.mp:
      self.mp[m].Restore(state[m])

  def RestartModel(self):
    """
    Restart the model to change action permutations
    """
    for m in self.mp:
      self.mp[m].RestartModel()
