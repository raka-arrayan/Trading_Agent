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

    # Kata kunci tidak relevan yang sering muncul pada artikel edukasi, promosi, atau insiden non-finansial
    IRRELEVANT_KEYWORDS = [
        "cara beli", "cara investasi", "panduan pemula", "tips pemula", 
        "belajar saham", "cara daftar", "panduan lengkap", "reksadana pemula",
        "cara membuka rekening", "pinjaman online", "pinjol", "promo diskon",
        "perampokan", "pembobolan atm", "gelapkan dana", "teller bank bawa kabur"
    ]

    def is_valid_headline(self, title: str) -> bool:
        """Menyaring judul berita untuk membuang berita sampah/clickbait."""
        if not title or len(title.strip()) < 10:
            return False
        title_lower = title.lower()
        for bad_word in self.IRRELEVANT_KEYWORDS:
            if bad_word in title_lower:
                return False
        return True

    def fetch_all_news(self, ticker: str) -> List[Dict]:
        """
        Fetches news related to the ticker and general market news.
        Appends new valid items incrementally to existing master_news.json.
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
        
        # Gabungkan semua berita baru yang ditarik
        all_new_news = gn_news + macro_query_items if 'macro_query_items' in locals() else gn_news + macro_news + cnbc_news
        
        # Muat berita lama jika sudah ada di cache lokal (agar arsip lama aman)
        existing_news = []
        if self.cache_manager.master_file_exists(ticker, "master_news.json"):
            existing_news = self.cache_manager.load_master_json(ticker, "master_news.json") or []

        # Gabungkan arsip lama dan berita baru, lakukan filter dan deduplikasi
        seen_titles = set()
        merged_news = []
        
        # Prioritaskan arsip lama yang sudah bersih
        for item in existing_news:
            if self.is_valid_headline(item.get('title', '')):
                if item['title'] not in seen_titles:
                    seen_titles.add(item['title'])
                    merged_news.append(item)
                    
        # Tambahkan berita baru yang lolos filter
        added_count = 0
        for item in all_new_news:
            if self.is_valid_headline(item.get('title', '')):
                if item['title'] not in seen_titles:
                    seen_titles.add(item['title'])
                    merged_news.append(item)
                    added_count += 1
                    
        print(f"  [Filter] {added_count} berita baru ditambahkan. Total koleksi bersih: {len(merged_news)} berita.")
        
        # Simpan kembali ke master_news.json di cache
        self.cache_manager.save_master_json(ticker, "master_news.json", merged_news)
        
        return merged_news
