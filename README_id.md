<p align="center">
  <img src="https://img.shields.io/badge/MiSi-Screener-0A0F1C?style=for-the-badge&logo=data:image/svg+xml;base64,&logoColor=00D4AA" alt="MiSi Screener">
  <img src="https://img.shields.io/badge/Versi-1.0.0-00D4AA?style=for-the-badge" alt="Versi">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Lisensi-Unlicense-blue?style=for-the-badge" alt="Lisensi">
</p>

<p align="center">
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README.md">English</a> |
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README_id.md">Bahasa Indonesia</a> |
  <a href="https://github.com/mulkymalikuldhrs/Misi-Screener/blob/master/README_zh.md">中文</a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=22&duration=3000&pause=1000&color=00D4AA&center=true&vCenter=true&width=600&lines=Platform+Hedge+Fund+Berbasis+AI;Mesin+Trading+Otonom;Terminal+Intelijensi+Kelas+Bloomberg;Arsitektur+Moduler+Berbasis+Agen" alt="Typing SVG" />
</p>

---

## Gambaran Umum

MiSi Screener adalah platform sumber terbuka yang powerful untuk membangun, menguji, dan menerapkan strategi trading otomatis berbasis AI. Dirancang sebagai ekosistem lengkap, platform ini berfungsi ganda sebagai **mesin trading otonom** dan **terminal intelijensi interaktif kelas Bloomberg**.

Sistem ini dirancang dari dasar untuk melampaui sekadar analisis menuju eksekusi nyata, menyediakan seluruh komponen inti dari hedge fund otomatis: definisi strategi, generasi sinyal, manajemen portofolio, eksekusi simulasi, dan validasi performa melalui backtesting. Proyek ini merupakan bagian dari ekosistem [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS), inisiatif yang lebih luas untuk membangun sistem intelijensi keuangan berbasis AI kelas sovereign.

## Fitur Utama

- **Mesin Trading Otonom**: Agen master menjalankan loop trading secara berkelanjutan, mengeksekusi strategi secara otomatis berdasarkan data pasar real-time. `HedgeFundMasterAgent` mengorkestrasi generasi sinyal, manajemen risiko, dan eksekusi perdagangan dalam siklus yang sepenuhnya otonom.
- **Definisi Strategi via YAML**: Tentukan strategi trading yang kompleks dengan file YAML yang jelas dan mudah dibaca manusia, menentukan kondisi entry/exit, parameter manajemen risiko, dan aturan position sizing. Tidak perlu perubahan kode untuk mengiterasi strategi.
- **Mesin Backtesting "No Gimmick"**: Backtester berbasis CLI yang powerful (`run_backtest.py`) menggunakan komponen yang *persis sama* dengan mesin trading live, memastikan validasi performa strategi yang realistis tanpa lookahead bias.
- **Dashboard Operasional**: Terminal interaktif yang telah berevolusi menjadi pusat komando. Mulai dan hentikan agen otonom, pantau performa portofolio real-time (`/portfolio`), dan lakukan riset pasar dari satu antarmuka.
- **Arsitektur Modular Berbasis Agen**: Sistem terdiri dari agen-agen khusus (`SignalAgent`, `PortfolioManager`, `HedgeFundMasterAgent`) yang bekerja sama, membuat logika bersih, terpisah, dan dapat diperluas.
- **Integrasi Data Real-Time**: Terhubung ke API publik gratis untuk seluruh data pasar, termasuk Yahoo Finance, Alpha Vantage, dan NewsAPI, memastikan analisis dan trading berdasarkan data nyata.
- **Orkestrator Kueri AI**: Antarmuka bahasa alami yang memahami kueri kompleks, mengidentifikasi banyak ticker, dan merutekan permintaan ke konektor data dan modul analitis yang sesuai.
- **Mesin Quant Scoring**: Sistem scoring proprietary yang mengagregasi indikator teknikal, fundamental, dan sentimen menjadi penilaian kuantitatif terpadu untuk setiap aset.

## Arsitektur Sistem

Proyek ini disusun sebagai sistem trading lengkap dengan pemisahan tanggung jawab yang jelas:

```
Misi-Screener/
├── strategies/           # Definisi strategi trading berbasis YAML
├── agents/               # "Otak": sinyal, portofolio, orkestrasi
│   ├── signal_agent.py          # Interpretasi strategi & generasi sinyal
│   ├── portfolio_manager.py     # Position sizing & manajemen risiko
│   ├── master_agent.py          # Orkestrator loop trading otonom
│   ├── advanced_orchestrator.py # Parsing kueri bahasa alami
│   ├── technical_analyst.py     # Agen analisis teknikal
│   ├── fundamental_analyst.py   # Agen analisis fundamental
│   ├── sentiment_analyst.py     # Agen analisis sentimen pasar
│   ├── trader_agent.py          # Agen eksekusi perdagangan
│   └── risk_manager.py          # Penilaian & manajemen risiko
├── components/           # Modul analitis dan mesin scoring
│   ├── technical_indicators.py  # Perhitungan indikator teknikal inti
│   ├── quant_scoring/           # Mesin scoring kuantitatif
│   ├── final_verdict/           # Mesin agregasi verdict akhir
│   ├── market_structure/        # Analisis struktur pasar
│   ├── liquidity_orderflow/     # Analisis likuiditas & aliran order
│   ├── order_book_venue/        # Analisis order book & venue
│   ├── intermarket/             # Analisis korelasi antar-pasar
│   ├── positioning_crowd/       # Analisis posisi kerumunan
│   ├── dex_intelligence/        # Modul intelijensi DEX
│   ├── macro_analysis/          # Analisis makroekonomi
│   ├── monetary_fundamental/    # Analisis fundamental kebijakan moneter
│   └── execution_plan/          # Pembangun rencana eksekusi
├── execution/            # Broker paper trading simulasi
├── data_sources/         # Konektor untuk API data eksternal
│   ├── yfinance_connector.py
│   ├── alpha_vantage_connector.py
│   └── news_connector.py
├── dashboard/            # Terminal web interaktif
│   ├── backend/                 # Backend FastAPI
│   └── frontend/                # Antarmuka web
├── tests/                # Pengujian unit dan integrasi
└── run_backtest.py       # Mesin backtesting mandiri
```

