class HFandOAIBothPresentError(Exception):
    """
    Exception to be raised when both OpenAI and Hugging Face
    API keys are present.
    """
    def __init__(self, *args: object) -> None:
        super().__init__("""Both OpenAI and HuggingFace API keys are present. Please only use any one of them""")