# VAK Sistem

Sistem Analisis Gaya Belajar VAK berbasis web yang dibangun dengan Flask untuk membantu identifikasi gaya belajar siswa berdasarkan pendekatan Visual, Auditori, dan Kinestetik (VAK). Aplikasi ini memadukan data siswa, analisis clustering K-Means dan Fuzzy C-Means, serta rekomendasi jurusan yang disesuaikan dengan karakteristik belajar peserta didik.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-FF6B6B?style=for-the-badge" alt="Frontend" />
  <img src="https://img.shields.io/badge/Data-CSV%20%2B%20JSON-4ECDC4?style=for-the-badge" alt="Data" />
</p>

## Ringkasan Proyek

Proyek ini dirancang untuk membantu pengelolaan dan analisis data siswa secara cepat dan terstruktur. Fitur utama yang tersedia meliputi:

- autentikasi berbasis token untuk role guru dan siswa
- dashboard guru dengan statistik dan daftar siswa
- pencarian data siswa berdasarkan inisial
- analisis gaya belajar Visual, Auditori, dan Kinestetik
- hasil clustering K-Means dan Fuzzy C-Means
- proporsi dan membership cluster
- rekomendasi jurusan sesuai gaya belajar dominan
- antarmuka web yang modern dan profesional

## Fitur Utama

- Login dengan token
- Role-based access: guru dan siswa
- Dashboard guru
- Hasil analisis personal siswa
- Visualisasi proporsi gaya belajar
- Hasil K-Means dan FCM
- Rekomendasi jurusan
- UI yang responsif dan siap untuk deployment

## Teknologi yang Digunakan

- Python 3.11+
- Flask
- Pandas
- Jinja2 Templates
- HTML5
- CSS3
- JavaScript
- Data CSV dan JSON

## Struktur Proyek

```bash
WEB/
├── app.py
├── README.md
├── requirement.txt
├── data/
│   ├── SMA1_DATABASE.CSV
│   └── token.json
├── js/
│   └── login.js
├── static/
│   ├── assets/
│   ├── css/
│   └── js/
├── template/
│   ├── login.html
│   ├── tentang.html
│   ├── guru/
│   │   ├── dashboard.html
│   │   └── hasil_siswa.html
│   ├── rekomendasi/
│   │   ├── rekomendasi_visual.html
│   │   ├── rekomendasi_auditori.html
│   │   └── rekomendasi_kinestetik.html
│   └── siswa/
│       └── hasil.html
├── utils/
│   ├── auth.py
│   ├── data.py
│   └── rekomendasi.py
└── .venv/
```

## Persyaratan Sistem

- Python 3.11 atau lebih tinggi
- pip
- browser modern
- Git

## Instalasi

### 1. Clone repository

```bash
git clone https://github.com/kimithora/VAKSistem.git
cd VAKSistem
```

### 2. Buat environment virtual

Windows PowerShell:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dependency

```bash
pip install -r requirement.txt
```

Jika file `requirement.txt` belum lengkap, Anda bisa install manual:

```bash
pip install flask pandas
```

## Menjalankan Aplikasi

```bash
python app.py
```

Buka browser dan akses:

```bash
http://127.0.0.1:5000/
```

## Struktur Login dan Role

System login dibagi berdasarkan role user:

- Guru: dapat mengakses dashboard dan melihat hasil analisis siswa
- Siswa: dapat melihat hasil gaya belajar dan rekomendasi jurusan

Token diolah melalui file `data/token.json` dan modul autentikasi pada `utils/auth.py`.

## Data yang Digunakan

Aplikasi membaca data siswa dari file:

```bash
data/SMA1_DATABASE.CSV
```

Data yang diproses mencakup informasi seperti:

- Inisial
- Kelas
- Rombel
- Sekolah
- Jurusan
- Visual
- Auditori
- Kinestetik
- Visual_prop
- Auditori_prop
- Kinestetik_prop
- KMeans_Cluster
- KMeans_Gaya_Belajar
- FCM_Membership_Cluster_0
- FCM_Membership_Cluster_1
- FCM_Membership_Cluster_2
- FCM_Cluster
- FCM_Gaya_Belajar
- FCM_Derajat_Keanggotaan

