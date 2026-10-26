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
| 3 | **CNBC Indonesia** | *(Tanpa query — URL RSS langsung)* | Mengambil seluruh **headline berita pasar modal** terbaru dari portal berita keuangan terbesar di Indonesia |

Ketiga aliran berita ini kemudian digabungkan menjadi satu kumpulan dan dibersihkan dari judul yang duplikat (*deduplikasi*). Total berita unik yang tersimpan mencapai **±130–140 artikel**. Data berita ini merupakan bahan baku utama bagi **Agen Analis Sentimen** (untuk membaca suasana pasar terhadap saham tertentu) dan **Agen Analis Makroekonomi** (untuk memahami dampak kebijakan BI/OJK terhadap harga saham perbankan).

---

## TRANSISI FASE 1 → FASE 2

Setelah seluruh data mentah berhasil diidentifikasi dari ketiga sumber di atas, data tersebut **belum bisa langsung digunakan oleh AI**. Data masih berupa respons mentah dari API internet yang formatnya berantakan dan belum terstandarisasi. Oleh karena itu, data tersebut harus melewati proses pembersihan, penyimpanan, dan pengayaan terlebih dahulu. Di sinilah peran Fase 2 dimulai — Python bertindak sebagai **"Tangan"** yang menerima data mentah dari "Mata" (Fase 1), membersihkannya, menyimpannya secara lokal, dan menghitung indikator tambahan sebelum data siap diserahkan ke otak AI.

Secara visual pada diagram, panah dari ketiga kotak sumber data di Fase 1 (Yahoo Finance OHLCV, Yahoo Finance Fundamental, dan 3 RSS Berita) semuanya **berkonvergensi** (menyatu) menuju satu titik masuk di Fase 2, yaitu kotak **Data Fetcher + News Fetcher**.

---

## FASE 2: PYTHON ENGINE (*Pra-Pemrosesan Data*)

Fase kedua merupakan dapur pengolahan data yang sepenuhnya dijalankan oleh **Python** secara lokal di komputer pengguna. Pada fase ini, tidak ada AI yang terlibat — semua proses bersifat deterministik (hasilnya selalu sama jika inputnya sama). Di dalam Fase 2, terdapat **3 komponen utama** yang bekerja secara berurutan:

### 2A. Data Fetcher + News Fetcher

Komponen pertama adalah dua fungsi Python yang bertugas **menarik dan membersihkan** data dari sumber eksternal di Fase 1:

- **Data Fetcher** (`tools/data_fetcher.py`): Mengunduh data OHLCV dan Fundamental dari Yahoo Finance menggunakan pustaka `yfinance`. Setelah data berhasil diunduh, Python melakukan pembersihan otomatis: meratakan kolom bertingkat (*MultiIndex*), mengonversi nama kolom ke huruf kecil, dan menghapus kolom duplikat.
- **News Fetcher** (`tools/news_fetcher.py`): Mengunduh berita dari 3 stream RSS menggunakan pustaka `feedparser`. Setelah ketiga aliran digabungkan, Python menghapus artikel dengan judul yang sama (*deduplikasi*) agar tidak ada informasi yang terhitung ganda.

### 2B. Local Cache

Setelah data berhasil ditarik dan dibersihkan, Python menyimpannya secara lokal di dalam folder `data/cache/{ticker}/` sebagai **3 file master**:

| Nama File | Format | Isi |
|:---|:---|:---|
| `master_ohlcv.csv` | CSV | Seluruh data harga harian (OHLCV) historis |
| `master_fundamentals.json` | JSON | Snapshot valuasi, laporan laba rugi, dan neraca keuangan |
| `master_news.json` | JSON | Kumpulan ±130–140 artikel berita unik beserta judul, tanggal, sumber, dan tautan |

Mekanisme *caching* ini memiliki manfaat penting: jika sistem dijalankan berulang kali (misalnya saat *backtesting* 16 minggu), Python tidak perlu mengunduh ulang data dari internet setiap kali. Python cukup membaca data dari file lokal yang sudah tersimpan, sehingga proses menjadi **sangat cepat dan hemat kuota internet**.

### 2C. Indicator Calculator

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

#  Topologi Directed Acyclic Graph (DAG) — Orkestrasi 12 Agen AI via LangGraph

---

## GAMBARAN UMUM

Diagram ini menggambarkan **struktur organisasi internal dari mesin kecerdasan buatan** yang menjadi inti sistem *Multi-Agent LLM Trading*. Sistem ini menggunakan 12 agen AI yang diorganisasikan ke dalam 4 tim hierarkis menggunakan kerangka kerja **LangGraph** dengan pola arsitektur **Directed Acyclic Graph (DAG)**.

**DAG** berarti aliran data bersifat **satu arah dan tidak pernah berputar balik**. Setiap agen hanya menerima data dari tim sebelumnya dan meneruskan kesimpulannya ke tim berikutnya — persis seperti rantai komando di sebuah perusahaan investasi nyata.

