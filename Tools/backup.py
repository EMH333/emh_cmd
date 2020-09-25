#!/usr/bin/env python3

# get the intended destination and type (full, partial, auto)
# get the excluded and included file paths (exclude, include, exclude-words, include-words) #TODO exclude words and include should come first
# combine into command
# run only if not dryrun

from getConfig import get_value, load_configs

load_configs()

baseCommand = "duplicity --asynchronous-upload --allow-source-mismatch"
source = get_value("backup.source")  # TODO make sure not null
exclude_paths = get_value("backup.exclude", [])
include_paths = get_value("backup.include", [])
exclude_words = get_value("backup.exclude-words", [])
include_words = get_value("backup.include-words", [])

# TODO handle destination with more options
destination = get_value("backup.destination.default")

#now start building the command
command = baseCommand + " \\\n"

for e in exclude_words:
    command += " --exclude ignorecase:'**" + e + "**' \\\n"
for i in include_paths:
    command += " --include ignorecase:'" + i + "' \\\n"
for e in exclude_paths:
    command += " --exclude ignorecase:'" + e + "' \\\n"

command += source + " \\\n"
command += destination

print(command)
