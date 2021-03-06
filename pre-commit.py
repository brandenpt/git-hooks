#!/usr/bin/env python3
from __future__ import print_function
import sys
from subprocess import run
import textwrap
from threading import Timer
from git import Repo
import git


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


rev_parse = run(["git", "rev-parse", "--show-toplevel"], text=True)

if rev_parse.returncode != 0 or rev_parse.stderr is not None \
        or rev_parse.stdout is None:
    eprint("ERROR: Git repository directory not found.")
    sys.exit(-1)

# rev_parse is already a string because of text=True argument
# I only use str() to not get an IDE complain
project_dir = str(rev_parse.stdout).replace("\n", "")
main_gradle_settings_dir = project_dir + "/settings.gradle.kts"
plugins_gradle_settings_dir = project_dir \
                              + "/build-config-plugins/settings.gradle.kts"

needle = "//build-config-plugins-needle"
# Save the part after the needle
with open(plugins_gradle_settings_dir, mode="r+") as plugins_gradle_settings:
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
                         if i < needle_index.pop()]
        set_to_copy = set(map(str.strip, lines_to_copy))

        lines_to_copy = "".join(lines_to_copy)

        if set_to_be_overwritten != set_to_copy:
            eprint(textwrap.dedent("""\
            ERROR: The build-config-plugins' settings.gradle.kts
            should be the same as the project's settings.gradle.kts.
            You can overwrite the file or cancel the commit.
            """))

            timeout = 5
            t = Timer(timeout, print, ["Canceling the commit..."])
            t.start()
            prompt = "Overwrite the build-config-plugins' settings file? " \
                     "[y/N] (%d seconds to respond)\n" % timeout
            overwrite_answer = input(prompt)
            t.cancel()

            if overwrite_answer is None \
                    or overwrite_answer != "y" and overwrite_answer != "Y":
                sys.exit(1)

        plugins_gradle_settings.write(lines_to_copy)

with open(plugins_gradle_settings_dir, mode="a") as plugins_gradle_settings:
    plugins_gradle_settings.write(lines_to_preserve)

repo = Repo(project_dir)
if repo.bare:
    eprint("ERROR: GitPython repo could not be initialized.")
    sys.exit(-2)

repo.index.add(plugins_gradle_settings_dir)
