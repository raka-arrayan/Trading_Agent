# Data Ingestion & Data Sources
### Arsitektur Pipeline Data Sistem Multi-Agent LLM Trading

---

## 1. PEMILIHAN ALAMIAH & CAKUPAN BANK (INVESTMENT UNIVERSE)

Dalam perancangan sistem perdagangan kuantitatif dan multi-agen berbasis LLM untuk pasar modal Indonesia, penentuan cakupan semesta aset (*asset universe*) tidak dilakukan secara acak, melainkan menggunakan kriteria seleksi yang terukur secara kuantitatif dan teknis.

### A. Daftar Bank Terpilih (Universe Portfolio)

| No | Simbol Ticker | Nama Emiten | Klasifikasi Modal | Kapitalisasi Pasar (Kisaran) |
|:--:|:---|:---|:---|:---|
| 1 | **BBRI.JK** | PT Bank Rakyat Indonesia (Persero) Tbk | KBMI 4 (BUMN) | ± Rp 750 – 850 Triliun |
| 2 | **BBCA.JK** | PT Bank Central Asia Tbk | KBMI 4 (Swasta) | ± Rp 1.150 – 1.300 Triliun |
| 3 | **BMRI.JK** | PT Bank Mandiri (Persero) Tbk | KBMI 4 (BUMN) | ± Rp 600 – 700 Triliun |
| 4 | **BBNI.JK** | PT Bank Negara Indonesia (Persero) Tbk | KBMI 4 (BUMN) | ± Rp 180 – 220 Triliun |
| 5 | **BRIS.JK** | PT Bank Syariah Indonesia Tbk | KBMI 3 (BUMN Syariah) | ± Rp 110 – 130 Triliun |

---

### B. Rasionalisasi Kriteria (Teknis & Kuantitatif)

```text
                    KRITERIA SELEKSI UNIVERSE PERBANKAN
┌───────────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
│     Likuiditas &      │   │     Kepatuhan &        │   │    Densitas Berita     │
│   Kapitalisasi Pasar  │   │ Transparansi Finansial │   │   & Liputan Media      │
│  (Top 5 Sektor Bank)  │   │  (Audit BEI & OJK)     │   │   (Google & CNBC)      │
└───────────────────────┘   └────────────────────────┘   └────────────────────────┘
```

* **Dominasi Kapitalisasi Pasar (*Market Capitalization Dominance*)**
  * Sektor perbankan merupakan jangkar utama Indeks Harga Saham Gabungan (IHSG), menyumbang >30% dari total bobot IHSG.
  * Kelima bank di atas mewakili >60% total aset industri perbankan nasional. Pergerakan kelima emiten ini merefleksikan sentimen makroekonomi domestik secara langsung.

* **Likuiditas Harian & Low Slippage**
  * Nilai transaksi harian (*Average Daily Turnover*) rata-rata di atas Rp 100 Miliar per hari.
  * Likuiditas yang tebal meminimalkan risiko *market impact* dan *slippage*, menjamin asumsi biaya transaksi (*broker fee* 0,2%) pada *backtester* tetap valid dan realistis.

* **Kelengkapan & Integritas Laporan Keuangan (OJK & BEI)**
  * Sebagai emiten tier-tertinggi, kelima bank memiliki kepatuhan rilis laporan keuangan kuartalan (Q1, Q2, Q3) dan tahunan teraudit (*Audited Annual Report*) yang konsisten tanpa keterlambatan sanksi bursa.
  * Hal ini menjamin API data provider (Yahoo Finance) memiliki data fundamental yang bersih tanpa nilai *null* ekstrem.

* **Kepadatan Liputan Berita (*News Coverage Density*)**
  * Agen LLM (*Sentiment Analyst* dan *Macro Analyst*) memerlukan asupan teks berita yang konstan. Bank-bank ini memiliki liputan media tertinggi setiap hari di portal berita nasional (kebijakan dividen, restrukturisasi kredit, suku bunga acuan BI-Rate, hingga aksi korporasi).

* **Divergensi Model Bisnis (*Cross-Segment Evaluation*)**
  * **BBRI:** Fokus kredit Mikro & UMKM (sensitif terhadap daya beli akar rumput dan bansos).
  * **BBCA:** Bank transaksional swasta dengan rasio CASA (*Current Account Saving Account*) tertinggi dan NPL terendah.
  * **BMRI:** Portofolio kredit korporasi dan infrastruktur terbesar.
  * **BBNI:** Perbankan internasional dan sindikasi luar negeri.
  * **BRIS:** Representasi perbankan syariah terbesar (non-bunga / bagi hasil), memberikan dimensi riset *novelty* terhadap performa agen LLM.

