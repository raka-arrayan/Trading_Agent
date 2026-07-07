# Dokumentasi Arsitektur Multi-Agent System (MAS) untuk Trading Saham

Dokumen ini memuat struktur direktori, penjelasan peran dari setiap komponen file, dan alur mekanisme (dari input pengguna hingga keputusan *trading* akhir) dari arsitektur *Multi-Agent System* yang diusulkan untuk sistem pendukung keputusan investasi saham pada sektor perbankan di IHSG.

---

## 1. Struktur Folder & File

```text
.
├── main.py                     # Entry point (Program utama) untuk menjalankan Backtesting
├── PROJECT_STRUCTURE.md        # File dokumentasi struktur proyek (file ini)
├── data/
│   └── cache/                  # Direktori penyimpanan data historis lokal berformat JSON/CSV
├── config/                     # Direktori konfigurasi dan parameter statis sistem
│   ├── glossary.py             # Kamus istilah finansial pasar modal Indonesia (Indonesian-English)
│   ├── llm_config.py           # Konfigurasi koneksi ke model LLM (Ollama, Gemini, Groq, dll.)
│   └── prompts/                # Direktori pemisahan instruksi (System Prompts) untuk setiap agen
│       ├── analyst_prompts.py  # Prompt untuk 4 analis awal (Fundamental, Teknikal, Sentimen, Makro)
│       ├── research_prompts.py # Prompt untuk agen periset (Bullish, Bearish, Facilitator)
│       ├── risk_prompts.py     # Prompt untuk agen risiko (Aggressive, Conservative, Facilitator)
│       └── execution_prompts.py# Prompt untuk manajer portofolio dan Trading Agent akhir
├── orchestration/              # Direktori jantung orkestrasi (pengendali alur agen)
│   ├── state.py                # Definisi struktur data tunggal (TradingState) yang memuat seluruh konteks
│   ├── graph.py                # Implementasi LangGraph (StateGraph) yang mendefinisikan rute dan eksekusi ke-13 agen
│   └── backtester.py           # Mesin simulasi day-by-day yang mengatur iterasi waktu dan eksekusi graf
├── agents/                     # Direktori implementasi fungsi logika masing-masing agen AI
│   ├── analysts.py             # Implementasi node LLM untuk 4 agen Analis Dasar
│   ├── researchers.py          # Implementasi node LLM untuk agen Debat Riset
│   ├── risk_management.py      # Implementasi node LLM untuk agen Debat Risiko
│   └── execution.py            # Implementasi node LLM untuk Portfolio Manager dan Trading Agent (dengan JSON Parser)
├── tools/                      # Direktori fungsionalitas pendukung (API Call, Kalkulasi)
│   ├── cache_manager.py        # Pengelola penyimpanan/pengambilan cache lokal untuk mencegah look-ahead bias
│   ├── data_fetcher.py         # Pengunduh data pasar (OHLCV & Fundamental) dari yfinance
│   ├── indicator_calculator.py # Penghitung indikator teknikal murni (MACD, RSI, SMA) menggunakan stockstats
│   └── news_fetcher.py         # Scraper dan pengumpul data berita dari feed RSS eksternal
├── utils/                      # Direktori modul utilitas untuk evaluasi akhir
│   ├── metrics.py              # Penghitung metrik finansial (Cumulative Return, Sharpe Ratio, Max Drawdown, Win Rate)
│   └── visualizer.py           # Pembuat grafik perbandingan performa portofolio (matplotlib)
├── scripts/                    # Direktori skrip uji coba parsial (Unit Test)
│   ├── test_pipeline.py        # Skrip uji coba untuk memastikan fungsionalitas data di folder tools/ berjalan
│   └── test_agents.py          # Skrip uji coba untuk memeriksa injeksi konteks ke agen LLM (tanpa menjalankan seluruh sistem)
└── results/                    # Direktori hasil eksekusi backtester (CSV trades, CSV NAV harian, dan Plot .png)
```

---

## 2. Penjelasan Detail Komponen

