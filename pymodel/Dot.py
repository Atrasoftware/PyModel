"""
Dot - generate graphics in dot language
"""

import os.path
import re

def insert_newlines(string, every=10):
    string = re.sub(r'([:])', r'\1\n', string)
    string = re.sub(r'([}]+(^[}]))', r'\1\n', string)
    string = re.sub(r'([,])', r'\1\n', string)
    return string
    # return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def node(n, fsm, nodeLabel):
    try: # FSM modules written by PyModel Analyzer have frontier attribute etc.
        unsafe = fsm.unsafe
        frontier = fsm.frontier
        finished = fsm.finished
        deadend = fsm.deadend
        runstarts = fsm.runstarts
    except AttributeError: # FSM modules written by hand may not have these
        unsafe = list()
        frontier = list()
        finished = list()
        deadend = list()
        runstarts = list()
    return '%s [ style=filled, shape=ellipse, peripheries=%s, fillcolor=%s,\n      label="%s"' % \
        (n, 2 if n in fsm.accepting else 1, # peripheries
         'red' if n in unsafe else
         'orange' if n in frontier else # high priority, analysis inconclusive
         'yellow' if n in deadend else
         'lightgreen' if n in finished else
         'lightgray' if n == fsm.initial or n in runstarts else #lowest priority
         'white', # other states
         n if not nodeLabel else insert_newlines(str(fsm.states[n])))

def state(n, fsm, nodeLabel, noStateTooltip):
    if noStateTooltip:
        return '%s ]' % node(n,fsm,nodeLabel)
    else:
        return '%s,\n      tooltip="%s" ]' % (node(n,fsm,nodeLabel), fsm.states[n])


def quote_string(x): # also appears in Analyzer
    if isinstance(x,tuple):
        return str(x)
    else:
        return "'%s'" % x if isinstance(x, str) else "%s" % x

def rlabel(result):
    return '/%s' % quote_string(result) if result != None else ''

def transition(t, style, noTransitionTooltip):
    current, (a, args, result), next = t
    action = '%s%s%s' % (a.__name__, args, rlabel(result))
    if style == 'name':
        label = '%s' % a.__name__
    elif style == 'none':
        label = ''
    else: # 'action'
        label = action
    if noTransitionTooltip:
        return '%s -> %s [ label="%s" ]' % \
            (current, next, label)
    else:
        return '%s -> %s [ label="%s", tooltip="%s" ]' % \
            (current, next, label, action)

def dotfile(fname, fsm, style, nodeLabel, noStateTooltip, noTransitionTooltip):
    f = open(fname, 'w')
    f.write('digraph %s {\n' % os.path.basename(fname).partition('.')[0])
    f.write('\n  // Nodes\n')
    try: # FSM modules written by PyModel Analyzer have states attribute
        f.writelines([ '  %s\n' % state(n,fsm,nodeLabel,noStateTooltip) \
            for n in fsm.states ])
    except: # FSM modules written by hand may not have states attribute
        nodes = set([current for (current,trans,next) in fsm.graph]
                    + [next for (current,trans,next) in fsm.graph])
        f.writelines([ '  %s ]\n' % node(n,fsm,nodeLabel) for n in nodes ])
    f.write('\n  // Transitions\n')
    f.writelines([ '  %s\n' % transition(t, style,noTransitionTooltip)
                   for t in fsm.graph ])
    f.write('}\n')
    f.close()
