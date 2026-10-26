# DOKUMEN PROPOSAL SKRIPSI
## SISTEM PERDAGANGAN SAHAM MULTI-AGEN BERBASIS LARGE LANGUAGE MODEL MENGGUNAKAN ORKESTRASI LANGGRAPH DAG DAN MEKANISME DEBAT ADVERSARIAL PADA SEKTOR PERBANKAN IHSG

---

# BAB 1
# PENDAHULUAN

## 1.1 Latar Belakang
Pasar modal merupakan salah satu indikator vital stabilitas dan pertumbuhan ekonomi nasional. Di Indonesia, dinamika Indeks Harga Saham Gabungan (IHSG) yang dikelola oleh PT Bursa Efek Indonesia (BEI) sangat dipengaruhi oleh pergerakan saham di sektor keuangan, khususnya industri perbankan. Saham-saham perbankan berkapitalisasi pasar besar (*big-cap banks*), seperti PT Bank Rakyat Indonesia (Persero) Tbk (BBRI), PT Bank Central Asia Tbk (BBCA), PT Bank Mandiri (Persero) Tbk (BMRI), PT Bank Negara Indonesia (Persero) Tbk (BBNI), dan PT Bank Syariah Indonesia Tbk (BRIS), secara konsisten menyumbang lebih dari 30% dari total kapitalisasi pasar IHSG dan mendominasi likuiditas transaksi harian [9], [10]. Pergerakan harga saham perbankan ini sangat sensitif terhadap berbagai dimensi informasi yang kompleks, mulai dari fluktuasi harga historis (kuantitatif), laporan kinerja keuangan kuartalan (fundamental), hingga dinamika kebijakan makroekonomi seperti suku bunga acuan Bank Indonesia (BI-Rate) dan regulasi Otoritas Jasa Keuangan (OJK) yang tersebar dalam bentuk berita teks harian (kualitatif).

Dalam praktiknya, pengambilan keputusan investasi yang optimal menuntut integrasi simultan antara analisis teknikal, fundamental, dan sentimen pasar. Namun, investor individu maupun praktisi sering kali menghadapi keterbatasan kapasitas kognitif manusia (*cognitive overload*). Membaca dan mensintesis puluhan hingga ratusan artikel berita finansial setiap hari sembari menghitung indikator kuantitatif secara bersamaan sering kali memicu kelelahan mental, bias konfirmasi (*confirmation bias*), serta keputusan yang didorong oleh kepanikan emosional (*fear and greed*).

Perkembangan mutakhir dalam bidang kecerdasan artifisial, khususnya *Large Language Models* (LLM), telah membuka paradigma baru dalam pemrosesan informasi multimodal dan penalaran teks finansial berdensitas tinggi [3]. Meskipun demikian, penerapan LLM model tunggal (*single-agent LLM*) secara mandiri dalam domain perdagangan saham menghadapi tantangan fundamental berupa halusinasi informasi (*hallucination*) dan rasa terlalu percaya diri (*overconfidence*) [6]. Ketika sebuah model AI diminta menganalisis seluruh data pasar sekaligus dan langsung mengeluarkan keputusan beli atau jual, model tersebut cenderung mengalami *context loss*, gagal menangkap sinyal kontradiktif antar-indikator, serta menghasilkan rekomendasi yang rapuh tanpa dasar penalaran yang terverifikasi.

Untuk mengatasi kelemahan model tunggal, riset terkini beralih ke paradigma *Multi-Agent Systems* (MAS). Pendekatan ini mengadopsi prinsip pembagian kerja (*separation of concerns*) selayaknya divisi operasional pada firma manajemen investasi nyata [1], [5]. Dalam arsitektur MAS, tugas-tugas kompleks didekomposisi ke dalam agen-agen spesialis yang memiliki fokus analisis sempit, seperti analis teknikal, fundamental, sentimen, dan makroekonomi [4]. Lebih lanjut, penelitian teoretis mengenai *AI Safety via Debate* membuktikan bahwa interaksi *adversarial* antara dua agen AI yang saling menantang argumen dari perspektif berlawanan secara signifikan membatasi ruang halusinasi dan memaksa sistem mencapai konklusi yang lebih objektif dan jujur [2]. Temuan empiris terbaru oleh Cai et al. dalam *FinDebate* mengonfirmasi bahwa penyematan mekanisme debat (kubu *Bullish* vs *Bearish*) secara efektif memitigasi bias *overconfidence* pada analisis portofolio saham [6].

Meskipun potensi MAS sangat menjanjikan, tantangan kritis lain yang kerap merusak validitas penelitian perdagangan berbasis AI adalah fenomena *Look-Ahead Bias* (kebocoran informasi masa depan ke masa lalu). Banyak kerangka kerja perdagangan kuantitatif secara tidak sengaja mengizinkan algoritma membaca data harga atau teks berita yang terbit setelah tanggal simulasi transaksi, sehingga menghasilkan performa *backtesting* semu yang tidak dapat direplikasi pada kondisi riil [1].

Berdasarkan latar belakang tersebut, penelitian ini merancang dan membangun arsitektur sistem perdagangan saham berbasis *Multi-Agent LLM* (Agent_Saham) yang diorkestrasi menggunakan topologi *Directed Acyclic Graph* (DAG) melalui kerangka kerja LangGraph. Sistem ini mengintegrasikan pipeline *data ingestion* otomatis yang dilengkapi mekanisme *runtime time-slicing* guna menjamin ketiadaan *look-ahead bias*, menerapkan debat adversarial (*Bullish vs Bearish*) serta evaluasi risiko dua arah (*Aggressive vs Conservative*), dan memvalidasi keandalan penalarannya (*Explainable AI*) pada 5 saham perbankan terkemuka di Bursa Efek Indonesia.

---

## 1.2 Rumusan Masalah
Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam penelitian ini dirumuskan sebagai berikut:
1. Bagaimana merancang dan membangun arsitektur *pipeline data ingestion* terotomasi multi-sumber (data deret waktu harga OHLCV, data fundamental, dan teks berita harian) yang secara deterministik mencegah kebocoran informasi masa depan (*Look-Ahead Bias*) pada simulasi perdagangan saham perbankan IHSG?
2. Bagaimana merancang topologi orkestrasi 12 agen LLM berbasis *Directed Acyclic Graph* (DAG) menggunakan kerangka kerja LangGraph dengan pembagian hierarki peran yang terspesialisasi?
3. Bagaimana mekanisme perdebatan adversarial antara agen *Bullish Researcher* dan *Bearish Researcher*, yang disintesis bersama agen manajemen risiko, mampu memitigasi halusinasi model serta menghasilkan keputusan transaksi (*BUY/SELL/HOLD*) yang terukur dan transparan (*Explainable AI*)?

---

## 1.3 Tujuan Penelitian
Tujuan yang ingin dicapai melalui penelitian tugas akhir ini adalah:
1. Mengembangkan arsitektur *pipeline data ingestion* otomatis berbasis Python dan Windows Task Scheduler yang dilengkapi algoritma *runtime temporal time-slicing* pada data harga ($t \le \text{Date}$) dan jendela data berita ($\text{Date}-7 \le t_{\text{published}} \le \text{Date}$).
2. Membangun sistem perdagangan multi-agen 12 node berbasis LangGraph DAG yang mengintegrasikan media transfer memori estafet (*TradingState*) dan mekanisme *Reducer* untuk mencegah konflik data konkuren.
3. Mengimplementasikan mekanisme debat adversarial (*Bullish vs Bearish*) dan evaluasi toleransi risiko (*Aggressive vs Conservative*) guna menekan bias *overconfidence* serta menghasilkan log penalaran eksplisit (*Reasoning Log*) dan sinyal eksekusi JSON terstruktur.

