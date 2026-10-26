# DOKUMEN PROPOSAL SKRIPSI
## SISTEM PERDAGANGAN SAHAM MULTI-AGEN BERBASIS LARGE LANGUAGE MODEL MENGGUNAKAN ORKESTRASI LANGGRAPH DAG DAN MEKANISME DEBAT ADVERSARIAL PADA SEKTOR PERBANKAN IHSG

*Disusun mengacu pada Pedoman dan Format Penulisan Tugas Akhir Fakultas Teknik, Program Studi S1 Teknik Komputer, Universitas Indonesia.*

---

# BAB 1
# PENDAHULUAN

## 1.1 Latar Belakang
Pasar modal memegang fungsi krusial sebagai barometer aktivitas ekonomi nasional sekaligus wahana intermediasi modal bagi ekspansi korporasi. Di Bursa Efek Indonesia (BEI), arah pergerakan Indeks Harga Saham Gabungan (IHSG) memiliki ketergantungan yang sangat kuat terhadap sektor keuangan, terutama subsektor perbankan. Saham perbankan dengan kapitalisasi pasar besar (*big-cap banks*), seperti PT Bank Rakyat Indonesia (Persero) Tbk (BBRI), PT Bank Central Asia Tbk (BBCA), PT Bank Mandiri (Persero) Tbk (BMRI), PT Bank Negara Indonesia (Persero) Tbk (BBNI), dan PT Bank Syariah Indonesia Tbk (BRIS), secara agregat menyumbang lebih dari 30% total kapitalisasi pasar bursa dan secara berkala mendominasi perputaran likuiditas harian [9], [10]. Karakteristik pergerakan harga saham emiten perbankan dipengaruhi oleh persilangan berbagai modalitas informasi: fluktuasi harga transaksi historis (kuantitatif), kinerja neraca dan rasio rentabilitas berkala (fundamental), hingga rilis regulasi moneter Bank Indonesia (BI-Rate) dan kebijakan perbankan Otoritas Jasa Keuangan (OJK) yang terdistribusi dalam bentuk narasi berita harian (kualitatif).

Dalam praktik investasi profesional, perumusan strategi perdagangan saham menuntut sintesis simultan antara analisis teknikal, fundamental, dan sentimen pasar. Namun, pemrosesan manual oleh investor perseorangan maupun tim analis konvensional kerap terbentur pada keterbatasan daya tampung kognitif manusia (*cognitive overload*). Menelaah puluhan warta pasar modal setiap hari sembari mengkalkulasi matriks indikator teknikal deret waktu sering kali menimbulkan kelelahan analisis (*decision fatigue*), bias konfirmasi (*confirmation bias*), serta dorongan psikologis emosional seperti ketakutan tertinggal momentum (*fear of missing out*) dan kepanikan likuidasi aset (*panic selling*).

Kemunculan teknologi *Large Language Models* (LLM) membuka peluang revolusioner dalam memproses teks tak terstruktur dan penalaran informasi berdensitas tinggi [3]. Berbeda dengan model pembelajaran mesin konvensional yang kaku, arsitektur berbasis *Transformer* mampu mengekstrak konteks makna semantik dari narasi finansial dan menghubungkannya dengan metrik kinerja korporasi. Kendati demikian, penerapan model tunggal (*single-agent LLM*) secara mandiri dalam lingkungan perdagangan pasar modal memiliki kelemahan struktural yang signifikan, yaitu kerentanan menghasilkan halusinasi faktual (*hallucination*) dan estimasi keyakinan yang berlebihan (*overconfidence*) [6]. Ketika sebuah model LLM tunggal dibebani instruksi untuk membaca seluruh data pasar sekaligus lalu langsung memutuskan transaksi, model tersebut rentan kehilangan fokus konteks (*context drift*), gagal mengenali kontradiksi antar-indikator, serta memberikan rekomendasi yang sulit diaudit penalarannya.

Guna mengatasi keterbatasan tersebut, pendekatan rekayasa perangkat lunak kecerdasan artifisial beralih ke paradigma *Multi-Agent Systems* (MAS). Pendekatan ini mengadopsi prinsip dekomposisi peran (*separation of concerns*) yang lazim diterapkan pada divisi riset dan manajemen investasi profesional [1], [5]. Beban analisis dibagi ke dalam beberapa entitas agen otonom dengan tugas spesifik, seperti agen analis fundamental, analis teknikal, analis sentimen, dan analis makroekonomi [4]. 

Selain pembagian peran, interaksi antar-agen menjadi faktor penentu kualitas keputusan. Teori *AI Safety via Debate* yang dipelopori oleh Irving et al. dari Google DeepMind membuktikan secara matematis bahwa dua agen cerdas yang diposisikan dalam perdebatan *adversarial* (saling menyanggah dari sudut pandang yang berlawanan) akan terdorong secara rasional untuk mengekspos kelemahan logika dan bias dari pihak lawan [2]. Proses perdebatan ini menyaring distorsi informasi sehingga pengambil keputusan netral dapat mengevaluasi substansi yang teruji. Penemuan empiris terbaru oleh Cai et al. melalui kerangka kerja *FinDebate* mengonfirmasi bahwa penyematan kubu *Bullish* dan *Bearish* secara efektif menekan bias *overconfidence* pada analisis portofolio saham [6]. Sementara itu, Xiao et al. dalam kerangka kerja *TradingAgents* menunjukkan bahwa hierarki tim yang terstruktur antara analis, periset, dan manajer risiko mampu menghasilkan ketahanan portofolio yang superior dibandingkan model tunggal [1].

Meskipun keunggulan MAS telah diuji pada bursa saham global, penerapannya pada pasar saham Indonesia (IHSG) menghadapi dua tantangan utama yang belum diselesaikan dalam riset-riset terdahulu:
1. **Pencegahan Look-Ahead Bias:** Banyak sistem simulasi kuantitatif secara tidak sengaja membaca data harga atau teks berita yang terbit melampaui tanggal simulasi transaksi, menghasilkan performa semu (*data leakage*) yang runtuh saat diuji di pasar nyata [1].
2. **Karakteristik Unik Pasar Indonesia:** Struktur regulasi Bursa Efek Indonesia yang menerapkan fraksi satuan 1 lot = 100 lembar, batas *auto rejection*, dominasi perbankan KBMI 3 dan KBMI 4, serta asupan berita dwibahasa (Indonesia-Inggris) menuntut arsitektur pipa data (*data pipeline*) dan orkestrasi agen yang disesuaikan secara khusus [9], [10].

Berdasarkan kesenjangan tersebut, penelitian ini merancang dan mengembangkan sistem perdagangan saham *Multi-Agent LLM* (Agent_Saham) yang diorkestrasi menggunakan topologi *Directed Acyclic Graph* (DAG) berbasis LangGraph. Sistem ini memadukan *pipeline data ingestion* otomatis dengan mekanisme pemotongan temporal (*runtime time-slicing*) anti-bias, menerapkan debat adversarial *Bullish vs Bearish*, menjalankan simulasi manajemen risiko ganda (*Aggressive vs Conservative*), serta memvalidasi transparansi penalaran investasi (*Explainable AI*) pada 5 saham perbankan terkemuka di Bursa Efek Indonesia.

---

## 1.2 Rumusan Masalah
Berdasarkan latar belakang yang dipaparkan, permasalahan yang diselesaikan dalam penelitian ini dirumuskan sebagai berikut:
1. Bagaimana merancang dan mengimplementasikan arsitektur *pipeline data ingestion* otomatis multi-sumber (deret waktu harga OHLCV, data fundamental kuartalan, dan teks berita harian) yang secara deterministik mengeliminasi kebocoran informasi masa depan (*Look-Ahead Bias*) pada simulasi perdagangan saham perbankan IHSG?
2. Bagaimana membangun topologi orkestrasi 12 agen LLM berbasis *Directed Acyclic Graph* (DAG) menggunakan kerangka kerja LangGraph yang memfasilitasi aliran data searah tanpa siklus serta membagi peran kerja ke dalam empat tim hierarkis (Analis, Peneliti Debat, Manajemen Risiko, dan Eksekusi)?
3. Bagaimana mekanisme perdebatan adversarial antara agen *Bullish Researcher* dan *Bearish Researcher*, yang disintesis bersama agen manajemen risiko, memitigasi halusinasi model serta menghasilkan keputusan transaksi (*BUY/SELL/HOLD*) yang terukur dan dapat diaudit penalarannya (*Explainable AI*)?

---

## 1.3 Tujuan Penelitian
Tujuan dari penelitian tugas akhir ini meliputi:
1. Membangun sistem *data ingestion* otomatis berbasis Python dan penjadwal sistem operasi yang menerapkan algoritma pemotongan temporal (*runtime time-slicing*) pada data harga ($t \le \text{Date}$) dan jendela berita ($\text{Date}-7 \le t_{\text{published}} \le \text{Date}$).
2. Mengembangkan orkestrasi sistem 12 agen LLM menggunakan LangGraph dengan arsitektur DAG yang memanfaatkan media memori estafet bertipe `TypedDict` (*TradingState*) dan fungsi agregasi *Reducer* untuk mencegah konflik data konkuren.
3. Menguji efektivitas mekanisme debat adversarial (*Bullish vs Bearish*) dan evaluasi toleransi risiko (*Aggressive vs Conservative*) dalam memvalidasi sinyal pasar serta menghasilkan rekomendasi perdagangan terstruktur dalam format JSON beserta berkas audit penalaran (*Reasoning Log*).

---

