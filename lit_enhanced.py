import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
import re
from pyzotero import zotero
import fitz  # PyMuPDF

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="AI Literature Helper",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Sidebar: Help Button
# ---------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center;">
    <a href="https://ntu-ai-literature-search-question.streamlit.app/" target="_blank">
        <button style="
            background-color: #ff4b5c;
            color: white;
            padding: 14px 28px;
            margin-top: 15px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.2s ease, background-color 0.3s ease;
        " onmouseover="this.style.backgroundColor='#e63946'; this.style.transform='scale(1.05)'" onmouseout="this.style.backgroundColor='#ff4b5c'; this.style.transform='scale(1)'">
            🆘 HELP ME! I’m Lost
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar: Controls
# ---------------------------
st.sidebar.title("🔧 Settings")
source = st.sidebar.selectbox("Choose source", ["Google Scholar", "Semantic Scholar", "PubMed"])
query = st.sidebar.text_input("Enter your research topic")
num_papers = st.sidebar.slider("Number of papers", 5, 50, 10)
min_score = st.sidebar.slider("Minimum relevance score", 0.0, 1.0, 0.5)
save_to_zotero = st.sidebar.checkbox("Save to Zotero", value=False)
allow_duplicates = st.sidebar.checkbox("Allow duplicate saves", value=False)

# ---------------------------
# Secrets Configuration
# ---------------------------
SCRAPERAPI_KEY = st.secrets["SCRAPERAPI_KEY"]
SEMANTIC_SCHOLAR_API_KEY = st.secrets["SEMANTIC_SCHOLAR_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# ---------------------------
# Main Title
# ---------------------------
st.title("📚 AI Literature Helper")
st.markdown("Search academic papers, analyze relevance with Gemini, and optionally save to Zotero.")

# ---------------------------
# Gemini Analysis Function
# ---------------------------
def analyze_article(title, abstract):
    prompt = f"Summarize this article and generate 5 relevant tags:\n\nTitle: {title}\nAbstract: {abstract}"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return reply
    except Exception as e:
        return f"❌ Gemini error: {e}"

# ---------------------------
# Zotero Save Function
# ---------------------------
def save_article_to_zotero(article, analysis, zotero_client, allow_duplicates):
    title = article["title"]
    doi = article.get("doi", "")
    url = article.get("url", "")
    
    if not allow_duplicates:
        existing = zotero_client.items(q=title, itemType="journalArticle")
        for item in existing:
            if "DOI" in item["data"] and item["data"]["DOI"] == doi:
                st.info(f"🔁 Skipped duplicate: {title}")
                return

    zotero_item = {
        "itemType": "journalArticle",
        "title": title,
        "abstractNote": article.get("abstract", ""),
        "url": url,
        "DOI": doi,
        "tags": [{"tag": tag.strip()} for tag in analysis.split("\n") if tag.strip()],
        "creators": [{"creatorType": "author", "firstName": "AI", "lastName": "Helper"}]
    }
    zotero_client.create_items([zotero_item])
    st.success(f"✅ Saved to Zotero: {title}")

# ---------------------------
# Simulated Article Fetch
# ---------------------------
def fetch_articles(query, source, num):
    return [{
        "title": f"{query} Study #{i+1}",
        "abstract": f"This is a simulated abstract for {query} article #{i+1}.",
        "doi": f"10.1234/example.{i+1}",
        "url": f"https://example.com/{query.replace(' ', '_')}/{i+1}"
    } for i in range(num)]

# ---------------------------
# Main Logic
# ---------------------------
if query:
    st.header("📚 AI Literature Results")
    articles = fetch_articles(query, source, num_papers)

    if save_to_zotero:
        ZOTERO_API_KEY = st.secrets["ZOTERO_API_KEY"]
        ZOTERO_USER_ID = st.secrets["ZOTERO_USER_ID"]
        ZOTERO_COLLECTION_ID = st.secrets["ZOTERO_COLLECTION_ID"]
        zotero_client = zotero.Zotero(ZOTERO_USER_ID, "user", ZOTERO_API_KEY)

    saved_count = 0
    skipped_count = 0

    for i, article in enumerate(articles):
        st.subheader(f"{i+1}. {article['title']}")
        st.markdown(f"**Abstract:** {article['abstract']}")
        st.markdown(f"[🔗 View Article]({article['url']})")

        with st.spinner("Analyzing with Gemini..."):
            analysis = analyze_article(article["title"], article["abstract"])

        st.markdown("**🧠 AI Summary & Tags:**")
        st.code(analysis)

        with st.expander("📤 Export Options"):
            bibtex = f"""@article{{{{{article['doi'].split('/')[-1]}}}}},
  title={{{{ {article['title']} }}}},
  author={{{{AI Helper}}}},
  journal={{{{Generated by AI Literature Helper}}}},
  year={{{{2025}}}},
  doi={{{{ {article['doi']} }}}},
  url={{{{ {article['url']} }}}}
}}"""
            st.download_button("Download BibTeX", bibtex, file_name=f"{article['title']}.bib", mime="text/plain")

            markdown = f"""### {article['title']}
**Abstract:** {article['abstract']}

**Tags:**  
{analysis}

[🔗 View Article]({article['url']})
"""
            st.download_button("Download Markdown", markdown, file_name=f"{article['title']}.md", mime="text/markdown")

        if save_to_zotero:
            try:
                before = len(zotero_client.items())
                save_article_to_zotero(article, analysis, zotero_client, allow_duplicates)
                after = len(zotero_client.items())
                if after > before:
                    saved_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                st.error(f"❌ Zotero error: {e}")
                skipped_count += 1

    if save_to_zotero:
        st.markdown("---")
        st.success(f"📦 Zotero Summary: Saved {saved_count} | Skipped {skipped_count}")



