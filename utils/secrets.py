"""
Central place for reading API keys.

Priority order:
  1. Real environment variables (e.g. set on a server / Docker container)
  2. A local ".env" file (loaded via python-dotenv, for local development)
  3. Streamlit secrets ("secrets.toml", used on Streamlit Community Cloud)

Nothing here is ever hardcoded, and none of it is exposed on the frontend —
components/sidebar.py only ever reads from PROVIDER_KEYS to check whether a
key exists, it never displays or accepts key values.
"""

import os

import streamlit as st
from dotenv import load_dotenv

# Loads variables from a local .env file into os.environ, if one exists.
# Safe to call even if there's no .env file (e.g. in production).
load_dotenv()


def get_secret(name: str) -> str:
    """Read a secret by name from env vars first, then Streamlit secrets."""
    value = os.environ.get(name, "")
    if not value:
        try:
            value = st.secrets.get(name, "")  # type: ignore[attr-defined]
        except Exception:
            value = ""
    return value


GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
GROQ_API_KEY = get_secret("GROQ_API_KEY")

# Generic map so the rest of the app can check "does provider X have a key?"
# without caring about the specific env var name behind it.
PROVIDER_KEYS = {
    "gemini": GEMINI_API_KEY,
    "openai": OPENAI_API_KEY,
    "groq": GROQ_API_KEY,
}
