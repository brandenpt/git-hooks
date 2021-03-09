#!/usr/bin/env python3
#
# Copyright 2021 Braden (R) Portuguese company
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.


from __future__ import print_function
import sys
from subprocess import run
import textwrap
import os
from git import Repo
from typing import NamedTuple, Set, Optional
from pathlib import PurePath
from hooksutils import eprint, input_with_timeout, TimeoutExpired
from copyconfigargs import dir_overwrite, file_names_list, \
    needles_dict, default_needle, timeout

# region Functions Definitions
# -----------------------------------------------------------------------------
# SCRIPT FUNCTION AND CLASS DEFINITIONS
# -----------------------------------------------------------------------------


class ParsePluginsFileReturn(NamedTuple):
    compare_lines_set: Set[str]
    preserve_lines: str
    needle: str = default_needle


class ParseMainFileReturn(NamedTuple):
    compare_lines_set: Set[str]
    copy_lines: str
    needle: str = default_needle


class FileToParse(NamedTuple):
    file_path: PurePath
    needle: str = default_needle


def parse_plugins_file(plugins_file_parse: FileToParse) \
        -> ParsePluginsFileReturn:
    with open(plugins_file_parse.file_path, mode="r") as plugins_file:
        lines = plugins_file.read().splitlines(keepends=True)

        needle_index = [i for i, word in enumerate(lines)
                        if word.find(plugins_file_parse.needle) > -1]

        if len(needle_index) > 1:
            eprint("ERROR: More than one needle found in "
                   + plugins_file_parse.file_path.parent.name
                   + "/" + plugins_file_parse.file_path.name)
            sys.exit(11)
        elif len(needle_index) == 0:
            eprint("ERROR: No needle found in "
                   + plugins_file_parse.file_path.parent.name
                   + "/" + plugins_file_parse.file_path.name)
            sys.exit(11)

        needle_index = needle_index.pop()
        lines_to_be_overwritten = [x for i, x in enumerate(lines)
                                   if i < needle_index]

        # Using a set to compare the files
        set_to_be_overwritten = set(map(str.strip, lines_to_be_overwritten))

        lines_to_preserve = "".join(tuple(x for i, x in enumerate(lines)
                                          if i >= needle_index))

        return ParsePluginsFileReturn(set_to_be_overwritten, lines_to_preserve,
                                      plugins_file_parse.needle)


def parse_main_file(main_file_parse: FileToParse) -> ParseMainFileReturn:
    with open(main_file_parse.file_path, mode="r") as main_file:
        lines = main_file.read().splitlines(keepends=True)

        needle_index = [i for i, word in enumerate(lines)
                        if word.find(main_file_parse.needle) > -1]

        if len(needle_index) > 1:
            eprint("ERROR: More than one needle found in "
                   + main_file_parse.file_path.parent.name
                   + "/" + main_file_parse.file_path.name)
            sys.exit(12)
        elif len(needle_index) == 0:
            eprint("ERROR: No needle found in "
                   + main_file_parse.file_path.parent.name
                   + "/" + main_file_parse.file_path.name)
            sys.exit(12)

        needle_index = needle_index.pop()
        lines_to_copy = tuple(x for i, x in enumerate(lines)
                              if i < needle_index)
        set_to_copy = set(map(str.strip, lines_to_copy))

        lines_to_copy = "".join(lines_to_copy)

        return ParseMainFileReturn(set_to_copy, lines_to_copy,
                                   main_file_parse.needle)


