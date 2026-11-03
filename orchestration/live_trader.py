import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from tools.cache_manager import CacheManager
from tools.data_fetcher import YFinanceFetcher
from tools.indicator_calculator import TechnicalIndicatorCalculator
from tools.news_fetcher import NewsFetcher
from orchestration.graph import create_trading_graph
from tabulate import tabulate


class LiveTrader:
    """
    LiveTrader Engine for real-time / on-demand decision making.
    Runs the 12-agent consensus on current market data and news today without backtest looping.
    """
    def __init__(self, ticker: str, capital: float = 100_000_000.0, fee_rate: float = 0.002):
        self.ticker = ticker
        self.capital = capital
        self.fee_rate = fee_rate
        self.cache_manager = CacheManager(base_dir="data/cache")
        self.data_fetcher = YFinanceFetcher(self.cache_manager)
        self.indicator_calc = TechnicalIndicatorCalculator()
        self.news_fetcher = NewsFetcher(self.cache_manager)
        self.graph = create_trading_graph()

    def run_live(self) -> dict:
        today_str = datetime.now().strftime("%Y-%m-%d")
        print("=" * 70)
        print(f"  MULTI-AGENT SYSTEM (MAS) - LIVE DECISION SESSION")
        print(f"  Ticker       : {self.ticker}")
        print(f"  Date         : {today_str}")
        print(f"  Cash Capital : Rp {self.capital:,.2f}")
        print("=" * 70)

        # 1. Fetch latest OHLCV
        # 2 years buffer to ensure technical indicators (SMA-50, etc) are accurate
        start_buffer = (datetime.now() - timedelta(days=365 * 2)).strftime("%Y-%m-%d")
        print("\n[1/4] Mengambil dan memperbarui data OHLCV...")
        df_ohlcv = self.data_fetcher.fetch_ohlcv(self.ticker, start_buffer, today_str)
        
        if df_ohlcv is None or df_ohlcv.empty:
            raise RuntimeError(f"Gagal mengambil data harga untuk {self.ticker}")

        # Ensure index is DatetimeIndex
        if not isinstance(df_ohlcv.index, pd.DatetimeIndex):
            df_ohlcv['date'] = pd.to_datetime(df_ohlcv['date'])
            df_ohlcv.set_index('date', inplace=True)

        # 2. Compute Technical Indicators for Today
        print("\n[2/4] Menghitung indikator teknikal real-time...")
        indicators = self.indicator_calc.calculate_indicators(df_ohlcv, today_str)
        current_price = indicators.get("close", 0.0)
        if current_price == 0.0:
            # Fallback to last row close
            current_price = float(df_ohlcv['close'].iloc[-1])
            indicators['close'] = current_price

        # 3. Fetch Latest Fundamentals & News
        print("\n[3/4] Mengambil data fundamental dan umpan berita 7 hari terakhir...")
        fundamentals = self.data_fetcher.fetch_fundamentals(self.ticker)
        all_news = self.news_fetcher.fetch_all_news(self.ticker)
        
        # Slice news within 7-day lookback window up to today
        seven_days_ago = datetime.now() - timedelta(days=7)
        sliced_news = []
        for item in all_news:
            pub_str = item.get("published", "")
            try:
                art_dt = pd.to_datetime(pub_str, errors='coerce')
                if art_dt is not None and not pd.isna(art_dt):
                    art_dt = art_dt.tz_localize(None) if art_dt.tzinfo else art_dt
                    if seven_days_ago <= art_dt <= datetime.now():
                        sliced_news.append(item)
            except Exception:
                continue

        if not sliced_news:
            # Fallback to last 10 articles if date parsing fails
            sliced_news = all_news[:10]

        print(f"  -> Total berita valid untuk analisis live: {len(sliced_news)} artikel.")
        print(f"  -> Harga pasar saat ini: Rp {current_price:,.2f}")

        # 4. Prepare State for 12 Agents
        state = {
            "ticker": self.ticker,
            "date": today_str,
            "market_data": {
                "fundamentals": fundamentals.get("info", {}) if fundamentals else {},
                "indicators": indicators,
                "news": sliced_news
            },
            "analyst_reports": {},
            "research_debate": [],
            "research_consensus": "",
            "risk_reports": {},
            "risk_debate": [],
            "risk_consensus": "",
            "portfolio_status": {
                "current_cash": self.capital,
                "holdings": 0
            },
            "trading_decision": {}
        }

        # 5. Invoke 12-Agent Graph
        print("\n[4/4] Memulai sidang dan musyawarah 12 Agen (LangGraph)...")
        final_state = self.graph.invoke(state)
        decision = final_state.get("trading_decision", {})

        return {
            "date": today_str,
            "ticker": self.ticker,
            "current_price": current_price,
            "capital": self.capital,
            "indicators": indicators,
            "final_state": final_state,
            "decision": decision
        }
