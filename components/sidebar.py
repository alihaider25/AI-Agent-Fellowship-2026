"""
Sidebar UI: model picker, system prompt, prompt templates, session manager,
dark mode toggle, and usage stats.

Note: there is intentionally NO field here to type in an API key. Keys live
only in utils/secrets.py (backed by .env / environment variables / Streamlit
secrets). This component only reads utils.secrets.PROVIDER_KEYS to show
whether a backend key is configured for the selected model.
"""

from datetime import datetime

import streamlit as st

from config import DEFAULT_SYSTEM_PROMPTS, MODEL_OPTIONS
from core.session_state import new_session
from utils.secrets import PROVIDER_KEYS
from utils.templates import BUILT_IN_TEMPLATES


def render_sidebar(sess: dict) -> tuple[str, str, str, str]:
    """Render the sidebar and return (model_label, provider, model_id, system_prompt_text)."""

    with st.sidebar:
        st.markdown('<div class="app-title">💬 AI Chat Workspace</div>', unsafe_allow_html=True)

        current_model_label = "Gemini 2.5 Flash (Google)"
        if "model_label" in st.session_state and st.session_state.model_label in MODEL_OPTIONS:
            current_model_label = st.session_state.model_label

        st.markdown(
            f'<div class="app-subtitle">Session: <span class="accent-badge">{sess["name"]}</span><br>'
            f"Model: <span class='accent-badge'>{current_model_label.split(' (')[0]}</span></div>",
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown("### ⚙️ Configuration")
        model_label = st.selectbox("Model", list(MODEL_OPTIONS.keys()), index=0, key="model_label")
        selected_provider = MODEL_OPTIONS[model_label]["provider"]
        selected_model = MODEL_OPTIONS[model_label]["model_id"]

        if not PROVIDER_KEYS[selected_provider]:
            st.caption(
                f"⚠️ No backend API key configured for **{model_label.split(' (')[0]}**. "
                f"Set it in your `.env` file or server environment variables."
            )
        else:
            st.caption(f"🔒 Using backend-configured key for **{model_label.split(' (')[0]}**.")

        st.divider()
        st.markdown("### 🎭 System Prompt")
        preset = st.selectbox(
            "Preset",
            list(DEFAULT_SYSTEM_PROMPTS.keys()),
            index=list(DEFAULT_SYSTEM_PROMPTS.keys()).index(st.session_state.system_prompt_choice),
        )
        st.session_state.system_prompt_choice = preset

        if preset == "Custom":
            system_prompt_text = st.text_area(
                "Custom system prompt",
                value=st.session_state.custom_system_prompt,
                placeholder='e.g. "You are a professional software engineer."',
                height=90,
            )
            st.session_state.custom_system_prompt = system_prompt_text
        else:
            system_prompt_text = DEFAULT_SYSTEM_PROMPTS[preset]
            st.caption(f"“{system_prompt_text}”")

        st.divider()
        st.markdown("### 📝 Prompt Templates")
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

        st.divider()
        st.markdown("### 💬 Chat Sessions")
        session_names = {sid: s["name"] for sid, s in st.session_state.sessions.items()}
        current = st.selectbox(
            "Active session",
            list(session_names.keys()),
            format_func=lambda sid: session_names[sid],
            index=list(session_names.keys()).index(st.session_state.current_session),
        )
        st.session_state.current_session = current

        current_sess_dict = st.session_state.sessions[st.session_state.current_session]
        new_sess_name = st.text_input("Rename Current Session", value=current_sess_dict["name"])
        if new_sess_name != current_sess_dict["name"] and new_sess_name.strip():
            current_sess_dict["name"] = new_sess_name.strip()
            st.rerun()

        if st.button("➕ New Chat Session", use_container_width=True):
            st.session_state.current_session = new_session()
            st.session_state.api_error = None
            st.rerun()

        st.divider()
        st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

        st.divider()
        st.markdown("### 📊 Usage")
        st.caption(f"Input tokens: **{sess['input_tokens']}**")
        st.caption(f"Output tokens: **{sess['output_tokens']}**")
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

    return model_label, selected_provider, selected_model, system_prompt_text