---

## 1.4 Manfaat Penelitian
Penelitian ini diharapkan memberikan manfaat teoretis dan praktis sebagai berikut:
1. **Manfaat Teoretis:** Memberikan kontribusi ilmiah dalam literatur rekayasa perangkat lunak kecerdasan artifisial, khususnya penerapan *Multi-Agent Systems*, topologi DAG, dan teori *AI Safety via Debate* pada pasar modal negara berkembang (*emerging market*) yang memiliki likuiditas dan sensitivitas regulasi unik.
2. **Manfaat Praktis:** Menyediakan platform sistem perdagangan kuantitatif yang transparan bagi investor ritel, manajer investasi, dan akademisi, di mana setiap keputusan investasi disertai dengan audit jejak pemikiran (*Explainable AI*) yang terbebas dari bias emosional manusia.

---

## 1.5 Ruang Lingkup Penelitian
Ruang lingkup dan batasan masalah dalam penelitian perancangan sistem ini mencakup:
1. **Semesta Aset (*Asset Universe*):** Pengujian sistem dibatasi pada 5 emiten sektor perbankan terkemuka di Bursa Efek Indonesia, yaitu BBRI.JK, BBCA.JK, BMRI.JK, BBNI.JK (klasifikasi KBMI 4), dan BRIS.JK (klasifikasi KBMI 3) [10].
2. **Sumber dan Format Data:** Data harga historis (OHLCV) dan data fundamental ditarik melalui Yahoo Finance API. Data berita ditarik secara otomatis dari 3 aliran RSS (Google News query spesifik emiten, Google News query makroekonomi BI/OJK, dan CNBC Indonesia Market Feed) [9].
3. **Model Komputasi Bahasa:** Inferensi kecerdasan artifisial menggunakan model *Large Language Model* Google Gemini (`gemini-flash-lite-latest`) yang diakses melalui antarmuka pemrograman aplikasi (API) LangChain.
4. **Frekuensi Perdagangan:** Keputusan investasi disimulasikan secara mingguan (*weekly trading step*) pada penutupan sesi perdagangan hari Jumat.
5. **Asumsi Pasar Modal:** Simulasi memperhitungkan aturan satuan perdagangan BEI (1 lot = 100 lembar) dan biaya transaksi broker (*slippage* dan komisi) sebesar 0,2% per transaksi [9].
6. **Batasan Dokumen Proposal:** Naskah laporan ini berfokus pada metodologi, perancangan arsitektur sistem, dan skenario evaluasi (Bab 1 sampai Bab 3). Hasil empiris komputasi *backtesting* akan disajikan pada Bab 4.

---

## 1.6 Sistematika Penulisan
Laporan skripsi ini disusun dengan sistematika penulisan sebagai berikut:
* **BAB 1 PENDAHULUAN:** Memuat latar belakang permasalahan, rumusan masalah, tujuan penelitian, manfaat penelitian, ruang lingkup batasan masalah, dan sistematika penulisan.
* **BAB 2 TINJAUAN PUSTAKA:** Membahas teori-teori dasar pendukung penelitian meliputi karakteristik pasar modal Indonesia, landasan analisis teknikal dan fundamental, arsitektur Transformer dan LLM, konsep *Multi-Agent Systems*, teori *AI Safety via Debate*, mitigasi *look-ahead bias*, serta telaah penelitian terkait (*State of the Art*).
* **BAB 3 METODOLOGI DAN PERANCANGAN SISTEM:** Menguraikan metodologi penelitian, justifikasi pemilihan perangkat lunak, perancangan arsitektur global 7 fase, perancangan detail pipeline *data ingestion* dan mitigasi bias, perancangan topologi 12 agen LangGraph DAG, serta rancangan skenario pengujian *backtesting* dan *ablation study*.
* **BAB 4 PENGUJIAN DAN EVALUASI:** Menyajikan hasil implementasi sistem, eksekusi simulasi *backtesting* pada 5 bank, analisis metrik performa portofolio (*Cumulative Return, Sharpe Ratio, Maximum Drawdown, Win Rate*), perbandingan terhadap strategi *baseline*, evaluasi *ablation study*, serta analisis transparansi *Explainable AI*.
* **BAB 5 PENUTUP:** Berisi kesimpulan akhir yang menjawab rumusan masalah penelitian serta saran-saran pengembangan untuk penelitian lanjutan di masa mendatang.
* **DAFTAR REFERENSI:** Memuat daftar pustaka acuan yang disusun menggunakan standar IEEE.

---

# BAB 2
# TINJAUAN PUSTAKA

## 2.1 Karakteristik Pasar Modal Indonesia & Sektor Perbankan
Pasar modal Indonesia diselenggarakan oleh PT Bursa Efek Indonesia (BEI) di bawah pengawasan Otoritas Jasa Keuangan (OJK). Mekanisme transaksi efek ekuitas diatur secara ketat melalui **Keputusan Direksi PT BEI Nomor Kep-00061/BEI/07-2021 perihal Peraturan Nomor II-A tentang Perdagangan Efek Bersifat Ekuitas** [9]. Dalam peraturan tersebut, transaksi saham di pasar reguler wajib memenuhi batasan fraksi harga (*tick size*) dan dilakukan dalam satuan perdagangan standar, di mana **1 Lot setara dengan 100 lembar saham** [9]. Peraturan ini juga menetapkan batasan pergerakan harga harian maksimum melalui mekanisme penolakan penawaran otomatis (*Auto Rejection*), baik batas atas (ARA) maupun batas bawah (ARB), guna menjaga stabilitas pasar dari fluktuasi harga yang tidak wajar.

Di antara berbagai sektor yang tercatat di BEI, industri perbankan memegang peranan paling strategis. Otoritas Jasa Keuangan melalui **Peraturan OJK (POJK) Nomor 12/POJK.03/2021 tentang Bank Umum** mengelompokkan industri perbankan nasional ke dalam Kelompok Bank berdasarkan Modal Inti (KBMI) [10]:
1. **KBMI 1:** Bank dengan modal inti sampai dengan Rp 6.000.000.000.000 (enam triliun rupiah).
2. **KBMI 2:** Bank dengan modal inti lebih dari Rp 6.000.000.000.000 sampai dengan Rp 14.000.000.000.000.
3. **KBMI 3:** Bank dengan modal inti lebih dari Rp 14.000.000.000.000 sampai dengan Rp 70.000.000.000.000.
4. **KBMI 4:** Bank dengan modal inti lebih dari Rp 70.000.000.000.000 (tujuh puluh triliun rupiah).

Emiten perbankan yang tergabung dalam kategori KBMI 4, yaitu BBRI, BBCA, BMRI, dan BBNI, merepresentasikan lebih dari separuh total aset perbankan di Indonesia. Sementara itu, BRIS merupakan bank syariah terbesar nasional yang berada pada kategori KBMI 3 [10]. Karakteristik likuiditas yang tinggi, kapitalisasi pasar yang masif, serta keterbukaan informasi publik yang sangat disiplin menjadikan kelima bank ini sebagai semesta aset (*investment universe*) yang ideal dan representatif untuk pengujian sistem kecerdasan artifisial kuantitatif.

---

## 2.2 Landasan Analisis Finansial: Teknikal, Fundamental, dan Sentimen Berita
Pengambilan keputusan perdagangan saham secara komprehensif bertumpu pada sintesis tiga pilar analisis finansial:

