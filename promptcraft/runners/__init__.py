from typing import Any

####################################
# LangChain supports a LOT - https://python.langchain.com/en/latest/modules/models/llms/integrations.html
# We will eventually support all of them.
# We will allow everything for the users to mix different LLM
####################################
from langchain.prompts import PromptTemplate

from langchain.llms import OpenAI, OpenAIChat  # OpenAI Specific

from .test_runner_base import BaseTestRunner
from .test_runner import TestRunner


def get_llm(llm_provider: str, 
               model_type: str, 
               model_name: str, 
               api_key: str, 
               init_params: dict) -> Any:
    if llm_provider == "OpenAI":
        if model_type == "instruction following":
            return OpenAI(model_name=model_name, openai_api_key=api_key, **init_params)


def get_prompt_template(input_vars: list, template: str) -> type[PromptTemplate]:
    return PromptTemplate(input_variables=input_vars,
                          template=template)