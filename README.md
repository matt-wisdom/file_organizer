# fileorg_tool
![test_status](https://github.com/matt-wisdom/file_organizer/actions/workflows/main.yml/badge.svg?event=push)


## Features
fotools is an extensible file searching and organization tool.  
It can help you:
 1. Organize your files into alphabetic groups e.g a-e, f-z
 2. Organize your files by file type e.g pdf, html, mpeg files
 3. Organize your files by type groups e.g Source codes, Audio, Videos, Documents
 4. Search for files using fuzzy search with tunable ratio
 5. Rename files using regex extracted part from their names
 6. Reverse the above actions.

## Examples

Lets examine some scenarios where thi program will be useful.  
Say we have the following folder structure.
```
files
├── bg2.jpg
├── bg4.jpg
├── bg5.jpg
├── bg.jpg
├── blog.js
├── elf.png
├── facebook.png
├── favicon.ico
├── fonts
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── adventpro.ttf
│   ├── LICENSE.txt
│   ├── logo.png
│   ├── luckiest-guy.zip
│   ├── Roboto-BlackItalic.ttf
│   └── Roboto-Black.ttf
├── jquery.js
├── photo1.jpg
├── Roboto.zip
├── RSS.png
├── sunset.png
└── webdes.jpg

```
We'll start simple.

**To list all png/jpg files**
<pre><font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ fotool.py -y png,jpg -r 
/home/wisdom/yun/files/RSS.png
/home/wisdom/yun/files/bg.jpg
/home/wisdom/yun/files/webdes.jpg
/home/wisdom/yun/files/elf.png
/home/wisdom/yun/files/bg4.jpg
/home/wisdom/yun/files/bg5.jpg
/home/wisdom/yun/files/bg2.jpg
/home/wisdom/yun/files/sunset.png
/home/wisdom/yun/files/photo1.jpg
/home/wisdom/yun/files/favicon.ico
/home/wisdom/yun/files/facebook.png
/home/wisdom/yun/files/fonts/1.jpg
/home/wisdom/yun/files/fonts/2.jpg
/home/wisdom/yun/files/fonts/logo.png</pre>

**To use fuzzy search to find "LCENSE"**
<pre><font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ fotool.py -s LCENSE -r
/home/wisdom/yun/files/fonts/LICENSE.txt
</pre>

**To organize the files into groups**
<pre><font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ fotool -a move -r -g
<font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ tree
<font color="#42A5F5"><b>.</b></font>
├── action_log
├── <font color="#42A5F5"><b>Archives</b></font>
│   ├── <font color="#C3D82C"><b>luckiest-guy.zip</b></font>
│   └── <font color="#C3D82C"><b>Roboto.zip</b></font>
├── <font color="#42A5F5"><b>Documents</b></font>
│   └── <font color="#C3D82C"><b>LICENSE.txt</b></font>
├── <font color="#42A5F5"><b>fonts</b></font>
├── <font color="#42A5F5"><b>Fonts</b></font>
│   ├── <font color="#C3D82C"><b>adventpro.ttf</b></font>
│   ├── <font color="#C3D82C"><b>Roboto-BlackItalic.ttf</b></font>
│   └── <font color="#C3D82C"><b>Roboto-Black.ttf</b></font>
├── <font color="#42A5F5"><b>Images</b></font>
│   ├── <font color="#C3D82C"><b>1.jpg</b></font>
│   ├── <font color="#C3D82C"><b>2.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg2.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg4.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg5.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg.jpg</b></font>
│   ├── <font color="#C3D82C"><b>elf.png</b></font>
│   ├── <font color="#C3D82C"><b>facebook.png</b></font>
│   ├── <font color="#C3D82C"><b>favicon.ico</b></font>
│   ├── <font color="#C3D82C"><b>logo.png</b></font>
│   ├── <font color="#C3D82C"><b>photo1.jpg</b></font>
│   ├── <font color="#C3D82C"><b>RSS.png</b></font>
│   ├── <font color="#C3D82C"><b>sunset.png</b></font>
│   └── <font color="#C3D82C"><b>webdes.jpg</b></font>
└── <font color="#42A5F5"><b>Source_Codes</b></font>
    ├── <font color="#C3D82C"><b>blog.js</b></font>
    └── <font color="#C3D82C"><b>jquery.js</b></font>
</pre>

<b>To reverse the above action or any action that's happened in this folder</b>
<pre>
wisdom@wisdom:~/yun/files$ fotool -j 
/home/wisdom/yun/files/RSS.png
/home/wisdom/yun/files/bg.jpg
/home/wisdom/yun/files/webdes.jpg
/home/wisdom/yun/files/elf.png
/home/wisdom/yun/files/bg4.jpg
/home/wisdom/yun/files/bg5.jpg
/home/wisdom/yun/files/bg2.jpg
/home/wisdom/yun/files/sunset.png
/home/wisdom/yun/files/blog.js
/home/wisdom/yun/files/action_log
/home/wisdom/yun/files/jquery.js
/home/wisdom/yun/files/photo1.jpg
/home/wisdom/yun/files/Roboto.zip
/home/wisdom/yun/files/favicon.ico
/home/wisdom/yun/files/facebook.png
wisdom@wisdom:~/yun/files$ tree
.
├── action_log
├── bg2.jpg
├── bg4.jpg
├── bg5.jpg
├── bg.jpg
├── blog.js
├── elf.png
├── facebook.png
├── favicon.ico
├── fonts
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── adventpro.ttf
│   ├── LICENSE.txt
│   ├── logo.png
│   ├── luckiest-guy.zip
│   ├── Roboto-BlackItalic.ttf
│   └── Roboto-Black.ttf
├── jquery.js
├── photo1.jpg
├── Roboto.zip
├── RSS.png
├── sunset.png
└── webdes.jpg
</pre>

<b>To organize by file types</b>
<pre><font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ fotool -a move -r -t
<font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ tree
<font color="#42A5F5"><b>.</b></font>
├── action_log
├── <font color="#42A5F5"><b>fonts</b></font>
├── <font color="#42A5F5"><b>FONT-SFNT Files</b></font>
│   ├── <font color="#C3D82C"><b>adventpro.ttf</b></font>
│   ├── <font color="#C3D82C"><b>Roboto-BlackItalic.ttf</b></font>
│   └── <font color="#C3D82C"><b>Roboto-Black.ttf</b></font>
├── <font color="#42A5F5"><b>Javascript Source Files</b></font>
│   ├── <font color="#C3D82C"><b>blog.js</b></font>
│   └── <font color="#C3D82C"><b>jquery.js</b></font>
├── <font color="#42A5F5"><b>JPEG Files</b></font>
│   ├── <font color="#C3D82C"><b>1.jpg</b></font>
│   ├── <font color="#C3D82C"><b>2.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg2.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg4.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg5.jpg</b></font>
│   ├── <font color="#C3D82C"><b>bg.jpg</b></font>
│   ├── <font color="#C3D82C"><b>photo1.jpg</b></font>
│   └── <font color="#C3D82C"><b>webdes.jpg</b></font>
├── <font color="#42A5F5"><b>PNG Files</b></font>
│   ├── <font color="#C3D82C"><b>elf.png</b></font>
│   ├── <font color="#C3D82C"><b>facebook.png</b></font>
│   ├── <font color="#C3D82C"><b>favicon.ico</b></font>
│   ├── <font color="#C3D82C"><b>logo.png</b></font>
│   ├── <font color="#C3D82C"><b>RSS.png</b></font>
│   └── <font color="#C3D82C"><b>sunset.png</b></font>
├── <font color="#42A5F5"><b>Text File</b></font>
│   └── <font color="#C3D82C"><b>LICENSE.txt</b></font>
└── <font color="#42A5F5"><b>ZIP Files</b></font>
    ├── <font color="#C3D82C"><b>luckiest-guy.zip</b></font>
    └── <font color="#C3D82C"><b>Roboto.zip</b></font>
</pre>

<b>To remove roboto from the font names</b>
<pre><font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ fotool -a move -r -x &quot;(?&lt;=Roboto)(.*)&quot; -s &quot;roboto&quot; -z fonts/
<font color="#C3D82C"><b>wisdom@wisdom</b></font>:<font color="#42A5F5"><b>~/yun/files</b></font>$ tree
<font color="#42A5F5"><b>.</b></font>
├── action_log
├── <font color="#C3D82C"><b>bg2.jpg</b></font>
├── <font color="#C3D82C"><b>bg4.jpg</b></font>
├── <font color="#C3D82C"><b>bg5.jpg</b></font>
├── <font color="#C3D82C"><b>bg.jpg</b></font>
├── <font color="#C3D82C"><b>blog.js</b></font>
├── <font color="#C3D82C"><b>elf.png</b></font>
├── <font color="#C3D82C"><b>facebook.png</b></font>
├── <font color="#C3D82C"><b>favicon.ico</b></font>
├── <font color="#42A5F5"><b>fonts</b></font>
│   ├── <font color="#C3D82C"><b>1.jpg</b></font>
│   ├── <font color="#C3D82C"><b>2.jpg</b></font>
│   ├── <font color="#C3D82C"><b>adventpro.ttf</b></font>
│   ├── <font color="#C3D82C"><b>-BlackItalic.ttf</b></font>
│   ├── <font color="#C3D82C"><b>-Black.ttf</b></font>
│   ├── <font color="#C3D82C"><b>LICENSE.txt</b></font>
│   ├── <font color="#C3D82C"><b>logo.png</b></font>
│   └── <font color="#C3D82C"><b>luckiest-guy.zip</b></font>
├── <font color="#C3D82C"><b>jquery.js</b></font>
├── <font color="#C3D82C"><b>photo1.jpg</b></font>
├── <font color="#C3D82C"><b>RSS.png</b></font>
├── <font color="#C3D82C"><b>sunset.png</b></font>
└── <font color="#C3D82C"><b>webdes.jpg</b></font>

1 directory, 22 files
</pre>

#Extending fotools  
To extend fotools, all you need do is create a python file  
and define an extension class with its name ending with Extension  
eg `class DeleteExtension:`.  
Then run   
```sh
        fotool.py --install-extension /path/to/extension.py
```
To extend a function simply create a similar method with name similar to that 
of the method name without the 'default_' prepended to it e.g `default_fuzzy_search`
becomes `fuzzy_search`.  
To use the extension simply supply the `-e` or `--extension argument` with the value set
to the filename without .py.  
You can list installed extensions with the  `--list-extensions` flag
This program comes with some extensions (in the extensions folder") 
which you use as reference.
They are:  
       
 1. **delete** - Adds delete command to the `-a` flag.   
    Example usage:  
        ```sh
            fotool.py -e delete -a delete -s "__pycache__" -l
        ```  
        
 2. **search_contents** - Search the content of allowed types.  
    See search_contents.py for the list of allowed types  
        Example usage:  
        ```sh
            fotool.py -e search_contents -s "william shakespeare" -r
        ```  
        
 3. **pcloud_upload** - Uploads matching files to pcloud.  
    Requires PCLOUD_USER and PCLOUD_PASS environment variables  
    to be set.  

## USAGE

<pre>
usage: fotool.py [-h] [-s SEARCH_STRING] [-e EXTENSION] [-d DIRECTORY] [-z DESTINATION] [-m MIN_RATIO] [-b GROUPS] [-n NOMATCHDIR] [-a ACTION]
                 [-r] [-q] [-k] [-j [REVERSE]] [-p ACTION_LOG] [-u OPCOUNT] [--reverse-timestamp-start RTSTART]
                 [--reverse-timestamp-stop RTSTOP] [-l | -f] [-i | -g | -t] [-w] [-c | -x GEN_REGEX] [-y FILEEXTENSIONS]
                 [--install-extension EXTENSION_NAME] [--list-extensions] [--extension-help EXTENSION_NAME]

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH_STRING, --search_string SEARCH_STRING
                        The string to search for.
  -e EXTENSION, --extension EXTENSION
                        Use extension specified where extension is of the form 'parent_dir.child_dir.extension_module:class' or
                        'extension_module:class' or 'extension_module' where extension_module is a valid extension python file
  -d DIRECTORY, --directory DIRECTORY
                        The directory to work on.
  -z DESTINATION, --destination-directory DESTINATION
                        Target directory for file operations.
  -m MIN_RATIO, --min-levenshtein-ratio MIN_RATIO
                        This Program uses Levenshtein Distance Algorithm to search for match by default unless the -s or --simple-match
                        options are specified. This option specified the minimun ratio that will be considered a match using
                        partial_set_ratio. Defaults to 75
  -b GROUPS, --groups GROUPS
                        Number of groups to divide each class (alphas and nums) will be divided into for generating destination directory
                        based on initials of filenames (used with the -i or --initials arguments) .
  -n NOMATCHDIR, --nomatchdir NOMATCHDIR
                        Directory to copy or move files to if no match is found. Defaults to ignore. This program allows you to use [:dd:] to
                        reference the directory matched files are moved to (specified with -d or --destination-directory argument). So the
                        move all unmatched files to a folder named 'unknown' in the target directory pass '[:dd:]/unknown' as the value to
                        this argument.
  -a ACTION, --action ACTION
                        The action to carry out on matched files, valid options are: print, move, copy_rename, rename, copy. Defaults to
                        print. You can also add custom actions in extensions
  -r, --recursive       Recursively find files.
  -q, --newline         print a newline after each output
  -k, --irreversible    Disable reversibility i.e action are not written to actionlog to provide the ability to reverse action.
  -j [REVERSE], --reverse [REVERSE]
                        Reverse last actions from actions log.
  -p ACTION_LOG, --action-log-file ACTION_LOG
                        File to log actions for reversibility of operations.
  -u OPCOUNT, --count OPCOUNT
                        Specifies the maximum number of operations to carry out.
  --reverse-timestamp-start RTSTART
                        Reverse operations that where carried out on or after this timestamp. If reverse-timestamp-stop is specified, then
                        operations carried out between reverse-timestamp-start and reverse-timestamp-stop are reversed
  --reverse-timestamp-stop RTSTOP
                        Reverse operations that where carried out on or before this timestamp. If reverse-timestamp-start is specified, then
                        operations carried out between reverse-timestamp-start and reverse-timestamp-stop are reversed
  -l, --simple-match    Simple string match.
  -f, --fuzz-match      Fuzzy string match.
  -i, --initials        Use initials of filenames to generate groups. Directories are created with the group name as destination for file
                        operations.
  -g, --group
  -t, --type            Generate location for matched files by using their filetype.
  -w, --case-sensitive  Makes regex filename generation case-sensitive
  -c, --generate-combinations
                        Used to generate new names for matched files based on various combinations of characters.
  -x GEN_REGEX, --generate-regex GEN_REGEX
                        Used to generate new names for matched files based of strings extracted from filenames using regular expressions.
  -y FILEEXTENSIONS, --file-types FILEEXTENSIONS
                        Only match files of the path type(s)/extension(s) given. Value can be a single file type like 'pdf' or a comma
                        seperated list of file types like 'pdf,txt,html,exe,zip'. There are currently 72 recognized file types and they are:
                        py, html, htm, css, js, cpp, c, rb, pl, php, r, go,java, svg, png, jpg, jpx, gif, webp, cr2, tif, bmp, jxr,psd, ico,
                        heic, mp4, m4v, mkv, webm, mov, avi, wmv, mpg,flv, swf, mid, mp3, m4a, ogg, flac, wav, amr, zip, tar,rar, gz, bz2, 7z,
                        xz, ar, deb, z, lz, exe, cab, pyc, jar,pdf, docx, doc, ppt, pptx, epub, rtf, txt, ps, woff,woff2, ttf, otf, md files.
  --install-extension EXTENSION_NAME
                        Install a file as an extension
  --list-extensions     List installed extensions
  --extension-help EXTENSION_NAME
                        View an extension module docstring
</pre>
