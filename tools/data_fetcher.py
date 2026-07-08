import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any

class YFinanceFetcher:
    """
    Fetches market data and fundamentals from Yahoo Finance and caches it.
    """
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
        
    def fetch_ohlcv(self, ticker: str, end_date: str, start_date: str = None) -> pd.DataFrame:
        """
        Fetches OHLCV data up to end_date. 
        If start_date is not provided, fetches 2 years of history to ensure enough data for indicators.
        Saves to cache.
        """
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            # Default to 2 years before end_date for indicators like 200-SMA
            start_dt = end_dt - timedelta(days=365*2)
            
        # yfinance download expects end date to be exclusive, so we add 1 day
        yf_end_dt = end_dt + timedelta(days=1)
        
        # Download data
        print(f"Fetching OHLCV for {ticker} from {start_dt.strftime('%Y-%m-%d')} to {end_date}...")
        df = yf.download(ticker, start=start_dt.strftime("%Y-%m-%d"), end=yf_end_dt.strftime("%Y-%m-%d"), progress=False)
        
        if df.empty:
            print(f"Warning: No OHLCV data found for {ticker} between {start_date} and {end_date}")
            return df
            
        # yfinance >= 0.2.33 returns multi-index columns for single tickers if auto_adjust is false or other cases
        # Flatten if necessary to match standard stockstats format (lowercase columns: open, close, high, low, volume)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Convert columns to lowercase for stockstats compatibility
        df.columns = [col.lower() for col in df.columns]
        
        # Ensure index is named 'date'
        df.index.name = 'date'
            
        # Save to cache
        self.cache_manager.save_csv(ticker, end_date, "ohlcv.csv", df)
        
        return df

    def fetch_ohlcv_master(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Downloads OHLCV data once for the full backtest range (with 2-year lookback
        for indicator calculation) and saves it as a single master CSV at the 
        ticker level: data/cache/{ticker}/ohlcv_master.csv
        
        The backtester slices from this master at runtime to avoid look-ahead bias.
        
        Returns the full DataFrame.
        """
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        # 2-year lookback so indicators (e.g., 200-SMA) have enough history
        lookback_start_dt = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=365 * 2)
        # yfinance end is exclusive
        yf_end_dt = end_dt + timedelta(days=1)

        print(f"[Master Fetch] Downloading OHLCV for {ticker} "
              f"from {lookback_start_dt.strftime('%Y-%m-%d')} to {end_date} ...")
        
        df = yf.download(
            ticker,
            start=lookback_start_dt.strftime("%Y-%m-%d"),
            end=yf_end_dt.strftime("%Y-%m-%d"),
            progress=False
        )
        
        if df.empty:
            print(f"WARNING: yfinance returned NO data for {ticker}. "
                  f"Check your internet connection or ticker symbol.")
            return df

        # Flatten multi-index columns (yfinance >= 0.2.33 quirk)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Lowercase columns for stockstats compatibility
        df.columns = [col.lower() for col in df.columns]
        df.index.name = 'date'

        # Remove duplicate column names (yfinance sometimes returns dupes)
        df = df.loc[:, ~df.columns.duplicated()]

        # Save as master CSV at ticker level
        self.cache_manager.save_master_csv(ticker, "ohlcv_master.csv", df)
        
        print(f"[Master Fetch] Saved {len(df)} rows for {ticker}.")
        return df

    def fetch_fundamentals(self, ticker: str, end_date: str) -> Dict[str, Any]:
        """
        Fetches basic fundamentals (P/E, Market Cap) and financial statements.
        Saves to cache as JSON. Note: For accurate point-in-time fundamentals, 
        yfinance has limitations as it only provides current info and latest statements.
        """
        print(f"Fetching fundamentals for {ticker}...")
        stock = yf.Ticker(ticker)
        
        info = {}
        try:
            info = stock.info
        except Exception as e:
            print(f"Warning: Failed to fetch info for {ticker}: {e}")
            
        fundamentals = {
            "info": {
                "marketCap": info.get("marketCap"),
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "priceToBook": info.get("priceToBook"),
                "dividendYield": info.get("dividendYield"),
                "sector": info.get("sector"),
                "industry": info.get("industry")
            }
        }
        
        # Helper to convert DataFrame to dict with string keys for JSON serialization
        def df_to_dict(df):
            if df is None or df.empty: return None
            # Convert timestamp columns to strings
            df_str = df.copy()
            df_str.columns = [c.strftime('%Y-%m-%d') if isinstance(c, pd.Timestamp) else str(c) for c in df_str.columns]
            return df_str.to_dict()

        try:
            fundamentals["income_statement"] = df_to_dict(stock.income_stmt)
        except Exception:
            pass
            
        try:
            fundamentals["balance_sheet"] = df_to_dict(stock.balance_sheet)
        except Exception:
            pass
            
        # Save to cache
        self.cache_manager.save_json(ticker, end_date, "fundamentals.json", fundamentals)
        
        return fundamentals