## Cara Kerja Sistem

### 1. Input data siswa
Data siswa diperoleh dari file CSV.

### 2. Analisis VAK
Sistem menghitung skor dan proporsi untuk masing-masing gaya belajar:

- Visual
- Auditori
- Kinestetik

### 3. Clustering
Aplikasi melakukan analisis lebih lanjut dengan:

- K-Means
- Fuzzy C-Means

### 4. Hasil dan Rekomendasi
Sistem menampilkan hasil dengan format yang mudah dibaca serta merekomendasikan jurusan berdasarkan gaya belajar dominan.

## Halaman Aplikasi

### Halaman Login
Halaman untuk masuk ke sistem menggunakan token.

### Dashboard Guru
Guru dapat melihat:

- daftar siswa
- statistik data
- hasil analisis per siswa
- rekomendasi yang sesuai

### Halaman Hasil Siswa
Menampilkan:

- identitas siswa
- skor VAK
- hasil K-Means
- hasil FCM
- rekomendasi jurusan

## Deployment

### Local Development

```bash
python app.py
```

### Vercel Deployment

Proyek ini juga siap untuk deployment ke Vercel. Untuk kebutuhan deployment, pastikan konfigurasi aplikasi dan environment variable sudah sesuai, termasuk pengaturan `SECRET_KEY` bila diperlukan.

## Environment Variables

```bash
SECRET_KEY=your-secret-key
VERCEL=1
```

## Changelog

### v1.1.3: Persiapan rilis berikutnya
- Penyempurnaan dokumentasi project
- Penataan README agar lebih profesional dan rapi
- Persiapan versi publik repository
- Penyesuaian catatan perubahan aplikasi

### v1.1.2: Vercel deployment
- Deployment aplikasi ke Vercel
- Penyempurnaan konfigurasi runtime
- Penyesuaian untuk lingkungan hosting

### v1.1.1: Penyempurnaan sedikit
- Perbaikan antarmuka
- Optimasi flow login dan token
- Penyempurnaan pengalaman pengguna

### v1.1.0: Siap launching
- Persiapan launch aplikasi
- Stabilisasi fitur utama
- Penyempurnaan desain dan navigasi

### Menentukan 2 theme: elegant dan klasik atau colorful dan cyber
- Evaluasi desain visual yang cocok untuk interface aplikasi
- Pemilihan arah tema modern dan profesional

### v0.1.0: Pembuatan sistem awal
- Inisialisasi proyek
- Pembuatan struktur dasar sistem
- Implementasi analisis awal gaya belajar

## Roadmap

- integrasi database relasional
- pengembangan API backend
- export data ke PDF/Excel
- dashboard analitik lebih modern
- logging aktivitas user
- optimasi UX dan UI

## Kontribusi

Kontribusi sangat terbuka untuk pengembangan lebih lanjut. Anda bisa melakukan:

1. fork repository
2. buat branch baru
3. commit perubahan
4. buka pull request

## Lisensi

Proyek ini dibuat untuk kebutuhan penelitian dan pengembangan aplikasi analisis gaya belajar. Silakan sesuaikan lisensi sesuai kebutuhan institusi atau tim pengembang.

## Kontak

- GitHub: https://github.com/kimithora
- Project: VAK Sistem

## Penutup

VAK Sistem adalah aplikasi berbasis web yang menggabungkan analisis gaya belajar siswa dengan pendekatan data dan clustering. Aplikasi ini diharapkan menjadi alat bantu yang berguna untuk analisis pembelajaran, rekomendasi jurusan, serta kebutuhan penelitian di bidang pendidikan.

> Proyek ini terus berkembang dan siap untuk melangkah ke rilis berikutnya dengan dokumentasi yang lebih rapi dan profesional.

