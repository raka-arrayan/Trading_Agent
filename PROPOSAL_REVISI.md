# PROPOSAL SKRIPSI (REVISI)

**Judul:**
Penerapan Multi-Agent System untuk Sistem Pendukung Keputusan Investasi Saham pada Sektor Perbankan di IHSG

**Program Studi:** Teknik Komputer

---

## BAB I. PENDAHULUAN

### 1.1 Latar Belakang

Pengambilan keputusan investasi saham merupakan proses yang kompleks karena harus mengintegrasikan berbagai jenis informasi: data fundamental perusahaan, indikator teknikal, sentimen pasar, serta berita makroekonomi. Pendekatan algoritmik konvensional (misalnya *rule-based strategy* seperti MACD, SMA, atau RSI) umumnya hanya mengandalkan data numerik historis dan tidak mampu memahami konteks tekstual seperti berita atau laporan keuangan secara komprehensif.

Perkembangan *Large Language Model* (LLM) membuka peluang baru dalam membangun sistem pendukung keputusan investasi yang lebih adaptif dan *explainable*. Salah satu pendekatan yang menjanjikan adalah penggunaan arsitektur *Multi-Agent System* (MAS), di mana beberapa agen LLM dengan peran terspesialisasi (analis fundamental, analis sentimen, analis teknikal, peneliti bullish/bearish, trader, dan manajer risiko) berkolaborasi meniru struktur organisasi firma trading nyata. Kerangka kerja **TradingAgents** (Xiao et al., 2025) membuktikan bahwa pendekatan kolaboratif multi-agen ini mampu mengungguli strategi *rule-based* konvensional pada saham teknologi Amerika Serikat (AAPL, GOOGL, AMZN) dalam metrik *Cumulative Return*, *Sharpe Ratio*, dan *Maximum Drawdown*.

Namun demikian, validasi kerangka kerja tersebut masih terbatas pada pasar saham global (Nasdaq) dan belum diuji pada karakteristik pasar modal Indonesia, khususnya sektor perbankan yang tercatat di Bursa Efek Indonesia (IHSG). Sektor perbankan dipilih karena memiliki karakteristik unik: sangat sensitif terhadap kebijakan suku bunga Bank Indonesia (BI-7DRR), regulasi OJK, sentimen makroekonomi domestik, serta ketersediaan data fundamental dan berita berbahasa Indonesia yang berbeda struktur dan volumenya dibandingkan data berbahasa Inggris yang digunakan pada penelitian acuan.

Selain itu, terdapat tantangan teknis dalam adaptasi sistem multi-agen ke pasar Indonesia: ketidaktersediaan API data terstruktur yang setara dengan Finnhub dan Alpha Vantage (yang digunakan pada paper acuan), kebutuhan pemrosesan teks berbahasa Indonesia oleh LLM, serta perbedaan mikrostruktur pasar (lot size, jam perdagangan, biaya transaksi). Oleh karena itu, diperlukan penelitian untuk mengadaptasi arsitektur multi-agen tersebut ke konteks data, bahasa, dan regulasi pasar saham Indonesia, sekaligus mengevaluasi efektivitasnya dibandingkan strategi konvensional.

### 1.2 Rumusan Masalah

1. Bagaimana mekanisme kolaborasi antar-agen LLM (analis, peneliti bullish/bearish, trader, dan manajer risiko) dapat dirancang dan diintegrasikan untuk menghasilkan rekomendasi keputusan investasi (Buy/Hold/Sell) yang koheren pada saham sektor perbankan di IHSG dengan mempertimbangkan sumber data berbahasa Indonesia (berita, laporan keuangan, sentimen publik)?
2. Sejauh mana efektivitas hasil debat (*debate mechanism*) antara agen Bullish Researcher dan Bearish Researcher berkontribusi terhadap kualitas keputusan akhir dibandingkan dengan pendekatan tanpa mekanisme debat dan pendekatan agen tunggal (*single-agent*) dalam memprediksi pergerakan harga saham perbankan IHSG?
3. Bagaimana performa sistem multi-agen yang dibangun (diukur melalui *Cumulative Return*, *Sharpe Ratio*, *Maximum Drawdown*, dan *Win-Rate*) dibandingkan dengan strategi *Buy and Hold* serta strategi *rule-based* konvensional (MACD, SMA) pada saham-saham sektor perbankan IHSG periode 2024–2025?

### 1.3 Tujuan Penelitian

1. Merancang dan mengimplementasikan arsitektur *Multi-Agent System* yang terdiri atas Tim Analis (Fundamental, Sentimen, Macro, Teknikal), Tim Peneliti (Bullish–Bearish) beserta Fasilitator Debat, Agen Trader, Tim Manajemen Risiko (Aggressive–Conservative) beserta Fasilitator, dan Portfolio Manager yang mampu memproses data saham perbankan IHSG dan menghasilkan keputusan investasi terstruktur.
2. Mengukur peningkatan kualitas keputusan investasi akibat mekanisme debat multi-agen melalui *ablation study*, membandingkan konfigurasi sistem lengkap (MAS + debat), MAS tanpa debat, dan agen tunggal, dengan target minimal terjadi peningkatan *win-rate* keputusan sebesar ≥10% pada konfigurasi sistem lengkap dibandingkan konfigurasi tanpa debat.
3. Mengevaluasi performa sistem melalui simulasi *backtesting* pada 3 emiten *big-cap* sektor perbankan IHSG (BBCA, BBRI, BMRI) periode 2024–2025, dengan target sistem mampu menghasilkan *Cumulative Return* dan *Sharpe Ratio* yang lebih tinggi pada mayoritas emiten dan mayoritas baseline, serta *Maximum Drawdown* yang setara atau lebih rendah dibandingkan rata-rata strategi *rule-based* pembanding.

### 1.4 Batasan Masalah

1. Objek penelitian dibatasi pada 3 emiten *big-cap* sektor perbankan yang terdaftar di IHSG, yaitu: **BBCA** (Bank Central Asia), **BBRI** (Bank Rakyat Indonesia), dan **BMRI** (Bank Mandiri). Meskipun demikian, sistem dirancang secara modular sehingga dapat menerima input ticker emiten lain.
2. Periode data historis yang digunakan untuk simulasi *backtesting* dibatasi pada rentang **Januari 2024 – Desember 2025** (menyesuaikan ketersediaan data pada saat penelitian dilakukan).
3. Sumber data yang digunakan mencakup:
   - **Data harga historis (OHLCV):** Yahoo Finance melalui *library* `yfinance` (ticker format `*.JK`).
   - **Data berita keuangan:** Google News RSS feed dengan query berbahasa Indonesia, serta RSS feed portal berita keuangan Indonesia (CNBC Indonesia, Kontan.co.id, Bisnis.com).
   - **Data fundamental perbankan:** Data umum (laporan laba-rugi, neraca) diperoleh dari `yfinance`; data spesifik perbankan (NPL, CAR, NIM) dikompilasi secara manual dari laporan keuangan kuartalan yang dipublikasikan di idx.co.id (total ~72 data poin: 3 emiten × 8 kuartal × 3 rasio).
   - **Analisis sentimen:** Dilakukan secara langsung oleh agen LLM terhadap teks berita berbahasa Indonesia, tanpa tahap translasi terpisah.
   - Penelitian **tidak menggunakan** API premium (Bloomberg Terminal, Refinitiv) maupun API berbayar (Finnhub, Alpha Vantage) yang tidak memiliki cakupan memadai untuk saham Indonesia.