## 1.4 Manfaat Penelitian
Penelitian ini diharapkan memberikan kontribusi nyata dari sisi teoretis maupun praktis:
1. **Manfaat Teoretis:** Memperkaya khazanah keilmuan teknik komputer dan informatika, khususnya integrasi *Multi-Agent Systems*, kerangka kerja LangGraph DAG, dan teori *AI Safety via Debate* pada instrumen pasar modal negara berkembang (*emerging market*) yang memiliki volatilitas dan regulasi khas.
2. **Manfaat Praktis:** Menyediakan landasan rekayasa perangkat lunak bagi pelaku pasar modal, analis keuangan, dan investor ritel dalam memanfaatkan agen LLM sebagai asisten keputusan investasi yang transparan, objektif, dan dapat dipertanggungjawabkan proses penalarannya.

---

## 1.5 Ruang Lingkup Penelitian
Guna menjaga fokus dan kedalaman pembahasan, batasan masalah dalam penelitian ini ditetapkan sebagai berikut:
1. **Semesta Saham (*Universe*):** Analisis dibatasi pada lima emiten perbankan dengan kapitalisasi pasar dan likuiditas tertinggi di Bursa Efek Indonesia: BBRI.JK, BBCA.JK, BMRI.JK, BBNI.JK (kategori KBMI 4), dan BRIS.JK (kategori KBMI 3) [10].
2. **Sumber Perolehan Data:** Data kuantitatif harga historis (OHLCV) dan laporan fundamental ditarik melalui antarmuka pemrograman aplikasi Yahoo Finance. Data kualitatif teks berita dihimpun dari tiga aliran sindikasi RSS: Google News query spesifik emiten, Google News query makroekonomi BI/OJK, dan CNBC Indonesia Market Feed.
3. **Penyedia Komputasi LLM:** Inferensi kecerdasan artifisial menggunakan model Google Gemini (`gemini-flash-lite-latest`) yang dihubungkan melalui pustaka orkestrasi LangChain.
4. **Siklus Keputusan Investasi:** Simulasi perdagangan dijalankan dengan interval mingguan (*weekly step*), mengambil patokan harga penutupan bursa setiap hari Jumat.
5. **Ketentuan Transaksi Finansial:** Perhitungan simulasi menerapkan aturan formal BEI berupa satuan perdagangan fraksi 1 lot = 100 lembar dan memasukkan komponen biaya komisi broker serta pajak transaksi sebesar 0,2% pada setiap aksi beli maupun jual [9].
6. **Batas Muatan Laporan:** Naskah proposal ini menitikberatkan pada metodologi, perancangan arsitektur sistem, dan desain skenario pengujian (Bab 1 hingga Bab 3). Hasil empiris komputasi portofolio disajikan pada Bab 4.

---

## 1.6 Sistematika Penulisan
Laporan skripsi ini disusun dengan sistematika pembahasan sebagai berikut:
* **BAB 1 PENDAHULUAN:** Menguraikan latar belakang permasalahan, rumusan masalah, tujuan penelitian, manfaat penelitian, ruang lingkup batasan masalah, dan sistematika penulisan laporan.
* **BAB 2 TINJAUAN PUSTAKA:** Menyajikan landasan teori yang mencakup karakteristik pasar modal Indonesia, prinsip analisis finansial (teknikal, fundamental, dan teks berita), arsitektur Transformer dan LLM, teori sistem multi-agen (*MetaGPT* dan *FinCon*), teori *AI Safety via Debate*, prinsip pencegahan *look-ahead bias*, serta matriks komparasi penelitian terkait (*State of the Art*).
* **BAB 3 METODOLOGI DAN PERANCANGAN SISTEM:** Menguraikan metodologi rekayasa sistem, justifikasi perangkat lunak, perancangan arsitektur global 7 fase, arsitektur pipeline *data ingestion* dan mitigasi bias, rancangan topologi orkestrasi 12 agen LangGraph DAG, serta perancangan skenario pengujian *backtesting* dan studi ablasi (*ablation study*).
* **BAB 4 PENGUJIAN DAN EVALUASI:** Membahas implementasi teknis sistem, eksekusi simulasi *backtesting* pada kelima saham perbankan, evaluasi performa finansial (*Cumulative Return, Sharpe Ratio, Maximum Drawdown, Win Rate*), komparasi strategi *baseline*, hasil studi ablasi peran debat, dan evaluasi keterjelasan jejak penalaran (*Explainable AI*).
* **BAB 5 PENUTUP:** Menyimpulkan temuan penelitian yang menjawab rumusan masalah serta menyajikan rekomendasi saran teknis untuk pengembangan sistem pada masa mendatang.
* **DAFTAR REFERENSI:** Memuat daftar rujukan ilmiah yang disitir dalam naskah dengan standar penulisan IEEE.

---

# BAB 2
# TINJAUAN PUSTAKA

## 2.1 Karakteristik Pasar Modal Indonesia & Sektor Perbankan
Pasar modal Indonesia diselenggarakan dan diawasi oleh PT Bursa Efek Indonesia (BEI) bersama Otoritas Jasa Keuangan (OJK). Aturan operasional perdagangan saham diatur melalui **Keputusan Direksi PT Bursa Efek Indonesia Nomor Kep-00061/BEI/07-2021 perihal Peraturan Nomor II-A tentang Perdagangan Efek Bersifat Ekuitas** [9]. Peraturan tersebut menetapkan bahwa transaksi efek pada pasar reguler dan pasar tunai wajib dieksekusi dalam satuan perdagangan standar (round lot), di mana **1 Lot setara dengan 100 lembar saham** [9]. Selain itu, BEI menerapkan ketentuan rentang fraksi harga (*tick size*) dan mekanisme penolakan penawaran otomatis (*Auto Rejection*)—baik batas atas (ARA) maupun batas bawah (ARB)—untuk meredam volatilitas liar yang tidak didukung oleh pembentukan harga yang wajar.

Di dalam ekosistem bursa, industri perbankan memegang peranan sentral. Melalui **Peraturan Otoritas Jasa Keuangan (POJK) Nomor 12/POJK.03/2021 tentang Bank Umum**, perbankan nasional diklasifikasikan ke dalam empat tingkatan Kelompok Bank berdasarkan Modal Inti (KBMI) [10]:
1. **KBMI 1:** Modal inti sampai dengan Rp 6 triliun.
2. **KBMI 2:** Modal inti lebih dari Rp 6 triliun hingga Rp 14 triliun.
3. **KBMI 3:** Modal inti lebih dari Rp 14 triliun hingga Rp 70 triliun.
4. **KBMI 4:** Modal inti di atas Rp 70 triliun.

Empat bank terbesar nasional yang diteliti dalam skripsi ini (BBRI, BBCA, BMRI, dan BBNI) merupakan emiten berkategori KBMI 4 dengan modal inti di atas Rp 70 triliun [10]. Keempat entitas ini menguasai lebih dari separuh peredaran aset dan penyaluran kredit perbankan nasional. Adapun BRIS menempati posisi perbankan syariah terbesar di Indonesia yang masuk ke dalam kategori KBMI 3 [10]. Karakteristik likuiditas yang sangat tinggi, rasio *free-float* saham publik yang besar, serta kewajiban keterbukaan pelaporan audit yang ketat menjadikan kelima bank tersebut sebagai semesta aset (*universe*) yang sangat representatif untuk pemodelan kuantitatif.

---

## 2.2 Landasan Analisis Finansial: Teknikal, Fundamental, dan Sentimen Berita
Pengambilan keputusan perdagangan kuantitatif yang kokoh memerlukan sintesis dari tiga modalitas analisis pasar:

### 2.2.1 Analisis Teknikal
Analisis teknikal mengevaluasi instrumen finansial berdasarkan data transaksi pasar masa lalu, terutama pergerakan harga dan volume [7]. Berdasarkan rujukan standar John J. Murphy (1999) [7], deret waktu harga transaksi harian direpresentasikan dalam lima kolom utama: *Open* (pembukaan), *High* (tertinggi), *Low* (terendah), *Close* (penutupan), dan *Volume* (kuantitas lembar ditransaksikan), atau disingkat OHLCV. Indikator matematis yang digunakan dalam sistem ini meliputi:
1. **Simple Moving Average (SMA):** Nilai rata-rata hitung harga penutupan selama periode jendela waktu $N$:
   $$\text{SMA}_t = \frac{1}{N} \sum_{i=0}^{N-1} \text{Close}_{t-i}$$
   Sistem memanfaatkan persilangan (*crossover*) antara SMA periode pendek (SMA-20) dan periode menengah (SMA-50) untuk mendeteksi arah tren pergerakan modal.
2. **Relative Strength Index (RSI):** Indikator osilator yang mengukur kekuatan relatif momentum kenaikan terhadap penurunan harga dalam rentang indeks 0 hingga 100:
   $$\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right), \quad \text{RS} = \frac{\text{Rata-rata Keuntungan } N \text{ Periode}}{\text{Rata-rata Kerugian } N \text{ Periode}}$$
   Ambang batas di atas 70 menunjukkan kondisi jenuh beli (*overbought*), sedangkan di bawah 30 mengindikasikan jenuh jual (*oversold*) [7].
3. **Moving Average Convergence Divergence (MACD):** Indikator yang mengukur momentum tren melalui selisih dua rata-rata bergerak eksponensial (*Exponential Moving Average* / EMA):
   $$\text{MACD Line} = \text{EMA}_{12}(\text{Close}) - \text{EMA}_{26}(\text{Close})$$
   $$\text{Signal Line} = \text{EMA}_{9}(\text{MACD Line})$$
   $$\text{Histogram} = \text{MACD Line} - \text{Signal Line}$$
4. **Bollinger Bands:** Indikator volatilitas dinamis yang memetakan pita harga di sekitar SMA-20 dengan lebar pita sebesar dua kali simpangan baku ($\sigma$) [7]:
   $$\text{Upper Band} = \text{SMA}_{20} + 2\sigma, \quad \text{Lower Band} = \text{SMA}_{20} - 2\sigma$$

