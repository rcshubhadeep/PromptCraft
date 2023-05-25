from typing import Callable, Any, Union

from .prompt_generator_base import PromptGeneratorBase
from .role_based_prompt_generator import RoleBasedPromptGenerator
from promptcraft.config import PROMPT_TYPES
from promptcraft.exceptions import UnregisteredPromptTypeError


def register_prompt_type(type_name: str) -> None:
    PROMPT_TYPES.append(type_name)


def get_prompt_generator(type_of_prompt: str, data: dict, tokenizer: Callable[..., Any] = None) -> Union[Any, None]:
    if type_of_prompt is None or type_of_prompt not in PROMPT_TYPES:
        raise UnregisteredPromptTypeError(type_of_prompt)
    
    if type_of_prompt == "role_based":
        return RoleBasedPromptGenerator(data, tokenizer)
    elif type_of_prompt == "qa":
        pass
    elif type_of_prompt == "summary":
        pass
    elif type_of_prompt == "translation":
        pass
    elif type_of_prompt == "free_form":
        pass
    else:
        return None
