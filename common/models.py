"""Factory for OpenRouter-backed chat models used by all agents in this demo."""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_MODELS = {
    "sanitation": "meta-llama/llama-3.3-70b-instruct:free",
    "supplier": "qwen/qwen-2.5-72b-instruct:free",
    "process": "deepseek/deepseek-chat-v3.1:free",
    "cross_reference": "deepseek/deepseek-chat-v3.1:free",
    "single_agent": "deepseek/deepseek-chat-v3.1:free",
}


def get_api_key() -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai/keys "
            "and set it in a .env file (see .env.example) or as an environment variable."
        )
    return api_key


def make_model(role: str) -> ChatOpenAI:
    """Build a ChatOpenAI instance pointed at OpenRouter for the given agent role.

    The model id can be overridden per-role via an env var, e.g. MODEL_SANITATION,
    MODEL_SUPPLIER, MODEL_PROCESS, MODEL_CROSS_REFERENCE, MODEL_SINGLE_AGENT.
    """
    env_var = f"MODEL_{role.upper()}"
    model_id = os.environ.get(env_var, DEFAULT_MODELS[role])
    return ChatOpenAI(
        model=model_id,
        api_key=get_api_key(),
        base_url=OPENROUTER_BASE_URL,
        temperature=0.2,
    )
