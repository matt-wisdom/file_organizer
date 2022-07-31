#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-


# Copyright 2021 Matthew Wisdom
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import os.path as pth
import argparse
import importlib
import logging

logger = logging.getLogger(__name__)

from organizer import DefaultOrganizer

extension = []
desc = """ """
min_levenshtein_help = """This Program uses Levenshtein Distance Algorithm to search for match by
                            default unless the -s or --simple-match options are specified.
                            This option specified the minimun ratio that will be considered a match
                            using partial_set_ratio.
                            Defaults to 75
                        """

recognize_types = "py, html, htm, css, js, cpp, c, rb, pl, php, r, go, java, svg, png, jpg, jpx, gif, webp, cr2, tif, bmp, jxr, psd, ico, heic, mp4, m4v, mkv, webm, mov, avi, wmv, mpg, flv, swf, mid, mp3, m4a, ogg, flac, wav, amr, zip, tar, rar, gz, bz2, 7z, xz, ar, deb, z, lz, exe, cab, pyc, jar, pdf, docx, doc, ppt, pptx, epub, rtf, txt, ps, woff, woff2, ttf, otf"
num = len(recognize_types.split(","))
filetypehelp = f"""Only match files of the path type(s)/extension(s) given. Value can be a single file type like 'pdf' or a comma seperated list of file types like 'pdf,txt,html,exe,zip'.
  There are currently {num} recognized file types and they are: {recognize_types} files.""".format()

extension_help = """Use extension specified where extension is of the form 'parent_dir.child_dir.extension_module:class'\n
or 'extension_module:class' or 'extension_module' where extension_module is a valid extension python file
 """
groups_help = """Number of groups to divide each class (alphas and nums) will be divided into for generating destination directory based on
initials of filenames (used with the -i or --initials arguments) ."""

nomatchdir_help = """Directory to copy or move files to if no match is found. Defaults to ignore. This program allows you to use [:dd:]
		     to reference the directory matched files are moved to (specified with -d or --destination-directory argument). So the move all unmatched files
		     to a folder named 'unknown' in the target directory pass '[:dd:]/unknown' as the value to this argument.
"""

action_help = """The action to carry out on matched files, valid options are: print, move, copy_rename, rename, copy.  Defaults to print.
"""

initials_help = """Use initials of filenames to generate groups. Directories are created with the group name as destination for file operations."""

group_help = """Generate destinations for files using in-built groups. The groups are defined in 
		organizer.py
		"""

genregexphelp = """Used to generate new names for matched files based on strings extracted from filenames using regular expressions."""

gencombhelp = """Used to generate new names for matched files based on various combinations of characters."""

irreversibilityhelp = """Disable reversibility i.e action are not written to action log to provide the ability to reverse action."""

reversehelp = """ Reverse last actions from actions log. """

opcounthelp = "Specifies the maximum number of operations to carry out."

tsstarthelp = """Reverse operations that where carried out on or after this timestamp.
				 If reverse-timestamp-stop is specified, then operations carried out between reverse-timestamp-start and 
				 reverse-timestamp-stop are reversed
			  """

tsstophelp = """Reverse operations that where carried out on or before this timestamp.
				If reverse-timestamp-start is specified, then operations carried out between reverse-timestamp-start and 
				 reverse-timestamp-stop are reversed
			"""


def parse_extension(extension):
    """
    Parse extension argument value and return extension class
    """

    if ":" in extension:
        print("Parsing")
        import os, sys

        sys.path.append(os.getcwd())
        print(os.getcwd())
        # Parser for when custom class name is used for extension in the format 'modulename:class_name'
        module, classname = extension.split(":")
        try:
            print(module)
            imported = importlib.__import__(module)
            return getattr(imported, classname)
        except Exception as e:
            print("Could not load extension ", extension, e)
    # Default extension class name is 'Extension'
    else:
        try:
            imported = importlib.import_module(extension)
            try:
                return getattr(imported, "Extension")
            except Exception as e:
                print("Could not find extension class in ", extension, e)
        except Exception as e:
            print("Could not load extension 2", extension, e)