Untuk penjelasan lebih detail, lihat [ARCHITECTURE.md](./ARCHITECTURE.md).

## Memulai

### Prasyarat

- Python 3.11 atau lebih tinggi
- Manajer paket pip
- Kunci API untuk fitur yang disempurnakan (opsional tetapi disarankan)

### 1. Instalasi

Clone repositori dan instal dependensi:

```bash
git clone https://github.com/mulkymalikuldhrs/Misi-Screener.git
cd Misi-Screener
pip install -r requirements.txt
```

### 2. Siapkan Kunci API

Atur variabel lingkungan berikut. Meskipun tidak diperlukan untuk strategi RSI, kunci ini diperlukan untuk perintah `/news` dan `/FA`:

```bash
export NEWS_API_KEY='kunci_anda_dari_newsapi.org'
export ALPHA_VANTAGE_API_KEY='kunci_anda_dari_alphavantage.co'
```

### 3. Backtesting Strategi

Sebelum menjalankan agen secara live, selalu validasi strategi dengan backtester:

```bash
python run_backtest.py strategies/mean_reversion_rsi.yml --start "2023-01-01" --end "2023-12-31"
```

Ini menjalankan strategi `MeanReversionRSI` pada periode historis yang ditentukan dan mencetak laporan performa detail termasuk total pengembalian, drawdown, dan statistik perdagangan.

### 4. Menjalankan Agen Otonom

Mulai server backend dari direktori root proyek:

```bash
python -m uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
```

Kemudian buka browser web Anda ke `http://127.0.0.1:8000`.

- Klik **"Start Agent"** untuk menginisialisasi `HedgeFundMasterAgent`. Agen akan mulai mengeksekusi loop trading setiap 60 detik secara default.
- Gunakan perintah `/portfolio` untuk memantau posisi dan performa secara real-time.
- Klik **"Stop Agent"** untuk mematikan loop trading secara graceful.

## Agen Inti

| Agen | Modul | Peran |
|------|-------|-------|
| `HedgeFundMasterAgent` | `agents/master_agent.py` | Orkestrator master yang menjalankan loop trading otonom |
| `SignalAgent` | `agents/signal_agent.py` | Interpretasi strategi dan generasi sinyal (BUY/SELL/HOLD) |
| `PortfolioManager` | `agents/portfolio_manager.py` | Position sizing, manajemen risiko, dan pelacakan status portofolio |
| `AdvancedQueryOrchestrator` | `agents/advanced_orchestrator.py` | Parsing kueri bahasa alami dan perutean multi-ticker |
| `TechnicalAnalyst` | `agents/technical_analyst.py` | Analisis teknikal dan pengenalan pola |
| `FundamentalAnalyst` | `agents/fundamental_analyst.py` | Analisis fundamental dan valuasi |
| `SentimentAnalyst` | `agents/sentiment_analyst.py` | Analisis sentimen pasar dan berita |
| `RiskManager` | `agents/risk_manager.py` | Penilaian risiko portofolio dan manajemen |
| `TraderAgent` | `agents/trader_agent.py` | Eksekusi perdagangan dan manajemen order |

## Dokumentasi

- [Panduan Arsitektur](./ARCHITECTURE.md) - Arsitektur sistem detail dan interaksi komponen
- [Panduan Kontribusi](./CONTRIBUTING.md) - Cara berkontribusi ke MiSi Screener
- [Catatan Perubahan](./CHANGELOG.md) - Riwayat rilis dan perubahan penting
- [Filosofi](./docs/philosophy.md) - Filosofi desain intelijensi kelas sovereign berbasis AI
- [Keterbatasan](./docs/limitations.md) - Keterbatasan sistem saat ini dan masalah yang diketahui
- [Validasi](./docs/validation.md) - Metodologi validasi strategi
- [Referensi](./docs/references.md) - Referensi akademis dan teknis

## Proyek Terkait

- [HermesQuantOS](https://github.com/mulkymalikuldhrs/HermesQuantOS) - Ekosistem intelijensi keuangan berbasis AI yang lebih luas
- [SolSniperX](https://github.com/mulkymalikuldhrs/SolSniperX) - Bot sniper memecoin Solana berbasis AI

## Lisensi

Proyek ini dirilis ke domain publik di bawah [Unlicense](./LICENSE). Anda bebas untuk menyalin, memodifikasi, mempublikasikan, menggunakan, mengkompilasi, menjual, atau mendistribusikan perangkat lunak ini untuk tujuan apa pun, komersial maupun non-komersial.

## Penulis

**Mulky Malikul Dhaher**

- Email: mulkymalikuldhaher@email.com
- GitHub: [@mulkymalikuldhrs](https://github.com/mulkymalikuldhrs)

<p align="center">
  <img src="https://img.shields.io/github/stars/mulkymalikuldhrs/Misi-Screener?style=social" alt="Stars">
  <img src="https://img.shields.io/github/forks/mulkymalikuldhrs/Misi-Screener?style=social" alt="Forks">
  <img src="https://img.shields.io/github/watchers/mulkymalikuldhrs/Misi-Screener?style=social" alt="Watchers">
</p>
