---
title: 'Penjelasan Alur Diagram'

---

# Arsitektur Global (*High-Level*) Sistem Multi-Agent LLM Trading

---

## PENDAHULUAN UMUM

### Apa Tujuan Diagram Ini Dibuat?

Diagram ini dirancang untuk memberikan gambaran menyeluruh (*bird's-eye view*) tentang bagaimana seluruh komponen sistem *Multi-Agent LLM Trading* bekerja secara terintegrasi dari ujung ke ujung (*end-to-end*). Diagram ini menjawab satu pertanyaan besar: **"Bagaimana data mentah dari internet berubah menjadi keputusan investasi (BUY/SELL/HOLD) yang rasional dan transparan?"**

### Apa Pengertian dari Diagram Ini?

Diagram Arsitektur Global (*High-Level Architecture*) adalah peta visual yang menunjukkan seluruh alur kerja sistem secara makro — mulai dari sumber data eksternal, pemrosesan oleh mesin Python, pengambilan keputusan oleh 12 agen AI yang saling berdebat, hingga penyajian hasil akhir kepada pengguna melalui antarmuka web. Diagram ini terbagi menjadi **7 fase** yang tersusun dari kiri ke kanan, di mana setiap fase merepresentasikan satu tahapan logis dalam *pipeline* pengolahan data. Aliran data bergerak secara **unidireksional** (satu arah, dari kiri ke kanan), memastikan tidak ada kebuntuan (*deadlock*) atau perulangan tak terbatas (*infinite loop*) di dalam sistem.

---

## FASE 1: SUMBER DATA (*Data Sources*)

Fase pertama merupakan titik awal dari seluruh sistem. Pada fase ini, Python bertindak sebagai **"Mata"** sistem — ia bertugas melihat dan mengumpulkan informasi dari dunia luar (internet) agar AI memiliki bahan baku untuk berpikir. Tanpa fase ini, otak AI tidak memiliki informasi apapun tentang kondisi pasar saham dan akan beroperasi secara buta.

Di dalam Fase 1, terdapat **3 kelompok sumber data** yang masing-masing memiliki fungsi dan asal yang berbeda:

### 1A. Yahoo Finance — Data Harga Saham Harian (OHLCV)

Sumber data pertama adalah **Yahoo Finance**, yang menyediakan data harga saham historis harian. Data ini dikenal dengan sebutan **OHLCV**, yang merupakan akronim dari lima kolom utamanya:

| Kolom | Penjelasan |
|:---|:---|
| **Open** | Harga pembukaan saham pada hari tersebut |
| **High** | Harga tertinggi yang dicapai selama hari perdagangan |
| **Low** | Harga terendah yang dicapai selama hari perdagangan |
| **Close** | Harga penutupan saham pada hari tersebut (digunakan sebagai harga acuan transaksi) |
| **Volume** | Total jumlah lembar saham yang diperjualbelikan pada hari tersebut |

Data OHLCV ini merupakan bahan baku utama bagi **Agen Analis Teknikal**, yang nantinya akan menggunakan data ini untuk menghitung indikator-indikator teknikal seperti MACD, RSI, dan Bollinger Bands. Sistem secara otomatis menarik data historis dengan **buffer mundur 2 tahun** dari tanggal mulai yang diminta pengguna, agar indikator yang membutuhkan jendela panjang (seperti SMA-200) memiliki cukup data historis untuk dihitung tanpa menghasilkan nilai kosong.

### 1B. Yahoo Finance — Data Fundamental Perusahaan

Sumber data kedua juga berasal dari **Yahoo Finance**, namun jenis datanya berbeda. Data fundamental berisi **potret kesehatan keuangan perusahaan** pada suatu waktu tertentu. Data ini mencakup:

- **Informasi Valuasi:** Kapitalisasi pasar (*Market Cap*), Rasio Harga terhadap Laba (*P/E Ratio*), Rasio Harga terhadap Nilai Buku (*Price to Book*), dan Imbal Hasil Dividen (*Dividend Yield*).
- **Laporan Laba Rugi (*Income Statement*):** Pendapatan, beban operasional, dan laba bersih perusahaan.
- **Neraca Keuangan (*Balance Sheet*):** Aset, liabilitas (utang), dan ekuitas (modal sendiri) perusahaan.

Data fundamental ini merupakan bahan baku utama bagi **Agen Analis Fundamental**, yang bertugas mengevaluasi apakah harga saham saat ini tergolong mahal (*overvalued*) atau murah (*undervalued*) berdasarkan kondisi keuangan intrinsik perusahaan.

### 1C. Data Berita Ekonomi & Saham (3 Stream RSS)

Sumber data ketiga adalah **berita** yang diambil dari internet melalui teknologi **RSS (*Really Simple Syndication*) Feed**. Sistem mengambil berita dari **3 aliran (stream)** yang berbeda secara bersamaan untuk mendapatkan pandangan yang komprehensif:

| No. | Sumber | Kata Kunci Pencarian (*Query*) | Tujuan |
|:---|:---|:---|:---|
| 1 | **Google News** | `"{ticker} saham"` (contoh: `"BBRI saham"`) | Mengambil berita **spesifik mikro** tentang perusahaan tersebut (misal: laba BBRI naik, BBRI bagi dividen) |
| 2 | **Google News** | `"suku bunga Bank Indonesia OJK"` | Mengambil berita **makroekonomi** yang berdampak langsung pada sektor perbankan (misal: BI menaikkan suku bunga acuan) |
| 3 | **CNBC Indonesia** | *(Tanpa query — URL RSS langsung)* | Mengambil seluruh **headline dan ringkasan berita pasar modal** terbaru dari portal berita keuangan terbesar di Indonesia |

Ketiga aliran berita ini kemudian diproses secara otomatis setiap hari pada pukul 11:00 WIB melalui pipeline cloud terotomasi menggunakan **GitHub Actions** dan **Docker**, digabungkan menjadi satu kumpulan, dibersihkan dari tag HTML dan teks template, serta dibersihkan dari judul yang duplikat (*deduplikasi*). Data berita ini dilengkapi dengan field ringkasan (*description*) yang informatif dan menjadi bahan baku utama bagi **Agen Analis Sentimen** (untuk membaca suasana pasar terhadap saham tertentu) dan **Agen Analis Makroekonomi** (untuk memahami dampak kebijakan BI/OJK terhadap harga saham perbankan).

---

## TRANSISI FASE 1 → FASE 2

Setelah seluruh data mentah berhasil diidentifikasi dari ketiga sumber di atas, data tersebut **belum bisa langsung digunakan oleh AI**. Data masih berupa respons mentah dari API internet yang formatnya berantakan dan belum terstandarisasi. Oleh karena itu, data tersebut harus melewati proses otomasi penarikan terjadwal, pembersihan, penyimpanan, dan pengayaan terlebih dahulu. Di sinilah peran Fase 2 dimulai — Python bersama Docker dan GitHub Actions bertindak sebagai **"Tangan"** yang menerima data mentah dari "Mata" (Fase 1), membersihkannya, menyimpannya secara lokal dan di repositori cloud, serta menghitung indikator tambahan sebelum data siap diserahkan ke otak AI.

Secara visual pada diagram, panah dari ketiga kotak sumber data di Fase 1 (Yahoo Finance OHLCV, Yahoo Finance Fundamental, dan 3 RSS Berita) semuanya **berkonvergensi** (menyatu) menuju titik masuk di Fase 2, yaitu modul **News Fetcher** dan **Data Fetcher**.

---

## FASE 2: PYTHON ENGINE & CLOUD PIPELINE (*Pra-Pemrosesan Data & Otomasi*)

Fase kedua merupakan dapur pengolahan data yang dijalankan oleh mesin **Python** serta didukung oleh otomasi cloud **GitHub Actions** dan kontainer **Docker**. Pada fase ini, tidak ada AI yang terlibat — semua proses bersifat deterministik (hasilnya selalu sama jika inputnya sama). Di dalam Fase 2, terdapat **4 komponen utama** yang bekerja secara terintegrasi:

### 2A. Otomasi Cloud Scheduler & Containerization (GitHub Actions + Docker)

Untuk menjamin ketersediaan data harian secara berkala (*high availability*) tanpa membebani komputer lokal peneliti, sistem dilengkapi rantai otomasi terstandarisasi:
- **GitHub Actions Workflow (`cron: '0 4 * * *'` / 11:00 AM WIB):** Layanan komputasi awan yang menyala otomatis setiap hari pukul 11:00 WIB untuk memicu eksekusi pengumpulan berita harian 5 bank (`BBRI.JK`, `BBCA.JK`, `BMRI.JK`, `BBNI.JK`, `BRIS.JK`).
- **Docker Container (`python:3.12-slim`):** Membungkus lingkungan aplikasi agar berjalan seragam (*cross-platform*) di sistem operasi mana pun tanpa kendala perbedaan pustaka atau path direktori.
- **Auto-Commit & Push ke GitHub Remote:** Hasil pengumpulan berita baru secara otomatis di-commit dan di-push kembali ke repositori, sehingga peneliti cukup menjalankan `git pull` di laptop untuk menyinkronkan data cache terbaru.

### 2B. Data Fetcher + News Fetcher

Komponen ini adalah modul Python yang bertugas **menarik dan membersihkan** data dari sumber eksternal:

- **Data Fetcher** (`tools/data_fetcher.py`): Mengunduh data OHLCV dan Fundamental dari Yahoo Finance menggunakan pustaka `yfinance`. Modul ini menerapkan perhitungan mundur buffer 2 tahun (*2-Year Buffer Calculation*) untuk menjamin kelengkapan data indikator jangka panjang, meratakan kolom bertingkat (*MultiIndex*), dan mengonversi nama kolom ke huruf kecil (*lowercase*).
- **News Fetcher** (`tools/news_fetcher.py`): Mengunduh berita dari 3 stream RSS menggunakan pustaka `feedparser`. Modul ini memiliki mekanisme pembersihan tingkat lanjut:
  1. *Negative Keyword Filter:* Membuang artikel berita clickbait, promosi pinjaman online, dan panduan pemula non-finansial.
  2. *HTML Image Tag Stripper:* Menghapus tag gambar HTML (`<img src="...">`) dari feed berita (seperti CNBC/Detik) sehingga hanya teks inti informatif yang disimpan.
  3. *Google Boilerplate Filter:* Menyaring dan mengosongkan teks slogan Google News agar tidak menjadi noise bagi analisis sentimen LLM.
  4. *Incremental Append & Deduplication:* Memeriksa keunikan judul berita sehingga hanya artikel baru yang ditambahkan ke arsip.

### 2C. Local Cache (`data/cache/{ticker}/`)

Setelah data berhasil ditarik dan dibersihkan, Python menyimpannya secara lokal di dalam folder `data/cache/{ticker}/` sebagai **3 file master**:

| Nama File | Format | Isi |
|:---|:---|:---|
| `master_ohlcv.csv` | CSV | Seluruh data harga harian (OHLCV) historis |
| `master_fundamentals.json` | JSON | Snapshot valuasi, laporan laba rugi, dan neraca keuangan |
| `master_news.json` | JSON | Kumpulan ribuan artikel berita bersih beserta judul, tanggal, sumber, tautan, dan deskripsi informatif (*Cleaned Description*) |

Mekanisme *caching* ini menjamin efisiensi tinggi: saat simulasi perdagangan *backtesting* dijalankan, mesin cukup membaca data dari file lokal tanpa perlu mengunduh ulang dari internet, menjamin kecepatan eksekusi dan ketiadaan latensi jaringan.

### 2D. Indicator Calculator

Komponen terakhir di Fase 2 adalah **Kalkulator Indikator Teknikal** (`tools/indicator_calculator.py`). Komponen ini membaca data OHLCV dari *cache* lokal, lalu menghitung **5 kelompok indikator teknikal** berikut:

| No. | Indikator | Fungsi Analisis |
|:---|:---|:---|
| 1 | **MACD** (3 nilai: Line, Signal, Histogram) | Mengukur momentum dan arah tren harga |
| 2 | **RSI-14** (*Relative Strength Index*) | Mengukur kondisi *overbought* (jenuh beli) atau *oversold* (jenuh jual) |
| 3 | **SMA-20 & SMA-50** (*Simple Moving Average*) | Mengidentifikasi tren jangka pendek dan menengah |
| 4 | **Bollinger Bands** (3 nilai: Upper, Middle, Lower) | Mengukur volatilitas dan potensi *breakout* harga |
| 5 | **KDJ Stochastic** (3 nilai: %K, %D, %J) | Mengidentifikasi titik balik momentum harga |

Seluruh nilai indikator ini dikemas menjadi satu struktur data (*dictionary*) Python yang siap disuntikkan ke dalam instruksi (*prompt*) untuk otak AI di fase selanjutnya.

---

## TRANSISI FASE 2 → FASE 3

Pada titik ini, seluruh data sudah bersih, tersimpan secara lokal, dan diperkaya dengan indikator teknikal. Namun, **AI (LLM) tidak bisa membaca file CSV atau JSON secara langsung**. AI hanya memahami teks berbentuk bahasa manusia (*natural language*). Oleh karena itu, diperlukan proses **konversi dan pembungkusan** data menjadi teks instruksi (*prompt*) yang dapat dipahami oleh otak AI. Inilah yang terjadi di Fase 3.

Secara visual pada diagram, satu panah besar keluar dari seluruh blok Fase 2 dan masuk ke Fase 3, menandakan bahwa seluruh hasil pengolahan data (OHLCV bersih, fundamental, berita, dan indikator teknikal) semuanya diteruskan ke tahap konfigurasi AI.

---

## FASE 3: PROMPT & LLM CONFIG (*Konfigurasi Instruksi dan Model AI*)

Fase ketiga merupakan jembatan antara dunia data (Python) dan dunia kecerdasan buatan (LLM). Pada fase ini, data yang telah diolah di Fase 2 **dibungkus menjadi teks instruksi (*prompt*)** dan dikirimkan ke model AI bersama dengan konfigurasi parameter tertentu. Di dalam Fase 3, terdapat **3 komponen utama**:

### 3A. Prompt Templates

Komponen pertama adalah kumpulan **templat instruksi** yang tersimpan di folder `config/prompts/`. Setiap agen AI memiliki *prompt* khusus yang mendefinisikan dua hal penting:

- **Persona (Jabatan):** Siapa agen tersebut dan apa spesialisasinya. Contoh: *"Kamu adalah seorang Analis Fundamental elit yang mengkhususkan diri pada saham perbankan Indonesia."*
- **Aturan Jawaban:** Batasan ketat tentang format dan panjang jawaban. Contoh: *"Tuliskan laporan dalam Bahasa Indonesia formal, maksimal 3 kalimat, tanpa format Markdown."*

Data mentah (angka OHLCV, teks berita, nilai indikator) **disuntikkan (*injected*)** ke dalam templat *prompt* ini oleh Python. Dengan demikian, AI tidak hanya menerima perintah kosong, tetapi juga menerima seluruh konteks data yang dibutuhkan untuk menghasilkan analisis yang akurat.

### 3B. Temperature (Suhu AI)

Komponen kedua adalah parameter **Temperature** yang mengontrol tingkat keacakan (*randomness*) jawaban AI:

| Nilai Suhu | Simbol | Digunakan Oleh | Karakteristik |
|:---|:---|:---|:---|
| **0.0** | ❄️ Faktual | Agen Analis & Manajer | Jawaban sangat kaku, deterministik, dan konsisten. Jika ditanya 2 kali dengan data yang sama, jawabannya akan identik. Cocok untuk pelaporan fakta. |
| **0.7** | 🔥 Kreatif | Agen Debater & Researcher | Jawaban lebih beragam dan eksploratif. AI didorong untuk mencari celah argumen dan perspektif baru. Cocok untuk mekanisme perdebatan (*adversarial debate*). |

Pemisahan suhu ini merupakan keputusan desain yang krusial: agen yang bertugas melaporkan fakta (Analis) harus selalu konsisten, sementara agen yang bertugas berdebat (Bullish/Bearish) harus cukup kreatif untuk menemukan argumen dari sudut pandang yang berbeda.

### 3C. LLM Provider (Penyedia Model AI)

Komponen ketiga menunjukkan bahwa sistem ini dirancang secara **modular (*provider-agnostic*)**. Sistem tidak terkunci pada satu penyedia AI tertentu. Terdapat 3 opsi penyedia yang siap digunakan hanya dengan mengubah satu parameter konfigurasi:

| Provider | Model | Keunggulan |
|:---|:---|:---|
| **Google Gemini** *(Default)* | `gemini-flash-lite-latest` | Cepat, ringan, dan gratis (*Free Tier*) |
| **Groq** | `llama-3.3-70b-versatile` | Inferensi sangat cepat via GPU cloud |
| **Ollama** | `llama3.1:latest` | 100% lokal/offline, tanpa memerlukan koneksi internet |

Fleksibilitas ini memastikan bahwa sistem tetap dapat beroperasi meskipun salah satu penyedia mengalami gangguan atau perubahan kebijakan harga.

---

## TRANSISI FASE 3 → FASE 4

Setelah teks *prompt* (berisi data + instruksi) dan konfigurasi parameter (suhu, model) disiapkan di Fase 3, paket instruksi tersebut **dikirimkan melalui API ke server penyedia LLM** (misalnya, server Google Gemini). Di sinilah kendali berpindah dari mesin lokal pengguna ke infrastruktur *cloud* penyedia AI. Fase 4 menjelaskan apa yang terjadi **di dalam otak model AI** saat ia menerima dan memproses teks *prompt* tersebut.

---

## FASE 4: OTAK LLM (*Proses Internal Large Language Model*)

Fase keempat menggambarkan proses komputasi yang terjadi **di dalam arsitektur internal model *Large Language Model* (LLM)** — dalam hal ini, Google Gemini. Fase ini bersifat transparan bagi pengguna (pengguna tidak dapat mengintervensi prosesnya), namun pemahaman terhadap mekanisme internalnya penting untuk menjelaskan **mengapa AI mampu menghasilkan analisis yang koheren**. Terdapat **3 tahapan komputasi utama**:

### 4A. Tokenisasi (*Tokenization*)

Tahapan pertama adalah **pemecahan teks menjadi unit-unit kecil bernama *token***. AI tidak memahami huruf atau kata dalam bahasa manusia secara langsung. Seluruh teks *prompt* (termasuk data angka dan instruksi) dipecah menjadi potongan-potongan kecil, lalu setiap potongan dikonversi menjadi representasi numerik berupa **vektor *embedding*** — yaitu deretan angka desimal yang merepresentasikan makna semantik dari token tersebut dalam ruang vektor berdimensi tinggi.

**Contoh:** Teks `"Laba BBRI Naik"` dipecah menjadi token `["Laba", " BB", "RI", " Na", "ik"]`, lalu setiap token diubah menjadi vektor numerik seperti `[[0.12, -0.45, ...], [0.88, 0.31, ...], ...]`.

### 4B. Multi-Head Attention (Mekanisme Q, K, V)

Tahapan kedua adalah inti dari arsitektur *Transformer* — yaitu mekanisme **Scaled Dot-Product Attention**. Pada tahapan ini, AI membangun pemahaman tentang **hubungan antar setiap token** di dalam teks. Setiap token menghasilkan tiga vektor:

- **Query (Q):** *"Informasi apa yang sedang dicari oleh token ini?"*
- **Key (K):** *"Label informasi apa yang dimiliki oleh token ini?"*
- **Value (V):** *"Makna inti dari token ini."*

Jika skor kecocokan antara Query suatu token dengan Key token lainnya tinggi, maka Value dari token tersebut akan diekstrak dan digunakan. Proses ini dilakukan secara paralel oleh **beberapa "kepala" (*heads*)** yang masing-masing fokus pada aspek hubungan yang berbeda (misalnya: satu kepala fokus pada hubungan tata bahasa, kepala lain fokus pada hubungan numerik, dan kepala lain fokus pada sentimen). Hasil dari seluruh kepala kemudian digabungkan.

### 4C. Normalisasi (*Layer Normalization*)

Tahapan terakhir adalah **stabilisasi nilai numerik** yang dihasilkan oleh proses *Attention*. Setelah melalui perhitungan matriks yang kompleks, angka-angka vektor bisa menjadi sangat besar atau sangat kecil (*exploding/vanishing gradient*). Normalisasi bertugas menyeimbangkan (*scaling*) angka-angka tersebut agar model AI tetap stabil dan tidak menghasilkan teks yang tidak koheren (*halusinasi*).

Ketiga tahapan ini (Tokenisasi → Attention → Normalisasi) **berulang sebanyak puluhan lapisan (*layers*)** di dalam model Gemini sebelum akhirnya menghasilkan teks jawaban yang dikirim kembali ke Python.

---

## TRANSISI FASE 4 → FASE 5

Setelah otak LLM memproses *prompt* dan menghasilkan teks jawaban, jawaban tersebut **diterima kembali oleh Python di mesin lokal pengguna**. Namun, satu kali pemanggilan LLM hanya menghasilkan jawaban dari **satu agen AI saja**. Sistem ini memiliki **12 agen** yang masing-masing harus dipanggil secara terpisah dengan *prompt* yang berbeda-beda. Siapa yang mengatur urutan pemanggilan ke-12 agen ini? Itulah tugas Fase 5 — **orkestrator utama** yang bertindak sebagai "Manajer Lalu Lintas" untuk memastikan setiap agen bekerja pada urutan yang tepat.

---

## FASE 5: ORKESTRASI 12-AGEN — LangGraph DAG (*Directed Acyclic Graph*)

Fase kelima adalah **jantung dan inti dari seluruh sistem**. Pada fase ini, pustaka **LangGraph** mengatur 12 agen AI untuk bekerja secara terkoordinasi menggunakan teori **Directed Acyclic Graph (DAG)** — sebuah struktur graf berarah yang menjamin aliran data hanya bergerak maju (tidak pernah berputar balik), sehingga sistem terhindar dari kebuntuan (*infinite loop*). Ke-12 agen diorganisasikan ke dalam **4 lapisan hierarkis**:

### Lapis 1: 4 Analis Spesialis (Paralel)

Lapisan pertama terdiri dari **4 agen analis** yang bekerja secara **paralel (bersamaan)** untuk menghemat waktu:

| Agen | Spesialisasi | Data yang Dibaca |
|:---|:---|:---|
| **Analis Fundamental** | Mengevaluasi kesehatan keuangan perusahaan (valuasi, laba, utang) | `master_fundamentals.json` |
| **Analis Teknikal** | Menganalisis pola harga dan sinyal indikator teknikal | `master_ohlcv.csv` + Indikator (MACD, RSI, dll.) |
| **Analis Sentimen** | Membaca suasana pasar dari berita spesifik saham | `master_news.json` (berita spesifik) |
| **Analis Makroekonomi** | Mengevaluasi dampak kebijakan BI/OJK terhadap sektor perbankan | `master_news.json` (berita makro) |

Setiap analis membaca data mentah yang berbeda, lalu **menyimpulkannya menjadi maksimal 3 kalimat padat**. Hanya kesimpulan ringkas inilah (bukan data mentah) yang diteruskan ke lapisan berikutnya melalui mekanisme **AgentState (Memori Estafet)**.

### Lapis 2: Debat Adversarial (Bullish ⚔ Bearish)

Setelah ke-4 analis selesai, lapisan kedua memulai **mekanisme perdebatan (*adversarial debate*)**:

- **Agen Bullish** membaca kesimpulan 4 analis dan membangun argumen terkuat **mengapa saham ini layak dibeli**.
- **Agen Bearish** membaca kesimpulan 4 analis yang sama dan membangun argumen terkuat **mengapa saham ini harus dijual/dihindari**.
- **Fasilitator Debat** merangkum kedua argumen tersebut menjadi satu **konsensus penelitian** yang seimbang.

Mekanisme debat ini bertujuan untuk **menekan halusinasi dan *overconfidence*** pada LLM. Jika hanya ada satu AI yang menganalisis, AI tersebut cenderung terlalu percaya diri (*overconfident*) terhadap kesimpulannya sendiri. Dengan adanya dua pihak yang saling menantang, kelemahan argumen akan terekspos secara alami.

### Lapis 3: Manajemen Risiko (Konservatif 🛡 Agresif)

Lapisan ketiga mengevaluasi **toleransi risiko** dari dua perspektif yang berlawanan:

- **Agen Risiko Konservatif** memprioritaskan keamanan modal dan menyarankan posisi yang lebih kecil atau defensif.
- **Agen Risiko Agresif** memprioritaskan potensi keuntungan dan menyarankan posisi yang lebih besar atau ofensif.
- **Fasilitator Risiko** merangkum kedua perspektif menjadi satu **konsensus risiko** yang menyeimbangkan keamanan dan peluang.

### Lapis 4: Pengambilan Keputusan (Portfolio Manager → Trading Agent)

Lapisan terakhir merupakan puncak hierarki:

- **Portfolio Manager (PM)** bertindak sebagai **"Hakim Tertinggi"**. Ia membaca konsensus debat (dari Lapis 2) dan konsensus risiko (dari Lapis 3), lalu mengambil keputusan akhir: apakah saham ini harus **dibeli (BUY)**, **dijual (SELL)**, atau **ditahan (HOLD)**, beserta jumlah lot dan tingkat keyakinan (*confidence*).
- **Trading Agent** menerima instruksi dari PM dan memformatnya menjadi keluaran **JSON terstruktur** yang dapat langsung dieksekusi oleh mesin transaksi Python.

### Komponen Pendukung: AgentState (Memori Estafet)

Di sisi kanan Fase 5 pada diagram terdapat bilah vertikal bertuliskan **"AgentState Memori Estafet"**. Ini adalah komponen kritis yang memastikan **tidak ada informasi yang hilang** saat data berpindah dari satu agen ke agen lainnya. AgentState berupa struktur data `TypedDict` (berbentuk JSON) yang dioper dari lapisan ke lapisan. Setiap agen menulis hasil kerjanya ke dalam kotak (*field*) yang telah ditentukan di dalam AgentState, dan agen berikutnya dapat membaca kotak tersebut tanpa perlu membaca ulang data mentah atau riwayat percakapan yang panjang. Mekanisme ini dilengkapi dengan **Reducer** — sebuah fungsi khusus LangGraph yang memastikan ketika beberapa agen menulis ke kotak yang sama secara bersamaan (paralel), tulisan mereka **digabungkan (*merge*)** dan bukan saling menimpa.

---

## TRANSISI FASE 5 → FASE 6

Setelah ke-12 agen selesai menjalankan tugasnya dan Trading Agent telah memformat keputusan akhir dalam bentuk JSON, seluruh hasil kerja agen — mulai dari teks analisis, argumen debat, evaluasi risiko, hingga keputusan final — **diekstrak dari AgentState dan dicetak ke dalam file output** yang dapat dibaca oleh manusia maupun mesin. Proses pencetakan ini dilakukan oleh Python di dalam modul `backtester.py`.

---

## FASE 6: OUTPUT SISTEM

Fase keenam menghasilkan **2 jenis keluaran** yang masing-masing melayani kebutuhan yang berbeda:

### 6A. Reasoning Log (.txt) — Explainable AI (XAI)

Keluaran pertama adalah **file log teks** yang berisi seluruh rekam jejak pemikiran dari ke-12 agen. File ini mencatat:

- Apa yang dilaporkan oleh setiap analis.
- Argumen apa yang diajukan oleh Agen Bullish dan Agen Bearish.
- Bagaimana konsensus debat dan risiko dirumuskan.
- Mengapa Portfolio Manager mengambil keputusan tertentu.

File ini berfungsi sebagai **bukti transparansi keputusan AI (*Explainable AI / XAI*)**. Dalam konteks skripsi, file log ini menjadi bahan utama pembahasan di **Bab 4 (Hasil dan Pembahasan)**, di mana peneliti dapat menunjukkan bahwa keputusan AI bukan merupakan "kotak hitam" yang tidak dapat dijelaskan, melainkan proses deliberasi terstruktur yang dapat dilacak dan diaudit.

### 6B. Trade Decision (JSON) — Keputusan Transaksi

Keluaran kedua adalah **keputusan transaksi** dalam format JSON terstruktur yang berisi tiga informasi utama:

```json
{
  "action": "BUY",
  "quantity": 500,
  "confidence": 0.85
}
```

- **action:** Aksi yang direkomendasikan (BUY / SELL / HOLD).
- **quantity:** Jumlah lot saham yang disarankan untuk diperdagangkan.
- **confidence:** Tingkat keyakinan AI terhadap rekomendasinya (skala 0.0 hingga 1.0).

Format JSON ini dirancang agar dapat langsung diproses oleh mesin transaksi Python tanpa perlu interpretasi manual, sehingga cocok untuk digunakan baik dalam *backtesting* otomatis maupun *forward testing* di masa depan.

---

## TRANSISI FASE 6 → FASE 7

Kedua keluaran dari Fase 6 (file log teks dan keputusan JSON/CSV) sudah cukup untuk keperluan *backtesting* dan analisis akademis. Namun, agar sistem ini dapat **didemonstrasikan secara visual** — baik kepada dosen penguji saat sidang maupun kepada calon pengguna (investor) — diperlukan sebuah **antarmuka grafis** yang menyajikan hasil-hasil tersebut dalam bentuk yang interaktif dan mudah dipahami. Inilah peran Fase 7.

---

## FASE 7: ANTARMUKA PENGGUNA (*User Interface*)

Fase ketujuh dan terakhir merupakan lapisan presentasi yang menghubungkan sistem AI dengan **manusia (pengguna akhir)**. Antarmuka ini dibangun menggunakan framework **Streamlit** — sebuah pustaka Python yang memungkinkan pembuatan aplikasi web interaktif secara cepat tanpa memerlukan pengetahuan tentang HTML, CSS, atau JavaScript.

### Fitur Utama Dashboard:

| Tab | Fungsi |
|:---|:---|
| **Tab 1: Live AI Debate** | Menampilkan teks perdebatan antar-agen AI secara *streaming* (berjalan satu per satu di layar), sehingga pengguna dapat menyaksikan proses berpikir AI secara transparan dan *real-time*. Di akhir, ditampilkan kartu keputusan akhir (BUY/SELL/HOLD) beserta tingkat keyakinan dan penjelasan singkat (*XAI*). |
| **Tab 2: Backtest Charts** | Menampilkan grafik performa portofolio hasil *backtesting* historis, termasuk perbandingan strategi 12-Agen vs *baseline* (SMA, MACD, *Buy & Hold*) dan grafik *candlestick* dengan penanda titik beli/jual. |

### Pengguna Akhir: Investor

Di bagian paling bawah Fase 7 terdapat ikon **Investor/Pengguna** yang dihubungkan oleh **panah dua arah** dengan dashboard Streamlit. Panah dua arah ini menandakan bahwa interaksi bersifat **interaktif**: pengguna dapat memilih *ticker* saham, menentukan modal awal, dan menekan tombol "Mulai Analisis", lalu sistem akan merespons dengan menampilkan hasil analisis AI secara visual.

---