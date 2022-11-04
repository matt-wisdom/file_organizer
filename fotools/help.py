desc = """ """
min_levenshtein_help = """This Program uses Levenshtein Distance Algorithm to
                          search for match by default unless the -s or
                           --simple-match options are specified.
                          This option specified the minimun ratio that will be
                          considered a match using partial_set_ratio.

                          Defaults to 75
                        """

recognize_types = ("py, html, htm, css, js, cpp, c, rb, pl, php, r, go,"
                   "java, svg, png, jpg, jpx, gif, webp, cr2, tif, bmp, jxr,"
                   "psd, ico, heic, mp4, m4v, mkv, webm, mov, avi, wmv, mpg,"
                   "flv, swf, mid, mp3, m4a, ogg, flac, wav, amr, zip, tar,"
                   "rar, gz, bz2, 7z, xz, ar, deb, z, lz, exe, cab, pyc, jar,"
                   "pdf, docx, doc, ppt, pptx, epub, rtf, txt, ps, woff,"
                   "woff2, ttf, otf, md")

num = len(recognize_types.split(","))
filetypehelp = f"""Only match files of the path type(s)/extension(s) given.
  Value can be a single file type like 'pdf' or a comma seperated list of file
  types like 'pdf,txt,html,exe,zip'.
  There are currently {num} recognized file types and they are:
  {recognize_types} files.""".format()

extension_help = """Use extension specified where extension is of the form
  'parent_dir.child_dir.extension_module:class'\n or 'extension_module:class'
  or 'extension_module' where  extension_module is a valid extension python
  file
 """
groups_help = """Number of groups to divide each class (alphas and nums) will
be divided into for generating destination directory based on
initials of filenames (used with the -i or --initials arguments) ."""

nomatchdir_help = """Directory to copy or move files to if no match is found.
  Defaults to ignore. This program allows you to use [:dd:]
  to reference the directory matched files are moved to (specified with -d or
  --destination-directory argument). So the move all unmatched files
             to a folder named 'unknown' in the target directory pass
             '[:dd:]/unknown' as the value to this argument.
"""

action_help = """The action to carry out on matched files, valid options are:
print, move, copy_rename, rename, copy.  Defaults to print. You can also
add custom actions in extensions
"""

initials_help = """Use initials of filenames to generate groups.
Directories are created with the group name as destination for file
operations."""

group_help = """Generate destinations for files using in-built groups.
The groups are defined in organizer.py"""

genregexphelp = """Used to generate new names for matched files based of
strings extracted from filenames using regular expressions."""

gencombhelp = """Used to generate new names for matched files based on various
combinations of characters."""

irreversibilityhelp = """Disable reversibility i.e action are not written to
actionlog to provide the ability to reverse action."""

reversehelp = """ Reverse last actions from actions log. """

opcounthelp = "Specifies the maximum number of operations to carry out."

tsstarthelp = """Reverse operations that where carried out on or after this
timestamp.
If reverse-timestamp-stop is specified, then operations carried out between
reverse-timestamp-start and reverse-timestamp-stop are reversed
"""

tsstophelp = """Reverse operations that where carried out on or before
this timestamp.
If reverse-timestamp-start is specified, then operations carried out between
reverse-timestamp-start and reverse-timestamp-stop are reversed
"""

install_extension_help = """Install a file as an extension"""

list_extensions_help = """List installed extensions"""
