import streamlit as st
from src.analyzer import NewsAgent

# Configure page settings
st.set_page_config(page_title="Pro AI News Analyst", layout="wide")

def render_analysis(article_data, agent):
    """Helper to render the UI for a single article result."""
    with st.expander(f"{article_data.get('title', 'Unknown Title')}", expanded=True):
        st.caption(f"Source: {article_data.get('url')}")
        
        if not article_data.get('success'):
            st.error(f"Failed to load: {article_data.get('error')}")
            return

        with st.spinner("AI Analyst is reading..."):
            analysis = agent.analyze_content(article_data.get('text'))
            st.markdown(analysis)

def main():
    # Header
    st.title("Enterprise AI News Agent")
    st.markdown("""
    **Automated Intelligence for the Modern Age.** Scrape single URLs, batch process lists, or crawl entire news feeds autonomously.
    """)
    
    st.divider()

    # Initialize Backend
    try:
        agent = NewsAgent()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()

    # Layout: Tabs for different modes
    tab1, tab2, tab3 = st.tabs(["Single Analysis", "Batch Processing", "Autonomous Crawler"])

    # --- TAB 1: Single URL ---
    with tab1:
        st.subheader("Deep Dive Analysis")
        url = st.text_input("Paste Article URL:", placeholder="https://techcrunch.com/...")
        
        if st.button("Analyze Article", key="btn_single"):
            if url:
                data = agent.fetch_article(url)
                render_analysis(data, agent)
            else:
                st.warning("Please enter a URL.")

    # --- TAB 2: Batch Processing ---
    with tab2:
        st.subheader("Bulk Intelligence")
        urls_input = st.text_area("Paste URLs (one per line):", height=150)
        
        if st.button("Process All", key="btn_batch"):
            urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
            
            if urls:
                progress_bar = st.progress(0)
                for i, u in enumerate(urls):
                    data = agent.fetch_article(u)
                    render_analysis(data, agent)
                    progress_bar.progress((i + 1) / len(urls))
                st.success("Batch processing complete.")
            else:
                st.warning("No URLs provided.")

    # --- TAB 3: Crawler ---
    with tab3:
        st.subheader("Live Feed Monitor")
        col1, col2 = st.columns([3, 1])
        with col1:
            domain = st.text_input("News Domain:", placeholder="https://bbc.com")
        with col2:
            limit = st.number_input("Max Articles:", 1, 10, 3)
            
        if st.button("Crawl & Analyze", key="btn_crawl"):
            if domain:
                with st.spinner(f"Crawling {domain} for top stories..."):
                    articles = agent.fetch_feed(domain, limit)
                
                if not articles:
                    st.warning("No articles found (or site blocked scraping).")
                else:
                    st.success(f"Found {len(articles)} articles.")
                    for art in articles:
                        render_analysis(art, agent)

if __name__ == "__main__":
    main()