4. Karena keterbatasan ketersediaan API data terstruktur di pasar Indonesia dibandingkan pasar AS (yang menjadi konteks paper acuan), agen Sentimen dan agen Macro beroperasi dengan volume data yang lebih rendah. Dampak perbedaan ketersediaan data ini dianalisis sebagai bagian dari analisis kualitatif eksplainabilitas sistem.
5. Sistem tidak melakukan eksekusi transaksi riil (*live trading*); seluruh evaluasi dilakukan dalam simulasi *paper trading* / *backtesting* historis menggunakan *library* Backtrader.
6. Model LLM yang digunakan mengikuti strategi *hybrid* bertingkat untuk efisiensi biaya:
   - **Tahap development:** Model lokal melalui **Ollama** (misal: Llama 3.1 8B untuk *quick-thinking*, Qwen 2.5 14B untuk *deep-thinking*) untuk iterasi cepat tanpa biaya API.
   - **Tahap backtesting akhir:** Model *free-tier* API, yaitu **Google Gemini** (Gemini 2.0 Flash untuk *quick-thinking*, Gemini 2.5 Pro untuk *deep-thinking*) dan/atau **Groq** (Llama 3.3 70B) sebagai alternatif.
   - Tidak dilakukan *fine-tuning* model dari awal.
7. Penelitian tidak membahas aspek regulasi/legalitas robo-advisory di pasar modal Indonesia (OJK), melainkan berfokus pada aspek teknis sistem pendukung keputusan.

### 1.5 Manfaat Penelitian

1. **Manfaat Teoritis:** Memberikan bukti empiris mengenai efektivitas arsitektur *Multi-Agent System* berbasis LLM pada konteks pasar saham berkembang (Indonesia) dengan data berbahasa non-Inggris, memperluas validasi yang sebelumnya terbatas pada pasar AS.
2. **Manfaat Praktis:** Menghasilkan prototipe sistem pendukung keputusan investasi yang *explainable* (dapat menjelaskan alasan di balik setiap rekomendasi melalui *reasoning trace*), yang dapat dikembangkan lebih lanjut oleh peneliti maupun praktisi pasar modal Indonesia.

---

## BAB II. TINJAUAN PUSTAKA

### 2.1 Penelitian Terdahulu

Berikut lima referensi akademik yang relevan sebagai landasan teori dan metodologi penelitian, disusun dalam format IEEE:

[1] Y. Xiao, E. Sun, D. Luo, and W. Wang, "TradingAgents: Multi-Agents LLM Financial Trading Framework," *arXiv preprint arXiv:2412.20138v7*, Jun. 2025. [Online]. Available: https://arxiv.org/abs/2412.20138

[2] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," *arXiv preprint arXiv:2308.00352*, 2024. [Online]. Available: https://arxiv.org/abs/2308.00352

[3] Y. Yu, Z. Yao, H. Li, Z. Deng, Y. Cao, Z. Chen, J. W. Suchow, R. Liu, Z. Cui, and D. Zhang, "FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making," *Proc. NeurIPS 2024*, 2024. [Online]. Available: https://arxiv.org/abs/2407.06567

[4] S. Wu, O. Irsoy, S. Lu, V. Dabravolski, M. Dredze, S. Gehrmann, P. Kambadur, D. Rosenberg, and G. Mann, "BloombergGPT: A Large Language Model for Finance," *arXiv preprint arXiv:2303.17564*, 2023. [Online]. Available: https://arxiv.org/abs/2303.17564

[5] Y. Yu, H. Li, Z. Chen, Y. Jiang, Y. Li, D. Zhang, R. Liu, J. W. Suchow, and K. Khashanah, "FinMem: A Performance-Enhanced LLM Trading Agent with Layered Memory and Character Design," *arXiv preprint arXiv:2311.13743*, 2023. [Online]. Available: https://arxiv.org/abs/2311.13743

### 2.2 Ringkasan Kontribusi Setiap Referensi

| No | Referensi | Kontribusi Utama terhadap Penelitian Ini |
|----|-----------|-------------------------------------------|
| 1 | [1] TradingAgents | Menjadi **rujukan utama arsitektur**: struktur peran agen (Fundamental, Sentiment, News, Technical Analyst, Researcher, Trader, Risk Manager, Portfolio Manager), mekanisme debat multi-putaran dengan fasilitator, dan metrik evaluasi (CR, AR, SR, MDD) yang diadopsi langsung. Implementasi menggunakan LangGraph sebagai kerangka orkestrasi. |
| 2 | [2] MetaGPT | Landasan konsep **protokol komunikasi terstruktur antar-agen** melalui pola *publish-subscribe* pada *shared global message pool*. Setiap agen mempublikasikan dokumen terstruktur ke *pool* dan agen lain melakukan *subscribe* berdasarkan peran, sehingga setiap agen membaca dari **sumber primer** (dokumen terstruktur) — bukan parafrase agen sebelumnya — untuk mencegah *"telephone effect"* (degradasi informasi antar-agen). |
| 3 | [3] FinCon | Referensi tentang mekanisme **Conceptual Verbal Reinforcement (CVR)** pada sistem multi-agen finansial — setelah setiap episode trading, sistem menghasilkan *verbal concept* (pelajaran dalam bahasa alami) yang disimpan dan diambil kembali untuk memperbaiki keputusan di masa depan. Juga menggunakan **hirarki Manager-Analyst** dan **CVaR** untuk manajemen risiko. |
| 4 | [4] BloombergGPT | Landasan teori tentang **LLM khusus domain finansial**, memperkuat argumentasi perlunya adaptasi agen analis terhadap istilah dan data keuangan spesifik (termasuk konteks perbankan Indonesia). |
| 5 | [5] FinMem | Referensi desain **layered memory** (Working, Episodic, Semantic) pada agen trader tunggal dengan *character design* (profil risiko). Digunakan sebagai **baseline agen tunggal** pada *ablation study* untuk menjawab rumusan masalah kedua. |

### 2.3 Kerangka Berpikir

