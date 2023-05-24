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