def run(app_class=DefaultOrganizer, **kwargs):
    global app
    match_count = 0
    operations_count = 0
    opcount = kwargs.get("opcount")
    rtstart = kwargs.get("rtstart")
    regex = kwargs.get("regex")
    rtstop = kwargs.get("rtstop")
    if kwargs.get("extension"):
        print(kwargs.get("extension"))
        app_class = parse_extension(kwargs.get("extension"))
    action_log = kwargs.get("action_log")
    reverse = kwargs.get("reverse")
    if reverse:
        action_log = reverse
    reversible = not kwargs.get("irreversible")
    app = app_class(
        reversible=reversible,
        reverse=reverse,
        action_log=action_log,
        reverse_count=opcount,
        reversetimerangestart=rtstart,
        reversetimerangestop=rtstop,
        newline=kwargs.get("newline"),
    )
    group_gen = getattr(
        app,
        "generate_destination_group",
        getattr(app, "default_generate_destination_group"),
    )
    type_gen = getattr(
        app,
        "generate_destination_type",
        getattr(app, "default_generate_destination_type"),
    )
    others_gen = getattr(app, "generate_destination_others", "")
    dgens = {
        "initials": getattr(app, "default_generate_destination_alphabetic"),
        "group": group_gen,
        "type": type_gen,
        "others": others_gen,
    }
    groups = kwargs.get("groups")
    nomatch_dir = kwargs.get("nomatchdir")
    working_dir = pth.realpath(kwargs.get("directory", "."))
    destination_dir = pth.realpath(kwargs.get("destination_dir", "."))
    simple_match = kwargs.get("simple_match", False)
    recurse = kwargs.get("recursive", False)
    action_function = getattr(app, "action", getattr(app, "default_action"))
    destination_generation = kwargs.get("d_gen", None)
    destination_generation_function = dgens.get(destination_generation)
    action = kwargs.get("action")
    min_ratio = kwargs.get("min_ratio", 70)
    fileextensions = kwargs.get("fileextensions")
    search = kwargs.get("search", "")
    name_gens = {
        "comb": getattr(app, "default_gen_new_name_combination"),
        "regex": getattr(app, "default_gen_new_name_regex"),
    }
    name_gen = name_gens.get(kwargs.get("name_gen"))
    app.case_sensitive = kwargs.get("case_sensitive")
    if fileextensions:
        fileextensions = fileextensions.split(",")
        fileextensions = [
            ext.strip() for ext in fileextensions
        ]  # Allowed extension names can have spaces after the commas

    if simple_match:
        # Check if user provided custom methods and use the default if not
        match_function = getattr(
            app, "simple_search", getattr(app, "default_simple_search")
        )
    else:
        match_function = getattr(
            app, "fuzzy_search", getattr(app, "default_fuzzy_search")
        )

    if recurse:
        # Check if user provided custom methods and use the default if not
        generate_files_function = getattr(
            app, "walk_dir_recursive", getattr(app, "default_walk_dir_recursive")
        )
    else:
        generate_files_function = getattr(
            app, "walk_dir", getattr(app, "default_walk_dir")
        )
    logger.info("Finding...")
    for file in generate_files_function(working_dir, extensions=fileextensions):
        if match_function(search, file, min_ratio):
            match_count += 1
            if opcount:
                if opcount >= match_count:
                    break
            if destination_generation_function:

                des = (
                    destination_generation_function(
                        file,
                        groups=groups,
                        destination_dir=destination_dir,
                        nomatchdir=nomatch_dir,
                    )
                    if nomatch_dir
                    else destination_generation_function(
                        file, groups=groups, destination_dir=destination_dir
                    )
                )
                if des:
                    os.makedirs(des) if not pth.exists(des) and des else donothing()
                    if name_gen:
                        filename = pth.split(file)[1]
                        des = pth.join(
                            des,
                            name_gen(filename, regex) if regex else name_gen(filename),
                        )
                    action_function(file, to=des, action=action)
                    operations_count += 1
            else:
                if destination_dir:
                    if name_gen:
                        filename = pth.split(file)[1]
                        des = pth.join(
                            destination_dir,
                            name_gen(filename, regex) if regex else name_gen(filename),
                        )
                        action_function(file, action=action, to=des)
                        operations_count += 1
                    else:
                        action_function(file, action=action, to=destination_dir)
                        operations_count += 1
                else:
                    if name_gen:
                        filename = pth.split(file)[1]
                        des = pth.join(
                            destination_dir,
                            name_gen(filename, regex) if regex else name_gen(filename),
                        )
                        action_function(file, action=action, to=des)
                        operations_count += 1
                    else:
                        action_function(file, action=action)
                        operations_count += 1
    try:
        app.default_write_action_log()
    except Exception as e:
        logger.exception("[!!!] Could not write to action log: " + str(e))
    logger.info("Finished")
    logger.info(
        " Matches-%d items / Operations-%d operations"
        % (match_count, operations_count)
    )


def donothing():
    pass


