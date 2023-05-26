from promptcraft.config import LATEST_VERSION


class HFandOAIBothPresentError(Exception):
    """
    Exception to be raised when both OpenAI and Hugging Face
    API keys are present.
    """
    def __init__(self, *args: object) -> None:
        super().__init__("""Both OpenAI and HuggingFace API keys are present. Please only use any one of them""")


class CouldnotProcessConfigurationError(Exception):
    """
    Exception to be raised when the configuration file can't be parsed
    OR something else went wrong. And hence advancing is impossible.
    """
    def __init__(self, *args: object) -> None:
        file_name = args[0]
        super().__init__(f"Could not read {file_name}")


class VersionMismatchError(Exception):
    """
    Exception to be raised when the version in the yml does not match with
    the latest version admitted by the package
    """
    def __init__(self, *args: object) -> None:
        given_version = args[0]
        super().__init__(f"The given version {given_version} is higher than the admitted version {LATEST_VERSION}")


class UnregisteredPromptTypeError(Exception):
    """
    Exception to be raised when we do not know what type of prompt to generate
    """
    def __init__(self, *args: object) -> None:
        prompt_type = args[0]
        super().__init__(f"Prompt type '{prompt_type}' is not recognized. You can register it before")


class MandatoryPropertyMissingError(Exception):
    """
    Exception to be raised when there is a mandatory filed missing in the app description
    """
    def __init__(self, *args: object) -> None:
        filed_name = args[0]
        super().__init__(f"Mandatory field '{filed_name}' missing from app file")


class UnsafeCodeExecutionError(Exception):
    """
    Exception to be raised if we try to execute unsafe code in Python REPL unless we explicitly ask to do so
    """
    def __init__(self, *args: object) -> None:
        code = args[0]
        super().__init__(f"Unsafe code execution\n\n{code}")


# class NoModelProvider(Exception):
#     """
#     Exception to be raised when no model provider was supplied.
#     """
#     def __init__(self, *args: object) -> None:
#         super().__init__("No model provider or model provider is unknown")


# class NoModelName(Exception):
#     """
#     Exception to be raised if no model name is provided.
#     """