from typing import Callable, Any, Tuple, List, Union
from .prompt_generator_base import PromptGeneratorBase
from promptcraft.config import OUTPUT_TYPES, MODEL_TYPES, MODEL_PROVIDERS
from promptcraft.exceptions import MandatoryPropertyMissingError


class RoleBasedPromptGenerator(PromptGeneratorBase):
    """
    This is the prompt generator which helps to generate prompt based on roles.
    """
    def __init__(self, data: dict, tokenizer: Callable[..., Any] = None) -> None:
        super().__init__(data, tokenizer)
    
    def _craft_role_part(self) -> str:
        if self.data.get('role') is None:
            raise MandatoryPropertyMissingError('role')
        
        main_role = f"""You are a {self.data.get('role')}.\n"""

        if self.data.get('extra_attributes'):
            extras = ", ".join(self.data.get('extra_attributes')[:-1])
            extras = extras + ", and " + self.data.get('extra_attributes')[-1]
        main_role = main_role + f"You are {extras}\n"
        return main_role
    
    def _craft_task_part(self) -> str:
        if self.data.get('task') is None:
            raise MandatoryPropertyMissingError('task')

        main_task = f"\nYour task is to {self.data.get('task')}.\n"

        if self.data.get('only_output'):
            main_task = main_task + "IMPORTANT - Please ONLY produce the output\n"
        else:
            main_task = main_task + "IMPORTANT - Please produce a step by step explanation.\n"
        
        return main_task
    
    def _restrict_type_of_output(self) -> str:
        if self.data.get('output_type') in OUTPUT_TYPES:
            if self.data.get('output_type') == 'code':
                type_restrict = """\nIMPORTANT - Please only produce output enclosed in three back-quotes
Example - 
```
    OUTPUT
```"""
                return type_restrict
            elif self.data.get('output_type') == 'json':
                type_restrict = """\nIMPORTANT - Please produce ONLY json as output\n"""
                return type_restrict
            elif self.data.get('output_type') == 'csv':
                type_restrict = """\nIMPORTANT - Please produce CSV (Comma Separated Value) as output
Example -
value1, value2, value3, ..."""
                return type_restrict
            else:
                return ""
        else:
            return ""

    def _generate_prompt(self, start: str = "", end: str = "") -> Tuple[str, Union[List[dict], None]]:
        role_part = start + "\n" + self._craft_role_part() + self._craft_task_part() + self._restrict_type_of_output() + "\n"

        system_message = role_part + end if end else role_part
        
        input_vars = self.data.get('input_vars')
        var_names = []
        if input_vars:
            separator = input_vars.get('separator', "")
            if input_vars.get('var_names') is None:
                raise MandatoryPropertyMissingError('var_names')
            for inv_var in input_vars['var_names']:
                temp = f"\n{{{inv_var}}}{separator}"
                system_message = system_message + temp
                var_names.append(inv_var)
        
        if self.data.get('test_cases') is None:
            test_cases = [{k: "" for k in var_names}]
        else:
            test_cases = []
            for case_name, case_details in self.data.get('test_cases').items():
                formatted_output = {}
                formatted_output['inputs'] = {}
                for v in var_names:
                    formatted_output['inputs'][v] = case_details.get(v) if case_details.get(v) else ""
                formatted_output['expected_output'] = case_details.get('expected_output') if case_details.get('expected_output') else ""
                formatted_output['test_method'] = case_details.get('test_method')
                test_cases.append(formatted_output)

        return system_message, test_cases