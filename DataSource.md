# Penjelasan Alur Diagram Fase 1: Data Ingestion & Data Sources
## Arsitektur Pipeline Data Sistem Multi-Agent LLM Trading

---

## GAMBARAN UMUM

Diagram ini menggambarkan **arsitektur pipeline pengumpulan, pembersihan, penyimpanan, dan penyajian data** yang menjadi fondasi bagi seluruh sistem kecerdasan buatan Multi-Agent LLM Trading. Diagram terbagi ke dalam **6 lapisan fungsional** yang tersusun secara vertikal dari atas ke bawah, menggambarkan perjalanan data dari dunia luar (Internet) hingga siap dikonsumsi oleh 4 Agen Analis AI.

Tujuan utama dari diagram ini adalah membuktikan bahwa sistem memiliki **jalur data yang transparan, terstruktur, dan bebas dari kecurangan informasi masa depan (Look-Ahead Bias)** — sebuah syarat mutlak dalam penelitian perdagangan kuantitatif yang valid secara akademis.

---

## LAPISAN 1: SUMBER DATA EKSTERNAL (INTERNET)

Lapisan paling atas pada diagram menggambarkan **5 sumber data mentah dari internet** yang menjadi bahan bakar utama seluruh sistem. Kelima sumber ini terbagi menjadi dua kategori besar:

### Kategori A: Data Kualitatif (Teks Berita) — 3 Sumber RSS

1. **Google News RSS — Query: `'{ticker} saham'`**
   Sumber ini menarik berita-berita spesifik yang membahas emiten perbankan tertentu secara langsung. Misalnya, untuk ticker `BBRI.JK`, query yang dikirimkan ke Google News adalah `"BBRI saham"`. Hasil yang dikembalikan adalah kumpulan judul berita (*headline*) seperti: *"Investor Asing Borong Saham BBRI Rp 1,53 Triliun"*, *"Laba Bersih BBRI Naik 15% di Kuartal I"*, dan sejenisnya. Berita jenis ini menjadi bahan bacaan bagi **Sentiment Analyst** untuk menentukan suasana pasar terhadap saham tersebut.

2. **Google News RSS — Query: `'suku bunga BI OJK'`**
   Sumber ini menarik berita-berita makroekonomi nasional yang tidak spesifik pada satu emiten, melainkan berdampak pada keseluruhan sektor perbankan. Contoh topik yang ditarik: kebijakan suku bunga acuan Bank Indonesia (BI-7DRR), regulasi Otoritas Jasa Keuangan (OJK), tingkat inflasi, dan stabilitas nilai tukar Rupiah. Berita jenis ini menjadi bahan bacaan bagi **Macro Analyst**.

3. **CNBC Indonesia RSS — Stream: Market Feed**
   Sumber ini menarik berita umum pasar modal dan pergerakan bursa efek dari portal berita keuangan terkemuka di Indonesia. Topiknya mencakup dinamika Indeks Harga Saham Gabungan (IHSG), aksi korporasi emiten besar, serta sentimen investor global terhadap pasar berkembang (*emerging market*). Berita dari sumber ini turut melengkapi analisis kedua agen di atas (Sentiment dan Macro).

### Kategori B: Data Kuantitatif (Angka Numerik) — 2 Sumber Yahoo Finance API

4. **Yahoo Finance API — OHLCV Daily Historical**
   Sumber ini menarik deret waktu harga transaksi saham harian yang terdiri dari 5 kolom standar pasar modal: Open (Harga Pembukaan), High (Harga Tertinggi), Low (Harga Terendah), Close (Harga Penutupan), dan Volume (Jumlah Lembar Saham yang Ditransaksikan). Data ini merupakan bahan baku utama untuk menghitung rumus-rumus indikator teknikal seperti MACD, RSI, SMA, Bollinger Bands, dan KDJ.

