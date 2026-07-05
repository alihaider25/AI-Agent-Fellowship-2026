"""
Main chat area: message history display, template-staging workspace, the
chat input box, and the logic that streams a response from whichever
provider is currently selected.
"""

import time

import streamlit as st

from core.providers import STREAM_DISPATCH, provider_sdk_available
from utils.secrets import PROVIDER_KEYS


def render_chat_history(sess: dict) -> "st.delta_generator.DeltaGenerator":
    """Render the scrollable message history and return the container."""
    chat_box = st.container(height=580, border=True)
    with chat_box:
        for msg in sess["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("meta"):
                    st.markdown(f'<div class="meta-line">{msg["meta"]}</div>', unsafe_allow_html=True)
    return chat_box


def render_template_staging() -> str:
    """If a template was clicked, show an editable staging box. Returns staged text (or '')."""
    final_payload = ""
    if st.session_state.chat_box:
        st.markdown(
            '<div class="template-staging">📋 <b>Template Workspace</b> '
            '(Complete or edit your text below, then type anything in the chat field to execute)</div>',
            unsafe_allow_html=True,
        )
        edited_template = st.text_area("Edit Template Text:", value=st.session_state.chat_box, height=110)
        final_payload = edited_template

        if st.button("❌ Discard Template"):
            st.session_state.chat_box = ""
            st.rerun()

    return final_payload


def handle_submission(
    sess: dict,
    chat_box,
    model_label: str,
    selected_provider: str,
    selected_model: str,
    system_prompt_text: str,
) -> None:
    """Read the chat input, combine with any staged template, and stream a reply."""

    final_payload = render_template_staging()

    user_input = st.chat_input("Type your addition here, or press Enter to submit staged template…")

    if user_input:
        if final_payload:
            user_input = final_payload + "\n" + user_input.strip()
        st.session_state.chat_box = ""

    if not user_input:
        return

    prompt_text = user_input.strip()
    st.session_state.api_error = None

    if not provider_sdk_available(selected_provider):
        pkg = "google-genai" if selected_provider == "gemini" else "openai"
        st.session_state.api_error = f"❌ The `{pkg}` package is not installed."
        st.rerun()
        return

    if not PROVIDER_KEYS[selected_provider]:
        st.session_state.api_error = (
            f"🔒 No backend API key configured for **{model_label}**. "
            f"Set the corresponding variable in your `.env` file or server environment."
        )
        st.rerun()
        return

    sess["messages"].append({"role": "user", "content": prompt_text})

    try:
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt_text)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_reply = ""
                in_tokens, out_tokens = 0, 0
                start = time.time()

                stream_fn = STREAM_DISPATCH[selected_provider]
                stream_gen = stream_fn(selected_model, system_prompt_text, sess["messages"])

                for text_chunk, i_tok, o_tok in stream_gen:
                    full_reply += text_chunk
                    in_tokens = i_tok if i_tok else in_tokens
                    out_tokens = o_tok if o_tok else out_tokens
                    placeholder.markdown(full_reply + " <span class='typing-caret'>▌</span>", unsafe_allow_html=True)

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
