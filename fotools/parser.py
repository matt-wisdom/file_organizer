import argparse

from fotools.help import *

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
    "-n",
    "--nomatchdir",
    action="store",
    dest="nomatchdir",
    help=nomatchdir_help
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
    help="print a newline after each output",
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
    "-i",
    "--initials",
    action="store_true",
    dest="initials",
    help=initials_help
)
destination_generation_group.add_argument(
    "-g",
    "--group",
    action="store_true",
    dest="group"
)
destination_generation_group.add_argument(
    "-t",
    "--type",
    action="store_true",
    dest="type",
    help="Generate location for matched files by using their filetype.",
)

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
    "-x",
    "--generate-regex",
    action="store",
    dest="gen_regex",
    help=genregexphelp
)

parser.add_argument(
    "-y",
    "--file-types",
    action="store",
    dest="fileextensions",
    help=filetypehelp
)

parser.add_argument(
    "--install-extension",
    action="store",
    metavar="EXTENSION_NAME",
    dest="install_extension",
    help=install_extension_help
)

parser.add_argument(
    "--list-extensions",
    dest="list_extensions",
    action="store_true",
    help=list_extensions_help
)

parser.add_argument(
    "--extension-help",
    dest="get_extension_help",
    action="store",
    metavar="EXTENSION_NAME",
    help="""View an extension module docstring"""
)