def assert_overwrite(set_to_be_overwritten: Set[str],
                     set_to_copy: Set[str], file_path: PurePath) -> bool:
    if set_to_be_overwritten == set_to_copy:
        return False
    else:
        if timeout < -1:
            eprint("ERROR: timeout with the wrong value of " + str(timeout))
            sys.exit(105)
        elif timeout == 0:
            eprint(textwrap.dedent("""\
                ERROR: The {parent_path}/{file_name}
                should be the same as the project's {file_name}.
                Canceling the commit...\
                """.format(parent_path=file_path.parent.name,
                           file_name=file_path.name)))
            sys.exit(1)

        eprint(textwrap.dedent("""\
            ERROR: The {parent_path}/{file_name}
            should be the same as the project's {file_name}.
            You can overwrite the file or cancel the commit.
            """.format(parent_path=file_path.parent.name,
                       file_name=file_path.name)))

        if timeout == -1:
            prompt = "Overwrite the {parent_path}/{file_name} file? " \
                     "[y/N] ".format(parent_path=file_path.parent.name,
                                     file_name=file_path.name)

            overwrite_answer = input(prompt)
            print()
        else:
            prompt = "Overwrite the {parent_path}/{file_name} file? " \
                     "[y/N] ({timeout} seconds to respond) "\
                .format(parent_path=file_path.parent.name,
                        file_name=file_path.name,
                        timeout=timeout)
            try:
                overwrite_answer = input_with_timeout(prompt, timeout)
                print()
            except TimeoutExpired:
                eprint("Canceling the commit...")
                sys.exit(1)

        if overwrite_answer is None \
                or overwrite_answer != "y" and overwrite_answer != "Y":
            eprint("Canceling the commit...")
            sys.exit(1)

        return True


def process_files(main_gradle_path: PurePath,
                  plugins_gradle_path: PurePath,
                  process_needle: Optional[str] = None) -> None:
    if process_needle is None:
        main_gradle_file = FileToParse(main_gradle_path)
        plugins_gradle_file = FileToParse(plugins_gradle_path)
    else:
        main_gradle_file = FileToParse(main_gradle_path, process_needle)
        plugins_gradle_file = FileToParse(plugins_gradle_path, process_needle)

    parsed_main = parse_main_file(main_gradle_file)
    parsed_plugins = parse_plugins_file(plugins_gradle_file)

    do_overwrite = assert_overwrite(parsed_main.compare_lines_set,
                                    parsed_plugins.compare_lines_set,
                                    plugins_gradle_path)

    if do_overwrite:
        # Overwrite the plugins settings file
        with open(plugins_gradle_path, mode="w") as file:
            file.write(parsed_main.copy_lines)

        # Copy the lines to be preserved
        with open(plugins_gradle_path, mode="a") as file:
            file.write(parsed_plugins.preserve_lines)


# endregion

# -----------------------------------------------------------------------------
# START OF THE SCRIPT
# -----------------------------------------------------------------------------

# use git rev-parse to get the project path
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
project_path = PurePath(str(rev_parse.stdout).replace("\n", ""))

# Check if there's something to commit
repo = Repo(project_path)
if repo.bare:
    eprint("ERROR: GitPython repo could not be initialized.")
    sys.exit(-2)

# if there is no staged file then silently exit
# because git is going to throw the error
index = repo.index
if len(list(index.diff("HEAD"))) < 1:
    sys.exit(0)

for file_name in file_names_list:
    main_file_path = PurePath(project_path, file_name)
    plugins_file_path = PurePath(project_path, dir_overwrite,
                                 file_name)
    needle = needles_dict.get(file_name)

    if needle is not None:
        if not needle.isascii():
            eprint("ERROR: %s needle is made of non ASCII characters"
                   % file_name)
            sys.exit(103)
        needle_no_w_char = "".join(needle.split())
        if len(needle_no_w_char) == 0:
            eprint("ERROR: %s needle is empty or is made with only whitespaces"
                   % file_name)
            sys.exit(103)
    else:
        if default_needle is None:
            eprint("ERROR: there must be a default needle")
            sys.exit(103)
        if not default_needle.isascii():
            eprint("ERROR: default needle is made of non ASCII characters")
            sys.exit(103)
        needle_no_w_char = "".join(default_needle.split())
        if len(needle_no_w_char) == 0:
            eprint("ERROR: default needle is empty or is made with only "
                   "whitespaces")
            sys.exit(103)

    process_files(main_file_path, plugins_file_path,
                  needle)

    # Check if this script changed the files and
    # if it did add to the commit
    # Also if one file is added then add the other.
    changedFiles = [item.a_path for item in index.diff(None)]
    if plugins_file_path in changedFiles or main_file_path in changedFiles:
        index.add(plugins_file_path)
        index.add(main_file_path)