### 2.2.1 Analisis Teknikal
Analisis teknikal adalah metode evaluasi sekuritas melalui analisis statistik yang dihasilkan oleh aktivitas pasar, seperti harga historis dan volume perdagangan [7]. Berdasarkan buku acuan klasik oleh John J. Murphy (1999) [7], data deret waktu harga transaksi harian direpresentasikan dalam format OHLCV (*Open, High, Low, Close, Volume*). Indikator-indikator teknikal utama yang digunakan dalam sistem ini meliputi:
1. **Simple Moving Average (SMA):** Rata-rata aritmatika dari harga penutupan selama periode waktu tertentu $N$:
   $$\text{SMA}_t = \frac{1}{N} \sum_{i=0}^{N-1} \text{Close}_{t-i}$$
   Sistem memanfaatkan perpotongan antara SMA jangka pendek (SMA-20) dan jangka menengah (SMA-50) untuk mendeteksi arah tren.
2. **Relative Strength Index (RSI):** Indikator osilator momentum yang mengukur kecepatan dan perubahan pergerakan harga dalam rentang 0 hingga 100:
   $$\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right), \quad \text{di mana } \text{RS} = \frac{\text{Rata-rata Keuntungan } N \text{ hari}}{\text{Rata-rata Kerugian } N \text{ hari}}$$
   Nilai RSI di atas 70 mengindikasikan kondisi jenuh beli (*overbought*), sedangkan di bawah 30 mengindikasikan kondisi jenuh jual (*oversold*) [7].
3. **Moving Average Convergence Divergence (MACD):** Indikator momentum yang mengikuti tren, dihitung dari selisih *Exponential Moving Average* (EMA) 12-hari dan 26-hari:
   $$\text{MACD Line} = \text{EMA}_{12}(\text{Close}) - \text{EMA}_{26}(\text{Close})$$
   $$\text{Signal Line} = \text{EMA}_{9}(\text{MACD Line})$$
   $$\text{Histogram} = \text{MACD Line} - \text{Signal Line}$$
4. **Bollinger Bands:** Indikator volatilitas yang terdiri dari pita tengah ($\text{SMA}_{20}$) serta pita atas dan pita bawah yang berjarak dua kali deviasi standar ($\sigma$) dari pita tengah [7]:
   $$\text{Upper Band} = \text{SMA}_{20} + 2\sigma, \quad \text{Lower Band} = \text{SMA}_{20} - 2\sigma$$

### 2.2.2 Analisis Fundamental
Analisis fundamental berfokus pada penilaian kesehatan keuangan perusahaan dan kemampuan operasionalnya untuk menghasilkan laba di masa depan [8]. Berdasarkan kerangka kerja valuasi Aswath Damodaran (2012) [8], indikator fundamental perbankan mencakup:
* **Price-to-Earnings Ratio (PER):** Rasio harga saham terhadap laba bersih per lembar saham (*Earnings Per Share* / EPS), mengukur seberapa mahal pasar menilai potensi laba emiten.
* **Price-to-Book Value (PBV):** Rasio harga pasar terhadap nilai buku ekuitas per lembar saham. Dalam industri perbankan di mana aset didominasi oleh instrumen likuid dan kas, PBV merupakan metrik valuasi paling esensial.
* **Return on Equity (ROE):** Mengukur efisiensi manajemen perbankan dalam menghasilkan laba bersih dari modal ekuitas pemegang saham.

### 2.2.3 Analisis Sentimen dan Teks Berita Finansial
Sentimen pasar mencerminkan sikap psikologis agregat dari para pelaku pasar terhadap suatu aset. Penelitian penting oleh Loughran dan McDonald (2011) dalam *The Journal of Finance* membuktikan bahwa analisis linguistik pada dokumen keuangan memiliki korelasi langsung terhadap pergerakan harga saham dan volatilitas pasar [11]. Penelitian tersebut menegaskan bahwa teks finansial memiliki karakteristik unik, di mana kata-kata umum dalam kamus bahasa sehari-hari sering kali memiliki konotasi berbeda saat diterapkan pada konteks pasar modal [11]. Oleh karena itu, kemampuan LLM dalam memahami makna semantik konteks (*contextual semantic*) menjadi keunggulan utama dalam mengekstrak sinyal sentimen dari judul-judul berita pasar terkini.

---

## 2.3 Arsitektur Large Language Model (LLM) & Mekanisme Perhatian
*Large Language Model* modern dibangun di atas arsitektur *Transformer* yang pertama kali diperkenalkan oleh Vaswani et al. (2017) melalui paper monumental *"Attention Is All You Need"* [3]. Berbeda dengan model *Recurrent Neural Network* (RNN) terdahulu yang memproses teks secara sekuensial langkah demi langkah, Transformer mengandalkan mekanisme perhatian penuh (*Self-Attention*) yang memungkinkan pemrosesan token secara paralel di seluruh jendela konteks teks [3].

Proses komputasi LLM diawali dengan tahap tokenisasi, di mana teks dipecah menjadi unit-unit token diskret dan dipetakan ke dalam vektor ruang dimensi tinggi (*Embedding*). Inti matematis dari mekanisme Transformer terletak pada fungsi *Scaled Dot-Product Attention*, yang dinyatakan pada Persamaan (2.1) [3]:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V \tag{2.1}$$

di mana $Q$ adalah matriks *Query* (informasi yang dicari), $K$ adalah matriks *Key* (label informasi yang tersedia), $V$ adalah matriks *Value* (kandungan semantik informasi), dan $d_k$ merepresentasikan dimensi vektor dari *Key* yang bertindak sebagai faktor penskalaan (*scaling factor*) untuk mencegah lenyapnya gradien (*vanishing gradient*) pada fungsi *softmax* [3].

Mekanisme ini diperluas menjadi *Multi-Head Attention*, di mana komputasi perhatian diproyeksikan ke dalam beberapa sub-ruang representasi yang berbeda secara paralel. Setiap *head* mampu menangkap korelasi linguistik yang berbeda (misalnya hubungan antara entitas korporasi, metrik angka laba, dan sentimen kebijakan moneter). Hasil komputasi kemudian distabilkan melalui normalisasi lapisan (*Layer Normalization*) guna menjamin koherensi generasi teks [3].

Dalam proses inferensi, salah satu hiperparameter pengendali perilaku model yang paling kritis adalah *Temperature*. Nilai *temperature* mendekati 0.0 menghasilkan distribusi probabilitas token yang sangat tajam (deterministik dan konsisten), ideal untuk tugas pelaporan data faktual. Sebaliknya, *temperature* yang lebih tinggi (misalnya 0.7) menghasilkan variasi teks yang lebih luas dan eksploratif, sangat sesuai untuk skenario perdebatan argumen dan pencarian sudut pandang risiko [1].

---

## 2.4 Sistem Multi-Agen (MAS) & Prinsip Pemisahan Tugas
Penerapan satu model AI raksasa (*monolithic single-agent*) untuk menangani seluruh rantai analisis finansial terbukti menimbulkan degradasi performa (*prompt degradation*) akibat tumpang tindih instruksi yang berlebihan [5]. Untuk mengatasi kendala ini, Hong et al. (2023) dalam paper *MetaGPT* memperkenalkan prinsip *Separation of Concerns* (pemisahan tanggung jawab) ke dalam kerangka kerja *Multi-Agent Systems* (MAS) [5]. Dalam pendekatan ini, model AI dibagi ke dalam beberapa agen mandiri, di mana setiap agen diberikan definisi peran (*persona*), batasan lingkup tugas, dan prosedur operasi standar (*Standard Operating Procedures* / SOP) yang tegas [5].

