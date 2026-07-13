# SISTEM DOKUMENTASI
## Multi-Agent System untuk Sistem Pendukung Keputusan Investasi Saham pada Sektor Perbankan di IHSG

> Dokumen ini merupakan dokumentasi teknis dan akademis menyeluruh dari proyek Multi-Agent System (MAS) yang dikembangkan sebagai bagian dari penelitian skripsi. Seluruh isi dokumen disusun secara sistematis dan konsisten dengan desain sistem yang telah diimplementasikan.

---

## Daftar Isi

1. [Profil Penelitian](#1-profil-penelitian)
   - 1.1 [Judul Penelitian](#11-judul-penelitian)
   - 1.2 [Pengertian Sistem](#12-pengertian-sistem)
   - 1.3 [Tujuan dan Manfaat](#13-tujuan-dan-manfaat)
   - 1.4 [Batasan Masalah](#14-batasan-masalah)
2. [Metodologi dan Perancangan Sistem](#2-metodologi-dan-perancangan-sistem)
   - 2.1 [Arsitektur Agen](#21-arsitektur-agen)
   - 2.2 [Justifikasi Modifikasi Arsitektur](#22-justifikasi-modifikasi-arsitektur)
   - 2.3 [Mekanisme Debat dan Konsensus](#23-mekanisme-debat-dan-konsensus)
   - 2.4 [Teknologi AI: LLM sebagai Engine Penalaran](#24-teknologi-ai-llm-sebagai-engine-penalaran)
3. [Alur Kerja (Workflow)](#3-alur-kerja-workflow)
   - 3.1 [Interaksi Antar-Agen](#31-interaksi-antar-agen)
   - 3.2 [Proses End-to-End](#32-proses-end-to-end)
4. [Struktur Proyek](#4-struktur-proyek)
   - 4.1 [Tabel Struktur Folder](#41-tabel-struktur-folder)
   - 4.2 [Penjelasan File Utama](#42-penjelasan-file-utama)
5. [Daftar Pustaka](#5-daftar-pustaka)

---

## 1. Profil Penelitian

### 1.1 Judul Penelitian

**"Penerapan Multi-Agent System untuk Sistem Pendukung Keputusan Investasi Saham pada Sektor Perbankan di IHSG"**

Penelitian ini merupakan studi replikasi dan adaptasi (*replication and domain adaptation study*) dari kerangka kerja TradingAgents (Xiao et al., 2025) yang dikembangkan untuk pasar saham Amerika Serikat. Kontribusi orisinal penelitian ini terletak pada adaptasi arsitektur multi-agen tersebut ke konteks pasar modal Indonesia, khususnya sektor perbankan yang terdaftar di Bursa Efek Indonesia (IHSG).

### 1.2 Pengertian Sistem

Sistem Pendukung Keputusan (SPK) berbasis Multi-Agent System (MAS) dalam konteks penelitian ini didefinisikan sebagai sebuah sistem perangkat lunak yang terdiri atas sekumpulan agen cerdas otonom — masing-masing didukung oleh Large Language Model (LLM) — yang berkolaborasi untuk menganalisis data pasar saham dari berbagai perspektif (fundamental, teknikal, sentimen, dan makroekonomi) dan menghasilkan rekomendasi investasi terstruktur berupa keputusan Buy, Hold, atau Sell.

Setiap agen dalam sistem ini memiliki peran terspesialisasi yang meniru struktur organisasi firma investasi nyata (*real-world trading firm*). Agen-agen tersebut berkomunikasi melalui sebuah *global shared state* — suatu struktur data terpusat yang menjadi wadah pertukaran informasi — sehingga setiap agen dapat membaca output agen lain secara langsung tanpa degradasi informasi (*telephone effect*). Pola komunikasi ini mengadopsi paradigma *publish-subscribe* yang diperkenalkan oleh MetaGPT (Hong et al., 2024).

Keunggulan utama pendekatan MAS berbasis LLM dibandingkan sistem pendukung keputusan konvensional adalah kemampuannya untuk:

1. **Memproses data multimodal** — mengintegrasikan data numerik (harga, rasio keuangan, indikator teknikal) dengan data tekstual (berita, laporan keuangan) dalam satu pipeline penalaran.
2. **Menghasilkan keputusan yang *explainable*** — setiap rekomendasi disertai jejak penalaran (*reasoning trace*) dari seluruh agen, sehingga pengguna dapat menelusuri logika di balik setiap keputusan.
3. **Memanfaatkan mekanisme debat dialektik** — argumen pro (bullish) dan kontra (bearish) dipertandingkan secara eksplisit sebelum mencapai konsensus, mengurangi bias konfirmasi yang umum terjadi pada agen tunggal.

### 1.3 Tujuan dan Manfaat

#### 1.3.1 Tujuan Penelitian

1. **Merancang dan mengimplementasikan arsitektur Multi-Agent System** yang terdiri atas 12 agen terspesialisasi — meliputi Tim Analis (Fundamental, Sentimen, Macro, Teknikal), Tim Peneliti (Bullish Researcher, Bearish Researcher, Research Facilitator), Tim Manajemen Risiko (Aggressive Risk Analyst, Conservative Risk Analyst, Risk Facilitator), serta Tim Eksekusi (Portfolio Manager, Trading Agent) — yang mampu memproses data saham perbankan IHSG dan menghasilkan keputusan investasi terstruktur.

2. **Mengukur peningkatan kualitas keputusan investasi** yang dihasilkan oleh mekanisme debat multi-agen melalui *ablation study*, membandingkan konfigurasi sistem lengkap (Full MAS dengan debat) terhadap konfigurasi MAS tanpa debat dan konfigurasi agen tunggal (*single agent*).

3. **Mengevaluasi performa sistem** melalui simulasi *backtesting* historis pada emiten *big-cap* sektor perbankan IHSG (BBCA, BBRI, BMRI) periode 2024–2025, menggunakan metrik standar industri meliputi Cumulative Return, Sharpe Ratio, Maximum Drawdown, dan Win-Rate.

#### 1.3.2 Manfaat Penelitian

**Manfaat Teoritis:**

- Memberikan bukti empiris mengenai efektivitas arsitektur Multi-Agent System berbasis LLM pada konteks pasar saham berkembang (Indonesia) dengan data berbahasa non-Inggris, memperluas validasi yang sebelumnya terbatas pada pasar Amerika Serikat.
- Mendokumentasikan tantangan dan solusi adaptasi arsitektur multi-agen ke pasar modal dengan karakteristik data, bahasa, dan regulasi yang berbeda dari konteks penelitian acuan.

**Manfaat Praktis:**

- Menghasilkan prototipe sistem pendukung keputusan investasi yang *explainable* — mampu menjelaskan alasan di balik setiap rekomendasi melalui *reasoning trace* — yang dapat dikembangkan lebih lanjut oleh peneliti maupun praktisi pasar modal Indonesia.
- Menyediakan kerangka kerja (*framework*) modular dan *ticker-agnostic* yang memungkinkan pengguna menganalisis emiten lain di luar sampel penelitian hanya dengan mengubah parameter input.

### 1.4 Batasan Masalah

1. **Objek Penelitian:** Dibatasi pada emiten *big-cap* sektor perbankan IHSG, dengan BBCA.JK (Bank Central Asia) sebagai objek studi utama untuk pengembangan dan pengujian (*development and testing*). Meskipun demikian, sistem dirancang secara *ticker-agnostic* — pengguna cukup mengubah parameter `--ticker` pada saat eksekusi untuk menganalisis emiten lain (misal: BBRI.JK, BMRI.JK).

2. **Periode Data:** Data historis yang digunakan untuk simulasi *backtesting* berada pada rentang Januari 2024 – Desember 2025, menyesuaikan ketersediaan data pada saat penelitian dilakukan.

3. **Sumber Data:**
   - Data harga historis (OHLCV) diperoleh melalui *library* `yfinance` dengan format ticker Jakarta (`*.JK`).
   - Data berita keuangan diperoleh dari Google News RSS feed (dengan query berbahasa Indonesia) dan RSS feed portal berita CNBC Indonesia.
   - Data fundamental perbankan diperoleh melalui `yfinance` (laporan laba-rugi, neraca, rasio umum).
   - Penelitian **tidak menggunakan** API premium (Bloomberg, Refinitiv) maupun API berbayar (Finnhub, Alpha Vantage).

4. **Metode:** Penelitian menggunakan pendekatan Multi-Agent System (MAS) berbasis LLM dengan kerangka orkestrasi LangGraph. Setiap agen ditenagai oleh model LLM yang berjalan secara lokal melalui Ollama (Llama 3.1 8B) pada tahap pengembangan, dengan opsi migrasi ke model *free-tier* API (Google Gemini, Groq) pada tahap *backtesting* akhir.

5. **Validasi:** Seluruh evaluasi dilakukan dalam simulasi *paper trading* / *backtesting* historis. Sistem tidak melakukan eksekusi transaksi riil (*live trading*). Strategi pencegahan *look-ahead bias* diterapkan secara ketat melalui mekanisme *in-memory slicing* pada data master yang telah di-*cache*.

6. **Model LLM:** Tidak dilakukan *fine-tuning* model LLM dari awal. Sistem memanfaatkan kemampuan *zero-shot reasoning* model yang sudah tersedia (*pre-trained*), dengan pengarahan perilaku dilakukan sepenuhnya melalui *system prompt* yang terspesialisasi per agen.

---

## 2. Metodologi dan Perancangan Sistem

### 2.1 Arsitektur Agen

Sistem terdiri atas **12 agen** yang diorganisasikan dalam empat lapisan tim, diimplementasikan sebagai *node* dalam graf berarah (*directed graph*) menggunakan kerangka orkestrasi LangGraph. Berikut adalah deskripsi peran spesifik dari masing-masing agen:

#### 2.1.1 Tim Analis (*Analyst Team*) — 4 Agen, Eksekusi Paralel

Keempat agen analis bekerja secara **paralel** pada setiap siklus harian, masing-masing menerima potongan data pasar yang relevan dari *global state* dan menghasilkan laporan analisis dalam format paragraf naratif padat berbahasa Indonesia (maksimal 3 kalimat).

**1. Fundamental Analyst**

Agen ini bertugas menganalisis kesehatan keuangan dan valuasi intrinsik emiten berdasarkan data fundamental. Data input yang diproses meliputi rasio keuangan umum (P/E, P/B, *Dividend Yield*, *Market Cap*), laporan laba-rugi, dan neraca yang diperoleh dari `yfinance`. Agen ini mengevaluasi apakah saham *undervalued*, *fairly valued*, atau *overvalued* berdasarkan metrik valuasi, serta menilai tren profitabilitas perusahaan. *System prompt* agen ini diperkaya dengan glosarium keuangan Indonesia (NPL, CAR, NIM, DPK, IHSG) untuk memastikan pemahaman kontekstual terhadap istilah perbankan lokal.

Implementasi: `agents/analysts.py` → fungsi `fundamental_analyst()`, menggunakan *prompt* dari `config/prompts/analyst_prompts.py` → `FUNDAMENTAL_ANALYST_PROMPT`, membaca data dari `state["market_data"]["fundamentals"]`.

**2. Macro Analyst**

Agen ini berfokus pada analisis kondisi makroekonomi Indonesia dan dampaknya terhadap sektor perbankan. Agen mengevaluasi implikasi kebijakan suku bunga Bank Indonesia (BI-7DRR), regulasi Otoritas Jasa Keuangan (OJK), kondisi inflasi, nilai tukar rupiah, dan dinamika ekonomi global terhadap kinerja saham perbankan. Secara khusus, agen ini menilai bagaimana perubahan suku bunga acuan memengaruhi *Net Interest Margin* (NIM) emiten perbankan — yang merupakan sumber pendapatan utama bank di Indonesia.

Implementasi: `agents/analysts.py` → fungsi `macro_analyst()`, menggunakan *prompt* `MACRO_ANALYST_PROMPT`, membaca data dari `state["market_data"]["news"]`.

**3. Sentiment Analyst**

Agen ini bertugas menganalisis sentimen pasar terhadap emiten berdasarkan berita keuangan terkini berbahasa Indonesia. Data input berupa daftar *headline* berita yang diperoleh dari Google News RSS dan CNBC Indonesia RSS. Agen mengklasifikasikan sentimen keseluruhan sebagai Positif, Negatif, atau Netral, serta mengidentifikasi katalis atau kekhawatiran utama yang tercermin dalam pemberitaan. Kemampuan LLM untuk memproses teks berbahasa Indonesia secara langsung (*zero-shot multilingual*) menjadi keunggulan kritis agen ini.

Implementasi: `agents/analysts.py` → fungsi `sentiment_analyst()`, menggunakan *prompt* `SENTIMENT_ANALYST_PROMPT`, membaca data dari `state["market_data"]["news"]`.

**4. Technical Analyst**

Agen ini menganalisis indikator teknikal yang dihitung dari data harga historis (OHLCV) untuk mengidentifikasi tren harga dan momentum. Indikator yang dikalkulasi meliputi: MACD (*Moving Average Convergence Divergence*), RSI-14 (*Relative Strength Index* 14 hari), Bollinger Bands (upper, middle, lower), KDJ (*Stochastic Oscillator*), SMA-20 (*Simple Moving Average* 20 hari), dan SMA-50 (50 hari). Agen menentukan apakah kondisi pasar menunjukkan *overbought*/*oversold* (berdasarkan RSI dan KDJ), arah tren (berdasarkan MACD dan SMA), serta apakah *setup* saat ini bersifat *bullish* atau *bearish*.

Implementasi: `agents/analysts.py` → fungsi `technical_analyst()`, menggunakan *prompt* `TECHNICAL_ANALYST_PROMPT`, membaca data dari `state["market_data"]["indicators"]` yang telah dikalkulasi oleh modul `tools/indicator_calculator.py` menggunakan *library* `stockstats`.

#### 2.1.2 Tim Peneliti (*Researcher Team*) — 3 Agen, Mekanisme Debat

Tim Peneliti menerima seluruh laporan dari keempat agen analis dan melakukan sintesis melalui mekanisme debat dialektik.

**5. Bullish Researcher**

Agen ini berperan sebagai advokat posisi investasi positif. Tugas utamanya adalah meninjau seluruh laporan Tim Analis dan menyusun argumen sekuat mungkin mengenai **mengapa saham layak dibeli** (*buy case*). Agen ini secara deliberate berfokus pada sinyal-sinyal positif yang teridentifikasi di keempat laporan analis — valuasi menarik, momentum teknikal positif, sentimen pasar mendukung, dan kondisi makroekonomi kondusif — dan merangkainya menjadi narasi *bullish* yang persuasif namun tetap berdasarkan data.

Implementasi: `agents/researchers.py` → fungsi `bullish_researcher()`, menggunakan *prompt* `BULLISH_PROMPT`, membaca dari `state["analyst_reports"]`.

**6. Bearish Researcher**

Agen ini berperan sebagai advokat posisi investasi negatif — kebalikan eksak dari Bullish Researcher. Tugas utamanya adalah menyusun argumen sekuat mungkin mengenai **mengapa saham sebaiknya dijual atau dihindari** (*sell case* / *avoid case*). Agen ini secara deliberate berfokus pada risiko dan sinyal negatif dari keempat laporan analis — valuasi mahal, momentum teknikal melemah, sentimen negatif, dan risiko makroekonomi — dan merangkainya menjadi narasi *bearish* yang persuasif.

Implementasi: `agents/researchers.py` → fungsi `bearish_researcher()`, menggunakan *prompt* `BEARISH_PROMPT`, membaca dari `state["analyst_reports"]`.

**7. Research Facilitator**

Agen ini berfungsi sebagai moderator dan penilai objektif dari debat antara Bullish Researcher dan Bearish Researcher. Tugas utamanya adalah menimbang kekuatan argumen kedua pihak secara berimbang, menentukan apakah bukti secara keseluruhan condong ke arah *Bullish*, *Bearish*, atau *Neutral*, dan menghasilkan sintesis terstruktur yang menangkap argumen terkuat dari kedua sisi. Output dari agen ini disebut **Research Consensus** — yang menjadi input bagi Tim Manajemen Risiko pada tahap selanjutnya.

Implementasi: `agents/researchers.py` → fungsi `research_facilitator()`, menggunakan *prompt* `RESEARCH_FACILITATOR_PROMPT`, membaca dari `state["research_debate"]`.

#### 2.1.3 Tim Manajemen Risiko (*Risk Management Team*) — 3 Agen, Mekanisme Debat

Tim Manajemen Risiko menerima *Research Consensus* dan mengevaluasinya dari dua perspektif risiko yang saling berlawanan.

**8. Aggressive Risk Analyst**

Agen ini mengevaluasi *Research Consensus* dari perspektif pengambilan risiko secara maksimal demi *return* yang tinggi. Fokus utamanya adalah pada biaya peluang (*opportunity cost*) dan potensi keuntungan. Jika konsensus riset bersifat *bullish*, agen ini berargumen mengapa risiko yang ada dapat diterima dan mengapa posisi investasi sebaiknya dimaksimalkan. Jika konsensus bersifat *bearish*, agen ini berusaha mengidentifikasi potensi *contrarian upside* — peluang keuntungan yang mungkin terlewatkan oleh analisis konvensional.

Implementasi: `agents/risk_management.py` → fungsi `aggressive_risk_analyst()`, menggunakan *prompt* `AGGRESSIVE_RISK_PROMPT`, membaca dari `state["research_consensus"]`.

**9. Conservative Risk Analyst**

Agen ini mengevaluasi *Research Consensus* dari perspektif kehati-hatian dan pelestarian modal (*capital preservation*). Fokus utamanya adalah pada perlindungan terhadap risiko penurunan (*downside protection*). Agen ini secara aktif mengidentifikasi risiko makroekonomi, fundamental, atau teknikal yang berpotensi menyebabkan *drawdown* signifikan. Jika konsensus riset bersifat *bullish*, agen ini berargumen mengapa investor sebaiknya membatasi ukuran posisi atau menunggu konfirmasi lebih lanjut sebelum masuk.

Implementasi: `agents/risk_management.py` → fungsi `conservative_risk_analyst()`, menggunakan *prompt* `CONSERVATIVE_RISK_PROMPT`, membaca dari `state["research_consensus"]`.

**10. Risk Facilitator**

Agen ini berperan sebagai moderator dan penilai objektif dari debat antara Aggressive Risk Analyst dan Conservative Risk Analyst. Tugas utamanya adalah menyeimbangkan kebutuhan pelestarian modal dengan peluang *return*, menghasilkan penilaian risiko akhir (Low Risk, Moderate Risk, atau High Risk), dan menyediakan panduan konkret mengenai ukuran posisi (*position sizing*) yang sesuai dengan tingkat risiko tersebut. Output dari agen ini disebut **Risk Consensus** — yang menjadi input bagi Portfolio Manager pada tahap selanjutnya.

Implementasi: `agents/risk_management.py` → fungsi `risk_facilitator()`, menggunakan *prompt* `RISK_FACILITATOR_PROMPT`, membaca dari `state["risk_debate"]` dan `state["research_consensus"]`.

#### 2.1.4 Tim Eksekusi (*Execution Team*) — 2 Agen, Eksekusi Sekuensial

**11. Portfolio Manager**

Agen ini memiliki kewenangan keputusan final atas strategi investasi keseluruhan. Agen menerima tiga input utama: (1) *Research Consensus* dari Tim Peneliti, (2) *Risk Consensus* dari Tim Manajemen Risiko, dan (3) status portofolio terkini (saldo kas tersedia dan posisi saham yang sedang dimiliki). Berdasarkan ketiga input tersebut, Portfolio Manager memutuskan apakah akan membuka posisi baru, menambah posisi yang ada, mengurangi posisi, atau keluar sepenuhnya dari posisi. Rekomendasi disampaikan dalam format naratif eksplisit yang menyertakan alasan strategis.

Implementasi: `agents/execution.py` → fungsi `portfolio_manager()`, menggunakan *prompt* `PORTFOLIO_MANAGER_PROMPT`, membaca dari `state["research_consensus"]`, `state["risk_consensus"]`, dan `state["portfolio_status"]`.

**12. Trading Agent**

Agen ini merupakan agen terakhir dalam *pipeline* dan bertugas menerjemahkan rekomendasi naratif dari Portfolio Manager menjadi order kuantitatif yang dapat dieksekusi oleh mesin *backtesting*. Output dihasilkan dalam format JSON terstruktur yang ketat (*machine-readable*) dengan skema: `{"action": "BUY|SELL|HOLD", "quantity": int, "confidence": float}`. Kuantitas dinyatakan dalam satuan lot (1 lot = 100 lembar saham, sesuai aturan Bursa Efek Indonesia). Agen ini dilengkapi dengan mekanisme *fallback* parsing — jika LLM menghasilkan output yang tidak sesuai format JSON (misalnya menyertakan *markdown formatting*), sistem secara otomatis mengekstrak blok JSON menggunakan *regex* sebelum melakukan *fallback* ke *default* HOLD.

Implementasi: `agents/execution.py` → fungsi `trading_agent()`, menggunakan *prompt* `TRADING_AGENT_PROMPT`, membaca dari `state["portfolio_status"]["recommendation"]`.

### 2.2 Justifikasi Modifikasi Arsitektur

Sub-bab ini membandingkan arsitektur agen yang diimplementasikan dalam penelitian ini dengan struktur agen pada kerangka kerja TradingAgents (Xiao et al., 2025) yang menjadi jurnal referensi utama, serta menjelaskan alasan akademis di balik setiap penyesuaian yang dilakukan.

#### 2.2.1 Perbandingan Struktural

| Aspek | TradingAgents (Paper Acuan) | Sistem Penelitian Ini |
|-------|----------------------------|----------------------|
| **Tim Analis** | 4 agen: Fundamentals, News, Social Media, Technical | 4 agen: Fundamental, **Macro**, **Sentiment**, Technical |
| **Tim Peneliti** | 2 agen: Bull Researcher, Bear Researcher + 1 Research Manager | 2 agen: Bullish Researcher, Bearish Researcher + 1 **Research Facilitator** |
| **Manajemen Risiko** | 1 agen: Risk Manager (terintegrasi dengan Trader) | **3 agen terpisah**: Aggressive Risk, Conservative Risk, **Risk Facilitator** |
| **Eksekusi** | 1 agen: Trader (gabungan keputusan trading + risiko) | **2 agen terpisah**: Portfolio Manager + Trading Agent |
| **Total Agen** | ~8 agen | **12 agen** |
| **Sumber Data Berita** | Finnhub, Reddit (API berbahasa Inggris) | Google News RSS, CNBC Indonesia RSS (berbahasa Indonesia) |
| **Data Fundamental** | Alpha Vantage, Finnhub (API terstruktur) | yfinance (ticker `*.JK`) |
| **Indikator Teknikal** | Dihitung via API eksternal | Dihitung lokal via `stockstats` (*in-memory*) |

#### 2.2.2 Alasan Penyesuaian

**Penyesuaian 1: Pengelompokan Ulang Fungsi Analis**

Paper acuan membagi agen analis menjadi Fundamentals, News, Social Media, dan Technical. Penelitian ini menggabungkan fungsi agen News dan Social Media menjadi satu **Sentiment Analyst** dan menambahkan **Macro Analyst** sebagai agen terpisah.

Justifikasi akademis:
- Di pasar modal Indonesia, sumber data sentimen dari media sosial (Reddit, StockTwits) tidak memiliki volume dan kualitas yang setara dengan pasar AS. Forum investor lokal (seperti Stockbit) tidak menyediakan API publik yang dapat diintegrasikan secara programatis. Oleh karena itu, fungsi analisis sentimen dikonsolidasikan menjadi satu agen yang memproses *headline* berita dari Google News RSS dan portal berita keuangan Indonesia.
- Sebaliknya, faktor makroekonomi memiliki pengaruh yang sangat signifikan terhadap saham perbankan Indonesia — khususnya kebijakan suku bunga BI-7DRR yang secara langsung memengaruhi *Net Interest Margin* (NIM) dan profitabilitas bank. Pemisahan agen Macro dari agen Sentiment memungkinkan sistem memberikan perhatian terdedikasi pada analisis dampak kebijakan moneter, regulasi OJK, dan dinamika makroekonomi domestik.

**Penyesuaian 2: Pemisahan dan Perluasan Tim Manajemen Risiko**

Paper acuan menggunakan satu agen Risk Manager yang terintegrasi dengan Trader. Penelitian ini memisahkan fungsi manajemen risiko menjadi **tiga agen terpisah** (Aggressive Risk Analyst, Conservative Risk Analyst, dan Risk Facilitator) dengan mekanisme debat internal.

Justifikasi akademis:
- Pasar modal Indonesia memiliki karakteristik volatilitas dan likuiditas yang berbeda dari pasar Nasdaq. Saham-saham perbankan IHSG, meskipun tergolong *big-cap*, dapat mengalami fluktuasi harga signifikan akibat sentimen domestik (misalnya perubahan kebijakan BI-7DRR, regulasi OJK, atau gejolak politik). Oleh karena itu, evaluasi risiko yang lebih granular dan dialektik diperlukan.
- Mekanisme debat pada Tim Manajemen Risiko mencerminkan praktik nyata komite risiko (*risk committee*) pada firma investasi, di mana perspektif agresif dan konservatif dipertandingkan secara eksplisit sebelum mencapai konsensus. Hal ini merupakan kontribusi desain orisinal penelitian ini yang tidak terdapat pada arsitektur paper acuan.
- Pemisahan ini memungkinkan *ablation study* yang lebih kaya — peneliti dapat menguji kontribusi spesifik mekanisme debat risiko terhadap kualitas keputusan akhir.

**Penyesuaian 3: Pemisahan Portfolio Manager dan Trading Agent**

Paper acuan menggabungkan fungsi keputusan strategis dan eksekusi order dalam satu agen Trader. Penelitian ini memisahkan menjadi **Portfolio Manager** (keputusan strategis) dan **Trading Agent** (translasi ke order kuantitatif).

Justifikasi akademis:
- Pemisahan ini mengikuti prinsip *separation of concerns* — keputusan investasi strategis (apakah membeli/menjual dan berapa besar alokasi) merupakan fungsi yang secara konseptual berbeda dari penerjemahan keputusan tersebut ke dalam format order yang dapat dieksekusi (jumlah lot, format JSON).
- Dari perspektif *explainability*, pemisahan ini menghasilkan *reasoning trace* yang lebih transparan: pengguna dapat menelusuri secara terpisah logika keputusan strategis Portfolio Manager dan logika kuantifikasi Trading Agent.
- Pemisahan ini juga meningkatkan keandalan (*reliability*) sistem — jika Trading Agent gagal menghasilkan JSON yang valid, Portfolio Manager tidak perlu dieksekusi ulang.

### 2.3 Mekanisme Debat dan Konsensus

Mekanisme debat merupakan komponen inti dari arsitektur MAS ini yang membedakannya dari pendekatan agen tunggal. Sistem mengimplementasikan **dua lapisan debat** yang beroperasi secara sekuensial:

#### 2.3.1 Debat Lapisan 1: Bullish vs Bearish Researcher

**Alur Debat:**

1. Kedua Researcher — Bullish dan Bearish — menerima **seluruh** laporan Tim Analis secara paralel dari `state["analyst_reports"]`.
2. Masing-masing Researcher menyusun argumen dari perspektifnya secara independen dan simultan.
3. Bullish Researcher menyajikan argumen investasi positif — menekankan sinyal-sinyal mendukung dari data fundamental, teknikal, sentimen, dan makroekonomi.
4. Bearish Researcher menyajikan argumen peringatan — menekankan risiko dan sinyal negatif dari sumber data yang sama.
5. Kedua argumen disimpan dalam `state["research_debate"]` sebagai *list* pesan terstruktur `[{"agent": "Bullish", "message": "..."}, {"agent": "Bearish", "message": "..."}]`.
6. **Research Facilitator** membaca seluruh argumen dari kedua pihak, menimbang kekuatan relatif masing-masing, dan menghasilkan **Research Consensus** — sintesis objektif yang menentukan apakah bukti secara keseluruhan condong *Bullish*, *Bearish*, atau *Neutral*.

**Prinsip Desain:**
- Setiap agen membaca dari *sumber primer* (laporan analis langsung dari *global state*), bukan dari parafrase agen sebelumnya, untuk mencegah *telephone effect* (degradasi informasi antar-agen) sesuai prinsip MetaGPT (Hong et al., 2024).
- Format output setiap agen dibatasi pada paragraf naratif padat maksimal 3 kalimat dalam bahasa Indonesia formal, tanpa format *markdown*, untuk menjamin konsistensi dan estetika *logging* terminal.

#### 2.3.2 Debat Lapisan 2: Aggressive vs Conservative Risk Analyst

**Alur Debat:**

1. Kedua Risk Analyst menerima **Research Consensus** dari `state["research_consensus"]` secara paralel.
2. Aggressive Risk Analyst mengevaluasi potensi keuntungan relatif terhadap risiko — berargumen mengapa risiko yang teridentifikasi dapat diterima dan posisi sebaiknya dimaksimalkan.
3. Conservative Risk Analyst mengevaluasi potensi kerugian dan risiko *drawdown* — berargumen mengapa posisi sebaiknya dibatasi atau ditunda.
4. Kedua argumen disimpan dalam `state["risk_debate"]`.
5. **Risk Facilitator** membaca argumen kedua pihak beserta *Research Consensus* asli, dan menghasilkan **Risk Consensus** — penilaian risiko akhir (Low/Moderate/High Risk) beserta panduan *position sizing*.

#### 2.3.3 Dari Konsensus ke Keputusan Akhir

Setelah kedua lapisan debat selesai, alur keputusan berlanjut secara sekuensial:

1. **Portfolio Manager** menerima *Research Consensus* dan *Risk Consensus*, serta data status portofolio terkini (saldo kas, jumlah saham yang dimiliki). Berdasarkan ketiga input ini, Portfolio Manager merumuskan rekomendasi strategis — apakah membuka posisi baru, menambah, mengurangi, atau keluar dari posisi.

2. **Trading Agent** menerima rekomendasi naratif Portfolio Manager dan menerjemahkannya menjadi order kuantitatif dalam format JSON: `{"action": "BUY|SELL|HOLD", "quantity": <lot>, "confidence": <0.0-1.0>}`.

3. **Engine Backtester** (`orchestration/backtester.py`) menerima output JSON dari Trading Agent dan mengeksekusi order sesuai aturan pasar Indonesia (1 lot = 100 saham, biaya transaksi 0,2%), memperbarui saldo kas dan posisi saham pada *global state*.

### 2.4 Teknologi AI: LLM sebagai Engine Penalaran

#### 2.4.1 Mengapa LLM, Bukan Metode Tradisional?

Penelitian ini memilih pendekatan Multi-Agent berbasis Large Language Model (LLM) sebagai *engine* penalaran untuk setiap agen, alih-alih metode tradisional (seperti model *machine learning* statistik, *neural network* prediktif, atau sistem pakar berbasis aturan). Pilihan ini didasarkan pada beberapa pertimbangan akademis berikut:

1. **Kemampuan pemrosesan data multimodal.** Metode tradisional umumnya hanya mampu memproses satu jenis data — *time series* numerik untuk prediksi harga, atau model NLP terpisah untuk analisis sentimen. LLM secara inheren mampu mengintegrasikan data numerik (harga, rasio keuangan, indikator teknikal) dan data tekstual (berita, laporan keuangan) dalam satu konteks penalaran, menghasilkan analisis yang lebih holistik.

2. **Pemahaman kontekstual multibahasa.** Penelitian ini memerlukan pemrosesan teks berita berbahasa Indonesia. Model LLM *pre-trained* modern (Llama 3.1, Gemini) telah terpapar data multilingual dalam volume besar selama proses pelatihan, sehingga mampu memahami dan menganalisis teks berbahasa Indonesia tanpa memerlukan tahap translasi terpisah atau *fine-tuning* khusus.

3. **Explainability.** Berbeda dengan model *black-box* (seperti *deep neural network* atau *ensemble model*) yang hanya menghasilkan prediksi numerik tanpa penjelasan, setiap agen LLM menghasilkan *reasoning trace* dalam bahasa alami — penjelasan eksplisit mengenai logika di balik setiap rekomendasi. Aspek *explainability* ini krusial untuk konteks sistem pendukung keputusan, di mana pengguna perlu memahami *mengapa* suatu rekomendasi diberikan.

4. **Fleksibilitas peran melalui *prompt engineering*.** Satu model LLM yang sama dapat berperan sebagai analis fundamental, analis sentimen, atau *risk analyst* hanya dengan mengganti *system prompt*. Hal ini menghilangkan kebutuhan untuk melatih model terpisah untuk setiap fungsi.

#### 2.4.2 Implementasi LLM: Ollama sebagai Engine Lokal

Sistem menggunakan **Ollama** sebagai *runtime engine* untuk menjalankan model LLM secara lokal pada mesin pengembang. Konfigurasi model diatur dalam file `config/llm_config.py` dengan strategi *role-based temperature*:

| Peran Agen | Model | Temperature | Alasan |
|------------|-------|-------------|--------|
| Analyst, Facilitator, PM, Trader | `llama3.1:latest` | 0.0 | Memerlukan output faktual dan deterministik — analisis harus konsisten dan tidak kreatif |
| Researcher (Debater) | `llama3.1:latest` | 0.7 | Memerlukan output argumentatif dan kreatif — debater perlu menyusun argumen persuasif dari perspektif yang berbeda |

Sistem juga mendukung provider LLM alternatif untuk tahap *backtesting* akhir:
- **Google Gemini** (`gemini-2.0-flash`) melalui *package* `langchain-google-genai`
- **Groq** (`llama-3.3-70b-versatile`) melalui *package* `langchain-groq`

Pemilihan provider dilakukan melalui parameter `provider` pada fungsi `get_llm()`, memungkinkan migrasi antar-provider tanpa mengubah kode agen.

#### 2.4.3 Kerangka Orkestrasi: LangGraph

Orkestrasi seluruh agen dilakukan menggunakan **LangGraph** — sebuah *library* dari ekosistem LangChain yang menyediakan abstraksi *StateGraph* untuk membangun *workflow* berbasis graf berarah. LangGraph dipilih karena:

1. Implementasi asli TradingAgents (Xiao et al., 2025) menggunakan LangGraph, meminimalkan *effort* adaptasi dari paper acuan ke implementasi penelitian ini.
2. LangGraph menyediakan kontrol granular atas *state machine* dan alur eksekusi — mendukung eksekusi paralel (untuk 4 agen analis) dan *fan-in/fan-out pattern* (menunggu semua agen paralel selesai sebelum melanjutkan ke tahap berikutnya).
3. LangGraph secara native mengelola *global state* dengan dukungan *custom reducer* — memungkinkan beberapa agen menulis ke kunci yang sama pada *state* secara paralel tanpa konflik (*race condition*).

---

## 3. Alur Kerja (Workflow)

### 3.1 Interaksi Antar-Agen

Seluruh komunikasi antar-agen dilakukan melalui **TradingState** — sebuah *global shared state* yang didefinisikan sebagai `TypedDict` Python dalam file `orchestration/state.py`. Setiap agen membaca data input dari *state* dan menulis hasil outputnya kembali ke *state*. Tidak ada komunikasi langsung (pesan) antar-agen — pola komunikasi ini mengadopsi paradigma *publish-subscribe* dari MetaGPT.

**Diagram Alur Data (*Data Flow*):**

```
                         ┌─────────────────────────────────────┐
                         │           INPUT PENGGUNA             │
                         │  (ticker, start_date, end_date,      │
                         │   initial_capital)                   │
                         └──────────────┬──────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────────────┐
                         │      DATA PIPELINE (Backtester)      │
                         │  ┌────────┐ ┌──────────┐ ┌────────┐ │
                         │  │ OHLCV  │ │Fundamntal│ │ Berita │ │
                         │  │yfinance│ │ yfinance │ │  RSS   │ │
                         │  └───┬────┘ └────┬─────┘ └───┬────┘ │
                         │      └─────┬─────┴─────┬─────┘      │
                         │            ▼           ▼            │
                         │  [Indikator Teknikal]  [Cache]      │
                         │     (stockstats)       (master_*)   │
                         └──────────────┬──────────────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │   FUNDAMENTAL     │   │   SENTIMENT      │   │   MACRO          │
   │   ANALYST         │   │   ANALYST         │   │   ANALYST        │
   │                   │   │                   │   │                  │
   │ Input: fundamntls │   │ Input: news       │   │ Input: news      │
   │ Output: laporan   │   │ Output: laporan   │   │ Output: laporan  │
   └────────┬──────────┘   └────────┬──────────┘   └────────┬─────────┘
            │                       │                        │
            │    ┌──────────────────┐                        │
            │    │   TECHNICAL      │                        │
            │    │   ANALYST        │                        │
            │    │                  │                        │
            │    │ Input: indicators│                        │
            │    │ Output: laporan  │                        │
            │    └────────┬─────────┘                        │
            │             │                                  │
            └──────┬──────┴──────────────┬───────────────────┘
                   │                     │
                   ▼                     ▼
    ┌──────────────────────┐  ┌──────────────────────┐
    │  BULLISH RESEARCHER  │  │  BEARISH RESEARCHER  │
    │                      │  │                      │
    │ Input: 4 laporan     │  │ Input: 4 laporan     │
    │ Output: argumen beli │  │ Output: argumen jual │
    └──────────┬───────────┘  └──────────┬───────────┘
               │                         │
               └────────────┬────────────┘
                            ▼
              ┌──────────────────────────┐
              │  RESEARCH FACILITATOR    │
              │                          │
              │ Input: argumen debat     │
              │ Output: Research         │
              │         Consensus        │
              └────────────┬─────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼                             ▼
┌──────────────────────┐   ┌──────────────────────┐
│  AGGRESSIVE RISK     │   │  CONSERVATIVE RISK   │
│  ANALYST             │   │  ANALYST             │
│                      │   │                      │
│ Input: res. consensus│   │ Input: res. consensus│
│ Output: argumen risk │   │ Output: argumen risk │
└──────────┬───────────┘   └──────────┬───────────┘
           │                          │
           └────────────┬─────────────┘
                        ▼
          ┌──────────────────────────┐
          │     RISK FACILITATOR     │
          │                          │
          │ Input: argumen risiko +  │
          │        res. consensus    │
          │ Output: Risk Consensus   │
          └────────────┬─────────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │   PORTFOLIO MANAGER      │
          │                          │
          │ Input: res. consensus +  │
          │        risk consensus +  │
          │        portfolio status  │
          │ Output: rekomendasi      │
          └────────────┬─────────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │     TRADING AGENT        │
          │                          │
          │ Input: rekomendasi PM    │
          │ Output: JSON order       │
          │ {action, quantity,       │
          │  confidence}             │
          └────────────┬─────────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │    EKSEKUSI ORDER         │
          │   (Backtester Engine)     │
          │                          │
          │ → Update saldo & posisi  │
          │ → Catat NAV harian       │
          │ → Log transaksi          │
          └──────────────────────────┘
```

### 3.2 Proses End-to-End

Berikut adalah langkah-langkah lengkap yang terjadi ketika sistem menerima input dari pengguna hingga menghasilkan output akhir:

#### Tahap 0: Inisialisasi (Satu Kali)

1. Pengguna menjalankan sistem melalui CLI dengan parameter:
   ```
   python main.py --ticker BBCA.JK --start 2024-01-01 --end 2024-01-31 --capital 100000000
   ```

2. `main.py` menginisialisasi objek `Backtester` dengan parameter yang diberikan.

3. Backtester membuat instansi seluruh komponen pendukung:
   - `CacheManager` — pengelola *cache* data di `data/cache/`
   - `YFinanceFetcher` — pengambil data OHLCV dan fundamental dari Yahoo Finance
   - `TechnicalIndicatorCalculator` — kalkulator indikator teknikal berbasis `stockstats`
   - `NewsFetcher` — pengambil berita dari Google News RSS dan CNBC Indonesia RSS
   - `create_trading_graph()` — kompilasi graf LangGraph yang mendefinisikan *workflow* 12 agen

#### Tahap 1: Persiapan Data (*Data Pipeline*) — Satu Kali

4. Backtester menjalankan `_prepare_data()` yang melakukan:
   - **Cleanup Legacy:** Menghapus folder-folder per-tanggal dari arsitektur lama (jika ada).
   - **Download/Load OHLCV:** Jika `master_ohlcv.csv` sudah ada di *cache* dan mencakup rentang tanggal yang diminta, data dimuat dari *cache*. Jika tidak, data diunduh dari Yahoo Finance dengan *lookback* 2 tahun (untuk perhitungan SMA-200 dan indikator teknikal lainnya) dan disimpan sebagai master CSV.
   - **Download/Load Fundamentals:** Proses serupa untuk `master_fundamentals.json`.
   - **Download/Load News:** Proses serupa untuk `master_news.json`.
   - **Identifikasi Tanggal Trading:** Menentukan tanggal-tanggal perdagangan valid dalam rentang yang diminta berdasarkan data OHLCV (mengecualikan akhir pekan dan hari libur bursa).

#### Tahap 2: Loop Harian — Berulang untuk Setiap Tanggal Trading

Untuk setiap tanggal trading yang valid, sistem menjalankan langkah-langkah berikut:

5. **Perhitungan Indikator Teknikal (*In-Memory Slicing*)**
   - Data OHLCV master dipotong (*slice*) secara *in-memory* hingga tanggal berjalan (inklusif) untuk mencegah *look-ahead bias*.
   - Indikator teknikal (MACD, RSI, Bollinger Bands, KDJ, SMA) dihitung dari potongan data tersebut menggunakan `stockstats`.

6. **Penyusunan State Awal**
   - Objek `TradingState` diinisialisasi dengan: ticker, tanggal, data pasar (fundamental, indikator, berita), status portofolio (saldo kas, jumlah saham), dan *placeholder* kosong untuk output agen.

7. **Eksekusi Graf LangGraph**
   - `graph.invoke(state)` memicu eksekusi seluruh 12 agen sesuai urutan yang didefinisikan dalam graf:
     - **Paralel:** 4 agen analis (Fundamental, Macro, Sentiment, Technical) dieksekusi secara simultan.
     - **Fan-in → Paralel:** Setelah keempat analis selesai, 2 Researcher (Bullish, Bearish) dieksekusi secara paralel.
     - **Fan-in → Sekuensial:** Setelah kedua Researcher selesai, Research Facilitator dieksekusi.
     - **Paralel:** 2 Risk Analyst (Aggressive, Conservative) dieksekusi secara paralel.
     - **Fan-in → Sekuensial:** Risk Facilitator → Portfolio Manager → Trading Agent, masing-masing dieksekusi secara sekuensial.

8. **Pencetakan Ringkasan Konsensus (*Explainable AI*)**
   - Fungsi `_print_consensus_summary()` mencetak ringkasan harian yang mencakup:
     - Laporan setiap agen beserta strategi yang diekstrak (BUY/SELL/HOLD)
     - Tabel matriks konsensus seluruh 12 agen menggunakan modul `tabulate`

9. **Eksekusi Order**
   - Fungsi `_execute_trade()` mengeksekusi order dari Trading Agent:
     - **BUY:** Menghitung biaya total (harga × lot × 100 + biaya transaksi 0,2%), memverifikasi kecukupan saldo, mengurangi kas, dan menambah posisi saham.
     - **SELL:** Menghitung pendapatan bersih (harga × saham − biaya transaksi), menambah kas, dan mengurangi posisi saham.
     - **HOLD:** Tidak ada transaksi.

10. **Pembaruan NAV**
    - Net Asset Value (NAV) dihitung: `NAV = saldo kas + (jumlah saham × harga penutupan)`.
    - NAV *Buy & Hold* juga dihitung sebagai pembanding.

#### Tahap 3: Agregasi Hasil — Satu Kali Setelah Loop Selesai

11. **Perhitungan Metrik Performa**
    - `utils/metrics.py` menghitung:
      - *Cumulative Return*: $CR = \frac{NAV_{akhir} - NAV_{awal}}{NAV_{awal}}$
      - *Sharpe Ratio*: $SR = \sqrt{252} \times \frac{\bar{R}_{excess}}{\sigma_{excess}}$ (diannualisasi, risk-free rate = BI-7DRR ≈ 6% per tahun)
      - *Maximum Drawdown*: $MDD = \max\left(\frac{Peak_t - NAV_t}{Peak_t}\right)$
      - *Win Rate*: Persentase transaksi SELL yang menghasilkan profit

12. **Penyimpanan Hasil**
    - Log transaksi disimpan ke CSV di `results/trades_*.csv`
    - NAV harian disimpan ke CSV di `results/nav_*.csv`
    - Grafik performa (MAS vs Buy & Hold) disimpan ke PNG di `results/plot_*.png`

13. **Visualisasi**
    - `utils/visualizer.py` menghasilkan grafik perbandingan kurva NAV antara portofolio MAS dan strategi *Buy & Hold* menggunakan `matplotlib`.

---

## 4. Struktur Proyek

### 4.1 Tabel Struktur Folder

```
Kode/
│
├── main.py                                  # Entry point utama (CLI)
├── requirements.txt                         # Daftar dependensi Python
├── PROPOSAL_REVISI.md                       # Dokumen proposal skripsi
├── PROJECT_STRUCTURE.md                     # Catatan struktur proyek
├── SISTEM_DOKUMENTASI.md                    # Dokumentasi ini
├── simulasi_3_hari_BBCA.txt                 # Log simulasi 3 hari (output terminal)
├── simulasi_5_hari_BBCA.txt                 # Log simulasi 5 hari (output terminal)
│
├── agents/                                  # Definisi seluruh agen per tim
│   ├── analysts.py                          # 4 Agen Analis (Fundamental, Technical,
│   │                                        #   Sentiment, Macro)
│   ├── researchers.py                       # 3 Agen Peneliti (Bullish, Bearish,
│   │                                        #   Research Facilitator)
│   ├── risk_management.py                   # 3 Agen Manajemen Risiko (Aggressive,
│   │                                        #   Conservative, Risk Facilitator)
│   └── execution.py                         # 2 Agen Eksekusi (Portfolio Manager,
│                                            #   Trading Agent)
│
├── config/                                  # Konfigurasi sistem
│   ├── llm_config.py                        # Konfigurasi model LLM (Ollama/Gemini/Groq)
│   ├── glossary.py                          # Glosarium keuangan Indonesia
│   └── prompts/                             # System prompt per tim agen
│       ├── analyst_prompts.py               # Prompt 4 agen analis
│       ├── research_prompts.py              # Prompt 3 agen peneliti
│       ├── risk_prompts.py                  # Prompt 3 agen risiko
│       └── execution_prompts.py             # Prompt PM + Trading Agent
│
├── orchestration/                           # Orkestrasi dan engine backtesting
│   ├── state.py                             # Definisi TradingState (TypedDict)
│   ├── graph.py                             # Definisi workflow LangGraph (StateGraph)
│   └── backtester.py                        # Engine backtesting utama
│
├── tools/                                   # Alat bantu pengambilan data
│   ├── data_fetcher.py                      # Wrapper yfinance (OHLCV + fundamental)
│   ├── cache_manager.py                     # Manajemen cache terpusat (master files)
│   ├── indicator_calculator.py              # Kalkulator indikator teknikal (stockstats)
│   └── news_fetcher.py                      # Pengambil berita (Google News + CNBC RSS)
│
├── utils/                                   # Utilitas pendukung
│   ├── metrics.py                           # Perhitungan metrik performa (CR, SR, MDD, WR)
│   └── visualizer.py                        # Visualisasi grafik performa (matplotlib)
│
├── scripts/                                 # Skrip pengujian
│   ├── test_data_fetch.py                   # Validasi pipeline data (centralized caching)
│   ├── test_agents.py                       # Uji coba agen tunggal (Fundamental Analyst)
│   ├── test_graph.py                        # Uji coba eksekusi graf lengkap (12 agen)
│   └── test_pipeline.py                     # Smoke test pipeline data (3 emiten)
│
├── data/                                    # Direktori data
│   └── cache/                               # Cache terpusat per ticker
│       ├── BBCA.JK/                         # Cache data BBCA
│       │   ├── master_ohlcv.csv             #   Data harga historis
│       │   ├── master_fundamentals.json     #   Data fundamental
│       │   └── master_news.json             #   Data berita
│       ├── BBRI.JK/                         # Cache data BBRI
│       └── BMRI.JK/                         # Cache data BMRI
│
└── results/                                 # Hasil backtesting
    ├── nav_BBCA_JK_*.csv                    # NAV harian (MAS vs B&H)
    ├── trades_BBCA_JK_*.csv                 # Log transaksi
    └── plot_BBCA_JK_*.png                   # Grafik performa
```

### 4.2 Penjelasan File Utama

#### 4.2.1 `main.py` — Entry Point Sistem

**Lokasi:** Root proyek
**Jumlah Baris:** 91
**Peran dalam Pipeline:** Titik masuk utama (*entry point*) yang mengoordinasikan seluruh *pipeline* eksekusi dari awal hingga akhir.

**Logika Kode:**

File ini mengimplementasikan fungsi `main()` yang menjalankan empat tahap utama secara sekuensial:

1. **Parsing Argumen CLI:** Menggunakan `argparse` untuk menerima parameter dari pengguna:
   - `--ticker` (default: `BBCA.JK`) — kode saham yang akan dianalisis.
   - `--start` (default: `2024-01-01`) — tanggal awal simulasi.
   - `--end` (default: `2024-01-31`) — tanggal akhir simulasi.
   - `--capital` (default: `100.000.000`) — modal awal dalam Rupiah.

2. **Inisialisasi dan Eksekusi Backtester:** Membuat instansi `Backtester` dengan parameter yang telah di-*parse*, lalu memanggil `backtester.run()` yang mengembalikan dictionary berisi `dates`, `mas_nav`, `bh_nav`, dan `trades`.

3. **Perhitungan Metrik:** Memanggil `calculate_metrics()` untuk menghitung metrik performa portofolio MAS dan *Buy & Hold* secara terpisah, kemudian menampilkan perbandingan kedua strategi dalam format tabel di terminal.

4. **Penyimpanan Hasil:** Menyimpan log transaksi ke CSV, NAV harian ke CSV, dan grafik performa ke PNG di direktori `results/`.

**Ketergantungan:**
- `orchestration/backtester.py` → Backtester
- `utils/metrics.py` → calculate_metrics
- `utils/visualizer.py` → plot_performance

---

#### 4.2.2 `agents/analysts.py` — Tim Analis (4 Agen)

**Lokasi:** `agents/`
**Jumlah Baris:** 72
**Peran dalam Pipeline:** Lapisan pertama dalam *workflow* agen — menerima data pasar mentah dan menghasilkan laporan analisis terstruktur.

**Logika Kode:**

File ini mendefinisikan empat fungsi agen (`fundamental_analyst`, `technical_analyst`, `sentiment_analyst`, `macro_analyst`) yang semuanya dibangun di atas fungsi *helper* tunggal `_run_analyst_node()`.

Fungsi `_run_analyst_node(state, role_name, data_key, prompt_template)` mengimplementasikan pola eksekusi yang seragam untuk seluruh agen analis:

1. **Inisialisasi LLM:** Memanggil `get_llm("analyst", "ollama")` yang mengembalikan instansi `ChatOllama` dengan temperature 0.0 (deterministik).

2. **Konstruksi Pesan:** Membuat pasangan pesan `SystemMessage` (berisi *system prompt* spesifik agen) dan `HumanMessage` (berisi ticker, tanggal, dan data pasar yang relevan dalam format JSON).

3. **Pencegahan Overflow Konteks:** Jika representasi JSON data melebihi 3000 karakter, data dipotong dengan penanda `[TRUNCATED]` untuk mencegah melebihi jendela konteks model (Llama 3.1 8B memiliki konteks ~8K token).

4. **Invokasi LLM dan Penanganan Error:** Memanggil `llm.invoke([sys_msg, human_msg])` dan menangkap *exception* untuk menghasilkan laporan *fallback* jika LLM gagal merespons.

5. **Pengembalian Hasil:** Mengembalikan dictionary `{"analyst_reports": {role_name.lower(): report}}` yang akan di-*merge* ke *global state* melalui *custom reducer* `update_dict`.

Fungsi `_extract_strategy(text)` melakukan ekstraksi strategi dominan (BUY/SELL/HOLD) dari teks respons LLM menggunakan penghitungan frekuensi *keyword* berbasis *regex* — strategi dengan kemunculan terbanyak dianggap sebagai rekomendasi dominan agen.

**Ketergantungan:**
- `orchestration/state.py` → TradingState
- `config/llm_config.py` → get_llm
- `config/prompts/analyst_prompts.py` → FUNDAMENTAL_ANALYST_PROMPT, TECHNICAL_ANALYST_PROMPT, SENTIMENT_ANALYST_PROMPT, MACRO_ANALYST_PROMPT
- `langchain_core.messages` → HumanMessage, SystemMessage

---

#### 4.2.3 `agents/researchers.py` — Tim Peneliti (3 Agen)

**Lokasi:** `agents/`
**Jumlah Baris:** 88
**Peran dalam Pipeline:** Lapisan kedua — menerima laporan dari Tim Analis dan melakukan sintesis melalui debat dialektik.

**Logika Kode:**

File ini mendefinisikan tiga fungsi agen:

1. `bullish_researcher(state)` — Membaca `state["analyst_reports"]`, menginvokasi LLM dengan *prompt* `BULLISH_PROMPT` yang menginstruksikan agen untuk menyusun argumen investasi positif terkuat, dan mengembalikan `{"research_debate": [{"agent": "Bullish", "message": argument}]}`.

2. `bearish_researcher(state)` — Struktur identik dengan Bullish Researcher, tetapi menggunakan *prompt* `BEARISH_PROMPT` yang menginstruksikan agen untuk menyusun argumen peringatan/negatif terkuat.

3. `research_facilitator(state)` — Membaca `state["research_debate"]` (yang berisi argumen Bullish dan Bearish), menginvokasi LLM dengan *prompt* `RESEARCH_FACILITATOR_PROMPT` yang menginstruksikan agen untuk mensintesis debat secara objektif, dan mengembalikan `{"research_consensus": consensus}`.

Kedua Researcher menggunakan `get_llm("researcher", "ollama")` dengan temperature 0.7 untuk menghasilkan argumen yang lebih kreatif dan bervariasi, sedangkan Facilitator menggunakan temperature 0.0 untuk konsistensi.

**Ketergantungan:**
- `config/prompts/research_prompts.py` → BULLISH_PROMPT, BEARISH_PROMPT, RESEARCH_FACILITATOR_PROMPT

---

#### 4.2.4 `agents/risk_management.py` — Tim Manajemen Risiko (3 Agen)

**Lokasi:** `agents/`
**Jumlah Baris:** 89
**Peran dalam Pipeline:** Lapisan ketiga — menerima *Research Consensus* dan mengevaluasi risiko dari dua perspektif berlawanan.

**Logika Kode:**

Struktur file ini merefleksikan pola yang sama dengan `researchers.py`, mengimplementasikan debat lapisan kedua:

1. `conservative_risk_analyst(state)` — Membaca `state["research_consensus"]`, menginvokasi LLM dengan *prompt* `CONSERVATIVE_RISK_PROMPT`, dan mengembalikan `{"risk_debate": [{"agent": "ConservativeRisk", "message": argument}]}`.

2. `aggressive_risk_analyst(state)` — Membaca `state["research_consensus"]`, menginvokasi LLM dengan *prompt* `AGGRESSIVE_RISK_PROMPT`, dan mengembalikan `{"risk_debate": [{"agent": "AggressiveRisk", "message": argument}]}`.

3. `risk_facilitator(state)` — Membaca `state["risk_debate"]` dan `state["research_consensus"]`, mensintesis debat kedua pihak, dan mengembalikan `{"risk_consensus": final_consensus}`.

**Ketergantungan:**
- `config/prompts/risk_prompts.py` → CONSERVATIVE_RISK_PROMPT, AGGRESSIVE_RISK_PROMPT, RISK_FACILITATOR_PROMPT

---

#### 4.2.5 `agents/execution.py` — Tim Eksekusi (2 Agen)

**Lokasi:** `agents/`
**Jumlah Baris:** 81
**Peran dalam Pipeline:** Lapisan terakhir — merumuskan keputusan strategis dan menerjemahkannya menjadi order kuantitatif.

**Logika Kode:**

1. `portfolio_manager(state)` — Membaca tiga input kunci: `state["research_consensus"]`, `state["risk_consensus"]`, dan `state["portfolio_status"]` (yang berisi `current_cash` dan `holdings`). Menginvokasi LLM untuk merumuskan rekomendasi strategis. Menyimpan rekomendasi ke `state["portfolio_status"]["recommendation"]`.

2. `trading_agent(state)` — Membaca `state["portfolio_status"]["recommendation"]`. Menginvokasi LLM dengan *prompt* yang secara ketat menginstruksikan output dalam format JSON. Mengimplementasikan **mekanisme parsing bertingkat**:
   - **Tahap 1:** Mencoba mengekstrak blok JSON dari teks respons menggunakan *regex* `re.search(r'\{.*\}', content, re.DOTALL)`.
   - **Tahap 2 (Fallback):** Jika *regex* gagal, menggunakan `JsonOutputParser` dari LangChain.
   - **Tahap 3 (Fallback Final):** Jika kedua metode gagal, mengembalikan *default* `{"action": "HOLD", "quantity": 0, "confidence": 0.0}` untuk menjamin sistem tidak berhenti (*graceful degradation*).

**Ketergantungan:**
- `config/prompts/execution_prompts.py` → PORTFOLIO_MANAGER_PROMPT, TRADING_AGENT_PROMPT
- `langchain_core.output_parsers` → JsonOutputParser

---

#### 4.2.6 `orchestration/backtester.py` — Engine Backtesting

**Lokasi:** `orchestration/`
**Jumlah Baris:** 368
**Peran dalam Pipeline:** Komponen sentral yang mengoordinasikan seluruh proses *backtesting* — dari persiapan data hingga eksekusi order dan penghitungan NAV.

**Logika Kode:**

Kelas `Backtester` merupakan komponen paling kompleks dalam sistem, mengimplementasikan beberapa tanggung jawab utama:

1. **Inisialisasi (`__init__`):**
   - Menerima parameter `ticker`, `start_date`, `end_date`, `initial_capital` (default Rp 100 juta), dan `fee_rate` (default 0,2%).
   - Menginisialisasi seluruh komponen pendukung: `CacheManager`, `YFinanceFetcher`, `TechnicalIndicatorCalculator`, `NewsFetcher`, dan graf LangGraph (`create_trading_graph()`).
   - Menginisialisasi variabel *state tracking*: `current_cash`, `holdings` (dalam lembar saham), `nav_history`, `dates_history`, `trades`, serta variabel *baseline* `bh_shares` dan `bh_nav_history` untuk strategi *Buy & Hold*.

2. **Persiapan Data (`_prepare_data`):**
   - Menjalankan *pipeline* pengambilan data **satu kali** sebelum loop *backtesting* dimulai.
   - Memuat tiga *master file* (OHLCV, fundamentals, news) dari *cache* jika tersedia, atau mengunduh dari sumber jika belum ada.
   - Mengimplementasikan validasi cakupan tanggal — jika data *cache* tidak mencakup `end_date` yang diminta, data diunduh ulang.
   - Menentukan `valid_dates` — daftar tanggal perdagangan valid dalam rentang yang diminta, berdasarkan tanggal-tanggal yang memiliki data OHLCV.

3. **Perhitungan Indikator (*_compute_indicators_for_date*):**
   - Melakukan *in-memory slicing* pada `master_ohlcv` hingga tanggal target (inklusif) untuk mencegah *look-ahead bias*.
   - Memanggil `indicator_calc.calculate_indicators(df_slice, date_str)` untuk menghitung indikator teknikal pada potongan data tersebut.

4. **Pencetakan Ringkasan Konsensus (`_print_consensus_summary`):**
   - Mengimplementasikan *Explainable AI* melalui pencetakan terstruktur seluruh output agen.
   - Memproses output setiap agen secara sekuensial (Analis → Peneliti → Risiko → PM → Trader) meskipun eksekusi internal bersifat paralel.
   - Menghasilkan tabel matriks konsensus menggunakan modul `tabulate` yang merangkum strategi BUY/SELL/HOLD dan tingkat keyakinan seluruh agen.

5. **Eksekusi Order (`_execute_trade`):**
   - Mengkonversi kuantitas lot ke lembar saham (1 lot = 100 saham, sesuai aturan BEI).
   - Untuk BUY: memverifikasi kecukupan saldo kas, menghitung biaya total (harga × saham + *fee*), mengurangi kas, menambah kepemilikan.
   - Untuk SELL: menghitung pendapatan bersih (harga × saham − *fee*), menambah kas, mengurangi kepemilikan. Mengimplementasikan *safety check* — jumlah saham yang dijual tidak boleh melebihi jumlah yang dimiliki.

6. **Loop Utama (`run`):**
   - Iterasi melalui setiap tanggal trading valid.
   - Untuk setiap tanggal: menghitung indikator, menyusun *state*, mengeksekusi graf LangGraph, mencetak ringkasan, mengeksekusi order, dan memperbarui NAV.
   - Menginisialisasi *Buy & Hold baseline* pada hari pertama — membeli saham sebanyak mungkin dengan seluruh modal.
   - Mengembalikan dictionary hasil: `dates`, `mas_nav`, `bh_nav`, `trades`.

**Ketergantungan:**
- `tools/cache_manager.py` → CacheManager
- `tools/data_fetcher.py` → YFinanceFetcher
- `tools/indicator_calculator.py` → TechnicalIndicatorCalculator
- `tools/news_fetcher.py` → NewsFetcher
- `orchestration/graph.py` → create_trading_graph

---

#### 4.2.7 `orchestration/graph.py` — Definisi Workflow LangGraph

**Lokasi:** `orchestration/`
**Jumlah Baris:** 65
**Peran dalam Pipeline:** Mendefinisikan struktur graf berarah (*directed graph*) yang mengatur urutan eksekusi dan dependensi antar-agen.

**Logika Kode:**

Fungsi `create_trading_graph()` membangun dan mengompilasi `StateGraph` LangGraph melalui tiga langkah:

1. **Registrasi Node (Agen):** Mendaftarkan 12 fungsi agen sebagai *node* dalam graf.

2. **Definisi Edge (Alur Eksekusi):**
   - `START → [fundamental, technical, sentiment, macro]` — Keempat analis dieksekusi paralel saat graf dimulai.
   - `[fundamental, technical, sentiment, macro] → [bullish_researcher, bearish_researcher]` — Setiap analis terhubung ke kedua Researcher. LangGraph secara otomatis menunggu **semua** analis selesai sebelum memulai Researcher (*fan-in behavior*).
   - `[bullish_researcher, bearish_researcher] → research_facilitator` — Fan-in: Facilitator menunggu kedua Researcher.
   - `research_facilitator → [conservative_risk, aggressive_risk]` — Fan-out: kedua Risk Analyst dieksekusi paralel.
   - `[conservative_risk, aggressive_risk] → risk_facilitator` — Fan-in.
   - `risk_facilitator → portfolio_manager → trading_agent → END` — Eksekusi sekuensial final.

3. **Kompilasi Graf:** `builder.compile()` mengembalikan graf yang siap dieksekusi melalui `.invoke(state)`.

**Ketergantungan:**
- `langgraph.graph` → StateGraph, START, END
- Seluruh modul agen di `agents/`

---

#### 4.2.8 `orchestration/state.py` — Definisi Global State

**Lokasi:** `orchestration/`
**Jumlah Baris:** 56
**Peran dalam Pipeline:** Mendefinisikan skema data (*schema*) untuk komunikasi antar-agen melalui *global shared state*.

**Logika Kode:**

File ini mendefinisikan:

1. **Custom Reducers:**
   - `update_dict(dict1, dict2)` — Menggabungkan dua dictionary. Digunakan oleh `analyst_reports` agar keempat agen analis dapat menulis ke kunci yang sama secara paralel tanpa saling menimpa (setiap agen menulis ke sub-kunci yang berbeda: `"fundamental"`, `"technical"`, `"sentiment"`, `"macro"`).
   - `append_list(list1, list2)` — Menggabungkan dua list. Digunakan oleh `research_debate` dan `risk_debate` agar Bullish dan Bearish Researcher dapat menambahkan argumen ke list yang sama secara paralel.

2. **TradingState (TypedDict):**
   - `ticker: str` — Kode saham (contoh: `"BBCA.JK"`)
   - `date: str` — Tanggal simulasi berjalan
   - `market_data: Dict[str, Any]` — Data pasar mentah (fundamental, indikator, berita)
   - `analyst_reports: Annotated[Dict[str, str], update_dict]` — Laporan 4 analis
   - `research_debate: Annotated[List[Dict[str, str]], append_list]` — Argumen debat Bullish/Bearish
   - `research_consensus: str` — Konsensus riset
   - `risk_reports: Annotated[Dict[str, str], update_dict]` — (Cadangan untuk laporan risiko tambahan)
   - `risk_debate: Annotated[List[Dict[str, str]], append_list]` — Argumen debat risiko
   - `risk_consensus: str` — Konsensus risiko
   - `portfolio_status: Dict[str, Any]` — Status portofolio (kas, kepemilikan, rekomendasi)
   - `trading_decision: Dict[str, Any]` — Keputusan trading final (JSON dari Trading Agent)

---

#### 4.2.9 `tools/data_fetcher.py` — Pengambil Data Pasar

**Lokasi:** `tools/`
**Jumlah Baris:** 111
**Peran dalam Pipeline:** Mengambil data OHLCV dan fundamental dari Yahoo Finance dan menyimpannya sebagai *master file* di *cache* terpusat.

**Logika Kode:**

Kelas `YFinanceFetcher` mengimplementasikan dua metode utama:

1. `fetch_ohlcv(ticker, start_date, end_date)` — Mengunduh data harga historis dengan **lookback 2 tahun** dari `start_date` (bukan dari `start_date` itu sendiri) untuk memastikan indikator teknikal seperti SMA-200 memiliki cukup data historis. Melakukan normalisasi kolom (lowercase) untuk kompatibilitas dengan `stockstats`, menangani *quirk* multi-index pada `yfinance >= 0.2.33`, dan menyimpan sebagai `master_ohlcv.csv`.

2. `fetch_fundamentals(ticker)` — Mengambil data fundamental (Market Cap, P/E, P/B, Dividend Yield, sektor, industri) dan laporan keuangan (laba-rugi, neraca) menggunakan API `yfinance.Ticker`. Mengkonversi `Timestamp` kolom ke string untuk kompatibilitas JSON, dan menyimpan sebagai `master_fundamentals.json`.

**Ketergantungan:** `yfinance`, `pandas`, `tools/cache_manager.py`

---

#### 4.2.10 `tools/cache_manager.py` — Manajemen Cache Terpusat

**Lokasi:** `tools/`
**Jumlah Baris:** 105
**Peran dalam Pipeline:** Mengelola penyimpanan dan pemuatan data *cache* dalam arsitektur terpusat (*centralized caching*) untuk efisiensi I/O.

**Logika Kode:**

Kelas `CacheManager` mengimplementasikan arsitektur *cache* yang berpusat pada **master file per ticker** (bukan per-tanggal), dengan struktur: `data/cache/{ticker}/master_*`. Arsitektur ini dipilih untuk:
- Mengurangi jumlah file I/O secara drastis (dari ratusan file per-tanggal menjadi 3 master file per ticker).
- Mempercepat *backtesting* karena seluruh data dimuat ke memori satu kali di awal.
- Menyederhanakan manajemen *cache* (hanya perlu memeriksa keberadaan 3 file, bukan ratusan folder).

Metode-metode kunci:
- `save_master_csv()` / `load_master_csv()` — Menyimpan/memuat DataFrame ke/dari CSV.
- `save_master_json()` / `load_master_json()` — Menyimpan/memuat dictionary ke/dari JSON.
- `master_file_exists()` — Memeriksa keberadaan master file.
- `cleanup_legacy_folders()` — Menghapus folder per-tanggal dan file non-master dari arsitektur versi sebelumnya.

**Ketergantungan:** `pandas`, `json`, `shutil`, `pathlib`

---

#### 4.2.11 `tools/indicator_calculator.py` — Kalkulator Indikator Teknikal

**Lokasi:** `tools/`
**Jumlah Baris:** 88
**Peran dalam Pipeline:** Menghitung indikator teknikal dari data OHLCV secara *in-memory* tanpa file I/O.

**Logika Kode:**

Kelas `TechnicalIndicatorCalculator` menggunakan *library* `stockstats` untuk menghitung indikator teknikal berikut:

| Indikator | Deskripsi | Penggunaan |
|-----------|-----------|------------|
| MACD, MACDS, MACDH | Moving Average Convergence Divergence + Signal + Histogram | Identifikasi momentum dan arah tren |
| RSI-14 | Relative Strength Index (14 hari) | Deteksi overbought (>70) / oversold (<30) |
| Bollinger Bands (UB, MB, LB) | Band volatilitas atas, tengah, bawah | Identifikasi volatilitas dan breakout |
| KDJ (K, D, J) | Stochastic Oscillator | Deteksi momentum dan titik pembalikan |
| SMA-20, SMA-50 | Simple Moving Average | Identifikasi tren jangka pendek/menengah |

Metode `calculate_indicators(df, date_str)`:
1. Membuat salinan DataFrame (karena `stockstats` memodifikasi *in-place*).
2. Menghitung seluruh indikator secara *lazy* (stockstats menghitung saat diakses).
3. Mencari tanggal terdekat yang tersedia jika `date_str` jatuh pada akhir pekan/libur.
4. Mengkonversi seluruh nilai ke `float` Python (*native*), menangani nilai `NaN` secara eksplisit.

**Ketergantungan:** `stockstats`, `pandas`, `math`

---

#### 4.2.12 `tools/news_fetcher.py` — Pengambil Berita Keuangan

**Lokasi:** `tools/`
**Jumlah Baris:** 81
**Peran dalam Pipeline:** Mengambil berita keuangan dari Google News RSS dan CNBC Indonesia RSS untuk dianalisis oleh Sentiment Analyst dan Macro Analyst.

**Logika Kode:**

Kelas `NewsFetcher` mengambil berita dari tiga sumber:

1. **Google News RSS (spesifik ticker):** Query `"{ticker_base} saham"` dengan parameter `hl=id&gl=ID&ceid=ID:id` untuk memastikan hasil berbahasa Indonesia.
2. **Google News RSS (makroekonomi):** Query `"suku bunga Bank Indonesia OJK"` untuk berita makroekonomi yang relevan dengan sektor perbankan.
3. **CNBC Indonesia RSS:** Feed berita pasar dari `cnbcindonesia.com/market/rss`.

Berita dari ketiga sumber digabungkan dan dide-duplikasi berdasarkan judul (*title*), kemudian disimpan sebagai `master_news.json`.

**Catatan Penting:** RSS feed hanya menyediakan berita terkini (*current*), bukan berita historis. Untuk *backtesting* pada periode lampau, idealnya diperlukan database berita historis yang telah di-*scrape* sebelumnya. Keterbatasan ini didokumentasikan sebagai bagian dari batasan sistem.

**Ketergantungan:** `feedparser`, `urllib.parse`, `tools/cache_manager.py`

---

#### 4.2.13 `config/llm_config.py` — Konfigurasi Model LLM

**Lokasi:** `config/`
**Jumlah Baris:** 40
**Peran dalam Pipeline:** Menyediakan fungsi *factory* yang mengembalikan instansi LLM sesuai peran agen dan provider yang dipilih.

**Logika Kode:**

Fungsi `get_llm(role, provider)` mengimplementasikan dua dimensi konfigurasi:

- **Dimensi Temperature (berdasarkan role):**
  - `"analyst"` / `"manager"` → temperature 0.0 (deterministik, faktual)
  - `"debater"` / `"researcher"` → temperature 0.7 (kreatif, argumentatif)

- **Dimensi Provider:**
  - `"ollama"` → `ChatOllama(model="llama3.1:latest", base_url="http://localhost:11434")`
  - `"gemini"` → `ChatGoogleGenerativeAI(model="gemini-2.0-flash")`
  - `"groq"` → `ChatGroq(model="llama-3.3-70b-versatile")`

**Ketergantungan:** `langchain_ollama`, `langchain_google_genai`, `langchain_groq`

---

#### 4.2.14 `config/glossary.py` — Glosarium Keuangan Indonesia

**Lokasi:** `config/`
**Jumlah Baris:** 22
**Peran dalam Pipeline:** Menyediakan glosarium istilah keuangan dan perbankan Indonesia yang diinjeksikan ke dalam *system prompt* agen-agen yang memproses data berbahasa Indonesia.

Glosarium mencakup istilah-istilah kunci: IHSG, Emiten, DPK, NPL, NIM, CAR, Laba Bersih, BI-7DRR, OJK, Kredit Macet, LDR, Saham, Perbankan — beserta definisi singkat dan konteks penggunaannya di pasar Indonesia.

---

#### 4.2.15 `config/prompts/` — System Prompt per Tim Agen

**Lokasi:** `config/prompts/`
**Jumlah File:** 4 (`analyst_prompts.py`, `research_prompts.py`, `risk_prompts.py`, `execution_prompts.py`)
**Peran dalam Pipeline:** Mendefinisikan *system prompt* terspesialisasi untuk setiap agen yang mengarahkan perilaku LLM sesuai perannya.

Setiap *system prompt* mengikuti struktur:
1. **Role Definition:** Identitas dan spesialisasi agen.
2. **Task Specification:** Tugas spesifik yang harus dilakukan.
3. **Instructions:** Langkah-langkah analisis yang harus diikuti.
4. **Output Format Constraint:** Instruksi ketat untuk menghasilkan output dalam format teks polos (tanpa *markdown*), bahasa Indonesia formal, paragraf naratif padat maksimal 3 kalimat. Khusus Trading Agent: output JSON terstruktur.
5. **Domain Knowledge:** Glosarium keuangan Indonesia (diinjeksikan pada agen yang memproses data konteks Indonesia).

---

#### 4.2.16 `utils/metrics.py` — Perhitungan Metrik Performa

**Lokasi:** `utils/`
**Jumlah Baris:** 67
**Peran dalam Pipeline:** Menghitung metrik evaluasi performa portofolio setelah *backtesting* selesai.

Fungsi `calculate_metrics(nav_history, trades, risk_free_rate_annual)` menghitung:

- **Cumulative Return:** $(NAV_{akhir} - NAV_{awal}) / NAV_{awal}$
- **Sharpe Ratio:** $\sqrt{252} \times \frac{\text{mean}(R_{excess})}{\text{std}(R_{excess})}$ di mana $R_{excess} = R_{daily} - R_f$ dan $R_f = R_{annual} / 252$
- **Maximum Drawdown:** $\max\left(\frac{Peak - NAV}{Peak}\right)$ menggunakan akumulasi puncak berjalan (*running peak*)
- **Win Rate:** Persentase transaksi SELL yang memiliki `profit_loss > 0`

---

#### 4.2.17 `utils/visualizer.py` — Visualisasi Grafik Performa

**Lokasi:** `utils/`
**Jumlah Baris:** 45
**Peran dalam Pipeline:** Menghasilkan grafik perbandingan kurva NAV antara portofolio MAS dan strategi *Buy & Hold*.

Fungsi `plot_performance()` menggunakan `matplotlib` untuk menghasilkan grafik dengan:
- Kurva biru solid (MAS NAV) dan kurva abu-abu *dashed* (Buy & Hold NAV)
- Rotasi label sumbu-X otomatis untuk keterbacaan
- Output PNG dengan resolusi 300 DPI

---

#### 4.2.18 `data/cache/` — Direktori Cache Terpusat

**Lokasi:** `data/cache/`
**Peran dalam Pipeline:** Menyimpan data pasar yang telah diunduh untuk menghindari pengunduhan berulang dan mempercepat iterasi pengembangan.

Struktur:
```
data/cache/
├── BBCA.JK/
│   ├── master_ohlcv.csv          # Data harga historis (OHLCV) dengan lookback 2 tahun
│   ├── master_fundamentals.json  # Data fundamental (P/E, P/B, Market Cap, dll.)
│   └── master_news.json          # Daftar berita dari Google News + CNBC Indonesia
├── BBRI.JK/
│   └── (struktur serupa)
└── BMRI.JK/
    └── (struktur serupa)
```

Prinsip desain:
- **Satu master file per sumber data per ticker** — bukan per-tanggal — untuk efisiensi I/O.
- **Slicing dilakukan in-memory** oleh Backtester pada saat runtime untuk mencegah *look-ahead bias*.
- **Cleanup otomatis** terhadap folder per-tanggal dari arsitektur versi lama dilakukan saat sistem diinisialisasi.

---

## 5. Daftar Pustaka

[1] Y. Xiao, E. Sun, D. Luo, and W. Wang, "TradingAgents: Multi-Agents LLM Financial Trading Framework," *arXiv preprint arXiv:2412.20138v7*, Jun. 2025. [Online]. Available: https://arxiv.org/abs/2412.20138

[2] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," *arXiv preprint arXiv:2308.00352*, 2024. [Online]. Available: https://arxiv.org/abs/2308.00352

[3] Y. Yu, Z. Yao, H. Li, Z. Deng, Y. Cao, Z. Chen, J. W. Suchow, R. Liu, Z. Cui, and D. Zhang, "FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making," *Proc. NeurIPS 2024*, 2024. [Online]. Available: https://arxiv.org/abs/2407.06567

[4] S. Wu, O. Irsoy, S. Lu, V. Dabravolski, M. Dredze, S. Gehrmann, P. Kambadur, D. Rosenberg, and G. Mann, "BloombergGPT: A Large Language Model for Finance," *arXiv preprint arXiv:2303.17564*, 2023. [Online]. Available: https://arxiv.org/abs/2303.17564

[5] Y. Yu, H. Li, Z. Chen, Y. Jiang, Y. Li, D. Zhang, R. Liu, J. W. Suchow, and K. Khashanah, "FinMem: A Performance-Enhanced LLM Trading Agent with Layered Memory and Character Design," *arXiv preprint arXiv:2311.13743*, 2023. [Online]. Available: https://arxiv.org/abs/2311.13743

---

> **Catatan:** Dokumentasi ini disusun berdasarkan implementasi aktual kode sumber proyek dan proposal skripsi revisi. Seluruh referensi ke file, fungsi, dan variabel telah diverifikasi terhadap kode yang berjalan pada saat dokumentasi ini ditulis (Juli 2026).
