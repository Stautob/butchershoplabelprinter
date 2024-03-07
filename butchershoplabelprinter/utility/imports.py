from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from inspect import isclass, getfile


def import_subclasses_in_this_dir(cls: type):
    """ Imports all Subclasses of cls that reside in the same directory as the file containing cls """
    cls_dir =  Path(getfile(cls)).resolve().parent
    cls_base_module = cls.__module__.removesuffix(f".{cls.__name__}")
    for _, module_name, _ in iter_modules([cls_dir]):
        module = import_module(f"{cls_base_module}.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isclass(attribute) and issubclass(attribute, cls):
                globals()[attribute_name] = attribute
