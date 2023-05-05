"""Invoke tasks for the project."""

import logging

from invoke import task

logging.basicConfig(level=logging.INFO)


@task
def streamlit(c, file_path: str = "src/01_🏠_Accueil.py"):
    """Run Streamlit app."""
    c.run(f"streamlit run {file_path}")