Pemecahan file ke dalam modul-modul ini didesain menggunakan prinsip *Separation of Concerns* (pemisahan tanggung jawab) yang lazim digunakan dalam rekayasa perangkat lunak berskala besar. Hal ini memudahkan pemeliharaan kode (maintenance), lokalisasi *bug*, dan iterasi *prompt engineering* tanpa merusak logika aliran data.

### `config/` (Konfigurasi & Prompts)
Fungsi direktori ini adalah memisahkan parameter dinamis LLM dari kode murni Python.
- **`glossary.py`**: Berfungsi sebagai injeksi pemahaman konteks lokal (*local knowledge base*). Mengkonversi terminologi lokal (seperti *IHSG*, *NPL*, *Laba Bersih*) agar LLM global tidak berhalusinasi.
- **`llm_config.py`**: Abstraksi *factory* yang mengelola inisiasi LLM. Bertujuan agar pergantian *provider* model (dari Ollama lokal ke Gemini API) hanya perlu diubah di satu file ini saja.
- **`prompts/*.py`**: Seluruh teks instruksi LLM (dalam bahasa Inggris agar limit token optimal) dipisah ke modul ini agar *tuning* perilaku agen dapat dilakukan tanpa menyentuh logika eksekusinya.

### `orchestration/` (Orkestrasi)
Jantung koordinasi logika sistem. 
- **`state.py`**: Mendefinisikan *State Schema* (kumpulan variabel mutlak) yang dibawa berputar-putar melintasi agen-agen. Ini adalah satu-satunya "ingatan" yang dimiliki oleh arsitektur ini saat sedang berjalan.
- **`graph.py`**: Peta jalan (*roadmap*). Modul ini memanfaatkan `LangGraph` untuk mengarahkan alur (Misal: setelah 4 Analis selesai secara paralel, maka hasilnya diarahkan ke Periset).
- **`backtester.py`**: Skrip ini bertindak sebagai manajer waktu (*time-keeper*). Karena *Multi-Agent* tidak punya konsep waktu harian, modul inilah yang memasok data "tanggal A", menyuruh graf berjalan, mencatat laba rugi hari A, kemudian berlanjut ke "tanggal B", dan seterusnya.

### `agents/` (Implementasi Logika Agen)
Direktori ini menjembatani perpindahan dari modul abstraksi ke pemanggilan API Model yang sesungguhnya.
- File-file di dalamnya (`analysts.py`, `researchers.py`, dll.) bertugas menarik data spesifik yang diperlukan dari *State*, memaketkannya bersama instruksi (*Prompt*), mengirimnya ke LLM, mengekstrak respons teksnya, dan menyimpannya kembali ke *State*.
- File **`execution.py`** sangat krusial karena ia mengimplementasikan `JsonOutputParser` yang menggunakan reguler ekspresi (Regex) berlapis untuk "memaksa" LLM memberikan jawaban akhir dalam bentuk objek JSON absolut (Tindakan, Kuantitas, Tingkat Kepercayaan) dan bukan tulisan naratif biasa.

### `tools/` & `utils/` (Infrastruktur Pendukung)
- **`tools/`**: Adalah mata dan telinga agen. Tempat kode-kode non-AI bekerja mengambil nilai saham dan berita secara independen (Data Pipeline). Penggunaan `cache_manager.py` didesain untuk menjamin *reproducibility* riset tesis Anda secara akademis dan menghilangkan kecurangan penglihatan masa depan (*look-ahead bias*).
- **`utils/`**: Berjalan setelah siklus simulasi selesai. Fungsinya sebagai penganalisis matematis kinerja *bot trading* itu sendiri (menerbitkan nilai validasi objektif semacam rasio Sharpe).

---

## 3. Mekanisme Sistem (Alur Input ke Output)

Bagaimana sistem memproses perintah pengguna hingga mencetak hasil perdagangan? Alurnya dirancang berlapis-lapis layaknya firma investasi dunia nyata.

