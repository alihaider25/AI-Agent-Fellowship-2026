"""App-wide constants: page settings, model registry, and system prompt presets."""

PAGE_TITLE = "AI Chat Workspace"
PAGE_ICON = "💬"

MODEL_OPTIONS = {
    "Gemini 2.5 Flash (Google)": {"provider": "gemini", "model_id": "gemini-2.5-flash"},
    "GPT-4o (OpenAI)": {"provider": "openai", "model_id": "gpt-4o"},
    "Groq — Llama 3.3 70B": {"provider": "groq", "model_id": "llama-3.3-70b-versatile"},
}

DEFAULT_SYSTEM_PROMPTS = {
    "General Assistant": "You are a helpful, concise AI assistant.",
    "Software Engineer": "You are a professional software engineer. Give precise, well-structured technical answers with code examples where useful.",
    "AI Research Assistant": "You are an AI research assistant. Explain concepts rigorously, cite reasoning clearly, and flag uncertainty when it exists.",
    "Custom": "",
}
