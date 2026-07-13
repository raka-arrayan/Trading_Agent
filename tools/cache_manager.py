import os
import json
import shutil
import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any, List

class CacheManager:
    """
    Manages local caching of data at the ticker level (centralized).
    
    Data is stored as master files in data/cache/{ticker}/ format:
        - master_ohlcv.csv
        - master_fundamentals.json
        - master_news.json
    
    No per-date subfolders are created. All slicing is done in-memory
    by the backtester at runtime to prevent look-ahead bias.
    """
    
    def __init__(self, base_dir: str = "data/cache"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_ticker_dir(self, ticker: str) -> Path:
        """Returns the ticker-level cache directory (e.g., data/cache/BBCA.JK/)."""
        safe_ticker = ticker.replace('^', '')
        ticker_dir = self.base_dir / safe_ticker
        ticker_dir.mkdir(parents=True, exist_ok=True)
        return ticker_dir

    # --- Master CSV ---

    def save_master_csv(self, ticker: str, filename: str, df: pd.DataFrame):
        """Saves a DataFrame as a master CSV at the ticker level."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        df.to_csv(filepath)
        print(f"  [Cache] Saved master CSV: {filepath} ({len(df)} rows)")

    def load_master_csv(self, ticker: str, filename: str, parse_dates=None, index_col=None) -> Union[pd.DataFrame, None]:
        """Loads a master CSV from the ticker level if it exists, otherwise returns None."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        
        if filepath.exists():
            return pd.read_csv(filepath, parse_dates=parse_dates, index_col=index_col)
        return None

    # --- Master JSON ---

    def save_master_json(self, ticker: str, filename: str, data: Union[Dict, List]):
        """Saves a dictionary or list as a master JSON file at the ticker level."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"  [Cache] Saved master JSON: {filepath}")

    def load_master_json(self, ticker: str, filename: str) -> Union[Dict, List, None]:
        """Loads a master JSON file if it exists, otherwise returns None."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def master_file_exists(self, ticker: str, filename: str) -> bool:
        """Checks if a master file exists for the given ticker."""
        ticker_dir = self._get_ticker_dir(ticker)
        filepath = ticker_dir / filename
        return filepath.exists()

    # --- Cleanup ---

    def cleanup_legacy_folders(self, ticker: str):
        """
        Removes all per-date subfolders and non-master files left over from
        the old architecture inside data/cache/{ticker}/.
        
        Keeps only files matching the master_* naming convention.
        """
        ticker_dir = self._get_ticker_dir(ticker)
        removed_dirs = 0
        removed_files = 0

        for item in sorted(ticker_dir.iterdir()):
            if item.is_dir():
                # Remove any subfolder (e.g., 2024-01-02/, 2024-01-03/)
                shutil.rmtree(item)
                removed_dirs += 1
            elif item.is_file() and not item.name.startswith("master_"):
                # Remove non-master files (e.g., old ohlcv_master.csv)
                item.unlink()
                removed_files += 1

        if removed_dirs > 0 or removed_files > 0:
            print(f"  [Cleanup] {ticker}: Removed {removed_dirs} legacy folder(s) "
                  f"and {removed_files} non-master file(s).")
        else:
            print(f"  [Cleanup] {ticker}: Cache directory already clean.")
