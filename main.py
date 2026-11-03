import argparse
import pandas as pd
import json
import os
import glob
import sys
from orchestration.backtester import Backtester
from orchestration.live_trader import LiveTrader
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

    return df_master


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
        dates = results.get("dates", [])
        mas_nav = results.get("mas_nav", [])
        bh_nav = results.get("bh_nav", [])
        trades = results.get("trades", [])

        if not dates:
            print("\n[PERINGATAN] Tidak ada hari bursa yang valid pada rentang tanggal tersebut!")
            print(f"Pastikan rentang tanggal ({args.start} s/d {args.end}) berada di masa lalu dan data OHLCV tersedia di pasar.")
            return

        # 3. Generate Benchmark NAVs and Plots
        df_master = generate_benchmark_and_plots(
            ticker=args.ticker,
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital,
            dates=dates,
            mas_nav=mas_nav,
            out_dir=out_dir
        )

        bh_series = df_master['BH_NAV'].tolist() if 'BH_NAV' in df_master else bh_nav
        sma_series = df_master['SMA_NAV'].tolist() if 'SMA_NAV' in df_master else [args.capital]*len(dates)
        macd_series = df_master['MACD_NAV'].tolist() if 'MACD_NAV' in df_master else [args.capital]*len(dates)

        # 4. Calculate Metrics for All Strategies
        mas_metrics = calculate_metrics(mas_nav, trades, risk_free_rate_annual=0.06)
        bh_metrics = calculate_metrics(bh_series, [], risk_free_rate_annual=0.06)
        sma_metrics = calculate_metrics(sma_series, [], risk_free_rate_annual=0.06)
        macd_metrics = calculate_metrics(macd_series, [], risk_free_rate_annual=0.06)

        results_table = (
            "\n" + "=" * 92 + "\n"
            + "                                  BACKTEST RESULTS                                            \n"
            + "=" * 92 + "\n"
            + f"{'Metric':<20} | {'MAS Portfolio':<15} | {'Buy & Hold':<15} | {'SMA Crossover':<15} | {'MACD Signal':<15}\n"
            + "-" * 92 + "\n"
            + f"{'Final NAV (Rp)':<20} | {mas_nav[-1]:>15,.0f} | {bh_series[-1]:>15,.0f} | {sma_series[-1]:>15,.0f} | {macd_series[-1]:>15,.0f}\n"
            + f"{'Cumulative Return':<20} | {mas_metrics['Cumulative Return']*100:>14.2f}% | {bh_metrics['Cumulative Return']*100:>14.2f}% | {sma_metrics['Cumulative Return']*100:>14.2f}% | {macd_metrics['Cumulative Return']*100:>14.2f}%\n"
            + f"{'Sharpe Ratio':<20} | {mas_metrics['Sharpe Ratio']:>15.2f} | {bh_metrics['Sharpe Ratio']:>15.2f} | {sma_metrics['Sharpe Ratio']:>15.2f} | {macd_metrics['Sharpe Ratio']:>15.2f}\n"
            + f"{'Max Drawdown':<20} | {mas_metrics['Max Drawdown']*100:>14.2f}% | {bh_metrics['Max Drawdown']*100:>14.2f}% | {sma_metrics['Max Drawdown']*100:>14.2f}% | {macd_metrics['Max Drawdown']*100:>14.2f}%\n"
            + f"{'Win Rate':<20} | {mas_metrics['Win Rate']*100:>14.2f}% | {'N/A':>15} | {'N/A':>15} | {'N/A':>15}\n"
            + "=" * 92
        )
        print(results_table)

    finally:
        sys.stdout = original_stdout
        log_file.close()

    # Tampilkan tabel hasil ke console
    print(results_table)
    print(f"\n[INFO] Simulasi selesai. Log perdebatan AI tersimpan di: {log_path}")

    # 5. Save Trades to CSV
    csv_trades_path = os.path.join(out_dir, f"trades_{clean_ticker}.csv")
    if trades:
        df_trades = pd.DataFrame(trades)
        df_trades.to_csv(csv_trades_path, index=False)
        print(f"Saved trade logs to {csv_trades_path}")
    else:
        # Jika tidak ada transaksi, simpan format kosong agar visualizer tidak error
        pd.DataFrame(columns=["date", "action", "price", "shares", "cost"]).to_csv(csv_trades_path, index=False)
        print(f"No trades executed. Created empty trade log at {csv_trades_path}")

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


