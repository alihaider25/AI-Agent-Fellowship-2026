"""
AI Chat Workspace — multi-provider chat interface (Gemini / GPT-4o / Groq)
with editable prompt templates, multiple chat sessions, dark mode, and a
full-bleed animated UI.

Run with:   streamlit run app.py

Setup:
  1. Copy .env.example to .env
  2. Fill in whichever API key(s) you have (GEMINI_API_KEY / OPENAI_API_KEY / GROQ_API_KEY)
  3. streamlit run app.py

See README.md for full setup instructions.
"""

import streamlit as st

from components.chat import handle_submission, render_chat_history
from components.sidebar import render_sidebar
from config import PAGE_ICON, PAGE_TITLE
from core.session_state import current_session, init_session_state
from utils.theme import inject_css

# --------------------------------------------------------------------------
# Page config (must be the first Streamlit call)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# State + theme
# --------------------------------------------------------------------------
init_session_state()
inject_css(st.session_state.dark_mode)

sess = current_session()

# --------------------------------------------------------------------------
# Sidebar (model picker, system prompt, templates, sessions, usage)
# --------------------------------------------------------------------------
model_label, selected_provider, selected_model, system_prompt_text = render_sidebar(sess)

# --------------------------------------------------------------------------
# Error banner
# --------------------------------------------------------------------------
if st.session_state.api_error:
    st.error(st.session_state.api_error)
    if st.button("Clear Error"):
        st.session_state.api_error = None
        st.rerun()

# --------------------------------------------------------------------------
# Chat history + input handling
# --------------------------------------------------------------------------
chat_box = render_chat_history(sess)
handle_submission(sess, chat_box, model_label, selected_provider, selected_model, system_prompt_text)

if not sess["messages"] and not st.session_state.api_error and not st.session_state.chat_box:
    st.info("👋 Pick a model on the left, choose a system prompt, and send a message to get started!")
