# cp .env.example .env
import os
import re
import time
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from utils.components import (
    render_empty_state,
    render_sidebar_summary,
    render_status_badge,
    render_template_banner,
)
from utils.styles import inject_css as inject_theme_css
from utils.styles import render_brand_header, render_sidebar_title

load_dotenv()  # reads .env in the project root, if present

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# --------------------------------------------------------------------------
# Page config (must be first Streamlit call)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="FLASH AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Provider keys — BACKEND ONLY, read from environment variables (.env) or
# Streamlit secrets. There is intentionally no frontend field for these —
# the user only ever picks a model, and the app wires up the matching key
# automatically. Never hardcode a real key in this file.
# --------------------------------------------------------------------------
def _get_secret(name: str) -> str:
    val = os.environ.get(name, "")
    if not val:
        try:
            val = st.secrets.get(name, "")  # type: ignore[attr-defined]
        except Exception:
            val = ""
    return val


GEMINI_API_KEY = _get_secret("GEMINI_API_KEY")
OPENAI_API_KEY = _get_secret("OPENAI_API_KEY")
GROQ_API_KEY = _get_secret("GROQ_API_KEY")
OPENROUTER_API_KEY = _get_secret("OPENROUTER_API_KEY")
OPENROUTER_MODEL = _get_secret("OPENROUTER_MODEL")

PROVIDER_KEYS = {
    "gemini": GEMINI_API_KEY,
    "openai": OPENAI_API_KEY,
    "groq": GROQ_API_KEY,
    "openrouter": OPENROUTER_API_KEY,
}

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
MODEL_OPTIONS = {
    "OpenRouter — DeepSeek R1": {"provider": "openrouter", "model_id": "deepseek/deepseek-r1"},
    "OpenRouter — Gemini 2.0 Flash": {"provider": "openrouter", "model_id": "google/gemini-2.0-flash-001"},
    "OpenRouter — GPT-4o Mini": {"provider": "openrouter", "model_id": "openai/gpt-4o-mini"},
    "OpenRouter — Llama 3.3 70B": {"provider": "openrouter", "model_id": "meta-llama/llama-3.3-70b-instruct"},
    "OpenRouter — Custom": {"provider": "openrouter", "model_id": OPENROUTER_MODEL or "openai/gpt-4o-mini"},
}

DEFAULT_SYSTEM_PROMPTS = {
    "General Assistant": "You are a helpful, concise AI assistant.",
    "Software Engineer": "You are a professional software engineer. Give precise, well-structured technical answers with code examples where useful.",
    "AI Research Assistant": "You are an AI research assistant. Explain concepts rigorously, cite reasoning clearly, and flag uncertainty when it exists.",
    "Custom": "",
}

BUILT_IN_TEMPLATES = {
    "Summarize Text": "Please summarize the following text concisely, keeping the key points:\n\n",
    "Explain Code": "Please explain what the following code does, step by step:\n\n",
    "Generate Ideas": "Generate 5 creative, distinct ideas about the following topic:\n\n",
    "Rewrite Content": "Please rewrite the following content to improve clarity and tone:\n\n",
    "Translate": "Translate the following text to [target language]:\n\n",
    "Create Email": "Write a professional email about the following:\n\n",
}


# --------------------------------------------------------------------------
# Session state initialization
# --------------------------------------------------------------------------
def new_session(name: str | None = None) -> str:
    session_id = str(uuid.uuid4())
    if name is None:
        name = f"Chat {st.session_state.next_session_number}"
        st.session_state.next_session_number += 1

    st.session_state.sessions[session_id] = {
        "name": name,
        "messages": [],
        "input_tokens": 0,
        "output_tokens": 0,
    }
    return session_id


def generate_session_title(text: str, max_words: int = 4) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    cleaned = re.sub(r"[^A-Za-z0-9\s-]", "", cleaned)
    words = [word for word in cleaned.split() if word]
    if not words:
        return "New Chat"
    title = " ".join(words[:max_words]).strip()
    return title[:44].rstrip() or "New Chat"


def maybe_rename_session(session_data: dict, prompt_text: str) -> None:
    if not prompt_text.strip():
        return
    if re.match(r"^Chat\s+\d+$", session_data.get("name", "")):
        session_data["name"] = generate_session_title(prompt_text)


if "next_session_number" not in st.session_state:
    st.session_state.next_session_number = 1