Selaras dengan hal tersebut, Yu et al. (2024) melalui penelitian *FinCon* membuktikan bahwa efisiensi pengambilan keputusan finansial meningkat drastis ketika sistem mengadopsi hierarki komunikasi verbal berjenjang [4]. Alih-alih mentransfer seluruh tumpukan data mentah dari satu agen ke agen lain, sistem MAS yang efisien merangkum data menjadi sintesis informasi tingkat tinggi (*executive summary*), meniru struktur komando firma investasi profesional di mana staf analis menyerahkan ringkasan temuan kepada manajer portofolio [4].

---

## 2.5 Teori AI Safety via Debate & Mitigasi Overconfidence
Secara fundamental, LLM dioptimasi untuk memprediksi token berikutnya berdasarkan pola probabilitas bahasa, sehingga rentan menghasilkan pernyataan yang terdengar sangat meyakinkan namun salah secara faktual (*hallucinatory overconfidence*). Dalam lingkungan pasar modal yang stokastik dan penuh ketidakpastian, bias *overconfidence* dapat berakibat fatal pada alokasi modal portofolio [6].

Sebagai landasan teoretis untuk memitigasi bias tersebut, Irving et al. (2018) dari Google DeepMind merumuskan paradigma *AI Safety via Debate* [2]. Teori ini membuktikan secara formal bahwa jika dua agen AI ditempatkan dalam skenario permainan *zero-sum* di mana masing-masing agen diprogram untuk mempertahankan sudut pandang yang saling berlawanan (*adversarial*), agen-agen tersebut secara rasional terdorong untuk mengekspos kelemahan, celah logika, dan asumsi tidak berdasar dari argumen lawannya [2]. Melalui proses kontradiksi ini, seorang juri atau fasilitator pihak ketiga yang netral dapat mengevaluasi fakta yang tersisa secara jauh lebih mudah dan objektif dibanding mendengarkan monolog satu agen [2].

Konsep debat adversarial ini dibuktikan secara empiris dalam domain keuangan oleh Cai et al. (2025) melalui kerangka kerja *FinDebate* [6]. Penelitian tersebut menunjukkan bahwa agen AI yang dipaksa berdebat antara perspektif optimis (*Bullish*) dan pesimis (*Bearish*) menghasilkan kalibrasi keyakinan (*confidence calibration*) yang jauh lebih akurat, secara signifikan menekan angka transaksi ceroboh, serta menghasilkan imbal hasil portofolio yang lebih stabil terhadap guncangan pasar (*market volatility*) [6].

---

## 2.6 Prinsip Pencegahan Look-Ahead Bias pada Perdagangan Kuantitatif
Dalam rekayasa algoritma perdagangan kuantitatif, *Look-Ahead Bias* (atau kebocoran data temporal) didefinisikan sebagai penggunaan informasi masa depan secara tidak sah pada titik waktu simulasi masa lalu [1]. Contoh bias ini meliputi penggunaan harga penutupan hari esok untuk menghitung sinyal hari ini, atau pembacaan berita yang baru terbit pada hari Sabtu untuk mensimulasikan keputusan investasi hari Jumat.

Secara formal, jika simulasi perdagangan dieksekusi pada stempel waktu $T_{\text{sim}}$, maka himpunan informasi yang diizinkan untuk dikonsumsi oleh seluruh modul sistem, $\mathcal{I}_{\text{valid}}$, harus memenuhi batasan ketat:
$$\mathcal{I}_{\text{valid}} = \{ x \in \mathcal{D} \mid t(x) \le T_{\text{sim}} \}$$

di mana $t(x)$ merepresentasikan waktu publikasi atau pencatatan resmi dari data $x$. Kegagalan mematuhi batasan ini menyebabkan sistem menghasilkan performa simulasi yang luar biasa tinggi (*overfitted*), namun mengalami kerugian telak saat diuji pada perdagangan langsung (*live forward testing*) [1]. Oleh karena itu, penerapan mekanisme pemotongan data (*time-slicing*) berbasis kode yang deterministik menjadi syarat mutlak dalam validitas penelitian kuantitatif.

---

## 2.7 Penelitian Terkait (*State of the Art*) & Posisi Penelitian
Penelitian mengenai penerapan kecerdasan artifisial pada pasar modal telah berkembang pesat. Xiao et al. (2024) memperkenalkan *TradingAgents*, sebuah kerangka kerja multi-agen LLM yang membagi sistem ke dalam tim analis teknikal/fundamental, peneliti pasar, manajer risiko, dan eksekutor transaksi untuk pasar saham Amerika Serikat [1]. Meskipun demikian, penelitian tersebut belum mengintegrasikan mekanisme penarikan berita real-time multi-sumber secara otomatis dan belum menguji efektivitas sistem pada pasar modal negara berkembang seperti Indonesia.

Tabel 2.1 menyajikan pemetaan posisi penelitian terdahulu yang relevan, sedangkan Tabel 2.2 merangkum matriks perbandingan fitur antara penelitian-penelitian kunci tersebut dengan penelitian yang diusulkan dalam tugas akhir ini.

**Tabel 2.1. State of the art dan posisi penelitian ini**
| Peneliti & Tahun | Platform / Model | Komponen / Arsitektur | Fokus Evaluasi |
|:---|:---|:---|:---|
| **Xiao et al. (2024) [1]** | LLM Multi-Agent (*TradingAgents*) | Tim Analis, Riset, Manajer Risiko, Trader | Evaluasi performa perdagangan saham US market dan studi ablasi (*ablation study*) komponen agen. |
| **Irving et al. (2018) [2]** | Teori AI Safety (*Debate Framework*) | Dua agen pendebat adversarial dan satu agen juri/evaluator | Pembuktian teoretis bahwa debat AI membatasi halusinasi dan meningkatkan transparansi kejujuran model. |
| **Vaswani et al. (2017) [3]** | Arsitektur Transformer | *Multi-Head Attention*, *LayerNorm*, *Feed Forward* | Fondasi komputasi representasi bahasa dan mekanisme perhatian skalar pada *deep learning*. |
| **Yu et al. (2024) [4]** | LLM Multi-Agent (*FinCon*) | Agen hierarkis analis dan *verbal reinforcement manager* | Evaluasi efisiensi komunikasi berjenjang dan pemangkasan konteks pada keputusan finansial. |
| **Hong et al. (2023) [5]** | Multi-Agent Framework (*MetaGPT*) | SOP berbasis peran, *Separation of Concerns* | Pengurangan distorsi konteks pada rekayasa perangkat lunak multi-agen kolaboratif. |
| **Cai et al. (2025) [6]** | Multi-Agent System (*FinDebate*) | Mekanisme debat adversarial *Bullish vs Bearish* | Mitigasi bias *overconfidence* pada analisis portofolio keuangan dan saham global. |
| **Penelitian Ini** | LangGraph DAG Multi-Agent (12 Node) | Pipeline Data Anti-Bias, 4 Tim Agen, Debat Adversarial, Konsensus Risiko | Integrasi pipeline data otomatis bebas *look-ahead bias*, orkestrasi 12 agen via DAG, evaluasi saham perbankan IHSG. |

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

Berdasarkan Tabel 2.2, kebaruan (*novelty*) dan posisi penelitian ini terletak pada integrasi menyeluruh antara kerangka kerja orkestrasi 12-agen berbasis DAG, penerapan mekanisme debat adversarial simultan dengan evaluasi risiko ganda, serta penerapan pipeline *data ingestion* bebas *look-ahead bias* yang dikalibrasi khusus untuk dinamika pasar saham perbankan di Indonesia.

---

# BAB 3
# METODOLOGI DAN PERANCANGAN SISTEM