### 2.2.2 Analisis Fundamental
Analisis fundamental berfokus pada penilaian kesehatan neraca, profitabilitas operasional, serta kelayakan valuasi harga saham relatif terhadap nilai intrinsik perusahaan [8]. Mengacu pada prinsip valuasi korporasi oleh Aswath Damodaran (2012) [8], indikator fundamental utama emiten perbankan mencakup:
* **Price-to-Earnings Ratio (PER):** Rasio perbandingan harga saham terhadap laba bersih per saham (*Earnings Per Share* / EPS), menggambarkan valuasi pasar atas profitabilitas emiten.
* **Price-to-Book Value (PBV):** Rasio perbandingan harga pasar terhadap nilai buku ekuitas (*Book Value per Share*). Dalam konteks institusi perbankan di mana aset didominasi oleh instrumen moneter likuid, PBV menjadi tolok ukur utama kewajaran harga saham.
* **Return on Equity (ROE):** Rasio imbal hasil ekuitas yang mengukur efisiensi manajemen dalam mengoptimalkan modal bersih pemegang saham untuk menghasilkan laba bersih.

### 2.2.3 Analisis Sentimen dan Teks Berita Finansial
Sentimen pasar merefleksikan ekspektasi psikologis kolektif para pelaku pasar terhadap prospek ekonomi. Riset empiris oleh Loughran dan McDonald (2011) di *The Journal of Finance* membuktikan bahwa analisis linguistik pada dokumen dan publikasi keuangan memiliki korelasi signifikan terhadap fluktuasi harga saham dan volume perdagangan [11]. Loughran dan McDonald menegaskan bahwa leksikon bahasa umum tidak dapat diterapkan secara langsung pada analisis finansial, karena kosakata tertentu seperti *liability* atau *cost* membawa makna akuntansi rutin, bukan selalu merefleksikan sentimen negatif [11]. Keunggulan arsitektur LLM terletak pada kemampuannya memahami arti kontekstual kata di dalam kalimat berita pasar secara dinamis, sehingga ekstraksi sentimen menjadi jauh lebih presisi dibandingkan metode pencocokan kata kunci konvensional.

---

## 2.3 Arsitektur Large Language Model (LLM) & Mekanisme Perhatian
Fondasi teknologi model bahasa modern berakar pada arsitektur *Transformer* yang dirumuskan oleh Vaswani et al. (2017) melalui publikasi *"Attention Is All You Need"* [3]. Inovasi kunci arsitektur ini adalah penghapusan struktur rekursif (*Recurrent Neural Network*) yang lambat dan menggantikannya dengan mekanisme perhatian mandiri (*Self-Attention Mechanism*), memungkinkan komputasi representasi token secara simultan di sepanjang konteks [3].

Secara komputasional, teks masukan dipecah menjadi unit token diskret yang kemudian dipetakan ke dalam ruang vektor berdimensi tinggi (*token embeddings*). Inti matematis dari mekanisme atensi ditunjukkan pada Persamaan (2.1) [3]:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V \tag{2.1}$$

Dalam persamaan tersebut, matriks $Q$ (*Query*) memuat informasi yang dicari oleh sebuah token, $K$ (*Key*) memuat label identitas seluruh token dalam konteks, dan $V$ (*Value*) merepresentasikan bobot semantik informasi. Pembagian dengan faktor skalar $\sqrt{d_k}$ (akar dari dimensi ruang kunci) berfungsi mencegah perkalian titik (*dot product*) menghasilkan nilai ekstrem yang dapat melenyapkan gradien saat fungsi *softmax* diterapkan [3].

Mekanisme ini diimplementasikan secara paralel melalui *Multi-Head Attention*, di mana model secara bersamaan menaruh atensi pada hubungan gramatikal, entitas angka finansial, dan keterkaitan sentimen kebijakan makroekonomi pada sub-ruang representasi yang berbeda. Stabilitas komputasi dijaga melalui normalisasi residual (*Layer Normalization*) [3].

Dalam proses inferensi agen, kontrol probabilistik token diatur melalui parameter *Temperature*. Nilai *temperature* rendah ($T = 0.0$) mengunci distribusi token pada probabilitas teratas (*greedy sampling*), menjamin jawaban yang deterministik, konsisten, dan faktual bagi agen pelapor data. Sebaliknya, nilai *temperature* moderat ($T = 0.7$) memperluas keragaman penalaran bagi agen pendebat agar mampu mengeksplorasi sudut pandang alternatif [1].

---

## 2.4 Sistem Multi-Agen (MAS) & Prinsip Pemisahan Tugas
Upaya membangun sistem analitik kompleks dengan menugaskan seluruh analisis kepada satu model LLM tunggal terbukti memicu degradasi kinerja penalaran (*prompt congestion*) [5]. Untuk mengatasi hambatan tersebut, Hong et al. (2023) dalam perancangan *MetaGPT* memperkenalkan prinsip rekayasa perangkat lunak *Separation of Concerns* ke dalam sistem kecerdasan multi-agen [5]. Setiap agen LLM diberikan tugas tunggal yang spesifik, dilengkapi dengan batasan persona, instruksi terfokus, serta format dokumen luaran standar (*Standard Operating Procedures* / SOP) [5].

Selaras dengan temuan tersebut, penelitian *FinCon* oleh Yu et al. (2024) membuktikan bahwa koordinasi finansial yang efektif tercipta melalui komunikasi hierarkis terstruktur [4]. Alih-alih mentransfer seluruh data mentah dari modul satu ke modul lain, sistem yang terdesentralisasi merangkum data menjadi pesan eksekutif berbobot tinggi. Pendekatan ini meniru organisasi divisi investasi dunia nyata, di mana staf analis menyerahkan ringkasan temuan kepada pengambil keputusan manajerial tanpa membebani jendela memori konteks [4].

---

## 2.5 Teori AI Safety via Debate & Mitigasi Overconfidence
Secara alamiah, model bahasa generatif dilatih untuk menyusun kalimat yang terdengar masuk akal berdasarkan statistik kemunculan kata, sehingga rentan memproduksi argumen keliru dengan gaya bahasa yang sangat meyakinkan (*hallucinatory overconfidence*). Pada pasar finansial yang volatil, kesalahan estimasi semacam ini dapat memicu kepanikan transaksi atau alokasi modal yang berisiko tinggi [6].

Sebagai fondasi ilmiah mitigasi halusinasi, Irving et al. (2018) merumuskan kerangka kerja *AI Safety via Debate* [2]. Pembuktian teoretis DeepMind tersebut menunjukkan bahwa ketika dua model kecerdasan artifisial diposisikan dalam kompetisi *zero-sum* (satu pihak bertindak sebagai pembela premis, pihak lain sebagai penyanggah), strategi optimal bagi kedua agen adalah membeberkan bukti faktual yang paling sulit dibantah dan mengekspos celah kebohongan pihak lawan [2]. Melalui proses dialektika ini, pengambil keputusan pihak ketiga yang netral dapat membedakan kebenaran secara jauh lebih mudah dan objektif dibandingkan hanya mengevaluasi satu agen tanpa pembanding [2].

Eksperimen empiris pada domain pasar modal dibuktikan oleh Cai et al. (2025) dalam publikasi *FinDebate* [6]. Penelitian tersebut menegaskan bahwa menghadapkan agen analis berkarakter *Bullish* dengan analis berkarakter *Bearish* secara konsisten menurunkan bias keyakinan berlebihan (*overconfidence*), memperketat kriteria persetujuan transaksi, serta meningkatkan imbal hasil portofolio pada masa gejolak pasar [6].

---

## 2.6 Prinsip Pencegahan Look-Ahead Bias pada Perdagangan Kuantitatif
Dalam rekayasa algoritma perdagangan saham, *Look-Ahead Bias* didefinisikan sebagai kekeliruan fatal di mana sistem komputasi memanfaatkan informasi masa depan yang belum tersedia pada titik waktu simulasi masa lalu [1]. Misalnya, menghitung sinyal beli hari Jumat menggunakan harga penutupan hari Senin berikutnya, atau menganalisis sentimen portofolio menggunakan artikel berita yang baru terbit beberapa hari pasca-transaksi.

Secara formal, apabila sebuah langkah simulasi perdagangan berlangsung pada stempel waktu $T_{\text{sim}}$, himpunan data yang sah untuk diakses oleh agen, $\mathcal{I}_{\text{valid}}$, harus memenuhi batasan relasi temporal berikut:
$$\mathcal{I}_{\text{valid}} = \{ x \in \mathcal{D} \mid t(x) \le T_{\text{sim}} \}$$

di mana $t(x)$ merepresentasikan waktu resmi pencatatan atau rilis publikasi data $x$. Tanpa mekanisme pemotongan data (*time-slicing*) yang ketat, hasil simulasi historis akan tampak sangat menguntungkan (*overfitted*), namun mengalami kerugian telak saat diuji pada perdagangan nyata [1]. Oleh sebab itu, mekanisme pemotongan data deterministik berbasis kode merupakan syarat integritas mutlak dalam penelitian kuantitatif.

---

## 2.7 Penelitian Terkait (*State of the Art*) & Posisi Penelitian
Eksplorasi kecerdasan multi-agen pada pasar modal berkembang pesat dalam beberapa tahun terakhir. Xiao et al. (2024) mempublikasikan *TradingAgents*, sebuah kerangka kerja multi-agen LLM yang membagi sistem menjadi tim analis teknikal/fundamental, peneliti pasar, manajer risiko, dan eksekutor untuk pasar saham Amerika Serikat [1]. Kendati demikian, kerangka kerja tersebut belum menyediakan mekanisme pengumpulan teks berita otomatis secara kontinu dan belum menguji efektivitas sistem pada pasar modal negara berkembang seperti Indonesia.

