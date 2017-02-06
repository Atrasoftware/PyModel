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

    ('Generate dot commands from SpeedControl FSM',
     'pmg SpeedControl'),

    ('Generate SVG file from dot commands',
     'dotsvg SpeedControl'),

    ('Generate FSM from composition of PowerSwitch and SpeedControl, show interleaving',
     'pma SpeedControl PowerSwitch -o PowerSpeed'),

    ('Generate dot commands from composed FSM',
     'pmg PowerSpeed'),

    ('Generate SVG from dot',
     'dotsvg PowerSpeed')

    # Now you can display PowerSwitch.svg, SpeedControl.svg and PowerSpeed.svg
    # in three browser tabs
]
