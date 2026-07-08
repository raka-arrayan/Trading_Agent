"""
Test Data Fetch -- Validasi end-to-end bahwa data pipeline bekerja dengan benar.

Skrip ini menguji:
1. Koneksi internet ke yfinance
2. Download OHLCV master CSV
3. Slicing per-tanggal + perhitungan indikator teknikal
4. Verifikasi file tersimpan di folder yang benar
5. Verifikasi close price bukan 0 atau dummy

Cara menjalankan:
    python scripts/test_data_fetch.py
"""

import os
import sys
import io
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from tools.cache_manager import CacheManager
from tools.data_fetcher import YFinanceFetcher
from tools.indicator_calculator import TechnicalIndicatorCalculator

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# === Configuration ===
TICKER = "BBCA.JK"
START_DATE = "2024-01-02"
END_DATE = "2024-01-04"
CACHE_DIR = "data/cache"

def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_internet_connection():
    """Test 1: Cek koneksi internet ke yfinance."""
    separator("TEST 1: Koneksi Internet ke yfinance")
    
    import yfinance as yf
    try:
        df = yf.download(TICKER, period="1d", progress=False)
        if df.empty:
            print("[FAIL] GAGAL: yfinance terhubung tapi tidak mengembalikan data.")
            print("   Kemungkinan: ticker salah atau market sedang tutup.")
            return False
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        close = df['Close'].iloc[-1] if 'Close' in df.columns else df['close'].iloc[-1]
        print(f"[OK] BERHASIL: Terhubung ke yfinance.")
        print(f"   Ticker: {TICKER}")
        print(f"   Close terakhir: Rp {close:,.2f}")
        return True
    except Exception as e:
        print(f"[FAIL] GAGAL: Tidak bisa terhubung ke yfinance.")
        print(f"   Error: {e}")
        print(f"   Solusi: Cek koneksi internet Anda.")
        return False

def test_master_csv_download():
    """Test 2: Download dan simpan master OHLCV CSV."""
    separator("TEST 2: Download Master OHLCV CSV")
    
    cache_manager = CacheManager(base_dir=CACHE_DIR)
    data_fetcher = YFinanceFetcher(cache_manager)
    
    # Hapus master CSV lama jika ada (untuk test bersih)
    master_path = Path(CACHE_DIR) / TICKER / "ohlcv_master.csv"
    if master_path.exists():
        os.remove(master_path)
        print(f"   Menghapus master CSV lama: {master_path}")
    
    # Download
    df = data_fetcher.fetch_ohlcv_master(TICKER, START_DATE, END_DATE)
    
    if df.empty:
        print("[FAIL] GAGAL: fetch_ohlcv_master mengembalikan DataFrame kosong.")
        return False, None
    
    # Verifikasi file tersimpan
    if not master_path.exists():
        print(f"[FAIL] GAGAL: File master CSV tidak ditemukan di {master_path}")
        return False, None
    
    file_size = master_path.stat().st_size
    print(f"[OK] BERHASIL: Master CSV tersimpan.")
    print(f"   Path: {master_path}")
    print(f"   Ukuran: {file_size:,} bytes")
    print(f"   Jumlah baris: {len(df)}")
    print(f"   Kolom: {list(df.columns)}")
    print(f"   Rentang tanggal: {df.index[0].strftime('%Y-%m-%d')} → {df.index[-1].strftime('%Y-%m-%d')}")
    
    return True, df

