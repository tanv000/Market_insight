import streamlit as st
from config import CACHE_PATH
from data_processing import process_urls
from query_handler import parse_summarize_query, create_prompt, generate_response
from utils import save_cache, load_cache, cache_exists
import os

st.set_page_config(page_title="News Research Tool", layout="wide")
st.title("🗞️ News Research Tool")
st.sidebar.title("🔗 Load News Articles")

# Collect up to 3 URLs from sidebar inputs
urls = [st.sidebar.text_input(f"URL {i+1}") for i in range(3)]
urls = [url.strip() for url in urls if url.strip()]

# Upload text file with URLs (one URL per line)
uploaded_file = st.sidebar.file_uploader("📄 Upload .txt file with URLs", type="txt")
if uploaded_file:
    try:
        file_urls = uploaded_file.read().decode().splitlines()
        urls.extend([u.strip() for u in file_urls if u.strip()])
        urls = list(set(urls))  # Deduplicate
        st.sidebar.success(f"Loaded {len(file_urls)} URLs from file.")
    except Exception as e:
        st.sidebar.error(f"Failed to read uploaded file: {e}")

process_btn = st.sidebar.button("🔍 Process Articles")
clear_cache = st.sidebar.button("🧹 Clear Cache")

# Clear cache button functionality
if clear_cache:
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)
        st.sidebar.success("✅ Cache cleared.")
    else:
        st.sidebar.info("ℹ️ No cache found to clear.")

# Process articles button functionality
if process_btn:
    if not urls:
        st.sidebar.warning("⚠️ Please enter at least one URL.")
        st.stop()

    try:
        with st.spinner("🔄 Loading and processing articles..."):
            vectorstore, raw_docs = process_urls(urls)
            save_cache((vectorstore, raw_docs))
        st.sidebar.success("✅ Articles processed and cached.")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to process articles: {e}")
        st.stop()

# Query input and handling
query = st.text_input("❓ Ask a question or say 'summarise all' / 'summarise 1st and 2nd'...")

if query:
    if not cache_exists():
        st.warning("⚠️ Please process articles first.")
        st.stop()

    vectorstore, raw_docs = load_cache()

    # Determine if user asked for summary or question
    if "summarise" in query.lower():
        docs_to_use = parse_summarize_query(query, raw_docs)
        if not docs_to_use:
            st.warning("⚠️ Could not find articles matching your summary request.")
            st.stop()
    else:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
        docs_to_use = retriever.get_relevant_documents(query)

    prompt = create_prompt(query, docs_to_use)
    try:
        with st.spinner("🤖 Generating response from Gemini LLM..."):
            response = generate_response(prompt)
        st.header("📌 Answer")
        st.markdown(response)

        st.subheader("🔗 Sources")
        sources = [doc.metadata.get("source", "") for doc in docs_to_use]
        for src in set(filter(None, sources)):
            st.markdown(f"- [{src}]({src})")
    except Exception as e:
        st.error(f"❌ API error: {e}")
