"""
Test Data Fetch -- Validasi end-to-end untuk arsitektur Centralized Caching.

Skrip ini menguji:
1. Koneksi internet ke yfinance
2. Download dan simpan master_ohlcv.csv
3. In-memory slicing + perhitungan indikator teknikal (tanpa file per-tanggal)
4. Verifikasi struktur cache bersih (hanya master files, tanpa folder tanggal)

Cara menjalankan:
    python scripts/test_data_fetch.py
"""

import os
import sys
import io
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
from tools.cache_manager import CacheManager
from tools.data_fetcher import YFinanceFetcher
from tools.indicator_calculator import TechnicalIndicatorCalculator

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
            print("[FAIL] yfinance terhubung tapi tidak mengembalikan data.")
            return False
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        close = df['Close'].iloc[-1] if 'Close' in df.columns else df['close'].iloc[-1]
        print(f"[OK] Terhubung ke yfinance. Close terakhir: Rp {close:,.2f}")
        return True
    except Exception as e:
        print(f"[FAIL] Tidak bisa terhubung: {e}")
        return False

def test_master_csv_download():
    """Test 2: Download dan simpan master OHLCV CSV."""
    separator("TEST 2: Download Master OHLCV CSV")
    
    cache_manager = CacheManager(base_dir=CACHE_DIR)
    data_fetcher = YFinanceFetcher(cache_manager)
    
    # Hapus master CSV lama jika ada (untuk test bersih)
    master_path = Path(CACHE_DIR) / TICKER / "master_ohlcv.csv"
    if master_path.exists():
        os.remove(master_path)
        print(f"  Menghapus master CSV lama: {master_path}")
    
    # Download
    df = data_fetcher.fetch_ohlcv(TICKER, START_DATE, END_DATE)
    
    if df.empty:
        print("[FAIL] fetch_ohlcv mengembalikan DataFrame kosong.")
        return False, None
    
    # Verifikasi file tersimpan
    if not master_path.exists():
        print(f"[FAIL] File master CSV tidak ditemukan di {master_path}")
        return False, None
    
    file_size = master_path.stat().st_size
    print(f"[OK] Master CSV tersimpan.")
    print(f"  Path     : {master_path}")
    print(f"  Ukuran   : {file_size:,} bytes")
    print(f"  Rows     : {len(df)}")
    print(f"  Kolom    : {list(df.columns)}")
    print(f"  Rentang  : {df.index[0].strftime('%Y-%m-%d')} -> {df.index[-1].strftime('%Y-%m-%d')}")
    
    return True, df

def test_inmemory_indicator_calculation(master_df: pd.DataFrame):
    """Test 3: In-memory slicing + perhitungan indikator (tanpa file I/O)."""
    separator("TEST 3: In-Memory Slicing + Indikator")
    
    indicator_calc = TechnicalIndicatorCalculator()
    
    # Dapatkan tanggal trading dalam rentang
    start_dt = pd.to_datetime(START_DATE)
    end_dt = pd.to_datetime(END_DATE)
    trading_dates = [d.strftime('%Y-%m-%d') for d in master_df.index 
                     if start_dt <= d <= end_dt]
    
    if not trading_dates:
        print(f"[FAIL] Tidak ada tanggal trading antara {START_DATE} dan {END_DATE}")
        return False
    
    print(f"  Tanggal trading: {trading_dates}")
    
    all_ok = True
    for date_str in trading_dates:
        target_dt = pd.to_datetime(date_str)
        
        # Slice in-memory (no look-ahead bias)
        df_slice = master_df.loc[master_df.index <= target_dt].copy()
        
        # Calculate indicators in-memory (no file I/O!)
        indicators = indicator_calc.calculate_indicators(df_slice, date_str)
        
        close_price = indicators.get("close", 0)
        if close_price is None or close_price == 0:
            print(f"  [FAIL] {date_str}: close price = {close_price} (INVALID)")
            all_ok = False
            continue
        
        rsi = indicators.get("rsi_14")
        macd = indicators.get("macd")
        print(f"  [OK] {date_str}: Close=Rp {close_price:,.2f} | RSI={rsi:.2f} | MACD={macd:.4f}")
    
    if all_ok:
        print(f"\n[OK] Semua {len(trading_dates)} tanggal berhasil dihitung in-memory.")
    else:
        print(f"\n[FAIL] Ada tanggal yang gagal.")
    
    return all_ok

def test_cleanup_legacy():
    """Test 4: Jalankan cleanup untuk menghapus folder lama."""
    separator("TEST 4: Cleanup Legacy Folders")
    
    cache_manager = CacheManager(base_dir=CACHE_DIR)
    cache_manager.cleanup_legacy_folders(TICKER)
    return True

def test_clean_cache_structure():
    """Test 5: Verifikasi folder cache bersih setelah cleanup."""
    separator("TEST 5: Verifikasi Struktur Cache Bersih")
    
    ticker_dir = Path(CACHE_DIR) / TICKER
    
    if not ticker_dir.exists():
        print(f"[FAIL] Folder ticker tidak ditemukan: {ticker_dir}")
        return False
    
    # List all items in the ticker directory
    items = list(ticker_dir.iterdir())
    master_files = [f for f in items if f.is_file()]
    subfolders = [d for d in items if d.is_dir()]
    
    print(f"  Folder: {ticker_dir}")
    print(f"  Master files: {[f.name for f in master_files]}")
    
    if subfolders:
        print(f"  [FAIL] Masih ada subfolder: {[d.name for d in subfolders]}")
        return False
    else:
        print(f"  [OK] Tidak ada subfolder -- struktur cache bersih!")
    
    # Check expected master files
    expected = ["master_ohlcv.csv"]
    found = [f.name for f in master_files]
    
    all_ok = True
    for expected_file in expected:
        if expected_file in found:
            print(f"  [OK] {expected_file} ditemukan")
        else:
            print(f"  [FAIL] {expected_file} TIDAK ditemukan")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("  DATA FETCH VALIDATION (Centralized Caching)")
    print(f"  Ticker: {TICKER}  Period: {START_DATE} -> {END_DATE}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Internet
    results["internet"] = test_internet_connection()
    if not results["internet"]:
        print("\n[STOP] Koneksi internet gagal.")
        return
    
    # Test 2: Master CSV
    success, master_df = test_master_csv_download()
    results["master_csv"] = success
    if not success:
        print("\n[STOP] Gagal download master CSV.")
        return
    
    # Test 3: In-memory indicators
    results["indicators"] = test_inmemory_indicator_calculation(master_df)
    
    # Test 4: Cleanup legacy folders
    results["cleanup"] = test_cleanup_legacy()

    # Test 5: Clean cache structure
    results["cache_structure"] = test_clean_cache_structure()
    
    # Summary
    separator("RINGKASAN")
    for test_name, passed in results.items():
        status = "[OK] PASS" if passed else "[FAIL] FAIL"
        print(f"  {status}  {test_name}")
    
    if all(results.values()):
        print("\n>>> SEMUA TEST BERHASIL! <<<")
        print("  Jalankan backtest:")
        print(f"  python main.py --ticker {TICKER} --start {START_DATE} --end {END_DATE} --capital 100000000")
    else:
        print("\n[WARNING] Ada test yang gagal.")

if __name__ == "__main__":
    main()
