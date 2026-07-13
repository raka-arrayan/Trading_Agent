import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import re
from tools.cache_manager import CacheManager
from tools.data_fetcher import YFinanceFetcher
from tools.indicator_calculator import TechnicalIndicatorCalculator
from tools.news_fetcher import NewsFetcher
from orchestration.graph import create_trading_graph

class Backtester:
    def __init__(self, ticker: str, start_date: str, end_date: str, initial_capital: float = 100_000_000.0, fee_rate: float = 0.002):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.fee_rate = fee_rate
        
        self.cache_manager = CacheManager(base_dir="data/cache")
        self.data_fetcher = YFinanceFetcher(self.cache_manager)
        self.indicator_calc = TechnicalIndicatorCalculator()
        self.news_fetcher = NewsFetcher(self.cache_manager)
        self.graph = create_trading_graph()
        
        # State tracking
        self.current_cash = initial_capital
        self.holdings = 0  # In shares
        self.nav_history = []
        self.dates_history = []
        self.trades = []
        
        # Baseline tracking (Buy and Hold)
        self.bh_shares = 0
        self.bh_nav_history = []

        # In-memory master data (loaded by _prepare_data)
        self.master_ohlcv = None         # pd.DataFrame
        self.master_fundamentals = {}    # dict
        self.master_news = []            # list
        self.valid_dates = []            # list of str, populated in _prepare_data

    def _prepare_data(self):
        """
        Data preparation pipeline -- runs ONCE before the backtest loop.
        
        Loads all data into memory from master files (or downloads if not cached):
        1. master_ohlcv.csv   -> self.master_ohlcv (DataFrame)
        2. master_fundamentals.json -> self.master_fundamentals (dict)
        3. master_news.json   -> self.master_news (list)
        
        No per-date folders are created. All slicing is done in-memory at runtime.
        """
        print(f"\n{'='*60}")
        print(f"  PREPARING DATA PIPELINE for {self.ticker}")
        print(f"{'='*60}")

        # --- Step 0: Cleanup legacy per-date folders ---
        self.cache_manager.cleanup_legacy_folders(self.ticker)

        # --- Step 1: Master OHLCV ---
        if self.cache_manager.master_file_exists(self.ticker, "master_ohlcv.csv"):
            print("  [OHLCV] Loading from cached master_ohlcv.csv ...")
            self.master_ohlcv = self.cache_manager.load_master_csv(
                self.ticker, "master_ohlcv.csv",
                parse_dates=['date'], index_col='date'
            )
            
            # Check if cached data covers the requested end date
            end_dt = pd.to_datetime(self.end_date)
            max_cached_date = self.master_ohlcv.index.max()
            
            if max_cached_date < end_dt:
                print(f"  [OHLCV] Cached data only covers up to {max_cached_date.strftime('%Y-%m-%d')}.")
                print(f"  [OHLCV] Requested end date is {self.end_date}. Re-downloading new master data...")
                self.master_ohlcv = self.data_fetcher.fetch_ohlcv(
                    self.ticker, self.start_date, self.end_date
                )
            else:
                print(f"  [OHLCV] Loaded {len(self.master_ohlcv)} rows from cache (sufficient date range).")
        else:
            self.master_ohlcv = self.data_fetcher.fetch_ohlcv(
                self.ticker, self.start_date, self.end_date
            )
            
        if self.master_ohlcv is None or self.master_ohlcv.empty:
            print("  CRITICAL: Failed to download OHLCV data. Cannot proceed.")
            return

        # --- Step 2: Master Fundamentals ---
        if self.cache_manager.master_file_exists(self.ticker, "master_fundamentals.json"):
            print("  [Fundamentals] Loading from cached master_fundamentals.json ...")
            self.master_fundamentals = self.cache_manager.load_master_json(
                self.ticker, "master_fundamentals.json"
            ) or {}
        else:
            self.master_fundamentals = self.data_fetcher.fetch_fundamentals(self.ticker)

        # --- Step 3: Master News ---
        if self.cache_manager.master_file_exists(self.ticker, "master_news.json"):
            print("  [News] Loading from cached master_news.json ...")
            self.master_news = self.cache_manager.load_master_json(
                self.ticker, "master_news.json"
            ) or []
        else:
            try:
                self.master_news = self.news_fetcher.fetch_all_news(self.ticker)
            except Exception as e:
                print(f"  Warning: News fetch failed ({e}). Continuing without news.")
                self.master_news = []

        print(f"\n  Data pipeline summary:")
        print(f"    OHLCV rows    : {len(self.master_ohlcv)}")
        print(f"    Fundamentals  : {'Loaded' if self.master_fundamentals else 'Empty'}")
        print(f"    News articles : {len(self.master_news)}")
        
        # Determine valid trading dates from the loaded master OHLCV
        start_dt = pd.to_datetime(self.start_date)
        end_dt = pd.to_datetime(self.end_date)
        mask = (self.master_ohlcv.index >= start_dt) & (self.master_ohlcv.index <= end_dt)
        self.valid_dates = [d.strftime('%Y-%m-%d') for d in self.master_ohlcv[mask].index]
        
        print(f"    Trading dates : {len(self.valid_dates)} valid days found in range.")
        print(f"{'='*60}\n")

    def _compute_indicators_for_date(self, date_str: str) -> dict:
        """
        Slices master OHLCV up to date_str (inclusive) to prevent look-ahead bias,
        then computes technical indicators in-memory.
        """
        target_dt = pd.to_datetime(date_str)
        df_slice = self.master_ohlcv.loc[self.master_ohlcv.index <= target_dt]
        
        if df_slice.empty:
            return {}
        
        return self.indicator_calc.calculate_indicators(df_slice, date_str)

    @staticmethod
    def _extract_strategy_from_text(text: str) -> str:
        """Extract dominant BUY/SELL/HOLD from text by keyword frequency."""
        if not text:
            return "HOLD"
        upper = text.upper()
        buy_count = len(re.findall(r'\bBUY\b', upper))
        sell_count = len(re.findall(r'\bSELL\b', upper))
        hold_count = len(re.findall(r'\bHOLD\b', upper))
        
        counts = {"BUY": buy_count, "SELL": sell_count, "HOLD": hold_count}
        return max(counts, key=counts.get) if max(counts.values()) > 0 else "HOLD"

    def _print_consensus_summary(self, final_state: dict, date: str):
        """
        Prints the daily consensus summary block in a strictly sequential, academic format.
        Part A: Narrative Summary
        Part B: Tabular Consensus
        """
        from tabulate import tabulate
        
        analyst_reports = final_state.get("analyst_reports", {})
        trading_decision = final_state.get("trading_decision", {})
        research_debate = final_state.get("research_debate", [])
        research_consensus = final_state.get("research_consensus", "")
        risk_debate = final_state.get("risk_debate", [])
        risk_consensus = final_state.get("risk_consensus", "")
        portfolio_status = final_state.get("portfolio_status", {})
        pm_rec = portfolio_status.get("recommendation", "")
        
        def clean_text(text):
            if not text: return "(kosong)"
            return text.replace('\n', ' ').strip()
            
        print(f"\n============================================================")
        print(f"  ANALISIS HARIAN: {date}")
        print(f"============================================================")
        
        table_data = []
        
        def print_agent(name, text, strategy_override=None, confidence="-"):
            if not text: return
            strategy = strategy_override or self._extract_strategy_from_text(text)
            conclusion = clean_text(text)
            print(f"\n[{name}]")
            print(f"Kesimpulan: {conclusion}")
            print(f"Strategi: {strategy}")
            table_data.append([name, strategy, confidence])
            
        # 1. Analysts (Strict order)
        analyst_order = ["fundamental", "macro", "sentiment", "technical"]
        for key in analyst_order:
            if key in analyst_reports:
                print_agent(f"{key.capitalize()} Analyst", analyst_reports[key])
                
        # 2. Researchers
        for debate in research_debate:
            agent = debate.get("agent", "")
            strategy = "BUY" if agent == "Bullish" else "SELL" if agent == "Bearish" else None
            print_agent(f"{agent} Researcher", debate.get("message", ""), strategy)
            
        if research_consensus:
            print_agent("Research Facilitator", research_consensus)
            
        # 3. Risk Management
        for debate in risk_debate:
            agent = debate.get("agent", "")
            print_agent(f"{agent} Analyst", debate.get("message", ""))
            
        if risk_consensus:
            print_agent("Risk Facilitator", risk_consensus)
            
        # 4. Portfolio Manager
        if pm_rec:
            print_agent("Portfolio Manager", pm_rec)
            
        # 5. Trading Agent (Final Decision)
        if trading_decision:
            action = trading_decision.get("action", "HOLD")
            qty = trading_decision.get("quantity", 0)
            conf = trading_decision.get("confidence", 0.0)
            name = "Trading Agent"
            print(f"\n[{name}]")
            print(f"Kesimpulan: Eksekusi {action} {qty} lot.")
            print(f"Strategi: {action}")
            table_data.append([name, action, conf])
            
        print("\n" + tabulate(table_data, headers=["Nama Agen", "Strategi", "Keyakinan"], tablefmt="grid"))
        print("\n")

    def _execute_trade(self, decision: dict, current_price: float, date: str):
        action = decision.get("action", "HOLD")
        quantity = decision.get("quantity", 0)  # assumed in lots
        
        shares_to_trade = quantity * 100  # 1 lot = 100 shares in Indonesia
        
        if action == "BUY" and shares_to_trade > 0:
            cost = shares_to_trade * current_price
            fee = cost * self.fee_rate
            total_cost = cost + fee
            
            if self.current_cash >= total_cost:
                self.current_cash -= total_cost
                self.holdings += shares_to_trade
                self.trades.append({
                    "date": date,
                    "action": "BUY",
                    "price": current_price,
                    "shares": shares_to_trade,
                    "cost": total_cost
                })
                print(f"  [{date}] Executed BUY: {shares_to_trade} shares @ Rp {current_price:,.2f}")
            else:
                print(f"  [{date}] Insufficient funds for BUY.")
                
        elif action == "SELL" and shares_to_trade > 0:
            # We can only sell what we have
            shares_to_sell = min(shares_to_trade, self.holdings)
            if shares_to_sell > 0:
                revenue = shares_to_sell * current_price
                fee = revenue * self.fee_rate
                net_revenue = revenue - fee
                
                # Simple average cost logic could be added here for profit_loss
                # For now, we'll just track raw revenue to cash
                self.current_cash += net_revenue
                self.holdings -= shares_to_sell
                
                self.trades.append({
                    "date": date,
                    "action": "SELL",
                    "price": current_price,
                    "shares": shares_to_sell,
                    "revenue": net_revenue,
                    "profit_loss": net_revenue - (shares_to_sell * current_price)
                })
                print(f"  [{date}] Executed SELL: {shares_to_sell} shares @ Rp {current_price:,.2f}")
                
    def run(self):
        print(f"\n--- Starting Backtest for {self.ticker} ---")

        # Run data pipeline ONCE -- load all master data into memory
        self._prepare_data()
        
        if self.master_ohlcv is None or self.master_ohlcv.empty:
            print("ERROR: No OHLCV data available. Aborting backtest.")
            return {"dates": [], "mas_nav": [], "bh_nav": [], "trades": []}
        
        bh_initialized = False
        
        for date in self.valid_dates:
            print(f"\n{'='*60}")
            print(f"  Processing Date: {date}")
            print(f"{'='*60}")
            
            # 1. Compute indicators in-memory (sliced up to this date, no look-ahead)
            indicators = self._compute_indicators_for_date(date)
            
            # Build data dict for the graph
            data = {
                "fundamentals": self.master_fundamentals.get("info", {}) if self.master_fundamentals else {},
                "indicators": indicators,
                "news": self.master_news
            }
            
            # Get close price from indicators
            current_price = indicators.get("close", 0)
            if current_price == 0 or current_price is None:
                print(f"  WARNING: No close price for {date}. Skipping.")
                continue
                
            # Initialize Buy and Hold (Buy with all cash on first day)
            if not bh_initialized:
                max_shares = int(self.initial_capital / (current_price * (1 + self.fee_rate)))
                self.bh_shares = max_shares
                cash_spent = max_shares * current_price * (1 + self.fee_rate)
                self.bh_cash = self.initial_capital - cash_spent
                bh_initialized = True
                print(f"  [{date}] Buy & Hold initialized: {self.bh_shares} shares @ Rp {current_price:,.2f}")
                
            # 2. Prepare TradingState
            state = {
                "ticker": self.ticker,
                "date": date,
                "market_data": data,
                "analyst_reports": {},
                "research_debate": [],
                "research_consensus": "",
                "risk_reports": {},
                "risk_debate": [],
                "risk_consensus": "",
                "portfolio_status": {
                    "current_cash": self.current_cash,
                    "holdings": self.holdings
                },
                "trading_decision": {}
            }
            
            # 3. Execute LangGraph (all agents)
            try:
                final_state = self.graph.invoke(state)
                decision = final_state.get("trading_decision", {})
                
                # 4. Print consensus summary (Explainable AI)
                self._print_consensus_summary(final_state, date)
                
                # 5. Execute Trade
                self._execute_trade(decision, current_price, date)
                
            except Exception as e:
                print(f"  Error during graph execution on {date}: {e}")
                
            # 6. Update NAVs
            current_nav = self.current_cash + (self.holdings * current_price)
            self.nav_history.append(current_nav)
            
            bh_nav = self.bh_cash + (self.bh_shares * current_price)
            self.bh_nav_history.append(bh_nav)
            
            self.dates_history.append(date)
            
            print(f"  [{date}] EOD MAS NAV: Rp {current_nav:,.2f} | B&H NAV: Rp {bh_nav:,.2f}")
            
        print("\n--- Backtest Complete ---")
        return {
            "dates": self.dates_history,
            "mas_nav": self.nav_history,
            "bh_nav": self.bh_nav_history,
            "trades": self.trades
        }