---


# Penjelasan Alur Diagram Fase 1: Data Ingestion & Data Sources
## Arsitektur Pipeline Data Sistem Multi-Agent LLM Trading (Cloud Automation & Containerized Edition)

---

## GAMBARAN UMUM

Diagram ini menggambarkan **arsitektur pipeline pengumpulan, pembersihan, penyimpanan, dan penyajian data** yang menjadi fondasi bagi seluruh sistem kecerdasan buatan Multi-Agent LLM Trading. Diagram terbagi ke dalam **6 lapisan fungsional** yang tersusun secara terstruktur, menggambarkan perjalanan data dari dunia luar (Internet) hingga siap dikonsumsi oleh 4 Agen Analis AI.

Tujuan utama dari diagram ini adalah membuktikan bahwa sistem memiliki:
1. **Jalur data yang transparan, terstruktur, dan bebas dari kecurangan informasi masa depan (*Zero Look-Ahead Bias*)** — sebuah syarat mutlak dalam penelitian perdagangan kuantitatif yang valid secara akademis.
2. **Kemandirian operasional berbasis cloud (*Cloud-Native High Availability*)** menggunakan **GitHub Actions** dan **Docker**, sehingga proses penarikan data harian berjalan secara konsisten setiap hari tanpa bergantung pada perangkat laptop peneliti.

---

## LAPISAN 1: SUMBER DATA EKSTERNAL (INTERNET)

Lapisan paling atas pada diagram menggambarkan **5 sumber data mentah dari internet** yang menjadi bahan bakar utama seluruh sistem. Kelima sumber ini terbagi menjadi dua kategori besar:

### Kategori A: Data Kualitatif (Teks Berita) — 3 Sumber RSS

1. **Google News RSS — Query: `'{ticker} saham'`**
   Sumber ini menarik berita-berita spesifik yang membahas emiten perbankan tertentu secara langsung. Misalnya, untuk ticker `BBRI.JK`, query yang dikirimkan ke Google News adalah `"BBRI saham"`. Hasil yang dikembalikan adalah kumpulan judul berita (*headline*) seperti: *"Investor Asing Borong Saham BBRI Rp 1,53 Triliun"*, *"Laba Bersih BBRI Naik 15% di Kuartal I"*, dan sejenisnya. Berita jenis ini menjadi bahan bacaan bagi **Sentiment Analyst** untuk menentukan suasana pasar terhadap saham tersebut.

2. **Google News RSS — Query: `'suku bunga BI OJK'`**
   Sumber ini menarik berita-berita makroekonomi nasional yang tidak spesifik pada satu emiten, melainkan berdampak pada keseluruhan sektor perbankan. Contoh topik yang ditarik: kebijakan suku bunga acuan Bank Indonesia (BI-Rate), regulasi Otoritas Jasa Keuangan (OJK), tingkat inflasi, dan stabilitas nilai tukar Rupiah. Berita jenis ini menjadi bahan bacaan bagi **Macro Analyst**.

3. **CNBC Indonesia RSS — Stream: Market Feed**
   Sumber ini menarik berita umum pasar modal dan pergerakan bursa efek dari portal berita keuangan terkemuka di Indonesia. Topiknya mencakup dinamika Indeks Harga Saham Gabungan (IHSG), aksi korporasi emiten besar, serta sentimen investor global terhadap pasar berkembang (*emerging market*). Berita dari sumber ini turut melengkapi analisis kedua agen di atas (Sentiment dan Macro).

### Kategori B: Data Kuantitatif (Angka Numerik) — 2 Sumber Yahoo Finance API

4. **Yahoo Finance API — OHLCV Daily Historical**
   Sumber ini menarik deret waktu harga transaksi saham harian yang terdiri dari 5 kolom standar pasar modal: Open (Harga Pembukaan), High (Harga Tertinggi), Low (Harga Terendah), Close (Harga Penutupan), dan Volume (Jumlah Lembar Saham yang Ditransaksikan). Data ini merupakan bahan baku utama untuk menghitung rumus-rumus indikator teknikal seperti MACD, RSI, SMA, Bollinger Bands, dan KDJ.

5. **Yahoo Finance API — Info, Income Statement, Balance Sheet**
   Sumber ini menarik ringkasan kesehatan keuangan perusahaan, yaitu: rasio valuasi pasar (P/E Ratio, Price-to-Book, Dividend Yield), laporan laba rugi (pendapatan, beban, laba bersih), serta neraca keuangan (total aset, total liabilitas, ekuitas). Data ini bersifat kuartalan/tahunan dan relatif stabil dalam jangka menengah.