Penelitian ini memposisikan diri sebagai **studi replikasi dan adaptasi** (*replication and domain adaptation study*) dari arsitektur TradingAgents [1], dengan kontribusi orisinal berupa:

1. **Adaptasi sumber data** ke konteks emiten dan berita berbahasa Indonesia, termasuk penanganan tantangan ketersediaan data yang lebih terbatas dibandingkan pasar AS.
2. **Evaluasi pada karakteristik sektor perbankan IHSG**, yang memiliki dinamika berbeda dari saham teknologi AS (sensitivitas terhadap BI-7DRR, regulasi OJK, rasio keuangan spesifik perbankan).
3. **Analisis kuantitatif kontribusi mekanisme debat** melalui *ablation study* terstruktur (Full MAS vs. MAS tanpa debat vs. Single Agent) pada pasar dengan volatilitas dan likuiditas yang berbeda dari pasar Nasdaq.
4. **Demonstrasi kemampuan LLM multilingual** dalam memproses dan menganalisis data finansial berbahasa Indonesia tanpa tahap translasi terpisah.

---

## BAB III. METODOLOGI PENELITIAN

Penelitian ini menggunakan pendekatan **Design Science Research (DSR)**, karena bertujuan merancang, membangun, dan mengevaluasi sebuah artefak (sistem multi-agen) untuk memecahkan permasalahan nyata (pengambilan keputusan investasi). Tahapan metodologi disusun sebagai berikut:

### 3.1 Tahap 1 — Studi Literatur

- Mengkaji paper *TradingAgents* [1] secara mendalam, termasuk kode sumber pada repositori GitHub `TauricResearch/TradingAgents` (khususnya arsitektur LangGraph, skema state, dan mekanisme debat) untuk memahami alur eksekusi, struktur *prompt*, dan pemanggilan *tools*.
- Mengkaji literatur pendukung terkait *Multi-Agent Orchestration* (MetaGPT [2], khususnya pola *publish-subscribe*), *Financial LLM* (BloombergGPT [4]), sistem *verbal reinforcement* (FinCon [3]), dan *layered memory* pada trading agent (FinMem [5]).
- Menyusun peta kesenjangan (*gap analysis*) antara implementasi orisinal (pasar AS, data Finnhub/Alpha Vantage) dengan kebutuhan riset pada pasar saham perbankan IHSG (data lokal, bahasa Indonesia).

### 3.2 Tahap 2 — Pengumpulan dan Persiapan Data

#### 3.2.1 Data Harga Historis (OHLCV)
- Diambil melalui *library* `yfinance` dengan format ticker Jakarta: `BBCA.JK`, `BBRI.JK`, `BMRI.JK`.
- Periode: Januari 2024 – Desember 2025 (data harian, ~480 hari perdagangan).
- Dilengkapi data indeks IHSG (`^JKSE`) sebagai referensi pergerakan pasar keseluruhan.
- **Validasi kualitas data:** implementasi pengecekan anomali (harga OHLC identik, volume nol) dan koreksi aksi korporasi (*stock split*, *rights issue*).

#### 3.2.2 Data Berita Keuangan
- **Sumber primer:** Google News RSS feed dengan query berbahasa Indonesia:
  ```
  https://news.google.com/rss/search?q=BBCA+saham&hl=id&gl=ID&ceid=ID:id
  https://news.google.com/rss/search?q=suku+bunga+Bank+Indonesia&hl=id&gl=ID&ceid=ID:id
  ```
- **Sumber pendukung:** RSS feed portal berita keuangan Indonesia:
  - CNBC Indonesia (`cnbcindonesia.com/rss`)
  - Kontan (`investasi.kontan.co.id/rss`)
  - Bisnis.com (`finansial.bisnis.com/rss`)
- Data diparsing menggunakan *library* `feedparser` dan disimpan dalam format JSON per tanggal per emiten.

#### 3.2.3 Data Fundamental Perbankan
- **Data umum** (laporan laba-rugi, neraca, arus kas): diperoleh melalui `yfinance` (`ticker.income_stmt`, `ticker.balance_sheet`, `ticker.cashflow`).
- **Rasio spesifik perbankan** (NPL, CAR, NIM): dikompilasi **secara manual** dari laporan keuangan kuartalan yang dipublikasikan di situs idx.co.id dan situs *investor relations* masing-masing emiten. Total: ~72 data poin (3 emiten × 8 kuartal × 3 rasio), disimpan dalam format CSV.
- **Rasio turunan** (ROE, ROA): dihitung secara programatis dari data laporan keuangan `yfinance`.

#### 3.2.4 Data Risk-Free Rate
- Menggunakan **BI-7DRR (BI 7-Day Reverse Repo Rate)** sebagai proksi *risk-free rate* untuk perhitungan Sharpe Ratio, yang merupakan padanan langsung *3-month Treasury bill* pada konteks Indonesia.
- Data historis BI-7DRR diperoleh dari situs Bank Indonesia (`bi.go.id/id/statistik/indikator/bi-7day-rr.aspx`).
- Konversi ke *daily risk-free rate*: $R_{f,daily} = (1 + R_{f,annual})^{1/252} - 1$

#### 3.2.5 Strategi Pencegahan *Look-Ahead Bias* dan *Centralized Caching*
- **Seluruh data dikumpulkan dan di-*cache* secara terpusat (Centralized Caching)** di tingkat *ticker* sebelum simulasi *backtesting* dimulai.
- Untuk efisiensi ruang penyimpanan dan kecepatan I/O, sistem tidak lagi membuat folder per tanggal (seperti rancangan awal), melainkan menggunakan satu *master file* per sumber data (`master_ohlcv.csv`, `master_fundamentals.json`, `master_news.json`).
- Proses *slicing* (pemotongan data berdasarkan tanggal simulasi berjalan) dilakukan secara *in-memory* menggunakan filter Pandas Dataframe. Setiap agen hanya menerima potongan data dengan tanggal ≤ tanggal simulasi berjalan (*current_date*), sehingga *look-ahead bias* dihindari secara mutlak dan terprogram.
- Struktur *cache*: `data/cache/{ticker}/master_*`.

### 3.3 Tahap 3 — Perancangan Arsitektur Multi-Agen

- Mendefinisikan peran, tujuan (*goal*), batasan (*constraint*), *tools*, dan *system prompt* untuk setiap agen (dijelaskan rinci pada BAB IV).
- Merancang **skema global state** (`TradingState`) sebagai struktur data TypedDict yang menjadi wadah pertukaran informasi antar-agen, mengadopsi pola *publish-subscribe* dari MetaGPT [2].
- Merancang mekanisme debat multi-putaran antara agen Bullish dan Bearish (pada Tim Peneliti) serta antara agen Aggressive dan Conservative (pada Tim Manajemen Risiko), masing-masing dengan **agen Fasilitator Debat** yang merangkum hasil debat menjadi output terstruktur.
- Merancang **tiga konfigurasi sistem** untuk *ablation study*:
  1. **Full MAS:** Sistem lengkap dengan mekanisme debat.
  2. **MAS tanpa Debat:** Bullish & Bearish digabung menjadi 1 Researcher; 3 Risk Manager digabung menjadi 1.
  3. **Single Agent:** 1 agen LLM menerima seluruh data dan menghasilkan keputusan langsung (baseline gaya FinMem [5]).

