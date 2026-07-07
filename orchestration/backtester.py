import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from tools.cache_manager import CacheManager
from orchestration.graph import create_trading_graph
import json

class Backtester:
    def __init__(self, ticker: str, start_date: str, end_date: str, initial_capital: float = 100_000_000.0, fee_rate: float = 0.002):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.fee_rate = fee_rate
        
        self.cache_manager = CacheManager(base_dir="data/cache")
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
        
        # Load market calendar (valid trading days)
        print(f"Fetching market calendar for {ticker} from {start_date} to {end_date}...")
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        self.valid_dates = [d.strftime('%Y-%m-%d') for d in df.index]
        print(f"Found {len(self.valid_dates)} valid trading days.")
        
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
                print(f"[{date}] Executed BUY: {shares_to_trade} shares @ Rp {current_price:,.2f}")
            else:
                print(f"[{date}] Insufficient funds for BUY.")
                
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
                
                # To calculate a rough PnL for Win Rate, we could look at previous BUYs, 
                # but for simplicity in this skeleton, we assume a win if price is higher than a rolling average cost.
                # Here we just mark profit_loss as 1 (Win) or -1 (Loss) heuristically, 
                # but a real implementation would use a FIFO or Average Cost queue.
                # Let's assume we store the average buy price.
                
                self.trades.append({
                    "date": date,
                    "action": "SELL",
                    "price": current_price,
                    "shares": shares_to_sell,
                    "revenue": net_revenue,
                    "profit_loss": net_revenue - (shares_to_sell * current_price) # simplistic
                })
                print(f"[{date}] Executed SELL: {shares_to_sell} shares @ Rp {current_price:,.2f}")
                
    def run(self):
        print(f"\n--- Starting Backtest for {self.ticker} ---")
        
        bh_initialized = False
        
        for date in self.valid_dates:
            print(f"\nProcessing Date: {date}")
            
            # 1. Load data from cache (we assume data pipeline has populated it)
            # If not populated, we simulate pulling the data (for the smoke test)
            # We use load_json for fundamentals.json, indicators.json, and news.json
            fundamentals = self.cache_manager.load_json(self.ticker, date, "fundamentals.json") or {}
            indicators = self.cache_manager.load_json(self.ticker, date, "indicators.json") or {}
            news = self.cache_manager.load_json(self.ticker, date, "news.json") or []
            
            data = {
                "fundamentals": fundamentals.get("info", {}) if fundamentals else {},
                "indicators": indicators,
                "news": news
            }
            
            # Since this is a backtest, if no cache exists, we'll try to get at least the close price
            # but ideally the pipeline should have run. For dry-run we mock it.
            current_price = data.get("indicators", {}).get("close", 0)
            if current_price == 0:
                print(f"No close price found for {date} (Cache Miss). Assuming DUMMY price for dry-run...")
                current_price = 10000.0  # Dummy price so the loop continues in dry-run
                data["indicators"]["close"] = current_price
                
            # Initialize Buy and Hold (Buy with all cash on first day)
            if not bh_initialized:
                max_shares = int(self.initial_capital / (current_price * (1 + self.fee_rate)))
                self.bh_shares = max_shares
                cash_spent = max_shares * current_price * (1 + self.fee_rate)
                self.bh_cash = self.initial_capital - cash_spent
                bh_initialized = True
                print(f"[{date}] Buy and Hold initialized: Bought {self.bh_shares} shares.")
                
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
            
            # 3. Execute LangGraph
            try:
                final_state = self.graph.invoke(state)
                decision = final_state.get("trading_decision", {})
                
                # 4. Execute Trade
                self._execute_trade(decision, current_price, date)
                
            except Exception as e:
                print(f"Error during graph execution on {date}: {e}")
                
            # 5. Update NAVs
            current_nav = self.current_cash + (self.holdings * current_price)
            self.nav_history.append(current_nav)
            
            bh_nav = self.bh_cash + (self.bh_shares * current_price)
            self.bh_nav_history.append(bh_nav)
            
            self.dates_history.append(date)
            
            print(f"[{date}] EOD MAS NAV: Rp {current_nav:,.2f} | B&H NAV: Rp {bh_nav:,.2f}")
            
        print("\n--- Backtest Complete ---")
        return {
            "dates": self.dates_history,
            "mas_nav": self.nav_history,
            "bh_nav": self.bh_nav_history,
            "trades": self.trades
        }