def main():
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-s", "--search_string", help="The string to search for.", default=""
    )
    parser.add_argument(
        "-e", "--extension", action="store", dest="extension", help=extension_help
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="The directory to work on.",
        action="store",
        dest="directory",
        default=".",
    )
    parser.add_argument(
        "-z",
        "--destination-directory",
        action="store",
        dest="destination",
        help="Target directory for file operations.",
        default=".",
    )
    parser.add_argument(
        "-m",
        "--min-levenshtein-ratio",
        type=int,
        action="store",
        dest="min_ratio",
        default=75,
        help=min_levenshtein_help,
    )
    parser.add_argument(
        "-b",
        "--groups",
        type=int,
        action="store",
        dest="groups",
        default=5,
        help=groups_help,
    )
    parser.add_argument(
        "-n", "--nomatchdir", action="store", dest="nomatchdir", help=nomatchdir_help
    )
    parser.add_argument(
        "-a",
        "--action",
        action="store",
        dest="action",
        default="print",
        help=action_help,
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        dest="recursive",
        help="Recursively find files.",
    )
    parser.add_argument(
        "-q",
        "--newline",
        action="store_true",
        dest="newline",
        help="Print a newline after each output",
    )
    parser.add_argument(
        "-k",
        "--irreversible",
        action="store_true",
        dest="irreversible",
        help=irreversibilityhelp,
    )
    parser.add_argument(
        "-j",
        "--reverse",
        action="store",
        dest="reverse",
        const="action_log",
        nargs="?",
        help=reversehelp,
    )
    parser.add_argument(
        "-p",
        "--action-log-file",
        action="store",
        dest="action_log",
        default="action_log",
        help="File to log actions for reversibility of operations.",
    )
    parser.add_argument(
        "-u", "--count", action="store", dest="opcount", help=opcounthelp, type=int
    )
    parser.add_argument(
        "--reverse-timestamp-start",
        action="store",
        dest="rtstart",
        help=tsstarthelp,
        type=float,
    )
    parser.add_argument(
        "--reverse-timestamp-stop",
        action="store",
        dest="rtstop",
        help=tsstophelp,
        type=float,
    )

    search_type_group = parser.add_mutually_exclusive_group()
    search_type_group.add_argument(
        "-l",
        "--simple-match",
        action="store_true",
        dest="simple_match",
        help="Simple string match.",
    )
    search_type_group.add_argument(
        "-f",
        "--fuzz-match",
        action="store_false",
        dest="simple_match",
        help="Fuzzy string match.",
    )

    destination_generation_group = parser.add_mutually_exclusive_group()
    destination_generation_group.add_argument(
        "-i", "--initials", action="store_true", dest="initials", help=initials_help
    )
    destination_generation_group.add_argument(
        "-g", "--group", action="store_true", dest="group"
    )
    destination_generation_group.add_argument(
        "-t",
        "--type",
        action="store_true",
        dest="type",
        help="Generate location for matched files by using their filetype.",
    )
    # destination_generation_group.add_argument('-o', '--other', action='store_true', dest='others')

    parser.add_argument(
        "-w",
        "--case-sensitive",
        action="store_true",
        dest="case_sensitive",
        help="Makes regex filename generation case-sensitive",
    )

    name_generation_group = parser.add_mutually_exclusive_group()
    name_generation_group.add_argument(
        "-c",
        "--generate-combinations",
        action="store_true",
        dest="gen_comb",
        help=gencombhelp,
    )
    name_generation_group.add_argument(
        "-x", "--generate-regex", action="store", dest="gen_regex", help=genregexphelp
    )

    parser.add_argument(
        "-y", "--file-types", action="store", dest="fileextensions", help=filetypehelp
    )

    args = parser.parse_args()

    if args.group:
        dgen = "group"
    elif args.type:
        dgen = "type"
    elif args.initials:
        dgen = "initials"
    else:
        dgen = None

    regex = None

    if args.gen_comb:
        name_gen = "comb"
    elif args.gen_regex:
        name_gen = "regex"
        regex = args.gen_regex
    else:
        name_gen = None

    nomatchdir = "" if not args.nomatchdir else args.nomatchdir

    run_args = {
        "search": args.search_string,
        "nomatchdir": args.nomatchdir,
        "directory": args.directory,
        "destination_dir": args.destination,
        "min_ratio": args.min_ratio,
        "simple_match": args.simple_match,
        "recursive": args.recursive,
        "extension": args.extension,
        "d_gen": dgen,
        "groups": args.groups,
        "action": args.action,
        "name_gen": name_gen,
        "regex": regex,
        "fileextensions": args.fileextensions,
        "newline": args.newline,
        "case_sensitive": args.case_sensitive,
        "reverse": args.reverse,
        "irreversible": args.irreversible,
        "action_log": args.action_log,
        "opcount": args.opcount,
        "rtstart": args.rtstart,
        "rtstop": args.rtstop,
    }
    run(**run_args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[INFO] Tidying up...")
        if app.reversible:
            try:
                app.default_write_action_log()
            except:
                print("[!!!] Could not write to action log.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
