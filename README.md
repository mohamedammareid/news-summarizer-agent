# Enterprise AI News Intelligence Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

**An autonomous news aggregation and analysis system designed to combat information overload.**

This application leverages **Generative AI** and **Web Crawling** agents to fetch, filter, and summarize news content in real-time. It transforms raw HTML into structured executive briefings, enabling users to digest complex global events in seconds.

## Core Features

### 1. Single Article Deep Dive
- Extracts clean content (text, authors, metadata) from any news URL.
- Uses **GPT-4o-mini** to generate structured executive summaries.
- Performs **Sentiment & Bias Analysis** to detect the tone of the reporting.

### 2. Bulk Batch Processing
- Accepts a list of URLs and processes them sequentially.
- Ideal for analysts researching specific topics across multiple sources.

### 3. Autonomous Site Crawler
- **Agentic Behavior:** Given a domain (e.g., `bbc.com`), the agent autonomously crawls the homepage, identifies trending stories, and generates instant reports.
- Includes logic to filter out ads and irrelevant snippets.

---

## Technical Architecture

The project follows a clean **Service-Oriented Architecture (SOA)** pattern to separate concerns:

```text
pro-news-agent/
│
├── app.py                # Presentation Layer (Streamlit UI)
├── .env                  # Configuration (API Keys)
└── src/
    ├── __init__.py       # Package definition
    └── analyzer.py       # Logic Layer (Encapsulated NewsAgent Class)
````

### Key Technologies

  - **LLM Integration:** OpenAI API for context-aware summarization.
  - **Web Scraping:** `Newspaper3k` for article extraction and parsing.
  - **Frontend:** Streamlit for rapid, interactive UI development.
  - **Error Handling:** Robust try/except blocks to manage network failures and API limits.

-----

## Installation

1.  **Clone the repo:**

    ```bash
    git clone [https://github.com/yourusername/news-agent.git](https://github.com/yourusername/news-agent.git)
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment:**
    Create a `.env` file and add your OpenAI Key:

    ```env
    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
    ```

4.  **Run the App:**

    ```bash
    streamlit run app.py
    ```