def test_indicator_calculation(master_df: pd.DataFrame):
    """Test 3: Slice per-tanggal dan hitung indikator."""
    separator("TEST 3: Slicing + Perhitungan Indikator (ini mungkin lambat)")
    
    cache_manager = CacheManager(base_dir=CACHE_DIR)
    indicator_calc = TechnicalIndicatorCalculator(cache_manager)
    
    # Dapatkan tanggal trading dalam rentang
    start_dt = pd.to_datetime(START_DATE)
    end_dt = pd.to_datetime(END_DATE)
    trading_dates = [d.strftime('%Y-%m-%d') for d in master_df.index 
                     if start_dt <= d <= end_dt]
    
    if not trading_dates:
        print(f"[FAIL] GAGAL: Tidak ada tanggal trading antara {START_DATE} dan {END_DATE}")
        return False
    
    print(f"   Tanggal trading ditemukan: {trading_dates}")
    
    all_ok = True
    for date_str in trading_dates:
        target_dt = pd.to_datetime(date_str)
        df_slice = master_df.loc[master_df.index <= target_dt].copy()
        
        # Simpan slice ke folder tanggal
        cache_manager.save_csv(TICKER, date_str, "ohlcv.csv", df_slice)
        
        # Hitung indikator
        indicators = indicator_calc.calculate_indicators(TICKER, date_str)
        
        # Verifikasi
        ohlcv_path = Path(CACHE_DIR) / TICKER / date_str / "ohlcv.csv"
        indicators_path = Path(CACHE_DIR) / TICKER / date_str / "indicators.json"
        
        if not ohlcv_path.exists():
            print(f"   [FAIL] {date_str}: ohlcv.csv TIDAK DITEMUKAN")
            all_ok = False
            continue
            
        if not indicators_path.exists():
            print(f"   [FAIL] {date_str}: indicators.json TIDAK DITEMUKAN")
            all_ok = False
            continue
        
        close_price = indicators.get("close", 0)
        if close_price is None or close_price == 0:
            print(f"   [FAIL] {date_str}: close price = {close_price} (INVALID)")
            all_ok = False
            continue
        
        rsi = indicators.get("rsi_14")
        macd = indicators.get("macd")
        print(f"   [OK] {date_str}: Close=Rp {close_price:,.2f} | RSI={rsi} | MACD={macd}")
    
    if all_ok:
        print(f"\n[OK] BERHASIL: Semua {len(trading_dates)} tanggal terisi dengan benar.")
    else:
        print(f"\n[FAIL] SEBAGIAN GAGAL: Lihat detail di atas.")
    
    return all_ok

def test_cache_structure():
    """Test 4: Verifikasi struktur folder cache."""
    separator("TEST 4: Verifikasi Struktur Cache")
    
    base = Path(CACHE_DIR) / TICKER
    
    # Check master CSV
    master_path = base / "ohlcv_master.csv"
    print(f"   Master CSV: {'[OK] Ada' if master_path.exists() else '[FAIL] Tidak ada'} ({master_path})")
    
    # Check per-date folders
    import yfinance as yf
    df = yf.download(TICKER, start=START_DATE, end=END_DATE, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    trading_dates = [d.strftime('%Y-%m-%d') for d in df.index]
    
    all_ok = True
    for date_str in trading_dates:
        date_dir = base / date_str
        ohlcv = date_dir / "ohlcv.csv"
        indicators = date_dir / "indicators.json"
        
        ohlcv_ok = ohlcv.exists()
        ind_ok = indicators.exists()
        
        status = "[OK]" if (ohlcv_ok and ind_ok) else "[FAIL]"
        if not (ohlcv_ok and ind_ok):
            all_ok = False
        
        print(f"   {status} {date_str}/  "
              f"ohlcv.csv={'[OK]' if ohlcv_ok else '[FAIL]'}  "
              f"indicators.json={'[OK]' if ind_ok else '[FAIL]'}")
    
    return all_ok

def main():
    print("=" * 60)
    print("  DATA FETCH VALIDATION SCRIPT")
    print("  Ticker: {}  Period: {} -> {}".format(TICKER, START_DATE, END_DATE))
    print("=" * 60)
    
    results = {}
    
    # Test 1: Internet
    results["internet"] = test_internet_connection()
    if not results["internet"]:
        print("\n[STOP] Berhenti: Koneksi internet gagal. Perbaiki koneksi lalu coba lagi.")
        return
    
    # Test 2: Master CSV
    results["master"], master_df = test_master_csv_download()
    if not results["master"]:
        print("\n[STOP] Berhenti: Gagal download master CSV.")
        return
    
    # Test 3: Indicators
    results["indicators"] = test_indicator_calculation(master_df)
    
    # Test 4: Cache structure
    results["cache"] = test_cache_structure()
    
    # Summary
    separator("RINGKASAN")
    for test_name, passed in results.items():
        if test_name == "master":
            continue  # Skip tuple result
        status = "[OK] PASS" if passed else "[FAIL] FAIL"
        print(f"   {status}  {test_name}")
    
    if all(v if not isinstance(v, tuple) else v[0] for v in results.values()):
        print("\n>>> SEMUA TEST BERHASIL! <<<")
        print("   Anda dapat menjalankan backtest dengan percaya diri:")
        print(f"   python main.py --ticker {TICKER} --start {START_DATE} --end {END_DATE} --capital 100000000")
    else:
        print("\n[WARNING] Ada test yang gagal. Periksa detail di atas.")

if __name__ == "__main__":
    main()
