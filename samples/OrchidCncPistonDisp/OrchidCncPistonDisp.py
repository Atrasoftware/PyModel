"""
PowerSwitch, based on C# example at nmodel.codeplex.com, model program page


"""


# coding: utf-8
from __future__ import print_function
import random
import time
import redis
import grpc
import asyncio
from asyncio import run_coroutine_threadsafe as rct
import threading
from enum import Enum
from concurrent import futures

import orchid.contrib.cnc_piston_disp as cnc_piston_disp
from orchid.core.component import generator_factory


class TempSettings():
    """Fake settings."""
    def __init__(self):
        self.GENERIC_SETTINGS = {
            'dry_run': True,
            'COMPONENT_INSTANCES': []
        }
        self.SPECIFIC_SETTINGS = {
          'CncPistonDisp':
            {'PistonDispenser':
                {
                    'purge_cap_piston': {
                        'virtualized': True,
                        'gpio_driver_map': {
                            'HK3_0': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                            'HK3_2': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                            'HK2_5': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                        },
                        'purge_piston_pull_out': {
                            'name': "HK3_0",
                            'default_value': True,
                        },
                        'purge_piston_pull_in': {
                            'name': "HK3_2",
                            'default_value': False,
                        },
                        'purge_piston_ev': {
                            'name': "HK2_5",
                            'default_value': True,
                        },
                    },
                    'gcode_machine': {
                        'hostname': 'localhost',
                        'port': 4444,
                        'custom_control_handler': 'orchid.contrib.cnc_piston_disp'
                                                  '.mocks.gcode_server'
                                                  '.gcode_grpc_server',
                        'custom_connection_handler': 'orchid.contrib.cnc_piston_disp'
                                                  '.mocks.gcode_server'
                                                  '.gcode_tcp_server',
                        'control_port': 50051,
                        'gpio_driver_map': {
                            'D2_P0': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                            'P8_27': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                            'P8_29': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                            'P8_42': 'orchid.core.hal.mocks.mock_gpio.Gpio',
                        },
                        'purging_position': (19, 0, 25),
                        'dispensing_units': [{
                            'virtualized': True,
                            'tandem': False,  # Ignored for now
                            'axes': [
                                'a',  # Must be one without tandem
                            ],
                            'components': {
                                'c1_diameter': 25,  # mm
                                'c2_diameter': 12.7,  # mm
                            },
                            'cylinder_height': 37,  # mm
                            'valves_delay': 0.1,  # seconds
                            'nozzles': [
                                # The aux will be automatically assigned in this order
                                # so, for the first nozzle, rv = 0, mv = 1, for the
                                # second rv = 2, mv = 3, etc...
                                {
                                    'prod_1': 'P8_42',
                                    'prod_2': 'P8_27',
                                    'active': True,
                                },
                                {
                                    'prod_1': 'P8_29',
                                    'prod_2': 'D2_P0',
                                    'active': True,
                                },
                            ],
                        }],
                        'conditional_inputs': {
                        },
                        'potlife': {
                            'timeout': 2400,  # seconds
                            'quantity': 8,  # cc
                            'flowrate': 0.5,  # cc/s
                        },
                        'priming': {
                            'quantity': 8,  # cc
                            'flowrate': 0.5,  # cc/s
                        },
                    }
                }
            },
        }


rserver = redis.StrictRedis(host='localhost', port='6379', db=0)
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
server.add_insecure_port('localhost' + ':' + '6666')
server.start()
PistonDispenser = None
shapes = None
# loop = None
tempset_obj = None
pid = 42
program_name = "best program"
program_description = "the answer to life the universe and everything"
program_gcode = "G1 X42\nG1 Y42\nG1 Z42"

error_sources = [0]
error_names = ["zero"]

# State
cpd_errors = list()
state_changes = 0
cpd_state = str()

out_file = open("test_output.txt","w")

run_counter = 0
actions_permutations = "?"

loop = asyncio.get_event_loop()

