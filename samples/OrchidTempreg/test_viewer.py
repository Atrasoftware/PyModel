"""
Like test_graphics, except just uses one pvm command
instead of three: pma, pmg, dot.
Output files have the same names and should have the same contents as
in test_graphics output files saved in fsmpy/ and svg/
"""

cases = [
    ('Generate FSM from PowerSwitch model program',
     'pmv -T svg PowerSwitch'),

    # Now you can display PowerSwitchFSM.svg
]
