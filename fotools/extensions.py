import importlib
import inspect
import os
import pathlib
import shutil
from typing import List, Union

from fotools.organizer import DefaultOrganizer


def install_extension(path_to_py_file: pathlib.Path) -> None:
    """
        Install extensions by copying python
        extension file to extensions directory
    """
    print("Installing...")
    extensions_folder = pathlib.Path(__file__).parent.parent / "extensions"
    path_to_py_file = pathlib.Path(path_to_py_file).absolute()
    type_ = DefaultOrganizer().default_get_file_type(path_to_py_file)
    if type_ != ('py', 'Python Source Files'):
        raise ValueError("Invalid extension format")
    res = shutil.copy(path_to_py_file, extensions_folder)
    print("Extension installed at", res)


def inject_default(extension_returning_func) -> Union[None,
                                                      DefaultOrganizer,
                                                      List[DefaultOrganizer]]:
    """
        Dynamically add DefaultOrganizer as a parent class to
        extension class.
    """
    def inner_inject(*args, **kwargs):
        extension_object = extension_returning_func(*args, **kwargs)
        if isinstance(extension_object, list):
            return [type(object.__name__,
                         (object, DefaultOrganizer), {}) for object in extension_object]
        if extension_object:
            extension_object = type(extension_object.__name__,
                                    (extension_object, DefaultOrganizer),
                                    {})
        return extension_object
    return inner_inject


@inject_default
def find_extension_class(extension_name: str,
                         classname: str = None,
                         many: bool = False) -> Union[None,
                                                      DefaultOrganizer,
                                                      List[DefaultOrganizer]]:
    """
        Search an extension module for its class definition
    """
    module = importlib.import_module(f"extensions.{extension_name}")
    extensions = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            endswith = "Extension"
            if classname:
                endswith = classname
            if obj != DefaultOrganizer and obj.__name__.endswith(endswith):
                extensions.append(obj)
    if many:
        return extensions
    if extensions:
        return extensions[0]
    return


def parse_extension(extension: str) -> DefaultOrganizer:
    """
    Parse extension argument value and return extension class
    """

    if ":" in extension:
        # Parser for when custom class name is used for extension in the format
        #  'modulename:class_name'
        module, classname = extension.split(":")
        ext = find_extension_class(module, classname)
    # Default extension class name is 'Extension'
    else:
        ext = find_extension_class(extension)
    if not ext:
        raise Exception("could not find ")
    return ext


def list_extensions() -> List[DefaultOrganizer]:
    """
        List all installed extensions
    """
    extensions_folder = pathlib.Path(__file__).parent.parent / "extensions"
    extensions = []
    for extension_file in os.listdir(extensions_folder):
        extension_name = pathlib.Path(extension_file).stem
        objs = find_extension_class(extension_name, many=True)
        if objs:
            for obj in objs:
                extensions.append(extension_name + ":" + str(obj.__name__))
    return extensions


def get_extension_doc(extension_name: str) -> str:
    module = importlib.import_module(f"extensions.{extension_name}")
    return module.__doc__