### Langkah 1: Inisialisasi dan Injeksi Waktu (User Input)
1. Pengguna menjalankan **`main.py`** dan memberikan argumen (misal: analisis BBCA.JK dari 1 Januari - 31 Januari).
2. **`main.py`** membangun mesin **`backtester.py`**, menyiapkan portofolio virtual senilai Rp 100 Juta, dan meloloskan jadwal kalender harian untuk dievaluasi hari demi hari.
3. Pada hari T, **`backtester.py`** menyedot data dari direktori lokal (`data/cache/`) yang disiapkan dari *Data Pipeline*. Data mentah berupa harga, indikator teknikal (RSI, MACD), berita hari ini, dan laporan fundamental disuntikkan ke dalam kanvas ingatan universal bernama **`TradingState`** (`state.py`).

### Langkah 2: Evaluasi Paralel (Para Analis)
1. **`TradingState`** dilempar ke lintasan utama dalam **`graph.py`**.
2. Graf akan memicu 4 agen spesialis pertama yang berada di **`agents/analysts.py`**:
   - **Fundamental Analyst**: Mengevaluasi P/E Ratio dan P/B Ratio perusahaan.
   - **Technical Analyst**: Menilai indikator tren momentum saham murni dari kurva angka.
   - **Sentiment Analyst**: Membaca sentimen tekstual pada berita (*news*).
   - **Macro Analyst**: Membaca konteks berita secara gambaran besar.
3. Keempatnya mengkaji data secara bersamaan (paralel) dan menuliskan rekomendasi maksimal 3 kalimatnya kembali ke dalam `TradingState`.

### Langkah 3: Mekanisme Debat Sintetis (Periset & Risiko)
1. Narasi 4 Analis tadi mengalir masuk ke agen periset (**`agents/researchers.py`**). **Bullish Researcher** diminta berargumen ekstrem positif (*mengapa kita harus BUY*), sementara **Bearish Researcher** berargumen ekstrem negatif (*mengapa kita harus SELL*). 
2. Sebuah **Research Facilitator** merangkum perdebatan ini menjadi sebuah resolusi *consensus* obyektif.
3. Hasil riset tersebut mengalir ke bagian departemen manajemen risiko (**`agents/risk_management.py`**). Terjadi perseteruan serupa: **Aggressive Risk Analyst** menuntut perolehan kapital cepat, sedangkan **Conservative Risk Analyst** menyarankan penjagaan nilai (proteksi aset). Mereka mendebatkan posisi portofolio yang ada dan merangkumnya lewat **Risk Facilitator**.

### Langkah 4: Sintesis Keputusan Akhir (Eksekusi)
1. Laporan yang sudah tertata matang dari fasilitator riset dan fasilitator risiko, beserta laporan 4 analis pertama disodorkan ke **Portfolio Manager** (berada di **`agents/execution.py`**). Ia memadukan pandangan *return* dan pandangan *risk* untuk menyusun draf instruksi perdagangan yang holistik.
2. Draf tersebut diserahkan kepada agen ke-13: **Trading Agent** di file yang sama. Tugasnya hanyalah mengonversi instruksi kualitatif tadi menjadi perintah mesin secara matematis kuantitatif. 
3. *Trading Agent* menggunakan *JSON output parser* yang mengikat ketat instruksinya, memuntahkan respons JSON murni yang divalidasi, misalnya `{"action": "BUY", "quantity": 100, "confidence": 0.8}`.

### Langkah 5: Kalkulasi Hasil dan Iterasi (Output)
1. Aksi (BUY/SELL/HOLD) yang berupa objek JSON di atas ditangkap kembali oleh **`backtester.py`**.
2. Mesin waktu tersebut merekam kalkulasi potongan biaya *broker fee*, menarik uang tunai, menempatkan saham ke inventaris portofolio pengguna, dan memperbarui rekam jejak *Net Asset Value* (NAV) akhir hari itu.
3. Siklus ini diulang terus-menerus hingga seluruh tanggal simulasi habis.
4. Pada akhir siklus, algoritma akan masuk ke ranah **`utils/metrics.py`** dan **`utils/visualizer.py`** yang membandingkan performa robot kecerdasan buatan ini dengan investor pasif biasa (*Buy-and-Hold*) menjadi bagan visual yang terstruktur rapi.
