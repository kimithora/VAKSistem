# README Penggunaan Aplikasi Analisis Gaya Belajar

Aplikasi ini dibuat menggunakan Flask untuk menganalisis gaya belajar peserta berdasarkan data siswa pada file CSV. Aplikasi menampilkan hasil pencarian berdasarkan inisial, detail profil peserta, serta hasil analisis gaya belajar menggunakan metode K-Means dan Fuzzy C-Means.

## Fitur utama

- Pencarian data peserta berdasarkan inisial
- Menampilkan profil siswa lengkap
- Melihat skor gaya belajar Visual, Auditori, dan Kinestetik
- Menampilkan hasil analisis K-Means
- Menampilkan hasil analisis Fuzzy C-Means
- Menampilkan rekomendasi jurusan sesuai gaya belajar dominan
- Antarmuka web sederhana dan responsif

## Teknologi yang digunakan

- Python
- Flask
- Pandas
- HTML + CSS
- CSV sebagai database lokal

## Struktur folder

```bash
WEB/
├── app.py
├── SMA1_DATABASE.csv
├── README.md
├── static/
│   └── css/
├── templates/
│   ├── index.html
│   ├── hasil.html
│   ├── rekomendasi_visual.html
│   ├── rekomendasi_auditori.html
│   └── rekomendasi_kinestetik.html
└── venv/   (opsional jika Anda membuat environment virtual)
```

## Persyaratan

Pastikan perangkat Anda sudah memiliki:

- Python 3.9 atau versi lebih baru
- pip
- Akses ke file CSV data siswa

## Langkah instalasi

1. Buka terminal atau Command Prompt.
2. Masuk ke folder project:

```bash
cd c:\projek\penelitian2\Kodinga\WEB
```

3. Buat virtual environment (opsional tapi disarankan):

```bash
python -m venv venv
```

4. Aktifkan virtual environment:

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
venv\Scripts\activate.bat
```

5. Install dependency:

```bash
pip install flask pandas
```

## Menjalankan aplikasi

Jalankan perintah berikut di folder project:

```bash
python app.py
```

Setelah server berjalan, buka browser dan akses:

```bash
http://127.0.0.1:5000/
```

## Cara penggunaan aplikasi

### 1. Halaman utama

Pada halaman utama, Anda akan melihat form pencarian.

- Masukkan inisial siswa yang ingin dicari.
- Contoh: `KTR`, `ABC`, `RZ`.
- Klik tombol Cari.

### 2. Hasil pencarian

Aplikasi akan menampilkan daftar siswa yang sesuai dengan inisial yang dimasukkan. Setiap data akan memiliki link untuk melihat hasil analisis lebih detail.

### 3. Detail hasil analisis

Saat mengklik salah satu hasil pencarian, aplikasi akan membuka halaman detail peserta yang berisi:

- identitas peserta
- sekolah, kelas, rombel, jurusan
- skor Visual, Auditori, Kinestetik
- hasil analisis K-Means
- hasil analisis Fuzzy C-Means
- proporsi/derajat keanggotaan
- rekomendasi jurusan sesuai gaya belajar dominan

### 4. Rekomendasi jurusan

Berdasarkan gaya belajar dominan, aplikasi akan mengarahkan ke halaman rekomendasi, misalnya:

- /rekomendasi/visual
- /rekomendasi/auditori
- /rekomendasi/kinestetik

## Database

Aplikasi membaca data dari file:

```bash
SMA1_DATABASE.csv
```

File CSV harus memiliki kolom berikut:

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

Jika kolom-kolom tersebut tidak lengkap, aplikasi akan memberi peringatan dan tidak dapat memproses data.

## Endpoint utama

Berikut beberapa route yang tersedia pada aplikasi:

- `/` : halaman utama
- `/search` : pencarian data siswa
- `/hasil/<inisial>` : halaman detail profil siswa
- `/rekomendasi/visual` : halaman rekomendasi visual
- `/rekomendasi/auditori` : halaman rekomendasi auditori
- `/rekomendasi/kinestetik` : halaman rekomendasi kinestetik

## Catatan penting

- Pastikan file `SMA1_DATABASE.csv` berada di folder project yang sama dengan `app.py`.
- Jika Anda ingin mengganti data, cukup edit file CSV sesuai struktur kolom yang sudah ditentukan.
- Pada mode pengembangan, aplikasi dijalankan dengan `debug=True`, sehingga perubahan file akan otomatis ter-refresh di browser saat server berjalan.

## Troubleshooting

### Masalah: `File database tidak ditemukan`

Periksa apakah file `SMA1_DATABASE.csv` ada di folder project dan nama file benar.

### Masalah: `Kolom berikut tidak ditemukan`

Periksa kembali struktur kolom CSV. Pastikan nama kolom sesuai persis dengan yang dibutuhkan aplikasi.

### Masalah: `Tidak ditemukan peserta dengan inisial ...`

Cek apakah inisial yang Anda cari ada dalam data dan apakah format penulisan benar.

## Penutup

Aplikasi ini berguna untuk memudahkan proses analisis gaya belajar siswa secara cepat dan terstruktur berbasis data. Dengan tampilan web yang sederhana, pengguna dapat mencari dan melihat hasil analisis tanpa perlu menjalankan proses data secara manual.

## Version 
### v0.1.0
set up projek awal

### v0.2.0
beberapa perubahan yang harus on-going:
1. membuat sistem autentikasi baik untuk guru bk sebagai admin dan siswa sebagai user
2. membuat 1 bar persentase 