### 3.4 Tahap 4 — Implementasi Sistem

- Implementasi dilakukan menggunakan **Python 3.10+**, dengan kerangka orkestrasi agen **LangGraph** (`langgraph` + `langchain-core`). LangGraph dipilih karena:
  1. Implementasi asli TradingAgents [1] menggunakan LangGraph, meminimalkan *effort* adaptasi.
  2. LangGraph menyediakan kontrol granular atas *state machine* dan alur eksekusi.
  3. Mendukung eksekusi paralel (untuk 4 agen analis) dan *conditional edges* (untuk debat multi-putaran) secara native.
  4. Mendukung *checkpointing* via SQLite untuk pemulihan dari kegagalan.

- **Strategi model LLM bertingkat:**
  | Tahap | *Quick-Thinking* (Analis) | *Deep-Thinking* (Debat, Trader, PM) | Package |
  |-------|--------------------------|--------------------------------------|---------|
  | Development | Llama 3.1 8B (Ollama) | Qwen 2.5 14B (Ollama) | `langchain-ollama` |
  | Backtesting | Gemini 2.0 Flash (free-tier, 1500 RPD) | Gemini 2.5 Pro (free-tier, 25 RPD) atau Groq Llama 3.3 70B (14400 RPD) | `langchain-google-genai` atau `langchain-groq` |

- **Implementasi *rate limiter***: menggunakan *library* `tenacity` dengan *exponential backoff* untuk menangani batas *rate* API *free-tier*.
- Antarmuka pengguna dibangun menggunakan **Streamlit** sebagai antarmuka utama dan **CLI interaktif** sebagai alternatif.
- Simulasi *backtesting* menggunakan *library* **Backtrader** untuk simulasi portofolio, eksekusi order, dan perhitungan metrik.

### 3.5 Tahap 5 — Pengujian dan Evaluasi

- Melakukan simulasi *backtesting* harian pada data historis 2024–2025 untuk setiap emiten sampel (BBCA, BBRI, BMRI).
- Menjalankan *ablation study* dengan 3 konfigurasi sistem (Full MAS, MAS tanpa debat, Single Agent).
- Membandingkan performa sistem dengan 5 strategi baseline: *Buy and Hold*, MACD, SMA, KDJ+RSI, dan ZMR.
- Menghitung metrik evaluasi: *Cumulative Return* (CR), *Annualized Return* (AR), *Sharpe Ratio* (SR), *Maximum Drawdown* (MDD), dan *Win-Rate* (WR).
- Melakukan analisis kualitatif terhadap log penalaran (*reasoning trace*) agen untuk menilai aspek *explainability* sistem.

### 3.6 Diagram Alur Metodologi

```
┌─────────────────┐     ┌───────────────────────┐     ┌───────────────────────┐
│  Studi Literatur │────▶│  Pengumpulan Data      │────▶│  Perancangan Arsitektur│
│  & Gap Analysis  │     │  (yfinance, RSS, IDX)  │     │  & State Schema       │
└─────────────────┘     └───────────────────────┘     └───────────┬───────────┘
                                                                   │
     ┌─────────────────────────────────────────────────────────────┘
     ▼
┌───────────────────────┐     ┌───────────────────────┐     ┌─────────────────────┐
│  Implementasi          │────▶│  Pengujian &           │────▶│  Analisis Hasil &    │
│  (LangGraph + Ollama/  │     │  Backtesting           │     │  Penyusunan Laporan  │
│   Gemini/Groq)         │     │  (Backtrader)          │     │                      │
└───────────────────────┘     └───────────────────────┘     └─────────────────────┘
```

---

## BAB IV. PERANCANGAN SISTEM

### 4.1 Arsitektur Agen

Sistem terdiri atas lima lapisan tim agen yang bekerja secara berurutan dan kolaboratif, mengadaptasi struktur pada paper *TradingAgents* [1]:

#### 4.1.1 Tim Analis (*Analyst Team*) — Eksekusi Paralel
Empat agen analis bekerja secara **paralel** mengumpulkan dan merangkum data mentah menjadi laporan analisis terstruktur:

- **Fundamental Analyst**: Menganalisis laporan keuangan, rasio keuangan umum (ROE, ROA, P/E, P/B) serta rasio spesifik perbankan (NPL, CAR, NIM), dan data *insider* jika tersedia.
- **Sentiment Analyst**: Menganalisis sentimen publik terhadap emiten berdasarkan berita dan diskusi online, dengan kemampuan memproses teks **berbahasa Indonesia** secara langsung.
- **Macro Analyst**: Menganalisis kondisi makroekonomi (kebijakan BI-7DRR, regulasi OJK, kondisi global, nilai tukar rupiah) yang memengaruhi sektor dan emiten.
- **Technical Analyst**: Menghitung dan menginterpretasikan indikator teknikal (MACD, RSI, Bollinger Bands, ADX, SMA/EMA) berdasarkan data harga historis menggunakan *library* `stockstats`.

#### 4.1.2 Tim Peneliti (*Researcher Team*) — Mekanisme Debat
Terdiri atas tiga agen:

- **Bullish Researcher**: Menyusun argumen investasi positif berdasarkan laporan Tim Analis.
- **Bearish Researcher**: Menyusun argumen peringatan/negatif berdasarkan laporan Tim Analis.
- **Research Debate Facilitator**: Memoderasi debat, menentukan kesimpulan, dan menghasilkan **ringkasan terstruktur** yang menangkap argumen terkuat dari kedua sisi.

#### 4.1.3 Tim Manajemen Risiko (*Risk Management Team*) — Mekanisme Debat
Terdiri atas tiga agen:

- **Aggressive Risk Analyst**: Mengevaluasi dari perspektif pengambilan risiko secara maksimal untuk *return* tinggi.
- **Conservative Risk Analyst**: Mengevaluasi dari perspektif kehati-hatian, perlindungan modal, dan penghindaran volatilitas ekstrem.
- **Risk Facilitator**: Memoderasi perdebatan kedua profil risiko ekstrem dan menghasilkan rekomendasi risiko terkonsensus yang adaptif.

