#!/usr/bin/env python3
import os
import sys
import json

# load configuration settings
# return value of setting or non-zero exit code if doesn't exit
# settings follow test.test.test to signify "test":{"test":{"test":"This is the output"}}
# settings live in the "config" object of root json object
configVals = dict()


def load_configs():
    home = os.path.expanduser("~") + "/emh.json"
    if not os.path.isfile(home):
        return
    try:
        with open(home) as f:
            config = json.load(f)["config"]
            for setting in config:  # loop through all settings in config
                configVals[setting] = config[setting]
    except json.decoder.JSONDecodeError:
        print("There was an error decoding the JSON file")

# use this from other python programs
def get_value(value, default=""):
    valToGet = value.split('.')
    currentConfig = configVals
    for x in valToGet:
        try:
            currentConfig = currentConfig[x]
        except KeyError:
            return default
    return currentConfig

# only run if run on command line
if __name__ == "__main__":
    if len(sys.argv) == 1: # make sure there is a config val to get
        print("Need more arguments")
        sys.exit(1)

    load_configs()
    default = ""
    if len(sys.argv) > 2: # set the default if there is one
        default = sys.argv[2]
    val = get_value(sys.argv[1], default)

    if val == "": #error if a value isn't found
        print("Setting " + sys.argv[1].split('.')[-1] + " not found")
        sys.exit(1)
    else:
        print(val)