Tabel 2.1 merangkum perbandingan pustaka rujukan utama, sementara Tabel 2.2 menyajikan matriks posisi pembeda dari penelitian yang diajukan dalam skripsi ini.

**Tabel 2.1. State of the art dan posisi penelitian ini**
| Peneliti & Tahun | Platform / Model | Komponen / Arsitektur | Fokus Evaluasi |
|:---|:---|:---|:---|
| **Xiao et al. (2024) [1]** | LLM Multi-Agent (*TradingAgents*) | Tim Analis, Riset, Manajer Risiko, Trader | Evaluasi performa trading pada US market dan studi ablasi (*ablation study*) arsitektur 8-agen. |
| **Irving et al. (2018) [2]** | Teori AI Safety (*Debate Framework*) | Dua agen pendebat adversarial dan satu agen juri/evaluator | Pembuktian teoretis bahwa interaksi debat AI membatasi halusinasi dan memaksa kejujuran model. |
| **Vaswani et al. (2017) [3]** | Arsitektur Transformer | *Multi-Head Attention*, *LayerNorm*, *Feed Forward* | Fondasi komputasi representasi bahasa dan mekanisme atensi skalar pada model pembelajaran mendalam. |
| **Yu et al. (2024) [4]** | LLM Multi-Agent (*FinCon*) | Hirarki agen analis dan *verbal reinforcement manager* | Efisiensi komunikasi berjenjang dan peringkasan konteks untuk keputusan investasi. |
| **Hong et al. (2023) [5]** | Multi-Agent Framework (*MetaGPT*) | SOP berbasis peran, *Separation of Concerns* | Pengurangan distorsi konteks pada rekayasa perangkat lunak multi-agen kolaboratif. |
| **Cai et al. (2025) [6]** | Multi-Agent System (*FinDebate*) | Mekanisme debat adversarial *Bullish vs Bearish* | Mitigasi bias *overconfidence* pada analisis keuangan dan portofolio saham global. |
| **Penelitian Ini** | LangGraph DAG Multi-Agent (12 Node) | Pipeline Anti-Bias, 4 Tim Agen, Debat Adversarial, Konsensus Risiko | Pipa data otomatis bebas *look-ahead bias*, orkestrasi 12 agen via DAG, evaluasi saham perbankan IHSG. |

<br>

**Tabel 2.2. Matriks perbandingan state of the art penelitian**
| Penelitian | Multi-Agent Architecture | Mekanisme Debat Adversarial | Evaluasi Risiko Dua Arah | Pasar Modal Indonesia (IHSG) | Mitigasi Look-Ahead Bias Harian |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Xiao et al. (2024) [1]** | $\checkmark$ | $\times$ | $\checkmark$ | $\times$ | $\times$ |
| **Irving et al. (2018) [2]** | $\times$ | $\checkmark$ | $\times$ | $\times$ | $\times$ |
| **Yu et al. (2024) [4]** | $\checkmark$ | $\times$ | $\times$ | $\times$ | $\times$ |
| **Hong et al. (2023) [5]** | $\checkmark$ | $\times$ | $\times$ | $\times$ | $\times$ |
| **Cai et al. (2025) [6]** | $\checkmark$ | $\checkmark$ | $\times$ | $\times$ | $\times$ |
| **Penelitian Ini** | $\checkmark$ | $\checkmark$ | $\checkmark$ | $\checkmark$ | $\checkmark$ |

Matriks pada Tabel 2.2 menegaskan posisi dan kebaruan (*novelty*) penelitian ini: mengintegrasikan topologi DAG 12 agen LangGraph, menggabungkan mekanisme debat adversarial simultan dengan evaluasi risiko ganda, serta mengoperasikan *pipeline data ingestion* bebas *look-ahead bias* yang dikalibrasi secara spesifik untuk pasar saham perbankan di Indonesia.

---

# BAB 3
# METODOLOGI DAN PERANCANGAN SISTEM

## 3.1 Tujuan dan Ruang Lingkup Perancangan Sistem
### 3.1.1 Tujuan Perancangan Sistem
Perancangan sistem bertujuan merekayasa sebuah platform perdagangan saham otonom berbasis kecerdasan artifisial multi-agen yang memiliki integritas data temporal, keandalan analitik matematis, serta transparansi proses penalaran (*Explainable AI*). Sistem dirancang untuk mampu menghimpun data multi-modal secara otomatis, membersihkan informasi dari bias masa depan, mengorkestrasi 12 agen LLM dalam struktur alir terarah, dan menghasilkan keputusan transaksi portofolio yang dapat dipertanggungjawabkan secara saintifik.

### 3.1.2 Ruang Lingkup Perancangan Sistem
Ruang lingkup perancangan sistem mencakup rekayasa pada lima modul utama:
1. Modul pengunduh dan pembersih data terotomasi (Yahoo Finance API dan RSS feeds).
2. Penjadwal tugas sistem operasi Windows yang bekerja di latar belakang (*headless background*).
3. Struktur memori cache lokal dan modul komputasi indikator teknikal deterministik.
4. Graf eksekusi 12 agen berbasis LangGraph DAG yang terbagi ke dalam empat tim fungsional.
5. Antarmuka web interaktif berbasis Streamlit untuk visualisasi jalannya perdebatan AI dan kurva performa finansial.

---

## 3.2 Justifikasi Pemilihan Perangkat Lunak dan Alat Bantu Pengujian
Pemilihan perangkat lunak dan pustaka penunjang dalam penelitian ini didasarkan pada pertimbangan teknis berikut:
1. **Python 3.12:** Dipilih sebagai fondasi pemrograman utama karena efisiensi alokasi memori, stabilitas sintaks, dan dukungan komprehensif pustaka analitik kuantitatif (`pandas`, `numpy`, `yfinance`, `feedparser`).
2. **LangGraph (Ekosistem LangChain):** Dipilih sebagai kerangka kerja orkestrasi multi-agen karena menyediakan abstraksi *StateGraph* yang memungkinkan pembentukan topologi *Directed Acyclic Graph* (DAG) murni secara deterministik. LangGraph mendukung eksekusi cabang paralel (*fan-out/fan-in*) dan dilengkapi mekanisme *state checkpointing* untuk melacak transisi state agen secara andal.
3. **Google Gemini LLM (`gemini-flash-lite-latest`):** Dipilih sebagai mesin inferensi bahasa utama karena menawarkan latensi inferensi yang sangat rendah (<2 detik per node agen), kapasitas jendela konteks yang luas, serta efisiensi biaya operasional yang sangat ekonomis untuk eksekusi berulang.
4. **Penyimpanan Berkas Terstruktur Lokal (JSON dan CSV):** Sistem memilih arsitektur *local file caching* berbasis `master_news.json`, `master_ohlcv.csv`, dan `master_fundamentals.json` dibandingkan basis data relasional server (RDBMS) seperti PostgreSQL. Pendekatan ini menghilangkan ketergantungan konfigurasi jaringan (*zero-configuration*), menjamin portabilitas kode yang mudah dipindahkan ke lingkungan pengujian lain, serta menghasilkan latensi pembacaan data instan (*in-memory loading*) saat proses *backtesting*.
5. **Streamlit:** Pustaka visualisasi web berbasis Python murni yang efisien untuk menyajikan visualisasi jalannya perdebatan agen secara *streaming* dan menampilkan grafik performa portofolio interaktif.

---

## 3.3 Perancangan Arsitektur Sistem
### 3.3.1 Gambaran Umum Arsitektur Sistem
Arsitektur global sistem perdagangan multi-agen ini dirancang mengikuti alur kerja terintegrasi dari hulu ke hilir yang terbagi ke dalam **tujuh fase fungsional berurutan**. Seluruh aliran data bergerak secara searah (*unidirectional*) dari kiri ke kanan. Desain searah ini memastikan sistem bebas dari potensi kebuntuan siklus (*deadlock*) maupun perulangan tak terbatas (*infinite loop*).

Visualisasi rancangan arsitektur global 7 fase disajikan pada **Gambar 3.1**.

```
+--------------------------------------------------------------------------------------------------------------------+
|                                GAMBAR 3.1: ARSITEKTUR GLOBAL (HIGH-LEVEL) SISTEM 7 FASE                            |
+--------------------------------------------------------------------------------------------------------------------+
|                                                                                                                    |
|   [FASE 1: SUMBER DATA]                                                                                            |
|   - Yahoo Finance (OHLCV Historis)                                                                                 |
|   - Yahoo Finance (Fundamental & Rasio)                                                                            |
|   - 3 Aliran RSS Berita (Google News Emiten, Makro BI/OJK, CNBC Market)                                            |
|          |                                                                                                         |
|          v                                                                                                         |
|   [FASE 2: PYTHON ENGINE & PRE-PROCESSING]                                                                         |
|   - Data Fetcher & News Fetcher (Pembersihan, Lowercase, Buffer 2 Tahun)                                           |
|   - Master Cache Lokal (master_news.json, master_ohlcv.csv, master_fundamentals.json)                              |
|   - Indicator Calculator (Kalkulasi MACD, RSI, SMA, Bollinger Bands, KDJ)                                          |
|          |                                                                                                         |
|          v                                                                                                         |
|   [FASE 3: PROMPT & LLM CONFIG]                                                                                    |
|   - Prompt Templates (Definisi Persona & Batasan 3 Kalimat Executive Summary)                                      |
|   - Pengaturan Temperature (0.0 Faktual vs 0.7 Kreatif)                                                            |
|   - Provider LLM Modular (Gemini, Groq, Ollama)                                                                    |
|          |                                                                                                         |
|          v                                                                                                         |
|   [FASE 4: OTAK LLM (PROSES INTERNAL)]                                                                             |
|   - Tokenisasi & Vektorisasi Embedding                                                                             |
|   - Multi-Head Self-Attention (Komputasi Matriks Q, K, V)                                                          |
|   - Normalisasi Lapisan (LayerNorm) & Generasi Teks Semantik                                                       |
|          |                                                                                                         |
|          v                                                                                                         |
|   [FASE 5: ORKESTRASI 12-AGEN LANGGRAPH DAG]                                                                       |
|   - Tim Analis (4 Agen Paralel: Fundamental, Teknikal, Sentimen, Makro)                                            |
|   - Tim Peneliti (Debat Adversarial: Bullish vs Bearish -> Research Facilitator)                                   |
|   - Tim Manajemen Risiko (Konservatif vs Agresif -> Risk Facilitator)                                              |
|   - Tim Eksekusi (Portfolio Manager -> Trading Agent)                                                              |
|   - Didukung oleh TradingState (Memori Estafet + Operator Reducer)                                                 |
|          |                                                                                                         |
|          v                                                                                                         |
|   [FASE 6: OUTPUT SISTEM]                                                                                          |
|   - Reasoning Log (.txt) -> Audit Transparansi Keputusan (Explainable AI)                                          |
|   - Trade Decision (JSON) -> {"action": "BUY/SELL/HOLD", "quantity": N, "confidence": X}                          |
|          |                                                                                                         |
|          v                                                                                                         |
|   [FASE 7: ANTARMUKA PENGGUNA (STREAMLIT UI)]                                                                      |
|   - Tab 1: Live AI Debate (Visualisasi Transkrip Streaming & Kartu Keputusan)                                      |
|   - Tab 2: Backtest Charts (Grafik Portofolio, Candlestick Titik Beli/Jual, Perbandingan Baseline)                  |
|          |                                                                                                         |
+--------------------------------------------------------------------------------------------------------------------+
```

