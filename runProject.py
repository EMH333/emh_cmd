import os, sys, json, subprocess, signal

types = dict(python="python3 $file",
             golang="go run $file",
             java="javac $file && java ${file%.*}",
             node="node $file",
             nodemon="nodemon $file")


# loads commands in array from the home emh.json
def load_home_commands():
    home = os.path.expanduser("~") + "/emh.json"
    if not os.path.isfile(home):
        return
    programs_loaded = 0
    try:
        with open(home) as f:
            prgms = json.load(f)
            for command in prgms:  # loop through all programs in home commands
                if isinstance(command["name"], list):  # if name is an array, add all aliases to commands
                    for name in command["name"]:
                        types[name] = command["command"]
                else:
                    types[command["name"]] = command["command"]
                programs_loaded += 1
    except json.decoder.JSONDecodeError:
        print("There was an error decoding the JSON file")

    if programs_loaded > 0:
        print("Loaded " + str(programs_loaded) + " programs from home")


def run():
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))  # remove traceback when exiting

    file = "./emh.json"
    if not os.path.isfile("./emh.json"):
        print("emh.json not found in local directory")

    # if there is a command that is being asked to run, and it exists in emh.json files, run it
    load_home_commands()
    if len(sys.argv) > 1 and sys.argv[1] in types:
        print("Using Command")
        if len(sys.argv) > 2:
            os.environ["file"] = sys.argv[2]  # export file variable for use if needed as second argument
        subprocess.run(["bash", "-c", types[sys.argv[1]]])
        return

    if os.path.isfile(file):
        print("Found file")
        try:
            with open(file) as f:
                data = json.load(f)
                directory = os.path.dirname(f.name)
                os.chdir(directory)  # change to that directory

                # TODO let per dir emh.json also be an array or a plain object. if array, should have command named "default" or
                # TODO an unnamed command that will be run when emh run is called without arguments
                if "type" in data and "file" in data:
                    # look up command to run and run it on file
                    if data["type"] in types:
                        custom_env = os.environ.copy()
                        os.environ["file"] = data["file"]  # make sure the program knows what file to run
                        subprocess.run(["bash", "-c", types[data["type"]]])  # run command with a type and file
                        return
                    else:
                        print("Sorry, don't know how to run that type of program")

                if "command" in data:
                    subprocess.run(["bash", "-c", data["command"]])  # run command in config
                    return

        except json.decoder.JSONDecodeError:
            print("There was an error decoding the JSON file")
    else:
        print("File not found:")
        print(file)


run()
