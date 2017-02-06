"""
Like test_graphics, except just uses one pvm command
instead of three: pma, pmg, dot.
Output files have the same names and should have the same contents as
in test_graphics output files saved in fsmpy/ and svg/
"""

cases = [
    ('Generate FSM from OrchidCncPistonDisp model program',
     'pmv -T svg OrchidCncPistonDisp'),

    # Now you can display OrchidCncPistonDispFSM.svg
]
