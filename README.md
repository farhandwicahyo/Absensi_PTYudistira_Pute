# Sistem Presensi Karyawan Berbasis Website

Sistem presensi karyawan berbasis website yang dibangun menggunakan Flask (Python), SQL Server, dan Flowbite/Tailwind CSS.

## Fitur

- ✅ Login dan Hak Akses Pengguna (Admin, HRD, Atasan, Karyawan)
- ✅ Presensi Kehadiran (Check-in & Check-out)
- ✅ Presensi Berbasis Lokasi (Geolocation)
- ✅ Validasi Waktu dan Perangkat
- ✅ Manajemen Data Karyawan (CRUD, Import/Export)
- ✅ Pengajuan Izin, Cuti, dan Sakit dengan Approval Workflow
- ✅ Pengajuan Lembur
- ✅ Notifikasi Sistem
- ✅ Audit Log dan Riwayat Aktivitas

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **Database**: Microsoft SQL Server
- **Frontend**: HTML, CSS, JavaScript, Flowbite, Tailwind CSS
- **Arsitektur**: MVC (Model-View-Controller)

## Instalasi

### 1. Prerequisites

- Python 3.8 atau lebih tinggi
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

### 2. Clone Repository

```bash
git clone <repository-url>
cd "Farhan Pribadi"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Database

Edit file `config.py` dan sesuaikan koneksi database:

```python
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://username:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server'
```

Atau gunakan environment variable:

```bash
export DATABASE_URL="mssql+pyodbc://username:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server"
```

### 5. Konfigurasi Lokasi Kantor

Edit file `config.py` untuk mengatur koordinat kantor:

```python
OFFICE_LATITUDE = -6.2088   # Ganti dengan latitude kantor Anda
OFFICE_LONGITUDE = 106.8456  # Ganti dengan longitude kantor Anda
GEO_RADIUS_METERS = 100      # Radius dalam meter
```

### 6. Inisialisasi Database

Jalankan script untuk membuat tabel dan user default:

```bash
python init_db.py
```

### 7. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Default User

Setelah menjalankan `init_db.py`, gunakan kredensial berikut:

- **Admin**: username: `admin`, password: `admin123`
- **HRD**: username: `hrd`, password: `hrd123`

> **PENTING**: Ganti password default setelah login pertama kali!

## Struktur Proyek

```
.
├── app.py                 # Aplikasi utama Flask
├── config.py              # Konfigurasi aplikasi
├── requirements.txt        # Dependencies Python
├── init_db.py            # Script inisialisasi database
├── models/               # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── employee.py
│   ├── attendance.py
│   ├── leave_request.py
│   ├── overtime.py
│   ├── notification.py
│   └── audit_log.py
├── controllers/          # Controllers (business logic)
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── dashboard_controller.py
│   ├── attendance_controller.py
│   ├── employee_controller.py
│   ├── leave_controller.py
│   ├── overtime_controller.py
│   ├── notification_controller.py
│   └── audit_controller.py
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── decorators.py
│   ├── audit_logger.py
│   ├── geolocation.py
│   ├── device_info.py
│   └── notification_helper.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── attendance/
│   ├── employee/
│   ├── leave/
│   ├── overtime/
│   └── audit/
└── uploads/            # Folder untuk file upload
```

## Penggunaan

### Presensi

1. Login sebagai karyawan
2. Buka halaman Presensi
3. Klik tombol "Check In" (pastikan lokasi GPS aktif)
4. Sistem akan memvalidasi lokasi dan waktu
5. Untuk check-out, klik tombol "Check Out"

### Manajemen Karyawan (Admin/HRD)

1. Buka halaman Data Karyawan
2. Tambah karyawan baru atau edit data yang ada
3. Import/Export data menggunakan CSV

### Pengajuan Izin/Cuti/Sakit

1. Login sebagai karyawan
2. Buka halaman Izin/Cuti/Sakit
3. Klik "Ajukan Izin/Cuti/Sakit"
4. Isi form dan kirim
5. Atasan dan HRD akan menerima notifikasi untuk approval

### Pengajuan Lembur

1. Login sebagai karyawan
2. Buka halaman Lembur
3. Klik "Ajukan Lembur"
4. Isi form (tanggal, jam mulai, jam selesai, alasan)
5. Kirim pengajuan untuk approval

## Keamanan

- Password di-hash menggunakan Werkzeug
- Session management dengan Flask
- Role-based access control
- Audit log untuk semua aktivitas penting
- Validasi lokasi untuk presensi
- Validasi waktu untuk presensi

## Troubleshooting

### Error Koneksi Database

Pastikan:
- SQL Server sudah berjalan
- ODBC Driver 17 for SQL Server sudah terinstall
- Kredensial database benar
- Database sudah dibuat

### Error Geolocation

- Pastikan browser mendukung Geolocation API
- Izinkan akses lokasi di browser
- Pastikan koordinat kantor sudah benar di config.py

## Lisensi

Proyek ini dibuat untuk keperluan akademik dan implementasi di perusahaan.

## Kontribusi

Silakan buat issue atau pull request untuk perbaikan dan fitur baru.
