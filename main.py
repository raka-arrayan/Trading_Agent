import argparse
import pandas as pd
import json
import os
import glob
from orchestration.backtester import Backtester
from utils.metrics import calculate_metrics
from utils.visualizer import plot_performance, plot_mas_ohlcv


def run_backtest(args):
    """
    Mode BACKTEST: Menjalankan seluruh logika Multi-Agent System (MAS),
    melakukan simulasi trading, menghasilkan log, dan menyimpan data CSV
    (transaksi & NAV) ke folder results/.
    """
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


def run_plot(args):
    """
    Mode PLOT: Tidak menjalankan simulasi MAS yang berat. Hanya membaca
    file CSV dari hasil backtest sebelumnya di folder results/ dan data
    OHLCV dari cache, lalu menghasilkan grafik candlestick komprehensif
    dengan penanda keputusan BUY/SELL dari Multi-Agent System.
    """
    print("==================================================")
    print("  MAS TRADING VISUALIZER (Candlestick + MAS Decisions)")
    print("==================================================")
    print(f"Ticker: {args.ticker}")
    print("==================================================")

    # --- Tentukan path file trades CSV ---
    trades_csv = args.trades_csv
    if trades_csv is None:
        # Auto-detect: cari file trades terbaru di folder results/ berdasarkan ticker
        ticker_safe = args.ticker.replace('.', '_')
        pattern = f"results/trades_{ticker_safe}_*.csv"
        candidates = sorted(glob.glob(pattern))
        if not candidates:
            print(f"Error: Tidak ditemukan file trades untuk ticker '{args.ticker}' di folder results/.")
            print(f"  Pastikan Anda sudah menjalankan --mode backtest terlebih dahulu.")
            print(f"  Atau tentukan path secara eksplisit: --trades-csv <path>")
            return
        trades_csv = candidates[-1]  # Ambil file terbaru (urutan alfabet terakhir)
        print(f"  Auto-detected trades CSV: {trades_csv}")

    if not os.path.exists(trades_csv):
        print(f"Error: File tidak ditemukan: {trades_csv}")
        return

    # --- Tentukan path file OHLCV ---
    ohlcv_path = os.path.join("data", "cache", args.ticker, "master_ohlcv.csv")
    if not os.path.exists(ohlcv_path):
        print(f"Error: File OHLCV tidak ditemukan: {ohlcv_path}")
        print(f"  Pastikan data cache tersedia untuk ticker '{args.ticker}'.")
        return

    print(f"  OHLCV data : {ohlcv_path}")
    print(f"  Trades log : {trades_csv}")
    print("--------------------------------------------------")

    # --- Tentukan path output grafik ---
    # Ambil nama file trades untuk membuat nama output yang konsisten
    trades_basename = os.path.splitext(os.path.basename(trades_csv))[0]
    output_suffix = trades_basename.replace("trades_", "")
    output_path = f"results/candlestick_{output_suffix}.png"

    # --- Panggil fungsi visualisasi candlestick ---
    plot_mas_ohlcv(
        ohlcv_path=ohlcv_path,
        trades_csv_path=trades_csv,
        ticker=args.ticker,
        output_path=output_path
    )


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Trading Backtester")
    parser.add_argument("--mode", type=str, choices=["backtest", "plot"], default="backtest",
                        help="Mode operasi: 'backtest' menjalankan simulasi MAS penuh, "
                             "'plot' hanya menghasilkan grafik candlestick dari hasil backtest sebelumnya")
    parser.add_argument("--ticker", type=str, default="BBCA.JK", help="Stock ticker (e.g., BBCA.JK)")
    parser.add_argument("--start", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-01-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100_000_000.0, help="Initial capital in IDR")
    parser.add_argument("--trades-csv", type=str, default=None,
                        help="Path ke file trades CSV (untuk --mode plot). "
                             "Jika tidak ditentukan, akan otomatis mencari di folder results/")
    parser.add_argument("--nav-csv", type=str, default=None,
                        help="Path ke file NAV CSV (untuk --mode plot, opsional)")

    args = parser.parse_args()

    if args.mode == "backtest":
        run_backtest(args)
    elif args.mode == "plot":
        run_plot(args)


if __name__ == "__main__":
    main()