5. **Yahoo Finance API — Info, Income Statement, Balance Sheet**
   Sumber ini menarik ringkasan kesehatan keuangan perusahaan, yaitu: rasio valuasi pasar (P/E Ratio, Price-to-Book, Dividend Yield), laporan laba rugi (pendapatan, beban, laba bersih), serta neraca keuangan (total aset, total liabilitas, ekuitas). Data ini bersifat kuartalan/tahunan dan relatif stabil dalam jangka menengah.

---

## ⟶ TRANSISI 1: Sumber Data Eksternal → Python Extraction & Pre-Processing

Panah dari Lapisan 1 menuju Lapisan 3 menggambarkan proses **penarikan data mentah dari internet ke dalam mesin pemrosesan Python**. Ketiga sumber RSS (Google News dan CNBC) mengalir ke kotak **NewsFetcher**, sedangkan kedua sumber Yahoo Finance mengalir ke kotak **YFinanceFetcher**. Pemisahan ini menunjukkan bahwa data kualitatif (teks) dan data kuantitatif (angka) diproses oleh modul Python yang berbeda, masing-masing dengan logika pembersihan yang sesuai dengan karakteristik datanya.

---

## LAPISAN 3: PYTHON EXTRACTION & PRE-PROCESSING

Lapisan ini merupakan **"dapur pembersihan data"** tempat data mentah dari internet divalidasi, dibersihkan, dan diformat sebelum disimpan ke penyimpanan lokal. Terdapat 2 modul utama:

### Modul A: NewsFetcher (`tools/news_fetcher.py`)
Modul ini memiliki dua mekanisme pembersihan kritis:
- **Negative Keyword Filter:** Menyaring dan membuang artikel berita yang bersifat edukasi pemula, promosi platform investasi, atau insiden kriminal lokal yang tidak memiliki nilai analisis finansial. Contoh kata kunci yang dibuang: *"cara beli"*, *"panduan pemula"*, *"pembobolan ATM"*. Dengan filter ini, hanya berita yang benar-benar memuat sinyal pergerakan pasar (kinerja laba, arus dana asing, kebijakan moneter) yang lolos masuk ke penyimpanan.
- **Incremental Append & Deduplication:** Saat menarik berita baru, modul ini tidak menimpa (*overwrite*) arsip berita lama. Sebaliknya, modul membaca arsip yang sudah ada, mengecek apakah judul berita sudah pernah tercatat menggunakan struktur data `set()`, lalu hanya menambahkan (*append*) artikel-artikel baru yang belum ada sebelumnya. Mekanisme ini menjamin arsip berita tumbuh secara organik dari hari ke hari tanpa duplikasi.

### Modul B: YFinanceFetcher (`tools/data_fetcher.py`)
Modul ini memiliki dua mekanisme teknis:
- **2-Year Buffer Calculation:** Saat pengguna meminta data mulai dari tanggal tertentu (misal `--start 2026-08-01`), modul ini secara otomatis menghitung mundur 2 tahun ke belakang (menjadi `2024-08-01`) sebagai titik awal pengambilan data. Buffer 2 tahun ini diperlukan agar indikator teknikal berperiode panjang (seperti SMA-200 yang membutuhkan 200 hari data historis) memiliki data yang cukup dan tidak menghasilkan nilai kosong (*NaN*) di awal simulasi.
- **Lowercase Columns:** Seluruh nama kolom hasil unduhan Yahoo Finance dinormalisasi menjadi huruf kecil (`open`, `high`, `low`, `close`, `volume`) agar kompatibel dengan pustaka komputasi indikator teknikal `stockstats` yang mensyaratkan penamaan kolom *lowercase*.

---

## ⟶ TRANSISI 2: Python Extraction → Otomasi Scheduler (Garis Putus-Putus)

