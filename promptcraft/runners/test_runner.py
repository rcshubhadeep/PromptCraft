from typing import Any

from langchain.prompts import PromptTemplate
from langchain.utilities import PythonREPL
from rich import print

from .test_runner_base import BaseTestRunner
from promptcraft.exceptions import UnsafeCodeExecutionError


class TestRunner(BaseTestRunner):

    def __init__(self, llm: Any, prompt_template: PromptTemplate) -> None:
        super().__init__(llm, prompt_template)
    
    def run_tests(self, test_cases: dict) -> bool:
        for test_case in test_cases:
            result = self.chain.run(**test_case['inputs'])
            test_passed = self._verify_result(test_case, result)
            if not test_passed:
                print("[red bold]Test Failed[/red bold]")
                print("[green]Expected[/green]")
                print(test_case['expected_output'])
                print("[red]Got[/red]")
                print(result)
                return False
        print("[green bold]Tests passed[/green bold]")
            
        
    
    def _verify_code_run(self, produced_code: str, language: str, allow_unsafe: bool=False) -> bool:
        if language == "python":
            if produced_code.find("import") != -1 and not allow_unsafe:
                raise UnsafeCodeExecutionError(produced_code)
            repl = PythonREPL()
            r = repl.run(produced_code)
            if r.startswith('SyntaxError'):
                return False
            return True

    def _verify_semantic_similarity(self, produced_text, expected_text):
        pass
    
    def _verify_result(self, test_case: dict, test_result: str) -> bool:
        expected_output = test_case['expected_output']

        for strategy in test_case['test_method']['strategies']:
            if strategy == "run":
                allow_unsafe = test_case['test_method'].get('allow_unsafe') if test_case['test_method'].get('allow_unsafe') else False
                r = self._verify_code_run(test_result.replace("```", ""), test_case['test_method']['language'], allow_unsafe)
                if r is False:
                    return False
        
        return True
