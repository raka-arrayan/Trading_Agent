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