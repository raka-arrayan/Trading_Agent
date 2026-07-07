import argparse
import pandas as pd
import json
import os
from orchestration.backtester import Backtester
from utils.metrics import calculate_metrics
from utils.visualizer import plot_performance

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Trading Backtester")
    parser.add_argument("--ticker", type=str, default="BBCA.JK", help="Stock ticker (e.g., BBCA.JK)")
    parser.add_argument("--start", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-01-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100_000_000.0, help="Initial capital in IDR")
    
    args = parser.parse_args()
    
    print("==================================================")
    print("  MULTI-AGENT SYSTEM (MAS) TRADING BACKTESTER")
    print("==================================================")
    print(f"Ticker: {args.ticker}")
    print(f"Period: {args.start} to {args.end}")
    print(f"Initial Capital: Rp {args.capital:,.2f}")
    print("==================================================")
    
    # 1. Initialize and run Backtester
    backtester = Backtester(
        ticker=args.ticker,
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.capital
    )
    
    results = backtester.run()
    
    # 2. Extract results
    dates = results["dates"]
    mas_nav = results["mas_nav"]
    bh_nav = results["bh_nav"]
    trades = results["trades"]
    
    if not dates:
        print("Error: No trading dates processed. Check data cache.")
        return
        
    # 3. Calculate Metrics
    print("\nCalculating Performance Metrics...")
    metrics = calculate_metrics(mas_nav, trades, risk_free_rate_annual=0.06)
    
    # Calculate Buy and Hold Metrics for comparison
    bh_metrics = calculate_metrics(bh_nav, [], risk_free_rate_annual=0.06)
    
    print("\n==================================================")
    print("                BACKTEST RESULTS                  ")
    print("==================================================")
    print(f"{'Metric':<20} | {'MAS Portfolio':<15} | {'Buy & Hold':<15}")
    print("-" * 55)
    print(f"{'Final NAV (Rp)':<20} | {mas_nav[-1]:>15,.0f} | {bh_nav[-1]:>15,.0f}")
    print(f"{'Cumulative Return':<20} | {metrics['Cumulative Return']*100:>14.2f}% | {bh_metrics['Cumulative Return']*100:>14.2f}%")
    print(f"{'Sharpe Ratio':<20} | {metrics['Sharpe Ratio']:>15.2f} | {bh_metrics['Sharpe Ratio']:>15.2f}")
    print(f"{'Max Drawdown':<20} | {metrics['Max Drawdown']*100:>14.2f}% | {bh_metrics['Max Drawdown']*100:>14.2f}%")
    print(f"{'Win Rate':<20} | {metrics['Win Rate']*100:>14.2f}% | {'N/A':>15}")
    print("==================================================")
    
    # 4. Save Logs and Visualizations
    os.makedirs("results", exist_ok=True)
    
    # Save trades to CSV
    if trades:
        df_trades = pd.DataFrame(trades)
        csv_path = f"results/trades_{args.ticker.replace('.', '_')}_{args.start}_{args.end}.csv"
        df_trades.to_csv(csv_path, index=False)
        print(f"\nSaved trade logs to {csv_path}")
        
    # Save daily NAV to CSV
    df_nav = pd.DataFrame({
        "Date": dates,
        "MAS_NAV": mas_nav,
        "BH_NAV": bh_nav
    })
    nav_path = f"results/nav_{args.ticker.replace('.', '_')}_{args.start}_{args.end}.csv"
    df_nav.to_csv(nav_path, index=False)
    print(f"Saved daily NAV to {nav_path}")
    
    # Generate Plot
    plot_path = f"results/plot_{args.ticker.replace('.', '_')}_{args.start}_{args.end}.png"
    plot_performance(dates, mas_nav, bh_nav, args.ticker, output_path=plot_path)

if __name__ == "__main__":
    main()