Fondasi yang menghubungkan seluruh 12 agen adalah **TradingState** — sebuah objek memori bersama yang dioper dari satu tim ke tim berikutnya, memastikan tidak ada informasi yang hilang dalam perjalanan.

---

## TIM 1: ANALIS — Analisis Data Dasar

### Karakteristik Utama: Bekerja Secara PARALEL

Tim Analis adalah titik masuk pertama dari seluruh alur kerja AI. Tim ini terdiri dari **4 agen spesialis** yang bekerja secara **paralel (bersamaan)** — artinya keempat agen ini dijalankan serentak oleh LangGraph, bukan secara berurutan. Hal ini dilakukan untuk menghemat waktu komputasi.

Setiap agen di Tim Analis memiliki akses langsung ke data mentah yang sudah disimpan di *cache* lokal (Fase 2), namun masing-masing hanya membaca jenis data yang relevan dengan spesialisasinya.

### Agen 1: Fundamental Analyst
**Sumber Data:** `master_fundamentals.json`

Agen ini bertugas membedah **kesehatan keuangan perusahaan** dari sudut pandang akuntansi dan valuasi. Ia membaca laporan laba rugi (*income statement*), neraca keuangan (*balance sheet*), dan metrik valuasi seperti Rasio Harga terhadap Laba (P/E), Rasio Harga terhadap Nilai Buku (P/B), dan Imbal Hasil Dividen (*Dividend Yield*). Agen ini menjawab pertanyaan mendasar: *"Apakah perusahaan ini secara finansial sehat dan apakah harganya wajar?"*

### Agen 2: Technical Analyst
**Sumber Data:** `master_ohlcv.csv` + Indikator Teknikal

Agen ini bertugas membaca **pola pergerakan harga saham** menggunakan indikator-indikator matematika yang telah dihitung sebelumnya oleh *Indicator Calculator* (Fase 2). Indikator yang dianalisis meliputi MACD (momentum tren), RSI-14 (kondisi jenuh beli/jual), SMA-20 dan SMA-50 (tren rata-rata bergerak), Bollinger Bands (volatilitas), dan KDJ Stochastic (titik balik momentum). Agen ini menjawab pertanyaan: *"Ke mana arah harga bergerak dalam waktu dekat berdasarkan sinyal teknikal?"*

### Agen 3: Sentiment Analyst
**Sumber Data:** `master_news.json` (berita spesifik saham)

Agen ini bertugas **mengukur suasana pasar** terhadap saham tertentu dengan membaca berita-berita terkini dari Google News (query: nama ticker) dan CNBC Indonesia. Agen ini menentukan apakah sentimen pasar secara keseluruhan bersifat positif, negatif, atau netral terhadap saham yang dianalisis. Agen ini menjawab pertanyaan: *"Apa yang dibicarakan publik dan media tentang saham ini hari ini?"*

### Agen 4: Macro Analyst
**Sumber Data:** `master_news.json` (berita makroekonomi)

Agen ini bertugas menganalisis **kondisi lingkungan ekonomi makro** yang dapat mempengaruhi kinerja saham secara tidak langsung. Ia fokus pada berita seputar kebijakan suku bunga Bank Indonesia (BI-7DRR), tingkat inflasi, regulasi Otoritas Jasa Keuangan (OJK), dan dinamika pasar global. Agen ini menjawab pertanyaan: *"Apakah kondisi ekonomi makro saat ini mendukung atau menghambat kinerja sektor perbankan?"*

---

## ⟶ TRANSISI 1: Tim Analis → Tim Peneliti
### Label: "Laporan Analisis (3 kalimat per agen)"

Setelah keempat agen analis selesai bekerja secara paralel, masing-masing agen menghasilkan **satu laporan singkat maksimal 3 kalimat** yang disimpan ke dalam *TradingState*. Pembatasan 3 kalimat ini bukan kebetulan, melainkan merupakan keputusan desain yang disengaja berdasarkan dua alasan teknis:

**1. Mencegah Information Overload pada LLM:**
Jika setiap analis menulis laporan sepanjang beberapa halaman, agen-agen di Tim Peneliti harus memproses teks yang sangat panjang sekaligus. LLM yang dibebani konteks terlalu besar cenderung kehilangan fokus, memberikan jawaban yang tidak relevan, atau bahkan berhalusinasi (*Decision Paralysis*).

**2. Prinsip Executive Summary (Hierarki Informasi):**
Sistem ini menerapkan prinsip manajemen nyata: seorang analis tidak menyerahkan spreadsheet mentah kepada manajernya, melainkan menyajikan *Executive Summary* yang padat dan tajam. Tim Peneliti hanya perlu tahu **kesimpulan** dari setiap analis, bukan seluruh proses kalkulasi di baliknya.

