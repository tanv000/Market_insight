import re
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def parse_summarize_query(query, raw_docs):
    """
    Determines which documents to summarize based on query.
    Supports keywords like 'all', 'first', '2nd', etc.
    Returns a list of docs.
    """
    lower_query = query.lower()
    if "all" in lower_query:
        return raw_docs

    position_map = {
        "first": 0, "1st": 0,
        "second": 1, "2nd": 1,
        "third": 2, "3rd": 2,
        "fourth": 3, "4th": 3
    }

    indices = []
    for word, idx in position_map.items():
        if word in lower_query:
            indices.append(idx)

    indices += [int(x) - 1 for x in re.findall(r"article\s*(\d+)", lower_query)]
    indices += [int(x) - 1 for x in re.findall(r"\b(\d+)[a-z]{0,2}\b", lower_query)]

    # Remove duplicates and filter out of range
    indices = sorted(set(i for i in indices if 0 <= i < len(raw_docs)))

    if not indices:
        return []

    return [raw_docs[i] for i in indices]

def create_prompt(query, docs_to_use):
    combined_text = ""
    for i, doc in enumerate(docs_to_use):
        src = doc.metadata.get("source", f"Article {i+1}")
        combined_text += f"\n\n### Source: {src}\n{doc.page_content.strip()}"

    prompt = f"""
You are a skilled research analyst who helps users understand and interpret news articles.

=== USER REQUEST ===
{query}

=== RELEVANT ARTICLES ===
{combined_text}

=== TASK ===
If the user requested a **summary**, generate a detailed and relevant summary of the selected article(s) that:
- Covers all the important points thoroughly.
- Uses multiple paragraphs for clarity.
- Includes bullet points to highlight key facts or insights.
- Mentions different perspectives or nuances if available.
- Is not too short; provide enough detail to fully inform the reader.

If the user asked a **specific question**, provide an accurate, well-supported, and detailed answer based on the content above.

Always aim to help the user make informed decisions and gain deep insights from the news.

=== FINAL RESPONSE ===
"""
    return prompt

def generate_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
