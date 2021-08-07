# fileorg_tool
<pre>
An extensible file searching and organization tool with a couple of features 
including but not limited to fuzzy search and actions reversal

usage: fotools.py [-h] [-s SEARCH_STRING] [-e EXTENSION] [-d DIRECTORY]
                 [-z DESTINATION] [-m MIN_RATIO] [-b GROUPS] [-n NOMATCHDIR]
                 [-a ACTION] [-r] [-q] [-k] [-j [REVERSE]] [-p ACTION_LOG]
                 [-u OPCOUNT] [--reverse-timestamp-start RTSTART]
                 [--reverse-timestamp-stop RTSTOP] [-l | -f] [-i | -g | -t]
                 [-w] [-c | -x GEN_REGEX] [-y FILEEXTENSIONS]

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH_STRING, --search_string SEARCH_STRING
                        The string to search for.
  -e EXTENSION, --extension EXTENSION
                        Use extension specified where extension is of the form
                        'parent_dir.child_dir.extension_module:class' or
                        'extension_module:class' or 'extension_module' where
                        extension_module is a valid extension python file
  -d DIRECTORY, --directory DIRECTORY
                        The directory to work on.
  -z DESTINATION, --destination-directory DESTINATION
                        Target directory for file operations.
  -m MIN_RATIO, --min-levenshtein-ratio MIN_RATIO
                        This Program uses Levenshtein Distance Algorithm to
                        search for match by default unless the -s or --simple-
                        match options are specified. This option specified the
                        minimun ratio that will be considered a match using
                        partial_set_ratio. Defaults to 75
  -b GROUPS, --groups GROUPS
                        Number of groups each class (alphas and
                        nums) will be divided into for generating destination
                        directory from the initials of filenames (used with
                        the -i or --initials arguments) .
  -n NOMATCHDIR, --nomatchdir NOMATCHDIR
                        Directory to copy or move files to if it does not  
                        match the search parameters.
                        Defaults to ignore. This program allows you to
                        use [:dd:] to reference the directory matched files
                        are moved to (specified with -d or --destination-
                        directory argument). So the move all unmatched files
                        to a folder named 'unknown' in the target directory
                        pass '[:dd:]/unknown' as the value to this argument.
  -a ACTION, --action ACTION
                        The action to carry out on matched files, valid
                        options are: print, move, copy_rename, rename, copy.
                        Defaults to print.
  -r, --recursive       Recursively find files.
  -q, --newline         Print a newline after each output
  -k, --irreversible    Disable reversibility i.e action are not written to
                        action log to provide the ability to reverse action.
  -j [REVERSE], --reverse [REVERSE]
                        Reverse last actions from actions log.
  -p ACTION_LOG, --action-log-file ACTION_LOG
                        File to log actions for reversibility of operations.
  -u OPCOUNT, --count OPCOUNT
                        Specifies the number of operations to carry out.
  --reverse-timestamp-start RTSTART
                        Reverse operations that where carried out on or after
                        this timestamp. If reverse-timestamp-stop is
                        specified, then operations carried out between
                        reverse-timestamp-start and reverse-timestamp-stop are
                        reversed
  --reverse-timestamp-stop RTSTOP
                        Reverse operations that where carried out on or before
                        this timestamp. If reverse-timestamp-start is
                        specified, then operations carried out between
                        reverse-timestamp-start and reverse-timestamp-stop are
                        reversed
  -l, --simple-match    Simple string match.
  -f, --fuzz-match      Fuzzy string match.
  -i, --initials        Use initials of filenames to generate groups. Directories
                        are created with the group name as destination for file
                        operations.
  -g, --group           Generate destinations for files using in-built groups. The groups are defined in 
                        organizer.py
  -t, --type            Generate location for matched files by using their
                        filetype.
  -w, --case-sensitive  Makes regex filename generation case-sensitive
  -c, --generate-combinations
                        Used to generate new names for matched files based on
                        various combinations of characters.
  -x GEN_REGEX, --generate-regex GEN_REGEX
                        Used to generate new names for matched files based on
                        strings extracted from filenames using regular
                        expressions.
  -y FILEEXTENSIONS, --file-types FILEEXTENSIONS
                        Only match files of the path type(s)/extension(s)
                        given. Value can be a single file type like 'pdf' or a
                        comma seperated list of file types like
                        'pdf,txt,html,exe,zip'. There are currently 71
                        recognized file types and they are: py, html, htm,
                        css, js, cpp, c, rb, pl, php, r, go, java, svg, png,
                        jpg, jpx, gif, webp, cr2, tif, bmp, jxr, psd, ico,
                        heic, mp4, m4v, mkv, webm, mov, avi, wmv, mpg, flv,
                        swf, mid, mp3, m4a, ogg, flac, wav, amr, zip, tar,
                        rar, gz, bz2, 7z, xz, ar, deb, z, lz, exe, cab, pyc,
                        jar, pdf, docx, doc, ppt, pptx, epub, rtf, txt, ps,
                        woff, woff2, ttf, otf files.
                        
</pre>                 
**Extending fotools**
<pre>
To extend fotools, all you need do is create a python file with a class named
'Extension' or whatever you want, import and inherit the DefaultOrganizer class 
from organizer.py and create methods for whatever feature you need to extend.
To extend a method simply create a similar method with name similar to that 
of the method name without the 'default_' prepended to it e.g 'default_fuzzy_search'
becomes 'fuzzy_search'.
To use the extension simply supply the -e or --extension argument with the value set
to the importable module if the extension class is named 'Extension' else prepend a
semicolon to the custom class name and append it to the module name.
E.G if the module is named 'myextension.py' in the current working directory and the
classname is 'ReverseExtension' then the value to -e (or --extension) is 
'myextension:ReverseExtension'.
</pre>