#### 4.1.4 Tim Eksekusi (*Execution Team*)
- **Portfolio Manager**: Melakukan keputusan final (approve/reject/adjust) atas rekomendasi riset dan risiko, mempertimbangkan kondisi portofolio (saldo kas, posisi terbuka).
- **Trading Agent**: Menerjemahkan keputusan Portfolio Manager menjadi order kuantitatif (*action*, *quantity* dalam lot, *confidence*) dalam format mesin yang terstandarisasi.

**Total: 12 agen** (4 Analis + 3 Peneliti + 3 Manajer Risiko + 1 Portfolio Manager + 1 Trading Agent).

### 4.2 Skema Global State (*State Schema*)

Seluruh komunikasi antar-agen dilakukan melalui **global state** menggunakan pola *publish-subscribe* (diadopsi dari MetaGPT [2]). Setiap agen membaca dari dan menulis ke *state* ini — bukan mengirim pesan langsung ke agen lain — sehingga mencegah *telephone effect*.

```python
from typing import TypedDict, List, Optional

class TradingState(TypedDict):
    # ===== Input =====
    ticker: str                      # e.g., "BBCA.JK"
    current_date: str                # e.g., "2024-06-15"
    portfolio: dict                  # {"cash": float, "positions": {...}, "total_value": float}

    # ===== Laporan Tim Analis (diisi paralel) =====
    fundamental_report: str          # Laporan analis fundamental (Markdown + JSON skor)
    sentiment_report: str            # Laporan analis sentimen (JSON tren + skor)
    news_report: str                 # Laporan analis berita (Markdown naratif + tag)
    technical_report: str            # Laporan analis teknikal (JSON indikator + tren)

    # ===== Tim Peneliti (Debat) =====
    bull_arguments: List[str]        # Argumen bullish per putaran debat
    bear_arguments: List[str]        # Argumen bearish per putaran debat
    research_debate_rounds: int      # Jumlah putaran debat yang dilakukan
    research_summary: str            # Sintesis fasilitator (output terstruktur)

    # ===== Keputusan Trader =====
    trader_recommendation: str       # JSON: {"action": "BUY/HOLD/SELL", "confidence": ..., "rationale": ...}

    # ===== Tim Manajemen Risiko (Debat) =====
    aggressive_assessment: str       # Penilaian risk manager agresif
    moderate_assessment: str         # Penilaian risk manager moderat
    conservative_assessment: str     # Penilaian risk manager konservatif
    risk_debate_rounds: int          # Jumlah putaran debat risiko
    risk_summary: str                # Sintesis fasilitator risiko

    # ===== Keputusan Final =====
    final_decision: str              # JSON: {"action": ..., "confidence": ..., "quantity": ..., "summary": ...}
    reasoning_trace: List[str]       # Log penalaran untuk explainability
```

### 4.3 Mekanisme Input & Output per Agen

| Agen | Input Data | Format Output |
|------|-----------|----------------|
| **Fundamental Analyst** | Laporan keuangan (yfinance), rasio perbankan | Paragraf naratif (maksimal 3 kalimat) |
| **Sentiment Analyst** | Berita terkini (Google News RSS, dll.) | Paragraf naratif (maksimal 3 kalimat) |
| **Macro Analyst** | Berita makroekonomi (RSS feed), BI rate | Paragraf naratif (maksimal 3 kalimat) |
| **Technical Analyst** | Data OHLCV, indikator | Paragraf naratif (maksimal 3 kalimat) |
| **Bullish/Bearish Researcher** | Seluruh laporan Tim Analis | Paragraf naratif (maksimal 3 kalimat) |
| **Research Facilitator** | Argumen debat kedua Researcher | Paragraf naratif (maksimal 3 kalimat) |
| **Risk Analysts (Aggressive/Conservative)** | Kesimpulan riset | Paragraf naratif (maksimal 3 kalimat) |
| **Risk Facilitator** | Penilaian kedua Risk Analyst | Paragraf naratif (maksimal 3 kalimat) |
| **Portfolio Manager** | Ringkasan risiko + kondisi portofolio | Paragraf naratif (maksimal 3 kalimat) |
| **Trading Agent** | Keputusan Portfolio Manager | JSON: `{"action": "BUY/HOLD/SELL", "quantity": ..., "confidence": ...}` |

*Catatan: Seluruh agen (kecuali Trading Agent) diprogram dengan sangat ketat (melalui system prompt) untuk menghasilkan ringkasan berbasis teks polos (plain text) tanpa elemen markdown, untuk menjamin estetika logging yang bersih di terminal.*

### 4.4 Mekanisme Debat Antar-Agen

Mekanisme debat mengadopsi pendekatan dialektik pada paper acuan [1]:

1. **Debat Tim Peneliti (Bullish vs Bearish):**
   - Kedua Researcher menerima **seluruh** laporan Tim Analis dari global state.
   - Debat dilakukan dalam **n putaran** (default: 2–3, ditentukan oleh fasilitator berdasarkan tingkat konvergensi argumen).
   - Setiap putaran: Bullish menyajikan argumen → Bearish menanggapi secara eksplisit → Bullish memberikan *counter-argument* → Fasilitator mengevaluasi apakah debat perlu dilanjutkan.
   - Fasilitator menghasilkan **ringkasan terstruktur** (bukan transkrip penuh) yang dicatat ke global state — sesuai prinsip *structured communication protocol* untuk menghindari *telephone effect*.

2. **Debat Tim Manajemen Risiko (Agresif vs Netral vs Konservatif):**
   - Tiga Risk Manager mengevaluasi usulan Trader dari perspektif masing-masing.
   - Debat tiga-arah dengan mekanisme serupa: setiap agen menanggapi argumen agen lain secara eksplisit.
   - Fasilitator Risiko menghasilkan rekomendasi konsensus.

3. **Prinsip efisiensi:** Jumlah putaran debat tidak tetap (*fixed*) — fasilitator secara dinamis menentukan kapan debat telah mencapai kedalaman yang cukup, menyeimbangkan ketelitian analisis dengan efisiensi biaya API.

### 4.5 Strategi Penanganan Data Multibahasa

Karena adaptasi ke pasar Indonesia melibatkan pemrosesan teks berbahasa Indonesia oleh LLM yang dominan berbahasa Inggris, strategi berikut diterapkan:

| Aspek | Strategi | Alasan |
|-------|---------|--------|
| **Input data** | Bahasa Indonesia (berita, laporan) | Data asli tanpa translasi untuk mempertahankan konteks dan nuansa |
| **Pemrosesan internal agen** | Bahasa Inggris | LLM memiliki performa penalaran lebih konsisten dalam bahasa Inggris; mengurangi risiko hallucination |
| **Output ke global state** | Bahasa Inggris (JSON + Markdown) | Konsistensi antar-agen; data terstruktur tidak bergantung bahasa |
| **Output ke pengguna** | Bahasa Indonesia | Laporan akhir dan ringkasan diterjemahkan oleh Portfolio Manager untuk aksesibilitas pengguna |
| **Domain knowledge** | Glosarium keuangan Indonesia | Setiap *system prompt* menyertakan glosarium istilah spesifik (NPL, CAR, BI-7DRR, IHSG, OJK, lot saham) |