---

## LAPISAN 2: OTOMASI SCHEDULER & PIPELINE HARIAN (CLOUD-NATIVE AUTOMATION)

Lapisan di sebelah kiri menggambarkan **rantai otomasi modern (*DevOps / CI/CD Automation Chain*)** yang menjamin pengumpulan data berita harian berlangsung secara otomatis, konsisten, dan bebas hambatan perangkat fisik. Rantai ini terdiri dari 5 komponen yang saling terhubung:

### Komponen 1: GitHub Actions Workflow (`cron: '0 4 * * *' / 11:00 AM WIB`)
Layanan komputasi awan (*serverless runner*) milik GitHub yang bertindak sebagai pemicu waktu utama. Sesuai konfigurasi cron `0 4 * * *` (pukul 04:00 UTC atau 11:00 WIB), server GitHub di cloud secara otomatis menyala setiap hari tanpa memerlukan intervensi manusia dan tanpa memerlukan laptop peneliti dalam keadaan hidup.

### Komponen 2: Docker Container (`python:3.12-slim` Cross-Platform)
Lingkungan komputasi terisolasi yang membungkus seluruh sistem (Python 3.12, dependensi `feedparser`, `beautifulsoup4`, dan konfigurasi zona waktu `Asia/Jakarta`). Penggunaan Docker menjamin portabilitas penuh (*cross-platform consistency*), sehingga kode berjalan dengan perilaku yang identik baik di server cloud Linux, Windows, maupun macOS tanpa masalah ketergantungan library.

### Komponen 3: `daily_news_collector.py` (Iterasi 5 Bank: BBRI, BBCA, BMRI, BBNI, BRIS)
Skrip orkestrator utama yang dieksekusi di dalam kontainer Docker. Skrip ini mengendalikan urutan pemrosesan berita untuk 5 bank terkemuka Indonesia secara berurutan.

### Komponen 4: `scripts/collector_log.txt` (Audit Trail & Metric Counter)
Pencatatan riwayat audit eksekusi yang mendokumentasikan stempel waktu, status keberhasilan per bank, jumlah artikel baru yang ditambahkan, serta total berita bersih yang tersimpan.

### Komponen 5: GitHub Remote Repository (Auto-Commit & Push Updated Cache)
Setelah data 5 bank selesai diperbarui dan divalidasi, bot GitHub Actions secara otomatis melakukan *commit* dan *push* (`chore(data): auto-update master news cache via cloud container [skip ci]`) kembali ke repositori utama. Peneliti cukup menjalankan perintah `git pull` kapan saja di komputer lokal untuk menyinkronkan data terbaru.

---

## ⟶ TRANSISI PEMANGGILAN TERJADWAL & SINKRONISASI

1. **Garis Putus-Putus (*Pemanggilan Terjadwal*):**
   Panah dari `daily_news_collector.py` mengarah ke kotak **`NewsFetcher`** di Lapisan 3. Ini mencerminkan hubungan pemanggilan fungsi (*function invocation*), di mana skrip kolektor bertindak sebagai penggerak yang memanggil fungsi pembersih dan penarik data `news_fetcher.fetch_all_news(ticker)`.
2. **Garis Putus-Putus (*Git Pull*):**
   Panah dari `GitHub Remote Repository` mengarah ke Lapisan 4 `master_news.json`. Ini menunjukkan jalur sinkronisasi data dari cloud ke penyimpanan lokal peneliti.

---

## LAPISAN 3: PYTHON EXTRACTION & PRE-PROCESSING

Lapisan ini merupakan **"dapur pembersihan data"** tempat data mentah dari internet divalidasi, disaring, dan distandarisasi sebelum disimpan:

### Modul A: NewsFetcher (`tools/news_fetcher.py`)
Modul ini memiliki empat mekanisme pembersihan cerdas:
- **Negative Keyword Filter:** Membuang artikel non-finansial seperti edukasi pemula, promosi pinjaman online, atau kriminalitas lokal (misal: *"cara daftar"*, *"panduan pemula"*, *"pembobolan ATM"*).
- **HTML Image Tag Stripper:** Menghapus tag HTML gambar (`<img src="...">`) yang kerap menyertai RSS berita (seperti dari CNBC Indonesia / Detik Network), mengekstrak kalimat pengantar murni yang kaya informasi.
- **Google Boilerplate Filter:** Mendeteksi dan mengosongkan slogan baku bawaan Google News (*"Comprehensive, up-to-date news coverage..."*) agar tidak menjadi kebisingan (*noise*) bagi analisis AI.
- **Incremental Append & Deduplication:** Memeriksa kesamaan judul menggunakan struktur data *hash-set* sehingga hanya berita baru yang ditambahkan tanpa menduplikasi arsip lama.

