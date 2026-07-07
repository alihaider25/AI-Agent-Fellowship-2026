"""Shared CSS and UI styling helpers for the FLASH AI app."""

import streamlit as st


def inject_css(dark: bool = True) -> None:
    """Inject the application's visual theme and component styling."""
    del dark

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700;800&family=Nunito:wght@400;600;700&display=swap');

        :root {
            --bg: #0a0f1c;
            --bg-grad-a: #111827;
            --bg-grad-b: #060816;
            --panel: rgba(17, 24, 39, 0.78);
            --panel-solid: #111827;
            --panel-2: rgba(100, 116, 139, 0.12);
            --text: #f8fafc;
            --text-sub: #cbd5e1;
            --accent: #34d399;
            --accent-2: #2dd4bf;
            --border: rgba(148, 163, 184, 0.2);
            --success: #34d399;
            --danger: #fb7185;
            --shadow: 0 18px 45px rgba(2, 6, 23, 0.4);
            --glow: 0 0 0 1px rgba(52, 211, 153, 0.24), 0 12px 40px rgba(52, 211, 153, 0.16);
            --radius-sm: 10px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --radius-xl: 28px;
            --radius-pill: 999px;
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 12px;
            --space-4: 16px;
            --space-5: 24px;
            --font-title: 1.9rem;
            --font-body: 0.96rem;
            --font-sub: 0.85rem;
            --font-meta: 0.76rem;
            --ease: cubic-bezier(0.34, 1.56, 0.64, 1);
            --dur-fast: 160ms;
            --dur-base: 240ms;
            --dur-slow: 420ms;
        }

        html, body, [class*="css"] {
            font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: radial-gradient(1200px 600px at 10% -10%, rgba(52, 211, 153, 0.16) 0%, transparent 55%),
                        radial-gradient(900px 500px at 100% 0%, rgba(45, 212, 191, 0.12) 0%, transparent 50%),
                        linear-gradient(135deg, var(--bg-grad-a), var(--bg-grad-b));
            color: var(--text);
            transition: background var(--dur-slow) var(--ease), color var(--dur-slow) var(--ease);
            background-size: 140% 140%;
            animation: drift 18s ease-in-out infinite alternate;
        }

        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stMarkdownContainer"] li,
        .stApp [data-testid="stMarkdownContainer"] code,
        .stApp [data-testid="stCaptionContainer"],
        .stApp [data-testid="stMetricValue"],
        .stApp [data-testid="stMetricLabel"],
        .stApp [data-testid="stExpander"] summary,
        .stApp [data-testid="stSidebar"] *,
        .stApp [data-testid="stAlert"] * {
            color: var(--text) !important;
        }

        .stApp [data-testid="stAlert"] {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
        }

        * { scroll-behavior: smooth; }
        #MainMenu, footer { visibility: hidden; }

        [data-testid="stToolbar"],
        header[data-testid="stHeader"],
        header[data-testid="stHeader"] > div,
        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] [data-testid="stBaseButton"],
        header[data-testid="stHeader"] [data-testid="stStatusWidget"] {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        header[data-testid="stHeader"] *,
        [data-testid="stToolbar"] * {
            color: var(--text-sub) !important;
        }

        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"],
        .main .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding: var(--space-4) var(--space-5) var(--space-4) !important;
            animation: fadeIn var(--dur-slow) var(--ease);
        }
        .block-container > div:first-child {
            margin-top: -4px !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(9, 16, 30, 0.98), rgba(15, 23, 42, 0.97));
            border-right: 1px solid rgba(148, 163, 184, 0.24);
        }
        section[data-testid="stSidebar"] .block-container {
            background: transparent;
        }
        section[data-testid="stSidebar"] .block-container {
            animation: slideInLeft var(--dur-slow) var(--ease);
            padding-top: var(--space-4);
        }
        section[data-testid="stSidebar"] *,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] button,
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea,
        section[data-testid="stSidebar"] select,
        section[data-testid="stSidebar"] [role="combobox"],
        section[data-testid="stSidebar"] [role="textbox"],
        section[data-testid="stSidebar"] [data-baseweb="select"] > div,
        section[data-testid="stSidebar"] [data-baseweb="input"] > div {
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stTextInput"] input,
        section[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="input"],
        section[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="input"] > div,
        section[data-testid="stSidebar"] [data-testid="stTextInput"] [role="textbox"],
        section[data-testid="stSidebar"] [data-testid="stTextArea"] textarea,
        section[data-testid="stSidebar"] [data-testid="stTextArea"] [data-baseweb="textarea"],
        section[data-testid="stSidebar"] [data-testid="stTextArea"] [data-baseweb="textarea"] > div,
        section[data-testid="stSidebar"] [data-testid="stTextArea"] [role="textbox"],
        section[data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder,
        section[data-testid="stSidebar"] [data-testid="stTextArea"] textarea::placeholder {
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
        }
        section[data-testid="stSidebar"] ::placeholder {
            color: var(--text-sub) !important;
        }

        .brand-header {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            padding: var(--space-3) var(--space-5);
            margin-bottom: var(--space-3);
            border-radius: var(--radius-xl);
            background: linear-gradient(120deg, rgba(56,189,248,0.14), rgba(129,140,248,0.12));
            border: 1px solid var(--border);
            box-shadow: var(--glow);
            backdrop-filter: blur(12px);
            position: relative;
            overflow: hidden;
        }
        .brand-header::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
            transform: translateX(-100%);
            animation: shimmer 6s linear infinite;
        }
        .brand-icon {
            font-size: 1.8rem;
            width: 50px; height: 50px;
            display: flex; align-items: center; justify-content: center;
            border-radius: var(--radius-pill);
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 10px 24px rgba(56, 189, 248, 0.24);
        }
        .brand-title {
            font-family: 'Quicksand', sans-serif;
            font-weight: 800;
            font-size: var(--font-title);
            background: linear-gradient(90deg, var(--text), var(--accent));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            letter-spacing: -0.5px;
            line-height: 1.1;
        }
        .brand-sub {
            color: var(--text-sub);
            font-size: var(--font-sub);
            margin-top: 2px;
        }

        .app-title {
            font-family: 'Quicksand', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            color: var(--text);
            display: flex; align-items: center; gap: var(--space-2);
            margin-bottom: 2px;
        }
        .app-subtitle {
            color: var(--text-sub);
            font-size: var(--font-sub);
            margin-bottom: var(--space-4);
            line-height: 1.6;
        }
        .meta-line {
            color: var(--text-sub);
            font-size: var(--font-meta);
            margin-top: var(--space-1);
            animation: fadeIn var(--dur-base) var(--ease) forwards;
        }

        .section-label {
            font-family: 'Quicksand', sans-serif;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-sub);
            margin: var(--space-4) 0 var(--space-2) 0;
        }

        .stChatMessage {
            background: transparent;
            backdrop-filter: none;
            border: none;
            border-radius: 0;
            padding: var(--space-2) 0;
            box-shadow: none;
            transition: none;
            animation: messageIn var(--dur-base) var(--ease);
        }
        .stChatMessage:hover {
            transform: none;
            box-shadow: none;
            border-color: transparent;
            background: transparent;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) {
            background: transparent;
            border: none;
            border-radius: 0;
            width: 100% !important;
            box-shadow: none;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) > div {
            height: 100%;
            max-height: 100%;
            overflow-y: auto !important;
            overflow-x: hidden;
            padding-right: 0.35rem;
            padding-bottom: 0.5rem;
            scrollbar-width: thin;
            scrollbar-color: var(--border) transparent;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) > div::-webkit-scrollbar { width: 8px; }
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stChatMessage"]) > div::-webkit-scrollbar-thumb {
            background-color: var(--border);
            border-radius: var(--radius-sm);
        }

        .stButton>button {
            border-radius: var(--radius-pill);
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
            color: var(--text);
            font-weight: 700;
            font-family: 'Quicksand', sans-serif;
            transition: transform var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease), border-color var(--dur-fast) var(--ease), background-color var(--dur-fast) var(--ease), filter var(--dur-fast) var(--ease);
        }
        .stButton>button:hover {
            transform: translateY(-2px) scale(1.02);
            border-color: rgba(56, 189, 248, 0.52);
            box-shadow: 0 10px 24px rgba(56, 189, 248, 0.18);
            filter: brightness(1.04);
        }
        .stButton>button:active { transform: translateY(0px) scale(0.97); }

        div[data-testid="stSidebar"] .stButton>button {
            background: transparent;
        }

        section[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color: #020617;
            border: none;
            font-weight: 800;
            box-shadow: 0 10px 24px rgba(56, 189, 248, 0.24);
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stChatInput"] input,
        [data-testid="stChatInput"] textarea,
        [data-baseweb="select"] > div {
            border-radius: var(--radius-pill) !important;
            background: transparent !important;
            background-color: transparent !important;
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
            border: none !important;
            box-shadow: none !important;
            transition: border-color var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease), transform var(--dur-fast) var(--ease), background var(--dur-fast) var(--ease);
        }
        [data-testid="stTextArea"] textarea {
            border-radius: var(--radius-lg) !important;
            min-height: 92px;
        }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder,
        [data-testid="stChatInput"] input::placeholder,
        [data-testid="stChatInput"] textarea::placeholder {
            color: rgba(248, 250, 252, 0.6) !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stChatInput"] input:focus,
        [data-testid="stChatInput"] textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.18) !important;
            transform: translateY(-1px);
            background: transparent !important;
        }

        [data-testid="stChatInput"],
        .stChatInput {
            border-radius: var(--radius-xl) !important;
            border: 1px solid var(--border) !important;
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            transition: box-shadow var(--dur-base) var(--ease), border-color var(--dur-fast) var(--ease);
        }
        [data-testid="stChatInput"]:focus-within,
        .stChatInput:focus-within {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            border-color: rgba(56, 189, 248, 0.42) !important;
        }
        .stChatInput > div,
        .stChatInput > div > div,
        .stChatInput > div > div > div,
        .stChatInput textarea,
        .stChatInput input,
        .stChatInput [role="textbox"],
        [data-testid="stChatInput"] [data-baseweb="input"],
        [data-testid="stChatInput"] [data-baseweb="textarea"],
        [data-testid="stChatInput"] [data-baseweb="base-input"],
        [data-testid="stChatInput"] [data-baseweb="base-input"] > div,
        .st-as.st-am.st-cx.st-b4.st-b5.st-do.st-af.st-cd.st-cv.st-ai.st-aj.st-b6.st-dm,
        .st-ak.st-as.st-ar.st-am.st-cy.st-cz.st-d0.st-d1.st-az.st-b0.st-b1.st-b2.st-cu.st-b4.st-b5.st-de.st-df.st-dg.st-dh.st-di.st-dj.st-dk.st-dl.st-dm.st-d6.st-cw.st-dn.st-c1 {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        .stChatInput textarea,
        .stChatInput input,
        .stChatInput [role="textbox"],
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
        }
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input,
        .stChatInput textarea,
        .stChatInput input {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            caret-color: var(--accent) !important;
        }
        [data-testid="stChatInput"] textarea:focus,
        [data-testid="stChatInput"] input:focus,
        .stChatInput textarea:focus,
        .stChatInput input:focus {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] > div > div,
        [data-testid="stChatInput"] > div > div > div {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }

        [data-testid="stChatInput"] button,
        .stChatInput button {
            position: relative !important;
            width: 42px !important;
            min-width: 42px !important;
            height: 42px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
            color: transparent !important;
            border: none !important;
            box-shadow: 0 8px 20px rgba(52, 211, 153, 0.22) !important;
        }
        [data-testid="stChatInput"] button::before,
        .stChatInput button::before {
            content: "⚡";
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            color: #020617;
            font-weight: 800;
        }
        [data-testid="stChatInput"] button svg,
        .stChatInput button svg,
        [data-testid="stChatInput"] button path,
        .stChatInput button path {
            display: none !important;
        }

        .st-emotion-cache-128upt6.eqt0gmo3,
        .st-emotion-cache-1y34ygi.eqt0gmo7 {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }

        .accent-badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.12);
            color: #bae6fd;
            border: 1px solid rgba(56, 189, 248, 0.24);
            border-radius: var(--radius-pill);
            padding: 3px 12px;
            font-size: var(--font-meta);
            font-weight: 700;
            font-family: 'Quicksand', sans-serif;
        }
        .status-dot {
            display: inline-block;
            width: 8px; height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        .status-dot.ok { background: var(--success); box-shadow: 0 0 8px var(--success); }
        .status-dot.bad { background: var(--danger); box-shadow: 0 0 8px var(--danger); }

        .template-staging {
            background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(129,140,248,0.1));
            border: 1px dashed rgba(56, 189, 248, 0.38);
            padding: var(--space-3) var(--space-4);
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-3);
            animation: slideInUp var(--dur-base) var(--ease);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .chat-empty-hint {
            margin: 0.15rem 0 0.65rem 0;
            padding: 0.65rem 0.8rem;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(148, 163, 184, 0.16);
            color: #e2e8f0;
            line-height: 1.5;
        }
        .thinking-bubble {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            width: fit-content;
            margin: 0.2rem 0 0.35rem 0;
            padding: 0.55rem 0.75rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(148, 163, 184, 0.16);
            color: var(--text-sub);
            font-size: 0.92rem;
            animation: pulse 1.05s ease-in-out infinite;
        }

        div[data-testid="stAlert"] {
            border-radius: var(--radius-md);
            animation: slideInUp var(--dur-base) var(--ease);
        }

        hr { border-color: var(--border) !important; }

        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideInLeft { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes slideInUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes messageIn { from { opacity: 0; transform: translateY(6px) scale(0.99); } to { opacity: 1; transform: translateY(0) scale(1); } }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
        @keyframes drift { 0% { background-position: 0% 50%; } 100% { background-position: 100% 50%; } }
        @keyframes shimmer { 100% { transform: translateX(100%); } }
        .typing-caret { animation: pulse 1s var(--ease) infinite; color: var(--accent); }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.001ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.001ms !important;
                scroll-behavior: auto !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header() -> None:
    st.markdown(
        """
        <div class="brand-header">
            <div class="brand-icon">⚡</div>
            <div>
                <div class="brand-title">FLASH AI</div>
                <div class="brand-sub">Multi-model chat workspace — Gemini · GPT-4o · Groq</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_title() -> None:
    st.markdown('<div class="app-title">⚡ FLASH AI</div>', unsafe_allow_html=True)
