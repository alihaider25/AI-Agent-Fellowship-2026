"""
Theming — scalable design-token CSS system with animations & transitions.

Design tokens are declared once as CSS custom properties (--variables), so the
whole theme can be re-skinned by changing values in one place instead of
hunting through selectors. Two palettes (light/dark) are swapped by toggling
the token block that gets injected.
"""

import streamlit as st


def inject_css(dark: bool) -> None:
    if dark:
        tokens = {
            "--bg": "#12151C",
            "--panel": "#1A1E29",
            "--panel-2": "#20263380",
            "--text": "#EDEFF5",
            "--text-sub": "#9AA1B4",
            "--accent": "#4B9CFA",
            "--accent-2": "#7C6CFF",
            "--border": "#262B3A",
            "--success": "#3ECF8E",
            "--danger": "#FF6B6B",
            "--shadow": "0 8px 24px rgba(0,0,0,0.35)",
        }
    else:
        tokens = {
            "--bg": "#F7F8FA",
            "--panel": "#FFFFFF",
            "--panel-2": "#F0F2F5C0",
            "--text": "#1C2029",
            "--text-sub": "#6B7280",
            "--accent": "#1A73E8",
            "--accent-2": "#6C5CE7",
            "--border": "#E4E7EC",
            "--success": "#1FA971",
            "--danger": "#E5484D",
            "--shadow": "0 8px 24px rgba(20,20,40,0.08)",
        }

    # Fixed scale tokens — shared across both themes, kept separate so
    # spacing / radius / motion can be tuned independently of color.
    scale = {
        "--radius-sm": "6px",
        "--radius-md": "10px",
        "--radius-lg": "14px",
        "--radius-xl": "18px",
        "--space-1": "4px",
        "--space-2": "8px",
        "--space-3": "12px",
        "--space-4": "16px",
        "--space-5": "24px",
        "--font-title": "1.6rem",
        "--font-body": "0.95rem",
        "--font-sub": "0.85rem",
        "--font-meta": "0.78rem",
        "--ease": "cubic-bezier(0.4, 0, 0.2, 1)",
        "--dur-fast": "140ms",
        "--dur-base": "220ms",
        "--dur-slow": "420ms",
    }

    root_vars = "\n".join(f"{k}: {v};" for k, v in {**tokens, **scale}.items())

    st.markdown(
        f"""
        <style>
        :root {{
            {root_vars}
        }}

        .stApp {{
            background-color: var(--bg);
            color: var(--text);
            transition: background-color var(--dur-slow) var(--ease),
                        color var(--dur-slow) var(--ease);
        }}

        * {{
            scroll-behavior: smooth;
        }}

        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"],
        .main .block-container {{
            max-width: 100% !important;
            width: 100% !important;
            padding-left: var(--space-5) !important;
            padding-right: var(--space-5) !important;
            padding-top: var(--space-5) !important;
            animation: fadeIn var(--dur-slow) var(--ease);
        }}

        section[data-testid="stSidebar"] {{
            background-color: var(--panel);
            border-right: 1px solid var(--border);
            transition: background-color var(--dur-slow) var(--ease),
                        border-color var(--dur-slow) var(--ease);
        }}

        section[data-testid="stSidebar"] .block-container {{
            animation: slideInLeft var(--dur-slow) var(--ease);
        }}

        .app-title {{
            font-family: 'Georgia', serif;
            font-weight: 700;
            font-size: var(--font-title);
            color: var(--text);
            letter-spacing: -0.5px;
            margin-bottom: var(--space-1);
            display: flex;
            align-items: center;
            gap: var(--space-2);
        }}
        .app-subtitle {{
            color: var(--text-sub);
            font-size: var(--font-sub);
            margin-bottom: var(--space-4);
            line-height: 1.5;
        }}
        .meta-line {{
            color: var(--text-sub);
            font-size: var(--font-meta);
            margin-top: var(--space-1);
            opacity: 0;
            animation: fadeIn var(--dur-base) var(--ease) forwards;
        }}

        .stChatMessage {{
            background-color: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: var(--space-1) var(--space-2);
            transition: transform var(--dur-fast) var(--ease),
                        box-shadow var(--dur-fast) var(--ease),
                        border-color var(--dur-fast) var(--ease);
            animation: messageIn var(--dur-base) var(--ease);
        }}
        .stChatMessage:hover {{
            box-shadow: var(--shadow);
            border-color: var(--accent);
        }}

        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) {{
            background-color: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            width: 100% !important;
            transition: background-color var(--dur-slow) var(--ease),
                        border-color var(--dur-slow) var(--ease);
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) > div {{
            overflow-y: auto !important;
            scrollbar-width: thin;
            scrollbar-color: var(--border) transparent;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) > div::-webkit-scrollbar {{
            width: 8px;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) > div::-webkit-scrollbar-thumb {{
            background-color: var(--border);
            border-radius: var(--radius-sm);
        }}

        .stButton>button {{
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
            transition: transform var(--dur-fast) var(--ease),
                        box-shadow var(--dur-fast) var(--ease),
                        border-color var(--dur-fast) var(--ease),
                        background-color var(--dur-fast) var(--ease);
        }}
        .stButton>button:hover {{
            transform: translateY(-1px);
            border-color: var(--accent);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        .stButton>button:active {{
            transform: translateY(0px) scale(0.98);
        }}

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-baseweb="select"] > div {{
            border-radius: var(--radius-sm) !important;
            transition: border-color var(--dur-fast) var(--ease),
                        box-shadow var(--dur-fast) var(--ease);
        }}
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent) !important;
        }}

        [data-testid="stChatInput"] {{
            border-radius: var(--radius-lg) !important;
            transition: box-shadow var(--dur-base) var(--ease);
        }}
        [data-testid="stChatInput"]:focus-within {{
            box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent);
        }}

        [data-testid="stToggle"] {{
            transition: opacity var(--dur-fast) var(--ease);
        }}

        .accent-badge {{
            display: inline-block;
            background-color: color-mix(in srgb, var(--accent) 14%, transparent);
            color: var(--accent);
            border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent);
            border-radius: var(--radius-sm);
            padding: 1px 6px;
            font-size: var(--font-meta);
            font-weight: 600;
            transition: background-color var(--dur-fast) var(--ease);
        }}

        .template-staging {{
            background-color: var(--panel);
            border: 1px dashed var(--accent);
            padding: var(--space-3);
            border-radius: var(--radius-md);
            margin-bottom: var(--space-3);
            animation: slideInUp var(--dur-base) var(--ease);
        }}

        div[data-testid="stAlert"] {{
            border-radius: var(--radius-md);
            animation: slideInUp var(--dur-base) var(--ease);
        }}

        hr {{
            border-color: var(--border) !important;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
        }}
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-10px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes slideInUp {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes messageIn {{
            from {{ opacity: 0; transform: translateY(6px) scale(0.99); }}
            to   {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50%      {{ opacity: 0.35; }}
        }}
        .typing-caret {{
            animation: pulse 1s var(--ease) infinite;
        }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.001ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.001ms !important;
                scroll-behavior: auto !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
