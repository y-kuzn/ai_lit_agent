# pages/Help.py
import streamlit as st
import requests
import json

# Load Gemini API key
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent"

st.title("🆘 Help & Instructions")

st.markdown("""
### What is this?
AI Literature Helper is a research assistant that finds academic papers, analyzes their relevance using Gemini, and helps you export or save them.

### How to use:
1. Enter your research topic or keywords.
2. Choose a source: Google Scholar or Semantic Scholar.
3. Set how many papers to fetch and your minimum relevance score.
4. Optionally connect Zotero to save papers directly.
5. Click "Fetch & Analyze Articles".

### Export Options:
- BibTeX for citation managers
- Markdown for notes or documentation

### Zotero Integration:
- Requires API key, user ID, and collection ID.
- Only saves papers with relevance score ≥ your threshold.

### Troubleshooting:
- Missing modules? Check `requirements.txt`.
- API errors? Verify your keys in `.streamlit/secrets.toml` or Streamlit Cloud secrets.

---
""")

st.subheader("💬 Ask Gemini for Help")

# Initialize chat history
if "help_chat" not in st.session_state:
    st.session_state.help_chat = []

# Chat input
user_input = st.chat_input("Ask a question about using the app...")

if user_input:
    st.session_state.help_chat.append({"role": "user", "text": user_input})

    # Prepare Gemini prompt
    messages = [{"role": "user", "parts": [{"text": m["text"]}]} for m in st.session_state.help_chat if m["role"] == "user"]
    payload = {"contents": messages}

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    with st.spinner("Gemini is thinking..."):
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.session_state.help_chat.append({"role": "assistant", "text": reply})

# Display chat history
for msg in st.session_state.help_chat:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["text"])
    else:
        st.chat_message("assistant").markdown(msg["text"])
