import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from tools.cache_manager import CacheManager
from tools.data_fetcher import YFinanceFetcher
from tools.indicator_calculator import TechnicalIndicatorCalculator
from tools.news_fetcher import NewsFetcher

def run_smoke_test():
    print("Starting Data Pipeline Smoke Test...")
    
    # Initialize tools
    cache_manager = CacheManager(base_dir="data/cache")
    data_fetcher = YFinanceFetcher(cache_manager)
    indicator_calc = TechnicalIndicatorCalculator(cache_manager)
    news_fetcher = NewsFetcher(cache_manager)
    
    tickers = ["BBCA.JK", "BBRI.JK", "BMRI.JK"]
    end_date = "2024-01-31" # Smoke test date
    
    for ticker in tickers:
        print(f"\n{'='*40}")
        print(f"Testing pipeline for {ticker} up to {end_date}")
        print(f"{'='*40}")
        
        # 1. Fetch OHLCV
        print("\n1. Fetching OHLCV data...")
        df_ohlcv = data_fetcher.fetch_ohlcv(ticker, end_date)
        if not df_ohlcv.empty:
            print(f"Successfully fetched {len(df_ohlcv)} days of historical data.")
            print(f"Latest data:\n{df_ohlcv.tail(2)}")
            
        # 2. Fetch Fundamentals
        print("\n2. Fetching Fundamental data...")
        fundamentals = data_fetcher.fetch_fundamentals(ticker, end_date)
        if fundamentals and "info" in fundamentals:
            print(f"Successfully fetched fundamentals. P/E: {fundamentals['info'].get('trailingPE')}")
            
        # 3. Calculate Indicators
        print("\n3. Calculating Technical Indicators...")
        indicators = indicator_calc.calculate_indicators(ticker, end_date)
        if indicators:
            print(f"Successfully calculated indicators for {indicators.get('date')}:")
            print(f"Close: {indicators.get('close')}")
            print(f"MACD: {indicators.get('macd'):.4f}")
            print(f"RSI: {indicators.get('rsi_14'):.4f}")
            print(f"SMA_50: {indicators.get('sma_50'):.4f}")
            
        # 4. Fetch News
        print("\n4. Fetching News...")
        news = news_fetcher.fetch_all_news(ticker, end_date)
        if news:
            print(f"Successfully fetched {len(news)} news articles.")
            print("Latest 3 articles:")
            for i, article in enumerate(news[:3]):
                print(f"  {i+1}. [{article['source']}] {article['title']} ({article['published']})")

    print("\nSmoke test completed. Check data/cache directory for output files.")

if __name__ == "__main__":
    run_smoke_test()