Rincian interaksi antar-fase pada arsitektur global tersebut diuraikan sebagai berikut:

#### 1. Fase 1: Sumber Data Eksternal (*Data Sources*)
Fase pertama berfungsi sebagai sensor akuisisi informasi dari internet. Sumber data dikelompokkan menjadi data kuantitatif harga transaksi (OHLCV) dan data fundamental keuangan dari Yahoo Finance API, serta data kualitatif teks berita dari tiga aliran RSS sindikasi (Google News dan CNBC Indonesia).

#### 2. Fase 2: Mesin Pemrosesan Python (*Python Engine & Pre-Processing*)
Data mentah yang ditarik dari internet diproses secara lokal oleh mesin Python tanpa campur tangan model AI. Modul `Data Fetcher` membersihkan hierarki indeks kolom dan menerapkan penyangga mundur 2 tahun. Modul `NewsFetcher` menyaring kata kunci sampah dan menduplikasi judul berita. Seluruh data bersih disimpan ke dalam berkas penyimpanan lokal (*Local Cache*) dan diproses oleh `Indicator Calculator` untuk menghasilkan lima matriks indikator teknikal (MACD, RSI, SMA, Bollinger Bands, dan KDJ).

#### 3. Fase 3: Konfigurasi Prompt & Parameter Model (*Prompt & LLM Config*)
Data angka dan teks dari Fase 2 dikonversi menjadi format bahasa alami melalui penyuntikan konteks (*context injection*) ke dalam templat instruksi sistem (*prompt templates*). Pada fase ini, sistem mengonfigurasi batasan peran (*persona*), aturan format luaran (maksimal 3 kalimat per analis), serta nilai parameter *Temperature* (0.0 untuk tugas pelaporan faktual dan 0.7 untuk perdebatan eksploratif).

#### 4. Fase 4: Proses Komputasi Internal Model (*Otak LLM*)
Paket instruksi dikirimkan melalui API menuju kluster komputasi model bahasa (Google Gemini). Di dalam model, teks dipecah menjadi token diskret, dipetakan ke dalam vektor semantik, diproses melalui mekanisme *Multi-Head Self-Attention* menggunakan matriks *Query, Key, Value* (Q, K, V), dan distabilkan melalui *Layer Normalization* sebelum teks analisis dikembalikan ke mesin lokal.

#### 5. Fase 5: Orkestrasi 12-Agen LangGraph DAG (*Inti Sistem*)
Fase ini merupakan pengatur alur kerja utama di mana 12 agen AI dieksekusi secara berurutan dan paralel menggunakan topologi DAG. Aliran informasi dikoordinasikan secara penuh melalui memori bersama bertipe `TypedDict` yang disebut `TradingState`. Mekanisme estafet memori ini mencegah kehilangan data (*context loss*) dan memastikan setiap lapisan agen hanya menerima intisari kesimpulan dari lapisan sebelumnya.

#### 6. Fase 6: Format Luaran Sistem (*System Output*)
Setelah ke-12 agen menuntaskan siklus analisis, sistem menghasilkan dua jenis berkas keluaran:
1. **Reasoning Log (.txt):** Rekam jejak pemikiran lengkap yang mencatat seluruh laporan analis, transkrip perdebatan *Bullish vs Bearish*, pertimbangan risiko, hingga alasan akhir pemilihan keputusan oleh Portfolio Manager (*Explainable AI*).
2. **Trade Decision (JSON):** Perintah eksekusi formal terstruktur yang memuat aksi transaksi (`action`), kuantitas lot (`quantity`), dan derajat keyakinan model (`confidence`).

#### 7. Fase 7: Antarmuka Pengguna Interaktif (*Streamlit Dashboard*)
Lapisan visualisasi berbasis web yang menyediakan dua ruang kerja interaktif: Tab 1 (*Live AI Debate*) untuk memantau dialog perdebatan antar-agen secara langsung (*real-time streaming*), serta Tab 2 (*Backtest Charts*) untuk menelaah kurva pertumbuhan portofolio, titik eksekusi transaksi pada grafik *candlestick*, dan perbandingan terhadap strategi acuan (*baseline*).

### 3.3.2 Komponen dan Peran Sistem
Pembagian tugas dan pemetaan modul perangkat lunak pada setiap fase dirangkum dalam **Tabel 3.1**.

**Tabel 3.1. Pemetaan komponen utama, fase arsitektur, dan perannya dalam sistem**
| Fase Arsitektur | Komponen / Modul | Berkas Implementasi | Peran dan Tanggung Jawab Utama |
|:---|:---|:---|:---|
| **Fase 1: Sumber Data** | Yahoo Finance & RSS Feeds | Internet / Web Endpoints | Menyediakan data mentah harga harian, laporan rasio keuangan, dan umpan berita pasar modal. |
| **Fase 2: Python Engine** | Data & News Fetcher, Calculator | `tools/data_fetcher.py`<br>`tools/news_fetcher.py`<br>`tools/indicator_calculator.py` | Ekstraksi data, pembersihan noise, kalkulasi buffer historis, kalkulasi indikator teknikal, dan manajemen cache. |
| **Fase 3: Prompt Config** | Prompt Manager & LLM Setup | `config/prompts/`<br>`config/llm_config.py` | Standarisasi instruksi persona, injeksi data ke template, dan manajemen hiperparameter temperature. |
| **Fase 4: Otak LLM** | Gemini Cloud Inference | Google API Cloud | Komputasi vektor embedding, evaluasi atensi token QKV, dan generasi tanggapan semantik teks. |
| **Fase 5: Orkestrasi DAG** | LangGraph Workflow Engine | `orchestration/graph.py`<br>`orchestration/state.py` | Orkestrasi eksekusi 12 node agen, sinkronisasi memori estafet TradingState, dan isolasi konflik konkurensi. |
| **Fase 6: Output Sistem** | Backtester Formatter | `orchestration/backtester.py` | Pencetakan rekam jejak penalaran (Reasoning Log) dan pembentukan sinyal eksekusi transaksi JSON. |
| **Fase 7: Antarmuka Web** | Streamlit Dashboard | `main.py` / Streamlit Engine | Visualisasi interaktif dialog agen secara streaming dan komparasi grafik performa portofolio. |

---

## 3.4 Perancangan Pipeline Data Ingestion & Mitigasi Bias
Integritas hasil simulasi perdagangan saham bergantung sepenuhnya pada kualitas data masukan. Pipeline *data ingestion* dirancang untuk memastikan bahwa proses penarikan data berjalan mandiri, arsip tersimpan rapi, dan terbebas dari kesalahan kebocoran data masa depan (*Look-Ahead Bias*).

Struktur pipeline *data ingestion* dimodelkan dalam **enam lapisan fungsional bertingkat**, sebagaimana diilustrasikan pada **Gambar 3.2**.