Garis putus-putus (*dashed line*) yang menghubungkan Lapisan 3 ke Lapisan 2 menunjukkan bahwa **NewsFetcher dipanggil secara otomatis oleh skrip penjadwal harian**. Garis putus-putus (bukan garis solid) digunakan karena hubungan ini bersifat **pemanggilan terjadwal (*scheduled invocation*)**, bukan aliran data langsung. Artinya, NewsFetcher tidak berjalan terus-menerus, melainkan hanya dipanggil oleh skrip kolektor pada waktu yang sudah ditentukan.

---

## LAPISAN 2: OTOMASI SCHEDULER & PIPELINE HARIAN

Lapisan ini menggambarkan **rantai otomasi (*automation chain*)** yang memastikan pengumpulan berita berjalan setiap hari tanpa campur tangan manual dari pengguna. Rantai ini terdiri dari 4 komponen yang terhubung secara berurutan dari atas ke bawah:

### Komponen 1: Windows Task Scheduler (Daily 11:00 AM WIB / StartWhenAvailable)
Layanan bawaan sistem operasi Windows yang bertugas sebagai **"jam weker digital"**. Layanan ini disetel untuk memicu eksekusi pada pukul 11:00 Pagi WIB setiap hari. Fitur `StartWhenAvailable` memastikan bahwa jika laptop dalam keadaan mati atau tidur pada jam 11:00, Windows akan langsung menjalankan tugas tersebut begitu laptop dinyalakan kembali di waktu kapanpun setelahnya.

### Komponen 2: `run_collector.vbs` (Silent Headless Background)
File VBScript yang menjadi **jembatan eksekusi senyap**. File ini dipanggil oleh Task Scheduler dan bertugas menjalankan skrip batch (`run_collector.bat`) dengan parameter jendela tersembunyi (`0`). Hasilnya, seluruh proses pengumpulan berita berjalan sepenuhnya di latar belakang (*background*) tanpa memunculkan jendela hitam CMD yang mengganggu layar pengguna.

### Komponen 3: `daily_news_collector.py` (Iterasi 5 Bank: BBRI, BBCA, BMRI, BBNI, BRIS)
Skrip Python utama yang mengorkestrasi penarikan berita untuk kelima emiten bank secara berurutan. Skrip ini memanggil modul `NewsFetcher` sebanyak 5 kali (satu kali per bank), dan setiap pemanggilan akan menarik berita dari 3 sumber RSS, memfilter kata kunci sampah, menggabungkan dengan arsip lama, lalu menyimpan hasilnya ke folder cache masing-masing bank. Seluruh proses untuk 5 bank memakan waktu rata-rata hanya sekitar 5–8 detik.

### Komponen 4: `scripts/collector_log.txt` (Audit Trail & Metric Counter)
File teks log yang mencatat jejak audit setiap kali skrip kolektor dijalankan. Setiap entri log berisi stempel waktu eksekusi, jumlah berita baru yang berhasil ditambahkan, total akumulasi berita bersih per bank, serta status keberhasilan/kegagalan. File ini berfungsi sebagai **bukti dokumentasi operasional** bahwa pipeline data berjalan secara konsisten dan dapat diverifikasi oleh dosen penguji.

---

## ⟶ TRANSISI 3: Scheduler & Pre-Processing → Local Storage / Cache

Panah dari Lapisan 2 dan Lapisan 3 menuju Lapisan 4 menggambarkan proses **penyimpanan hasil akhir data yang sudah bersih ke dalam penyimpanan lokal (harddisk)**. Data yang keluar dari NewsFetcher disimpan sebagai `master_news.json`, data harga dari YFinanceFetcher disimpan sebagai `master_ohlcv.csv`, dan data fundamental disimpan sebagai `master_fundamentals.json`. Ketiga file ini diisolasi ke dalam folder terpisah per emiten (`data/cache/BBRI.JK/`, `data/cache/BBCA.JK/`, dst.) agar tidak tercampur antar emiten.

---