### 4.6 Kerangka *System Prompt* Agen

Setiap agen memiliki *system prompt* terstruktur dengan komponen berikut (contoh untuk Fundamental Analyst):

```markdown
## Role Definition
Anda adalah Fundamental Analyst yang mengkhususkan diri pada saham sektor perbankan Indonesia 
yang terdaftar di Bursa Efek Indonesia (IDX/IHSG).

## Task Specification
Analisis data keuangan berikut untuk emiten {ticker} pada tanggal {current_date}:
- Laporan laba-rugi, neraca, dan arus kas terkini
- Rasio keuangan umum: ROE, ROA, P/E, P/B
- Rasio spesifik perbankan: NPL (Non-Performing Loan), CAR (Capital Adequacy Ratio), 
  NIM (Net Interest Margin)
- Tren historis rasio-rasio tersebut (kuartal-ke-kuartal)

## Output Format
Hasilkan laporan dalam format JSON terstruktur:
{
  "valuation_score": <1-10>,
  "banking_health_score": <1-10>,
  "key_strengths": ["...", "..."],
  "key_risks": ["...", "..."],
  "narrative_summary": "..."
}

## Constraints
- HANYA gunakan data yang tersedia hingga tanggal {current_date}
- JANGAN membuat prediksi berdasarkan pengetahuan setelah tanggal tersebut
- Pertimbangkan konteks regulasi Indonesia (OJK, BI) dalam analisis

## Domain Knowledge (Glosarium)
- NPL: Non-Performing Loan — rasio kredit bermasalah, batas sehat OJK: <5%
- CAR: Capital Adequacy Ratio — rasio kecukupan modal, minimum OJK: 8%
- NIM: Net Interest Margin — selisih bunga pinjaman dan simpanan
- BI-7DRR: BI 7-Day Reverse Repo Rate — suku bunga acuan Bank Indonesia
- IHSG: Indeks Harga Saham Gabungan (Jakarta Composite Index)
```

*Catatan: System prompt lengkap untuk seluruh agen akan didefinisikan dalam file konfigurasi terpisah (`config/prompts/`) pada tahap implementasi.*

### 4.7 Asumsi Simulasi Backtesting

| Aspek | Asumsi | Keterangan |
|-------|--------|------------|
| **Eksekusi transaksi** | Harga pembukaan (*open*) hari berikutnya (T+1) | Sesuai asumsi paper acuan [1]; mencegah bias harga penutupan |
| **Biaya transaksi** | Beli: 0,15% — Jual: 0,25% (termasuk pajak) | Mengikuti rata-rata *fee* broker ritel Indonesia |
| **Lot size** | Kelipatan 100 lembar saham | Sesuai aturan Bursa Efek Indonesia |
| **Modal awal** | Rp 100.000.000 | Cukup representatif untuk investor ritel menengah |
| **Posisi** | Hanya *long* (beli) | Tanpa *short selling*, sesuai keterbatasan regulasi BEI untuk investor ritel |
| **Alokasi per emiten** | Seimbang (1/3 modal per emiten) atau seluruh modal untuk analisis per-emiten | Disesuaikan skenario pengujian |

### 4.8 Alur Data dan Interaksi Pengguna

#### Alur Eksekusi Sistem

```text
[Input: Ticker, Tanggal, Model LLM]
         │
         ▼
┌────────────────────────────────────────────┐
│ TIM ANALIS (4 agen, eksekusi paralel)      │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │Fundamntl │ │Sentimen  │ │Macro     │ │Teknikal  │ │
│ └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘ │
│       └──────┬─────┴─────┬──────┘             │      │
│              ▼           ▼                    ▼      │
│         [Global State: 4 Laporan Analis]             │
└────────────────────────┬───────────────────────────────┘
                         ▼
┌────────────────────────────────────────────┐
│ TIM PENELITI (Debat)                       │
│ ┌──────────┐    ┌──────────┐               │
│ │ Bullish  │◄──▶│ Bearish  │               │
│ └─────┬────┘    └─────┬────┘               │
│       └──────┬────────┘                     │
│              ▼                              │
│   [Research Facilitator]                   │
│              ▼                              │
│   [Global State: Ringkasan Investasi]      │
└────────────────────────┬───────────────────┘
                         ▼
┌────────────────────────────────────────────┐
│ TIM MANAJEMEN RISIKO (Debat)               │
│ ┌──────────┐    ┌──────────┐               │
│ │Aggressive│◄──▶│Consrvtive│               │
│ └─────┬────┘    └─────┬────┘               │
│       └──────┬────────┘                     │
│              ▼                              │
│   [Risk Facilitator]                       │
│              ▼                              │
│   [Global State: Rekomendasi Risiko]       │
└────────────────────────┬───────────────────┘
                         ▼
┌────────────────────────────────────────────┐
│ PORTFOLIO MANAGER (1 agen)                 │
│ [Keputusan Strategis Final Portofolio]     │
└────────────────────────┬───────────────────┘
                         ▼
┌────────────────────────────────────────────┐
│ TRADING AGENT (1 agen)                     │
│ [Order Eksekusi Kuantitatif JSON]          │
└────────────────────────┬───────────────────┘
                         ▼
                    [OUTPUT TABEL & LOG]
```

#### Antarmuka Pengguna (Streamlit)

1. **Halaman Input:** Form untuk memasukkan ticker, tanggal simulasi, dan pilihan model LLM.
2. **Halaman Eksekusi:** *Progress bar/status tracker* yang menampilkan tahapan eksekusi (Analyst → Researcher → Trader → Risk Mgmt → Portfolio Manager) dengan indikator status (*pending/running/completed*) untuk setiap agen, disertai log *tools* dan *reasoning trace* secara *streaming*.
3. **Halaman Hasil:** Ringkasan rekomendasi akhir (Buy/Hold/Sell + tingkat keyakinan), argumen per tim dalam *expandable card*, grafik performa historis, dan opsi *export* ke Markdown.

### 4.9 Struktur Direktori Proyek

