import os
import warnings
import pathlib

import click

from promptcraft.exceptions import HFandOAIBothPresentError
from promptcraft.engine import entry_point


@click.command()
@click.argument("conf_file", required=True)
@click.option("--openai_api_key", "-oaik", default=os.getenv("OPENAI_API_KEY"), help="OpenAI API Key")
@click.option("--hf_api_key", "-hfk", default=os.getenv("HF_API_TOKEN"), help="Hugging Face API Token")
@click.option("--verbose/--no-verbose", default=False, help="If you want verbose output")
def main(conf_file: str, openai_api_key:str, hf_api_key:str, verbose:bool):
    """
    Main interface for promptcraft CLI
    """
    if openai_api_key and hf_api_key:
        raise HFandOAIBothPresentError
    if not openai_api_key and not hf_api_key:
        warnings.warn("No API key is found. Only prompt generation is possible", UserWarning)
    
    if not pathlib.Path(conf_file).exists():
        raise FileNotFoundError(conf_file)
    
    api_key = openai_api_key if openai_api_key else hf_api_key
    
    entry_point(conf_file, api_key, verbose)


if __name__ == "__main__":
    main()