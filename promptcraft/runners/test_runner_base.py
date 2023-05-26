from abc import ABC, abstractmethod
from typing import Any

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class BaseTestRunner(ABC):

    def __init__(self, llm: Any, prompt_template: PromptTemplate) -> None:
        # self.test_cases = test_cases
        self.chain = LLMChain(llm=llm, prompt=prompt_template)

    @abstractmethod
    def run_tests(self, test_cases: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _verify_result(self, test_cases: dict, test_result: str) -> bool:
        raise NotImplementedError
