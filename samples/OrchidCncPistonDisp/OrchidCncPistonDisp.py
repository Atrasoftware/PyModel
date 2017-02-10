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

loop = asyncio.get_event_loop()

def initModel():
    global PistonDispenser
    global shapes
    global cpd_state
    global state_changes
    global cpd_errors
    global loop
    global tempset_obj

    tempset_obj = TempSettings()
    shapes = generator_factory(tempset_obj, server, rserver, loop)
    PistonDispenser = shapes[0]

    tasks = [asyncio.ensure_future(cmp.initialize()) for cmp in shapes]
    loop.run_until_complete(asyncio.gather(*tasks))

    loop.run_until_complete(
        PistonDispenser.StoreProgram(
            program_name, program_description, program_gcode, pid)
        )

    # class States(Enum):
    #     """These states should be the same as in the proto"""
    #     NOT_HOMED = 0  # Not yet homed
    #     RUNNING = 1  # Currently executing a program
    #     ERROR = 2  # Error status
    #     HOMING = 3  # I'm homing
    #     IDLE = 4  # I'm waiting for a program, always == to the park position
    #     PAUSED = 5  # I can just resume
    #     STOPPED = 6  # Stop command, I can resume or park
    #     JOG = 7

    # channel = grpc.insecure_channel('localhost:6666')
    # cpd_stub = interface_pb2.CncPistonDispStub(channel)
    # cpd_empty = interface_pb2.Empty()
    # get_stats = interface_pb2.Settings()
    # set_stats = interface_pb2.Settings()
    state_changes = 0
    cpd_state = '->' + PistonDispenser._gcode_machine.state_history.pop(0).name
    print("* Must be NOT_HOMED, but it is: ", cpd_state)
    print("* Must be NULL, but it is: ", PistonDispenser._gcode_machine.state_history)
    # state_watcher = Watcher(PistonDispenser._gcode_machine.state.name)

    # def cpd_status_watcher():
    #     global state_watcher
    #     while True:
    #         state_watcher.set_value(PistonDispenser._gcode_machine.state.name)
    #
    # thread = threading.Thread(target=cpd_status_watcher, args=())
    # thread.daemon = True
    # thread.start()

    # def cpd_status_streamer():
    #   machine_status = cpd_stub.MachineStatus(cpd_empty)
    #   global cpd_state
    #   for current in machine_status:
    #     cpd_state = current.state
    #
    # thread = threading.Thread(target=cpd_status_streamer, args=())
    # thread.daemon = True
    # thread.start()
    # ### Model

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
    global cpd_state
    global cpd_errors
    print("resolve error action...")
    PistonDispenser.cleared_error_listener(x, True,
        error_names[error_sources.index(x)])
    update_errors()
    update_state()

def block_everything(x):
    global cpd_state
    global cpd_errors
    print("block everything action...")
    loop.run_until_complete(
      PistonDispenser.block_everything(
        x, False, error_names[error_sources.index(x)]))
    update_state()
    update_errors()

def block_program_start(x):
    global cpd_state
    global cpd_errors
    print("block program start action...")
    PistonDispenser.block_program_start(
        x, False, error_names[error_sources.index(x)])
    update_state()
    update_errors()

def require_homing(x):
    global cpd_state
    global cpd_errors
    print("require homing action...")
    loop.run_until_complete(
      PistonDispenser.stop_and_require_homing(
        x, False, error_names[error_sources.index(x)]))
    update_state()
    update_errors()

def spr():
    global cpd_state
    global cpd_errors
    print("spr action...")
    loop.run_until_complete(PistonDispenser.Start(pid))
    time.sleep(0.1)
    loop.run_until_complete(PistonDispenser.Pause())
    time.sleep(0.1)
    loop.run_until_complete(PistonDispenser.Resume())
    time.sleep(0.1)
    update_state()
    update_errors()

def homing():
    global cpd_state
    global cpd_errors
    print("homing action...")
    loop.run_until_complete(PistonDispenser.Homing())
    print(PistonDispenser._gcode_machine.state_history)
    update_state()
    update_errors()

def start():
    global cpd_state
    global cpd_errors
    print("start action...")
    loop.run_until_complete(PistonDispenser.Start(pid))
    print(PistonDispenser._gcode_machine.state_history)
    update_state()
    update_errors()

def stop():
    global cpd_state
    global cpd_errors
    print("stop action...")
    loop.run_until_complete(PistonDispenser.Stop())
    print(PistonDispenser._gcode_machine.state_history)
    update_state()
    update_errors()

def pause():
    global cpd_state
    global cpd_errors
    print("pause action...")
    loop.run_until_complete(PistonDispenser.Pause())
    print(PistonDispenser._gcode_machine.state_history)
    update_state()
    update_errors()

def resume():
    global cpd_state
    global cpd_errors
    print("resume action...")
    loop.run_until_complete(PistonDispenser.Resume())
    print(PistonDispenser._gcode_machine.state_history)
    update_state()
    update_errors()

def clean():
    loop.close()

def Accepting():
    return False if state_changes else True

def RestartModel():
    global loop
    print(tempset_obj.SPECIFIC_SETTINGS)
    for task in asyncio.Task.all_tasks(loop):
        task.cancel()
    # loop.close()
    print(tempset_obj.SPECIFIC_SETTINGS)
    initModel()

# needed for multiple test runs in one session

def Reset():
    pass

### Metadata

state = ('cpd_state',)
check_state_changes = True

restart = RestartModel
actions = (start, stop, homing, )
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
