"""Utility code for the mail client."""

from os import getenv

from dotenv import load_dotenv

from email_service.src.mail.constants import DOTENV_PATH


def get_env_var(varname: str) -> str:
    """Get the provided environment variable."""
    envvar = getenv(varname, None)

    # If not available as an env var, try loading from .env file
    if envvar is None:

        load_dotenv(dotenv_path=DOTENV_PATH)
        envvar = getenv(varname, None)

    if envvar is None:
        raise RuntimeError(
            f"The environment variable {varname} couldn't be retrieved."
        )

    return envvar