if "sessions" not in st.session_state:
    st.session_state.sessions = {}
    first_id = new_session("Chat 1")
    st.session_state.current_session = first_id
    st.session_state.next_session_number = 2

if "system_prompt_choice" not in st.session_state:
    st.session_state.system_prompt_choice = "General Assistant"
if "custom_system_prompt" not in st.session_state:
    st.session_state.custom_system_prompt = ""
if "custom_templates" not in st.session_state:
    st.session_state.custom_templates = {}
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "chat_box" not in st.session_state:
    st.session_state.chat_box = ""
if "api_error" not in st.session_state:
    st.session_state.api_error = None


# --------------------------------------------------------------------------
# Theming — modern glass-panel design-token system
# --------------------------------------------------------------------------
def inject_css(dark: bool = True) -> None:
    inject_theme_css(dark)


inject_css(st.session_state.dark_mode)

sess = st.session_state.sessions[st.session_state.current_session]

# --------------------------------------------------------------------------
# Brand header (main area)
# --------------------------------------------------------------------------
render_brand_header()

# --------------------------------------------------------------------------
# Sidebar Configuration
# --------------------------------------------------------------------------
with st.sidebar:
    render_sidebar_title()

    current_model_label = "OpenRouter — DeepSeek R1"
    for label, options in MODEL_OPTIONS.items():
        if "model_label" in st.session_state and st.session_state.model_label == label:
            current_model_label = label

    render_sidebar_summary(sess["name"], current_model_label)

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.current_session = new_session()
        st.session_state.api_error = None
        st.rerun()

    st.divider()

    st.markdown('<div class="section-label">Model Selection</div>', unsafe_allow_html=True)
    model_label = st.selectbox("Model", list(MODEL_OPTIONS.keys()), index=0, key="model_label", label_visibility="collapsed")
    selected_provider = MODEL_OPTIONS[model_label]["provider"]
    selected_model = MODEL_OPTIONS[model_label]["model_id"]
    if selected_provider == "openrouter" and OPENROUTER_MODEL:
        selected_model = OPENROUTER_MODEL

    # No API key inputs on the frontend — keys live only on the backend
    # (.env / st.secrets) and are picked automatically for the chosen model.
    key_ok = bool(PROVIDER_KEYS[selected_provider])
    dot_class = "ok" if key_ok else "bad"
    dot_text = "Backend connected" if key_ok else "No backend key — check .env"
    render_status_badge(dot_class, dot_text)

    st.markdown('<div class="section-label">System Prompt</div>', unsafe_allow_html=True)
    preset = st.selectbox(
        "Preset",
        list(DEFAULT_SYSTEM_PROMPTS.keys()),
        index=list(DEFAULT_SYSTEM_PROMPTS.keys()).index(st.session_state.system_prompt_choice),
        label_visibility="collapsed",
    )
    st.session_state.system_prompt_choice = preset

    if preset == "Custom":
        system_prompt_text = st.text_area(
            "Custom system prompt",
            value=st.session_state.custom_system_prompt,
            placeholder='e.g. "You are a professional software engineer."',
            height=90,
            label_visibility="collapsed",
        )
        st.session_state.custom_system_prompt = system_prompt_text
    else:
        system_prompt_text = DEFAULT_SYSTEM_PROMPTS[preset]
        st.caption(f"“{system_prompt_text}”")

    st.markdown('<div class="section-label">Prompt Templates</div>', unsafe_allow_html=True)
    all_templates = {**BUILT_IN_TEMPLATES, **st.session_state.custom_templates}
    template_cols = st.columns(2)
    for i, (tname, ttext) in enumerate(all_templates.items()):
        col = template_cols[i % 2]
        if col.button(tname, use_container_width=True, key=f"tmpl_{tname}"):
            st.session_state.chat_box = ttext
            st.rerun()

    with st.expander("➕ Save a custom template"):
        new_tname = st.text_input("Template name", key="new_tname")
        new_ttext = st.text_area("Template text", key="new_ttext", height=70)
        if st.button("Save template"):
            if new_tname.strip() and new_ttext.strip():
                st.session_state.custom_templates[new_tname.strip()] = new_ttext
                st.success(f"Saved '{new_tname.strip()}'")
            else:
                st.warning("Give the template a name and some text first.")

    st.markdown('<div class="section-label">Chat Sessions</div>', unsafe_allow_html=True)
    session_names = {sid: s["name"] for sid, s in st.session_state.sessions.items()}
    current = st.selectbox(
        "Active session",
        list(session_names.keys()),
        format_func=lambda sid: session_names[sid],
        index=list(session_names.keys()).index(st.session_state.current_session),
        label_visibility="collapsed",
    )
    st.session_state.current_session = current

    current_sess_dict = st.session_state.sessions[st.session_state.current_session]
    new_sess_name = st.text_input(
        "Rename Current Session",
        value=current_sess_dict["name"],
        key="rename_session_input",
    )
    if new_sess_name != current_sess_dict["name"] and new_sess_name.strip():
        current_sess_dict["name"] = new_sess_name.strip()
        st.rerun()

    st.markdown('<div class="section-label">Usage</div>', unsafe_allow_html=True)
    st.caption(f"Total input tokens billed: **{sess['input_tokens']}**")
    # st.caption("_(each reply resends the full chat history, so this grows faster than message count)_")
    st.caption(f"Total output tokens: **{sess['output_tokens']}**")
    st.caption(f"Messages: **{len(sess['messages'])}**")

    if sess["messages"]:
        export_lines = [f"# {sess['name']} — exported {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
        for m in sess["messages"]:
            role = "**You**" if m["role"] == "user" else "**Assistant**"
            export_lines.append(f"{role}:\n\n{m['content']}\n")
        export_text = "\n---\n\n".join(export_lines)
        st.download_button(
            "⬇️ Export Chat (.md)",
            data=export_text.encode("utf-8"),
            file_name=f"{sess['name'].replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )


# --------------------------------------------------------------------------
# Main area — error alerts
# --------------------------------------------------------------------------
if st.session_state.api_error:
    st.error(st.session_state.api_error)
    if st.button("Clear Error"):
        st.session_state.api_error = None
        st.rerun()

# --------------------------------------------------------------------------
# Conversation history
# --------------------------------------------------------------------------
chat_box = st.container(height=500 if sess["messages"] else 320, border=True)
with chat_box:
    if not sess["messages"] and not st.session_state.api_error and not st.session_state.chat_box:
        render_empty_state()

    for msg in sess["messages"]:
        avatar = "🧑‍💻" if msg["role"] == "user" else "⚡"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("meta"):
                st.markdown(f'<div class="meta-line">{msg["meta"]}</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Streaming model logic
# --------------------------------------------------------------------------
def stream_gemini(model_id, system_prompt, history):
    client = genai.Client(api_key=GEMINI_API_KEY)
    gemini_contents = []
    for m in history:
        role = "user" if m["role"] == "user" else "model"
        gemini_contents.append({"role": role, "parts": [{"text": m["content"]}]})

    config = types.GenerateContentConfig(system_instruction=system_prompt if system_prompt else None)
    response_stream = client.models.generate_content_stream(model=model_id, contents=gemini_contents, config=config)

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if chunk.usage_metadata:
            in_tokens = chunk.usage_metadata.prompt_token_count
            out_tokens = chunk.usage_metadata.candidates_token_count
        yield chunk.text, in_tokens, out_tokens


def stream_openai(model_id, system_prompt, history):
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages = [{"role": "system", "content": system_prompt or ""}]
    for m in history:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})

    response_stream = client.chat.completions.create(
        model=model_id, messages=messages, max_tokens=1500, stream=True, stream_options={"include_usage": True}
    )

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if chunk.usage:
            in_tokens = chunk.usage.prompt_tokens
            out_tokens = chunk.usage.completion_tokens
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        yield delta, in_tokens, out_tokens


def stream_groq(model_id, system_prompt, history):
    client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    messages = [{"role": "system", "content": system_prompt or ""}]
    for m in history:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})

    response_stream = client.chat.completions.create(
        model=model_id, messages=messages, max_tokens=1500, stream=True, stream_options={"include_usage": True}
    )

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if chunk.usage:
            in_tokens = chunk.usage.prompt_tokens
            out_tokens = chunk.usage.completion_tokens
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        yield delta, in_tokens, out_tokens


