# MARKET-INSIGHT  
**An Interactive Framework for News Summarization and User-Driven Query Resolution**

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Problem Statement](#problem-statement)  
- [Approach](#approach)  
- [System Architecture](#system-architecture)  
- [Features](#features)  
- [Setup and Installation](#setup-and-installation)  
- [Usage](#usage)  
- [Future Work](#future-work)  
- [Contributing](#contributing)  
- [License](#license)

---

## Project Overview

MARKET-INSIGHT is an AI-powered research assistant designed to analyze, summarize, and answer questions on financial news articles. In an age of information overload, this tool helps investors, analysts, researchers, and students quickly extract actionable insights from large volumes of news content — enabling more informed financial decisions.

---

## Problem Statement

The financial industry generates an overwhelming amount of news daily. Manually reading, filtering, and summarizing these articles is time-consuming and error-prone, often leading to missed critical insights. Existing tools lack integrated summarization and targeted Q&A tailored specifically for financial news.

---

## Approach

MARKET-INSIGHT combines multiple state-of-the-art Natural Language Processing (NLP) techniques:

- **Document Loading:** Users input article URLs or upload text files containing URLs.  
- **Text Splitting:** Articles are chunked into manageable pieces for better processing.  
- **Embeddings & Indexing:** Each chunk is converted into vector embeddings using HuggingFace models and indexed with FAISS for fast similarity search.  
- **Question Answering & Summarization:** Google’s Gemini LLM is leveraged to provide detailed answers or article summaries based on retrieved relevant chunks.  
- **Interactive Interface:** Streamlit UI enables easy input, processing, querying, and visualization of results.

---

## System Architecture

User Inputs (URLs / Uploads)
↓
Document Loader (UnstructuredURLLoader)
↓
Text Splitter (RecursiveCharacterTextSplitter)
↓
Embeddings Generation (HuggingFace Embeddings)
↓
Vector Indexing (FAISS)
↓
Query Input → Retriever (FAISS) → Relevant Chunks
↓
Prompt Construction for LLM (Google Gemini)
↓
LLM Response → Answer or Summary Display


---

## Features

- Input multiple URLs directly or via batch upload (.txt file).  
- Automatic fetching and chunking of article content.  
- Embedding generation and efficient vector indexing with FAISS.  
- Supports asking specific questions related to the articles.  
- Provides detailed summaries of single or multiple articles on request.  
- Displays source links for verification and deeper exploration.  
- Cache mechanism to save and reuse processed data for speed and cost efficiency.  
- Clear cache option to refresh data as needed.  
- Friendly and responsive Streamlit UI with informative status messages.

---

## Setup and Installation

### Prerequisites

- Python 3.8+  
- Google Gemini API key (required)  

### Virtual Environment (Recommended)

To keep your project dependencies isolated and avoid conflicts with other Python projects or system packages, it is highly recommended to use a **virtual environment**. This ensures a clean and manageable development setup.

#### Steps to create and activate a virtual environment:

- On **Windows** (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- On **Windows** (Command Prompt):
```bash
python -m venv .venv
.\.venv\Scripts\activate.bat
```
- On **Linux/macOS** (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Installation Steps

1. Clone the repository:  
```bash
git clone https://github.com/yourusername/market-insight.git
cd market-insight 
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory with your API keys:
```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Usage
```bash
Run the Streamlit app:

bash
Copy
Edit
streamlit run app.py
How to Use
Step 1: Enter financial news article URLs in the sidebar (up to 3) or upload a .txt file with URLs.

Step 2: Click “Process Articles” to fetch, chunk, embed, and index the articles.

Step 3: Ask a question in the input box or request summaries by typing:

summarise all to summarize all loaded articles

summarise 1st or summarise 1st and 2nd to summarize specific articles

Any specific query related to the content to get targeted answers.

Step 4: View answers/summaries along with clickable source links.
```

### Future Work
Enhanced Source Tracking: Better citation and in-text referencing of source documents.

Multi-modal Support: Integrate other media types such as podcasts or videos.

Custom Knowledge Integration: Allow user-uploaded PDFs or documents as knowledge base.

Realtime News Feed: Auto-fetch and update latest financial news articles periodically.

Improved Summarization: Add options for executive summaries, bullet points, and tone customization.

Frontend Enhancements: Develop React or Next.js frontend for improved UX and scalability.

Advanced Analytics: Add trend analysis, sentiment scoring, and predictive insights based on news data.

### Contributing
Contributions are welcome! Feel free to open issues or submit pull requests with improvements.

### License
This project is licensed under the MIT License - see the LICENSE file for details.