**Isi data yang mengalir ke Tim Peneliti:**
Total **±12 kalimat** (4 agen × 3 kalimat) yang dioper melalui TradingState. Contoh bentuknya:
> - *Fundamental:* "Saham BBRI memiliki valuasi P/E yang murah dibanding rata-rata industri. Laba bersih kuartal ini tumbuh 15% YoY. Secara fundamental kondisi keuangan sangat solid."
> - *Technical:* "Indikator RSI-14 saat ini menunjukkan kondisi oversold di angka 28. MACD baru saja membentuk sinyal golden cross. Tren jangka pendek mengindikasikan potensi pembalikan arah ke atas."
> - *Sentiment:* "Sentimen pasar terhadap BBRI cenderung positif dalam 3 hari terakhir. Mayoritas berita membahas ekspektasi dividen yang tinggi. Tidak ditemukan berita negatif material."
> - *Macro:* "Bank Indonesia mempertahankan suku bunga di level 6,25% dalam rapat terakhir. Kondisi ini menguntungkan margin bunga bersih perbankan. Stabilitas nilai tukar Rupiah turut mendukung prospek sektor."

---

## TIM 2: PENELITI — Sintesis melalui Debat Adversarial

### Karakteristik Utama: Mekanisme Debat (Bullish vs Bearish)

Tim Peneliti adalah tim paling unik dalam arsitektur ini karena mengimplementasikan **mekanisme debat adversarial** — dua agen AI yang sengaja diberi instruksi untuk mengambil posisi yang **saling berlawanan** berdasarkan data yang sama persis.

### Agen 5: Bullish Researcher 🟢
Agen ini membaca 12 kalimat laporan dari Tim Analis dan bertugas membangun **argumen terkuat mengapa saham ini layak untuk dibeli (BUY)**. Ia diperintahkan untuk mencari, memilih, dan menonjolkan semua sinyal positif, peluang, dan katalis kenaikan harga yang ada dalam laporan analis.

### Agen 6: Bearish Researcher 🔴
Agen ini membaca **data yang persis sama** dengan Bullish Researcher, namun bertugas membangun **argumen terkuat mengapa saham ini sebaiknya dijual atau dihindari (SELL/AVOID)**. Ia diperintahkan untuk mencari risiko tersembunyi, kelemahan argumen bullish, dan skenario penurunan yang mungkin terjadi.

> **Mengapa sengaja dibuat berlawanan?**
> Berdasarkan teori *AI Safety via Debate* (Irving et al., 2018 - DeepMind), dua AI yang dipaksa berdebat dari posisi yang berlawanan akan saling mengekspos kelemahan argumen masing-masing, sehingga menghasilkan analisis yang jauh lebih jujur dan komprehensif dibandingkan satu AI yang menganalisis sendiri tanpa penantang.

### Agen 7: Research Facilitator ⚖️
Setelah Bullish dan Bearish Researcher masing-masing menyelesaikan argumennya, Research Facilitator bertindak sebagai **moderator yang objektif**. Ia membaca kedua argumen tersebut secara netral, menimbang kekuatan dan kelemahan setiap sisi, lalu menyusun **Research Consensus** — sebuah kesimpulan tunggal yang menyeimbangkan kedua perspektif dan memberikan rekomendasi awal (cenderung beli, cenderung jual, atau tidak jelas / *hold*).

---

## ⟶ TRANSISI 2: Tim Peneliti → Tim Manajemen Risiko
### Label: "Research Consensus"

Yang dikirimkan ke Tim Manajemen Risiko **bukanlah** seluruh transkrip perdebatan antara Bullish dan Bearish Researcher. Yang dikirim hanyalah **Research Consensus** — satu dokumen ringkas hasil sintesis moderator (sekitar 3–5 kalimat) yang sudah mewakili pandangan kedua sisi secara seimbang.

**Prinsip ini krusial:** Tim Manajemen Risiko tidak perlu membaca ulang seluruh laporan dari Tim Analis maupun perdebatan lengkap Bullish vs Bearish. Mereka hanya menerima "paket kesimpulan matang" dari Research Facilitator. Semakin ke kanan (semakin dekat ke keputusan akhir), semakin sedikit volume teks yang harus dibaca oleh setiap agen — efisiensi ini mencegah *token overload* dan menjaga ketajaman keputusan AI.

---

## TIM 3: MANAJEMEN RISIKO — Evaluasi Risiko

### Karakteristik Utama: Evaluasi Dua Perspektif Risiko

Tim Manajemen Risiko menerapkan **prinsip yang sama** dengan Tim Peneliti — dua agen dengan perspektif berlawanan — namun fokusnya bukan lagi pada arah harga, melainkan pada **dimensi risiko dan ukuran posisi** (*position sizing*).

### Agen 8: Aggressive Risk Analyst 🔥
Agen ini mengevaluasi Research Consensus dari **perspektif peluang keuntungan maksimal**. Ia akan mempertimbangkan: *"Jika konsensus ini benar, berapa potensi keuntungan yang bisa diraih? Apakah layak mengambil posisi besar?"* Agen ini secara alamiah akan merekomendasikan ukuran posisi yang lebih besar dan toleransi risiko yang lebih tinggi.

