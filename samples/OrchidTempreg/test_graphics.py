"""
PowerSwitch graphics tests
"""

cases = [
    ('Scenarios module with four runs, by itself',
     'pma Scenarios'),

    ('Scenarios module with four runs, by itself',
     'pmg ScenariosFSM'),

    ('Scenarios module with four runs, by itself',
     'dotsvg ScenariosFSM'),

    ('Generate FSM from PowerSwitch model program',
     'pma PowerSwitch'),

    ('Generate dot graphics commands from generated PowerSwitchFSM',
     'pmg PowerSwitchFSM'),

    ('Generate SVG file from dot commands',
     'dotsvg PowerSwitchFSM'),

    # Now you can display PowerSwitch.svg
]