def initModel():
    global PistonDispenser
    global shapes
    global cpd_state
    global state_changes
    global cpd_errors
    global loop
    global tempset_obj
    global run_counter
    global out_file

    run_counter += 1

    print("\n**************************************")
    print("    Starting Model Run:", run_counter, "/", actions_permutations)
    print("**************************************\n")

    out_file.write("\n*************************")
    out_file.write(" Starting Model Run: " + str(run_counter) + "/" + str(actions_permutations))
    out_file.write("*************************\n")

    tempset_obj = TempSettings()
    shapes = generator_factory(tempset_obj, server, rserver, loop)
    PistonDispenser = shapes[0]

    tasks = [asyncio.ensure_future(cmp.initialize()) for cmp in shapes]
    loop.run_until_complete(asyncio.gather(*tasks))

    loop.run_until_complete(
        PistonDispenser.StoreProgram(
            program_name, program_description, program_gcode, pid)
        )
    state_changes = 0
    out_file.write(str(PistonDispenser._gcode_machine.state_history))
    cpd_state = '->' + PistonDispenser._gcode_machine.state_history.pop(0).name

#### Model

initModel()

def update_state():
    global cpd_state
    global state_changes
    state_changes = len(PistonDispenser._gcode_machine.state_history)
    if state_changes > 0:
        cpd_state = ""
        for step in PistonDispenser._gcode_machine.state_history:
            cpd_state += '->' + step.name
        PistonDispenser._gcode_machine.state_history = []

def update_errors():
    global cpd_errors
    cpd_errors = []
    for kind, source in PistonDispenser._error_locks.items():
        if not len(source):
            continue
        cpd_errors.append(kind)

def resolve_error(x):
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> resolve error action...")
    PistonDispenser.cleared_error_listener(x, True,
        error_names[error_sources.index(x)])
    update_errors()
    update_state()

def block_everything(x):
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> block everything action...")
    loop.run_until_complete(
      PistonDispenser.block_everything(
        x, False, error_names[error_sources.index(x)]))
    update_state()
    update_errors()

def block_program_start(x):
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> block program start action...")
    PistonDispenser.block_program_start(
        x, False, error_names[error_sources.index(x)])
    update_state()
    update_errors()

def require_homing(x):
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> require homing action...")
    loop.run_until_complete(
      PistonDispenser.stop_and_require_homing(
        x, False, error_names[error_sources.index(x)]))
    update_state()
    update_errors()

def spr():
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> spr action...")
    loop.run_until_complete(PistonDispenser.Start(pid))
    time.sleep(0.1)
    loop.run_until_complete(PistonDispenser.Pause())
    time.sleep(0.1)
    loop.run_until_complete(PistonDispenser.Resume())
    time.sleep(0.1)
    update_state()
    update_errors()

def homing():
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> homing action...")
    loop.run_until_complete(PistonDispenser.Homing())
    out_file.write(str(PistonDispenser._gcode_machine.state_history))
    update_state()
    update_errors()

def start():
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> start action...")
    loop.run_until_complete(PistonDispenser.Start(pid))
    out_file.write(str(PistonDispenser._gcode_machine.state_history))
    update_state()
    update_errors()

def stop():
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> stop action...")
    loop.run_until_complete(PistonDispenser.Stop())
    out_file.write(str(PistonDispenser._gcode_machine.state_history))
    update_state()
    update_errors()

def pause():
    global cpd_state
    global out_file
    global cpd_errors
    out_file.write("\n>> pause action...")
    loop.run_until_complete(PistonDispenser.Pause())
    out_file.write(str(PistonDispenser._gcode_machine.state_history))
    update_state()
    update_errors()

def resume():
    global out_file
    global cpd_state
    global cpd_errors
    out_file.write("\n>> resume action...")
    loop.run_until_complete(PistonDispenser.Resume())
    out_file.write(str(PistonDispenser._gcode_machine.state_history))
    update_state()
    update_errors()

def clean():
    loop.close()

def Accepting():
    return False if state_changes else True

def RestartModel():
    global loop
    for task in asyncio.Task.all_tasks(loop):
        task.cancel()
    initModel()

# needed for multiple test runs in one session

def Reset():
    pass

### Metadata

state = ('cpd_state',)
check_state_changes = True

restart = RestartModel
actions = (start, stop, homing, require_homing, resolve_error,)
factor = len(actions)
actions_permutations = 1
while (factor > 0):
    actions_permutations *= factor
    factor -= 1
enablers = {}
domains = {
    block_everything: {
      'x': error_sources,
    },
    require_homing: {
      'x': error_sources,
    },
    block_program_start: {
      'x': error_sources,
    },
    resolve_error: {
      'x': error_sources,
    },
  }

cleanup = ()
