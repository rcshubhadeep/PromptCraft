from typing import Any
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import loader


def entry_point(file_name:str) -> Any:
    try:
        with open(file_name) as fp:
            return load(fp, Loader=Loader)
    except Exception:
        return None