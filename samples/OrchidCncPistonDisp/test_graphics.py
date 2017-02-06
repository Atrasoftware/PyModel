"""
OrchidCncPistonDisp graphics tests
"""

cases = [
    ('Scenarios module with four runs, by itself',
     'pma Scenarios'),

    ('Scenarios module with four runs, by itself',
     'pmg ScenariosFSM'),

    ('Scenarios module with four runs, by itself',
     'dotsvg ScenariosFSM'),

    ('Generate FSM from OrchidCncPistonDisp model program',
     'pma OrchidCncPistonDisp'),

    ('Generate dot graphics commands from generated OrchidCncPistonDispFSM',
     'pmg OrchidCncPistonDispFSM'),

    ('Generate SVG file from dot commands',
     'dotsvg OrchidCncPistonDispFSM'),

    # Now you can display OrchidCncPistonDisp.svg
]
