import streamlit as st

# Page setup
st.set_page_config(page_title="AI Literature Helper – Help", page_icon="🆘", layout="wide")

# Sidebar navigation
st.sidebar.title("📘 Help Navigation")
section = st.sidebar.radio("Jump to section:", [
    "Overview",
    "How to Use",
    "Zotero Integration",
    "Contact"
])

# Section: Overview
if section == "Overview":
    st.title("🆘 Help & Instructions")
    st.markdown("""
    Welcome to **AI Literature Helper**, your personal research assistant powered by Gemini and Streamlit.

    This app helps you:
    - Search academic papers from Google Scholar or Semantic Scholar
    - Analyze relevance using Gemini AI
    - Export citations in BibTeX or Markdown
    - Save papers directly to Zotero

    Whether you're a student, researcher, or curious mind, this tool is designed to streamline your literature review process.
    """)

# Section: How to Use
elif section == "How to Use":
    st.header("🚀 How to Use the App")
    st.markdown("""
    1. **Enter your research topic** in the input field.
    2. **Choose a source**: Google Scholar or Semantic Scholar.
    3. **Set the number of papers** to fetch and your minimum relevance score.
    4. **Optionally connect Zotero** to save papers directly to your library.
    5. Click **Fetch & Analyze Articles** to begin.

    After analysis, you’ll see:
    - AI-generated tags
    - Summary and relevance score
    - Export buttons for BibTeX and Markdown
    """)
    
# Section: Zotero Integration
elif section == "Zotero Integration":
    st.header("📥 Zotero Integration")
    st.markdown("""
    Zotero is a free reference manager. You can connect it to this app to automatically save relevant papers.

    ### 🔧 What You Need
    - **Zotero API Key**: [Generate here](https://www.zotero.org/settings/keys)
    - **User ID**: Found in your Zotero account settings
    - **Collection ID**: Go to your Zotero library → right-click a collection → “Edit Collection” → copy the ID from the URL

    ### 📝 Add to Secrets
    ```toml
    ZOTERO_API_KEY = "your_zotero_key"
    ZOTERO_USER_ID = "your_user_id"
    ZOTERO_COLLECTION_ID = "your_collection_id"
    ```

    ### ✅ What Gets Saved
    - Only papers with a relevance score ≥ your threshold
    - Includes title, authors, abstract, tags, and URL

    > ⚠️ Zotero does not accept empty fields. Make sure your metadata is complete.
    """)

# Section: Contact
elif section == "Contact":
    st.header("📬 Contact & Feedback")
    st.markdown("""
    Have questions, suggestions, or found a bug?

    - Open an issue on [GitHub](https://github.com/y-kuzn/ai_lit_agent/issues)
    - Email the developer at: `kuzn0001@e.ntu.edu.sg`
    - Or leave feedback directly in the app (coming soon!)

    We’re constantly improving the AI Literature Helper—your input helps make it better.
    """)

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and Gemini")
