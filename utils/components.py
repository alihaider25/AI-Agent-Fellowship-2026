"""Small reusable Streamlit components for the FLASH AI app."""

import streamlit as st


def render_sidebar_summary(session_name: str, current_model_label: str) -> None:
    st.markdown(
        f'<div class="app-subtitle">Session: <span class="accent-badge">{session_name}</span><br>'
        f"Model: <span class='accent-badge'>{current_model_label.split(' (')[0]}</span></div>",
        unsafe_allow_html=True,
    )


def render_status_badge(dot_class: str, dot_text: str) -> None:
    st.markdown(
        f'<span class="status-dot {dot_class}"></span><span style="font-size:0.85rem;color:var(--text-sub)">{dot_text}</span>',
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.markdown(
        "<div class='chat-empty-hint'>👋 Pick a model on the left, choose a system prompt, and send a message to get started with FLASH AI!</div>",
        unsafe_allow_html=True,
    )


def render_template_banner() -> None:
    st.markdown(
        '<div class="template-staging">📋 <b>Template Workspace</b> — edit below, then type anything in the chat field to send it</div>',
        unsafe_allow_html=True,
    )


def render_thinking_placeholder() -> tuple[object, object]:
    placeholder = st.empty()
    placeholder.markdown("<div class='thinking-bubble'>⚡ Flashing<span class='typing-caret'>▌</span></div>", unsafe_allow_html=True)
    return placeholder, None