## 3.1 Tujuan dan Ruang Lingkup Perancangan Sistem
### 3.1.1 Tujuan Perancangan Sistem
Tujuan perancangan sistem ini adalah menghasilkan sebuah arsitektur perangkat lunak perdagangan saham kuantitatif otonom yang terintegrasi, transparan, dan dapat diandalkan secara empiris. Sistem dirancang untuk mampu mengumpulkan data pasar modal secara mandiri dari internet, memproses dan menyaring informasi tanpa kebocoran waktu masa depan, serta mendistribusikan data tersebut ke dalam graf orkestrasi 12 agen LLM guna menghasilkan rekomendasi investasi yang dilengkapi jejak audit penalaran (*Explainable AI*).

### 3.1.2 Ruang Lingkup Perancangan Sistem
Ruang lingkup perancangan mencakup pengembangan modul pengumpul data (Yahoo Finance dan RSS feed), otomasi penjadwalan pada sistem operasi, pembersihan data terdistribusi lokal, struktur graf orkestrasi LangGraph, perancangan *prompt* spesialis, hingga antarmuka visualisasi interaktif pengguna berbasis web.

---

## 3.2 Justifikasi Pemilihan Perangkat Lunak dan Alat Bantu Pengujian
Perancangan sistem didukung oleh serangkaian pustaka perangkat lunak dan teknologi yang dipilih berdasarkan justifikasi teknis sebagai berikut:
1. **Python 3.12:** Dipilih sebagai bahasa pemrograman utama karena kestabilan sintaks, efisiensi eksekusi memori, dan ketersediaan ekosistem data kuantitatif yang matang (`pandas`, `numpy`, `yfinance`, `feedparser`).
2. **LangGraph (LangChain Ecosystem):** Dipilih sebagai kerangka kerja orkestrasi multi-agen karena menyediakan abstraksi *StateGraph* yang memungkinkan pembentukan topologi *Directed Acyclic Graph* (DAG) murni secara deterministik, mendukung percabangan paralel (*fan-out/fan-in*), serta memiliki mekanisme *state checkpointing*.
3. **Google Gemini LLM (`gemini-flash-lite-latest`):** Dipilih sebagai penyedia model inferensi bahasa karena menawarkan jendela konteks yang luas, latensi inferensi yang sangat rendah (<2 detik per pemanggilan agen), dan efisiensi biaya komputasi yang tinggi.
4. **Penyimpanan Berkas Terstruktur Lokal (JSON dan CSV):** Sistem memilih format penyimpanan flat file berbasis `master_news.json`, `master_ohlcv.csv`, dan `master_fundamentals.json` dibanding basis data relasional (RDBMS) seperti PostgreSQL. Pendekatan ini memberikan latensi I/O instan (*in-memory loading* satu kali saat eksekusi), tidak memerlukan konfigurasi server basis data eksternal (*zero-configuration*), serta menjamin portabilitas kode yang tinggi saat dipindahkan ke mesin pengujian lain.
5. **Streamlit:** Pustaka visualisasi berbasis web yang digunakan untuk membangun antarmuka interaktif pengguna (*dashboard*) guna menampilkan simulasi debat AI dan performa grafik portofolio secara *real-time*.

---

## 3.3 Perancangan Arsitektur Sistem
### 3.3.1 Gambaran Umum Arsitektur Sistem
Arsitektur global sistem perdagangan multi-agen ini dirancang mengikuti alur kerja komprehensif dari hulu ke hilir yang terbagi ke dalam **7 fase fungsional berurutan**. Seluruh aliran data bergerak secara searah (*unidirectional*) dari kiri ke kanan guna menjamin ketiadaan siklus tak berujung (*infinite loop*).

Ilustrasi rancangan arsitektur global 7 fase disajikan pada **Gambar 3.1**.

```
[GAMBAR 3.1: Diagram Arsitektur Global (High-Level) Sistem Multi-Agent LLM Trading (7 Fase)]
(Memuat representasi visual 7 fase: Fase 1 Sumber Data -> Fase 2 Python Engine -> Fase 3 Prompt & LLM Config -> Fase 4 Otak LLM -> Fase 5 LangGraph DAG 12-Agen -> Fase 6 Output Sistem -> Fase 7 Antarmuka Pengguna Streamlit)
```

Alur kerja arsitektur global 7 fase tersebut dapat diuraikan sebagai berikut:
* **Fase 1 (Sumber Data):** Pengambilan data mentah dari internet meliputi 3 aliran RSS berita (Google News dan CNBC Indonesia) serta 2 endpoint Yahoo Finance API (deret waktu harga harian dan laporan keuangan fundamental).
* **Fase 2 (Python Engine / Pra-Pemrosesan):** Mesin lokal Python bertindak membersihkan data, melakukan normalisasi nama kolom menjadi *lowercase*, menghitung penyangga historis 2 tahun, menyimpan data ke dalam *Local Cache*, serta menghitung 5 kelompok indikator teknikal (MACD, RSI, SMA, Bollinger Bands, KDJ) melalui modul `Indicator Calculator`.
* **Fase 3 (Prompt & LLM Config):** Data hasil pra-pemrosesan dikonversi dan disuntikkan ke dalam templat instruksi sistem (*system prompt templates*). Di fase ini, konfigurasi hiperparameter ditetapkan, khususnya pemisahan nilai *Temperature* (0.0 untuk pelaporan faktual analis dan 0.7 untuk perdebatan kreatif).
* **Fase 4 (Otak LLM):** Paket instruksi dikirim ke server model bahasa (Google Gemini) untuk diproses melalui komputasi internal Transformer: pemecahan token, vektorisasi *embedding*, komputasi *Multi-Head Self-Attention*, dan normalisasi lapisan (*LayerNorm*).
* **Fase 5 (Orkestrasi 12-Agen LangGraph DAG):** Inti dari sistem di mana 12 agen AI dieksekusi dalam topologi DAG terstruktur yang terbagi ke dalam 4 tim (Analis, Peneliti Debat, Manajemen Risiko, dan Eksekutor) dengan koordinasi memori bersama `TradingState`.
* **Fase 6 (Output Sistem):** Sistem mengekstraksi hasil kerja agen dari `TradingState` dan menghasilkan dua berkas luaran utama: berkas catatan penalaran eksplisit (*Reasoning Log* dalam format `.txt` sebagai wujud *Explainable AI*) dan keputusan transaksi terstruktur dalam format JSON (`action`, `quantity`, `confidence`).
* **Fase 7 (Antarmuka Pengguna):** Dashboard visual berbasis Streamlit yang menyajikan visualisasi jalannya perdebatan AI secara *streaming* pada Tab 1 (*Live AI Debate*) dan visualisasi grafik performa portofolio serta grafik *candlestick* pada Tab 2 (*Backtest Charts*).

### 3.3.2 Komponen dan Peran Sistem
Rincian komponen fungsional yang terlibat di setiap fase arsitektur sistem dirangkum pada **Tabel 3.1**.

