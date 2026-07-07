# ⚡ FLASH AI

A multi-provider streaming chat workspace built with Streamlit — Gemini 2.5
Flash, GPT-4o, and Groq, all switchable from one modern interface.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and paste in whichever real key(s) you have:
```
OPENROUTER_API_KEY= PASTE_YOUR_OPENROUTER_API_KEY_HERE

All the four maodel used Same OPENROUTER API key and it work according to model automatically
```

You only need the ones you plan to use — a model without a configured key
will just show a red "No backend key" status in the sidebar instead of
crashing the app.

Run it:
Step 1 :

```bash
cp .env.example .env
```
Step 2 
```bash
streamlit run app.py
```
OR
if incase this not Run ,try to run below command in terminal 

```bash
python -m streamlit run app.py
```
## Security note

Never paste real API keys directly into `app.py` or any other tracked file.
Keys belong only in `.env` (already excluded via `.gitignore`) or in
`.streamlit/secrets.toml` if you deploy to Streamlit Community Cloud. If a
key is ever exposed — pasted in a chat, committed to a public repo, shared
in a screenshot — revoke it immediately from that provider's console and
generate a new one.

## Features

- Streaming responses from Gemini, GPT-4o, or Groq — pick a model, everything
  else is wired up automatically on the backend
- Custom or preset system prompts
- Prompt templates (built-in + save your own)
- Multiple named chat sessions
- Token usage + response time shown per message
- Export any chat as Markdown
- Dark / light mode toggle
- Friendly error handling for missing keys, bad keys, connection issues, and
  rate limits

## Internship Overview
This project was built as part of my internship. You can read about my learning objectives and internship goals [here](./Fellowship_2026_intro.md).