```
+--------------------------------------------------------------------------------------------------------------------+
|                                GAMBAR 3.2: PIPELINE DATA INGESTION & MITIGASI BIAS                                 |
+--------------------------------------------------------------------------------------------------------------------+
|                                                                                                                    |
|   [LAPISAN 1: SUMBER DATA EKSTERNAL (INTERNET)]                                                                    |
|   - Google News RSS ('{ticker} saham') | Google News RSS ('suku bunga BI OJK') | CNBC Indonesia RSS Market         |
|   - Yahoo Finance API (OHLCV Historis) | Yahoo Finance API (Fundamental & Neraca Keuangan)                         |
|          |                                                          |                                              |
|          | (Aliran Teks Berita)                                     | (Aliran Angka Kuantitatif)                   |
|          v                                                          v                                              |
|   [LAPISAN 3: PYTHON EXTRACTION & PRE-PROCESSING]                                                                  |
|   - NewsFetcher (Negative Keyword Filter & Incremental Append Deduplication)                                       |
|   - YFinanceFetcher (Penyangga Mundur 2 Tahun & Normalisasi Lowercase Kolom)                                       |
|          |                                                          |                                              |
|          | (Pemanggilan Terjadwal via Task Scheduler)               |                                              |
|          v                                                          |                                              |
|   [LAPISAN 2: OTOMASI SCHEDULER & PIPELINE HARIAN]                  |                                              |
|   - Windows Task Scheduler (Daily 11:00 AM WIB, StartWhenAvailable) |                                              |
|   - run_collector.vbs (Eksekusi Headless Senyap tanpa Jendela CMD)  |                                              |
|   - daily_news_collector.py (Iterasi 5 Bank: BBRI, BBCA, BMRI, BBNI, BRIS)                                         |
|   - collector_log.txt (Audit Trail & Pencatatan Metrik Harian)      |                                              |
|          |                                                          |                                              |
|          v                                                          v                                              |
|   [LAPISAN 4: LOCAL STORAGE / MASTER CACHE (data/cache/{ticker}/)]                                                 |
|   - master_news.json (Arsip Teks Berita Bersih)                                                                    |
|   - master_ohlcv.csv (Matriks Deret Waktu Harga Harian)                                                           |
|   - master_fundamentals.json (Snapshot Rasio Valuasi & Laporan Keuangan)                                           |
|          |                                                          |                                              |
|          | (Pemuatan One-Shot ke Memori RAM saat Backtest Dimulai)  |                                              |
|          +----------------------------+-----------------------------+                                              |
|                                       v                                                                            |
|   [LAPISAN 5: RUNTIME BACKTESTING / TIME-SLICING (PENCEGAHAN BIAS)]                                                |
|   - Backtester Engine (Loop Mingguan Penutupan Jumat)                                                              |
|   - Time-Slicing Data Harga: Hanya memotong baris data di mana t <= Date                                           |
|   - Time-Slicing Data Berita: Hanya mengambil artikel di mana Date - 7 hari <= t_published <= Date                 |
|          |                                                                                                         |
|          v (Data Bersih Terpotong Temporal)                                                                        |
|   [LAPISAN 6: KONSUMSI AGEN ANALIS SPESIALIS (FASE 5)]                                                             |
|   - Technical Analyst  <-- Menerima Indikator dari Sliced OHLCV                                                    |
|   - Sentiment Analyst  <-- Menerima Judul Berita Mikro dari Sliced News                                            |
|   - Macro Analyst      <-- Menerima Judul Berita Kebijakan dari Sliced News                                        |
|   - Fundamental Analyst<-- Menerima Snapshot Rasio dari master_fundamentals.json                                   |
|                                                                                                                    |
+--------------------------------------------------------------------------------------------------------------------+
```

Rancangan teknis pada masing-masing lapisan diuraikan sebagai berikut:

### 3.4.1 Sumber Data Eksternal (Lapisan 1)
Sistem memproses lima aliran data dari internet yang dipisahkan berdasarkan karakteristik informasinya:
* **Kategori Kualitatif (Teks Naratif):**
  1. *Google News RSS Query* `'{ticker} saham'`: Menghimpun artikel berita mikro emiten (misalnya sentimen dividen BBRI atau pertumbuhan laba kredit BMRI).
  2. *Google News RSS Query* `'suku bunga BI OJK'`: Menghimpun berita ekonomi makro yang berdampak sistemik pada margin bunga perbankan nasional.
  3. *CNBC Indonesia RSS Market Feed*: Menghimpun dinamika bursa saham harian, aksi korporasi, dan arus dana investor asing (*foreign flow*).
* **Kategori Kuantitatif (Numerik Deret Waktu):**
  4. *Yahoo Finance OHLCV*: Data historis harga saham harian untuk kalkulasi indikator teknikal.
  5. *Yahoo Finance Fundamental*: Laporan neraca, laba rugi, dan rasio valuasi kuartalan.

### 3.4.2 Otomasi Penjadwal & Jejak Audit (Lapisan 2)
Guna memastikan kesinambungan akumulasi arsip berita harian tanpa ketergantungan pada tindakan manual pengguna, dirancang rantai otomasi sistem operasi:
1. **Windows Task Scheduler:** Layanan penjadwal sistem operasi yang disetel mengeksekusi skrip koleksi setiap hari pada pukul 11:00 WIB. Parameter `StartWhenAvailable` diaktifkan sehingga apabila komputer berada dalam status nonaktif atau mode tidur pada jadwal tersebut, Windows secara otomatis menjalankan tugas sesaat setelah sistem dinyalakan kembali.
2. **`run_collector.vbs`:** Skrip VBScript yang bertindak sebagai jembatan eksekusi senyap (*silent headless execution*). Skrip ini memanggil `run_collector.bat` dengan mode jendela tersembunyi (parameter `0`), sehingga eksekusi Python berjalan di latar belakang tanpa memunculkan jendela baris perintah (*Command Prompt*) yang mengganggu pengguna.
3. **`daily_news_collector.py`:** Program orkestrator yang mengulang prosedur penarikan berita untuk kelima emiten bank (BBRI, BBCA, BMRI, BBNI, BRIS) secara berurutan. Seluruh proses untuk kelima bank memerlukan waktu komputasi sekitar 5 hingga 8 detik per hari.
4. **`scripts/collector_log.txt`:** Berkas jejak audit operasional yang mencatat stempel waktu eksekusi, volume penambahan berita baru, total akumulasi arsip bersih, serta status integritas proses sebagai bukti verifikasi operasional sistem.

### 3.4.3 Pra-Pemrosesan Data Python (Lapisan 3)
Sebelum disimpan ke media penyimpanan lokal, data mentah divalidasi melalui dua modul pra-pemrosesan:
* **`NewsFetcher` (`tools/news_fetcher.py`):**
  * *Negative Keyword Filter:* Menyaring dan mengeliminasi artikel yang memuat kata kunci non-investasi atau artikel edukasi pemula (seperti *"cara beli"*, *"panduan pemula"*, *"pembobolan ATM"*). Filter ini memastikan arsip hanya diisi oleh warta yang memuat sinyal pergerakan pasar material.
  * *Incremental Append & Deduplication:* Modul membaca arsip yang telah tersimpan di cache lokal, membandingkan judul artikel baru menggunakan struktur data himpunan (*set*), dan hanya menambahkan artikel yang belum pernah tercatat. Pendekatan ini menjaga pertumbuhan arsip secara organik tanpa risiko duplikasi data.
* **`YFinanceFetcher` (`tools/data_fetcher.py`):**
  * *2-Year Historical Buffer:* Sistem secara otomatis menghitung mundur rentang waktu dua tahun dari tanggal awal simulasi. Penyangga data ini wajib disediakan agar indikator jangka panjang seperti SMA-200 memiliki kecukupan data historis dan tidak menghasilkan nilai kosong (*NaN*) pada awal simulasi.
  * *Lowercase Column Normalization:* Menormalisasi seluruh penamaan kolom hasil unduhan menjadi format huruf kecil (`open, high, low, close, volume`) guna menjamin kompatibilitas penuh dengan pustaka komputasi kuantitatif.

### 3.4.4 Struktur Master Cache Lokal (Lapisan 4)
Hasil pemrosesan disimpan pada direktori penyimpanan lokal terisolasi per emiten (`data/cache/{ticker}/`) dalam tiga berkas master:
1. `master_news.json`: Arsip berita bersih dengan atribut terstruktur `title`, `link`, `published`, dan `source`.
2. `master_ohlcv.csv`: Matriks deret waktu harga transaksi historis.
3. `master_fundamentals.json`: Potret metrik valuasi pasar dan laporan keuangan kuartalan.

### 3.4.5 Perancangan Runtime Time-Slicing & Pencegahan Bias (Lapisan 5)
Pada saat eksekusi simulasi *backtesting* mingguan, seluruh berkas master dimuat ke dalam memori komputer (RAM) satu kali di awal (*one-shot loading*). Pada setiap perulangan simulasi hari Jumat ($T_{\text{sim}}$), mesin *backtester* menerapkan pemotongan temporal secara deterministik:
* **Time-Slicing Data Harga ($t \le T_{\text{sim}}$):** Seluruh baris data transaksi dengan tanggal melampaui $T_{\text{sim}}$ dibuang dari memori kalkulasi indikator teknikal.
* **Time-Slicing Data Berita ($T_{\text{sim}} - 7 \text{ hari} \le t_{\text{published}} \le T_{\text{sim}}$):** Agen analis hanya diizinkan membaca artikel yang dipublikasikan dalam kurun waktu tujuh hari kalender menjelang hari Jumat simulasi. Berita yang terbit setelah hari Jumat dieliminasi sepenuhnya guna menjamin kondisi *Zero Look-Ahead Bias*. Berita yang terbit lebih dari tujuh hari sebelumnya diabaikan agar kesimpulan sentimen tetap merefleksikan dinamika pasar yang paling relevan.

---

## 3.5 Perancangan Topologi & Orkestrasi Multi-Agent (LangGraph DAG)
Inti kecerdasan artifisial sistem diorganisasikan menggunakan kerangka kerja LangGraph ke dalam topologi *Directed Acyclic Graph* (DAG). Sifat DAG menjamin bahwa aliran penalaran bergerak maju tanpa ada putaran balik, merefleksikan hierarki rantai komando pada institusi keuangan profesional.

Topologi orkestrasi 12 agen AI disajikan secara komprehensif pada **Gambar 3.3**.