**Tabel 3.1. Pemetaan komponen utama, fase arsitektur, dan perannya dalam sistem**
| Fase | Komponen Layanan | Peran dan Tanggung Jawab Utama |
|:---:|:---|:---|
| **Fase 1** | Yahoo Finance API, Google News RSS, CNBC Indonesia RSS | Menyediakan asupan data mentah eksternal dari pasar modal (angka transaksi, fundamental, dan teks berita). |
| **Fase 2** | `tools/data_fetcher.py`, `tools/news_fetcher.py`, `tools/indicator_calculator.py` | Ekstraksi data, kalkulasi buffer historis, pembersihan noise, kalkulasi indikator matematika, dan penyimpanan master cache. |
| **Fase 3** | `config/prompts/`, `config/llm_config.py` | Standarisasi persona agen, penyuntikan konteks data ke prompt, dan manajemen hiperparameter *temperature*. |
| **Fase 4** | Model Bahasa Google Gemini (`gemini-flash-lite-latest`) | Eksekusi inferensi representasi semantik bahasa, evaluasi konteks via *Self-Attention*, dan generasi respons teks. |
| **Fase 5** | `orchestration/graph.py`, `orchestration/state.py` | Orkestrasi graf eksekusi DAG 12 agen, sinkronisasi transfer memori estafet, mitigasi konflik konkuren via Reducer. |
| **Fase 6** | `orchestration/backtester.py` (Output Formatter) | Penyusunan log audit penalaran (*Explainable AI*) dan generasi perintah eksekusi JSON terstandarisasi. |
| **Fase 7** | Antarmuka Pengguna Streamlit (`main.py` / Web UI) | Penyajian dashboard interaktif hasil debat AI dan visualisasi kurva evaluasi portofolio investasi. |

---

## 3.4 Perancangan Pipeline Data Ingestion & Mitigasi Bias
Pipeline *data ingestion* merupakan fondasi integritas empiris sistem. Perancangan pipeline ini disajikan secara mendalam melalui **Gambar 3.2**, yang menggambarkan interaksi 6 lapisan fungsional data dari dunia luar hingga siap dikonsumsi oleh agen analis.

```
[GAMBAR 3.2: Diagram Arsitektur Pipeline Data Ingestion & Data Sources]
(Memuat 6 lapisan: Lapisan 1 Sumber Eksternal -> Lapisan 2 Otomasi Scheduler -> Lapisan 3 Python Extraction & Pre-Processing -> Lapisan 4 Master Cache Lokal -> Lapisan 5 Runtime Time-Slicing -> Lapisan 6 Konsumsi Agen AI)
```

Rincian perancangan pada setiap lapisan dalam pipeline *data ingestion* adalah sebagai berikut:

### 3.4.1 Sumber Data Eksternal (Lapisan 1)
Sistem mengakuisisi 5 sumber data mentah internet yang dikelompokkan ke dalam 2 domain:
* **Domain Kualitatif (Teks Berita):**
  1. *Google News RSS Query* `'{ticker} saham'`: Menarik artikel spesifik mikro emiten (misal: kinerja laba BBRI, aksi korporasi BMRI).
  2. *Google News RSS Query* `'suku bunga BI OJK'`: Menarik berita makroekonomi nasional yang berdampak sistemik pada sektor perbankan.
  3. *CNBC Indonesia RSS Market Feed*: Menarik sentimen umum pasar modal dan dinamika arus modal asing di IHSG.
* **Domain Kuantitatif (Numerik Yahoo Finance):**
  4. *OHLCV Daily Historical*: Deret waktu harga transaksi harian 5 kolom standar pasar modal.
  5. *Fundamental Endpoints*: Snapshot metrik valuasi (P/E, P/B), neraca keuangan, dan laporan laba rugi.

### 3.4.2 Otomasi Penjadwal & Jejak Audit (Lapisan 2)
Untuk menjamin pengumpulan data berita berjalan secara konsisten tanpa intervensi manual, dibangun rantai otomasi sistem:
* **Windows Task Scheduler:** Dikonfigurasi untuk mengeksekusi tugas setiap hari pukul 11:00 WIB. Parameter `StartWhenAvailable` diaktifkan guna memastikan jika perangkat laptop dalam keadaan mati pada jam yang ditentukan, tugas akan langsung dijalankan secara otomatis saat perangkat dinyalakan kembali.
* **`run_collector.vbs`:** Skrip VBScript yang memanggil batch file (`run_collector.bat`) dengan parameter jendela tersembunyi (`0`), memungkinkan seluruh proses pengumpulan data berjalan sepenuhnya di latar belakang (*headless background*) tanpa mengganggu aktivitas pengguna.
* **`daily_news_collector.py`:** Skrip orkestrator yang mengulang proses penarikan berita untuk kelima emiten bank secara berurutan.
* **`scripts/collector_log.txt`:** Berkas audit jejak operasional yang mencatat stempel waktu eksekusi, jumlah artikel baru yang tersaring, total akumulasi arsip bersih, serta status keberhasilan proses.

### 3.4.3 Pra-Pemrosesan Data Python (Lapisan 3)
Modul ekstraksi Python mengimplementasikan algoritma pembersihan data yang ketat:
* **`NewsFetcher` (`tools/news_fetcher.py`):**
  * *Negative Keyword Filter:* Menyaring dan mengeliminasi artikel yang memuat kata kunci sampah seperti *"cara beli"*, *"panduan pemula"*, dan *"pembobolan ATM"*, sehingga hanya berita bernilai finansial material yang dipertahankan.
  * *Incremental Append & Deduplication:* Membaca arsip berita lama di *cache*, mengevaluasi judul berita baru menggunakan struktur data `set()`, dan hanya menambahkan artikel yang belum pernah tersimpan sebelumnya guna mencegah duplikasi.
* **`YFinanceFetcher` (`tools/data_fetcher.py`):**
  * *2-Year Historical Buffer:* Menambahkan rentang mundur 2 tahun secara otomatis dari tanggal awal simulasi agar indikator berperiode panjang (seperti SMA-200) memiliki data historis yang memadai tanpa menghasilkan nilai *NaN*.
  * *Lowercase Column Normalization:* Menormalisasi seluruh nama kolom menjadi huruf kecil (`open, high, low, close, volume`) agar kompatibel dengan pustaka komputasi kuantitatif.

### 3.4.4 Struktur Master Cache Lokal (Lapisan 4)
Data bersih disimpan secara terisolasi per folder emiten pada `data/cache/{ticker}/` dalam 3 berkas master:
1. `master_news.json`: Berisi arsip berita bersih dengan skema terstruktur `[{title, link, published, source}]`.
2. `master_ohlcv.csv`: Berisi matriks deret waktu harga transaksi harian lengkap.
3. `master_fundamentals.json`: Berisi potret metrik valuasi dan laporan keuangan emiten.

### 3.4.5 Perancangan Runtime Time-Slicing & Pencegahan Bias (Lapisan 5)
Saat simulasi *backtesting* dijalankan, ketiga file master dimuat ke memori (RAM) satu kali di awal (*one-shot loading*). Pada setiap iterasi mingguan hari Jumat ($T_{\text{sim}}$), mesin `Backtester Engine` memotong data secara temporal:
* **Time-Slicing Data Harga:** Hanya data baris di mana tanggal baris $t \le T_{\text{sim}}$ yang diizinkan masuk ke kalkulasi indikator teknikal. Data masa depan dibuang dari memori perhitungan.
* **Time-Slicing Berita:** Mengimplementasikan jendela potong temporal ketat:
  $$T_{\text{sim}} - 7 \text{ hari} \le t_{\text{published}} \le T_{\text{sim}}$$
  Berita yang terbit setelah hari simulasi (masa depan) dieliminasi 100% untuk menjamin *Zero Look-Ahead Bias*. Berita yang terbit lebih dari 7 hari sebelum simulasi dieliminasi agar analisis sentimen tetap berfokus pada informasi paling relevan dan terhindar dari *noise* masa lalu.

---

## 3.5 Perancangan Topologi & Orkestrasi Multi-Agent (LangGraph DAG)
Lapisan kecerdasan buatan sistem diorganisasikan ke dalam sebuah struktur graf berarah tanpa siklus (*Directed Acyclic Graph* / DAG) menggunakan kerangka kerja LangGraph. Arsitektur orkestrasi 12 agen AI disajikan secara terperinci pada **Gambar 3.3**.