def stream_openrouter(model_id, system_prompt, history):
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "FLASH AI",
        },
    )
    messages = [{"role": "system", "content": system_prompt or ""}]
    for m in history:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})

    response_stream = client.chat.completions.create(
        model=model_id, messages=messages, max_tokens=1500, stream=True, stream_options={"include_usage": True}
    )

    in_tokens, out_tokens = 0, 0
    for chunk in response_stream:
        if getattr(chunk, "usage", None):
            in_tokens = chunk.usage.prompt_tokens
            out_tokens = chunk.usage.completion_tokens
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        yield delta, in_tokens, out_tokens


STREAM_DISPATCH = {
    "gemini": stream_gemini,
    "openai": stream_openai,
    "groq": stream_groq,
    "openrouter": stream_openrouter,
}


# --------------------------------------------------------------------------
# Template staging box
# --------------------------------------------------------------------------
final_payload = ""

if st.session_state.chat_box:
    render_template_banner()
    edited_template = st.text_area("Edit Template Text:", value=st.session_state.chat_box, height=110, label_visibility="collapsed")
    final_payload = edited_template

    if st.button("❌ Discard Template"):
        st.session_state.chat_box = ""
        st.rerun()

# --------------------------------------------------------------------------
# Chat input
# --------------------------------------------------------------------------
user_input = st.chat_input("Message FLASH AI, or press Enter to send the staged template…")