```
+--------------------------------------------------------------------------------------------------------------------+
|                       GAMBAR 3.3: TOPOLOGI DIRECTED ACYCLIC GRAPH (DAG) 12-AGEN VIA LANGGRAPH                      |
+--------------------------------------------------------------------------------------------------------------------+
|                                                                                                                    |
|   [TIM 1: ANALIS SPESIALIS] (Eksekusi Paralel)                                                                     |
|   +--------------------+  +--------------------+  +--------------------+  +--------------------+                   |
|   | Fundamental Analyst|  | Technical Analyst  |  | Sentiment Analyst  |  |   Macro Analyst    |                   |
|   | (P/E, P/B, ROE)    |  | (RSI, MACD, SMA)   |  | (Berita Emiten)    |  | (BI-Rate, OJK)     |                   |
|   +--------------------+  +--------------------+  +--------------------+  +--------------------+                   |
|             \                       |                       |                      /                               |
|              +----------------------+-----------------------+---------------------+                                |
|                                     |                                                                              |
|                                     v (Laporan Analisis: Maksimal 3 Kalimat per Analis = ~12 Kalimat)              |
|                                                                                                                    |
|   [TIM 2: PENELITI] (Sintesis melalui Debat Adversarial)                                                           |
|   +------------------------------------+         +-------------------------------------+                           |
|   |        Bullish Researcher          | <=====> |         Bearish Researcher          |                           |
|   |     (Eksplorasi Katalis Beli)      | (Debat) |      (Eksplorasi Risiko Jual)       |                           |
|   +------------------------------------+         +-------------------------------------+                           |
|                     \                                       /                                                      |
|                      +------------------+------------------+                                                       |
|                                         |                                                                          |
|                                         v                                                                          |
|                           +----------------------------+                                                           |
|                           |     Research Facilitator   |                                                           |
|                           | (Merumuskan Konsensus Riset|                                                           |
|                           +----------------------------+                                                           |
|                                         |                                                                          |
|                                         v (Research Consensus: 3-5 Kalimat)                                        |
|                                                                                                                    |
|   [TIM 3: MANAJEMEN RISIKO] (Evaluasi Dua Perspektif Risiko)                                                       |
|   +------------------------------------+         +-------------------------------------+                           |
|   |      Aggressive Risk Analyst       |         |      Conservative Risk Analyst      |                           |
|   |   (Maksimasi Peluang Keuntungan)   |         |    (Proteksi Modal & Drawdown)      |                           |
|   +------------------------------------+         +-------------------------------------+                           |
|                     \                                       /                                                      |
|                      +------------------+------------------+                                                       |
|                                         |                                                                          |
|                                         v                                                                          |
|                           +----------------------------+                                                           |
|                           |      Risk Facilitator      |                                                           |
|                           | (Panduan Alokasi Posisi)   |                                                           |
|                           +----------------------------+                                                           |
|                                         |                                                                          |
|                                         v (Risk Consensus: ~3 Kalimat)                                             |
|                                                                                                                    |
|   [TIM 4: EKSEKUSI] (Hierarki Keputusan Tunggal)                                                                   |
|   +------------------------------------------------------------------------------------+                           |
|   |                                Portfolio Manager                                   |                           |
|   |         (Hakim Tertinggi: Menilai Konsensus Riset, Konsensus Risiko, & Kas)        |                           |
|   +------------------------------------------------------------------------------------+                           |
|                                         |                                                                          |
|                                         v (Instruksi Keputusan: Aksi, Lot, Keyakinan)                              |
|   +------------------------------------------------------------------------------------+                           |
|   |                                  Trading Agent                                     |                           |
|   |         (Penerjemah Eksekusi: Konversi Satuan Lot BEI, Fee 0.2%, Format JSON)      |                           |
|   +------------------------------------------------------------------------------------+                           |
|                                         |                                                                          |
|                                         v                                                                          |
|                    OUTPUT AKHIR: {"action": "BUY", "quantity": 500, "confidence": 0.85}                            |
|                                                                                                                    |
|   ======================================================================================                           |
|   [FONDASI: TradingState - Memori Estafet Antar-Tim + Operator Reducer Penjaga Mutex]                              |
|   ======================================================================================                           |
|                                                                                                                    |
+--------------------------------------------------------------------------------------------------------------------+
```

Rincian pembagian kerja dan mekanisme interaksi pada setiap tingkatan adalah sebagai berikut:

### 3.5.1 Komponen Fondasi: TradingState & Operator Reducer
Seluruh pertukaran informasi antar-agen dijembatani oleh sebuah struktur data kamus terdefinisi (*TypedDict*) yang dinamakan `TradingState`. Objek ini bertindak sebagai media memori bersama yang diteruskan secara estafet dari satu tim ke tim berikutnya. 

Mengingat empat analis pada Tim 1 bekerja secara paralel dan menuliskan laporannya secara simultan, terdapat risiko penulisan bersama (*race condition*). Untuk meniadakan risiko tersebut, LangGraph dikonfigurasi dengan fungsi agregasi **Reducer**:
```python
def merge_analyst_reports(current: dict, update: dict) -> dict:
    current.update(update)
    return current
```
Operator ini memastikan bahwa hasil penalaran dari masing-masing agen paralel digabungkan secara aman tanpa saling menimpa (*non-destructive merge*).

### 3.5.2 Tim 1: Analis Spesialis (*Analisis Data Dasar*)
Tim pertama terdiri dari empat agen analis yang bekerja secara simultan (*fan-out execution*) untuk mengoptimalkan durasi pemrosesan. Masing-masing analis memiliki akses ke modalitas data yang berbeda sesuai domain keahliannya:
1. **Fundamental Analyst:** Mengkaji berkas `master_fundamentals.json` untuk mengevaluasi rasio valuasi historis (P/E, P/B), pertumbuhan laba bersih, struktur utang, dan profitabilitas ekuitas (ROE).
2. **Technical Analyst:** Menganalisis berkas `master_ohlcv.csv` dan kalkulasi indikator teknikal (RSI, MACD, SMA-20/50, Bollinger Bands, KDJ) guna membaca momentum harga dan potensi pembalikan arah tren.
3. **Sentiment Analyst:** Menelaah kumpulan judul berita spesifik emiten dari `master_news.json` hasil pemotongan temporal untuk mengukur suasana psikologis pasar terhadap saham target.
4. **Macro Analyst:** Mempelajari judul berita makroekonomi guna menilai dampak kebijakan suku bunga BI-Rate dan regulasi OJK terhadap likuiditas industri perbankan.

*Prinsip Desain Executive Summary:* Seluruh analis diwajibkan memadatkan laporannya menjadi **maksimal tiga kalimat terstruktur**. Pembatasan ini diterapkan guna mencegah kelebihan muatan token (*token overload*) dan menjaga ketajaman fokus konteks bagi agen pada lapisan berikutnya. Total informasi yang diteruskan ke Tim 2 berkisar pada 12 kalimat ringkas.

### 3.5.3 Tim 2: Peneliti (*Sintesis melalui Debat Adversarial*)
Tim Peneliti bertugas membedah laporan ringkas analis melalui mekanisme debat adversarial dua arah [2], [6]:
1. **Bullish Researcher:** Diprogram dengan persona optimis untuk membangun argumen terkuat mengapa saham bersangkutan layak dibeli (*BUY*), menonjolkan seluruh katalis kenaikan harga dan peluang pertumbuhan.
2. **Bearish Researcher:** Diprogram dengan persona skeptis untuk membangun argumen sanggahan mengapa saham bersangkutan berisiko turun atau harus dihindari (*SELL/AVOID*), mengidentifikasi ancaman valuasi dan potensi pembalikan tren.
3. **Research Facilitator:** Bertindak sebagai moderator independen yang mengevaluasi reliabilitas bukti dari kubu *Bullish* dan *Bearish*, lalu merumuskan dokumen kesimpulan tunggal: **Research Consensus** (sekitar 3 hingga 5 kalimat).

Mekanisme dialektika ini memastikan bahwa rekomendasi yang diteruskan ke tahap berikutnya bukan merupakan opini sepihak, melainkan sintesis yang telah diuji melalui kritik terbalik.

### 3.5.4 Tim 3: Manajemen Risiko (*Evaluasi Dua Perspektif Risiko*)
Tim Manajemen Risiko menerima dokumen *Research Consensus* dan mengevaluasi rencana transaksi berdasarkan prinsip kehati-hatian modal:
1. **Aggressive Risk Analyst:** Menilai transaksi dari sudut pandang peluang imbal hasil maksimal, mendorong alokasi porsi modal yang lebih berani ketika sinyal pasar terkonfirmasi kuat.
2. **Conservative Risk Analyst:** Menilai transaksi dari sudut pandang proteksi modal dan pencegahan penurunan nilai terdalam (*maximum drawdown*), mengusulkan pembatasan posisi atau penundaan aksi jika ketidakpastian pasar tergolong tinggi.
3. **Risk Facilitator:** Menyelaraskan rekomendasi agresif dan konservatif menjadi panduan alokasi risiko terukur: **Risk Consensus** (sekitar 3 kalimat). Dokumen ini merumuskan batas toleransi risiko (*stop-loss*) dan pedoman ukuran posisi modal (*position sizing*).

### 3.5.5 Tim 4: Eksekusi (*Pengambilan Keputusan Akhir*)
Tingkat akhir dari hierarki sistem dijalankan oleh dua agen pengambil tindakan:
1. **Portfolio Manager (PM):** Bertindak sebagai pemutus investasi tertinggi (*supreme judge*). PM membaca intisari *Research Consensus*, panduan *Risk Consensus*, serta saldo kas portofolio terkini untuk menetapkan keputusan final: **BUY**, **SELL**, atau **HOLD**, disertai penetapan nilai derajat keyakinan (*confidence score*) pada rentang 0.0 hingga 1.0.
2. **Trading Agent:** Bertindak sebagai eksekutor teknis. Agen ini menerjemahkan instruksi bahasa alami dari PM menjadi format terstruktur JSON, mengonversi jumlah lembar ke dalam satuan fraksi lot standar BEI (1 lot = 100 lembar) [9], serta memperhitungkan potongan biaya transaksi broker sebesar 0,2%.

Struktur data luaran JSON yang dihasilkan dari rantai orkestrasi didefinisikan sebagai berikut:
```json
{
  "action": "BUY",
  "quantity": 500,
  "confidence": 0.85
}
```

