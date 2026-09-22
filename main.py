import argparse
import pandas as pd
import json
import os
import glob
from orchestration.backtester import Backtester
from utils.metrics import calculate_metrics
from utils.visualizer import plot_performance, plot_mas_ohlcv


import sys

def run_backtest(args):
    """
    Mode BACKTEST: Menjalankan seluruh logika Multi-Agent System (MAS),
    melakukan simulasi trading, menghasilkan log, dan menyimpan data CSV
    (transaksi & NAV) ke folder results/.
    """
    folder_name = f"result_{args.ticker.replace('.', '_')}_{args.start}_{args.end}"
    out_dir = os.path.join("results", folder_name)
    os.makedirs(out_dir, exist_ok=True)
    
    # Redirect print outputs to a log file
    log_path = os.path.join(out_dir, f"log{args.agents}_{args.ticker.replace('.', '_')}.txt")
    original_stdout = sys.stdout
    
    # Buka file log dalam mode append atau write
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
        from utils.metrics import calculate_metrics
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
        # Kembalikan stdout ke terminal agar print selanjutnya muncul di layar
        sys.stdout = original_stdout
        log_file.close()
        
    print(f"\n[INFO] Simulasi selesai. Log perdebatan AI (termasuk tabel hasil) tersimpan di: {log_path}")

    # 4. Save Logs and Visualizations
    # Save trades to CSV (Hanya menyimpan milik agent saat ini)
    if trades:
        df_trades = pd.DataFrame(trades)
        csv_path = os.path.join(out_dir, f"trades_{args.agents}_{args.ticker.replace('.', '_')}.csv")
        df_trades.to_csv(csv_path, index=False)
        print(f"Saved trade logs to {csv_path}")

    # Save daily NAV to CSV (Sementara, untuk digabung nanti di compare_all)
    df_nav = pd.DataFrame({
        "Date": dates,
        f"MAS{args.agents}_NAV": mas_nav
    })
    nav_path = os.path.join(out_dir, f"nav_{args.agents}_{args.ticker.replace('.', '_')}.csv")
    df_nav.to_csv(nav_path, index=False)
    print(f"Saved daily NAV to {nav_path}")
    
    print("\n[INFO] Mode backtest selesai. Grafik tidak dibuat di mode ini.")
    print(f"[INFO] Silakan jalankan --mode compare_all jika semua agen (12, 8, 1) sudah selesai di-backtest.")


def run_compare_all(args):
    """
    Mode COMPARE_ALL:
    Menggabungkan NAV dari MAS 12, MAS 8, MAS 1 (jika ada) beserta baseline (B&H, SMA, MACD)
    ke dalam satu file NAV_Master_*.csv dan mencetak Line Chart perbandingan.
    """
    from utils.benchmark_strategies import run_buy_and_hold, run_sma_crossover, run_macd_signal
    from utils.visualizer import plot_ablation
    from tools.indicator_calculator import TechnicalIndicatorCalculator
    
    print("==================================================")
    print("  MENGGABUNGKAN SELURUH DATA & MENGGAMBAR GRAFIK (UJI ABLASI)")
    print("==================================================")
    
    folder_name = f"result_{args.ticker.replace('.', '_')}_{args.start}_{args.end}"
    out_dir = os.path.join("results", folder_name)
    
    if not os.path.exists(out_dir):
        print(f"Error: Folder {out_dir} tidak ditemukan. Silakan run backtest terlebih dahulu.")
        return

    nav_files = glob.glob(os.path.join(out_dir, f"nav_*_{args.ticker.replace('.', '_')}.csv"))
    if not nav_files:
        print("Error: Tidak ada file NAV MAS ditemukan.")
        return
        
    master_nav = pd.read_csv(nav_files[0])
    for f in nav_files[1:]:
        df_temp = pd.read_csv(f)
        master_nav = pd.merge(master_nav, df_temp, on="Date", how="outer")

    ohlcv_path = os.path.join("data", "cache", args.ticker, "master_ohlcv.csv")
    if os.path.exists(ohlcv_path):
        from stockstats import wrap
        df_ohlcv = pd.read_csv(ohlcv_path)
        df_ohlcv['date'] = pd.to_datetime(df_ohlcv['date'])
        
        # Gunakan stockstats untuk menghitung indikator teknikal ke seluruh row
        stock = wrap(df_ohlcv.copy())
        _ = stock['macd']
        _ = stock['macds']
        _ = stock['close_20_sma']
        _ = stock['close_50_sma']
        
        # Konversi kembali ke pandas DataFrame biasa untuk menghindari bug dari StockDataFrame
        df_ohlcv_with_indicators = pd.DataFrame(stock)
        df_ohlcv_with_indicators = df_ohlcv_with_indicators.reset_index()
        # Ubah nama kolom agar sesuai dengan yang diharapkan oleh benchmark
        df_ohlcv_with_indicators = df_ohlcv_with_indicators.rename(columns={
            'close_20_sma': 'sma_20',
            'close_50_sma': 'sma_50'
        })
        
        start_dt = pd.to_datetime(args.start)
        end_dt = pd.to_datetime(args.end)
        mask = (df_ohlcv_with_indicators['date'] >= start_dt) & (df_ohlcv_with_indicators['date'] <= end_dt)
        df_filtered = df_ohlcv_with_indicators[mask].copy()
        
        df_bh = run_buy_and_hold(df_filtered, initial_capital=args.capital)
        df_sma = run_sma_crossover(df_filtered, initial_capital=args.capital)
        df_macd = run_macd_signal(df_filtered, initial_capital=args.capital)
        
        master_nav['BH_NAV'] = df_bh['portfolio_value'].values
        master_nav['SMA_NAV'] = df_sma['portfolio_value'].values
        master_nav['MACD_NAV'] = df_macd['portfolio_value'].values

    master_csv_path = os.path.join(out_dir, f"NAV_Master_{args.ticker.replace('.', '_')}.csv")
    master_nav.to_csv(master_csv_path, index=False)
    print(f"Berhasil membuat tabel gabungan: {master_csv_path}")

    plot_path = os.path.join(out_dir, f"Plot_LineChart_{args.ticker.replace('.', '_')}.png")
    plot_ablation(master_nav, args.ticker, plot_path)
    print(f"Berhasil menggambar grafik perbandingan (Ablation Study): {plot_path}")


