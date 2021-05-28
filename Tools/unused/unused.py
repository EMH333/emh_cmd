import sys
import subprocess
from pathlib import Path


def find_all_files_with_extension(cwd, ext):
    """
    Find all files in a directory that have a certain extension, ignoring case
    :param cwd: directory
    :param ext: extension
    :return: a list of all the file paths
    """
    glob = "*."
    for i, v in enumerate(ext):
        glob += "["
        glob += ext.lower()
        glob += ext.upper()
        glob += "]"
    return list(Path(cwd).rglob(glob))


def file_has_uses(file, cwd):
    """
    Determines if a file might have a use, errors on the side of caution so strips of extensions before searching
    :param file: file to search for, in form of file path
    :param cwd: directory
    :return: if the file is used
    """
    name = file.name.split(".")[0]
    command = subprocess.run(['rg', name, cwd, '--count-matches', '--color=never', '--ignore-case'],
                             capture_output=True)
    if len(command.stdout) > 0:
        return True
    return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please supply the directory to work in and the file extension to focus on")
        sys.exit()

    has_rg = subprocess.run(['which', 'rg'], capture_output=True)
    if len(has_rg.stdout) == 0:
        print("Please install ripgrep")
        sys.exit()

    working_dir = sys.argv[1]
    file_extension = sys.argv[2]

    print("CWD:", working_dir, ", extension:", file_extension)
    files = find_all_files_with_extension(working_dir, file_extension)

    used_files = list()

    print("Going through", len(files), "files")
    for f in files:
        if not file_has_uses(f, working_dir):
            print(str(f))
        else:
            used_files.append(f)

    print("Files unused:", len(files) - len(used_files))
    print("Used files:", used_files)
