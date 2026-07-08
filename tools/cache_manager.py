import os
import json
import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any, List

class CacheManager:
    """
    Manages local caching of data to prevent look-ahead bias during backtesting.
    Data is stored in data/cache/{ticker}/{date}/ format.
    """
    
    def __init__(self, base_dir: str = "data/cache"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_cache_dir(self, ticker: str, date_str: str) -> Path:
        """Returns the specific cache directory for a ticker and date."""
        # Sanitize ticker (e.g. ^JKSE to JKSE)
        safe_ticker = ticker.replace('^', '')
        cache_dir = self.base_dir / safe_ticker / date_str
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def save_json(self, ticker: str, date_str: str, filename: str, data: Union[Dict, List]):
        """Saves a dictionary or list as a JSON file."""
        cache_dir = self._get_cache_dir(ticker, date_str)
        filepath = cache_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    def load_json(self, ticker: str, date_str: str, filename: str) -> Union[Dict, List, None]:
        """Loads a JSON file if it exists, otherwise returns None."""
        cache_dir = self._get_cache_dir(ticker, date_str)
        filepath = cache_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_csv(self, ticker: str, date_str: str, filename: str, df: pd.DataFrame):
        """Saves a pandas DataFrame as a CSV file."""
        cache_dir = self._get_cache_dir(ticker, date_str)
        filepath = cache_dir / filename
        df.to_csv(filepath)
        
    def load_csv(self, ticker: str, date_str: str, filename: str, parse_dates=None, index_col=None) -> Union[pd.DataFrame, None]:
        """Loads a CSV file into a pandas DataFrame if it exists, otherwise returns None."""
        cache_dir = self._get_cache_dir(ticker, date_str)
        filepath = cache_dir / filename
        
        if filepath.exists():
            return pd.read_csv(filepath, parse_dates=parse_dates, index_col=index_col)
        return None

    # --- Master CSV methods (ticker-level, no per-date duplication) ---

    def _get_ticker_dir(self, ticker: str) -> Path:
        """Returns the ticker-level cache directory (e.g., data/cache/BBCA.JK/)."""
        safe_ticker = ticker.replace('^', '')
        ticker_dir = self.base_dir / safe_ticker
        ticker_dir.mkdir(parents=True, exist_ok=True)
        return ticker_dir

    def save_master_csv(self, ticker: str, filename: str, df: pd.DataFrame):
        """Saves a DataFrame as a master CSV at the ticker level."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        df.to_csv(filepath)
        print(f"Saved master CSV: {filepath}")

    def load_master_csv(self, ticker: str, filename: str, parse_dates=None, index_col=None) -> Union[pd.DataFrame, None]:
        """Loads a master CSV from the ticker level if it exists, otherwise returns None."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        
        if filepath.exists():
            return pd.read_csv(filepath, parse_dates=parse_dates, index_col=index_col)
        return None