### Agen 9: Conservative Risk Analyst 🛡️
Agen ini mengevaluasi Research Consensus yang sama dari **perspektif pelestarian modal dan perlindungan terhadap kerugian maksimal (drawdown)**. Ia akan mempertimbangkan: *"Jika konsensus ini salah, berapa kerugian yang bisa terjadi? Apakah portofolio kita aman jika skenario terburuk terjadi?"* Agen ini secara alamiah akan merekomendasikan ukuran posisi yang lebih kecil atau bahkan merekomendasikan untuk tidak bertransaksi sama sekali.

### Agen 10: Risk Facilitator 🤝
Risk Facilitator bertugas **menyeimbangkan rekomendasi** dari Aggressive dan Conservative Risk Analyst untuk menghasilkan **Risk Consensus** — sebuah panduan yang berisi rekomendasi ukuran posisi (*position sizing*) yang optimal. Panduan ini menjawab: *"Berapa persen dari total modal yang sebaiknya dialokasikan untuk transaksi ini, dan berapa batas kerugian maksimal yang dapat diterima (stop-loss)?"*

---

## ⟶ TRANSISI 3: Tim Manajemen Risiko → Tim Eksekusi
### Label: "Risk Consensus"

Sama seperti transisi sebelumnya, yang dikirimkan ke Tim Eksekusi hanyalah **Risk Consensus** — satu dokumen ringkas berisi panduan ukuran posisi dan batasan risiko (sekitar 3 kalimat). Portfolio Manager di Tim Eksekusi akan menerima **dua paket kesimpulan sekaligus**:

1. **Research Consensus** — *"Apa sinyal pasar dan rekomendasi arah transaksinya?"*
2. **Risk Consensus** — *"Berapa besar posisi yang aman dan apa batas risikonya?"*

Dengan hanya memiliki dua paket ringkas ini (total sekitar 6–10 kalimat), Portfolio Manager dapat membuat keputusan yang sangat tajam tanpa terbebani oleh ribuan baris data historis atau ratusan kalimat transkrip perdebatan.

---

## TIM 4: EKSEKUSI — Keputusan Akhir

### Karakteristik Utama: Hierarki Komando Tunggal

Tim Eksekusi adalah **puncak hierarki** dari seluruh sistem. Tidak ada lagi debat di sini — hanya ada satu rantai komando yang jelas dari Portfolio Manager ke Trading Agent.

### Agen 11: Portfolio Manager 👑
Portfolio Manager adalah **"Hakim Tertinggi"** dari seluruh proses. Ia menerima Research Consensus dan Risk Consensus, lalu menggabungkannya dengan **kondisi portofolio terkini** (saldo kas yang tersedia, posisi saham yang sudah dimiliki, dan eksposur risiko saat ini) untuk mengambil **keputusan investasi final**:

- **BUY:** Beli saham dalam jumlah yang ditentukan Risk Consensus
- **SELL:** Jual saham yang sudah dimiliki
- **HOLD:** Tidak melakukan transaksi apapun, pertahankan posisi saat ini

Portfolio Manager juga menentukan **tingkat keyakinan (*confidence*)** terhadap keputusannya dalam skala 0.0 (tidak yakin sama sekali) hingga 1.0 (sangat yakin).

### ⟶ Transisi Internal: Portfolio Manager → Trading Agent
### Label: "Instruksi Keputusan"

Portfolio Manager mengirimkan instruksi keputusan dalam bahasa natural kepada Trading Agent, misalnya: *"Beli saham BBRI sebanyak 500 lembar dengan tingkat keyakinan 85%."*

### Agen 12: Trading Agent 🤖
Trading Agent adalah **"Penerjemah"** — ia tidak membuat keputusan baru, melainkan mengonversi instruksi dari Portfolio Manager menjadi format data terstruktur yang dapat langsung dibaca dan dieksekusi oleh mesin Python. Dalam prosesnya, Trading Agent juga menghitung:

- **Penyesuaian Satuan Lot:** Di Bursa Efek Indonesia (BEI), saham diperdagangkan dalam satuan lot (1 lot = 100 lembar). Jika PM memerintahkan "beli 500 lembar", Trading Agent mengonversinya menjadi "beli 5 lot".
- **Perhitungan Biaya Transaksi:** Setiap transaksi dikenakan biaya broker sebesar **0,2%** dari nilai transaksi. Trading Agent memperhitungkan biaya ini agar kalkulasi portofolio tetap realistis.

### OUTPUT AKHIR: JSON Eksekusi

```json
{
  "action": "BUY",
  "quantity": 500,
  "confidence": 0.85
}
```

Format JSON ini langsung dibaca oleh mesin *backtesting* Python untuk memperbarui saldo dan posisi portofolio secara otomatis.

---

## KOMPONEN FONDASI: TradingState — Memori Estafet

Bilah biru di bagian bawah diagram dengan panah putus-putus ke setiap tim merepresentasikan **TradingState** — komponen paling kritis yang sering terlewat namun menjadi tulang punggung seluruh sistem.

TradingState adalah sebuah objek Python bertipe `TypedDict` yang berfungsi sebagai **"papan tulis bersama"** yang dibawa dari satu tim ke tim berikutnya. Setiap agen **membaca** informasi yang dibutuhkannya dari TradingState, lalu **menuliskan** hasil kerjanya kembali ke TradingState sebelum meneruskannya ke agen berikutnya.