```text
skripsi-multiagent-saham/
│
├── config/
│   ├── prompts/                    # System prompts untuk setiap tim agen
│   │   ├── analyst_prompts.py
│   │   ├── research_prompts.py
│   │   ├── risk_prompts.py
│   │   └── execution_prompts.py
│   ├── llm_config.py               # Konfigurasi model LLM (Ollama/Gemini/Groq)
│   ├── data_sources.py             # Konfigurasi URL RSS, ticker, dll.
│   └── glossary.py                 # Glosarium keuangan Indonesia untuk prompt
│
├── data/
│   └── cache/                      # Centralized Cache per ticker (in-memory slicing)
│       └── {ticker}/               # Struktur: BBCA.JK/master_ohlcv.csv
│
├── agents/                         # Definisi Agen per Tim
│   ├── analysts.py                 # Fundamental, Sentiment, Macro, Technical
│   ├── researchers.py              # Bullish, Bearish, Facilitator
│   ├── risk_management.py          # Aggressive, Conservative, Facilitator
│   └── execution.py                # Portfolio Manager, Trading Agent
│
├── orchestration/
│   ├── graph.py                    # Definisi workflow LangGraph (StateGraph)
│   ├── state.py                    # TradingState TypedDict
│   └── backtester.py               # Engine backtesting dan logging terminal
│
├── tools/
│   ├── data_fetcher.py             # Wrapper yfinance untuk OHLCV + fundamental
│   ├── cache_manager.py            # Manajemen cache (master file)
│   └── utils.py                    # Helper fungsionalitas
│
├── main.py                         # Entry point eksekusi sistem (CLI)
│
├── backtesting/
│   ├── simulator.py                 # Integrasi Backtrader
│   ├── metrics.py                   # CR, AR, SR, MDD, WR
│   ├── baseline_strategies.py       # Buy&Hold, MACD, SMA, KDJ+RSI, ZMR
│   └── ablation_runner.py           # Runner untuk 3 konfigurasi ablation study
│
├── results/
│   ├── logs/                        # Reasoning trace per eksekusi
│   └── reports/                     # Laporan hasil backtesting
│
├── requirements.txt
├── .env.example                     # Template API keys
└── README.md
```

### 4.10 Eksplainabilitas & Logging Terminal Akademis

Untuk mendukung transparansi riset skripsi, sistem mengadopsi mekanisme **Explainable AI** yang divisualisasikan langsung di antarmuka *terminal*:
1. **Pembersihan Truncation**: Tidak ada limitasi jumlah karakter pada log keluaran agar logika agen (representasi utuh maksimal 3 kalimat naratif) bisa diakses dan didokumentasikan tanpa pemenggalan.
2. **Eksekusi Sekuensial**: Meskipun node Analis dieksekusi secara paralel di *background*, orkestrasi log diatur agar dicetak secara linear (sekuensial) berdasarkan *flowchart* (Analis → Peneliti → Risiko → PM → Trading), mempermudah pelacakan *chain of thought*.
3. **Tabular Visualization**: Setiap akhir siklus harian, sistem otomatis menghasilkan tabel matriks konsensus menggunakan modul `tabulate` yang merangkum keseluruhan strategi Buy/Sell/Hold setiap 12 agen secara *grid* akademis.

---

## BAB V. PENGUJIAN & HASIL (RENCANA EVALUASI)

### 5.1 Desain Eksperimen

Evaluasi dilakukan melalui simulasi *backtesting* historis tanpa *look-ahead bias*, di mana sistem hanya menggunakan data yang tersedia hingga tanggal simulasi berjalan. Eksperimen dilakukan pada 3 emiten sektor perbankan IHSG:

| Emiten | Ticker Yahoo Finance | Karakteristik |
|--------|---------------------|---------------|
| Bank Central Asia | `BBCA.JK` | *Big-cap* perbankan swasta, fundamental terkuat |
| Bank Rakyat Indonesia | `BBRI.JK` | *Big-cap* perbankan BUMN, fokus UMKM/mikro |
| Bank Mandiri | `BMRI.JK` | *Big-cap* perbankan BUMN, *commercial banking* |

Periode simulasi: **Januari 2024 – Desember 2025** (~480 hari perdagangan), mengikuti kalender perdagangan riil Bursa Efek Indonesia.

### 5.2 Desain *Ablation Study*

Untuk menjawab rumusan masalah kedua (kontribusi mekanisme debat), dilakukan *ablation study* dengan 3 konfigurasi:

| Konfigurasi | Deskripsi | Jumlah Agen | Tujuan |
|-------------|-----------|-------------|--------|
| **Full MAS** | Sistem lengkap: 4 Analis + 2 Researcher + Fasilitator + Trading Agent + 2 Risk Analyst + Fasilitator + Portfolio Manager | 12 | Baseline utama; sistem yang diusulkan |
| **MAS tanpa Debat** | 4 Analis + 1 Researcher (gabungan) + Trader + 1 Risk Manager (gabungan) + Portfolio Manager | 8 | Mengukur kontribusi spesifik mekanisme debat |
| **Single Agent** | 1 agen LLM menerima seluruh data dan menghasilkan keputusan langsung (mengadopsi pendekatan FinMem [5] tanpa layered memory) | 1 | Mengukur kontribusi arsitektur multi-agen secara keseluruhan |

Setiap konfigurasi dijalankan pada **ketiga emiten** dengan **model LLM dan data yang identik** untuk memastikan perbandingan yang adil.

### 5.3 Strategi Pembanding (*Baseline*)

Mengikuti pendekatan pada paper acuan [1], sistem dibandingkan dengan lima strategi *rule-based*:

1. **Buy and Hold** — investasi tetap tanpa perubahan posisi selama periode simulasi.
2. **MACD Strategy** — sinyal beli/jual berdasarkan *crossover* garis MACD dan *signal line*.
3. **SMA Strategy** — sinyal berdasarkan persilangan *Simple Moving Average* jangka pendek (20 hari) dan jangka panjang (50 hari).
4. **KDJ + RSI Strategy** — kombinasi osilator stokastik KDJ dan RSI untuk deteksi kondisi *overbought/oversold*.
5. **ZMR (Zero Mean Reversion)** — strategi *mean reversion* berbasis deviasi harga dari garis referensi.

*Catatan: Strategi KDJ+RSI dan ZMR dipilih untuk memastikan komparabilitas langsung dengan hasil pada paper acuan [1], meskipun tidak umum digunakan dalam literatur pasar Indonesia.*

### 5.4 Metrik Evaluasi

Lima metrik utama digunakan:

**1) Cumulative Return (CR)**

$$CR = \left(\frac{V_{end} - V_{start}}{V_{start}}\right) \times 100\%$$

**2) Annualized Return (AR)**

$$AR = \left[\left(\frac{V_{end}}{V_{start}}\right)^{\frac{1}{N}} - 1\right] \times 100\%$$

di mana $N$ adalah jumlah tahun periode simulasi.

**3) Sharpe Ratio (SR)**

$$SR = \frac{\bar{R} - R_f}{\sigma}$$

di mana $\bar{R}$ adalah rata-rata *return* harian portofolio, $R_f$ adalah *daily risk-free rate* yang diturunkan dari **BI-7DRR** (BI 7-Day Reverse Repo Rate) sebagai proksi *risk-free rate* konteks Indonesia (data dari bi.go.id), dan $\sigma$ adalah standar deviasi *return* harian. Konversi: $R_{f,daily} = (1 + R_{f,annual})^{1/252} - 1$.