```
[GAMBAR 3.3: Diagram Topologi Directed Acyclic Graph (DAG) — Orkestrasi 12 Agen AI via LangGraph]
(Memuat 4 tim berjenjang: Tim Analis 4 Agen Paralel -> Tim Peneliti Debat Adversarial 3 Agen -> Tim Manajemen Risiko 3 Agen -> Tim Eksekusi 2 Agen, ditopang oleh memori estafet TradingState)
```

Struktur dan mekanisme kerja ke-12 agen dikelompokkan ke dalam 4 tingkatan hierarkis sebagai berikut:

### 3.5.1 Komponen Fondasi: TradingState & Reducer
Tulang punggung komunikasi antar-agen adalah objek data terstruktur bertipe `TypedDict` yang dinamakan `TradingState`. Objek ini bertindak sebagai papan memori bersama yang dioper secara estafet dari satu tim ke tim berikutnya.
Untuk menangani situasi di mana beberapa agen mengeksekusi komputasi secara bersamaan (paralel), LangGraph dikonfigurasi dengan fungsi operator **Reducer**:
```python
def merge_reports(current: dict, update: dict) -> dict:
    current.update(update)
    return current
```
Operator ini menjamin bahwa tulisan dari masing-masing agen paralel digabungkan secara aman ke dalam *state* tanpa saling menimpa (*non-destructive merge*).

### 3.5.2 Tim 1: Analis Spesialis (4 Agen Bekerja Paralel)
Tim Analis adalah titik kontak pertama yang membaca data hasil *time-slicing*. Keempat analis dieksekusi secara serentak guna mengoptimalkan kecepatan komputasi:
1. **Fundamental Analyst:** Membaca `master_fundamentals.json` untuk mengevaluasi rasio valuasi (P/E, P/B, ROE) dan solvabilitas perusahaan.
2. **Technical Analyst:** Membaca `master_ohlcv.csv` dan kalkulasi indikator matematika (RSI, MACD, SMA, Bollinger Bands, KDJ) untuk menentukan momentum dan level support/resistance.
3. **Sentiment Analyst:** Membaca kumpulan judul berita spesifik emiten dari `master_news.json` hasil *time-slicing* untuk mengekstrak sentimen pasar jangka pendek.
4. **Macro Analyst:** Membaca judul berita kebijakan makroekonomi (BI-Rate, regulasi OJK) untuk menilai iklim moneter perbankan.

*Prinsip Desain Executive Summary:* Setiap analis diwajibkan memadatkan analisisnya menjadi **laporan ringkas maksimal 3 kalimat** (total ~12 kalimat dari keempat analis). Pembatasan ini krusial untuk mencegah kelebihan muatan konteks (*context explosion*) pada agen di lapisan berikutnya.

### 3.5.3 Tim 2: Peneliti (Sintesis melalui Debat Adversarial)
Tim Peneliti membaca laporan ringkas dari Tim Analis dan mengimplementasikan mekanisme debat adversarial [2], [6]:
1. **Bullish Researcher:** Diberikan persona optimis untuk membangun argumen terkuat mengapa saham layak dibeli (*BUY*), menonjolkan seluruh katalis positif.
2. **Bearish Researcher:** Diberikan persona skeptis untuk membangun argumen tandingan terkuat mengapa saham harus dijual atau dihindari (*SELL/AVOID*), mengidentifikasi risiko penurunan tersembunyi.
3. **Research Facilitator:** Bertindak sebagai evaluator netral yang menimbang keabsahan bukti dari kedua kubu dan merumuskan dokumen kesimpulan tunggal: **Research Consensus** (3–5 kalimat).

### 3.5.4 Tim 3: Manajemen Risiko (Evaluasi Dua Perspektif Risiko)
Tim Manajemen Risiko membaca *Research Consensus* dan mengevaluasi kelayakan transaksi dari dimensi pelestarian modal:
1. **Aggressive Risk Analyst:** Mengevaluasi potensi imbal hasil maksimal dan mendorong alokasi modal yang lebih agresif.
2. **Conservative Risk Analyst:** Mengevaluasi potensi risiko terburuk (*drawdown*) dan mendorong perlindungan modal atau pembatasan posisi.
3. **Risk Facilitator:** Menyelaraskan kedua rekomendasi risiko untuk menetapkan **Risk Consensus** yang memuat batas toleransi kerugian (*stop-loss*) dan panduan alokasi ukuran posisi (*position sizing*).

### 3.5.5 Tim 4: Eksekusi (Pengambilan Keputusan Akhir)
Puncak rantai hierarki dijalankan oleh dua agen eksekusi:
1. **Portfolio Manager (PM):** Bertindak sebagai pengambil keputusan tertinggi (*supreme judge*). PM membaca *Research Consensus*, *Risk Consensus*, dan status saldo kas saat ini untuk menetapkan keputusan akhir (*BUY, SELL, atau HOLD*) serta tingkat keyakinan (*confidence score* antara 0.0 hingga 1.0).
2. **Trading Agent:** Mengonversi instruksi keputusan bahasa alami dari PM menjadi format data JSON terstruktur, melakukan penyesuaian terhadap satuan 1 lot = 100 lembar sesuai aturan BEI [9], serta memperhitungkan potongan biaya broker 0,2%.

Format luaran JSON standar yang dihasilkan didefinisikan sebagai berikut:
```json
{
  "action": "BUY",
  "quantity": 500,
  "confidence": 0.85
}
```

### 3.5.6 Perancangan Prompt Persona & Konfigurasi Inferensi
Pengaturan hiperparameter model disesuaikan dengan karakteristik tugas masing-masing agen, seperti dirangkum pada **Tabel 3.2**.

**Tabel 3.2. Pemetaan persona agen, nilai temperature, dan sumber konteks input**
| No | Nama Agen | Peran / Tim | Temperature | Sumber Konteks Input Data |
|:---:|:---|:---|:---:|:---|
| 1 | Fundamental Analyst | Tim 1 (Analis) | 0.0 | Snapshot `master_fundamentals.json` |
| 2 | Technical Analyst | Tim 1 (Analis) | 0.0 | Metrik indikator teknikal dari `master_ohlcv.csv` |
| 3 | Sentiment Analyst | Tim 1 (Analis) | 0.0 | Judul berita mikro emiten hasil *time-slicing* |
| 4 | Macro Analyst | Tim 1 (Analis) | 0.0 | Judul berita makroekonomi hasil *time-slicing* |
| 5 | Bullish Researcher | Tim 2 (Peneliti) | 0.7 | 4 laporan analis (mencari sinyal beli) |
| 6 | Bearish Researcher | Tim 2 (Peneliti) | 0.7 | 4 laporan analis (mencari sinyal risiko/jual) |
| 7 | Research Facilitator | Tim 2 (Peneliti) | 0.0 | Transkrip perdebatan Bullish vs Bearish |
| 8 | Aggressive Risk Analyst | Tim 3 (Risiko) | 0.7 | *Research Consensus* (orientasi profit) |
| 9 | Conservative Risk Analyst | Tim 3 (Risiko) | 0.7 | *Research Consensus* (orientasi proteksi modal) |
| 10 | Risk Facilitator | Tim 3 (Risiko) | 0.0 | Rekomendasi Aggressive vs Conservative |
| 11 | Portfolio Manager | Tim 4 (Eksekusi) | 0.0 | *Research Consensus* + *Risk Consensus* + Kas |
| 12 | Trading Agent | Tim 4 (Eksekusi) | 0.0 | Keputusan PM + Aturan Fraksi Lot BEI |

