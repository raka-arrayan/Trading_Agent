# PANDUAN PENGOPERASIAN SISTEM MULTI-AGENT TRADING (DOCKER)

Dokumen ini memuat panduan ringkas, jelas, dan realistis untuk menjalankan proyek **Multi-Agent System (MAS) Trading** berbasis Docker. Proyek ini berfokus pada dua mode operasional utama:
1. **Mode Backtest**: Menguji performa sistem pada data historis terverifikasi (mulai 12 Oktober 2026 ke atas).
2. **Mode Live**: Mengambil data harga dan berita terkini hari ini untuk menghasilkan rekomendasi sinyal trading riil (*Actionable Decision Support*).

---

## DAFTAR ISI
1. [Prasyarat Sistem](#1-prasyarat-sistem)
2. [Langkah 1: Kloning Repositori (Data Berita Sudah Siap Pakai)](#langkah-1-kloning-repositori-data-berita-sudah-siap-pakai)
3. [Langkah 2: Konfigurasi API Key (.env)](#langkah-2-konfigurasi-api-key-env)
4. [Langkah 3: Membangun Citra Docker (Build Image)](#langkah-3-membangun-citra-docker-build-image)
5. [Langkah 4: Menjalankan Mode Backtest (Mulai 12 Oktober 2026)](#langkah-4-menjalankan-mode-backtest-mulai-12-oktober-2026)
6. [Langkah 5: Menjalankan Mode Live (Keputusan Real-Time Hari Ini)](#langkah-5-menjalankan-mode-live-keputusan-real-time-hari-ini)
7. [Penjelasan Fitur & Arsitektur Sistem](#penjelasan-fitur--arsitektur-sistem)
8. [Rangkuman Perintah Cepat (Cheatsheet)](#rangkuman-perintah-cepat-cheatsheet)

---

## 1. Prasyarat Sistem
Pastikan perangkat Anda memenuhi syarat berikut sebelum menjalankan perintah:
1. **Docker Desktop** sudah terpasang dan dalam status **aktif/berjalan** (indikator di pojok kiri bawah menunjukkan warna hijau *"Engine running"*).
2. **Koneksi Internet** aktif untuk mengunduh base image dan menghubungi API penyedia LLM.
3. **API Key LLM** (Google Gemini API Key) untuk operasional musyawarah 12 agen.

---

## Langkah 1: Kloning Repositori (Data Berita Sudah Siap Pakai)
Buka terminal **PowerShell** atau **Command Prompt (CMD)**:

```powershell
# 1. Pindah ke direktori kerja Anda
cd C:\Users\rifqi\Documents\Seminar

# 2. Clone repository dari GitHub
git clone https://github.com/raka-arrayan/Trading_Agent.git Kode

# 3. Masuk ke dalam direktori proyek
cd Kode
```

> **Catatan Penting Tentang Data & News Collector:**
> 1. **Data Siap Pakai**: Anda secara umum **TIDAK PERLU** menjalankan proses pengumpulan berita (*news collector*) manual lagi. Pipeline **GitHub Actions** telah mengumpulkan berita dan harga pasar harian secara otomatis sejak **12 Oktober 2026**. Arsip lengkap harian tanpa bias (*ground truth*) sudah tersedia di folder `data/cache/` begitu Anda melakukan clone atau `git pull`.
> 2. **Penggunaan News Collector (Opsional)**: Layanan `news-collector` tetap tersedia di dalam Docker (`docker compose run --rm news-collector`). Layanan ini dapat digunakan secara opsional jika pengguna ingin memicu penarikan arsip berita untuk periode sebelum 12 Oktober 2026 atau melakukan penarikan mandiri di luar jadwal GitHub Actions. Namun, perlu dicatat bahwa akibat keterbatasan RSS feed publik, berita sebelum 12 Oktober 2026 tidak selengkap data harian yang dihimpun secara konsisten.

---

## Langkah 2: Konfigurasi API Key (.env)
Sistem 12 agen memerlukan akses ke LLM untuk membaca data, berdebat, dan mengambil keputusan. Buat berkas bernama `.env` di folder utama proyek (sejajar dengan `Dockerfile`):

```ini
# Berkas: .env
GEMINI_API_KEY=masukkan_api_key_gemini_anda_di_sini
```

---

## Langkah 3: Membangun Citra Docker (Build Image)
Bangun kontainer Docker untuk mengemas lingkungan Python 3.12, seluruh dependensi `requirements.txt`, dan kode proyek:

```powershell
docker compose build
```
*(Langkah ini hanya perlu dijalankan sekali, atau diulang jika Anda mengubah kode/requirements).*

---

## Langkah 4: Menjalankan Mode Backtest (Mulai 12 Oktober 2026)
Simulasi backtest digunakan untuk mengevaluasi performa strategi MAS secara ketat dengan mekanisme **Zero Look-Ahead Bias**.

> **Mengapa Mulai 12 Oktober 2026?**  
> Sumber data RSS memiliki keterbatasan arsip mundur. Pengumpulan berita harian yang berkesinambungan dan lengkap per hari dimulai pada **12 Oktober 2026**. Oleh karena itu, seluruh pengujian backtest dilakukan dari rentang **12 Oktober 2026 ke atas**.

### Contoh Perintah Backtest (Saham BMRI.JK periode 12 – 30 Oktober 2026):
```powershell
docker compose run --rm backtest python main.py --mode backtest --ticker BMRI.JK --start 2026-10-12 --end 2026-10-30 --capital 100000000 --agents 12
```

### Parameter:
- `--mode backtest` : Menjalankan simulasi portofolio historis.
- `--ticker BMRI.JK` : Kode saham yang diuji (format Yahoo Finance).
- `--start 2026-10-12` : Tanggal awal pengujian (harus $\ge$ 2026-10-12).
- `--end 2026-10-30` : Tanggal akhir pengujian.
- `--capital 100000000` : Modal awal kas (misal: Rp 100.000.000).
- `--agents 12` : Menjalankan konsensus penuh 12 agen.

### Hasil Eksekusi:
Setelah perintah selesai, sistem **otomatis** menyimpan seluruh hasil ke dalam folder:
`results/result_{TICKER}_{START}_{END}/` (Contoh: `results/result_BMRI_JK_2026-10-12_2026-10-30/`) yang berisi:
1. **`Candlestick_{TICKER}.png`** : **Grafik Candlestick OHLCV** lengkap dengan penanda titik beli (*Buy* panah hijau) dan jual (*Sell* panah merah) hasil keputusan agen.
2. **`Plot_LineChart_{TICKER}.png`** : Grafik garis perbandingan NAV MAS melawan strategi *Buy & Hold*, *SMA Crossover*, dan *MACD Signal*.
3. **`NAV_Master_{TICKER}.csv`** : Data nilai portofolio harian MAS beserta ketiga strategi tolok ukur.
4. **`trades_{TICKER}.csv`** : Rincian setiap transaksi (tanggal, harga eksekusi, volume lot, biaya).
5. **`log_{TICKER}.txt`** : Notulensi lengkap perdebatan 12 agen setiap minggunya dan tabel metrik evaluasi akhir (*Cumulative Return, Sharpe Ratio, Max Drawdown, Win Rate*).

---

## Langkah 5: Menjalankan Mode Live (Keputusan Real-Time Hari Ini)
Mode Live digunakan untuk mendapatkan **rekomendasi keputusan trading on-demand hari ini (*Actionable Decision Support*)** tanpa proses simulasi kalender masa lalu. Mode ini membaca harga pasar terkini dan berita 7 hari terakhir, lalu langsung menggelar sidang 12 agen.

### Contoh Perintah Mode Live:
```powershell
docker compose run --rm backtest python main.py --mode live --ticker BMRI.JK --capital 100000000 --agents 12
```

### Parameter:
- `--mode live` : Mengaktifkan sesi pengambilan keputusan real-time hari ini.
- `--ticker BMRI.JK` : Kode saham yang dianalisis.
- `--capital 100000000` : Modal kas saat ini yang siap dialokasikan.
- `--agents 12` : Menjalankan musyawarah 12 agen.

### Hasil Eksekusi Mode Live:
1. **Layar Terminal Bersih**:  
   Hanya menampilkan status proses dan notifikasi selesai (tidak membanjiri terminal dengan ratusan baris dialog debat).
2. **Berkas Log Resmi (Hanya 1 File TXT)**:  
   Seluruh transkrip debat mendalam 12 agen (*Explainable AI*), tabel matriks konsensus, dan **Tiket Rekomendasi Trading** (Aksi: BUY/SELL/HOLD, Jumlah Lot, Estimasi Biaya, Sisa Kas) tersimpan rapi ke:
   `results/live/live_{TICKER}_{YYYY-MM-DD}.txt`  
   *(Contoh: `results/live/live_BMRI_JK_2026-11-02.txt`)*

---

## Penjelasan Fitur & Arsitektur Sistem

### 1. Zero Look-Ahead Bias Engine
Pada mode backtest, data harga dan berita dipotong (*time-sliced*) secara ketat pada runtime. Agen pada tanggal $t$ hanya menerima harga $\le t$ dan berita dalam jendela $[t-7, t]$. Tidak ada kebocoran data masa depan.

### 2. Mekanisme Mingguan (Weekly Rebalancing)
Dewan 12 agen hanya menggelar sidang perundingan pada penutupan mingguan (Jumat), sementara hari Senin–Kamis portofolio berstatus *HOLD*. Mekanisme ini menyaring kebisingan pasar (*market noise*), mencegah *overtrading*, dan menghemat kuota LLM.

### 3. Struktur Hierarki 12 Agen (DAG LangGraph)
- **Layer 1 (Domain Analysts)**: *Fundamental Analyst*, *Macro Analyst*, *Sentiment Analyst*, dan *Technical Analyst*.
- **Layer 2 (Research Debate)**: *Bullish Researcher* vs *Bearish Researcher* dimoderasi oleh *Research Facilitator*.
- **Layer 3 (Risk Debate)**: *Aggressive Risk Analyst* vs *Conservative Risk Analyst* dimoderasi oleh *Risk Facilitator*.
- **Layer 4 (Execution)**: *Portfolio Manager* (alokasi taktis) dan *Trading Agent* (penerbit tiket transaksi).

### 4. Strategi Benchmark (Pembanding)
MAS disandingkan langsung dengan 3 strategi standar industri:
- **Buy and Hold (B&H)**: Alokasi 100% modal sejak hari pertama tanpa rebalancing.
- **SMA Crossover**: Mengikuti persilangan tren SMA-20 dan SMA-50.
- **MACD Signal**: Mengikuti persilangan momentum garis MACD dan Signal Line.

---

## Rangkuman Perintah Cepat (Cheatsheet)

```powershell
# 1. Update repositori dari GitHub (menarik cache berita terbaru)
git pull origin main

# 2. Build citra Docker
docker compose build

# 3. Jalankan Backtest (Periode >= 12 Oktober 2026)
docker compose run --rm backtest python main.py --mode backtest --ticker BMRI.JK --start 2026-10-12 --end 2026-10-30 --capital 100000000 --agents 12

# 4. Jalankan Mode Live (Keputusan Rekomendasi Hari Ini)
docker compose run --rm backtest python main.py --mode live --ticker BMRI.JK --capital 100000000 --agents 12
```
