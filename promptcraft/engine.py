from typing import Any, Union, Tuple
from yaml import load
from yaml.parser import ParserError
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import loader
import semver
from rich import print

from promptcraft.exceptions import CouldnotProcessConfigurationError, VersionMismatchError
from promptcraft.config import LATEST_VERSION, MODEL_PROVIDERS
from promptcraft.prompt_generators import get_prompt_generator


def _check_version(data: dict) -> str:
    if data.get('version') is None:
        return LATEST_VERSION
    else:
        if semver.compare(LATEST_VERSION, data.get('version')) >= 0:
            return data.get('version')
        else:
            raise VersionMismatchError(data.get('version'))


def _check_model_provider(data: dict) -> Tuple[bool, Union[str, None]]:
    if data.get('model_provider') is None:
        return (False, None)
    elif data.get('model_provider') not in MODEL_PROVIDERS:
        return (False, data.get('model_provider'))
    else:
        return (True, data.get('model_provider'))
        

def entry_point(file_name:str, verbose) -> Any:
    try:
        with open(file_name) as fp:
            data = load(fp, Loader=Loader)
            version = _check_version(data)
            
            if verbose:
                print(f"Running with [green]{version}[/green]")
            
            present, model_provider = _check_model_provider(data)
            if not present:
                print(f"[red] The model provider '{model_provider}' is not known.[/red] Only prompt generation")
            
            prompt_generator = get_prompt_generator(data.get('type'), data)
            
            prompt, test_cases = prompt_generator.run()

            run_tests = False
            for _, v in test_cases[0].items():
                if v:
                    run_tests = True
                    break
            
            var_names = list(test_cases[0].keys()) if not run_tests else list(test_cases[0]['inputs'].keys())
            
            
    except ParserError:
        raise CouldnotProcessConfigurationError(file_name)