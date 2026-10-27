import argparse
import pandas as pd
import json
import os
import glob
import sys
from orchestration.backtester import Backtester
from utils.metrics import calculate_metrics
from utils.visualizer import plot_performance, plot_mas_ohlcv
from utils.benchmark_strategies import run_buy_and_hold, run_sma_crossover, run_macd_signal


def generate_benchmark_and_plots(ticker: str, start_date: str, end_date: str, initial_capital: float,
                                dates: list, mas_nav: list, out_dir: str):
    """
    Menghitung strategi benchmark (Buy & Hold, SMA, MACD),
    menyimpan master NAV gabungan, dan menggambar grafik garis performa.
    """
    clean_ticker = ticker.replace('.', '_')
    df_master = pd.DataFrame({
        "Date": dates,
        "MAS_NAV": mas_nav
    })

    ohlcv_path = os.path.join("data", "cache", ticker, "master_ohlcv.csv")
    if os.path.exists(ohlcv_path):
        try:
            from stockstats import wrap
            df_ohlcv = pd.read_csv(ohlcv_path)
            df_ohlcv['date'] = pd.to_datetime(df_ohlcv['date'])

            stock = wrap(df_ohlcv.copy())
            _ = stock['macd']
            _ = stock['macds']
            _ = stock['close_20_sma']
            _ = stock['close_50_sma']

            df_ohlcv_with_indicators = pd.DataFrame(stock).reset_index()
            df_ohlcv_with_indicators = df_ohlcv_with_indicators.rename(columns={
                'close_20_sma': 'sma_20',
                'close_50_sma': 'sma_50'
            })

            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            mask = (df_ohlcv_with_indicators['date'] >= start_dt) & (df_ohlcv_with_indicators['date'] <= end_dt)
            df_filtered = df_ohlcv_with_indicators[mask].copy()

            df_bh = run_buy_and_hold(df_filtered, initial_capital=initial_capital)
            df_sma = run_sma_crossover(df_filtered, initial_capital=initial_capital)
            df_macd = run_macd_signal(df_filtered, initial_capital=initial_capital)

            df_master['BH_NAV'] = df_bh['portfolio_value'].values
            df_master['SMA_NAV'] = df_sma['portfolio_value'].values
            df_master['MACD_NAV'] = df_macd['portfolio_value'].values
        except Exception as e:
            print(f"[WARN] Gagal menghitung benchmark teknikal: {e}")

    # Simpan NAV Master
    master_csv_path = os.path.join(out_dir, f"NAV_Master_{clean_ticker}.csv")
    df_master.to_csv(master_csv_path, index=False)
    print(f"Saved master NAV to {master_csv_path}")

    # Gambar grafik perbandingan garis
    plot_line_path = os.path.join(out_dir, f"Plot_LineChart_{clean_ticker}.png")
    
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.figure(figsize=(14, 7))
    plt.plot(df_master['Date'], df_master['MAS_NAV'], label='Multi-Agent System (MAS)', color='blue', linewidth=2.5)

    if 'BH_NAV' in df_master.columns:
        plt.plot(df_master['Date'], df_master['BH_NAV'], label='Buy & Hold', color='gray', linestyle='--', linewidth=1.5)
    if 'SMA_NAV' in df_master.columns:
        plt.plot(df_master['Date'], df_master['SMA_NAV'], label='SMA Crossover', color='green', linestyle='--', linewidth=1.5)
    if 'MACD_NAV' in df_master.columns:
        plt.plot(df_master['Date'], df_master['MACD_NAV'], label='MACD Signal', color='purple', linestyle='--', linewidth=1.5)

    plt.title(f"Trading Performance: Multi-Agent System vs Benchmarks ({ticker})", fontsize=14, fontweight='bold')
    plt.xlabel("Date")
    plt.ylabel("Net Asset Value (IDR)")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)

    if len(dates) > 10:
        plt.xticks(range(0, len(dates), len(dates)//10), rotation=45)
    else:
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(plot_line_path, dpi=300)
    plt.close()
    print(f"Saved performance chart to {plot_line_path}")


def run_backtest(args):
    """
    Mode BACKTEST: Menjalankan simulasi Multi-Agent System (MAS),
    menyimpan log teks, CSV transaksi, CSV NAV, dan langsung membuat
    grafik performa (Line Chart) serta visualisasi eksekusi (Candlestick).
    """
    clean_ticker = args.ticker.replace('.', '_')
    folder_name = f"result_{clean_ticker}_{args.start}_{args.end}"
    out_dir = os.path.join("results", folder_name)
    os.makedirs(out_dir, exist_ok=True)
    
    # Redirect print outputs to a log file
    log_path = os.path.join(out_dir, f"log_{clean_ticker}.txt")
    original_stdout = sys.stdout
    
    log_file = open(log_path, 'w', encoding='utf-8')
    sys.stdout = log_file

    try:
        print("==================================================")
        print("  MULTI-AGENT SYSTEM (MAS) TRADING BACKTESTER")
        print("==================================================")
        print(f"Ticker: {args.ticker}")
        print(f"Period: {args.start} to {args.end}")
        print(f"Initial Capital: Rp {args.capital:,.2f}")
        print(f"Architecture: {args.agents} Agents")
        print("==================================================")

        # 1. Initialize and run Backtester
        backtester = Backtester(
            ticker=args.ticker,
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital,
            architecture=args.agents
        )

        results = backtester.run()

        # 2. Extract results
        dates = results["dates"]
        mas_nav = results["mas_nav"]
        bh_nav = results["bh_nav"]
        trades = results["trades"]

        # 3. Calculate and Print Metrics
        mas_metrics = calculate_metrics(mas_nav, trades, risk_free_rate_annual=0.06)
        bh_metrics = calculate_metrics(bh_nav, [], risk_free_rate_annual=0.06)

        print("\n==================================================")
        print("                BACKTEST RESULTS                  ")
        print("==================================================")
        print(f"{'Metric':<20} | {'MAS Portfolio':<15} | {'Buy & Hold':<15}")
        print("-" * 55)
        print(f"{'Final NAV (Rp)':<20} | {mas_nav[-1]:>15,.0f} | {bh_nav[-1]:>15,.0f}")
        print(f"{'Cumulative Return':<20} | {mas_metrics['Cumulative Return']*100:>14.2f}% | {bh_metrics['Cumulative Return']*100:>14.2f}%")
        print(f"{'Sharpe Ratio':<20} | {mas_metrics['Sharpe Ratio']:>15.2f} | {bh_metrics['Sharpe Ratio']:>15.2f}")
        print(f"{'Max Drawdown':<20} | {mas_metrics['Max Drawdown']*100:>14.2f}% | {bh_metrics['Max Drawdown']*100:>14.2f}%")
        print(f"{'Win Rate':<20} | {mas_metrics['Win Rate']*100:>14.2f}% | {'N/A':>15}")
        print("==================================================")

    finally:
        sys.stdout = original_stdout
        log_file.close()
        
    print(f"\n[INFO] Simulasi selesai. Log perdebatan AI tersimpan di: {log_path}")

    # 4. Save Trades to CSV
    csv_trades_path = os.path.join(out_dir, f"trades_{clean_ticker}.csv")
    if trades:
        df_trades = pd.DataFrame(trades)
        df_trades.to_csv(csv_trades_path, index=False)
        print(f"Saved trade logs to {csv_trades_path}")
    else:
        # Jika tidak ada transaksi, simpan format kosong agar visualizer tidak error
        pd.DataFrame(columns=["date", "action", "price", "shares", "cost"]).to_csv(csv_trades_path, index=False)
        print(f"No trades executed. Created empty trade log at {csv_trades_path}")

    # 5. Save Daily NAV & Generate Comparison Line Chart
    generate_benchmark_and_plots(
        ticker=args.ticker,
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.capital,
        dates=dates,
        mas_nav=mas_nav,
        out_dir=out_dir
    )

    # 6. Generate Candlestick Visualization with Trade Markers
    ohlcv_path = os.path.join("data", "cache", args.ticker, "master_ohlcv.csv")
    if os.path.exists(ohlcv_path):
        candlestick_path = os.path.join(out_dir, f"Candlestick_{clean_ticker}.png")
        try:
            plot_mas_ohlcv(
                ohlcv_path=ohlcv_path,
                trades_csv_path=csv_trades_path,
                ticker=args.ticker,
                output_path=candlestick_path
            )
            print(f"Saved candlestick chart to {candlestick_path}")
        except Exception as e:
            print(f"[WARN] Gagal membuat grafik candlestick: {e}")
    else:
        print(f"[WARN] File master_ohlcv.csv tidak ditemukan di cache untuk membuat candlestick.")

    print(f"\n[SUKSES] Seluruh proses selesai! Semua hasil tersimpan di folder: {out_dir}")


def run_plot(args):
    """
    Mode PLOT: Digunakan jika ingin me-render ulang grafik candlestick tanpa simulasi ulang.
    """
    clean_ticker = args.ticker.replace('.', '_')
    folder_name = f"result_{clean_ticker}_{args.start}_{args.end}"
    out_dir = os.path.join("results", folder_name)
    trades_csv = args.trades_csv or os.path.join(out_dir, f"trades_{clean_ticker}.csv")

    if not os.path.exists(trades_csv):
        print(f"Error: File trades tidak ditemukan: {trades_csv}")
        return

    ohlcv_path = os.path.join("data", "cache", args.ticker, "master_ohlcv.csv")
    if not os.path.exists(ohlcv_path):
        print("Error: File OHLCV tidak ditemukan.")
        return

    output_path = os.path.join(out_dir, f"Candlestick_{clean_ticker}.png")
    plot_mas_ohlcv(
        ohlcv_path=ohlcv_path,
        trades_csv_path=trades_csv,
        ticker=args.ticker,
        output_path=output_path
    )
    print(f"Berhasil membuat candlestick: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Trading Backtester")
    parser.add_argument("--mode", type=str, choices=["backtest", "plot"], default="backtest",
                        help="Mode operasi: 'backtest' (default) atau 'plot' (render ulang candlestick)")
    parser.add_argument("--ticker", type=str, default="BBCA.JK", help="Stock ticker (e.g., BBCA.JK)")
    parser.add_argument("--start", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-01-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100_000_000.0, help="Initial capital in IDR")
    parser.add_argument("--trades-csv", type=str, default=None,
                        help="Path ke file trades CSV (opsional, untuk --mode plot)")
    parser.add_argument("--agents", type=int, choices=[1, 8, 12], default=12,
                        help="Jumlah agen untuk simulasi MAS (default 12 agen)")

    args = parser.parse_args()

    if args.mode == "backtest":
        run_backtest(args)
    elif args.mode == "plot":
        run_plot(args)


if __name__ == "__main__":
    main()
