import pandas as pd
from stockstats import wrap
import math

class TechnicalIndicatorCalculator:
    """
    Calculates technical indicators using the stockstats library.
    
    Operates purely in-memory: receives a DataFrame directly (already sliced
    up to the target date by the backtester) and returns a dict of indicators.
    No file I/O is performed.
    """

    def calculate_indicators(self, df: pd.DataFrame, date_str: str) -> dict:
        """
        Calculates technical indicators from the given OHLCV DataFrame.
        
        Args:
            df: OHLCV DataFrame (already sliced up to date_str to prevent look-ahead bias).
                Must have columns: open, high, low, close, volume. Index must be DatetimeIndex.
            date_str: The target date string (YYYY-MM-DD) to extract indicators for.
            
        Returns:
            Dict of indicator values for the target date, or empty dict if insufficient data.
        """
        if df is None or df.empty:
            print(f"  Warning: Empty DataFrame for indicator calculation on {date_str}")
            return {}
            
        # stockstats modifies the dataframe in-place, so we wrap a copy
        stock = wrap(df.copy())
        
        # Trigger calculation of standard indicators used by TradingAgents
        # Stockstats calculates them lazily when accessed
        _ = stock['macd']
        _ = stock['macds']
        _ = stock['macdh']
        _ = stock['rsi_14']
        _ = stock['boll']
        _ = stock['boll_ub']
        _ = stock['boll_lb']
        _ = stock['kdjk']
        _ = stock['kdjd']
        _ = stock['kdjj']
        _ = stock['close_20_sma']
        _ = stock['close_50_sma']
        
        # Extract the values for the target date
        # Since date_str might be a weekend/holiday, we find the latest available date <= date_str
        target_dt = pd.to_datetime(date_str)
        available_dates = df.index[df.index <= target_dt]
        
        if len(available_dates) == 0:
            print(f"  Warning: No data available on or before {date_str}")
            return {}
            
        latest_date = available_dates[-1]
        latest_row = stock.loc[latest_date]
        
        # Clean up any potential NaN values and convert to native python float
        def safe_float(val):
            if pd.isna(val) or (isinstance(val, float) and math.isnan(val)):
                return None
            return float(val)
            
        indicators = {
            "date": latest_date.strftime("%Y-%m-%d"),
            "close": safe_float(latest_row.get('close')),
            "open": safe_float(latest_row.get('open')),
            "high": safe_float(latest_row.get('high')),
            "low": safe_float(latest_row.get('low')),
            "volume": safe_float(latest_row.get('volume')),
            "macd": safe_float(latest_row.get('macd')),
            "macds": safe_float(latest_row.get('macds')),
            "macdh": safe_float(latest_row.get('macdh')),
            "rsi_14": safe_float(latest_row.get('rsi_14')),
            "boll": safe_float(latest_row.get('boll')),
            "boll_ub": safe_float(latest_row.get('boll_ub')),
            "boll_lb": safe_float(latest_row.get('boll_lb')),
            "kdjk": safe_float(latest_row.get('kdjk')),
            "kdjd": safe_float(latest_row.get('kdjd')),
            "kdjj": safe_float(latest_row.get('kdjj')),
            "sma_20": safe_float(latest_row.get('close_20_sma')),
            "sma_50": safe_float(latest_row.get('close_50_sma')),
        }
        
        return indicators