## LAPISAN 4: LOCAL STORAGE / CACHE (`data/cache/{ticker}/`)

Lapisan ini merepresentasikan **3 file master data** yang tersimpan di harddisk lokal komputer pengguna. Ketiga file ini menjadi satu-satunya sumber kebenaran (*single source of truth*) bagi seluruh proses simulasi *backtesting*:

1. **`master_news.json` (Cleaned Articles Archive)**
   Berisi arsip lengkap metadata berita yang telah melewati filter pembersihan. Setiap artikel hanya menyimpan 4 atribut: judul (*title*), tautan (*link*), tanggal publikasi (*published*), dan nama sumber (*source*). File ini tumbuh secara inkremental setiap hari sejalan dengan jadwal pengumpulan otomatis.

2. **`master_ohlcv.csv` (Time-Series Matrix)**
   Berisi matriks deret waktu harga saham harian dengan kolom: `date`, `open`, `high`, `low`, `close`, `volume`. Data ini mencakup rentang historis hingga 2 tahun ke belakang dari tanggal awal *backtest* untuk menjamin kecukupan kalkulasi indikator teknikal jangka panjang.

3. **`master_fundamentals.json` (Valuation & Statements)**
   Berisi snapshot rasio valuasi terkini (P/E, P/B, Dividend Yield) serta ringkasan laporan laba rugi dan neraca keuangan kuartalan/tahunan terakhir. Data ini bersifat relatif stabil dalam satu kuartal.

---

## ⟶ TRANSISI 4: Local Storage → Runtime Backtesting / Time-Slicing

Panah dari Lapisan 4 menuju Lapisan 5 menggambarkan proses **pemuatan (*loading*) ketiga file master dari harddisk ke dalam memori komputer (RAM)**. Saat pengguna menjalankan perintah *backtest*, mesin Backtester Engine membaca seluruh isi ketiga file master sekaligus ke dalam variabel Python di memori. Pemuatan ini hanya terjadi **satu kali di awal eksekusi** (*one-shot loading*), sehingga iterasi mingguan berikutnya tidak perlu membaca ulang dari harddisk dan menjadi sangat cepat.

---

## LAPISAN 5: RUNTIME BACKTESTING / TIME-SLICING

Lapisan ini merupakan **jantung pencegahan kecurangan data (*Look-Ahead Bias Prevention*)** dan menjadi komponen paling krusial secara akademis dalam arsitektur ini. Lapisan ini terdiri dari 3 komponen:

### Komponen 1: Backtester Engine (`orchestration/backtester.py`) — Weekly Step (Friday Loop)
Mesin simulasi utama yang menjalankan perulangan mingguan. Pada setiap iterasi, mesin ini mensimulasikan keputusan investasi di hari Jumat penutupan bursa. Mesin bergerak maju dari minggu pertama hingga minggu terakhir dalam rentang tanggal `--start` sampai `--end` yang ditentukan pengguna.

### Komponen 2: Time-Slicing OHLCV ($t \le \text{Date}$) — Compute Technical Indicators
Pada setiap hari Jumat simulasi, mesin memotong (*slice*) deret waktu harga saham sehingga **hanya data historis hingga hari Jumat tersebut** yang digunakan untuk menghitung indikator teknikal. Rumus pemotongan: seluruh baris data di mana tanggal baris ($t$) kurang dari atau sama dengan tanggal simulasi ($\text{Date}$). Data harga setelah hari Jumat tersebut (masa depan) secara otomatis dibuang dari memori perhitungan.

### Komponen 3: Time-Slicing News ($\text{Date} - 7 \le t_{\text{published}} \le \text{Date}$) — Zero Look-Ahead Bias
Pada setiap hari Jumat simulasi, mesin memotong arsip berita sehingga **hanya berita yang terbit dalam kurun 7 hari terakhir menjelang hari Jumat tersebut** yang diberikan kepada agen AI. Berita yang terbit setelah hari Jumat (masa depan) dibuang sepenuhnya. Berita yang terbit lebih dari 7 hari sebelumnya (sudah basi) juga dibuang agar analisis sentimen tetap relevan dan terkini.

