"""
Streaming clients for each supported provider (Gemini / OpenAI / Groq), plus a
dispatch table so the rest of the app can pick the right one automatically
based on which model was selected in the sidebar — no manual key entry or
branching needed outside this file.
"""

from utils.secrets import GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def stream_gemini(model_id: str, system_prompt: str, history: list[dict]):
    client = genai.Client(api_key=GEMINI_API_KEY)
    gemini_contents = []
    for m in history:
        role = "user" if m["role"] == "user" else "model"
        gemini_contents.append({"role": role, "parts": [{"text": m["content"]}]})

    config = types.GenerateContentConfig(
        system_instruction=system_prompt if system_prompt else None,
    )

    response_stream = client.models.generate_content_stream(
        model=model_id, contents=gemini_contents, config=config
    )

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if chunk.usage_metadata:
            in_tokens = chunk.usage_metadata.prompt_token_count
            out_tokens = chunk.usage_metadata.candidates_token_count
        yield chunk.text, in_tokens, out_tokens


def stream_openai(model_id: str, system_prompt: str, history: list[dict]):
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages = [{"role": "system", "content": system_prompt or ""}]
    for m in history:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})

    response_stream = client.chat.completions.create(
        model=model_id, messages=messages, max_tokens=1500, stream=True,
        stream_options={"include_usage": True},
    )

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if chunk.usage:
            in_tokens = chunk.usage.prompt_tokens
            out_tokens = chunk.usage.completion_tokens
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        if delta:
            yield delta, in_tokens, out_tokens


def stream_groq(model_id: str, system_prompt: str, history: list[dict]):
    client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    messages = [{"role": "system", "content": system_prompt or ""}]
    for m in history:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})

    response_stream = client.chat.completions.create(
        model=model_id, messages=messages, max_tokens=1500, stream=True,
        stream_options={"include_usage": True},
    )

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if chunk.usage:
            in_tokens = chunk.usage.prompt_tokens
            out_tokens = chunk.usage.completion_tokens
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        if delta:
            yield delta, in_tokens, out_tokens


# The model picked in the sidebar drives which client/key gets used — the
# rest of the app just does STREAM_DISPATCH[provider](...).
STREAM_DISPATCH = {
    "gemini": stream_gemini,
    "openai": stream_openai,
    "groq": stream_groq,
}


def provider_sdk_available(provider: str) -> bool:
    """Whether the Python package needed for this provider is installed."""
    if provider == "gemini":
        return genai is not None
    return OpenAI is not None
