<<<<<<< HEAD
# 💬 AI Chat Workspace

A multi-provider Streamlit chat app supporting **Gemini 2.5 Flash**, **GPT-4o**, and **Groq (Llama 3.3 70B)**, with editable prompt templates, multiple chat sessions, dark mode, and a full-bleed animated UI.

## ✨ Features

- Switch between Gemini / OpenAI / Groq from a single dropdown — no code changes needed
- Streaming responses with live token usage
- Editable prompt templates (built-in + your own custom ones)
- Multiple named chat sessions, exportable to Markdown
- Light/dark theme with a CSS design-token system
- Backend-only API keys — never exposed in the UI

## 📁 Project Structure

```
ai-chat-workspace/
├── app.py                  # Entry point — wires everything together
├── config.py                # Model registry & system prompt presets
├── requirements.txt
├── .env.example              # Copy to .env and fill in your keys
├── .gitignore
├── utils/
│   ├── secrets.py            # Reads API keys from .env / environment / st.secrets
│   ├── theme.py               # CSS design tokens & animations
│   └── templates.py           # Built-in prompt templates
├── core/
│   ├── session_state.py       # Chat session management
│   └── providers.py           # Gemini / OpenAI / Groq streaming clients + dispatch
└── components/
    ├── sidebar.py              # Sidebar UI (model picker, prompts, sessions)
    └── chat.py                  # Chat history, input handling, streaming
```

## 🚀 Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/ai-chat-workspace.git
   cd ai-chat-workspace
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API keys**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and fill in whichever keys you have:
   ```env
   GEMINI_API_KEY=your-gemini-key
   OPENAI_API_KEY=your-openai-key
   GROQ_API_KEY=your-groq-key
   ```
   You don't need all three — the app will simply disable models you haven't provided a key for.

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 🔐 Secrets & Security

- API keys are **never** entered or displayed in the UI.
- `utils/secrets.py` reads keys in this priority order: environment variables → `.env` file → `st.secrets` (for Streamlit Community Cloud).
- `.env` and `.streamlit/secrets.toml` are both listed in `.gitignore` — **never commit real keys**.

### Deploying to Streamlit Community Cloud
Instead of a `.env` file, add your keys under your app's **Settings → Secrets** in this format:
```toml
GEMINI_API_KEY = "your-gemini-key"
OPENAI_API_KEY = "your-openai-key"
GROQ_API_KEY = "your-groq-key"
```

## 🛠️ Adding a New Provider

1. Add a `stream_<provider>()` generator function to `core/providers.py` (yield `(text_chunk, input_tokens, output_tokens)`).
2. Register it in `STREAM_DISPATCH`.
3. Add its key to `utils/secrets.py` and `.env.example`.
4. Add the model(s) to `MODEL_OPTIONS` in `config.py`.

## 📄 License

MIT — feel free to use and modify.
=======
# AI Agent Fellowship 2026

## 👋 Introduction

Hello! My name is **Ali Haider**.

I'm an aspiring **AI/NLP Engineer** with a strong interest in **Natural Language Processing**,**Large Language Models (LLMs)** and **Generative AI**.

---

## 🎓 University

The University of Faisalabad(TUF)

---

## 🚀 Fellowship Track

AI Agent Fellowship 2026

---

## 🎯 Career Goals

I aim to become an AI/NLP Engineer specializing in Natural Language Processing (NLP), Large Language Models (LLMs), and Generative AI. My goal is to build intelligent, production-ready AI applications that solve real-world problems while continuously sharpening my skills through hands-on projects.


---

## 💻 Technical Skills

### 🧠 Artificial Intelligence & NLP
- **Machine Learning (ML)** 
- **Natural Language Processing (NLP)** 
- **Large Language Models (LLMs)**
- **Hugging Face Transformers** 
- **Prompt Engineering** 

### 🐍 Languages & Backend
- **Python** 
- **Flask**
- **PHP** 

### 🌐 Frontend Development
- **HTML5 & CSS3**
- **JavaScript** 
- **Bootstrap**

### 🗄️ Databases
- **MySQL**

### 🔧 Version control
- **Git & GitHub:**

---

## 📚 Learning Goals

During this fellowship, I want to:

- **Build Autonomous Agents:** Design and deploy production-ready AI Agents.
- **Master Advanced LLMs:** Learn LLM Fine-Tuning and advanced Prompt Engineering.
- **Integration:** Master production workflows working with industry AI APIs.
- **Software Excellence:** Improve my problem-solving, clean coding, and software development skills.
- **Career Readiness:** Accelerate my growth toward a full-time AI Engineering career.

## Contact
- **Email** : alihaider25.dev@gmail.com
- **LinkedIn** : www.linkedin.com/in/ali-haider-13238b2a2

>>>>>>> 60f0d84b127536ef2b334eb4a6f5ae45c9430d13
