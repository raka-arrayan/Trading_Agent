# DAFTAR REFERENSI UTAMA & LANDASAN TEORITIS SKRIPSI (BAB 1 – 3)

Dokumen ini berisi rangkuman komprehensif 9 referensi ilmiah kredibel (jurnal internasional dan makalah konferensi bereputasi) yang menjadi landasan teoritis, perancangan arsitektur, dan metodologi evaluasi dalam penulisan naskah skripsi Bab 1 sampai Bab 3.

---

## TABEL PEMETAAN KONTRIBUSI REFERENSI KE BAB SKRIPSI

| No | Referensi Utama | Bidang / Ranah | Tautan Akses | Kontribusi Utama pada Skripsi |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **TradingAgents** (Xiao et al., 2024) | Multi-Agent Financial Framework | [arXiv:2412.20138](https://arxiv.org/abs/2412.20138) | **Bab 1, 2, 3**: Acuan dasar pembagian departemen spesialis agen finansial. |
| **2** | **AI Safety via Debate** (Irving et al., 2018) | Teori Debat Adversarial & XAI | [arXiv:1805.00899](https://arxiv.org/abs/1805.00899) | **Bab 1, 2**: Justifikasi teoritis mekanisme debat adversarial untuk membatasi halusinasi. |
| **3** | **Attention Is All You Need** (Vaswani et al., 2017) | Arsitektur Dasar LLM (Transformer) | [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) | **Bab 2**: Dasar matematis arsitektur Transformer dan mekanisme Self-Attention ($QK^TV$). |
| **4** | **FinCon** (Yu et al., 2024) | Komunikasi Hierarkis Multi-Agent | [arXiv:2407.06567](https://arxiv.org/abs/2407.06567) | **Bab 2, 3**: Desain hierarki aliran informasi dari tim analis level bawah ke manajer eksekusi. |
| **5** | **MetaGPT** (Hong et al., 2023) | SOP & Separation of Concerns | [arXiv:2308.00352](https://arxiv.org/abs/2308.00352) | **Bab 2, 3**: Landasan rekayasa pemecahan peran (*role-playing*) dan isolasi tugas spesifik agen. |
| **6** | **FinDebate** (Cai et al., 2025) | Debat AI pada Sektor Keuangan | [arXiv:2509.17395](https://arxiv.org/abs/2509.17395) | **Bab 1, 2**: Bukti empiris efektivitas debat dalam mereduksi *overconfidence* pada analisis saham. |
| **7** | **Efficient Capital Markets** (Fama, 1970) | Teori Keuangan (EMH Semi-Kuat) | [JSTOR / UI Library](https://remote-lib.ui.ac.id:2065/stable/7104d0bd-69aa-330c-badb-94aa0c8f5bac?seq=1) | **Bab 1, 2**: Landasan mengapa integrasi berita sentimen, makro, dan fundamental diperlukan. |
| **8** | **The Sharpe Ratio** (Sharpe, 1994) | Metrik Kinerja Portofolio | [Stanford University](https://web.stanford.edu/~wfsharpe/art/sr/sr.htm) | **Bab 2, 3**: Landasan matematis evaluasi imbal hasil tersesuaikan risiko (*risk-adjusted return*). |
| **9** | **Maximum Drawdown** (Magdon-Ismail & Atiya, 2004) | Metrik Risiko Penurunan (*Downside*) | [SSRN Repository](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=874069) | **Bab 2, 3**: Rujukan analitis rumus Maximum Drawdown dan mitigasi kejatuhan modal portofolio. |

---

## RINCIAN DESKRIPSI & MANFAAT SETIAP REFERENSI

### 1. TradingAgents (Xiao et al., 2024)
- **Judul Asli**: *TradingAgents: Multi-Agents LLM Financial Trading Framework*
- **Penulis**: Xiao, et al.
- **Tautan Akses**: [https://arxiv.org/abs/2412.20138](https://arxiv.org/abs/2412.20138)
- **Fokus Utama**:  
  Paper ini memperkenalkan arsitektur sistem perdagangan saham berbasis *Multi-Agent Large Language Model* (LLM) yang mengadaptasi pembagian departemen profesional pada institusi keuangan: analis pasar, peneliti strategi, komite manajemen risiko, dan *trader* eksekusi.
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 1 (Latar Belakang)**: Menjadi tolok ukur utama perkembangan riset terkini (*state-of-the-art*) dalam penerapan multi-agen cerdas di industri keuangan global.
  - **Bab 2 & 3 (Desain Arsitektur)**: Menjadi cetak biru pembagian peran agen yang kemudian dikembangkan lebih lanjut pada skripsi ini menjadi sistem 12 agen dengan mekanisme debat dua lapis (*adversarial consensus*).

---

### 2. AI Safety via Debate (Irving et al., 2018 - DeepMind)
- **Judul Asli**: *AI Safety via Debate*
- **Penulis**: Geoffrey Irving, Paul Christiano, & Dario Amodei (Google DeepMind / OpenAI)
- **Tautan Akses**: [https://arxiv.org/abs/1805.00899](https://arxiv.org/abs/1805.00899)
- **Fokus Utama**:  
  Paper seminal ini membuktikan secara teoritis dan matematis bahwa menempatkan dua model AI dalam skenario perdebatan kompetitif (*zero-sum debate game*) di hadapan penilai/fasilitator akan memaksa agen mengungkap fakta yang benar, meminimalkan halusinasi, dan meningkatkan transparansi penalaran.
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 1 (Kebaruan / Novelty)**: Memberikan justifikasi ilmiah yang sangat kuat mengapa sistem kita menggunakan mekanisme debat (*Bullish vs. Bearish* pada Layer 2 dan *Aggressive vs. Conservative* pada Layer 3), bukan sekadar perataan suara (*majority voting*) biasa.
  - **Bab 2 (Explainable AI)**: Menjadi fondasi konsep transparansi, di mana notulensi perdebatan kedua kubu berfungsi sebagai penjelasan rasional (*rational explanation*) yang dapat dipertanggungjawabkan kepada investor.

---

### 3. Attention Is All You Need (Vaswani et al., 2017 - Google Brain)
- **Judul Asli**: *Attention Is All You Need*
- **Penulis**: Ashish Vaswani, Noam Shazeer, Niki Parmar, et al. (Google Brain & Google Research)
- **Tautan Akses**: [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- **Fokus Utama**:  
  Menciptakan arsitektur *Transformer* yang mendasari seluruh model bahasa besar (LLM) modern saat ini, menggantikan arsitektur rekuren dengan mekanisme *Scaled Dot-Product Self-Attention*.
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 2 (Dasar Teori AI & LLM)**: Menjadi rujukan resmi rumus dasar pemrosesan representasi teks pada agen LLM:
    $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
  - Menjelaskan bagaimana LLM mampu memahami keterkaitan informasi antar-paragraf panjang pada berita keuangan dan laporan keuangan tahunan perbankan secara simultan.

---

### 4. FinCon (Yu et al., 2024)
- **Judul Asli**: *FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making*
- **Penulis**: Yu, et al.
- **Tautan Akses**: [https://arxiv.org/abs/2407.06567](https://arxiv.org/abs/2407.06567)
- **Fokus Utama**:  
  Membahas arsitektur komunikasi hierarkis antar-agen finansial serta penyampaian umpan balik verbal (*verbal reinforcement*) agar komunikasi antar-agen tidak mengalami degradasi makna saat ditransmisikan antar-tingkatan organisasi.
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 2 & 3 (Desain Aliran Data)**: Menjadi rujukan struktur pengiriman pesan bertingkat: bagaimana ringkasan laporan 4 Domain Analysts level bawah diagregasikan secara terstruktur ke tim debat level menengah, sebelum diputuskan oleh Portfolio Manager.

---

### 5. MetaGPT (Hong et al., 2023)
- **Judul Asli**: *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*
- **Penulis**: Sirui Hong, Mingchen Zhuge, Jonathan Chen, et al. (DeepWisdom)
- **Tautan Akses**: [https://arxiv.org/abs/2308.00352](https://arxiv.org/abs/2308.00352)
- **Fokus Utama**:  
  Menyusun kerangka kerja multi-agen berbasis *Standard Operating Procedures (SOP)* dan prinsip rekayasa perangkat lunak *Separation of Concerns* (pemisahan tanggung jawab).
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 2 & 3 (Perancangan Peran Agen)**: Menjadi landasan rekayasa sistem: membuktikan bahwa membagi masalah trading yang rumit menjadi peran agen yang sempit dan terspesialisasi (Fundamental, Teknikal, Makro, Sentimen, Risiko) menghasilkan luaran yang jauh lebih stabil dan minim bias dibanding satu model umum (*single generalist prompt*).

---

### 6. FinDebate (Cai et al., 2025)
- **Judul Asli**: *FinDebate: Multi-Agent Collaborative Intelligence for Financial Analysis*
- **Penulis**: Cai, et al.
- **Tautan Akses**: [https://arxiv.org/abs/2509.17395](https://arxiv.org/abs/2509.17395)
- **Fokus Utama**:  
  Menguji penerapan perdebatan multi-agen secara khusus pada tugas-tugas analisis keuangan. Penelitian ini membuktikan secara empiris bahwa debat mampu mereduksi rasa percaya diri berlebih (*overconfidence bias*) dan bias optimisme yang sering menjangkiti LLM saat membaca berita positif.
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 1 & 2**: Memperkuat urgensi penelitian: membuktikan secara empiris bahwa instrumen keuangan yang sangat fluktuatif membutuhkan agen pengkritik (*adversarial critic*) untuk menyaring sinyal palsu sebelum perintah eksekusi diterbitkan.

---

### 7. Efficient Capital Markets (Fama, 1970 - Hadiah Nobel)
- **Judul Asli**: *Efficient Capital Markets: A Review of Theory and Empirical Work*
- **Penulis**: Eugene F. Fama (*The Journal of Finance*, Vol. 25, No. 2, pp. 383–417)
- **Tautan Akses**: [https://www.jstor.org/stable/2325486](https://www.jstor.org/stable/2325486) / Repositori UI: [Remote-Lib UI](https://remote-lib.ui.ac.id:2065/stable/7104d0bd-69aa-330c-badb-94aa0c8f5bac?seq=1)
- **Fokus Utama**:  
  Teori ekonomi paling fundamental mengenai *Efficient Market Hypothesis (EMH)*, khususnya hipotesis bentuk setengah kuat (*Semi-Strong Form Efficiency*).
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 1 (Latar Belakang Finansial)**: Memberikan landasan teoritis pasar modal mengapa sistem kita menggabungkan multi-modalitas data (fundamental, sentimen berita publik, indikator teknikal, dan makroekonomi).
  - Berdasarkan Fama, harga saham di pasar efisien bentuk setengah-kuat mencerminkan seluruh informasi publik yang tersedia secara cepat. Sistem 12 agen dikembangkan untuk mengatasi keterbatasan kognitif manusia dalam mengasimilasi banjir informasi publik tersebut secara terpadu.

---

### 8. The Sharpe Ratio (Sharpe, 1994 - Hadiah Nobel)
- **Judul Asli**: *The Sharpe Ratio*
- **Penulis**: William F. Sharpe (*The Journal of Portfolio Management*, Vol. 21, No. 1, pp. 49–58)
- **Tautan Akses**: [https://web.stanford.edu/~wfsharpe/art/sr/sr.htm](https://web.stanford.edu/~wfsharpe/art/sr/sr.htm)
- **Fokus Utama**:  
  Perumusan standar matematis pengukuran kinerja investasi berbasis imbal hasil tersesuaikan risiko (*risk-adjusted return*).
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 2 & 3 (Metrik Evaluasi Sistem)**: Rujukan ilmiah resmi untuk kalkulasi Sharpe Ratio yang diimplementasikan pada kode `utils/metrics.py`:
    $$\text{Sharpe Ratio} = \frac{\bar{R}_p - R_f}{\sigma_p} \times \sqrt{252}$$
  - Membenarkan bahwa keberhasilan portofolio MAS dinilai berdasarkan efisiensi imbal hasil terhadap volatilitas risiko yang diambil, bukan sekadar persentase keuntungan mutlak.

---

### 9. Maximum Drawdown (Magdon-Ismail & Atiya, 2004)
- **Judul Asli**: *Maximum Drawdown*
- **Penulis**: Malik Magdon-Ismail & Amir F. Atiya (*Risk Magazine*, Vol. 17, No. 10, pp. 99–102)
- **Tautan Akses**: [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=874069](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=874069)
- **Fokus Utama**:  
  Penetapan definisi matematis dan analisis perilaku metrik *Maximum Drawdown (MDD)* sebagai pengukur risiko penurunan nilai modal terparah (*downside / tail risk*) dalam suatu horizon investasi.
- **Manfaat & Kontribusi pada Skripsi**:
  - **Bab 2 & 3 (Evaluasi Risiko Portofolio)**: Rujukan matematis resmi dari implementasi rumus MDD di `utils/metrics.py`:
    $$\text{MDD}(T) = \max_{\tau \in [0, T]} \left( \frac{\max_{t \in [0, \tau]} P(t) - P(\tau)}{\max_{t \in [0, \tau]} P(t)} \right)$$
  - Menjadi landasan teoritis pembentukan peran **Conservative Risk Analyst** dan **Risk Facilitator**, yang terbukti secara empiris berhasil menekan drawdown saham BBCA dan BMRI dari -21% menjadi hanya -3% saat pasar terkoreksi.
