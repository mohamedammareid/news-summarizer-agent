import os
import newspaper
from newspaper import Article
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Union

# Load environment variables
load_dotenv()

class NewsAgent:
    """
    A professional News Intelligence Agent tailored for scraping, 
    crawling, and analyzing news content using OpenAI's GPT models.
    """

    def __init__(self):
        """Initialize the NewsAgent with OpenAI client configuration."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API Key is missing. Please check your .env file.")
        
        self.client = OpenAI(api_key=api_key)

    def fetch_article(self, url: str) -> Dict[str, Union[str, bool]]:
        """
        Fetches and parses a single news article from a URL.
        
        Args:
            url (str): The direct link to the article.
            
        Returns:
            dict: Contains title, authors, text, and metadata.
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                "success": True,
                "title": article.title,
                "authors": article.authors,
                "publish_date": str(article.publish_date),
                "text": article.text,
                "url": url
            }
        except Exception as e:
            return {"success": False, "error": str(e), "url": url}

    def fetch_feed(self, site_url: str, limit: int = 3) -> List[Dict]:
        """
        Crawls a news website homepage to find trending articles.
        
        Args:
            site_url (str): The homepage URL (e.g., https://cnn.com).
            limit (int): Maximum number of articles to process.
            
        Returns:
            list: A list of article dictionaries.
        """
        try:
            # memoize_articles=False forces a fresh scrape every time
            paper = newspaper.build(site_url, memoize_articles=False)
            
            articles_data = []
            count = 0
            
            for article in paper.articles:
                if count >= limit:
                    break
                
                try:
                    article.download()
                    article.parse()
                    
                    # Filter: Ignore short or empty articles
                    if len(article.text) > 500:
                        articles_data.append({
                            "success": True,
                            "title": article.title,
                            "authors": article.authors,
                            "text": article.text,
                            "url": article.url
                        })
                        count += 1
                except Exception:
                    continue # Skip failed articles gracefully
            
            return articles_data

        except Exception as e:
            return [{"success": False, "error": f"Crawling failed: {str(e)}"}]

    def analyze_content(self, text: str) -> str:
        """
        Uses OpenAI GPT-4o to generate an executive summary and sentiment analysis.
        
        Args:
            text (str): The raw article text.
            
        Returns:
            str: Markdown formatted analysis.
        """
        if not text:
            return "Error: No text provided for analysis."

        try:
            system_instruction = (
                "You are an elite News Analyst. "
                "Your goal is to provide objective, structured intelligence briefings."
            )
            
            # Context-aware prompting
            user_prompt = f"""
            Analyze the following news text:
            "{text[:3500]}" 

            Output ONLY the following Markdown structure:
            
            ### Executive Summary
            (A concise, high-level overview of the event in 3 sentences).

            ### Key Takeaways
            - (Bullet point 1)
            - (Bullet point 2)
            - (Bullet point 3)

            ### Sentiment & Bias
            **Sentiment:** (Positive / Negative / Neutral)
            **Tone:** (Professional / Sensationalist / Opinionated)
            """

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"AI Analysis Error: {str(e)}"