def run_live(args):
    """
    Mode LIVE: Menjalankan rekomendasi trading on-demand (real-time)
    berdasarkan data harga pasar terkini dan berita 7 hari terakhir.
    Mencetak tiket rekomendasi dan menyimpan satu berkas log notulensi 12 agen.
    """
    clean_ticker = args.ticker.replace('.', '_')
    today_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    out_dir = os.path.join("results", "live")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, f"live_{clean_ticker}_{today_str}.txt")

    trader = LiveTrader(
        ticker=args.ticker,
        capital=args.capital,
        fee_rate=0.002
    )

    # Arahkan seluruh print dan notulensi debat ke file log (seperti pada run_backtest)
    log_file = open(log_path, "w", encoding="utf-8")
    original_stdout = sys.stdout
    sys.stdout = log_file

    print(f"[INFO] Memulai sesi Live Decision untuk {args.ticker}...", file=original_stdout)

    try:
        live_result = trader.run_live()
        final_state = live_result["final_state"]
        decision = live_result["decision"]
        current_price = live_result["current_price"]

        # 1. Cetak Explainable AI (Notulensi 12 Agen) HANYA ke dalam file TXT
        from tabulate import tabulate
        analyst_reports = final_state.get("analyst_reports", {})
        research_debate = final_state.get("research_debate", [])
        research_consensus = final_state.get("research_consensus", "")
        risk_debate = final_state.get("risk_debate", [])
        risk_consensus = final_state.get("risk_consensus", "")
        portfolio_status = final_state.get("portfolio_status", {})
        pm_rec = portfolio_status.get("recommendation", "")

        def clean_text(text):
            if not text: return "(kosong)"
            if isinstance(text, list):
                text = " ".join([str(x) for x in text])
            return str(text).replace('\n', ' ').strip()

        print("\n" + "=" * 70)
        print("          NOTULENSI DEBAT & KONSENSUS 12 AGEN (EXPLAINABLE AI)         ")
        print("=" * 70)

        table_data = []

        def print_agent_record(name, text, strategy_override=None, confidence="-"):
            if not text: return
            strategy = strategy_override or Backtester._extract_strategy_from_text(text)
            conclusion = clean_text(text)
            print(f"\n[{name}]")
            print(f"Kesimpulan: {conclusion}")
            print(f"Strategi  : {strategy}")
            table_data.append([name, strategy, confidence])

        # Analysts
        for key in ["fundamental", "macro", "sentiment", "technical"]:
            if key in analyst_reports:
                print_agent_record(f"{key.capitalize()} Analyst", analyst_reports[key])

        # Researchers
        for debate in research_debate:
            agent = debate.get("agent", "")
            strategy = "BUY" if agent == "Bullish" else "SELL" if agent == "Bearish" else None
            print_agent_record(f"{agent} Researcher", debate.get("message", ""), strategy)

        if research_consensus:
            print_agent_record("Research Facilitator", research_consensus)

        # Risk Analysts
        for debate in risk_debate:
            agent = debate.get("agent", "")
            print_agent_record(f"{agent} Analyst", debate.get("message", ""))

        if risk_consensus:
            print_agent_record("Risk Facilitator", risk_consensus)

        # Portfolio Manager
        if pm_rec:
            print_agent_record("Portfolio Manager", pm_rec)

        # Trading Agent
        action = decision.get("action", "HOLD")
        qty = decision.get("quantity", 0)
        conf = decision.get("confidence", 0.0)
        print(f"\n[Trading Agent]")
        print(f"Kesimpulan: Eksekusi {action} {qty} lot.")
        print(f"Strategi  : {action}")
        table_data.append(["Trading Agent", action, conf])

        print("\n" + tabulate(table_data, headers=["Nama Agen", "Strategi", "Keyakinan"], tablefmt="grid"))

        # 2. Tiket Eksekusi Final (Dicatat ke file TXT)
        shares_to_trade = qty * 100
        cost = shares_to_trade * current_price
        fee = cost * 0.002
        total_spent = cost + fee
        remaining_cash = args.capital - total_spent if action == "BUY" else args.capital

        print("\n" + "=" * 70)
        print("                   TIKET REKOMENDASI TRADING LIVE                     ")
        print("=" * 70)
        print(f"Tanggal Sinyal    : {today_str}")
        print(f"Ticker Target     : {args.ticker}")
        print(f"Harga Pasar Terkini: Rp {current_price:,.2f}")
        print(f"Modal Kas Awal    : Rp {args.capital:,.2f}")
        print("-" * 70)
        print(f"REKOMENDASI AKSI  : {action}")
        print(f"Jumlah Eksekusi   : {qty} Lot ({shares_to_trade:,} Lembar)")
        if action == "BUY":
            print(f"Estimasi Nilai    : Rp {cost:,.2f}")
            print(f"Estimasi Fee (0.2%): Rp {fee:,.2f}")
            print(f"Total Pengeluaran : Rp {total_spent:,.2f}")
            print(f"Sisa Kas Portofolio: Rp {remaining_cash:,.2f}")
        elif action == "SELL":
            print(f"Potensi Pendapatan: Rp {cost:,.2f} (Sebelum Fee)")
        else:
            print(f"Keterangan        : Tidak ada perubahan posisi (Tahan Kas).")
        print("=" * 70)
        print(f"[SUKSES] Sesi live selesai! Notulensi resmi tersimpan di: {log_path}\n")

    finally:
        sys.stdout = original_stdout
        log_file.close()

    # Di terminal CMD hanya tampil pemberitahuan selesai yang bersih
    print(f"\n[SUKSES] Sesi live selesai!")
    print(f"Seluruh notulensi debat 12 agen dan tiket rekomendasi tersimpan rapi di:")
    print(f"-> {log_path}\n")


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System Trading Backtester")
    parser.add_argument("--mode", type=str, choices=["backtest", "live"], default="backtest",
                        help="Mode operasi: 'backtest' (default) atau 'live' (rekomendasi keputusan hari ini)")
    parser.add_argument("--ticker", type=str, default="BBCA.JK", help="Stock ticker (e.g., BBCA.JK)")
    parser.add_argument("--start", type=str, default="2026-10-12", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2026-10-30", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100_000_000.0, help="Initial capital in IDR")
    parser.add_argument("--agents", type=int, choices=[1, 8, 12], default=12,
                        help="Jumlah agen untuk simulasi MAS (default 12 agen)")

    args = parser.parse_args()

    if args.mode == "backtest":
        run_backtest(args)
    elif args.mode == "live":
        run_live(args)


if __name__ == "__main__":
    main()
