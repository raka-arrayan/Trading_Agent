import matplotlib
matplotlib.use('Agg')  # Backend non-interaktif: render ke file tanpa membuka jendela GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf
import os

def plot_performance(dates: list, mas_nav: list, bh_nav: list, ticker: str, output_path: str = "results/backtest_plot.png"):
    """
    Plot the performance of MAS vs Buy-and-Hold and save to a PNG file.
    
    Args:
        dates: list of str, date strings
        mas_nav: list of float, Net Asset Value of MAS portfolio
        bh_nav: list of float, Net Asset Value of Buy and Hold portfolio
        ticker: str, the stock ticker
        output_path: str, path to save the plot
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    # Plot MAS NAV
    plt.plot(dates, mas_nav, label=f"MAS Agent (NAV)", color="blue", linewidth=2)
    
    # Plot Buy and Hold NAV
    plt.plot(dates, bh_nav, label=f"Buy and Hold (NAV)", color="gray", linestyle="--", linewidth=2)
    
    plt.title(f"Performance Comparison: Multi-Agent System vs Buy-and-Hold ({ticker})")
    plt.xlabel("Date")
    plt.ylabel("Net Asset Value (IDR)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels if there are many dates
    if len(dates) > 10:
        plt.xticks(range(0, len(dates), len(dates)//10), rotation=45)
    else:
        plt.xticks(rotation=45)
        
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved successfully to {output_path}")
    
    plt.close()

def plot_ablation(df: pd.DataFrame, ticker: str, output_path: str):
    """
    Plot perbandingan hasil simulasi (Ablation Study).
    Menggambar garis untuk MAS 12, MAS 8, MAS 1, B&H, SMA, MACD.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(14, 7))
    
    dates = df['Date']
    
    # Warna yang berbeda untuk setiap strategi
    colors = {
        'MAS12_NAV': 'blue',
        'MAS8_NAV': 'orange',
        'MAS1_NAV': 'red',
        'BH_NAV': 'gray',
        'SMA_NAV': 'green',
        'MACD_NAV': 'purple'
    }
    
    labels = {
        'MAS12_NAV': 'MAS (12 Agen)',
        'MAS8_NAV': 'MAS (8 Agen)',
        'MAS1_NAV': 'MAS (1 Agen)',
        'BH_NAV': 'Buy & Hold',
        'SMA_NAV': 'SMA Crossover',
        'MACD_NAV': 'MACD Signal'
    }
    
    for col in df.columns:
        if col in colors:
            plt.plot(dates, df[col], label=labels[col], color=colors[col], linewidth=2 if 'MAS' in col else 1.5, linestyle='-' if 'MAS12' in col else '--')

    plt.title(f"Ablation Study & Benchmark Comparison ({ticker})", fontsize=14, fontweight='bold')
    plt.xlabel("Date")
    plt.ylabel("Net Asset Value (IDR)")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    if len(dates) > 10:
        plt.xticks(range(0, len(dates), len(dates)//10), rotation=45)
    else:
        plt.xticks(rotation=45)
        
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()



def plot_mas_ohlcv(ohlcv_path: str, trades_csv_path: str, ticker: str,
                   output_path: str = "results/candlestick_chart.png",
                   padding_days: int = 5):
    """
    Visualisasi Komprehensif: Candlestick OHLCV + Penanda Keputusan Multi-Agent System.
    
    Fungsi ini menghasilkan grafik candlestick yang menampilkan pergerakan harga saham
    beserta penanda (marker) pada titik-titik di mana Multi-Agent System (MAS) — yang
    terdiri dari 12 agen independen — telah mengambil keputusan trading melalui proses
    konsensus kolektif.
    
    PENTING - Dokumentasi Penanda:
    -----------------------------
    Penanda segitiga pada grafik ini BUKAN sinyal dari indikator teknikal tunggal.
    Setiap penanda merepresentasikan keputusan AKHIR yang telah diproses oleh
    Multi-Agent System (MAS), di mana 12 agen AI (termasuk analis fundamental,
    teknikal, makro, sentimen, peneliti bullish/bearish, fasilitator riset,
    analis risiko agresif/konservatif, fasilitator risiko, manajer portofolio,
    dan agen trading) secara kolektif berdebat dan mencapai konsensus.
    
    Jenis Penanda:
      ^ Segitiga Hijau (^) = Keputusan BUY  dari konsensus MAS
      v Segitiga Merah (v) = Keputusan SELL dari konsensus MAS
      (Hari tanpa penanda = HOLD / tidak ada aksi trading)
    
    Args:
        ohlcv_path: str, path absolut ke file master_ohlcv.csv
                    Format: date,close,high,low,open,volume
        trades_csv_path: str, path ke file trades CSV hasil backtest MAS
                         Format: date,action,price,shares,cost
        ticker: str, kode saham (e.g., "BBCA.JK")
        output_path: str, path untuk menyimpan grafik PNG
        padding_days: int, jumlah hari padding sebelum/sesudah rentang trades
                      untuk memberikan konteks pergerakan harga
    
    Returns:
        None. Grafik disimpan sebagai file PNG di output_path.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # ── 1. Muat Data OHLCV ──────────────────────────────────────────────
    print(f"\n  [1/4] Memuat data OHLCV dari: {ohlcv_path}")
    df_ohlcv = pd.read_csv(ohlcv_path, parse_dates=['date'], index_col='date')
    
    # Standarisasi nama kolom ke format yang dibutuhkan mplfinance
    # mplfinance mengharapkan: Open, High, Low, Close, Volume
    column_map = {}
    for col in df_ohlcv.columns:
        col_lower = col.lower()
        if col_lower == 'open':
            column_map[col] = 'Open'
        elif col_lower == 'high':
            column_map[col] = 'High'
        elif col_lower == 'low':
            column_map[col] = 'Low'
        elif col_lower == 'close':
            column_map[col] = 'Close'
        elif col_lower == 'volume':
            column_map[col] = 'Volume'
    
    df_ohlcv.rename(columns=column_map, inplace=True)
    df_ohlcv.index.name = 'Date'
    
    # Pastikan kolom yang diperlukan ada
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in required_cols:
        if col not in df_ohlcv.columns:
            print(f"  ERROR: Kolom '{col}' tidak ditemukan dalam data OHLCV.")
            print(f"  Kolom yang tersedia: {list(df_ohlcv.columns)}")
            return
    
    print(f"  Loaded {len(df_ohlcv)} rows of OHLCV data.")
    
    # ── 2. Muat Log Transaksi MAS ───────────────────────────────────────
    print(f"  [2/4] Memuat log transaksi MAS dari: {trades_csv_path}")
    df_trades = pd.read_csv(trades_csv_path, parse_dates=['date'])
    print(f"  Loaded {len(df_trades)} MAS trading decisions.")
    
    if df_trades.empty:
        print("  WARNING: File trades kosong. Grafik akan ditampilkan tanpa penanda.")
    
    # ── 3. Filter Rentang Tanggal ───────────────────────────────────────
    print(f"  [3/4] Memfilter data sesuai rentang tanggal trades...")
    
    if not df_trades.empty:
        # Tentukan rentang berdasarkan tanggal trades + padding
        min_trade_date = df_trades['date'].min()
        max_trade_date = df_trades['date'].max()
        
        start_filter = min_trade_date - pd.Timedelta(days=padding_days)
        end_filter = max_trade_date + pd.Timedelta(days=padding_days)
        
        # Filter OHLCV ke rentang yang relevan
        mask = (df_ohlcv.index >= start_filter) & (df_ohlcv.index <= end_filter)
        df_plot = df_ohlcv[mask].copy()
    else:
        # Jika tidak ada trades, tampilkan 30 hari terakhir
        df_plot = df_ohlcv.tail(30).copy()
    
    if df_plot.empty:
        print("  ERROR: Tidak ada data OHLCV dalam rentang tanggal yang diminta.")
        return
    
    print(f"  Rentang grafik: {df_plot.index.min().strftime('%Y-%m-%d')} "
          f"s/d {df_plot.index.max().strftime('%Y-%m-%d')} ({len(df_plot)} hari)")
    
    # -- 4. Siapkan Penanda BUY/SELL dari Keputusan MAS ------------------
    print(f"  [4/4] Menyiapkan penanda keputusan MAS pada grafik...")
    
    # Buat kolom NaN untuk marker (mplfinance membutuhkan NaN di hari tanpa marker)
    buy_markers = pd.Series(np.nan, index=df_plot.index)
    sell_markers = pd.Series(np.nan, index=df_plot.index)
    
    buy_count = 0
    sell_count = 0
    
    for _, trade in df_trades.iterrows():
        trade_date = trade['date']
        action = trade['action'].upper().strip()
        
        # Cari tanggal terdekat di data OHLCV (untuk menangani perbedaan timezone)
        if trade_date in df_plot.index:
            idx = trade_date
        else:
            # Cari tanggal terdekat yang ada di data
            closest_idx = df_plot.index.get_indexer([trade_date], method='nearest')
            if closest_idx[0] >= 0:
                idx = df_plot.index[closest_idx[0]]
            else:
                continue
        
        if action == 'BUY':
            # Letakkan marker BUY di bawah Low candle (agar segitiga di bawah)
            buy_markers[idx] = df_plot.loc[idx, 'Low'] * 0.998
            buy_count += 1
        elif action == 'SELL':
            # Letakkan marker SELL di atas High candle (agar segitiga di atas)
            sell_markers[idx] = df_plot.loc[idx, 'High'] * 1.002
            sell_count += 1
    
    print(f"  Penanda: {buy_count} BUY (^ hijau), {sell_count} SELL (v merah)")
    
    # ── 5. Konfigurasi dan Render Grafik ────────────────────────────────
    
    # Buat list addplot untuk marker BUY dan SELL
    add_plots = []
    
    if buy_count > 0:
        ap_buy = mpf.make_addplot(
            buy_markers,
            type='scatter',
            markersize=120,
            marker='^',          # Segitiga ke atas = BUY
            color='#00C853',     # Hijau terang
            label='BUY (MAS Decision)'
        )
        add_plots.append(ap_buy)
    
    if sell_count > 0:
        ap_sell = mpf.make_addplot(
            sell_markers,
            type='scatter',
            markersize=120,
            marker='v',          # Segitiga ke bawah = SELL
            color='#FF1744',     # Merah terang
            label='SELL (MAS Decision)'
        )
        add_plots.append(ap_sell)
    
    # Konfigurasi style grafik
    mc = mpf.make_marketcolors(
        up='#00C853',       # Candle naik = hijau
        down='#FF1744',     # Candle turun = merah
        edge='inherit',
        wick='inherit',
        volume='in',
        ohlc='i'
    )
    
    style = mpf.make_mpf_style(
        marketcolors=mc,
        figcolor='#FAFAFA',
        facecolor='#FAFAFA',
        gridcolor='#E0E0E0',
        gridstyle='--',
        gridaxis='both',
        y_on_right=True,
        rc={
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
        }
    )
    
    # Judul grafik
    title = (
        f"{ticker} - Candlestick Chart + Multi-Agent System (MAS) Decisions\n"
        f"Markers: ^ BUY (green) and v SELL (red) = MAS consensus decisions from 12 AI agents"
    )
    
    # Render grafik dengan mplfinance
    # Menggunakan returnfig=True agar mplfinance tidak memanggil plt.show()
    # yang bisa menyebabkan hang di terminal Windows tanpa GUI
    kwargs = dict(
        type='candle',
        style=style,
        title=title,
        ylabel='Harga (IDR)',
        ylabel_lower='Volume',
        volume=True,
        figsize=(16, 9),
        tight_layout=True,
        returnfig=True,
    )
    
    if add_plots:
        kwargs['addplot'] = add_plots
    
    fig, axes = mpf.plot(df_plot, **kwargs)
    
    # Simpan grafik secara manual
    fig.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    
    print(f"\n  [OK] Grafik candlestick berhasil disimpan ke: {output_path}")
    print(f"  Grafik menampilkan {len(df_plot)} hari data OHLCV dengan "
          f"{buy_count + sell_count} penanda keputusan MAS.")

