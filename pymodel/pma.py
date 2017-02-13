#!/usr/bin/env python
"""
PyModel Analyzer - generate FSM from product model program
"""

import Analyzer
import AnalyzerOptions
from ProductModelProgram import ProductModelProgram
import itertools

def main():
    (options, args) = AnalyzerOptions.parse_args()
    if not args:
        AnalyzerOptions.print_help()
        exit()
    else:
        mp = ProductModelProgram(options, args)
        for a in args:
            if options.recursive_restart:
                for permutation in itertools.permutations(mp.mp[a].actions):
                    mp.mp[a].actions = permutation
                    Analyzer.explore(mp, options.maxTransitions)
            else:
                Analyzer.explore(mp, options.maxTransitions)
        print(('%s states, %s transitions, %s accepting states, %s unsafe states' % \
            (len(Analyzer.states),len(Analyzer.graph),len(Analyzer.accepting),len(Analyzer.unsafe))))
        mname = options.output if options.output else '%sFSM' % args[0]
        Analyzer.save(mname)

if __name__ == '__main__':
    main ()