Tanpa TradingState, setiap agen akan bekerja dalam isolasi penuh — Bullish Researcher tidak akan tahu apa yang sudah ditulis oleh Fundamental Analyst, dan Portfolio Manager tidak akan bisa membaca Research Consensus yang dibuat oleh Research Facilitator.

**Mekanisme Reducer (Pencegah Konflik Tulis Paralel):**
Karena ke-4 agen di Tim Analis bekerja **secara paralel** dan semuanya akan menulis ke TradingState pada saat yang bersamaan, terdapat risiko bahwa hasil tulisan satu agen akan menimpa (*overwrite*) hasil tulisan agen lain. LangGraph mengatasi ini dengan **Reducer** — sebuah fungsi khusus yang memastikan setiap hasil tulisan dari agen paralel **digabungkan (*merge*)**, bukan saling menimpa.

---

## KESIMPULAN ALUR KESELURUHAN

```
Data Mentah (CSV, JSON, Berita)
        ↓
[TIM 1: 4 ANALIS — Paralel]
Fundamental + Technical + Sentiment + Macro
        ↓ (12 kalimat laporan singkat)
[TIM 2: 3 PENELITI — Debat Adversarial]
Bullish ⚔ Bearish → Research Facilitator
        ↓ (Research Consensus: 3-5 kalimat)
[TIM 3: 3 MANAJEMEN RISIKO — Evaluasi]
Aggressive 🔥 vs Conservative 🛡 → Risk Facilitator
        ↓ (Risk Consensus: 3 kalimat)
[TIM 4: 2 EKSEKUSI — Keputusan]
Portfolio Manager 👑 → Trading Agent 🤖
        ↓
OUTPUT: {"action":"BUY", "quantity":500, "confidence":0.85}
```

Setiap perpindahan antar-tim selalu mengompresi informasi menjadi lebih ringkas — memastikan agen di lapisan atas menerima **kebijaksanaan tersuling**, bukan kumpulan data mentah. Inilah yang membuat sistem ini **efisien, hemat biaya API, dan tahan terhadap halusinasi AI**.

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

## GAMBARAN UMUM

Diagram ini menggambarkan arsitektur pipeline pengumpulan, pembersihan, penyimpanan, dan penyajian data yang menjadi fondasi bagi seluruh sistem kecerdasan buatan Multi-Agent LLM Trading. Diagram terbagi ke dalam **6 lapisan fungsional** yang tersusun secara vertikal dari atas ke bawah, menggambarkan perjalanan data dari dunia luar (Internet) hingga siap dikonsumsi oleh 4 Agen Analis AI.

Tujuan utama dari diagram ini adalah membuktikan bahwa sistem memiliki jalur data yang transparan, terstruktur, dan bebas dari kecurangan informasi masa depan (*Look-Ahead Bias*) — sebuah syarat mutlak dalam penelitian perdagangan kuantitatif yang valid secara akademis.

---

## LAPISAN 1: SUMBER DATA EKSTERNAL (INTERNET)

Lapisan paling atas pada diagram menggambarkan 5 sumber data mentah dari internet yang menjadi bahan bakar utama seluruh sistem. Kelima sumber ini terbagi menjadi dua kategori besar:

### Kategori A: Data Kualitatif (Teks Berita) — 3 Sumber RSS
* **Google News RSS — Query: `{ticker} saham`**  
  Sumber ini menarik berita-berita spesifik yang membahas emiten perbankan tertentu secara langsung. Misalnya, untuk ticker `BBRI.JK`, query yang dikirimkan ke Google News adalah *"BBRI saham"*. Hasil yang dikembalikan adalah kumpulan judul berita (*headline*) seperti: *"Investor Asing Borong Saham BBRI Rp 1,53 Triliun"*, *"Laba Bersih BBRI Naik 15% di Kuartal I"*, dan sejenisnya. Berita jenis ini menjadi bahan bacaan bagi **Sentiment Analyst** untuk menentukan suasana pasar terhadap saham tersebut.
* **Google News RSS — Query: `suku bunga BI OJK`**  
  Sumber ini menarik berita-berita makroekonomi nasional yang tidak spesifik pada satu emiten, melainkan berdampak pada keseluruhan sektor perbankan. Contoh topik yang ditarik: kebijakan suku bunga acuan Bank Indonesia (BI-7DRR), regulasi Otoritas Jasa Keuangan (OJK), tingkat inflasi, dan stabilitas nilai tukar Rupiah. Berita jenis ini menjadi bahan bacaan bagi **Macro Analyst**.
* **CNBC Indonesia RSS — Stream: Market Feed**  
  Sumber ini menarik berita umum pasar modal dan pergerakan bursa efek dari portal berita keuangan terkemuka di Indonesia. Topiknya mencakup dinamika Indeks Harga Saham Gabungan (IHSG), aksi korporasi emiten besar, serta sentimen investor global terhadap pasar berkembang (*emerging market*). Berita dari sumber ini turut melengkapi analisis kedua agen di atas (Sentiment dan Macro).

