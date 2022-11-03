import importlib
import os
import os.path as pth
from fotool.parser import parser
from fotool.help import *
from fotool.organizer import DefaultOrganizer
from . import logger


extension = []


def parse_extension(extension):
    """
    Parse extension argument value and return extension class
    """

    if ":" in extension:
        # Parser for when custom class name is used for extension in the format
        #  'modulename:class_name'
        module, classname = extension.split(":")
        try:
            imported = importlib.import_module(f"extensions.{module}")
            return getattr(imported, classname)
        except (AttributeError, ModuleNotFoundError):
            logger.error("Could not load extension " + extension)
    # Default extension class name is 'Extension'
    else:
        try:
            imported = importlib.import_module(f"extensions.{extension}")
            try:
                return getattr(imported, "Extension")
            except AttributeError:
                logger.error(
                    "Could not find extension class in " + str(extension))
        except Exception as e:
            logger.error("Could not load extension " + str(e))


def run(app_class=DefaultOrganizer, **kwargs):
    global app
    match_count = 0
    operations_count = 0
    opcount = kwargs.get("opcount")
    rtstart = kwargs.get("rtstart")
    regex = kwargs.get("regex")
    rtstop = kwargs.get("rtstop")
    if kwargs.get("extension"):
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
            app,
            "walk_dir_recursive",
            getattr(app, "default_walk_dir_recursive")
        )
    else:
        generate_files_function = getattr(
            app, "walk_dir", getattr(app, "default_walk_dir")
        )
    logger.info("Finding...")
    for file in generate_files_function(
            working_dir, extensions=fileextensions):
        if match_function(search, file, min_ratio):
            match_count += 1
            if opcount:
                if opcount <= match_count - 1:
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
                    os.makedirs(des) if not pth.exists(des) and des\
                        else donothing()
                    if name_gen:
                        filename = pth.split(file)[1]
                        des = pth.join(
                            des,
                            name_gen(filename, regex) if regex
                            else name_gen(filename),
                        )
                    action_function(file, to=des, action=action)
                    operations_count += 1
            else:
                if destination_dir:
                    if name_gen:
                        filename = pth.split(file)[1]
                        des = pth.join(
                            destination_dir,
                            name_gen(filename, regex) if regex
                            else name_gen(filename),
                        )
                        action_function(file, action=action, to=des)
                        operations_count += 1
                    else:
                        action_function(
                            file,
                            action=action,
                            to=destination_dir)
                        operations_count += 1
                else:
                    if name_gen:
                        filename = pth.split(file)[1]
                        des = pth.join(
                            destination_dir,
                            name_gen(filename, regex) if regex
                            else name_gen(filename),
                        )
                        action_function(file, action=action, to=des)
                        operations_count += 1
                    else:
                        action_function(file, action=action)
                        operations_count += 1
    try:
        app.default_write_action_log()
    except Exception as e:
        logger.info("Could not write to action log: " + str(e))
    logger.info("Finished")
    logger.info(
        "Matches-%d items / Operations-%d operations"
        % (match_count, operations_count)
    )


def donothing():
    pass


def main():
    try:
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
    except Exception as e:
        print("Tidying up...", e)
        if app.reversible:
            try:
                app.default_write_action_log()
            except Exception as e:
                logger.error("Could not write to action log." + str(e))