---

## ⟶ TRANSISI 5: Time-Slicing → Konsumsi Agen AI

Panah dari Lapisan 5 menuju Lapisan 6 menggambarkan **penyerahan data yang telah diiris secara temporal kepada 4 Agen Analis AI**. Data yang sampai di tangan agen sudah dalam kondisi bersih, relevan secara waktu, dan bebas dari informasi masa depan. Setiap agen hanya menerima jenis data yang sesuai dengan spesialisasinya — tidak ada agen yang membaca data di luar kewenangannya.

---

## LAPISAN 6: KONSUMSI AGEN AI (FASE 5)

Lapisan terakhir pada diagram menggambarkan **4 Agen Analis Spesialis** yang menjadi konsumen akhir (*end consumer*) dari seluruh pipeline data Fase 1. Keempat agen ini bekerja secara paralel dan masing-masing membaca jenis data yang berbeda:

1. **Technical Analyst (Membaca RSI, MACD, SMA)**
   Menerima hasil perhitungan indikator teknikal dari **Time-Slicing OHLCV**. Agen ini menganalisis momentum harga, tren rata-rata bergerak, dan kondisi jenuh beli/jual berdasarkan sinyal-sinyal matematika. Agen ini tidak pernah membaca berita; tugasnya murni berbasis angka numerik.

2. **Sentiment Analyst (Membaca Berita Spesifik Ticker)**
   Menerima kumpulan judul berita spesifik emiten yang telah disaring oleh **Time-Slicing News**. Agen ini mengekstrak sentimen pasar jangka pendek (apakah suasana terhadap saham tersebut positif, negatif, atau netral) berdasarkan headline berita yang terbit dalam 7 hari terakhir.

3. **Macro Analyst (Membaca Berita Suku Bunga & OJK)**
   Menerima kumpulan judul berita makroekonomi yang telah disaring oleh **Time-Slicing News**. Agen ini mengevaluasi dampak kebijakan suku bunga Bank Indonesia, regulasi OJK, dan kondisi ekonomi global terhadap prospek margin bunga bersih sektor perbankan.

4. **Fundamental Analyst (Membaca P/E, P/B, ROE)**
   Menerima data valuasi dan laporan keuangan dari **`master_fundamentals.json`** secara langsung (tanpa melewati Time-Slicing, karena data fundamental bersifat kuartalan dan tidak berubah setiap hari). Agen ini menilai apakah harga saham saat ini wajar (*fairly valued*), murah (*undervalued*), atau mahal (*overvalued*) berdasarkan metrik kesehatan keuangan perusahaan.

---

## KESIMPULAN ALUR KESELURUHAN

```
INTERNET (5 Sumber Data)
        ↓
PYTHON PRE-PROCESSING (Filter Noise + Buffer 2 Tahun)
        ↓                         ↑
LOCAL CACHE (3 File Master)   ←   SCHEDULER HARIAN (Jam 11:00 WIB)
        ↓
BACKTESTER ENGINE (Loop Mingguan Hari Jumat)
        ↓
TIME-SLICING (Potong Data ≤ Tanggal Simulasi)
        ↓
4 AGEN ANALIS AI (Paralel: Technical, Sentiment, Macro, Fundamental)
```

Setiap lapisan dalam diagram ini memiliki peran yang tidak dapat dilewati (*non-bypassable*). Data mentah dari internet tidak pernah langsung menyentuh agen AI tanpa melewati proses pembersihan dan pemotongan waktu terlebih dahulu. Arsitektur berlapis ini menjamin bahwa keputusan yang dihasilkan oleh 12 agen AI di Fase 5 didasarkan pada data yang bersih, relevan, dan valid secara temporal.
