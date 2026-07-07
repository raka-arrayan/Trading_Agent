import pandas as pd
from stockstats import wrap

class TechnicalIndicatorCalculator:
    """
    Calculates technical indicators using the stockstats library based on cached OHLCV data.
    """
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
        
    def calculate_indicators(self, ticker: str, date_str: str) -> dict:
        """
        Reads OHLCV from cache, calculates indicators,
        returns the latest indicators for the target date, and saves to cache.
        """
        print(f"Calculating technical indicators for {ticker} up to {date_str}...")
        # Load OHLCV data from cache
        df = self.cache_manager.load_csv(ticker, date_str, "ohlcv.csv", parse_dates=['date'], index_col='date')
        if df is None or df.empty:
            print(f"Warning: No OHLCV data in cache for {ticker} on {date_str}")
            return {}
            
        # stockstats modifies the dataframe in-place, so we wrap it
        stock = wrap(df)
        
        # Trigger calculation of standard indicators used by TradingAgents/baseline
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
            print(f"Warning: No data available on or before {date_str} for {ticker}")
            return {}
            
        latest_date = available_dates[-1]
        latest_row = stock.loc[latest_date]
        
        # Clean up any potential NaN values and convert to native python float
        def safe_float(val):
            import math
            if pd.isna(val) or math.isnan(val):
                return None
            return float(val)
            
        indicators = {
            "date": latest_date.strftime("%Y-%m-%d"),
            "close": safe_float(latest_row.get('close')),
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
        
        # Save calculated indicators to cache
        self.cache_manager.save_json(ticker, date_str, "indicators.json", indicators)
        
        return indicators
