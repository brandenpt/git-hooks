#!/usr/bin/env python3
from __future__ import print_function
import sys
from subprocess import run
import textwrap
import signal
import os
from git import Repo


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class TimeoutExpired(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeoutExpired


def input_with_timeout(input_prompt, input_timeout):
    # set signal handler
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(input_timeout)  # produce SIGALRM in `timeout` seconds

    try:
        return input(input_prompt)
    finally:
        signal.alarm(0)  # cancel alarm


rev_parse = run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                text=True)

if rev_parse.returncode != 0 or rev_parse.stdout is None \
        or (rev_parse.stderr is not None
            and rev_parse.stderr == rev_parse.stdout):
    # Should not be happening if this script is called by pre-commit.
    eprint("ERROR: Git repository directory not found in " + os.getcwd())
    sys.exit(-1)

# rev_parse is already a string because of text=True argument
# I only use str() to not get an IDE complain
project_dir = str(rev_parse.stdout).replace("\n", "")
main_gradle_settings_dir = project_dir + "/settings.gradle.kts"
plugins_gradle_settings_dir = project_dir \
                              + "/build-config-plugins/settings.gradle.kts"

# Check if there's something to commit
repo = Repo(project_dir)
if repo.bare:
    eprint("ERROR: GitPython repo could not be initialized.")
    sys.exit(-2)

# if there is no staged file then silently exit
index = repo.index
if len(list(index.diff("HEAD"))) < 1:
    exit(0)

needle = "//build-config-plugins-needle"
# Save the part after the needle
with open(plugins_gradle_settings_dir, mode="r") as plugins_gradle_settings:
    lines = plugins_gradle_settings.read().splitlines(keepends=True)

    needle_index = [i for i, word in enumerate(lines)
                    if word.startswith(needle)]

    if len(needle_index) > 1:
        eprint("ERROR: More than one needle found in "
               "build-config-plugins/settings.gradle.kts")
        sys.exit(11)

    needle_index = needle_index.pop()
    lines_to_be_overwritten = [x for i, x in enumerate(lines)
                               if i < needle_index]

    # Using a set to compare the files
    set_to_be_overwritten = set(map(str.strip, lines_to_be_overwritten))

    lines_to_preserve = [x for i, x in enumerate(lines)
                         if i >= needle_index]
    lines_to_preserve = "".join(lines_to_preserve)

    with open(main_gradle_settings_dir, mode="r+") as main_gradle_settings:
        lines = main_gradle_settings.read().splitlines(keepends=True)

        needle_index = [i for i, word in enumerate(lines)
                        if word.startswith(needle)]

        if len(needle_index) > 1:
            eprint("ERROR: More than one needle found in "
                   "settings.gradle.kts")
            sys.exit(12)

        needle_index = needle_index.pop()
        lines_to_copy = [x for i, x in enumerate(lines)
                         if i < needle_index]
        set_to_copy = set(map(str.strip, lines_to_copy))

        lines_to_copy = "".join(lines_to_copy)

        if set_to_be_overwritten == set_to_copy:
            sys.exit(0)
        else:
            eprint(textwrap.dedent("""\
            ERROR: The build-config-plugins' settings.gradle.kts
            should be the same as the project's settings.gradle.kts.
            You can overwrite the file or cancel the commit.
            """))

            timeout = 5
            prompt = "Overwrite the build-config-plugins' settings file? " \
                     "[y/N] (%d seconds to respond) " % timeout
            try:
                overwrite_answer = input_with_timeout(prompt, timeout)
                print()
            except TimeoutExpired:
                eprint("Canceling the commit...")
                sys.exit(1)
            else:
                if overwrite_answer is None \
                        or overwrite_answer != "y" and overwrite_answer != "Y":
                    eprint("Canceling the commit...")
                    sys.exit(1)

# Overwrite the plugins settings file
with open(plugins_gradle_settings_dir, mode="w") as plugins_gradle_settings:
    plugins_gradle_settings.write(lines_to_copy)
with open(plugins_gradle_settings_dir, mode="a") as plugins_gradle_settings:
    plugins_gradle_settings.write(lines_to_preserve)

# Check if this script changed the files and
# if it did add to the commit
changedFiles = [ item.a_path for item in index.diff(None) ]
if plugins_gradle_settings_dir in changedFiles:
    index.add(plugins_gradle_settings_dir)

    if main_gradle_settings_dir in changedFiles:
        index.add(main_gradle_settings_dir)
