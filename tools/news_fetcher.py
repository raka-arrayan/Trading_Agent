import feedparser
import urllib.parse
from typing import List, Dict

class NewsFetcher:
    """
    Fetches financial news from Indonesian RSS feeds.
    Saves as master_news.json at the ticker level via CacheManager.
    """
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
        
    def fetch_google_news(self, query: str) -> List[Dict]:
        """Fetches news from Google News RSS using the given query."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"
        
        feed = feedparser.parse(url)
        news_list = []
        for entry in feed.entries:
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "source": entry.get("source", {}).get("title", "Google News") if isinstance(entry.get("source"), dict) else "Google News"
            })
        return news_list
        
    def fetch_cnbc_indonesia(self) -> List[Dict]:
        """Fetches from CNBC Indonesia Market RSS."""
        url = "https://www.cnbcindonesia.com/market/rss"
        feed = feedparser.parse(url)
        news_list = []
        for entry in feed.entries:
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "source": "CNBC Indonesia"
            })
        return news_list

    def fetch_all_news(self, ticker: str) -> List[Dict]:
        """
        Fetches news related to the ticker and general market news.
        Saves as master_news.json at the ticker level.
        
        Note: RSS feeds typically only provide recent news. For historical backtesting, 
        this would normally read from a pre-scraped historical database.
        For the pipeline foundation, we fetch live RSS and save it to the cache.
        """
        print(f"  [Fetch] Downloading news for {ticker}...")
        
        # 1. Google News specific to ticker
        ticker_base = ticker.replace('.JK', '')
        query = f"{ticker_base} saham"
        gn_news = self.fetch_google_news(query)
        
        # 2. General banking / macro news from Google News
        macro_query = "suku bunga Bank Indonesia OJK"
        macro_news = self.fetch_google_news(macro_query)
        
        # 3. Market news from CNBC Indonesia
        cnbc_news = self.fetch_cnbc_indonesia()
        
        # Combine all
        all_news = gn_news + macro_news + cnbc_news if 'cnbc_news' in locals() else gn_news + macro_news
        
        # Deduplicate by title
        seen_titles = set()
        unique_news = []
        for n in all_news:
            if n['title'] not in seen_titles:
                seen_titles.add(n['title'])
                unique_news.append(n)
                
        # Save as master JSON at ticker level
        self.cache_manager.save_master_json(ticker, "master_news.json", unique_news)
        
        return unique_news
