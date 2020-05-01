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


load_configs()
valToGet = sys.argv[1].split('.')
currentConfig = configVals
for x in valToGet:
    try:
        currentConfig = currentConfig[x]
    except KeyError:
        if len(sys.argv) > 2:
            currentConfig = sys.argv[2]
        else:
            print("Setting %s not found" % x)
            sys.exit(1)


print(currentConfig)