if user_input:
    if final_payload:
        user_input = final_payload + "\n" + user_input.strip()
    st.session_state.chat_box = ""

# --------------------------------------------------------------------------
# Submission processing
# --------------------------------------------------------------------------
if user_input:
    prompt_text = user_input.strip()
    st.session_state.api_error = None

    if selected_provider == "gemini" and genai is None:
        st.session_state.api_error = "❌ The `google-genai` package is not installed."
        st.rerun()
    elif selected_provider in ("openai", "groq", "openrouter") and OpenAI is None:
        st.session_state.api_error = "❌ The `openai` package is not installed."
        st.rerun()
    elif not PROVIDER_KEYS[selected_provider]:
        st.session_state.api_error = (
            f"🔒 No backend API key configured for **{model_label}**. "
            f"Add it to your `.env` file and restart the app."
        )
        st.rerun()
    else:
        maybe_rename_session(sess, prompt_text)
        sess["messages"].append({"role": "user", "content": prompt_text})

        try:
            with chat_box:
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(prompt_text)

                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("<div class='thinking-bubble'>⚡ Flashing<span class='typing-caret'>▌</span></div>", unsafe_allow_html=True)

                placeholder = None
                full_reply = ""
                in_tokens, out_tokens = 0, 0
                start = time.time()

                stream_fn = STREAM_DISPATCH[selected_provider]
                stream_gen = stream_fn(selected_model, system_prompt_text, sess["messages"])

                for text_chunk, i_tok, o_tok in stream_gen:
                    if placeholder is None:
                        thinking_placeholder.empty()
                        with st.chat_message("assistant", avatar="⚡"):
                            placeholder = st.empty()

                    in_tokens = i_tok if i_tok else in_tokens
                    out_tokens = o_tok if o_tok else out_tokens

                    for token in re.findall(r"\S+|\s+", text_chunk):
                        full_reply += token
                        placeholder.markdown(full_reply + " <span class='typing-caret'>▌</span>", unsafe_allow_html=True)
                        if token.strip():
                            time.sleep(0.02)

                if placeholder is not None:
                    elapsed = time.time() - start
                    meta = f"⏱ {elapsed:.2f}s · {in_tokens} in / {out_tokens} out tokens"
                    placeholder.markdown(full_reply)
                    st.markdown(f'<div class="meta-line">{meta}</div>', unsafe_allow_html=True)

            sess["messages"].append({"role": "assistant", "content": full_reply, "meta": meta})
            sess["input_tokens"] += in_tokens
            sess["output_tokens"] += out_tokens

        except Exception as e:
            msg = str(e).lower()
            if any(k in msg for k in ["authent", "api key", "401", "permission"]):
                st.session_state.api_error = f"🔒 Invalid backend API key for **{model_label}**."
            elif "connect" in msg or "timeout" in msg:
                st.session_state.api_error = f"🌐 Connection failed while reaching **{model_label}**."
            elif "rate" in msg or "429" in msg:
                st.session_state.api_error = f"⏳ Rate limit reached for **{model_label}**."
            else:
                st.session_state.api_error = f"❌ API Error: {str(e)}"

            if sess["messages"] and sess["messages"][-1]["role"] == "user":
                sess["messages"].pop()

        st.rerun()