### Kategori B: Data Kuantitatif (Angka Numerik) — 2 Sumber Yahoo Finance API
* **Yahoo Finance API — OHLCV Daily Historical**  
  Sumber ini menarik deret waktu harga transaksi saham harian yang terdiri dari 5 kolom standar pasar modal: Open (Harga Pembukaan), High (Harga Tertinggi), Low (Harga Terendah), Close (Harga Penutupan), dan Volume (Jumlah Lembar Saham yang Ditransaksikan). Data ini merupakan bahan baku utama untuk menghitung rumus-rumus indikator teknikal seperti MACD, RSI, SMA, Bollinger Bands, dan KDJ.
* **Yahoo Finance API — Info, Income Statement, Balance Sheet**  
  Sumber ini menarik ringkasan kesehatan keuangan perusahaan, yaitu: rasio valuasi pasar (P/E Ratio, Price-to-Book, Dividend Yield), laporan laba rugi (pendapatan, beban, laba bersih), serta neraca keuangan (total aset, total liabilitas, ekuitas). Data ini bersifat kuartalan/tahunan dan relatif stabil dalam jangka menengah.

> **⟶ TRANSISI 1: Sumber Data Eksternal → Python Extraction & Pre-Processing**  
> Panah dari Lapisan 1 menuju Lapisan 3 menggambarkan proses penarikan data mentah dari internet ke dalam mesin pemrosesan Python. Ketiga sumber RSS (Google News dan CNBC) mengalir ke kotak `NewsFetcher`, sedangkan kedua sumber Yahoo Finance mengalir ke kotak `YFinanceFetcher`. Pemisahan ini menunjukkan bahwa data kualitatif (teks) dan data kuantitatif (angka) diproses oleh modul Python yang berbeda, masing-masing dengan logika pembersihan yang sesuai dengan karakteristik datanya.

---

## LAPISAN 3: PYTHON EXTRACTION & PRE-PROCESSING

Lapisan ini merupakan "dapur pembersihan data" tempat data mentah dari internet divalidasi, dibersihkan, dan diformat sebelum disimpan ke penyimpanan lokal. Terdapat 2 modul utama:

### Modul A: NewsFetcher (`tools/news_fetcher.py`)
Modul ini memiliki dua mekanisme pembersihan kritis:
1. **Negative Keyword Filter:** Menyaring dan membuang artikel berita yang bersifat edukasi pemula, promosi platform investasi, atau insiden kriminal lokal yang tidak memiliki nilai analisis finansial. Contoh kata kunci yang dibuang: *"cara beli"*, *"panduan pemula"*, *"pembobolan ATM"*. Dengan filter ini, hanya berita yang benar-benar memuat sinyal pergerakan pasar (kinerja laba, arus dana asing, kebijakan moneter) yang lolos masuk ke penyimpanan.
2. **Incremental Append & Deduplication:** Saat menarik berita baru, modul ini tidak menimpa (*overwrite*) arsip berita lama. Sebaliknya, modul membaca arsip yang sudah ada, mengecek apakah judul berita sudah pernah tercatat menggunakan struktur data `set()`, lalu hanya menambahkan (*append*) artikel-artikel baru yang belum ada sebelumnya. Mekanisme ini menjamin arsip berita tumbuh secara organik dari hari ke hari tanpa duplikasi.

### Modul B: YFinanceFetcher (`tools/data_fetcher.py`)
Modul ini memiliki dua mekanisme teknis:
1. **2-Year Buffer Calculation:** Saat pengguna meminta data mulai dari tanggal tertentu (misal `--start 2026-08-01`), modul ini secara otomatis menghitung mundur 2 tahun ke belakang (menjadi `2024-08-01`) sebagai titik awal pengambilan data. Buffer 2 tahun ini diperlukan agar indikator teknikal berperiode panjang (seperti SMA-200 yang membutuhkan 200 hari data historis) memiliki data yang cukup dan tidak menghasilkan nilai kosong (*NaN*) di awal simulasi.
2. **Lowercase Columns:** Seluruh nama kolom hasil unduhan Yahoo Finance dinormalisasi menjadi huruf kecil (`open`, `high`, `low`, `close`, `volume`) agar kompatibel dengan pustaka komputasi indikator teknikal `stockstats` yang mensyaratkan penamaan kolom lowercase.

> **⟶ TRANSISI 2: Python Extraction → Otomasi Scheduler (Garis Putus-Putus)**  
> Garis putus-putus (*dashed line*) yang menghubungkan Lapisan 3 ke Lapisan 2 menunjukkan bahwa `NewsFetcher` dipanggil secara otomatis oleh skrip penjadwal harian. Garis putus-putus (bukan garis solid) digunakan karena hubungan ini bersifat pemanggilan terjadwal (*scheduled invocation*), bukan aliran data langsung. Artinya, `NewsFetcher` tidak berjalan terus-menerus, melainkan hanya dipanggil oleh skrip kolektor pada waktu yang sudah ditentukan.