### Modul B: YFinanceFetcher (`tools/data_fetcher.py`)
Modul ini memiliki dua mekanisme teknis:
- **2-Year Buffer Calculation:** Menarik data mundur 2 tahun sebelum tanggal awal simulasi agar kalkulasi indikator jangka panjang (misal SMA-200) memiliki data historis yang memadai tanpa menghasilkan nilai kosong (*NaN*).
- **Lowercase Columns:** Menormalisasi nama kolom menjadi huruf kecil (`open`, `high`, `low`, `close`, `volume`) sesuai standar pustaka `stockstats`.

---

## LAPISAN 4: STORAGE / CACHE (`data/cache/{ticker}/`)

Lapisan ini merepresentasikan **3 file master data** per emiten perbankan yang menjadi satu-satunya sumber kebenaran (*single source of truth*) dalam simulasi:

1. **`master_news.json` (Cleaned Articles Archive + Description):**
   Menyimpan arsip metadata berita yang telah bersih dengan atribut: `title`, `link`, `published`, `source`, dan `description` (ringkasan informatif bebas HTML dan bebas boilerplate).
2. **`master_ohlcv.csv` (Time-Series Matrix):**
   Matriks deret waktu harga transaksi saham harian.
3. **`master_fundamentals.json` (Valuation & Statements):**
   Snapshot rasio valuasi fundamental dan laporan keuangan kuartalan/tahunan.

---

## LAPISAN 5: RUNTIME BACKTESTING / TIME-SLICING

Lapisan ini bertugas menjamin validitas metodologis simulasi melalui pencegahan kecurangan data masa depan (**Zero Look-Ahead Bias**):

1. **Backtester Engine (`orchestration/backtester.py`) — Weekly Step (Friday Loop):**
   Menjalankan simulasi perdagangan berbasis langkah mingguan pada setiap hari Jumat penutupan bursa.
2. **Time-Slicing OHLCV ($t \le \text{Date}$):**
   Hanya memotong data harga hingga hari Jumat simulasi untuk menghitung indikator teknikal. Data harga di masa depan dipotong dari memori.
3. **Time-Slicing News ($\text{Date} - 7 \le t_{\text{published}} \le \text{Date}$):**
   Hanya menyajikan berita yang terbit dalam jendela 7 hari terakhir sebelum hari Jumat simulasi. Format yang diserahkan ke agen AI mencakup **Title + Clean Description**, memberikan konteks sentimen yang mendalam dan relevan.

---

## LAPISAN 6: KONSUMSI AGEN AI (FASE 5)

Lapisan akhir menampilkan 4 Agen Analis Spesialis yang menerima data hasil irisan waktu secara paralel:

1. **Sentiment Analyst (Membaca Judul + Deskripsi Berita Ticker):**
   Menganalisis sentimen mikro jangka pendek emiten berdasarkan kombinasi judul dan ringkasan berita yang telah dibersihkan.
2. **Macro Analyst (Membaca Berita Suku Bunga & OJK):**
   Mengevaluasi dinamika makroekonomi perbankan (kebijakan BI-Rate, regulasi OJK, inflasi).
3. **Technical Analyst (Membaca RSI, MACD, SMA):**
   Menganalisis tren pergerakan harga dan momentum berbasis sinyal matematika dari data OHLCV.
4. **Fundamental Analyst (Membaca P/E, P/B, ROE):**
   Mengevaluasi kelayakan valuasi harga saham berdasarkan laporan keuangan perusahaan terkini.

---

## KESIMPULAN ALUR KESELURUHAN

```
SUMBER EKSTERNAL (Internet: RSS & Yahoo Finance)
         │
         ▼
[GitHub Actions + Docker Cloud Ingestion (Jam 11:00 WIB)]
         │ (Memanggil tools/news_fetcher.py)
         ▼
PRE-PROCESSING (HTML Stripping + Slogan Filter + Buffer 2 Tahun)
         │
         ▼
STORAGE / CACHE (master_news.json, master_ohlcv.csv, master_fundamentals.json)
         │
         ▼
BACKTESTER ENGINE (Friday Loop & Zero Look-Ahead Time-Slicing)
         │
         ▼
4 AGEN ANALIS AI (Technical, Sentiment, Macro, Fundamental)
```
