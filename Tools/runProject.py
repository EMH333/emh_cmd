#!/usr/bin/env python3

import json
import os
import signal
import subprocess
import sys

commands = dict()


def extract_from_commands_object(commands_object):
    types = dict()
    for command in commands_object:  # loop through all programs in home commands
        if "names" in commands_object[command] and isinstance(commands_object[command]["names"],
                                                              list):  # if name is an array, add all aliases to commands
            for name in commands_object[command]["names"]:
                types[name] = commands_object[command]["command"]
        else:
            if "name" in commands_object[command]:  # if program wants to go by different name then definition
                types[commands_object[command]["name"]] = commands_object[command]["command"]
            else:  # just grab name of command
                # grab from command val if defined, else just value of the name val
                if "command" in commands_object[command]:
                    types[command] = commands_object[command]["command"]
                else:
                    types[command] = commands_object[command]
    return types


# loads commands in array from the home emh.json
def load_home_commands():
    home = os.path.expanduser("~") + "/emh.json"
    if not os.path.isfile(home):
        return
    programs_loaded = 0
    try:
        with open(home) as f:
            programs = json.load(f)["commands"]
            new_commands = extract_from_commands_object(programs)
            commands.update(new_commands)
            programs_loaded = len(new_commands)
    except json.decoder.JSONDecodeError:
        print("There was an error decoding the JSON file")

    if programs_loaded > 0:
        print("Loaded " + str(programs_loaded) + " programs from home")


# TODO eventually include npm scripts
def load_current_dir_commands():
    file = "./emh.json"
    if os.path.isfile(file):
        print("Found file")
        try:
            with open(file) as f:
                data = json.load(f)
                directory = os.path.dirname(f.name)
                os.chdir(directory)  # change to that directory

                # load and add to list of commands
                if "commands" in data:
                    new_commands = extract_from_commands_object(data["commands"])
                    commands.update(new_commands)
        except json.decoder.JSONDecodeError:
            print("There was an error decoding the JSON file")
    return False


def run(args):
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))  # remove traceback when exiting

    have_command_to_run: bool = len(args) > 1

    load_home_commands()
    load_current_dir_commands()

    # if a valid command then run it
    if have_command_to_run and sys.argv[1] in commands:
        print("Using Command")
        if len(sys.argv) > 2:
            os.environ["file"] = sys.argv[2]  # export file variable for use if needed as second argument
        subprocess.run(["bash", "-c", commands[sys.argv[1]]])
        return

    if have_command_to_run and not sys.argv[1] in commands:
        print("Invalid command")
        have_command_to_run = False

    # if no commands to run then then print
    if not have_command_to_run and len(commands) > 0:
        print("Commands:")
        for key, value in commands.items():
            print(key)


if __name__ == '__main__':
    run(sys.argv)