### 3.5.6 Perancangan Prompt Persona & Parameter Model
Konfigurasi parameter inferensi disesuaikan secara ketat dengan fungsi spesifik masing-masing agen, sebagaimana ditunjukkan pada **Tabel 3.2**.

**Tabel 3.2. Pemetaan persona agen, nilai temperature, dan sumber konteks input**
| No | Identitas Agen | Peran Tim | Temperature | Masukan Konteks Data |
|:---:|:---|:---|:---:|:---|
| 1 | Fundamental Analyst | Tim 1 (Analis) | 0.0 | Snapshot metrik rasio keuangan `master_fundamentals.json` |
| 2 | Technical Analyst | Tim 1 (Analis) | 0.0 | Nilai komputasi indikator teknikal dari `master_ohlcv.csv` |
| 3 | Sentiment Analyst | Tim 1 (Analis) | 0.0 | Judul berita spesifik emiten hasil pemotongan temporal |
| 4 | Macro Analyst | Tim 1 (Analis) | 0.0 | Judul berita moneter dan regulasi hasil pemotongan temporal |
| 5 | Bullish Researcher | Tim 2 (Peneliti) | 0.7 | 4 laporan ringkas analis (fokus katalis positif) |
| 6 | Bearish Researcher | Tim 2 (Peneliti) | 0.7 | 4 laporan ringkas analis (fokus risiko pelemahan) |
| 7 | Research Facilitator | Tim 2 (Peneliti) | 0.0 | Transkrip argumentasi Bullish vs Bearish Researcher |
| 8 | Aggressive Risk Analyst | Tim 3 (Risiko) | 0.7 | Naskah kesimpulan Research Consensus |
| 9 | Conservative Risk Analyst | Tim 3 (Risiko) | 0.7 | Naskah kesimpulan Research Consensus |
| 10 | Risk Facilitator | Tim 3 (Risiko) | 0.0 | Usulan rekomendasi Aggressive vs Conservative Analyst |
| 11 | Portfolio Manager | Tim 4 (Eksekusi) | 0.0 | Research Consensus, Risk Consensus, dan status saldo kas |
| 12 | Trading Agent | Tim 4 (Eksekusi) | 0.0 | Instruksi keputusan PM dan aturan fraksi perdagangan BEI |

---

## 3.6 Perancangan Skenario Pengujian dan Evaluasi
Guna mengevaluasi performa sistem secara objektif pada Bab 4, dirancang dua skenario eksperimen simulasi serta tolok ukur metrik evaluasi portofolio:

### 3.6.1 Skenario 1: Simulasi Backtesting Multi-Bank
* **Aset Uji:** 5 emiten perbankan Bursa Efek Indonesia (BBRI.JK, BBCA.JK, BMRI.JK, BBNI.JK, BRIS.JK).
* **Modal Awal Portofolio:** Ditetapkan sebesar Rp 100.000.000 (seratus juta rupiah) untuk masing-masing emiten.
* **Biaya Transaksi Finansial:** Dikenakan potongan biaya komisi broker dan pajak bursa sebesar 0,2% pada setiap transaksi beli maupun jual [9].
* **Interval Transaksi:** Simulasi keputusan mingguan pada setiap hari Jumat penutupan bursa.
* **Strategi Acuan Pembanding (*Baseline*):**
  1. *Buy and Hold Strategy:* Membeli saham pada awal periode pengujian dan mempertahankan posisi hingga akhir simulasi tanpa transaksi tambahan.
  2. *SMA Crossover Strategy:* Strategi aturan teknikal klasik yang mengeksekusi sinyal beli saat SMA-20 melintas ke atas SMA-50 (*Golden Cross*) dan sinyal jual saat melintas ke bawah (*Death Cross*).
  3. *MACD Strategy:* Strategi yang mengeksekusi aksi transaksi berdasarkan perpotongan garis MACD terhadap garis sinyal.

### 3.6.2 Skenario 2: Studi Ablasi (*Ablation Study*)
Mengadopsi metodologi evaluasi Xiao et al. [1], studi ablasi dirancang untuk mengisolasi dan membuktikan secara empiris kontribusi dari mekanisme debat adversarial:
1. **Konfigurasi A (Sistem Penuh 12-Agen):** Arsitektur usulan lengkap (4 Analis $\rightarrow$ Debat Adversarial Peneliti $\rightarrow$ Evaluasi Risiko $\rightarrow$ Eksekusi).
2. **Konfigurasi B (Sistem 8-Agen Tanpa Debat):** Menghilangkan Tim Peneliti Debat (laporan 4 Analis diteruskan langsung ke Tim Manajemen Risiko $\rightarrow$ Eksekusi).
3. **Konfigurasi C (Sistem Model Tunggal / Single-Agent):** Satu model LLM tunggal yang menerima seluruh indikator dan teks berita secara langsung untuk mengambil keputusan transaksi tanpa dekomposisi peran.

### 3.6.3 Metrik Evaluasi Kinerja Finansial
Performa investasi diukur secara kuantitatif melalui empat persamaan standar industri manajemen portofolio:
1. **Cumulative Return ($R_{\text{cum}}$):** Total persentase pertumbuhan nilai modal portofolio selama periode pengujian:
   $$R_{\text{cum}} = \frac{V_{\text{akhir}} - V_{\text{awal}}}{V_{\text{awal}}} \times 100\% \tag{3.1}$$
   di mana $V_{\text{awal}}$ adalah modal awal simulasi dan $V_{\text{akhir}}$ adalah nilai total likuiditas (kas ditambah nilai pasar saham) pada akhir pengujian.
2. **Sharpe Ratio ($S$):** Mengukur imbal hasil berlebih (*excess return*) relatif terhadap risiko volatilitas portofolio:
   $$S = \frac{\bar{R}_p - R_f}{\sigma_p} \tag{3.2}$$
   di mana $\bar{R}_p$ merepresentasikan rata-rata imbal hasil portofolio, $R_f$ adalah suku bunga bebas risiko (mengacu pada BI-Rate acuan), dan $\sigma_p$ adalah simpangan baku dari imbal hasil portofolio.
3. **Maximum Drawdown (MDD):** Persentase penurunan nilai portofolio terdalam dari titik puncak tertinggi (*peak*) menuju titik terendah (*trough*) sebelum puncak baru tercapai:
   $$\text{MDD} = \max_{t} \left( \frac{\text{Peak}_t - V_t}{\text{Peak}_t} \right) \times 100\% \tag{3.3}$$
4. **Win Rate ($W$):** Rasio persentase frekuensi transaksi yang menghasilkan laba bersih terhadap total transaksi yang diselesaikan:
   $$W = \frac{N_{\text{profit}}}{N_{\text{transaksi}}} \times 100\% \tag{3.4}$$

Melalui kerangka pengujian ini, evaluasi sistem pada Bab 4 dipastikan memiliki validitas komparasi yang saintifik, terukur, dan terbebas dari interpretasi subjektif.

---

# DAFTAR REFERENSI

[1] H. Xiao, D. S. Wang, Y. Zhang, M. Zhou, and P. Tang, "TradingAgents: Multi-Agents LLM Financial Trading Framework," *arXiv preprint arXiv:2412.20138*, 2024. [Online]. Available: https://arxiv.org/abs/2412.20138

[2] G. Irving, P. Christiano, and D. Amodei, "AI Safety via Debate," *arXiv preprint arXiv:1805.00899*, 2018. [Online]. Available: https://arxiv.org/abs/1805.00899

[3] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS 2017)*, vol. 30, Long Beach, CA, USA, 2017. [Online]. Available: https://arxiv.org/abs/1706.03762

[4] X. Yu, Z. Chen, Y. Ling, S. Dong, Z. Liu, and J. Lu, "FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making," *arXiv preprint arXiv:2407.06567*, 2024. [Online]. Available: https://arxiv.org/abs/2407.06567

[5] S. Hong, M. Zhuge, J. Chen, X. Zheng, C. Cheng, C. Zhang, J. Wang, S. Wang, Z. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Qin, "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," *arXiv preprint arXiv:2308.00352*, 2023. [Online]. Available: https://arxiv.org/abs/2308.00352

[6] Y. Cai, Y. Lin, C. Ding, and Y. Feng, "FinDebate: Multi-Agent Collaborative Intelligence for Financial Analysis," *arXiv preprint arXiv:2509.17395*, 2025. [Online]. Available: https://arxiv.org/abs/2509.17395

[7] J. J. Murphy, *Technical Analysis of the Financial Markets: A Comprehensive Guide to Trading Methods and Applications*. New York, NY, USA: New York Institute of Finance, 1999. [Online]. Available: https://archive.org/details/technicalanalysi0000murp

[8] A. Damodaran, *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset*, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2012. [Online]. Available: https://archive.org/details/investmentvaluat0000damo

[9] PT Bursa Efek Indonesia, *Keputusan Direksi PT Bursa Efek Indonesia Nomor Kep-00061/BEI/07-2021 perihal Peraturan Nomor II-A tentang Perdagangan Efek Bersifat Ekuitas*, Jakarta, Indonesia, 2021. [Online]. Available: https://www.scribd.com/document/561023773/Peraturan-II-A-Perdagangan-Efek-Bersifat-Ekuitas

[10] Otoritas Jasa Keuangan, *Peraturan Otoritas Jasa Keuangan Republik Indonesia Nomor 12/POJK.03/2021 tentang Bank Umum*, Jakarta, Indonesia, 2021. [Online]. Available: https://peraturan.bpk.go.id/Details/178044/pojk-no-12pojk032021

[11] T. Loughran and B. McDonald, "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks," *The Journal of Finance*, vol. 66, no. 1, pp. 35–65, Feb. 2011. [Online]. Available: https://ideas.repec.org/a/bla/jfinan/v66y2011i1p35-65.html