---

## 3.6 Perancangan Skenario Pengujian dan Evaluasi
Untuk membuktikan keandalan sistem pada Bab 4 mendatang, metodologi pengujian dirancang mencakup dua skenario eksperimen utama serta penetapan metrik evaluasi baku:

### 3.6.1 Skenario Pengujian 1: Simulasi Backtesting Utama Multi-Bank
* **Subjek Uji:** 5 saham perbankan (BBRI.JK, BBCA.JK, BMRI.JK, BBNI.JK, BRIS.JK).
* **Modal Awal Simulasi:** Rp 100.000.000 (seratus juta rupiah) dialokasikan per emiten.
* **Biaya Transaksi:** 0,2% dikenakan pada setiap nilai transaksi beli dan jual (mencakup komisi broker dan pajak transaksi bursa) [9].
* **Frekuensi Transaksi:** Keputusan mingguan pada hari Jumat penutupan bursa.
* **Strategi Baseline Pembanding:** Performa sistem 12-agen akan dibandingkan terhadap tiga strategi patokan:
  1. *Buy and Hold Strategy:* Membeli saham di awal periode simulasi dan menyimpannya hingga akhir periode.
  2. *SMA Crossover Strategy:* Strategi kuantitatif konvensional berbasis sinyal beli saat SMA-20 memotong ke atas SMA-50 (*Golden Cross*) dan sinyal jual saat memotong ke bawah (*Death Cross*).
  3. *MACD Strategy:* Strategi beli saat garis MACD memotong ke atas garis sinyal dan jual saat memotong ke bawah.

### 3.6.2 Skenario Pengujian 2: Studi Ablasi (Ablation Study)
Guna membuktikan kontribusi ilmiah dari mekanisme debat adversarial dan manajemen risiko ganda, dirancang pengujian komparatif terhadap 3 varian konfigurasi arsitektur sistem (mengadopsi metodologi Xiao et al. [1]):
1. **Konfigurasi A (12-Agen Lengkap):** Sistem usulan lengkap (4 Analis $\rightarrow$ Debat Adversarial $\rightarrow$ Manajemen Risiko $\rightarrow$ Eksekusi).
2. **Konfigurasi B (8-Agen Tanpa Debat):** Sistem tanpa Tim Peneliti Debat (4 Analis $\rightarrow$ langsung menuju Tim Manajemen Risiko $\rightarrow$ Eksekusi).
3. **Konfigurasi C (Single-Agent Baseline):** Satu agen LLM tunggal yang menerima seluruh data mentah dan langsung mengeluarkan keputusan transaksi.

### 3.6.3 Metrik Evaluasi Kinerja Finansial
Evaluasi performa portofolio dihitung secara kuantitatif menggunakan persamaan-persamaan standar manajemen investasi:
1. **Cumulative Return ($R_{\text{cum}}$):** Persentase total pertumbuhan nilai portofolio dari awal hingga akhir periode simulasi:
   $$R_{\text{cum}} = \frac{V_{\text{akhir}} - V_{\text{awal}}}{V_{\text{awal}}} \times 100\% \tag{3.1}$$
   di mana $V_{\text{awal}}$ adalah modal awal dan $V_{\text{akhir}}$ adalah nilai total aset (kas ditambah nilai pasar saham) pada akhir simulasi.
2. **Sharpe Ratio ($S$):** Mengukur efisiensi imbal hasil portofolio terhadap risiko volatilitas:
   $$S = \frac{\bar{R}_p - R_f}{\sigma_p} \tag{3.2}$$
   di mana $\bar{R}_p$ adalah rata-rata imbal hasil portofolio, $R_f$ adalah tingkat suku bunga bebas risiko (mengacu pada suku bunga acuan BI-Rate), dan $\sigma_p$ adalah deviasi standar dari imbal hasil portofolio.
3. **Maximum Drawdown (MDD):** Mengukur persentase penurunan terbesar portofolio dari titik puncak (*peak*) tertinggi ke titik terendah (*trough*) sebelum puncak baru terbentuk:
   $$\text{MDD} = \max_{t} \left( \frac{\text{Peak}_t - V_t}{\text{Peak}_t} \right) \times 100\% \tag{3.3}$$
4. **Win Rate ($W$):** Mengukur rasio efektivitas transaksi yang menghasilkan keuntungan terhadap total transaksi tertutup:
   $$W = \frac{N_{\text{profit}}}{N_{\text{total}}} \times 100\% \tag{3.4}$$

Melalui perancangan metodologi yang komprehensif ini, seluruh proses pengujian pada Bab 4 dipastikan memiliki landasan komparasi yang adil, saintifik, dan bebas dari bias interpretasi subjektif.

---

# DAFTAR REFERENSI

[1] H. Xiao, D. S. Wang, Y. Zhang, M. Zhou, and P. Tang, "TradingAgents: Multi-Agents LLM Financial Trading Framework," *arXiv preprint arXiv:2412.20138*, 2024. [Online]. Available: https://arxiv.org/abs/2412.20138

[2] G. Irving, P. Christiano, and D. Amodei, "AI Safety via Debate," *arXiv preprint arXiv:1805.00899*, 2018. [Online]. Available: https://arxiv.org/abs/1805.00899

[3] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS 2017)*, vol. 30, Long Beach, CA, USA, 2017. [Online]. Available: https://arxiv.org/abs/1706.03762

[4] X. Yu, Z. Chen, Y. Ling, S. Dong, Z. Liu, and J. Lu, "FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making," *arXiv preprint arXiv:2407.06567*, 2024. [Online]. Available: https://arxiv.org/abs/2407.06567

[5] S. Hong, M. Zhuge, J. Chen, X. Zheng, C. Cheng, C. Zhang, J. Wang, S. Wang, Z. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Qin, "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," *arXiv preprint arXiv:2308.00352*, 2023. [Online]. Available: https://arxiv.org/abs/2308.00352

[6] Y. Cai, Y. Lin, C. Ding, and Y. Feng, "FinDebate: Multi-Agent Collaborative Intelligence for Financial Analysis," *arXiv preprint arXiv:2509.17395*, 2025. [Online]. Available: https://arxiv.org/abs/2509.17395

[7] J. J. Murphy, *Technical Analysis of the Financial Markets: A Comprehensive Guide to Trading Methods and Applications*. New York, NY, USA: New York Institute of Finance, 1999. [Online]. Available: https://archive.org/details/technicalanalysi0000murp

[8] A. Damodaran, *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset*, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2012. [Online]. Available: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/vltnBK/InvVal3e/invvalpage.htm

[9] PT Bursa Efek Indonesia, *Keputusan Direksi PT Bursa Efek Indonesia Nomor Kep-00061/BEI/07-2021 perihal Peraturan Nomor II-A tentang Perdagangan Efek Bersifat Ekuitas*, Jakarta, Indonesia, 2021. [Online]. Available: https://www.idx.co.id/media/10547/kep-00061_bei_07-2021_peraturan_ii-a.pdf

[10] Otoritas Jasa Keuangan, *Peraturan Otoritas Jasa Keuangan Republik Indonesia Nomor 12/POJK.03/2021 tentang Bank Umum*, Jakarta, Indonesia, 2021. [Online]. Available: https://www.ojk.go.id/id/regulasi/Documents/Pages/POJK-tentang-Bank-Umum/POJK%2012-03-2021.pdf

[11] T. Loughran and B. McDonald, "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks," *The Journal of Finance*, vol. 66, no. 1, pp. 35–65, Feb. 2011. [Online]. Available: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1334913
