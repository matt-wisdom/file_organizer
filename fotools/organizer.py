import itertools
import marshal
import os
import os.path as pth
import pathlib
import re
import shutil
import time
from typing import Any, Generator, List, Tuple, Union

import filetype
from fuzzywuzzy import fuzz

from . import logger


class DefaultOrganizer:
    # Groups for sorting files by filetype/extension

    groups = {
        "Source_Codes": [
            "py",
            "html",
            "htm",
            "css",
            "js",
            "cpp",
            "c",
            "rb",
            "pl",
            "php",
            "r",
            "go",
            "java",
        ],
        "Images": [
            "svg",
            "png",
            "jpg",
            "jpx",
            "gif",
            "webp",
            "cr2",
            "tif",
            "bmp",
            "jxr",
            "psd",
            "ico",
            "heic",
        ],
        "Video": [
            "mp4",
            "m4v",
            "mkv",
            "webm",
            "mov",
            "avi",
            "wmv",
            "mpg",
            "flv",
            "swf",
        ],
        "Audio": ["mid", "mp3", "m4a", "ogg", "flac", "wav", "amr"],
        "Archives": [
            "zip",
            "tar",
            "rar",
            "gz",
            "bz2",
            "7z",
            "xz",
            "ar",
            "deb",
            "z",
            "lz",
            "exe",
            "cab",
            "pyc",
            "jar",
        ],
        "Documents": [
            "pdf",
            "docx",
            "doc",
            "ppt",
            "pptx",
            "epub",
            "rtf",
            "txt",
            "ps"
        ],
        "Fonts": ["woff", "woff2", "ttf", "otf"],
        "Others": [],
    }

    ext_type = {
        "txt": "Text File",
        "py": "Python Source Files",
        "c": "C Source Files",
        "css": "CSS Files",
        "csv": "CSV Files",
        "doc": "Microsoft Word Documents",
        "docx": "Microsoft Word Documents",
        "js": "Javascript Source Files",
        "json": "JSON Files",
        "php": "PHP Files",
        "ppt": "PowerPoint Presentations",
        "pptx": "PowerPoint Presentations",
        "odp": "OpenDocument Presentations",
        "rtf": "Rich Text Files",
        "sh": "Bourne Shell Scripts",
        "svg": "Scalable Vector Graphics Files",
        "go": "GO Source Files",
        "pl": "Perl Source Files",
        "java": "Java Source Files",
        "cs": "C# Source Files",
        "htm": "HTML File",
        "html": "HTML File",
        "xhtml": "XHTML File",
        "md": "Markdown File"
    }

    def __init__(
        self,
        reversible: bool = True,
        reverse: bool = False,
        action_log: pathlib.Path = "action_log",
        reverse_count: int = None,
        reversetimerangestart: float = None,
        reversetimerangestop: float = None,
        newline: bool = False,
        case_sensitive: bool = False,
    ):
        """
        """
        self.action_log_file = action_log
        self.newline = newline
        self.groups = {}
        self.names = None
        self.case_sensitive = case_sensitive
        self.reversible = reversible
        self.reverse_count = reverse_count
        self.reversetimerangestart = reversetimerangestart
        self.reversetimerangestop = reversetimerangestop

        if reverse:
            if not pth.exists(self.action_log_file):
                logger.error("Could not locate action log file for ")
                raise FileNotFoundError("Could not locate action \
                    log file for ")

        if reversible:
            # Load or create new log file
            try:
                self.action_log_obj = open(self.action_log_file, "rb+")
            except FileNotFoundError:
                self.action_log_obj = open(self.action_log_file, "wb+")
            content = self.action_log_obj.read().strip()
            content = marshal.loads(content) if len(content) > 0 else b""

            # action logs is an dictionary with a timestamp as key and a
            # list of action, old, and new as values
            self.action_logs = dict(
                content
            )

        if reverse:
            # Operations need to be reversed in the reverse order they
            #  were made
            keysaslist = list(self.action_logs.keys())
            keysaslist.sort(key=lambda x: float(x), reverse=True)
            self.orderedkeys = keysaslist
            reverse_method = getattr(self, "reverse", self.default_reverse)
            reverse_method()
            return

        self.extra_attr = {}

    def default_write_action_log(self) -> bool:
        """
            Write current log to disk
        """
        if not self.reversible:
            logger.info("Not writing action log to disk...")
            return False
        logger.info("Writing to action log.")
        content = marshal.dumps(self.action_logs)
        try:
            self.action_log_obj = open(self.action_log_file, "rb+")
        except FileNotFoundError:
            self.action_log_obj = open(self.action_log_file, "wb+")
        self.action_log_obj.write(content)
        self.action_log_obj.flush()
        logger.info("Finished writing to log.")
        return True

    def default_add_to_log(self,
                           action: str,
                           old: pathlib.Path,
                           new: pathlib.Path) -> None:
        """
            Add operation to log.

            :param action: operation carried out
            :param old: path to location of file before op.
            :param new: path to location of file after op.
        """
        name = str(time.time())  # Stores action list with timestamp key
        if pth.isdir(pth.abspath(new)):
            fname = pth.split(old)[1]  # Get filename to add to log
            new = pth.join(pth.abspath(new), fname)
        if not isinstance(new, str):
            new = str(new)
        self.action_logs[name] = [action, pth.abspath(old), new]

    def default_get_file_type(self,
                              file: pathlib.Path
                              ) -> Union[None, Tuple[str, str]]:
        """
            Get filetype of the give file.
            :param file: file path
            :return: (extension, mimetype) or None
        """
        if isinstance(file, (pathlib.Path, str)):
            ft = filetype.guess(file)
            if not ft:
                return self.default_get_more_types(file)
            return ft.extension, ft.mime.split("/")[1].upper() + " Files"
        ft_list = []
        for i in file:
            ft = filetype.guess(i)
            if ft is None:
                ft_list.append(self.default_get_more_types(i))
            else:
                ft_list.append((ft.extension, ft.mime))
        return ft_list

    def default_get_more_types(self,
                               filename: pathlib.Path) -> Tuple[str,
                                                                str]:
        """
           Get some extra types not recognized by filetype
           :param filename: file path
        """
        ext = pth.splitext(filename)[1][1:]
        if ext:
            type_ = DefaultOrganizer.ext_type.get(ext.lower())
            if type_:
                return (ext.lower(), type_)
        return ()

    def default_gen_new_names(self,
                              chars="0123456789") -> Generator[str,
                                                               None,
                                                               None]:
        """
        Generate names using combinations of chars for rename functionality
        :param chars: characters to use in generating new names
        """
        length = 1
        names = itertools.combinations_with_replacement(chars, length)
        while True:
            try:
                yield "".join(next(names))
            except StopIteration:
                length += 1
                names = itertools.combinations_with_replacement(chars, length)

    def default_gen_new_name_combination(self,
                                         filename: pathlib.Path) -> pathlib.Path:
        """
        Generate a new name for file using the default_gen_new_names generator
        :param filename: file path
        """
        if not self.names:
            self.names = self.default_gen_new_names()
        ext = pth.splitext(filename)[1]
        return next(self.names) + ext

    def default_gen_new_name_regex(self,
                                   filename: pathlib.Path,
                                   regexp: str) -> pathlib.Path:
        """
        Generates a new file name based on a portion of old filename to
        be extracted
        by regular expression.
        e.g
            If we have some files named as follow:
            sitemoviez.com-foobar-S01-E01.mp4
            sitemoviez.com-foobar-S01-E03.mp4
            sitemoviez.com-foobar-S01-E03.mp4
            .....
        The following regular expression would remove the site name from
        the file. '(?<=viez.com-)(.*)'

        :param filename: file path
        :param regexp: Regular expression to use in extracting names.
        """
        filename, ext = pth.splitext(pth.split(filename)[1])
        if self.case_sensitive:
            match = re.findall(regexp, filename)[0]
        else:
            match = re.findall(regexp, filename, re.I | re.M)[0]
        new_filename = match + ext
        return new_filename

    def default_generate_destination_group(self,
                                           filename: pathlib.Path,
                                           groups: int = None,
                                           destination_dir: pathlib.Path = ".",
                                           nomatchdir: pathlib.Path = "") -> pathlib.Path:
        """
        Returns the appropriate group folder for the filename using the groups
        dictionary ('returns nomatchpath for
        files do not belong to any of the above groups.')

        :param filename: file path
        :param destination_dir: destination file path
        :param nomatchdir: folder to assign non matching files to
        """
        destination_dir = destination_dir.rstrip("/")
        nomatchdir = nomatchdir.replace("[:dd:]", destination_dir)
        ext = self.default_get_file_type(filename)
        if ext:
            ext = ext[0]
        else:
            return nomatchdir
        for i in DefaultOrganizer.groups.keys():
            if ext in DefaultOrganizer.groups.get(i):
                return pth.join(destination_dir, i)
        return nomatchdir

    def default_generate_destination_type(self,
                                          filename: pathlib.Path,
                                          destination_dir: pathlib.Path = ".",
                                          groups=5,
                                          nomatchdir: pathlib.Path = "") -> pathlib.Path:
        """
        Generates directory based on file type and returns nomatchpath for
        unknown types

        :param filename: file path
        :param destination_dir: destination file path
        :param nomatchdir: folder to assign non matching files to
        """
        destination_dir = destination_dir.rstrip("/")
        types = self.default_get_file_type(filename)

        nomatchdir = nomatchdir.replace("[:dd:]", destination_dir)
        if not types:
            return nomatchdir
        return pth.join(destination_dir, types[1])

    def default_action(self,
                       from_: pathlib.Path,
                       to: Union[None, pathlib.Path] = None,
                       action: str = "print") -> Any:
        """
        Initiates actions to be carried out on matched files

        :param from_: file path
        :param to: destination file path
        :param action: action to carry out
        """
        out = ""
        if action == "copy":
            out = self.default_copy(from_, to)
        elif action == "rename":
            out = self.default_rename(from_, to)
        elif action == "copy_rename":
            out = self.default_rename(from_, to, True)
        elif action == "move":
            out = self.default_copy(from_, to, True)
        elif action == "print":
            print(from_)
            if self.newline:
                print("")
        elif action == "create_dir":
            self.default_add_to_log(action, from_, to)
        else:
            logger.error(
                f"Action {action} is invalid. Valid options are: copy, \
                    rename, copy_rename, move, print"
            )
            raise ValueError(
                f"Action {action} is invalid. Valid options are: copy, \
                    rename, copy_rename, move, print"
            )
        if (
            self.reversible and action != "print"
        ):  # No need to log print action as no change is made
            self.default_add_to_log(action, from_, to)
        return out

    def _reverse(self, to, from_, action):
        try:
            if action == "create_dir":
                os.rmdir(from_)
            else:
                self.default_action(to, from_, action)
        except Exception:
            pass

    def default_reverse(self) -> None:
        """
            Reverse operation carried out using log
        """
        if not self.orderedkeys and self.action_logs:
            logger.error("Could not get object for reverse operations.")
            raise ValueError("Could not get object for reverse operations.")
        count = 0
        tookaction = False
        for i in self.orderedkeys:
            action, from_, to = self.action_logs[i]
            tstart = self.reversetimerangestart
            tstop = self.reversetimerangestop
            fl = float(i)
            if tstart and not tstop:
                if fl >= tstart:
                    self._reverse(to, from_, action)
                    tookaction = True
            elif tstop and not tstart:
                if fl <= tstop:
                    self._reverse(to, from_, action)
                    tookaction = True
            elif tstart and tstop:
                if fl >= tstart and fl <= tstop:
                    self._reverse(to, from_, action)
                    tookaction = True
            else:
                self._reverse(to, from_, action)
                tookaction = True
            if (
                self.reversible and action != "print" and tookaction
            ):  # No need to log print action as no change is made
                self.default_add_to_log(action, to, from_)
                tookaction = False
            count += 1
            if self.reverse_count:
                if count >= self.reverse_count:
                    return

    def default_generate_groups(self, groups: int, sep_nums: bool) -> None:
        """
        Generates a dictionary of characters and their appropriate groups
        where a group is of the format a0-a1 where a0 is a character
        representing the lower group boundary and a1 represents upper group
        boundary, Each group represents all characters between a0 and a1 for
        alphabets and all numbers between a0 and a1 for numbers.

        :param groups: The number of groups each class (alphas
                       and nums) will be divided into.

        :param sep_nums: Specifies whether all numbers should be contained
                         in one group 0-9 or seperated into multiple groups
                        as determined by groups
        """
        alphas = "abcdefghijklmnopqrstuvwxyz"
        nums = "1234567890"
        if self.groups:
            return
        for i in list(range(0, len(alphas) - (len(alphas) % groups * groups),
                      groups)):
            for j in alphas[i:i + groups]:
                self.groups[j] = alphas[i] + "-" + alphas[i + groups - 1]

            for j in alphas[i + groups - 1:]:
                self.groups[j] = \
                    (alphas[i + groups - 1] + "-" + alphas[len(alphas) - 1])
        if not sep_nums:
            for i in nums:
                self.groups[i] = "0-9"
        else:
            for i in list(range(0, len(nums) - (len(nums) % groups * groups),
                          groups)):
                for j in alphas[i: i + groups]:
                    self.groups[j] = nums[i] + "-" + nums[i + groups - 1]

                for j in nums[i + groups - 1:]:
                    self.groups[j] = \
                        nums[i + groups - 1] + "-" + nums[len(nums) - 1]

    def default_generate_destination_alphabetic(
        self,
        path: pathlib.Path,
        groups: int = 5,
        destination_dir: pathlib.Path = ".",
        sep_nums: bool = False,
        nomatchpath: pathlib.Path = ""
    ) -> pathlib.Path:
        """
        Generate destination folder based on alpha-numerical ordering

        :param path: file path
        :param groups: Number of groups
        :param destination_dir: destination directory
        :param sep_nums: Specifies whether all numbers should be contained
                         in one group 0-9 or seperated into multiple groups
                         as determined by groups
        :param nomatchpath: folder to assign non matching files to
        """
        path = path.lower()
        destination_dir = destination_dir.rstrip("/")
        self.default_generate_groups(groups, sep_nums)
        firstchar = pth.split(path)[1][0]
        nomatchdir = nomatchpath.replace("[:dd:]", destination_dir)
        path = self.groups.get(firstchar, nomatchdir)
        if path == nomatchdir:
            return nomatchdir
        fullpath = pth.join(destination_dir, path)
        return fullpath

    def default_copy(self,
                     from_: pathlib.Path,
                     to: pathlib.Path,
                     move: bool = False,
                     overwrite: bool = False) -> Union[int, pathlib.Path]:
        """
        Copy files from 'from_' to 'to'.
        Set move to True to move instead of copy
        and set overwrite flag to overwrite existing files.
        """
        if pth.exists(to) and not overwrite and pth.isfile(to):
            return -1

        path, fname = pth.split(from_)
        name, ext = pth.splitext(fname)
        name = name
        fname = name + ext
        if pth.isdir(to):
            to = pth.join(to, fname)
        if not move:
            logger.info("Copying  %s to %s." % (from_, to))
            try:
                return shutil.copy2(from_, to)
            except Exception as e:
                logger.exception("Could not copy %s to %s: %s"
                                 % (from_, to, e))
                return -1
        logger.info("Moving  %s to %s." % (from_, to))
        try:
            return shutil.move(from_, to)
        except Exception as e:
            logger.exception("Could not move %s to %s: %s" % (from_, to, e))
            return -1

    def default_walk_dir_recursive(self, dir: pathlib.Path = ".", extensions: str = ""):
        """
        Recursively walk directory 'dir' and generate the files found.
        """
        for root, dirs, files in os.walk(dir, topdown=True):
            for name in files:
                if extensions:
                    fname = pth.join(root, name)
                    try:
                        ext = self.default_get_file_type(fname)[0]
                    except (TypeError, IndexError):
                        continue
                    if ext in extensions:
                        yield fname
                        continue
                    else:
                        continue
                yield pth.join(root, name)

    def default_walk_dir(self,
                         dir=".",
                         extensions: List[str] = []) -> Generator[str, None, None]:
        """
        Return the content of 'dir'

        :param dir: directory of walk
        :param extensions: List of allowed extensions
        """
        content = os.listdir(dir)
        files = filter(lambda x: pth.isfile(pth.join(dir, x)), content)
        files = [pth.join(dir, x) for x in files]
        for fname in files:
            if extensions:
                try:
                    ext = self.default_get_file_type(fname)[0]
                except Exception:
                    continue
                if ext in extensions:
                    yield fname
                    continue
                else:
                    continue
            yield fname

    def default_rename(self,
                       from_: pathlib.Path,
                       to: pathlib.Path,
                       copy: bool = False,
                       overwrite: bool = False) -> Union[int, pathlib.Path]:
        """
        Rename file

        :param from_: file path
        :param to: destination
        :param copy:  if True a copy is made with the new name instead
        """
        if pth.exists(to) and not overwrite:
            return -1
        if copy:
            try:
                logger.info("Copying %s to %s." % (from_, to))
                return shutil.copy2(from_, to)
            except Exception as e:
                logger.error("Renaming %s to %s failed." % (from_, to))
                logger.error(e)
        logger.info("Renaming %s to %s." % (from_, to))
        os.rename(from_, to)
        return to

    @staticmethod
    def default_fuzzy_search(search, filepath, min_ratio=70) -> bool:
        """
        Levenshtein fuzzy search

        :param search: search string
        :param filepath: file path
        :param min_ratio: min ratio
        """
        stem = pth.split(filepath)[1]
        if not search:
            return True
        if isinstance(search, str):
            ratio = fuzz.partial_token_set_ratio(search, stem)

            return True if ratio >= min_ratio else False

    def default_simple_search(self, search, filepath) -> bool:
        """
        Simple text matching

        :param search: search string
        :param filepath: file path
        :param min_ratio: min ratio
        """
        stem = pth.split(filepath)[1]
        if not search:
            return True
        if self.case_sensitive:
            i = re.search(search, stem)
        else:
            i = re.search(search, stem, re.I)
        return True if i else False
