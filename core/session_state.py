"""Streamlit session-state initialization and chat-session helpers."""

import uuid

import streamlit as st


def new_session(name: str | None = None) -> str:
    """Create a new chat session and return its id."""
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "name": name or f"Chat {len(st.session_state.sessions) + 1}",
        "messages": [],
        "input_tokens": 0,
        "output_tokens": 0,
    }
    return session_id


def init_session_state() -> None:
    """Populate st.session_state with all defaults the app relies on."""
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
        first_id = new_session("Chat 1")
        st.session_state.current_session = first_id

    st.session_state.setdefault("system_prompt_choice", "General Assistant")
    st.session_state.setdefault("custom_system_prompt", "")
    st.session_state.setdefault("custom_templates", {})
    st.session_state.setdefault("dark_mode", False)
    st.session_state.setdefault("chat_box", "")
    st.session_state.setdefault("api_error", None)


def current_session() -> dict:
    """Return the dict for the currently active chat session."""
    return st.session_state.sessions[st.session_state.current_session]