def run_plot(args):
    """
    Mode PLOT: Hanya membaca file trades milik agen spesifik (misal 12)
    lalu menghasilkan candlestick.
    """
    print("==================================================")
    print("  MAS TRADING VISUALIZER (Candlestick)")
    print("==================================================")
    
    folder_name = f"result_{args.ticker.replace('.', '_')}_{args.start}_{args.end}"
    out_dir = os.path.join("results", folder_name)
    trades_csv = os.path.join(out_dir, f"trades_{args.agents}_{args.ticker.replace('.', '_')}.csv")

    if not os.path.exists(trades_csv):
        print(f"Error: File trades tidak ditemukan: {trades_csv}")
        return

    ohlcv_path = os.path.join("data", "cache", args.ticker, "master_ohlcv.csv")
    if not os.path.exists(ohlcv_path):
        print(f"Error: File OHLCV tidak ditemukan.")
        return

    output_path = os.path.join(out_dir, f"Candlestick_{args.agents}_{args.ticker.replace('.', '_')}.png")

    plot_mas_ohlcv(
        ohlcv_path=ohlcv_path,
        trades_csv_path=trades_csv,
        ticker=args.ticker,
        output_path=output_path
    )
    print(f"Berhasil membuat candlestick: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Trading Backtester")
    parser.add_argument("--mode", type=str, choices=["backtest", "plot", "compare_all"], default="backtest",
                        help="Mode operasi: 'backtest', 'plot', atau 'compare_all'")
    parser.add_argument("--ticker", type=str, default="BBCA.JK", help="Stock ticker (e.g., BBCA.JK)")
    parser.add_argument("--start", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-01-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100_000_000.0, help="Initial capital in IDR")
    parser.add_argument("--trades-csv", type=str, default=None,
                        help="Path ke file trades CSV (untuk --mode plot). Jika tidak ditentukan, auto-detect.")
    parser.add_argument("--nav-csv", type=str, default=None,
                        help="Path ke file NAV CSV (opsional)")
    parser.add_argument("--agents", type=int, choices=[1, 8, 12], default=12,
                        help="Jumlah agen untuk simulasi MAS (12 = default, 8 = paper clone, 1 = single agent)")

    args = parser.parse_args()

    if args.mode == "backtest":
        run_backtest(args)
    elif args.mode == "plot":
        run_plot(args)
    elif args.mode == "compare_all":
        run_compare_all(args)


if __name__ == "__main__":
    main()