---

## LAPISAN 2: OTOMASI SCHEDULER & PIPELINE HARIAN

Lapisan ini menggambarkan rantai otomasi (*automation chain*) yang memastikan pengumpulan berita berjalan setiap hari tanpa campur tangan manual dari pengguna. Rantai ini terdiri dari 4 komponen yang terhubung secara berurutan:

1. **Windows Task Scheduler (`Daily 11:00 AM WIB / StartWhenAvailable`)**  
   Layanan bawaan sistem operasi Windows yang bertugas sebagai "jam weker digital". Layanan ini disetel untuk memicu eksekusi pada pukul 11:00 Pagi WIB setiap hari. Fitur *StartWhenAvailable* memastikan bahwa jika laptop dalam keadaan mati atau tidur pada jam 11:00, Windows akan langsung menjalankan tugas tersebut begitu laptop dinyalakan kembali di waktu kapanpun setelahnya.
2. **`run_collector.vbs` (`Silent Headless Background`)**  
   File VBScript yang menjadi jembatan eksekusi senyap. File ini dipanggil oleh Task Scheduler dan bertugas menjalankan skrip batch (`run_collector.bat`) dengan parameter jendela tersembunyi (`0`). Hasilnya, seluruh proses pengumpulan berita berjalan sepenuhnya di latar belakang (*background*) tanpa memunculkan jendela hitam CMD yang mengganggu layar pengguna.
3. **`daily_news_collector.py` (`Iterasi 5 Bank: BBRI, BBCA, BMRI, BBNI, BRIS`)**  
   Skrip Python utama yang mengorkestrasi penarikan berita untuk kelima emiten bank secara berurutan. Skrip ini memanggil modul `NewsFetcher` sebanyak 5 kali (satu kali per bank), dan setiap pemanggilan akan menarik berita dari 3 sumber RSS, memfilter kata kunci sampah, menggabungkan dengan arsip lama, lalu menyimpan hasilnya ke folder cache masing-masing bank. Seluruh proses untuk 5 bank memakan waktu rata-rata hanya sekitar 5–8 detik.
4. **`scripts/collector_log.txt` (`Audit Trail & Metric Counter`)**  
   File teks log yang mencatat jejak audit setiap kali skrip kolektor dijalankan. Setiap entri log berisi stempel waktu eksekusi, jumlah berita baru yang berhasil ditambahkan, total akumulasi berita bersih per bank, serta status keberhasilan/kegagalan. File ini berfungsi sebagai bukti dokumentasi operasional bahwa pipeline data berjalan secara konsisten dan dapat diverifikasi oleh dosen penguji.

> **⟶ TRANSISI 3: Scheduler & Pre-Processing → Local Storage / Cache**  
> Panah dari Lapisan 2 dan Lapisan 3 menuju Lapisan 4 menggambarkan proses penyimpanan hasil akhir data yang sudah bersih ke dalam penyimpanan lokal (*harddisk*). Data yang keluar dari `NewsFetcher` disimpan sebagai `master_news.json`, data harga dari `YFinanceFetcher` disimpan sebagai `master_ohlcv.csv`, dan data fundamental disimpan sebagai `master_fundamentals.json`. Ketiga file ini diisolasi ke dalam folder terpisah per emiten (`data/cache/BBRI.JK/`, `data/cache/BBCA.JK/`, dst.) agar tidak tercampur antar emiten.

---

## LAPISAN 4: LOCAL STORAGE / CACHE (`data/cache/{ticker}/`)

Lapisan ini merepresentasikan 3 file master data yang tersimpan di harddisk lokal komputer pengguna. Ketiga file ini menjadi satu-satunya sumber kebenaran (*single source of truth*) bagi seluruh proses simulasi backtesting:

* **`master_news.json` (*Cleaned Articles Archive*)**  
  Berisi arsip lengkap metadata berita yang telah melewati filter pembersihan. Setiap artikel hanya menyimpan 4 atribut: judul (*title*), tautan (*link*), tanggal publikasi (*published*), dan nama sumber (*source*). File ini tumbuh secara inkremental setiap hari sejalan dengan jadwal pengumpulan otomatis.
* **`master_ohlcv.csv` (*Time-Series Matrix*)**  
  Berisi matriks deret waktu harga saham harian dengan kolom: `date`, `open`, `high`, `low`, `close`, `volume`. Data ini mencakup rentang historis hingga 2 tahun ke belakang dari tanggal awal backtest untuk menjamin kecukupan kalkulasi indikator teknikal jangka panjang.
* **`master_fundamentals.json` (*Valuation & Statements*)**  
  Berisi snapshot rasio valuasi terkini (P/E, P/B, Dividend Yield) serta ringkasan laporan laba rugi dan neraca keuangan kuartalan/tahunan terakhir. Data ini bersifat relatif stabil dalam satu kuartal.

