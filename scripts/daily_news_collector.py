"""
Daily News Collector for Multi-Agent LLM Trading System
Mengumpulkan berita harian untuk 5 bank terkemuka Indonesia:
- BBRI.JK (Bank Rakyat Indonesia)
- BBCA.JK (Bank Central Asia)
- BMRI.JK (Bank Mandiri)
- BBNI.JK (Bank Negara Indonesia)
- BRIS.JK (Bank Syariah Indonesia)

Fitur:
- Otomatis membuat folder cache jika belum ada
- Menyaring kata kunci tidak relevan (clickbait, edukasi pemula, dll)
- Membersihkan format deskripsi berita (menghapus HTML gambar & boilerplate)
- Menggabungkan berita baru dengan arsip lama secara inkremental tanpa duplikasi
"""

import sys
import os
import datetime

# Tambahkan direktori root proyek ke sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.cache_manager import CacheManager
from tools.news_fetcher import NewsFetcher

TARGET_TICKERS = [
    "BBRI.JK",
    "BBCA.JK",
    "BMRI.JK",
    "BBNI.JK",
    "BRIS.JK"
]

def main():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=======================================================")
    print(f"[{now_str}] Memulai Koleksi Berita Harian 5 Bank")
    print(f"=======================================================")
    
    cache_manager = CacheManager()
    news_fetcher = NewsFetcher(cache_manager)
    
    success_count = 0
    for ticker in TARGET_TICKERS:
        try:
            print(f"\n--> Memproses {ticker}...")
            news_items = news_fetcher.fetch_all_news(ticker)
            print(f"    Berhasil: {len(news_items)} total berita valid tersimpan.")
            success_count += 1
        except Exception as e:
            print(f"    [Error] Gagal mengumpulkan berita untuk {ticker}: {e}")
            
    finish_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{finish_str}] Selesai! Berhasil memproses {success_count}/{len(TARGET_TICKERS)} bank.\n")


if __name__ == "__main__":
    main()
