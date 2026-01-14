# ✅ Setup Database Selesai!

Aplikasi Sistem Presensi Karyawan sudah berhasil di-setup dengan database SQL Server yang sesungguhnya.

## 🎉 Status Setup

- ✅ Database `AbsensiDB` sudah dibuat
- ✅ Semua tabel sudah dibuat
- ✅ User default sudah dibuat
- ✅ Aplikasi sedang berjalan di **http://localhost:5000**

## 🔑 Default Login

Setelah setup, gunakan kredensial berikut untuk login:

### Admin

- **Username**: `admin`
- **Password**: `admin123`

### HRD

- **Username**: `hrd`
- **Password**: `hrd123`

⚠️ **PENTING**: Ganti password default setelah login pertama kali!

## 🌐 Mengakses Aplikasi

Buka browser dan kunjungi: **http://localhost:5000**

## 📋 Fitur yang Tersedia

### Untuk Semua Role:

- ✅ Dashboard dengan statistik
- ✅ Presensi (Check-in & Check-out)
- ✅ Pengajuan Timeoff
- ✅ Pengajuan Lembur
- ✅ Notifikasi

### Untuk Admin:

- ✅ Manajemen Data Karyawan (CRUD)
- ✅ Import/Export Data Karyawan
- ✅ Audit Log
- ✅ Manajemen User

### Untuk HRD:

- ✅ Manajemen Data Karyawan (CRUD)
- ✅ Import/Export Data Karyawan
- ✅ Approval Timeoff
- ✅ Approval Lembur

### Untuk Atasan:

- ✅ Approval Timeoff
- ✅ Approval Lembur
- ✅ Lihat Data Karyawan Bawahan

### Untuk Karyawan:

- ✅ Presensi dengan Geolocation
- ✅ Pengajuan Timeoff
- ✅ Pengajuan Lembur
- ✅ Lihat Riwayat Presensi

## 🚀 Menjalankan Aplikasi di Masa Depan

### Opsi 1: Menggunakan Script PowerShell (Recommended)

```powershell
.\run_app.ps1
```

### Opsi 2: Manual

```powershell
# Set environment variables
$env:USE_WINDOWS_AUTH="true"
$env:SQL_SERVER="localhost"
$env:DATABASE_NAME="AbsensiDB"
$env:DEMO_MODE="false"

# Jalankan aplikasi
python app.py
```

## 🔧 Setup Ulang Database

Jika perlu setup ulang database, jalankan:

```powershell
.\setup_database.ps1
```

## 📁 Struktur Database

Database `AbsensiDB` berisi tabel-tabel berikut:

- `users` - Data user untuk login
- `employees` - Data karyawan
- `attendances` - Data presensi
- `leave_requests` - Data pengajuan Timeoff
- `overtimes` - Data pengajuan lembur
- `notifications` - Data notifikasi
- `audit_logs` - Log aktivitas sistem

## ⚙️ Konfigurasi

Konfigurasi aplikasi dapat diubah di file `config.py`:

- **Jam Presensi**: `CHECK_IN_START`, `CHECK_IN_END`, `CHECK_OUT_START`, `CHECK_OUT_END`
- **Lokasi Kantor**: `OFFICE_LATITUDE`, `OFFICE_LONGITUDE`, `GEO_RADIUS_METERS`
- **Upload File**: `UPLOAD_FOLDER`, `MAX_UPLOAD_SIZE`, `ALLOWED_EXTENSIONS`

## 🐛 Troubleshooting

### Error: Database tidak ditemukan

```powershell
# Buat database manual
sqlcmd -S localhost -Q "CREATE DATABASE AbsensiDB" -E

# Atau jalankan setup ulang
.\setup_database.ps1
```

### Error: Port 5000 sudah digunakan

Ubah port di `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Ganti port
```

### Error: Koneksi database gagal

1. Pastikan SQL Server sudah berjalan
2. Pastikan ODBC Driver 17 for SQL Server sudah terinstall
3. Cek konfigurasi di `config.py` atau environment variables

## 📝 Catatan Penting

1. **Data Real**: Semua data yang dimasukkan akan tersimpan di database SQL Server
2. **Geolocation**: Presensi memerlukan izin akses lokasi di browser
3. **Session**: Session akan expire setelah 8 jam tidak aktif
4. **Backup**: Lakukan backup database secara berkala

## 🎯 Next Steps

1. Login dengan user default
2. Ganti password default
3. Tambah data karyawan (untuk Admin/HRD)
4. Buat user baru untuk karyawan
5. Mulai menggunakan sistem presensi

---

**Selamat menggunakan Sistem Presensi Karyawan!** 🎉
