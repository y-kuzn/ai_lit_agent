import streamlit as st
import requests
import json

# Page config
st.set_page_config(page_title="AI Literature Helper – Help", page_icon="🆘")

# Gemini API setup
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent"

# Title and instructions
st.title("🆘 Help & Instructions")

st.markdown("""
Welcome to the **AI Literature Helper**! This tool helps you find, analyze, and organize academic papers using AI.

---

### 🚀 How to Use the App

1. **Enter your research topic** in the main input field.
2. **Choose a source**: Google Scholar or Semantic Scholar.
3. **Set the number of papers** to fetch and your minimum relevance score.
4. **Optionally connect Zotero** to save papers directly to your library.
5. Click **Fetch & Analyze Articles** to begin.

---

### 📦 Export Options

- **BibTeX**: For citation managers like Zotero, Mendeley, or EndNote.
- **Markdown**: For notes, documentation, or sharing summaries.

---

### 🔐 Zotero Integration

To save papers directly to Zotero:
- Provide your **Zotero API key**, **User ID**, and **Collection ID**.
- Only papers with a relevance score ≥ your threshold will be saved.

---

### 🛠️ Troubleshooting

- **Missing modules**: Make sure your `requirements.txt` includes all dependencies.
- **API errors**: Double-check your keys in `.streamlit/secrets.toml` or Streamlit Cloud secrets.
- **Gemini issues**: Try shorter prompts or switch to the `gemini-2.0-flash` model.

---

### 💬 Ask Gemini for Help
""")

# Chatbot section
st.subheader("💬 Gemini Assistant")

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

    try:
        with st.spinner("Gemini is thinking..."):
            response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            st.session_state.help_chat.append({"role": "assistant", "text": reply})
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        reason = e.response.reason
        st.error(f"Gemini API error: {status} – {reason}")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.stop()