**4) Maximum Drawdown (MDD)**

$$MDD = \max_{t\in[0,T]}\left(\frac{Peak_t - Trough_t}{Peak_t}\right)\times 100\%$$

**5) Win-Rate (WR)**

$$WR = \frac{\text{Jumlah keputusan yang menghasilkan profit}}{\text{Total keputusan transaksi (Buy/Sell)}} \times 100\%$$

Metrik ini digunakan khusus untuk menjawab rumusan masalah #2, membandingkan akurasi keputusan antar konfigurasi *ablation study*.

### 5.5 Kriteria Keberhasilan

Sistem dinyatakan **berhasil** apabila:

1. **Performa kuantitatif**: Pada **mayoritas emiten** (minimal 2 dari 3) dan **mayoritas baseline** (minimal 3 dari 5), konfigurasi Full MAS menghasilkan:
   - CR dan AR **lebih tinggi**
   - Sharpe Ratio **lebih tinggi** (menunjukkan *return* yang lebih baik secara *risk-adjusted*)
   - Maximum Drawdown **setara atau lebih rendah** dibandingkan rata-rata strategi *rule-based*

2. **Kontribusi debat**: Konfigurasi Full MAS menghasilkan Win-Rate **minimal 10% lebih tinggi** dibandingkan konfigurasi MAS tanpa Debat, yang diuji pada mayoritas emiten.

3. **Eksplainabilitas**: Sistem mampu menghasilkan *reasoning trace* yang koheren dan dapat dipertanggungjawabkan secara naratif pada studi kasus terpilih.

### 5.6 Analisis Tambahan

Selain evaluasi kuantitatif, dilakukan:

1. **Analisis kualitatif eksplainabilitas:** Menelaah log penalaran (*reasoning trace*) pada studi kasus penting (misalnya saat pengumuman BI-7DRR atau rilis laporan keuangan kuartalan emiten) untuk menilai kualitas kolaborasi antar-agen.

2. **Analisis dampak keterbatasan data:** Membandingkan kualitas laporan agen Sentimen dan agen Macro pada konteks Indonesia (data terbatas) dengan ekspektasi pada konteks AS (data melimpah), untuk mendokumentasikan dampak *data gap* terhadap kualitas keputusan.

### 5.7 Visualisasi Hasil yang Direncanakan

- Grafik perbandingan *cumulative return* konfigurasi Full MAS vs. seluruh baseline per emiten.
- Tabel ringkasan CR/AR/SR/MDD/WR seluruh strategi dan konfigurasi *ablation* (format serupa Tabel 1 pada paper acuan [1]).
- Grafik riwayat transaksi (sinyal *buy/sell*) yang di-*overlay* pada grafik *candlestick* harga saham.
- *Heatmap* perbandingan kinerja 3 konfigurasi *ablation study* pada 3 emiten.
- Contoh *reasoning trace* terseleksi dalam format *expandable* untuk analisis kualitatif.

---

## BAB VI. JADWAL PENELITIAN

| Fase | Durasi | Aktivitas Utama |
|------|--------|-----------------|
| **Fase 1: Persiapan** | 2–3 minggu | Konfigurasi environment (Python, LangGraph, Ollama, Backtrader); implementasi *tools* data fetcher (yfinance, RSS parser); kompilasi data fundamental manual; pengumpulan dan caching data |
| **Fase 2: Implementasi Agen** | 3–4 minggu | Implementasi 12 agen (4 analis + 3 researcher + 1 trader + 3 risk mgmt + 1 portfolio manager); desain *system prompt*; mekanisme debat |
| **Fase 3: Orkestrasi & UI** | 2 minggu | Integrasi LangGraph *workflow*; antarmuka Streamlit + CLI; *rate limiter* |
| **Fase 4: Backtesting** | 2–3 minggu | Simulasi pada 3 emiten × 3 konfigurasi *ablation*; perhitungan metrik; perbandingan baseline |
| **Fase 5: Analisis & Laporan** | 2–3 minggu | Analisis kuantitatif dan kualitatif; visualisasi; penyusunan laporan skripsi |
| **Total** | **~11–15 minggu** | |

---

## PENUTUP

Proposal revisi ini menyajikan kerangka penelitian yang mengadaptasi arsitektur *TradingAgents* [1] ke konteks saham sektor perbankan IHSG, dengan penyempurnaan berikut dibandingkan draft awal:

1. **Sumber data yang spesifik dan realistis** — menggantikan asumsi "API publik" dengan identifikasi konkret sumber data (yfinance, Google News RSS, RSS portal berita Indonesia, data fundamental manual, BI-7DRR).
2. **Komponen arsitektur yang lengkap** — penambahan Debate Facilitator, definisi TradingState, dan strategi penanganan multibahasa.
3. **Desain eksperimen yang lebih kuat** — *ablation study* 3 konfigurasi, metrik Win-Rate, kriteria keberhasilan yang realistis.
4. **Strategi implementasi yang efisien** — model LLM bertingkat (Ollama → Gemini/Groq free-tier), caching data, dan *rate limiter*.
5. **Penyederhanaan lingkup** — fokus pada 3 emiten *big-cap*, dengan sistem yang tetap modular untuk ekspansi.

Struktur di atas dirancang agar dapat langsung diimplementasikan menggunakan kerangka kerja open-source tanpa memerlukan sumber daya komputasi GPU maupun API berbayar, sejalan dengan prinsip aksesibilitas dan reprodusibilitas penelitian.

---

## DAFTAR PUSTAKA

[1] Y. Xiao, E. Sun, D. Luo, and W. Wang, "TradingAgents: Multi-Agents LLM Financial Trading Framework," *arXiv preprint arXiv:2412.20138v7*, Jun. 2025. [Online]. Available: https://arxiv.org/abs/2412.20138

[2] S. Hong *et al.*, "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," *arXiv preprint arXiv:2308.00352*, 2024. [Online]. Available: https://arxiv.org/abs/2308.00352

[3] Y. Yu *et al.*, "FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making," *Proc. NeurIPS 2024*, 2024. [Online]. Available: https://arxiv.org/abs/2407.06567

[4] S. Wu *et al.*, "BloombergGPT: A Large Language Model for Finance," *arXiv preprint arXiv:2303.17564*, 2023. [Online]. Available: https://arxiv.org/abs/2303.17564

[5] Y. Yu *et al.*, "FinMem: A Performance-Enhanced LLM Trading Agent with Layered Memory and Character Design," *arXiv preprint arXiv:2311.13743*, 2023. [Online]. Available: https://arxiv.org/abs/2311.13743