> **⟶ TRANSISI 4: Local Storage → Runtime Backtesting / Time-Slicing**  
> Panah dari Lapisan 4 menuju Lapisan 5 menggambarkan proses pemuatan (*loading*) ketiga file master dari harddisk ke dalam memori komputer (RAM). Saat pengguna menjalankan perintah backtest, mesin Backtester Engine membaca seluruh isi ketiga file master sekaligus ke dalam variabel Python di memori. Pemuatan ini hanya terjadi satu kali di awal eksekusi (*one-shot loading*), sehingga iterasi mingguan berikutnya tidak perlu membaca ulang dari harddisk dan menjadi sangat cepat.

---

## LAPISAN 5: RUNTIME BACKTESTING / TIME-SLICING

Lapisan ini merupakan jantung pencegahan kecurangan data (*Look-Ahead Bias Prevention*) dan menjadi komponen paling krusial secara akademis dalam arsitektur ini. Lapisan ini terdiri dari 3 komponen:

1. **Backtester Engine (`orchestration/backtester.py`) — Weekly Step (Friday Loop)**  
   Mesin simulasi utama yang menjalankan perulangan mingguan. Pada setiap iterasi, mesin ini mensimulasikan keputusan investasi di hari Jumat penutupan bursa. Mesin bergerak maju dari minggu pertama hingga minggu terakhir dalam rentang tanggal `--start` sampai `--end` yang ditentukan pengguna.
2. **Time-Slicing OHLCV ($t \le \text{Date}$) — Compute Technical Indicators**  
   Pada setiap hari Jumat simulasi, mesin memotong (*slice*) deret waktu harga saham sehingga hanya data historis hingga hari Jumat tersebut yang digunakan untuk menghitung indikator teknikal. Rumus pemotongan: seluruh baris data di mana tanggal baris ($t$) kurang dari atau sama dengan tanggal simulasi ($\text{Date}$). Data harga setelah hari Jumat tersebut (masa depan) secara otomatis dibuang dari memori perhitungan.
3. **Time-Slicing News ($\text{Date}-7 \le t_{\text{published}} \le \text{Date}$) — Zero Look-Ahead Bias**  
   Pada setiap hari Jumat simulasi, mesin memotong arsip berita sehingga hanya berita yang terbit dalam kurun 7 hari terakhir menjelang hari Jumat tersebut yang diberikan kepada agen AI. Berita yang terbit setelah hari Jumat (masa depan) dibuang sepenuhnya. Berita yang terbit lebih dari 7 hari sebelumnya (sudah basi) juga dibuang agar analisis sentimen tetap relevan dan terkini.

> **⟶ TRANSISI 5: Time-Slicing → Konsumsi Agen AI**  
> Panah dari Lapisan 5 menuju Lapisan 6 menggambarkan penyerahan data yang telah diiris secara temporal kepada 4 Agen Analis AI. Data yang sampai di tangan agen sudah dalam kondisi bersih, relevan secara waktu, dan bebas dari informasi masa depan. Setiap agen hanya menerima jenis data yang sesuai dengan spesialisasinya — tidak ada agen yang membaca data di luar kewenangannya.

---

## LAPISAN 6: KONSUMSI AGEN AI (FASE 5)

Lapisan terakhir pada diagram menggambarkan 4 Agen Analis Spesialis yang menjadi konsumen akhir (*end consumer*) dari seluruh pipeline data Fase 1. Keempat agen ini bekerja secara paralel dan masing-masing membaca jenis data yang berbeda:

* **Technical Analyst (Membaca RSI, MACD, SMA)**  
  Menerima hasil perhitungan indikator teknikal dari Time-Slicing OHLCV. Agen ini menganalisis momentum harga, tren rata-rata bergerak, dan kondisi jenuh beli/jual berdasarkan sinyal-sinyal matematika. Agen ini tidak pernah membaca berita; tugasnya murni berbasis angka numerik.
* **Sentiment Analyst (Membaca Berita Spesifik Ticker)**  
  Menerima kumpulan judul berita spesifik emiten yang telah disaring oleh Time-Slicing News. Agen ini mengekstrak sentimen pasar jangka pendek (apakah suasana terhadap saham tersebut positif, negatif, atau netral) berdasarkan headline berita yang terbit dalam 7 hari terakhir.
* **Macro Analyst (Membaca Berita Suku Bunga & OJK)**  
  Menerima kumpulan judul berita makroekonomi yang telah disaring oleh Time-Slicing News. Agen ini mengevaluasi dampak kebijakan suku bunga Bank Indonesia, regulasi OJK, dan kondisi ekonomi global terhadap prospek margin bunga bersih sektor perbankan.
* **Fundamental Analyst (Membaca P/E, P/B, ROE)**  
  Menerima data valuasi dan laporan keuangan dari `master_fundamentals.json` secara langsung (tanpa melewati Time-Slicing, karena data fundamental bersifat kuartalan dan tidak berubah setiap hari). Agen ini menilai apakah harga saham saat ini wajar (*fairly valued*), murah (*undervalued*), atau mahal (*overvalued*) berdasarkan metrik kesehatan keuangan perusahaan.